#!/usr/bin/env python3
"""Deterministic media, timeline, render, and Final Cut helpers for video-editor."""

from __future__ import annotations

import argparse
import html
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote


class EditError(Exception):
    pass


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def ffmpeg_has_filter(name: str) -> bool:
    result = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, check=True)
    return any(line.split()[1:2] == [name] for line in result.stdout.splitlines() if line.strip())


def ffprobe(path: Path) -> dict:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)
    ], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def media_summary(path: Path) -> dict:
    data = ffprobe(path)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    duration = float(data.get("format", {}).get("duration") or (video or {}).get("duration") or 0)
    return {
        "path": str(path.resolve()),
        "duration": round(duration, 6),
        "size_bytes": int(data.get("format", {}).get("size") or path.stat().st_size),
        "video": None if not video else {
            "codec": video.get("codec_name"), "width": video.get("width"), "height": video.get("height"),
            "fps": video.get("avg_frame_rate"), "rotation": (video.get("tags") or {}).get("rotate"),
        },
        "audio": None if not audio else {
            "codec": audio.get("codec_name"), "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"),
        },
    }


def load_edit(path: Path) -> tuple[dict, Path]:
    try:
        edit = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise EditError(f"cannot read {path}: {exc}") from exc
    return edit, path.resolve().parent


def resolved_sources(edit: dict, base: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for source in edit.get("sources", []):
        source_id = source.get("id")
        if not source_id or source_id in result:
            raise EditError(f"source ids must be non-empty and unique: {source_id!r}")
        path = Path(source.get("path", ""))
        if not path.is_absolute():
            path = (base / path).resolve()
        result[source_id] = {**source, "resolved_path": path}
    return result


def validate(edit: dict, base: Path, require_files: bool = True) -> tuple[dict[str, dict], float]:
    errors: list[str] = []
    if edit.get("version") != 1:
        errors.append("version must be 1")
    project = edit.get("project") or {}
    for key in ("name", "profile", "width", "height", "fps"):
        if key not in project:
            errors.append(f"project.{key} is required")
    if not isinstance(project.get("width"), int) or project.get("width", 0) <= 0:
        errors.append("project.width must be a positive integer")
    if not isinstance(project.get("height"), int) or project.get("height", 0) <= 0:
        errors.append("project.height must be a positive integer")
    if not isinstance(project.get("fps"), (int, float)) or project.get("fps", 0) <= 0:
        errors.append("project.fps must be positive")

    try:
        sources = resolved_sources(edit, base)
    except EditError as exc:
        errors.append(str(exc))
        sources = {}
    if not sources:
        errors.append("at least one source is required")
    if require_files:
        for source_id, source in sources.items():
            if not source["resolved_path"].is_file():
                errors.append(f"source {source_id} does not exist: {source['resolved_path']}")

    duration = 0.0
    clip_ids: set[str] = set()
    clips = edit.get("clips") or []
    if not clips:
        errors.append("at least one clip is required")
    for index, clip in enumerate(clips):
        label = f"clips[{index}]"
        clip_id = clip.get("id")
        if not clip_id or clip_id in clip_ids:
            errors.append(f"{label}.id must be non-empty and unique")
        clip_ids.add(clip_id)
        if clip.get("source") not in sources:
            errors.append(f"{label}.source is unknown: {clip.get('source')!r}")
        start, end = clip.get("in"), clip.get("out")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < 0 or end <= start:
            errors.append(f"{label} requires out > in >= 0")
            continue
        known = sources.get(clip.get("source"), {}).get("duration")
        if isinstance(known, (int, float)) and end > known + 0.05:
            errors.append(f"{label}.out {end} exceeds source duration {known}")
        if clip.get("fit", "fit") not in ("fit", "fill"):
            errors.append(f"{label}.fit must be fit or fill")
        duration += end - start

    previous = -1.0
    for index, caption in enumerate(edit.get("captions") or []):
        start, end = caption.get("start"), caption.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < 0 or end <= start:
            errors.append(f"captions[{index}] requires end > start >= 0")
            continue
        if start < previous:
            errors.append("captions must be ordered by start time")
        if end > duration + 0.05:
            errors.append(f"captions[{index}] exceeds output duration {duration:.3f}")
        if not str(caption.get("text", "")).strip():
            errors.append(f"captions[{index}].text is empty")
        previous = start

    if errors:
        raise EditError("invalid edit:\n- " + "\n- ".join(errors))
    return sources, duration


def timestamp_srt(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def timestamp_ass(seconds: float) -> str:
    centis = round(seconds * 100)
    hours, centis = divmod(centis, 360_000)
    minutes, centis = divmod(centis, 6_000)
    secs, centis = divmod(centis, 100)
    return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"


def ass_color(value: str) -> str:
    value = value.lstrip("#")
    if len(value) != 6:
        raise EditError(f"invalid caption color: {value!r}")
    return f"&H00{value[4:6]}{value[2:4]}{value[0:2]}"


def escape_ass(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def write_captions(edit: dict, workspace: Path) -> tuple[Path, Path]:
    captions = edit.get("captions") or []
    srt = workspace / "captions.srt"
    srt.write_text("\n\n".join(
        f"{index}\n{timestamp_srt(float(item['start']))} --> {timestamp_srt(float(item['end']))}\n{item['text']}"
        for index, item in enumerate(captions, 1)
    ) + ("\n" if captions else ""))

    project = edit["project"]
    style = project.get("caption_style") or {}
    width, height = project["width"], project["height"]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style.get('font', 'Helvetica Neue')},{style.get('font_size', 58)},{ass_color(style.get('primary_color', '#FFFFFF'))},{ass_color(style.get('highlight_color', '#FFD84D'))},{ass_color(style.get('outline_color', '#111111'))},&H00000000,-1,0,0,0,100,100,0,0,1,{style.get('outline_width', 4)},0,2,80,80,{style.get('margin_v', 180)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for item in captions:
        text = escape_ass(str(item["text"]))
        highlight = str(item.get("highlight", "")).strip()
        if highlight and highlight.lower() in str(item["text"]).lower():
            start_index = str(item["text"]).lower().index(highlight.lower())
            end_index = start_index + len(highlight)
            raw = str(item["text"])
            color = ass_color(style.get("highlight_color", "#FFD84D"))
            text = escape_ass(raw[:start_index]) + r"{\c" + color + "}" + escape_ass(raw[start_index:end_index]) + r"{\r}" + escape_ass(raw[end_index:])
        lines.append(f"Dialogue: 0,{timestamp_ass(float(item['start']))},{timestamp_ass(float(item['end']))},Default,,0,0,0,,{text}")
    ass = workspace / "captions.ass"
    ass.write_text(header + "\n".join(lines) + ("\n" if lines else ""))
    return srt, ass


def build_filter(edit: dict, sources: dict[str, dict]) -> tuple[list[Path], str]:
    project = edit["project"]
    width, height, fps = project["width"], project["height"], project["fps"]
    input_paths: list[Path] = []
    input_index: dict[str, int] = {}
    has_audio: dict[str, bool] = {}
    for clip in edit["clips"]:
        source_id = clip["source"]
        if source_id not in input_index:
            input_index[source_id] = len(input_paths)
            path = sources[source_id]["resolved_path"]
            input_paths.append(path)
            has_audio[source_id] = media_summary(path)["audio"] is not None

    filters: list[str] = []
    concat_parts: list[str] = []
    for idx, clip in enumerate(edit["clips"]):
        source_id = clip["source"]
        source_idx = input_index[source_id]
        start, end = float(clip["in"]), float(clip["out"])
        duration = end - start
        if clip.get("fit", "fit") == "fill":
            sizing = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
        else:
            sizing = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"
        filters.append(
            f"[{source_idx}:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,{sizing},fps={fps},setsar=1,format=yuv420p[v{idx}]"
        )
        fade = min(0.03, duration / 4)
        volume = float(clip.get("volume_db", 0))
        if has_audio[source_id]:
            audio_input = f"[{source_idx}:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS"
        else:
            audio_input = f"anullsrc=r=48000:cl=stereo,atrim=duration={duration}"
        filters.append(
            f"{audio_input},aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={volume}dB,afade=t=in:st=0:d={fade},afade=t=out:st={max(0, duration-fade)}:d={fade}[a{idx}]"
        )
        concat_parts.append(f"[v{idx}][a{idx}]")
    filters.append("".join(concat_parts) + f"concat=n={len(edit['clips'])}:v=1:a=1[vout][aout]")
    return input_paths, ";".join(filters)


def render(edit_path: Path, workspace: Path) -> None:
    edit, base = load_edit(edit_path)
    sources, _ = validate(edit, base)
    workspace.mkdir(parents=True, exist_ok=True)
    _, ass = write_captions(edit, workspace)
    input_paths, filter_complex = build_filter(edit, sources)
    inputs: list[str] = []
    for path in input_paths:
        inputs.extend(["-i", str(path)])
    clean = workspace / "clean-master.mp4"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", *inputs,
        "-filter_complex", filter_complex, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(clean),
    ])
    final = workspace / "final.mp4"
    if edit.get("captions"):
        if ffmpeg_has_filter("ass"):
            ass_filter_path = str(ass.resolve()).replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", str(clean),
                "-vf", f"ass=filename='{ass_filter_path}'", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-c:a", "copy", "-movflags", "+faststart", str(final),
            ])
        else:
            caption_renderer = Path(__file__).resolve().parent / "caption_png.swift"
            swift = shutil.which("swift")
            if not swift or not caption_renderer.is_file():
                raise EditError("ffmpeg lacks the ass filter and the macOS Swift caption renderer is unavailable")
            caption_dir = workspace / "generated" / "captions"
            caption_dir.mkdir(parents=True, exist_ok=True)
            style = edit["project"].get("caption_style") or {}
            pngs: list[Path] = []
            for index, caption in enumerate(edit["captions"]):
                png = caption_dir / f"caption-{index:04}.png"
                run([
                    swift, str(caption_renderer), str(png), str(edit["project"]["width"]), str(edit["project"]["height"]),
                    str(caption["text"]), str(style.get("font", "Helvetica Neue")), str(style.get("font_size", 58)),
                    str(style.get("primary_color", "#FFFFFF")), str(caption.get("highlight", "")),
                    str(style.get("highlight_color", "#FFD84D")), str(style.get("outline_color", "#111111")),
                    str(style.get("outline_width", 4)), str(style.get("margin_v", 180)),
                ])
                pngs.append(png)
            inputs = ["-i", str(clean)]
            for png in pngs:
                inputs.extend(["-loop", "1", "-i", str(png)])
            filters: list[str] = []
            previous = "[0:v]"
            for index, caption in enumerate(edit["captions"], 1):
                output_label = f"[captioned{index}]"
                filters.append(f"{previous}[{index}:v]overlay=0:0:enable='between(t,{float(caption['start'])},{float(caption['end'])})'{output_label}")
                previous = output_label
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", *inputs,
                "-filter_complex", ";".join(filters), "-map", previous, "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "copy", "-shortest",
                "-movflags", "+faststart", str(final),
            ])
    else:
        shutil.copy2(clean, final)
    preview = workspace / "preview.mp4"
    preview_width = min(1280, int(edit["project"]["width"]))
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", str(final),
        "-vf", f"scale={preview_width}:-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "29",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(preview),
    ])
    print(f"rendered {clean}\nrendered {final}\nrendered {preview}")


def frame_time(seconds: float, fps: float) -> str:
    frames = round(seconds * fps)
    if math.isclose(fps, round(fps)):
        return f"{frames}/{round(fps)}s"
    denominator = 30_000 if math.isclose(fps, 29.97, abs_tol=0.01) else 24_000
    numerator = round(frames * denominator / fps)
    return f"{numerator}/{denominator}s"


def file_uri(path: Path) -> str:
    return "file://" + quote(str(path.resolve()), safe="/")


def fcpxml_color(value: str, alpha: float = 1) -> str:
    cleaned = value.lstrip("#")
    if len(cleaned) != 6:
        raise EditError(f"invalid color: {value!r}")
    channels = [int(cleaned[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    return " ".join(f"{channel:.6g}" for channel in [*channels, alpha])


def fcpxml_caption(caption: dict, offset: float, duration: float, fps: float, style: dict, style_id: str) -> str:
    raw = str(caption["text"])
    highlight = str(caption.get("highlight", "")).strip()
    primary = fcpxml_color(style.get("primary_color", "#FFFFFF"))
    highlighted = fcpxml_color(style.get("highlight_color", "#FFD84D"))
    background = fcpxml_color(style.get("outline_color", "#111111"), 0.72)
    text_parts: list[str]
    style_defs = [
        f'<text-style-def id="{style_id}"><text-style fontFace="Regular" fontColor="{primary}" backgroundColor="{background}"/></text-style-def>'
    ]
    if highlight and highlight.lower() in raw.lower():
        start_index = raw.lower().index(highlight.lower())
        end_index = start_index + len(highlight)
        highlight_id = f"{style_id}h"
        text_parts = []
        if raw[:start_index]:
            text_parts.append(f'<text-style ref="{style_id}">{html.escape(raw[:start_index])}</text-style>')
        text_parts.append(f'<text-style ref="{highlight_id}">{html.escape(raw[start_index:end_index])}</text-style>')
        if raw[end_index:]:
            text_parts.append(f'<text-style ref="{style_id}">{html.escape(raw[end_index:])}</text-style>')
        style_defs.append(
            f'<text-style-def id="{highlight_id}"><text-style fontFace="Regular" fontColor="{highlighted}" backgroundColor="{background}" bold="1"/></text-style-def>'
        )
    else:
        text_parts = [f'<text-style ref="{style_id}">{html.escape(raw)}</text-style>']
    return (
        f'<caption name="{html.escape(raw)}" lane="1" offset="{frame_time(offset, fps)}" duration="{frame_time(duration, fps)}" '
        'role="Video Editor Captions?captionFormat=ITT.en">'
        f'<text placement="bottom">{"".join(text_parts)}</text>{"".join(style_defs)}</caption>'
    )


def fcpxml(edit_path: Path, output: Path) -> None:
    edit, base = load_edit(edit_path)
    sources, total_duration = validate(edit, base)
    project = edit["project"]
    fps = float(project["fps"])
    resources = [
        f'<format id="r1" name="FFVideoFormat{project["width"]}x{project["height"]}p{fps:g}" frameDuration="{frame_time(1/fps, fps)}" width="{project["width"]}" height="{project["height"]}" colorSpace="1-1-1 (Rec. 709)"/>'
    ]
    source_refs: dict[str, str] = {}
    for index, (source_id, source) in enumerate(sources.items(), 2):
        ref = f"r{index}"
        source_refs[source_id] = ref
        duration = float(source.get("duration") or media_summary(source["resolved_path"])["duration"])
        info = media_summary(source["resolved_path"])
        attrs = [f'id="{ref}"', f'name="{html.escape(source["resolved_path"].name)}"', f'duration="{frame_time(duration, fps)}"', 'start="0s"']
        if info["video"]:
            attrs.extend(['hasVideo="1"', 'format="r1"'])
        if info["audio"]:
            attrs.extend(['hasAudio="1"', 'audioSources="1"', f'audioChannels="{info["audio"]["channels"] or 2}"', f'audioRate="{info["audio"]["sample_rate"] or 48000}"'])
        resources.append(
            f'<asset {" ".join(attrs)}><media-rep kind="original-media" src="{file_uri(source["resolved_path"])}"/></asset>'
        )

    timeline = 0.0
    clip_xml: list[str] = []
    caption_counter = 0
    caption_style = project.get("caption_style") or {}
    for clip in edit["clips"]:
        duration = float(clip["out"]) - float(clip["in"])
        name = html.escape(clip.get("id") or sources[clip["source"]]["resolved_path"].name)
        volume = float(clip.get("volume_db", 0))
        position = clip.get("position", [0, 0])
        scale = float(clip.get("scale", 1))
        rotation = float(clip.get("rotation", 0))
        adjustments = [f'<adjust-conform type="{clip.get("fit", "fit")}"/>']
        if position != [0, 0] or scale != 1 or rotation:
            adjustments.append(f'<adjust-transform position="{float(position[0]):g} {float(position[1]):g}" scale="{scale:g} {scale:g}" rotation="{rotation:g}"/>')
        if volume:
            adjustments.append(f'<adjust-volume amount="{volume:g}dB"/>')
        caption_xml: list[str] = []
        clip_end = timeline + duration
        for caption in edit.get("captions") or []:
            overlap_start = max(timeline, float(caption["start"]))
            overlap_end = min(clip_end, float(caption["end"]))
            if overlap_end <= overlap_start:
                continue
            caption_counter += 1
            source_offset = float(clip["in"]) + (overlap_start - timeline)
            caption_xml.append(fcpxml_caption(
                caption, source_offset, overlap_end - overlap_start, fps, caption_style, f"ts{caption_counter}"
            ))
        clip_xml.append(
            f'<asset-clip name="{name}" ref="{source_refs[clip["source"]]}" offset="{frame_time(timeline, fps)}" start="{frame_time(float(clip["in"]), fps)}" duration="{frame_time(duration, fps)}" audioRole="dialogue">'
            + "".join(adjustments) + "".join(caption_xml) + '</asset-clip>'
        )
        timeline += duration

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>{''.join(resources)}</resources>
  <library>
    <event name="Video Editor">
      <project name="{html.escape(str(project['name']))}">
        <sequence format="r1" duration="{frame_time(total_duration, fps)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>{''.join(clip_xml)}</spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(xml)
    print(f"wrote {output}")


def report(edit_path: Path, output: Path) -> None:
    edit, base = load_edit(edit_path)
    sources, duration = validate(edit, base, require_files=False)
    lines = [
        f"# {edit['project']['name']} — edit report", "",
        f"- Profile: `{edit['project']['profile']}`",
        f"- Canvas: {edit['project']['width']}×{edit['project']['height']} at {edit['project']['fps']} fps",
        f"- Output duration: {duration:.3f}s", f"- Clips: {len(edit['clips'])}",
        f"- Captions: {len(edit.get('captions') or [])}", "", "## Sources", "",
    ]
    for source_id, source in sources.items():
        lines.append(f"- `{source_id}`: `{source.get('path')}` ({source.get('origin', 'unknown')})")
    lines.extend(["", "## Editorial decisions", ""])
    for clip in edit["clips"]:
        lines.append(f"- `{clip['id']}`: {clip.get('reason', 'No reason recorded')}")
    lines.extend(["", "## Semantic edits", ""])
    semantic = edit.get("semantic_edits") or []
    lines.extend(f"- {item.get('type', 'edit')}: {item.get('description', '')}" for item in semantic)
    if not semantic:
        lines.append("- None recorded.")
    lines.extend(["", "## Warnings and approximations", ""])
    warnings = edit.get("warnings") or []
    lines.extend(f"- {warning}" for warning in warnings)
    if not warnings:
        lines.append("- None recorded.")
    lines.extend(["", "## Verification", "", "- [ ] Full rendered video inspected", "- [ ] Every cut checked visually and audibly", "- [ ] Captions checked", "- [ ] Final Cut XML imported and editability checked", ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))
    print(f"wrote {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    probe_parser = sub.add_parser("probe", help="inventory media with ffprobe")
    probe_parser.add_argument("sources", nargs="+", type=Path)
    probe_parser.add_argument("--output", type=Path, required=True)

    sheet_parser = sub.add_parser("contact-sheet", help="extract a targeted frame contact sheet")
    sheet_parser.add_argument("source", type=Path)
    sheet_parser.add_argument("--output", type=Path, required=True)
    sheet_parser.add_argument("--start", type=float, default=0)
    sheet_parser.add_argument("--duration", type=float)
    sheet_parser.add_argument("--frames", type=int, default=12)
    sheet_parser.add_argument("--columns", type=int, default=4)
    sheet_parser.add_argument("--tile-width", type=int, default=320)

    validate_parser = sub.add_parser("validate", help="validate canonical edit JSON")
    validate_parser.add_argument("edit", type=Path)

    render_parser = sub.add_parser("render", help="render clean, captioned, and preview MP4s")
    render_parser.add_argument("edit", type=Path)
    render_parser.add_argument("--workspace", type=Path)

    fcpxml_parser = sub.add_parser("fcpxml", help="export an editable Final Cut timeline")
    fcpxml_parser.add_argument("edit", type=Path)
    fcpxml_parser.add_argument("--output", type=Path, required=True)

    report_parser = sub.add_parser("report", help="write a human-readable edit report")
    report_parser.add_argument("edit", type=Path)
    report_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    try:
        if args.command == "probe":
            items = []
            for path in args.sources:
                if not path.is_file():
                    raise EditError(f"source does not exist: {path}")
                items.append(media_summary(path))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps({"media": items}, indent=2) + "\n")
            print(f"wrote {args.output}")
        elif args.command == "contact-sheet":
            if not args.source.is_file():
                raise EditError(f"source does not exist: {args.source}")
            duration = args.duration or max(0.1, media_summary(args.source)["duration"] - args.start)
            rows = math.ceil(args.frames / args.columns)
            interval = args.frames / duration
            args.output.parent.mkdir(parents=True, exist_ok=True)
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(args.start), "-t", str(duration),
                "-i", str(args.source), "-vf", f"fps={interval},scale={args.tile_width}:-2,tile={args.columns}x{rows}:nb_frames={args.frames}:padding=4:margin=4",
                "-frames:v", "1", str(args.output),
            ])
            print(f"wrote {args.output}")
        elif args.command == "validate":
            edit, base = load_edit(args.edit)
            _, duration = validate(edit, base)
            print(f"valid edit: {len(edit['clips'])} clips, {duration:.3f}s")
        elif args.command == "render":
            render(args.edit, args.workspace or args.edit.resolve().parent)
        elif args.command == "fcpxml":
            fcpxml(args.edit, args.output)
        elif args.command == "report":
            report(args.edit, args.output)
    except (EditError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

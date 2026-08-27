#!/usr/bin/env python3
"""Representative end-to-end smoke test for video-editor helpers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from contextlib import nullcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER = HERE / "video_editor.py"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def duration(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)
    ], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", type=Path, help="Keep the generated fixture in this directory")
    args = parser.parse_args()
    if args.keep:
        args.keep.mkdir(parents=True, exist_ok=True)
        context = nullcontext(str(args.keep.resolve()))
    else:
        context = tempfile.TemporaryDirectory(prefix="video-editor-test-")
    with context as tmp:
        root = Path(tmp)
        source = root / "source.mp4"
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=4",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(source),
        ])
        edit = {
            "version": 1,
            "project": {
                "name": "Video Editor Smoke Test", "profile": "talking-head",
                "width": 640, "height": 360, "fps": 30,
                "caption_style": {"font_size": 28, "margin_v": 36},
            },
            "sources": [{"id": "source", "path": "source.mp4", "origin": "generated", "duration": 4}],
            "clips": [
                {"id": "first", "source": "source", "in": 0.5, "out": 1.5, "fit": "fill", "volume_db": -1, "reason": "First chosen take"},
                {"id": "second", "source": "source", "in": 2.0, "out": 3.5, "fit": "fit", "volume_db": 0, "reason": "Second chosen take"},
            ],
            "captions": [
                {"start": 0, "end": 1.3, "text": "This caption crosses the cut", "highlight": "crosses"},
                {"start": 1.3, "end": 2.4, "text": "Then comes the proof"},
            ],
            "semantic_edits": [], "warnings": [],
        }
        edit_path = root / "edit.json"
        edit_path.write_text(json.dumps(edit, indent=2) + "\n")
        run([sys.executable, str(HELPER), "probe", str(source), "--output", str(root / "media.json")])
        run([sys.executable, str(HELPER), "contact-sheet", str(source), "--output", str(root / "sheet.jpg"), "--frames", "8"])
        run([sys.executable, str(HELPER), "validate", str(edit_path)])
        run([sys.executable, str(HELPER), "render", str(edit_path), "--workspace", str(root)])
        run([sys.executable, str(HELPER), "fcpxml", str(edit_path), "--output", str(root / "project.fcpxml")])
        run([sys.executable, str(HELPER), "report", str(edit_path), "--output", str(root / "edit-report.md")])
        run(["xmllint", "--noout", str(root / "project.fcpxml")])

        xml_root = ET.parse(root / "project.fcpxml").getroot()
        assets = xml_root.findall("./resources/asset")
        if len(assets) != 1 or assets[0].find("media-rep") is None or "src" in assets[0].attrib:
            raise AssertionError("FCPXML assets must use FCPXML 1.10 media-rep elements")
        if len(xml_root.findall(".//asset-clip")) != 2:
            raise AssertionError("FCPXML clip count differs from the canonical timeline")
        if len(xml_root.findall(".//caption")) != 3:
            raise AssertionError("FCPXML captions were not split and preserved across clip boundaries")

        expected = ["media.json", "sheet.jpg", "captions.srt", "captions.ass", "clean-master.mp4", "final.mp4", "preview.mp4", "project.fcpxml", "edit-report.md"]
        missing = [name for name in expected if not (root / name).is_file() or (root / name).stat().st_size == 0]
        if missing:
            raise AssertionError(f"missing outputs: {missing}")
        if abs(duration(root / "final.mp4") - 2.5) > 0.15:
            raise AssertionError("rendered duration differs from the canonical timeline")
        print("video-editor smoke test passed")
        if args.keep:
            print(f"fixture kept at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Transcribe video/audio with ElevenLabs Scribe or local Whisper."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def transcribe_elevenlabs(source: Path, output: Path, key: str) -> None:
    with tempfile.TemporaryDirectory(prefix="video-editor-stt-") as tmp:
        audio = Path(tmp) / "audio.m4a"
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-vn", "-ac", "1", "-ar", "16000", "-c:a", "aac", "-b:a", "96k", str(audio),
        ])
        command = [
            "curl", "--silent", "--show-error", "--fail-with-body",
            "https://api.elevenlabs.io/v1/speech-to-text",
            "--config", "-",
            "-F", f"file=@{audio}",
            "-F", "model_id=scribe_v2",
            "-F", "timestamps_granularity=word",
            "-F", "diarize=true",
            "-F", "tag_audio_events=true",
        ]
        # Feed the secret through stdin so it never appears in the process argument list.
        result = subprocess.run(
            command, check=True, capture_output=True, text=True,
            input=f'header = "xi-api-key: {key}"\n',
        )
        payload = json.loads(result.stdout)
        payload["_video_editor"] = {"provider": "elevenlabs", "source": str(source.resolve())}
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def transcribe_whisper(source: Path, output: Path, model: str) -> None:
    whisper = shutil.which("whisper")
    if not whisper:
        raise RuntimeError("local Whisper is unavailable; install the `whisper` CLI or configure ELEVENLABS_API_KEY")
    with tempfile.TemporaryDirectory(prefix="video-editor-whisper-") as tmp:
        run([
            whisper, str(source), "--model", model, "--output_format", "json",
            "--word_timestamps", "True", "--output_dir", tmp,
        ])
        generated = Path(tmp) / f"{source.stem}.json"
        payload = json.loads(generated.read_text())
        payload["_video_editor"] = {"provider": "whisper", "source": str(source.resolve())}
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider", choices=("auto", "elevenlabs", "whisper"), default="auto")
    parser.add_argument("--sensitive", action="store_true", help="Force local transcription")
    parser.add_argument("--whisper-model", default="turbo")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"source does not exist: {args.source}")
    if not shutil.which("ffmpeg"):
        parser.error("ffmpeg is required")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    key = os.environ.get("ELEVENLABS_API_KEY")
    provider = "whisper" if args.sensitive else args.provider
    if provider == "auto":
        provider = "elevenlabs" if key else "whisper"
    if provider == "elevenlabs" and not key:
        parser.error("ELEVENLABS_API_KEY is required for provider=elevenlabs")

    try:
        if provider == "elevenlabs":
            transcribe_elevenlabs(args.source, args.output, key or "")
        else:
            transcribe_whisper(args.source, args.output, args.whisper_model)
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"transcription failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {provider} transcript: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

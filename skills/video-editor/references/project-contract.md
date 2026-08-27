# Project contract

Read this before creating, resuming, validating, rendering, or exporting a project.

## Workspace

```text
edit/
├── project.md
├── media.json
├── edit.json
├── transcripts/
├── sources/          # retrieved remote sources only
├── inspect/          # contact sheets and cut checks
├── generated/        # generated overlay/title assets
├── verify/           # review artifacts
├── captions.srt
├── captions.ass
├── preview.mp4
├── final.mp4
├── clean-master.mp4
├── project.fcpxml
└── edit-report.md
```

The input folder does not need this shape. Create the workspace wherever it is safe and practical. Never write generated files over source media.

## Canonical `edit.json`

All times are seconds on source or output timelines. Paths resolve relative to `edit.json` unless absolute.

```json
{
  "version": 1,
  "project": {
    "name": "Launch video",
    "profile": "short-form",
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "caption_style": {
      "font": "Helvetica Neue",
      "font_size": 58,
      "primary_color": "#FFFFFF",
      "highlight_color": "#FFD84D",
      "outline_color": "#111111",
      "outline_width": 4,
      "margin_v": 180
    }
  },
  "sources": [
    {
      "id": "camera",
      "path": "../camera.mov",
      "origin": "local",
      "duration": 120.4
    }
  ],
  "clips": [
    {
      "id": "clip-001",
      "source": "camera",
      "in": 4.2,
      "out": 9.8,
      "fit": "fill",
      "position": [0, 0],
      "scale": 1.0,
      "rotation": 0,
      "volume_db": 0,
      "reason": "Immediate hook"
    }
  ],
  "captions": [
    {"start": 0.0, "end": 1.8, "text": "I stopped editing this by hand.", "highlight": "stopped"}
  ],
  "semantic_edits": [
    {"type": "reorder", "description": "Moved the result before the explanation", "source_clips": ["clip-003", "clip-001"]}
  ],
  "warnings": []
}
```

## Rules

- `version` must be `1`.
- `sources[].id` and `clips[].id` must be unique.
- `clips` defines output order. A clip needs `out > in >= 0` and must not exceed known source duration.
- `fit` is `fit` (letterbox/pillarbox) or `fill` (crop to canvas).
- `position`, `scale`, and `rotation` are preserved for Final Cut. The portable renderer currently guarantees `fit`, scale-to-canvas, cuts, audio gain, fades, and captions; record any advanced-render approximation.
- Captions use output time, must be ordered, and must fit within total output duration.
- Always include captions for spoken content. Empty captions are valid only for silent footage and need a warning explaining why.
- Record narrative reorders, sentence surgery, and hidden continuity changes in `semantic_edits`.
- Register complex overlays as source assets/clips when practical. This keeps them replaceable in Final Cut.

## `project.md`

Append, do not overwrite, across sessions. Record source provenance, approved strategy, profile and reference traits, style overrides, render attempts, review findings, unresolved issues, and the exact delivered files.

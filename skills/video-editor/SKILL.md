---
name: video-editor
description: Autonomously edit existing video footage into polished captioned videos and editable Final Cut Pro timelines. Use for talking-head recordings, interviews, screen-recorded app demos, short-form social videos, general footage, rough cuts, filler removal, reframing, captions, overlays, pacing, audio cleanup, reference-video matching, or requests to turn raw clips into an MP4/FCPXML project.
---

# Video Editor

Edit existing footage as an opinionated editorial collaborator. Preserve every source. Create a resumable workspace, propose the story and profile, wait for strategy approval, then execute and self-review autonomously.

## Non-negotiable contract

- Edit existing footage; do not generate replacement footage or decorative AI B-roll unless explicitly asked.
- Accept any legitimately retrievable source. Cache remote inputs and record their origin. Never bypass access controls.
- Keep source media untouched. Put generated state and output in a new `edit/` workspace beside the sources when practical, or in an explicitly chosen location.
- Always generate captions. Keep editable caption data and also burn captions into the delivery MP4.
- Use one `edit.json` timeline to generate matching rendered and Final Cut outputs.
- Preserve the speaker's intended meaning. You may combine takes, reorder arguments, and hide cuts, but never synthesize words or imply a false continuous statement. Record semantic reorders.
- Require approval for the edit strategy, not for routine execution. After approval, inspect, edit, render, repair, and persist without repeatedly asking.
- Run at most three render-repair loops. Report unresolved problems precisely.
- Treat code/tests as insufficient proof. Inspect the actual video and, when Final Cut output matters, import the FCPXML into Final Cut.

## Workflow

### 1. Resolve sources and workspace

Inventory local files, URLs, browser/cloud downloads, mounted media, or existing project assets. Use `yt-dlp` where appropriate. Copy or download remote sources into `edit/sources/`; local files may remain referenced in place. Record provenance in `project.md`.

Run:

```bash
python3 <skill-dir>/scripts/video_editor.py probe <sources...> --output <workspace>/media.json
```

Read [project-contract.md](references/project-contract.md) before creating `edit.json` or resuming an existing project.

### 2. Transcribe speech

Prefer ElevenLabs Scribe v2 because word timestamps, diarization, and preserved disfluencies drive accurate cuts. Keep `no_verbatim` disabled. Resolve `ELEVENLABS_API_KEY` from the environment; it should be backed by 1Password, never written into the workspace.

Use local Whisper automatically when the key is unavailable or the content is private, confidential, medical, financial, or client-sensitive:

```bash
python3 <skill-dir>/scripts/transcribe.py <source> --output <workspace>/transcripts/<name>.json
python3 <skill-dir>/scripts/transcribe.py <source> --sensitive --output <workspace>/transcripts/<name>.json
```

Do not upload sensitive footage without explicit authorization.

### 3. Inspect before proposing

Read transcripts for narrative structure. Use contact sheets for layout changes, take comparisons, app-state changes, ambiguous pauses, likely highlights, and candidate cut boundaries:

```bash
python3 <skill-dir>/scripts/video_editor.py contact-sheet <source> --output <workspace>/inspect/range.jpg --start 12 --duration 8
```

Do not extract every frame. Transcript-led inspection plus targeted frames is the default. Read [editorial-profiles.md](references/editorial-profiles.md), infer `talking-head`, `app-demo`, `short-form`, `interview`, or `general`, and propose:

- intended story and audience;
- chosen takes and meaningful removals/reorders;
- pacing, aspect ratio, captions, reframing, overlays, audio, and supplied music;
- likely compromises or missing assets.

Wait for strategy approval.

### 4. Build the canonical edit

Write `<workspace>/edit.json` following [project-contract.md](references/project-contract.md). Make every cut, caption, transform, audio decision, overlay asset, and semantic reorder explicit.

Validate before rendering:

```bash
python3 <skill-dir>/scripts/video_editor.py validate <workspace>/edit.json
```

Use supplied music and effects when useful. If none are supplied, finish strong dialogue and suggest missing sound design. Never download arbitrary music with uncertain rights.

### 5. Render all deliverables

```bash
python3 <skill-dir>/scripts/video_editor.py render <workspace>/edit.json --workspace <workspace>
python3 <skill-dir>/scripts/video_editor.py fcpxml <workspace>/edit.json --output <workspace>/project.fcpxml
python3 <skill-dir>/scripts/video_editor.py report <workspace>/edit.json --output <workspace>/edit-report.md
```

Always produce:

- `preview.mp4` — lightweight review render with captions;
- `final.mp4` — high-quality captioned delivery;
- `clean-master.mp4` — high-quality master without burned captions;
- `captions.srt` and `captions.ass` — editable and burned-caption sources;
- `project.fcpxml` — editable Final Cut timeline;
- `edit-report.md` — decisions, semantic changes, provenance, warnings, and verification.

Render only the inferred/requested primary aspect ratio. Suggest useful 9:16, 16:9, or 1:1 variants; render them only when requested because each needs independent reframing review.

### 6. Self-review the real output

Inspect the rendered video, not merely command success:

1. Extract contact sheets across the full result and around every cut.
2. Listen around every cut for pops, clipped phonemes, discontinuous room tone, and music jumps.
3. Check captions for transcription errors, safe-area violations, awkward chunks, and collisions.
4. Check reframing, overlays, app-state continuity, pacing, meaning, and export duration.
5. Repair and rerender up to three times.

Use restrained branded captions by default: sentence-aware chunks, phrase emphasis, safe-area placement, and no generic bouncing-word treatment. Explicit instructions and reference-video traits override the defaults. Persist durable project choices in `project.md`.

### 7. Verify Final Cut handoff

Maximize native FCPXML elements: cuts, order, audio levels/fades, transforms, crops, roles, markers, and captions. Bake only effects or animation assets that cannot be represented reliably, place those as editable clips, and list every approximation in the report.

Validate XML structurally every time. When completing a new workflow or changing the exporter, import `project.fcpxml` into Final Cut Pro and confirm media links, duration, clip order, editable cuts, captions, and transforms. Do not claim Final Cut success from XML parsing alone.

## Helper boundaries

- `video_editor.py` is deterministic infrastructure, not the editor. The agent owns story judgment and writes `edit.json`.
- The bundled renderer intentionally supports a conservative portable core. Use direct FFmpeg commands or intermediate overlay assets for advanced work, then keep the canonical timeline and report accurate.
- Keep secrets and cached credentials outside footage workspaces.

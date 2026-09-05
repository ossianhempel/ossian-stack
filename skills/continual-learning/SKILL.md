---
name: continual-learning
description: "Mine project session transcripts for recurring lessons and improve project instructions. Use only when explicitly requested."
disable-model-invocation: true
---

# Continual Learning

Turn what past sessions learned the hard way into instructions the next session
reads for free.

Prefer one subagent with its own context for mining, judgment, and edits so transcript volume stays out of the coordinating context. If the host has no subagents, read the same updater instructions and mine bounded transcript batches sequentially inline. Identify the fallback; do not claim independent context. Preserve the requested scope: an audit produces proposals, not edits or a successful-edit marker.

## Run it

1. **Resolve the transcript directory.** If a session-start notice named one, use
   it. Otherwise ask the host where its transcripts for this project live rather
   than guessing — the path differs per runtime and per project.
2. **Dispatch one subagent, or use the inline fallback,** with the contents of
   [`references/memory-updater.md`](references/memory-updater.md) as its
   instructions, plus the transcript directory path and the path to the project's
   agent instruction file. Give it paths, not transcript contents.
3. **Return its result unchanged.** Do not re-summarise it and do not editorialise
   the bullets it wrote. Its report ends with the arithmetic — removed, corrected,
   sharpened, added. If it added more than it removed or corrected, that is worth
   the user seeing, not smoothing over.
4. **Mark the mine.** On a successful run, touch the marker file the session-start
   notice named, so the nudge stops repeating. If no marker path was given, skip
   this — do not invent one.

## What this is for

The file should get **better**, not longer. Its value is that a future session
reads it in full and acts on it — which stops the moment it becomes a changelog of
everything anyone ever noticed.

So the bias is `principle-subtract-before-you-add`: remove and correct first,
sharpen second, append last. Short-lived, task-specific, or already-enforced facts
are the failure mode to guard against, not the material to collect.

## Guardrails

- Keep transcript contents in the subagent when available. The inline fallback
  uses the same durable-lesson filter and reports the same change arithmetic.
- Do not run unprompted in the middle of someone's task. A session-start notice is
  an invitation to offer, not permission to start.
- One subagent. Fanning out across transcripts loses the deduplication that makes
  the output worth reading.

---
name: continual-learning
description: "Mine this project's past session transcripts for durable lessons and fold them into the project's agent instructions, so the same correction is not needed twice. Use for mine my transcripts, run continual learning, update AGENTS.md from past sessions, or when a session-start notice says transcripts are unmined."
disable-model-invocation: true
---

# Continual Learning

Turn what past sessions learned the hard way into instructions the next session
reads for free.

This skill is orchestration only. The mining, the judgement about what is durable,
and the edit all happen in a subagent with its own context, because reading a pile
of transcripts is exactly the kind of work that should not fill this one.

## Run it

1. **Resolve the transcript directory.** If a session-start notice named one, use
   it. Otherwise ask the host where its transcripts for this project live rather
   than guessing — the path differs per runtime and per project.
2. **Dispatch one subagent** with the contents of
   [`references/memory-updater.md`](references/memory-updater.md) as its
   instructions, plus the transcript directory path and the path to the project's
   agent instruction file. Give it paths, not transcript contents.
3. **Return its result unchanged.** Do not re-summarise it and do not editorialise
   the bullets it wrote.
4. **Mark the mine.** On a successful run, touch the marker file the session-start
   notice named, so the nudge stops repeating. If no marker path was given, skip
   this — do not invent one.

## Guardrails

- Do not mine transcripts or edit files in this flow. That is the subagent's job,
  and keeping it there is the point.
- Do not run unprompted in the middle of someone's task. A session-start notice is
  an invitation to offer, not permission to start.
- One subagent. Fanning out across transcripts loses the deduplication that makes
  the output worth reading.

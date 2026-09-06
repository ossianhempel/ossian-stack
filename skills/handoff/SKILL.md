---
name: handoff
description: Pause work at a safe boundary or resume it from a durable handoff reconciled with live repository state.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

Choose pause mode when the user asks to stop safely or prepare another session.
Choose resume mode when asked to continue from a handoff, transcript, branch, PR,
or prior task.

## Pause

Finish the current atomic step or back it out. Start nothing new. Do not create a
commit, push, or PR solely to pause unless the user already authorized it. Save a
resume document in the operating system's temporary directory.

Record the goal and finish condition, inherited authority and boundaries,
branch/worktree and Git state, completed work and evidence, current blockers,
open decisions, key artifacts, the first executable next step, and suggested
skills. Link a `show-me-your-work` trail when present rather than duplicating it.

## Resume

Read the handoff overview first, then reconcile it with current Git status, diff,
recent commits, PR or tracker state, and linked evidence. Treat prior conclusions
as inherited context and current external state as authoritative. Do not redo
completed investigation or verification merely to rebuild confidence. Name the
resume point, route the remaining work to the matching skill, and verify the final
result against the original goal.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, use them as the next session's focus.

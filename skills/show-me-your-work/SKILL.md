---
name: show-me-your-work
description: "Keep and audit a compact evidence-linked decision trail for long-running or unattended work."
---

# Show Me Your Work

Create a reviewable trail when a task spans many consequential decisions or runs
while the user is away. Ordinary short work does not need a log.

Use `decisions.tsv` unless several runs share the repository; then use
`.audit/<task-slug>.tsv`. Keep it local by default. Commit it only when the trail
materially helps a reviewer trust an ambitious change.

Write a header and one append-only row per decision or checkpoint:

```text
time\tphase\tdecision\treason\tevidence\tresult
```

Each row fits on one line. Evidence points to a command output, artifact, commit,
PR, source location, or runtime observation. Record rejected attempts and pivots
that shaped the result. Supersede a wrong row with a later row; do not rewrite
history. Never put secrets or raw private transcript content in the log.

Before handoff, reconcile the trail with the current diff, Git state, task record,
and evidence files. Remove only invented or aspirational entries before the trail
has been shared; after it becomes a review artifact, correct with a superseding
row. Mark missing evidence as unverified.

When an independent reviewer is available and the stakes justify it, ask one to
inspect the trail and changed artifacts for weak evidence, skipped verification,
scope drift, or risky decisions. Review the findings yourself. Do not require a
review panel for routine work.

## Reply

Give the trail path, the definition of done, current phase, verified decisions,
reverted attempts, and an Attention section containing any weak or missing proof.

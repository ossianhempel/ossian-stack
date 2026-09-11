# Monitoring and recovery

HQ owns monitoring. An owner that never reports is HQ's problem to detect. While
any queue item is dispatching or active, use the runtime's wait, completion
notification, or a heartbeat of about fifteen minutes. The daily watchdog is only
a recovery backstop.

## Check-in gate

Before every status reply and before messaging, interrupting, renaming, replacing,
or archiving an owner:

1. Read its newest state and whether it has an active turn when the runtime allows.
2. Refresh the authoritative artifact when the report changed or the expected
   report time passed. For a PR, inspect checks, mergeability, reviews, comments,
   and unresolved inline threads through the repository host.
3. Compare its current queue item, authority, stop boundary, and proof contract.
4. Classify it as progressing, blocked, completed, idle, missing, or duplicated.

When owner state is unreadable, inspect its branch, PR, document, logs, or other
artifact. Message it only after the artifact is quiet past its expected report
time. A progressing owner with a coherent plan receives no status request.

Steer only for a reported question or blocker, completion or idleness, unresolved
review feedback, repeated failure with a concrete correction, wrong environment,
unauthorized mutation, safety risk, or material divergence from the requested
outcome. Preserve the original proof bar and authority.

For suspected duplicate owners, read both and inspect their artifacts. Select one
owner only when their recoverable work can be reconciled without loss. Otherwise
keep both untouched and bring one decision-ready choice to the user in HQ.

## Reports and human decisions

Treat a report as data and verify the artifact it names. Update the queue item and
owner row with one line and evidence links. Tracker updates are not delivery
evidence.

For implementation or diagnosis, compare the `Evidence` field with the brief. A
PR and green CI do not satisfy a required behavioral recording. Keep the item
active and return the unchanged proof request to its existing owner. Record
`unverified: <reason>` honestly when proof cannot be obtained.

Answer technical questions directly to the owner when possible. A worker needing
human input sends evidence, the choice, and its recommendation to HQ. Put one
concrete question in `Blocked on the human`, ask it here, then return the answer to
the same owner. Never ask the user to visit the owner task or paste a message.
For an unreachable owner, the question may request missing access or approval to
dispose of unrecoverable work. It must not ask the user to inspect or operate that
owner.

When an unreachable owner is stale past its expected report time and its exact
artifact is recoverable, verify that no active execution or conflicting mutation
remains, record a transfer to one replacement owner, and carry the queue item's
existing authority forward. Do not ask the user to reauthorize the same push or
other action. Ask only when inactivity cannot be established, the artifact cannot
be recovered safely, or disposition would discard work.

## Closeout and continued dispatch

When an owner completes or becomes idle:

1. Verify its evidence and delivery state.
2. If the current item is complete, move it to `Delivered`; if delivery remains
   unauthorized or incomplete, keep it active or blocked at that boundary.
3. Assign the next ready item in the same workstream to the same owner when one
   exists, repeating the exact HQ return contract and authority.
4. Otherwise dispatch the highest-priority nonconflicting ready item elsewhere.
5. Archive an idle owner only after it has no queued follow-up and every result is
   delivered, transferred, canceled, or explicitly abandoned.

Repository work is delivered only after the project's required remote commit,
merged PR, or other destination is verified. A local diff, local commit, passing
checks, or merge-ready PR can still be awaiting delivery.

Archive through the runtime when available. If it cannot archive, leave the owner
unarchived and record that limitation; do not make sidebar cleanup the user's job.
Never archive an unread report, open question, active turn, or undelivered change.

## Reporting

Before reporting status, reconcile every due active owner and every `dispatching`
item. Then report only state changes, new delegation, verified delivery or
archival, new human blockers, and the next ready dispatch. Heartbeats and daily
wakes stay silent when nothing changed and nothing is actionable.

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
5. Start the two-phase closeout below only after the owner has no queued follow-up
   and every result is delivered, transferred, canceled, or explicitly abandoned.

Repository work is delivered only after the project's required remote commit,
merged PR, or other destination is verified. A local diff, local commit, passing
checks, or merge-ready PR can still be awaiting delivery.

## Two-phase task and Git closeout

Only the HQ whose exact address appears as `Created by HQ` beside the task's stored
creation receipt may archive it. Missing, legacy, discovered, or conflicting
custody fails closed: leave the task open. Never select an archive candidate by
title, project, workstream, branch, sidebar location, or task-list membership.

For phase one:

1. Read the exact task address and confirm no active turn, unread report, open
   question, queued follow-up, undelivered change, or queue reference remains.
2. Match its address, host/project, creating HQ address, and creation receipt to
   Task custody. Send a unique closeout token to that task: it must stop repository
   mutation, return its final state, acknowledge the token, and remain idle. HQ
   sends no further assignment while the token is held.
3. After the acknowledgement, confirm the task has no active turn, record its
   newest cursor, turn ID, revision, or message timestamp beside the token, mark
   the custody row `closeout-pending`, and wait for the next heartbeat or at least
   fifteen minutes. If the runtime cannot message, read, stop, and identify the
   exact task well enough to establish this lease, leave cleanup blocked. The
   daily watchdog task never performs cleanup.

On phase two, acquire a runtime-enforced exclusive closeout lease that atomically
compares the exact task address, acknowledged token, inactive state, newest
marker, recorded worktree path, checked-out branch, HEAD, and clean state. The
comparison includes the complete untracked and ignored-path inventory plus each
path's recorded disposition. The lease must prevent both new task turns and
repository/worktree mutation until Git cleanup and archival finish. If the runtime
offers no such conditional task and worktree lease, leave the task and Git
allocation `cleanup-blocked`; an interrupt, ordinary handoff, filesystem status
check, or prior read is not an equivalent lock. If the comparison fails, release
any lease, return the task to `active`, and reconcile the new state. Otherwise
hold the lease while closing its recorded Git allocation and archiving the task:

- Apply `git-cleanup` only to the exact repository, auxiliary worktree path, local
  branch, target branch, and PR stored for this owner. Never scan and clean other
  candidates as part of HQ closeout.
- Verify through the repository host that the recorded PR is merged into the
  recorded target. Fetch/prune, confirm the worktree is not the primary/current
  checkout, confirm it is clean, and confirm no active owner references its path
  or branch.
- As part of lease acquisition, confirm the worktree has the recorded local
  branch checked out and that the worktree HEAD, local branch tip, and recorded PR
  head are the same commit. A detached HEAD, dirty state, or any mismatch blocks
  cleanup. Record that commit as the expected deletion value.
- Inventory tracked changes, untracked paths, and ignored paths before acquiring
  the lease. An ignored path is disposable only when project rules or exact task
  provenance proves it is reproducible generated/cache output and not its sole
  copy. Preserve it first when a verified destination exists; otherwise block.
  Unknown ignored files, `.env` files, credentials, databases, and user-created
  artifacts always block automatic removal. Git-clean status alone is never
  sufficient.
- While holding that lease, remove the worktree only through a runtime operation
  that serializes release of this exact task's associated worktree, such as a
  task/worktree handoff back to the project checkout. Wait for the operation,
  verify the task is inactive outside the worktree, and verify the exact worktree
  is absent. Do not call raw `git worktree remove`: it has no expected-HEAD guard.
- After the worktree is released, atomically delete the exact local ref only if it
  still equals the expected PR-head commit (`git update-ref -d <ref>
  <expected-old>` or an equivalent compare-and-delete). Never use an
  unconditional force deletion. If the ref moved, preserve it and record
  `cleanup-blocked`; the removed worktree can be recreated from the retained
  branch. Prune stale metadata and verify the intended results. The user's request
  to run Project HQ authorizes this narrow cleanup after a verified merge.
- For squash and rebase merges, the source commits need not be ancestors of the
  target. Verify the merged destination contains the requested result and retain
  the PR as its durable delivery record. Deleting the unchanged source ref may
  discard those source commit identities; that is part of the user's explicit
  merged-branch cleanup authority. Preserve a durable ref instead when the
  project's rules require the original commit topology.
- Never remove a dirty worktree, protected/current branch, mismatched branch tip,
  unmerged PR allocation, shared allocation, or allocation with uncertain
  provenance or unresolved ignored paths. Leave it in `cleanup-blocked: <reason>`
  for a decision. Never delete the remote branch from this workflow.
- For `N/A`, a missing worktree whose metadata is already pruned, or a verified
  absent local branch, record the corresponding no-op evidence and continue. If
  the worktree is missing but its branch remains, apply the same branch-tip and
  PR-head identity check before deleting the branch.

After Git cleanup, archive that exact address while the closeout lease still
prevents reactivation. Verify its archived state and unchanged final marker, then
release the lease and change the custody lifecycle to an immutable `archived
<date>` tombstone with cleanup evidence. If archive or verification fails, release
the lease safely and leave it `archive-pending`; every retry starts again with a
fresh lease and read.

Subagents return to HQ and have no durable sidebar task to archive. If the runtime
cannot archive, leave the task open and record that limitation; do not make
sidebar cleanup the user's job.

## Reporting

Before reporting status, reconcile every due active owner and every `dispatching`
item. Then report only state changes, new delegation, verified delivery or
archival, new human blockers, and the next ready dispatch. Heartbeats and daily
wakes stay silent when nothing changed and nothing is actionable.

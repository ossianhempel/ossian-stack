# Monitoring And Recovery

Read for monitoring, receiving reports, recovery, and reconciliation. Follow the scope and safety contract in the skill entry point.

## Monitoring workstreams

HQ owns monitoring. Sub-threads report, and usually do, but a report that never
arrives is HQ's problem to notice, never the user's. If the user has to ask HQ
what a workstream is doing, HQ has already failed. So while any row is open,
HQ checks in on a heartbeat of about fifteen minutes, using whatever the
runtime gives it and recording the mechanism in the ledger header:

- **Codex:** read each open thread's current state directly. Where a call can
  wait on a thread with a timeout, use it for a thread HQ has nothing else to
  do but wait for; otherwise read on the heartbeat.
- **Claude Code:** background and worktree agents notify HQ when they finish;
  that notification is the check-in for level 3 rows. For everything else,
  schedule a wake for the next heartbeat and let it lapse when no rows are
  open. No tight polling: one wake per heartbeat, never a loop of short ones.
- **GitHub Copilot and anything else:** probe for reading a session's state and
  for a scheduled wake per `delegation.md`. Without a wake, the
  heartbeat is the user's next re-orient, and HQ says so once at delegation.
- **A runtime that cannot read a thread's state** checks the artifact instead:
  the PR, the branch, the doc. A status request to the thread itself is sent
  only when the artifact has gone quiet past the row's expected report time.

Assume someone, the user or another agent, may have steered any sub-thread
since HQ last looked. So every check-in, and every message HQ sends a thread,
passes this gate first:

1. Read the thread's latest state: its newest messages from anyone, and whether
   it has an active turn.
2. Treat the newest instruction given inside that thread as authoritative over
   HQ's older brief. HQ does not overrule the user's later words with its plan.
3. Refresh the authoritative state of what the row names. For a PR that means
   checks, mergeability, top-level comments, submitted reviews, and unresolved
   inline review threads, read through the repository host's interface rather
   than a single summary view that omits review threads.
4. Classify the thread as progressing, blocked, completed, or idle.

The gate is not a full sweep of everything every time. Step 3 is the expensive
part, so run it only for a row whose step 1 read showed something new, or whose
expected report time has passed. A row sitting in the blocked list with its
waiting-on unchanged is skipped entirely: nothing HQ reads there changes what it
is waiting for. A re-orient that lands inside the heartbeat interval reuses the
row's checked stamp instead of re-running the gate.

A progressing thread with a coherent plan gets nothing. HQ sends a message only
when the evidence shows one of:

- the thread asked HQ something, or reported a blocker;
- the thread has completed or run out of work in its scope and needs its next
  item or its closeout;
- its PR has requested changes, unresolved review threads, or review feedback
  the thread has not acknowledged;
- repeated failures with no progress, and HQ has a concrete correction;
- wrong repository, an unauthorized or destructive mutation, a security risk, a
  release-gate violation, or a direct conflict with the user's latest
  instruction;
- gross divergence from the agreed outcome, not merely a different reasonable
  design.

Every message HQ sends to the workstream retains its exact return address,
report triggers, and channel.

Do not restate the task, add requirements, or raise the proof bar mid-flight.
When the thread's intent is ambiguous, one concise question beats prescriptive
steering. A check-in that changes nothing writes nothing to the ledger beyond
the row's checked stamp, and produces no report line.

Never interrupt, archive, rename, duplicate, or replace a thread without first
reading its current state. For a suspected duplicate, read both; if either has
unique progress, edits, or an active turn, leave both alone and ask the user.

**Idle closeout.** A completed or idle thread is not left as a lane HQ polls
forever. After reading its state and verifying its artifact, HQ does exactly
one of:

1. Send it the next item within the same workstream's scope, if one exists. The
   assignment repeats the exact HQ address, report triggers, and return channel.
2. Prepare its open question to decision-ready, with proof and a
   recommendation, and put one concrete question to the user in the blocked
   list.
3. Have it finish delivery the user has already authorized. For repository
   implementation, send it back through the brief's bounded `commit-push-pr`
   route; if delivery is not authorized, that is the blocked-list entry.
4. Verify delivery and move the row to Done per the archive rule below.

**Before every status reply**, whether from a heartbeat or a re-orient: list
every open row, run the gate over each, steer where the gate says to, and only
then report. A report from memory or from what HQ spawned this turn is not a
status. Heartbeat replies are delta-only: rows that changed state, threads
created or archived, new blockers, decisions newly ready for the user. An
unchanged row is not mentioned; a ready PR is one line with its link.
## When a workstream reports

A report is the sub-thread telling HQ where it got to. HQ reads it as data,
checks the claim against the artifact it names (the PR, the diff, the doc, the
ticket), and decides what happens next. The ledger row gets one line: date,
state, what HQ is waiting on, with links to the evidence. For untracked work,
the brief, report, and artifacts hold the detail; do not create a ticket to
accept a report. For tracked work, the brief names the owned ticket and permitted
updates: keep its status current and comment only on meaningful progress, a new
or changed blocker, a decision needed, or completion. Use a few sentences with
evidence links, omitting empty sections. Do not repeat unchanged blockers or
mirror HQ/agent coordination. Preserve required claim/release/resume records;
keep durable decisions in the ticket/spec and link detailed evidence. Reconcile
material state differences within the thread's permissions; a new HQ report alone
does not require a tracker comment. Tracker updates are not delivery evidence.

If the report asks a question, HQ answers it by message to that thread when the
runtime allows, otherwise hands the user the answer to paste. If it needs a human
decision, that goes in the ledger's blocked list and in HQ's next reply, named by
workstream.

Archive completed repository work only after HQ verifies delivery against the project's
workflow: committed and pushed to the intended remote branch for direct commits,
or merged for PR work. For reports, specs, or decisions delivered outside the repo,
verify publication at the agreed destination. Link that evidence in the done row.
A finished implementation, passing checks, a local commit, or a merge-ready PR
still awaiting delivery stays in Open workstreams as awaiting commit, push, or
merge. Keep its thread available for follow-up. If delivery needs authorization,
record that blocker; the archive rule grants no permission to commit, push, or merge.

Once delivery is verified, move the row to Done and archive its thread. Other
retirement reasons require an explicit disposition of any undelivered changes:

- **Done**: the artifact landed (PR merged, spec published, decision recorded).
- **Redundant**: another thread has accepted ownership of the remaining work
  and its recoverable artifacts; record that handoff before archiving.
- **Dead end**: the user abandoned the work or approved its disposition; record
  what happens to any undelivered changes before archiving.

Archive through the runtime's thread-archive capability when the probe found
one, otherwise name the thread in the reply and ask the user to archive it.
Archiving is not deleting: the thread and its history stay reachable, and the
ledger's done list records that it was archived and why. Never archive a
thread with an unread report or an open question; read and record first, then archive.

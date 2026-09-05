# Delegation surfaces

The rule in the skill is *visible thread first, hand-made thread second, hidden
subagent last*. This file is how to tell which level a runtime gives you. Tool
names change between builds and are sometimes withheld from a session even when
the runtime has the feature, so probe by capability, record what you found in
the ledger, and re-probe when a later session looks different.

## Probe

Look through the tools available in this session for these capabilities:

| Capability | What it proves |
| --- | --- |
| Create a thread or session, optionally in a worktree, with a first message | Level 1 spawn |
| Send a message to an existing thread or session | Follow-ups without new threads; reports can come back by message |
| Set a thread's title, pin it | HQ can name itself and its threads |
| Archive a thread | HQ can retire done, redundant, and dead-end threads itself; without it, it asks the user each time |
| Read a thread's current state: its messages and whether it has an active turn | HQ can check in without messaging; the monitoring gate can run |
| Wait on a thread with a timeout, be notified when a background run finishes, or schedule a wake for this thread | HQ can heartbeat unattended; without any of these the user's re-orient is the heartbeat |
| Spawn a subagent that returns a result to this thread | Level 3 only |

A runtime can have the subagent tool without any of the thread tools. That is the case the
skill exists to catch: a subagent tool present while thread tools are absent
means level 2, not level 3, unless the work is a bounded report.

If the runtime's own instructions or tool descriptions say thread creation needs
an explicit user request, the `/orchestrate-threads` invocation plus the ledger row is
that request; say so in the ledger and in the reply.

## Return address

Resolve HQ's return address during the bootstrap probe. Record the exact HQ name
and, when the runtime exposes one, the task/thread/session id or messaging target
accepted by its cross-thread tool. When no stable id is exposed, record the exact
available addressing mechanism instead. Put that address and channel in every
initial brief and every later assignment or follow-up sent to the workstream.

Each kickoff, assignment, or follow-up tells the workstream to report proactively
when it is done, blocked or stuck, needs human input or a decision, or reaches its
authorized stop or delivery boundary. Use cross-thread messaging when the probe
found it. Without that capability, require the structured report as the
workstream's final message so the heartbeat can read it. Do not request routine
progress chatter or another copy of an unchanged blocker.

## What each runtime looks like today

Recorded so a probe result can be sanity-checked. Verify against the session,
never assume from this table.

- **Codex app.** Has thread creation, forking, titling, pinning, archiving,
  reading a thread's state, waiting on a thread, and cross-thread messaging,
  plus a separate subagent tool. Heartbeat by waiting on a thread with a
  timeout when HQ has nothing else to do; otherwise read only the rows due a
  check, not every open thread. The subagent tool is
  the one the model reaches for on the word "spawn"; do not. New threads appear
  in the sidebar as ordinary user threads. Some builds and remote-started
  threads withhold the thread tools; then fall to level 2.
- **GitHub Copilot app.** Probe visible session creation and messaging for level
  1, then verify that the child has a separate worktree before assigning repository
  mutation or delivery. A new session name alone does not prove checkout isolation.
  Fleet mode and custom agents are hidden subagents: level 3; they do not replace
  the separate visible workstream required for Copilot repository changes.
  No verified record exists here of reading another session's state or
  scheduling a wake, so probe both every bootstrap and record the result. Until
  a probe proves otherwise, the heartbeat is the user's re-orient, check-ins
  read the artifact (PR, branch, doc) rather than the session, and a message to
  a session is the last resort for a thread past its expected report time.
- **Claude Code.** Cannot open a sibling session from inside a session. The
  desktop app can list other sessions and message them, and can offer the user
  a one-click chip that starts a new session from a suggestion; that chip is a
  level 2 spawn and the preferred one. Background agents, worktree agents, and
  remote agents are level 3, and they notify HQ on completion. HQ cannot read
  another session's transcript, so the heartbeat is a scheduled wake that
  checks artifacts and anything messaged back; a status request to a level 2
  thread is the last resort, not the routine check.
- **Anything else.** Level 2 until proven otherwise.

## GitHub Copilot isolation and PR-link recovery

This boundary responds to a user-reported incident: a Copilot HQ became PR-linked
after branch/PR work, and title sync overrode its name. This is not an independently
verified claim about every Copilot version or session. Inspect supported
capabilities in the current runtime.

Before a child changes files or delivers work, verify its distinct session identity
and worktree path against the recorded HQ checkout. An in-place session, a same-
checkout fork, or a child instructed to change HQ's branch is not isolated. Reuse
an existing workstream only if it passes those checks. If a separate visible
session with a separate worktree cannot be obtained under the host's task-creation
rules, give a ready-to-use brief for the user to open separately. HQ continues
reading, planning, reporting, and maintaining its ledger on the original branch.

For existing dirty changes or ledger delivery, transfer only the authorized diff
or snapshot to the child with an explicit source and destination. Have it confirm
receipt and apply the changes in its own worktree, preserving unrelated work and
HQ's dirty files. The child must not reset, switch, commit, or publish from HQ's
checkout. Carry existing delivery authorization into the brief; isolation is a
routing requirement, not a reason to ask for that authorization again.

If HQ is already PR-linked or its title keeps reverting, inspect supported unlink
or session/settings capabilities first. Use a supported detach only within the
user's authorization and verify the result. Do not claim that no setting exists
across all Copilot versions. Do not edit private session metadata or caches, and
do not loop title restores to fight PR sync.

When no supported detach is available, explain that observed limitation and
recommend that the user explicitly create a replacement HQ. Do not automatically
create it from the recovery recommendation. Transfer ledger and workstream
references after the replacement is explicitly requested, preserving both session
histories and recoverable changes. Record the old PR-linked session as the PR
workstream, not as the new HQ; keep it open until delivery is verified under the
existing archive rule. Recovery does not authorize switching the old checkout's
branch or discarding its work.

## Level 2, the hand-made thread

Give the user two things, in a fenced block they can copy: the title per the
naming rules, and the kickoff brief. Tell them where to create it (new thread in
the same project, worktree on). The row's `Thread` cell is `pending` until the
user confirms the thread exists, then the exact title.

When the runtime lets a level 2 thread message HQ, give it the exact HQ target and
require proactive reports through that channel. Otherwise the brief's Report
block is the final workstream message that HQ reads on its heartbeat. HQ still
checks the artifact the row names. `handoff` is not a report channel: it writes a
continuation document for the next session in that same thread, and the user runs
it.

## Level 3, the subagent

Use a worktree. Give it the same brief. Its result is folded into the ledger
under the workstream it served, with `subagent` in the row's `Thread` cell,
because nobody can return to it later.

---
name: orchestrate-threads
description: "Establish or resume a persistent project HQ that coordinates visible workstream tasks and a durable ledger. Explicit invocation only."
argument-hint: "Project or workstream name, optionally what to work on first"
disable-model-invocation: true
---

# Orchestrate Threads

This chat is now **HQ** for one project or workstream. HQ is the thread the user
always comes back to. It never does the work itself beyond trivial edits: it
decides, writes briefs, delegates to a thread per workstream, tracks what came
back, and tells the user what needs a human. One-off chats stop existing; every
piece of work has a home thread that HQ knows about. On GitHub Copilot, the
checkout boundary below also excludes trivial implementation edits.

HQ has to survive two things: context compaction, and the user walking away for a
week. Both are solved the same way. Nothing HQ knows lives only in this chat. The
ledger (`references/ledger.md`) is HQ's thread registry: which thread owns which
workstream, what it is called, and one line on where it stands. Every
`/orchestrate-threads` call starts by reading it.

The ledger is sufficient to coordinate work. Planning, research, diagnosis, and
implementation can proceed without an issue tracker. Set tracking per workstream
from the user's request and active project workflow: use tickets when the user
requests them or the work calls for tracked delivery. An existing tracker config
only makes that capability available; delegation alone never authorizes creating
issues. For tracked work, link the tickets from the ledger rather than duplicating
them. For untracked work, link the brief, report, and resulting artifacts.

On each invocation, read the ledger and the bootstrap reference to establish whether this is bootstrap or reorientation. Carry inherited authority and exclusions into every brief. Use the monitoring reference while following active workstreams; keep outcomes and ownership durable in the ledger.

## GitHub Copilot HQ checkout boundary

On GitHub Copilot only, HQ stays on its original checkout branch (normally the
project's default branch) and coordinates. Record that branch on bootstrap;
do not switch to the default branch if HQ already starts elsewhere. HQ may write
and reconcile its ledger, but does not create/switch branches, implement even
trivial changes, commit, push, or create/deliver PRs in its session. A request to
ship authorizes delivery in a separate workstream, not those operations in HQ.

Delegate authorized repository changes and delivery, including ledger shipping,
to a separate visible session with a verified separate worktree. Carry the user's
scope and existing authorization into the brief without asking again. The child
must not operate on HQ's checkout indirectly. If session/worktree separation is
unavailable or unverified, provide a brief for a separate session and continue
coordination; do not perform the mutation in HQ as a fallback.

`references/delegation.md` covers the isolation checks and recovery when an HQ is
already linked to a PR. Other runtimes retain their existing behavior, including
the trivial-edit exception and project-approved direct work on trunk.

## Threads, not subagents

The point of HQ is that work happens in **visible threads the user can open, pin,
scroll, and return to**, one per workstream. A hidden subagent that runs and
vanishes is not that. It loses the conversation, the worktree, and the ability to
follow up.

So delegation resolves in this order, and the first available level wins:

1. **A visible thread or session the user can open**, created from here with the
   kickoff brief as its first message, in its own worktree when it touches code.
   Codex and the GitHub Copilot app expose this: search your tool list for
   creating, forking, titling, and messaging threads or sessions. Use those even
   when a subagent tool is also present and the request sounds like "spawn".
2. **A thread the user creates by hand** from a brief you hand them, titled and
   ready to paste. This is the universal fallback and the normal path on Claude
   Code, which cannot open a sibling session from inside a session. If the host
   offers a one-click "start a session from this suggestion" control, use it,
   since it produces the same visible session.
3. **A background subagent in a worktree** only for bounded work whose whole
   result is a report or a diff, where nobody will need to continue the
   conversation afterwards. The row's Thread cell says `subagent`.

`references/delegation.md` has the per-runtime detail and the checks that tell
the levels apart.

Only HQ creates threads. A sub-thread that wants another thread asks HQ in its
report. This keeps the sidebar readable and keeps thread creation under the
user's eye.

## What HQ never does

- Long implementation inline. The pull to just do it is the signal to brief it.
- Merge, release, push to a protected branch, or any irreversible act. Those go
  to the user, named in the blocked list.
- Create a second thread for a workstream that has one.
- Let a subagent stand in for a thread on a runtime that has threads.
- Leave a done, redundant, or dead-end thread sitting in the sidebar.
- Message, rename, or archive a thread without reading its current state first.
- Report status from memory, or wait for the user to ask how a thread is doing.

**Reply shape, every turn:** what changed, per workstream by name; what
was delegated and where it lives; what was archived and why; what is blocked on
the human; the single next thing HQ will do. On a heartbeat, only the delta;
nothing changed is one line.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Hq bootstrap](references/hq-bootstrap.md): bootstrapping HQ or reorienting from the durable ledger.
- [Workstream briefs](references/workstream-briefs.md): briefing and starting an authorized visible workstream.
- [Monitoring and recovery](references/monitoring-and-recovery.md): monitoring, receiving reports, recovery, and reconciliation.

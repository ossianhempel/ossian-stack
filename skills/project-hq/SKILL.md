---
name: project-hq
description: "Establish or resume one persistent project HQ that accepts the user's task queue, coordinates execution owners, and keeps durable operational state. Explicit invocation only."
argument-hint: "Project name, optionally one or more initial tasks"
disable-model-invocation: true
---

# Project HQ

This task is now **HQ** for one project. HQ is the interface the user always
returns to: they can enter one request or dump a backlog here without deciding
which thread, agent, or tool should handle it. HQ captures the requests, orders
them, delegates ready work, monitors execution, verifies results, and brings only
decisions or approval boundaries back to the user.

Execution tasks and subagents are durable or bounded owners behind HQ. They may
remain visible for audit and recovery, but the user is never required to open,
pin, monitor, or carry messages between them. A worker needing human input reports
to HQ with evidence and a recommendation; HQ asks the user here and returns the
answer to the same owner.

Use this machinery for a standing project with several tasks or durable
workstreams. It is not the default route for a bounded request that one task can
finish directly.

## Durable project state

Nothing needed for recovery lives only in chat. Read `references/ledger.md` and
`references/queue-and-memory.md` before changing project state. The ledger at
`docs/agents/hq.md` contains:

- the project goal, standing constraints, and canonical links;
- an inbox and queue with stable item IDs, dependencies, authority, and owners;
- the execution-owner registry and current blockers; and
- short links to delivered artifacts and durable decisions.

The ledger is HQ's medium-term memory. Do not create a second running diary.
Detailed work belongs in the owning task, report, specification, ticket, commit,
or PR. Promote a confirmed lesson to the project's durable instructions or docs
only when it should change future work, then link it from the ledger.

Every invocation reads the ledger and `references/hq-bootstrap.md`. Every new
request is captured before work starts. Reconcile queued, dispatching, active,
blocked, and completed items against live owners and artifacts before creating or
reassigning work. A queue item has one stable ID and one owner; retries reuse both.

## Coordination loop

HQ continues without waiting for the user while useful authorized work remains:

1. Capture and normalize new requests. Merge duplicates that seek the same
   outcome; preserve distinct constraints and authority.
2. Complete a trivial authorized item in HQ when it has one obvious action and
   no isolation rule forbids it. Record its evidence without creating an owner.
3. Mark dependencies and select the highest-priority ready items that do not
   conflict over a checkout, artifact, or irreversible boundary.
4. Reuse the durable owner for that workstream, or create one execution owner per
   `references/delegation.md`. Record `dispatching` before creation and attach the
   returned address before treating the item as active.
5. Monitor active owners through `references/monitoring-and-recovery.md` and
   verify their evidence before accepting completion.
6. Dispatch the next ready item as soon as capacity becomes available. Stop only
   when the queue is empty, every ready item is blocked, or the next action needs
   human input or authority.

For an unattended workstream with several consequential decisions, its brief may
reference `show-me-your-work`; the workstream owns that trail and the ledger links
it. Use `handoff` only when an owner must pause or move sessions.

## Daily recovery watchdog

On bootstrap and takeover, follow `references/daily-watchdog.md`. When the runtime
offers recurring automations and cross-task messaging, ensure one idempotent daily
watchdog exists and register this HQ. The watchdog uses the cheapest suitable
model and a low reasoning setting, wakes only registered HQ tasks that remain
pinned, and asks each to reorient, reconcile, and continue its ready queue. It is
recovery after inactivity, not a substitute for the shorter heartbeat while work
is active.

## GitHub Copilot HQ checkout boundary

On GitHub Copilot, HQ stays on its original checkout branch and coordinates.
Record that checkout on bootstrap. Repository mutation and delivery require a
verified separate worktree owner. HQ may reconcile its local ledger, but it does
not switch branches, commit, push, or create a PR from its own checkout.

Carry existing authorization into the separate owner without asking again. If
safe separation is unavailable, keep the item blocked in HQ with the exact
isolation problem. Do not send the user elsewhere to finish setup or carry a
brief. `references/delegation.md` covers recovery when HQ is already linked to a
PR. Other runtimes may perform trivial authorized edits in HQ when delegation
would add no value.

## Invariants

- One active HQ registration per project. A takeover retires the old address.
- Queue IDs use the ledger's exact monotonic `Q-001` form. One queue item ID and
  one execution owner serve the same outcome.
- Reuse a workstream owner for follow-up work; do not create a sibling by default.
- Only HQ creates, messages, renames, or archives execution tasks.
- Read an owner's newest state before messaging, interrupting, renaming, or
  archiving it.
- Never accept `done` without the evidence named in the brief.
- Never infer commit, push, issue, publish, release, merge, or destructive
  authority from delegation or from a queued request.
- Treat an explicit exclusion or withheld action as settled. Record the boundary
  and do not ask for that authority again unless the user reopens it.
- Pin HQ only. Execution tasks remain unpinned unless the user explicitly asks.
- Keep the user in HQ. Surface a worker task only when the user asks to inspect it.

**Reply shape:** report meaningful changes by workstream, new delegation and its
owner, verified delivery or archival, human blockers with one concrete question,
and the next ready item HQ will dispatch. On a heartbeat or daily wake, report only
the delta; when nothing changed and nothing is actionable, stay quiet.

## Task references

- [HQ bootstrap](references/hq-bootstrap.md): bootstrap, takeover, and reorientation.
- [Queue and memory](references/queue-and-memory.md): capture, ordering, ownership, deduplication, and durable state.
- [Delegation](references/delegation.md): choose and isolate execution owners without moving the user out of HQ.
- [Workstream briefs](references/workstream-briefs.md): brief authorized work and define its proof and return contract.
- [Monitoring and recovery](references/monitoring-and-recovery.md): monitor, receive reports, recover, and reconcile.
- [Daily watchdog](references/daily-watchdog.md): ensure the cheap-model daily recovery automation.

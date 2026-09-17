# Queue and memory

Read when HQ receives tasks, chooses what runs next, or needs to recover after a
gap or context compaction.

## Capture

Treat every actionable request in HQ as queue input. Before delegating:

1. State the observable outcome in one line.
2. Reconcile it against existing queue items, owners, branches, PRs, and artifacts.
3. Reuse an item when the new request refines the same outcome. Preserve the
   newest instruction and record changed scope or authority.
4. Create a stable ID for a distinct outcome. Record priority, dependencies,
   workstream, granted actions, and the first action outside authority.
5. Mark it `ready` only when dependencies are satisfied and an owner can act
   without a missing human decision.

An unmet dependency leaves an item `queued`. Use `blocked` only when progress
requires human input, missing access, or an unavailable capability.

Do not force the user to classify or sequence a task dump. Infer sensible
priority from urgency, dependencies, risk, and stated order. Ask one question in
HQ only when different interpretations would materially change the work.
An explicit exclusion or withheld action is not an open question. Record it as the
item's stop boundary and do not ask again unless the user reopens it.

## Dispatch and capacity

Run independent ready items concurrently when owners and working locations do not
conflict. Serialize items that touch the same checkout, migration, release train,
mutable environment, or decision. Prefer finishing or unblocking active work over
creating more owners.

Before creating an owner, write `dispatching` and the intended workstream to the
queue. After creation, record its exact address and mark the item `active`. On
recovery, inspect a `dispatching` item's live tasks and artifacts before retrying.
This two-step record prevents a wake or compacted session from duplicating work.

When an owner becomes idle, give it the next ready item inside the same workstream
and repeat the return contract. Create a new owner only when the work needs a
separate durable history, worktree, or concurrent isolation boundary.

## Memory boundaries

Use three layers:

- The ledger holds current operational truth and replaces stale state in place.
- Owner tasks and artifacts hold detailed reasoning, evidence, and implementation.
- Project docs and instructions hold confirmed decisions or lessons that should
  change future work.

Do not append a general working log. It duplicates the sources above, grows
without bound, and becomes a competing truth. Promote a reusable lesson only
after it is confirmed and within the user's authorization to edit its durable
destination.

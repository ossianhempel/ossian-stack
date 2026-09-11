# HQ bootstrap

Read for bootstrap, takeover, or reorientation. Follow the scope and safety
contract in the skill entry point.

## Naming

- **HQ:** `<project emoji> <Project>`, for example `🏋️ GainsLog`. Use the
  project's proper name. Record one stable project mark in the ledger. Only HQ is
  pinned.
- **Execution task:** `<Project> · <workstream>`, for example
  `GainsLog · csv export`. Reuse it for later queue items in that workstream.
- **Subagent:** record its run under the workstream and queue item; it needs no
  sidebar name.

## Invocation

A fresh task or `/project-hq <project> [tasks]` bootstraps. A bare `/project-hq`
inside an established HQ reorients. An existing ledger with a missing or retired
HQ means this task is taking over.

### Bootstrap or takeover

1. Read the project's active instructions and its docs index when available.
2. Read `docs/agents/hq.md` when it exists. On takeover, inspect every unfinished
   item and owner before changing state. Replace the old HQ address and retire its
   watchdog registration; preserve owner histories and recoverable artifacts.
3. Probe task creation, subagents, cross-task messaging, state reads, waits,
   archiving, recurring automations, and checkout isolation per `delegation.md`.
4. Record the tracker configuration when present. Availability never selects a
   ticket workflow or authorizes creating issues.
5. Set the stable HQ title and pin this task when the runtime supports it. Ask the
   user once in HQ when a manual title or pin is unavoidable.
6. Ensure and register the daily recovery watchdog per `daily-watchdog.md`.
7. Write the ledger header and project context. Tell the user in one short
   paragraph that this HQ accepts their task dump, coordinates owners, and returns
   only meaningful results and decisions here.
8. Capture every supplied task in the queue, then dispatch all nonconflicting
   ready work that fits the available capacity. Do not make the user restate it.

### Reorient

1. Read the ledger rather than relying on chat memory.
2. Reconcile every `dispatching` and active item with its newest owner state and
   artifact. Fold in reports that the ledger has not seen.
3. Capture any new requests from this invocation, merge true duplicates, and
   update dependencies or authority from the user's newest instruction.
4. Verify completed claims, close or block items truthfully, and dispatch the next
   ready authorized work.
5. Report only changed workstreams, human blockers, and the next action. Stay
   quiet after a scheduled wake when the queue is empty and nothing changed.

Reorientation mutates only operational state and work already authorized by the
queue. A mismatch between a claimed artifact and the working tree remains with
its owner; HQ records and routes it instead of silently repairing unrelated work.

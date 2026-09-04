---
summary: Durable HQ task registry for the Ossian Stack project.
read_when:
  - Re-orienting HQ or dispatching and reconciling project workstreams.
---

# HQ · Ossian Stack

Runtime: Codex desktop · delegation level: 1 · probed: 2026-09-04
Project: `/Users/ossianhempel/Developer/ossian-stack`
Project ID: `63c3b9b4-1053-464c-aa97-ac11dd0a19a1` · host: `local`
Tracker: none (`docs/agents/issue-tracker.md` is absent)
HQ task: `🧰 Ossian Stack` · pinned
HQ task ID: `01a06b52-5e84-7621-8bc9-71e2f561ccc6`
Project mark: 🧰
Established: 2026-09-04; no previous ledger existed.

## Operating contract

HQ briefs work, coordinates visible tasks, verifies reports, and maintains this
ledger. Substantial implementation belongs in owning workstream tasks. Reuse each
workstream's task for follow-ups. Human decisions and irreversible actions return
to the user. The user's explicit orchestrate invocation requests this visible-task
workflow; each dispatch must have a ledger row in the same turn.

Available capabilities: create, read, message, wait, title, pin, and archive tasks.
No workstream was requested at bootstrap, so no task was created or archived.
Before a planning dispatch, configure the project tracker. Follow the repository's
active branching instructions when choosing the task environment.

## Open workstreams

| Workstream | Task | Kind | State | Last report | Waiting on |
| --- | --- | --- | --- | --- | --- |

## Blocked on the human

None.

## Done

| Workstream | Artifact | Closed | Task |
| --- | --- | --- | --- |
| 🧭 ossian-mode | [Entry skill](../../skills/ossian-mode/SKILL.md) | 2026-09-04: HQ reviewed skill, routing, metadata, and rendered map; repository checks passed. User authorized commit and push to main. | `🧭 Ossian Stack · ossian-mode` (`01a06b6d-630e-7893-b1de-bdf1f7393cfb`, local), archived (done: approved implementation) |

## Inline edits

- 2026-09-04: Added one-password credential routing and conditional tracker/setup guidance to ossian-mode; updated map links and regenerated images. Repository checks passed. Generic skill validator does not support the existing disable-model-invocation field; preserved the required explicit-only metadata.
- 2026-09-04: Created this ledger and named and pinned HQ. Ledger contains task names, IDs, and status; no secrets. Left uncommitted for the user to decide whether to track it.

## Next

After publication, refresh the plugin and start a new session to use ossian-mode.

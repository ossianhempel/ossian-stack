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
| PR follow-through | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/e3145f29f4268fb505bf212f49cf13fbdebd26ca) | 2026-09-04: checks and map render passed; HQ verified commit on origin/main. Live PR follow-through remains unverified. | `Ossian Stack · PR follow-through` (`01a06be7-972f-7a81-bab7-69b449bbd836`, local), archived after verified push |
| 🧭 ossian-mode | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/f737a2e88d50325a5741641a455941e9407a961d) | 2026-09-04: HQ verified this commit on origin/main after push; repository checks passed. | `🧭 Ossian Stack · ossian-mode` (`01a06b6d-630e-7893-b1de-bdf1f7393cfb`, local), archived (implementation was archived early; delivery now verified) |

## Inline edits

- 2026-09-04: Updated orchestrate-threads, ledger guidance, and report template to keep undelivered implementation open until the required commit/push/merge is verified. Delivered in e3145f2, verified on origin/main.
- 2026-09-04: Added one-password credential routing and conditional tracker/setup guidance to ossian-mode; updated map links and regenerated images. Repository checks passed. Generic skill validator does not support the existing disable-model-invocation field; preserved the required explicit-only metadata.
- 2026-09-04: Created this ledger and named and pinned HQ. Ledger contains task names, IDs, and status; no secrets. Left uncommitted for the user to decide whether to track it.

## Next

Use the published workflow after plugin refresh and a new session; verify the handoff on the next requested PR. No open workstreams.

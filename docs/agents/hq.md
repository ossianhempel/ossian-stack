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
Planning and delegation can proceed without issues. Configure a tracker only for
a chosen ticket-based workflow; delegation alone never creates an issue. Follow
the repository's active branching instructions when choosing the task environment.

## Open workstreams

None.

## Blocked on the human

None.

## Done

| Workstream | Artifact | Closed | Task |
| --- | --- | --- | --- |
| ossian-mode | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/60666b5b7d6efcb7ae33a27e906b61bcc481c1a1) | 2026-09-04: concise tracker reporting reviewed; 5 source simulations / 13 assertions, map render and repository checks passed. HQ verified this SHA on origin/main. Existing project copies and installed runtime were not updated. | `🧭 Ossian Stack · ossian-mode` (`01a06b6d-630e-7893-b1de-bdf1f7393cfb`, local), archived after delivery verification |
| PR follow-through | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/f3ecb763b7eb0143b96a5ebd0728bb25b16942ed) | 2026-09-04: P3 autoreview clean; 17 Azure tests, 38 GitHub tests, map render and repository checks passed. HQ independently verified origin/main at this SHA. Live Azure behavior remains unverified. | `Ossian Stack · PR follow-through` (`01a06be7-972f-7a81-bab7-69b449bbd836`, local), archived after delivery verification |

## Inline edits

- 2026-09-04: Reopened ossian-mode for concise tracker comments. Prior optional-tracker fix delivered in 663c306 and verified on origin/main.

- 2026-09-04: Reopened ossian-mode for optional-tracker orchestration. Its initial entrypoint delivery remains verified in f737a2e.
- 2026-09-04: Initial PR follow-through delivered in e3145f2 and archived after verified push; reopened the same task for Azure DevOps support.
- 2026-09-04: Updated orchestrate-threads, ledger guidance, and report template to keep undelivered implementation open until the required commit/push/merge is verified. Delivered in e3145f2, verified on origin/main.
- 2026-09-04: Added one-password credential routing and conditional tracker/setup guidance to ossian-mode; updated map links and regenerated images. Repository checks passed. Generic skill validator does not support the existing disable-model-invocation field; preserved the required explicit-only metadata.
- 2026-09-04: Created this ledger and named and pinned HQ. Ledger contains task names, IDs, and status; no secrets. Left uncommitted for the user to decide whether to track it.

## Next

No open workstreams. Existing project template copies require a separate refresh to adopt concise tracker reporting.

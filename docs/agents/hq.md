---
summary: Durable Project HQ queue and owner registry for Ossian Stack.
read_when:
  - Reorienting HQ, capturing tasks, or reconciling execution owners.
---

# HQ · Ossian Stack

Runtime: Codex desktop · probed: 2026-09-11
Project: `/Users/ossianhempel/Developer/ossian-stack` · ID `63c3b9b4-1053-464c-aa97-ac11dd0a19a1`
HQ task: `🧰 Ossian Stack` · address `01a06b52-5e84-7621-8bc9-71e2f561ccc6` · host `local` · pinned
Daily watchdog: `project-hq-daily-wake` · registered 2026-09-11 · daily 08:00 Europe/Stockholm · Luna/low
Tracker available: none (`docs/agents/issue-tracker.md` is absent)

## Project context

- Goal: Maintain and distribute the ossian-stack plugin and its skill tree.
- Standing constraints: work directly on `main`; preserve unrelated work; the commit is the release; run `bun run check` after shipped skill changes.
- Canonical decisions and docs: [AGENTS.md](../../AGENTS.md), [plugin workflow](../plugin-workflow.md), [supported agents](../supported-agents.md)

The user communicates through this HQ. HQ captures task requests, coordinates
execution owners, verifies evidence, and returns results and decisions here. Only
HQ is pinned. Tracker availability never authorizes issue creation.

## Inbox and queue

| ID | Request | Priority | Depends on | Workstream | Authority | State | Last action |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Execution owners

| Workstream | Owner | Mode | State | Current item | Last report | Last checked | Waiting on |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Blocked on the human

None.

## Delivered

| ID | Workstream | Artifact | Closed | Owner |
| --- | --- | --- | --- | --- |
| Q-001 | workflow delivery | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/c705a55f78ea94837fc589a8c043ac69c06aaeeb) | 2026-09-05: iOS release babysit routing and P1 autoreview default delivered; repository checks passed. | `Ossian Stack · PR follow-through`, archived |
| Q-002 | coordination workflows | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/c705a55f78ea94837fc589a8c043ac69c06aaeeb) | 2026-09-05: routing, heartbeat monitoring, and proactive HQ reporting delivered. | `Ossian Stack · ossian-mode`, archived |
| Q-003 | ossian-mode | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/7bbeb08447c2e2d03c7579a61ae978df475019b3) | 2026-09-04: Copilot HQ isolation reviewed and source scenarios passed. | `Ossian Stack · ossian-mode`, archived |
| Q-004 | commit-push-pr | [Published commit](https://github.com/ossianhempel/ossian-stack/commit/7c6a900) | 2026-09-12: direct branch delivery added; full checks and structured review passed; pushed to `main` without a PR. | `🧰 Ossian Stack`, inline |

## Inline actions

- 2026-09-12: Updated `commit-push-pr` so ship intent defaults to the selected existing branch; branch, worktree, and PR creation now require explicit PR intent or active project policy.
- 2026-09-11: Migrated the skill and this ledger from orchestrate-threads to Project HQ; added the durable queue, sole-interface contract, duplicate-dispatch recovery, and registered daily Luna watchdog.
- 2026-09-05: Reused ossian-mode to make proactive report-back instructions part of every execution-owner assignment, not only initial priming.
- 2026-09-04: Reused ossian-mode to align project-hq task priming and PR follow-through; the clean Jira adapter remains awaiting delivery.
- 2026-09-04: Reused PR follow-through to align autoreview default reporting with P2; the completed iOS release babysit changes remain awaiting delivery.

- 2026-09-04: Reopened ossian-mode to make tracker setup adopt ninja-bq and other existing Jira conventions without silently creating shared Jira schema.

- 2026-09-04: Reopened PR follow-through for iOS release routing. Azure support previously delivered and verified in f3ecb76.

- 2026-09-04: Reopened ossian-mode for Copilot HQ isolation. Concise tracker reporting delivered and verified in 60666b5.

- 2026-09-04: Reopened ossian-mode for concise tracker comments. Prior optional-tracker fix delivered in 663c306 and verified on origin/main.

- 2026-09-04: Reopened ossian-mode for optional-tracker orchestration. Its initial entrypoint delivery remains verified in f737a2e.
- 2026-09-04: Initial PR follow-through delivered in e3145f2 and archived after verified push; reopened the same task for Azure DevOps support.
- 2026-09-04: Updated project-hq, ledger guidance, and report template to keep undelivered implementation open until the required commit/push/merge is verified. Delivered in e3145f2, verified on origin/main.
- 2026-09-04: Added one-password credential routing and conditional tracker/setup guidance to ossian-mode; updated map links and regenerated images. Repository checks passed. Generic skill validator does not support the existing disable-model-invocation field; preserved the required explicit-only metadata.
- 2026-09-04: Created this ledger and named and pinned HQ. Ledger contains task names, IDs, and status; no secrets. Left uncommitted for the user to decide whether to track it.

## Next

The queue is empty. Capture the next request here and route it through Project HQ.

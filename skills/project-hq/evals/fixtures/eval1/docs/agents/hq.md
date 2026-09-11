# HQ · GainsLog

Runtime: Claude Code · probed: 2026-09-01
Project: GainsLog
HQ task: `🏋️ GainsLog` · address: gainslog-hq · pinned
Daily watchdog: unavailable: runtime cannot message sibling sessions
Tracker available: docs/agents/issue-tracker.md

## Project context

- Goal: Maintain and improve GainsLog.
- Standing constraints: preserve deleted-set semantics.
- Canonical decisions and docs: none

## Inbox and queue

| ID | Request | Priority | Depends on | Workstream | Authority | State | Last action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q-001 | Export workouts as CSV | P1 | none | csv-export | edit through PR; stop before merge | active | 2026-09-01: owner csv-task |
| Q-002 | Redesign sync retry ownership | P2 | none | sync-rewrite | research only | active | 2026-08-30: owner sync-task |
| Q-003 | Diagnose duplicate sets | P2 | none | duplicate-sets | diagnose only | blocked | never: no programmatic owner surface |

## Execution owners

| Workstream | Owner | Mode | State | Current item | Last report | Last checked | Waiting on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| csv-export | `GainsLog · csv-export` (`csv-task`) | task | PR open | Q-001 | 2026-09-01: PR #212, CI green, one review thread | 2026-09-01: review pending | review |
| sync-rewrite | `GainsLog · sync-rewrite` (`sync-task`) | task | designing | Q-002 | 2026-08-30: approach drafted | 2026-08-30: progressing | nothing |

## Blocked on the human

- Q-001 / csv-export: review PR #212

## Delivered

| ID | Workstream | Artifact | Closed | Owner |
| --- | --- | --- | --- | --- |

## Inline actions

- 2026-09-01: fixed README typo "progresive"

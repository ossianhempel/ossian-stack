# The ledger

`docs/agents/hq.md` in the project is HQ's compact operational memory. HQ creates
it on bootstrap and rewrites it whenever queue, owner, blocker, or delivery state
changes. Keep it short and link to detail elsewhere.

Whether it is committed follows the user's authority and project workflow. Say
once at bootstrap that it contains task names and addresses but no secrets.

```markdown
# HQ · <Project>

Runtime: <runtime> · probed: <date>
Project: <path or project identifier>
HQ task: `<project emoji> <Project>` · address: <task/thread/session id> · pinned
Daily watchdog: <registered date | unavailable: reason>
Tracker available: <config link or none; selected per item>

## Project context

- Goal: <one sentence>
- Standing constraints: <short bullets or links>
- Canonical decisions and docs: <links or none>

## Inbox and queue

| ID | Request | Priority | Depends on | Workstream | Authority | State | Last action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q-001 | <observable outcome> | P1 | none | csv export | edit, test; stop before commit | active | <date time>: owner task-123 |
| Q-002 | <observable outcome> | P2 | Q-001 | sync | research only | queued | never |

## Execution owners

| Workstream | Owner | Mode | State | Current item | Last report | Last checked | Waiting on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| csv export | `GainsLog · csv export` (`task-123`) | task | implementing | Q-001 | <date + report link> | <date time + classification> | nothing |

## Blocked on the human

- Q-003 / <workstream>: <one decision-ready question with recommendation>

## Delivered

| ID | Workstream | Artifact | Closed | Owner |
| --- | --- | --- | --- | --- |
| Q-000 | setup | <commit or doc link> | <date + verified outcome> | archived after delivery |

## Inline actions

- <date>: <small action and why>
```

Rules:

- When reading a legacy HQ ledger, preserve every open row, blocker, delivered
  artifact, and owner address while converting it into Project context, Inbox and
  queue, Execution owners, Blocked on the human, and Delivered. Give each
  unfinished legacy row a stable queue ID before dispatching anything new.
- Queue IDs are monotonic within the project (`Q-001`, `Q-002`). Never reuse or
  renumber one. A follow-up that changes the same outcome updates the existing
  item; a distinct deliverable gets a new ID.
- `State` is `queued`, `ready`, `dispatching`, `active`, `blocked`, `delivered`,
  or `canceled`. Record `dispatching` before creating an owner. If creation fails,
  leave the item there with the error so recovery can reconcile before retrying.
- `Authority` records allowed actions and the first forbidden boundary. A later
  instruction may expand or narrow it; silence does neither.
- A workstream is a durable area of ownership. Reuse its owner for sequential
  items. `Mode` is `task`, `subagent`, or `HQ`.
- `Last action` contains the timestamp, owner address, and dispatch/result link.
  It is the idempotency record checked before a retry.
- Keep implementation awaiting commit, push, PR, merge, or publication in the
  queue until that authorized delivery is verified.
- The blocked section contains only questions that require the user. Technical
  blockers stay with the owner unless they need access or a decision.
- Move delivered items out of the active queue after verifying the remote commit,
  merged PR, published artifact, or other agreed destination.
- Archive an owner only when it has no queued follow-up and every recoverable
  result has been delivered, transferred, canceled, or explicitly abandoned.

# Workstream briefs

Read before starting or assigning an execution owner.

## Contract

The brief must stand alone. Carry the queue item ID, outcome, done condition,
dependencies, project facts, work location, proof contract, exact authority, first
forbidden action, and HQ return address. Delegation carries existing authority and
never adds commit, push, issue, publish, release, merge, or destructive permission.

For implementation and diagnosis, name the behavior or claim to prove, the real
surface and starting state, and the expected evidence. Accept screenshots or
recordings for visual behavior; logs, commands, API results, or other explicit
results for nonvisual behavior; or `unverified: <reason>`. Require an image diff
only for fixed-reference matching through `visual-parity`.

Every initial brief and later assignment includes the exact HQ name, address, and
return channel. The owner reports when it finishes, is blocked or stuck, needs
human input, or reaches its authorized boundary. Routine chatter and unchanged
blockers stay quiet. Workers prepare human questions for HQ and do not ask the user
to enter their task.

## Route the work

Choose by what remains unsettled:

- **Plan:** answer a question or settle a design. Give constraints and the expected
  recommendation or artifact. Use `grilling`, `domain-modeling`, or `prototype`
  when useful.
- **Build:** implement an agreed outcome. Carry accepted decisions and the proof
  contract. On Claude Code, use `codex-first` when applicable.
- **Babysit:** inspect or drive an existing PR through the authorized boundary with
  `babysit-pr`.
- **Diagnose:** establish a reproducible cause with `diagnosing-bugs`; return the
  diagnosis before widening into a fix.

For a normal durable implementation task, put the literal `/ossian-mode` command
as the first content line of its user-visible kickoff prompt. Omit it for bounded
subagents, research-only work, human-in-the-loop prototypes, read-only status, or
explicit local-only work. Those routes state their own scope directly.

## Delivery

State the closeout route even when it is not yet authorized:

- When commit, push, and PR work are authorized, invoke `commit-push-pr` after
  verification. Its default completed PR flow owns one `babysit-pr` drive through
  review and CI to merge-ready. It never merges.
- Do not start a second babysit or feedback-resolution loop.
- Preserve narrower outcomes exactly: local diff, commit, remote branch, draft PR,
  stop at PR, read-only status, or another explicit boundary.
- In a trunk-direct repository, authorized `commit-push-pr` ends after push.

Naming a skill does not authorize its external actions.

## Dispatch

For a trivial authorized edit with one obvious change outside GitHub Copilot, HQ
acts inline and records the item and evidence. Copilot HQ delegates all repository
mutation to a verified separate worktree.

Before owner creation, mark the item `dispatching`. After creation, store the exact
owner address, expected report time, and `active` state in the same turn. Arm the
active-work heartbeat when this is the first active item. A dispatch absent from
the ledger must be reconciled before any retry.

Use `priming.md` for the complete kickoff template and skill routing.

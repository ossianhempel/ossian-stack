# Ticket brief

Copy this file to the project's `docs/agents/ticket-brief.md` and delete this
line. It is the shape of every ticket body on the issue tracker. `to-tickets`,
`to-spec`, and `triage` write it; a pickup agent reads it cold, with no chat
access and no memory of how the ticket came to be. A field you cannot fill is a
ticket that is not ready for an agent.

---

# Ticket brief

Every ticket body has these sections, in this order. Skip a section only when it
is genuinely empty, and say so (`None`) rather than omitting it.

## Goal

One or two sentences. The outcome from the user's perspective, executable by a
stranger. Not a layer-by-layer implementation list.

## Scope

What this ticket may change and what it must not. Name modules, areas, or
surfaces in the project's domain vocabulary, not file paths, which go stale.
State the branch or worktree convention if the project has one.

## Context

Pointers, not prose: the parent spec or issue, related ADRs, the prototype that
settled a decision, the prior ticket this one builds on. Paste in anything a
cold agent needs that lives only in a conversation.

## Acceptance

Checkable criteria, one per line, as a task list. The ticket is done when every
box is ticked against the real artifact, not a self-report.

- [ ] …

## Verify

The exact commands, or the project's verification skill, that prove acceptance,
plus known gotchas (flaky tests, required env, a service that must be running).

## Forbidden

Actions this ticket may not take beyond the project's standing rules: no
migrations, no dependency bumps, no changes outside scope, no force-push.

## Blocked by

References to the tickets that gate this one, or `None — can start immediately`.
Use the tracker's native blocking relation as well where it has one.

Avoid file paths and code in the body. Exception: a snippet from a prototype
that encodes a decision more precisely than prose (a state machine, reducer,
schema, or type shape). Trim it to the decision-rich part and say where it came
from.

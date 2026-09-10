---
name: codex-multi-agent
description: "Coordinate parallel Codex subagents while staying responsive to the user: read-only scouts for exploration, owned workers for the implementation, an advisor for what gets stuck. Use when a task is large enough to fan out, needs several areas explored at once, or the user asks to delegate, parallelize, or spawn agents."
---

# Codex Multi-Agent

Codex sessions only, the spawn tools are Codex's.

Stay available to the user while delegating substantive work. Send focused,
read-only scouts out in parallel, and give the implementation to owned workers.
The Roles table below fixes each role's model and effort; the last section governs
the `fork_turns` value every spawn also needs. Give each agent clear ownership,
avoid overlapping assignments, and tell leaf workers not to delegate. Bring the
results together and keep approvals with the user.

## Roles

| Role | Model | Effort | Owns |
|---|---|---|---|
| Scout | `gpt-5.6-luna` | `max` | Reading one area. Never writes |
| Worker | `gpt-5.6-sol` | `medium`, `high` when hard | One area of the implementation |
| Advisor | `gpt-6-astra` | `medium` | A question a worker is stuck on. Never writes |

Scouts run at `max` even though they only read: a scout reads a lot and returns
a little, and one that misreads costs more than it saved because every worker
downstream inherits the mistake.

The advisor is consulted, never assigned. Spawn one when a worker stalls or two
readings both look defensible; give it the question, what was tried, and the
evidence. It decides, the worker still writes. Do not reach for it before a
worker has actually failed.

## fork_turns gates every override

`model` and `reasoning_effort` are accepted only when `fork_turns` is `"none"`
or a positive integer string. On `"all"`, or with the parameter omitted, the
agent inherits the parent's model and effort and **silently ignores** what you
passed.

So scouts and workers take `"none"` and a self-contained brief. The advisor
takes a positive integer string: it needs the stuck context, and `"all"` would
drop the Astra override and hand the question back to the model that just failed.

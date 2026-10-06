---
name: architect
description: "Settle caller usage, types, signatures, and module ownership before implementing code that crosses boundaries."
---

# Architect

Shape a change before implementation when it crosses a function, module, service,
persistence, or public API boundary. Keep the process proportional. A local edit
whose contract is already obvious does not need this skill.

## Ground the boundary

Reuse current evidence of the affected subsystem's contract and ownership. Run
`how` when that evidence is missing or stale; use `why` only when ownership or
layering may encode a deliberate constraint. State the callers, data flow,
owner, and invariants. Load `codebase-design` for interface, locality, and
testability criteria; reuse its assessment if already established in this task.

## Sketch from the caller inward

1. Write representative caller usage first.
2. Derive the data shape and organizing structure: typed model, state machine,
registry, reducer, boundary parser, or other concrete form.
3. Sketch types, signatures, errors, and module ownership. Bodies may remain
pseudocode or `not implemented`.
4. Name compatibility, migration, concurrency, and persistence constraints.
5. Judge the sketch with `codebase-design` and screen for escape hatches in the
type system. Apply the findings here; do not start a separate architecture audit.

When the shape is genuinely unsettled, produce two or three structurally distinct
candidates. Use the comparison lenses bundled with `codebase-design`, isolate
the attempts, choose one base, and record what the alternatives exposed. Do not run
a bakeoff when one established repository pattern already answers the question.

Proceed to implementation when it is within the user's authorized scope; honor
design-only and review-only requests. During implementation, treat repeated
deviations of the same shape as evidence that the
architecture is wrong. Re-ground and replace the sketch instead of adding a chain
of exceptions.

## Reply

Show caller usage first, followed by the chosen data shape, public signatures,
module ownership, constraints, rejected alternatives, and any implementation
friction that invalidated the design.

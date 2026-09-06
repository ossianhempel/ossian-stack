---
name: architect
description: "Settle caller usage, types, signatures, and module ownership before implementing code that crosses boundaries."
---

# Architect

Shape a change before implementation when it crosses a function, module, service,
persistence, or public API boundary. Keep the process proportional. A local edit
whose contract is already obvious does not need this skill.

## Ground the boundary

Run `how` over the affected subsystem. Use `why` only when existing ownership or
layering may encode a deliberate constraint. State the current callers, data flow,
owner, and invariants.

## Sketch from the caller inward

1. Write representative caller usage first.
2. Derive the data shape and organizing structure: typed model, state machine,
registry, reducer, boundary parser, or other concrete form.
3. Sketch types, signatures, errors, and module ownership. Bodies may remain
pseudocode or `not implemented`.
4. Name compatibility, migration, concurrency, and persistence constraints.
5. Screen for pass-through layers, leaked implementation details, temporal
coupling, shared mutable state, and escape hatches in the type system.

When the shape is genuinely unsettled, produce two or three structurally distinct
candidates. Isolate the attempts, judge them against caller simplicity and hidden
complexity, choose one base, and record what the alternatives exposed. Do not run
a bakeoff when one established repository pattern already answers the question.

Proceed to implementation unless the user requested a design checkpoint. During
implementation, treat repeated deviations of the same shape as evidence that the
architecture is wrong. Re-ground and replace the sketch instead of adding a chain
of exceptions.

## Reply

Show caller usage first, followed by the chosen data shape, public signatures,
module ownership, constraints, rejected alternatives, and any implementation
friction that invalidated the design.

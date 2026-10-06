---
name: codebase-design
description: "Design or assess module interfaces, hidden complexity, dependency seams, and testability. Supplies design criteria to architecture and structural refactoring; skip mechanical edits and readability-only cleanup."
---

# Codebase Design

Design **deep modules**: substantial behavior behind an interface callers can
understand easily. Concentrate knowledge, changes, and verification where that
behavior belongs. Judge depth by what callers gain, not implementation line count.

Use this discipline when choosing or assessing module boundaries and interfaces.
When another workflow loads it, apply the criteria to that workflow's current
sketch; return the judgment there without starting a second plan or review.
Reuse an assessment already made in this task unless new constraints invalidate
it. Mechanical renames, moves with settled ownership and contracts, and local
readability cleanup do not need it.

## Vocabulary

Use the project's established domain terms and framework names. The terms below
clarify design reasoning; they do not require renaming a service, component, or API.

- **Module:** code with an interface and an implementation, from a function to a
  package or a slice spanning deployment tiers.
- **Interface:** everything a caller must know: types, invariants, ordering,
  errors, configuration, side effects, and relevant performance constraints.
- **Implementation:** the code and internal decisions behind that interface.
- **Depth:** useful behavior per obligation the caller must understand. A shallow
  module asks callers to learn almost as much as its implementation does.
- **Seam:** a place where behavior can be substituted without editing its caller.
  Choosing where substitution happens is distinct from choosing what it does.
- **Adapter:** a concrete implementation satisfying an interface at a seam.
- **Leverage:** the capability callers gain from the interface.
- **Locality:** how much related knowledge, change, and verification stays together.

## Judge the design

- **Count caller obligations, not just methods.** A short signature is shallow
  when callers still coordinate ordering, duplicate decisions, or know internals.
  Hide those decisions and mutable state with the behavior that owns them; keep
  observable errors and effects explicit.
- **Apply the deletion test.** If removing a layer removes complexity, it was
  overhead. If its behavior must reappear across callers, it was earning its keep.
  Retain a thin adapter when it owns a real translation or compatibility contract.
- **Concentrate related behavior.** Prefer a change that can be understood and
  verified locally. A deep module may use small internal parts; depth does not
  require a monolith or merging unrelated responsibilities.
- **Justify substitution.** Introduce a seam for observed variation, a meaningful
  test substitute, or a real external dependency. Two adapters are evidence of
  useful variation, not a quota or a reason to invent another implementation.
- **Test observable contracts.** Exercise behavior through the interface that
  owns it. Keep internal seams internal and useful algorithm or integration tests
  where they establish distinct behavior. Testability alone does not justify
  exposing implementation details to every caller.
- **Make effects controllable.** Prefer returned values for computation. For
  necessary I/O, use the project's dependency construction pattern to control
  external effects in tests without threading dependencies through every caller.

When reshaping a cluster around I/O or replacing its tests, read
[DEEPENING.md](DEEPENING.md). When several interface shapes remain viable, read
[DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) for comparison lenses. An established
repository pattern is sufficient when it already satisfies the constraints.

## Done

Identify the caller obligations, what the module hides, where related changes
land, and how its observable behavior can be tested. Recommend a shape or explain
why the existing one should stay. Give the calling workflow only the findings
that affect its decision. If evidence is insufficient, name the missing fact;
do not add speculative layers, widen scope, or change behavior to force depth.

---
name: refactoring
description: "Restructure working code while preserving behavior: rename, extract, move, deduplicate, or reshape modules and APIs."
---

# Refactoring

**You own the contract. The structure changes; the behavior does not.**

Distinct from adding a feature, which changes behavior, and from fixing a bug,
which corrects it. Also distinct from `simplify-code`, which makes settled code
readable in place without moving it. This skill moves things: modules, APIs,
call graphs.

A refactor that smuggles in a behavior change loses its safety net. If the
cleanup reveals a missing feature or a real bug, split it out and ship the
structural change first against the pinned contract. A redesign is allowed, but
name it as one and obtain agreement if it exceeds the authorized scope.

Split an authorized large refactor into verifiable units. Stop only at an
unresolved decision, access limit, or scope boundary; continue independent
authorized work. Size alone is not a reason to abandon the requested refactor.

## 1. Pin the behavior first

Before moving structure, identify evidence that establishes unchanged behavior.
Reuse existing characterization tests, snapshots, or an equivalence harness when
they cover the contract. Add a meaningful behavioral pin where coverage is missing.

For a mechanical transformation, a structural/type proof is sufficient only when
it actually establishes equivalence across all affected uses. Compilation alone
cannot prove runtime behavior, persisted formats, or external callers unchanged.
Keep real-artifact proof for user-visible behavior; see `principle-prove-it-works`.

Use the `how` skill first when you do not already know the contract of the
subsystem you are about to reshape.

## 2. Name the structure the code is missing

Say what shape the code is reaching for: a state machine over scattered booleans,
a table or registry over spread-out branching, a typed model over repeated shape
assumptions, a reducer over ad hoc mutation.

The reshape must **delete branches or make invalid states unrepresentable**. If
it only adds indirection, it is not the right shape. Boring code stays when the
shape is already clear and local.

## 3. Name the target shape before moving

State what the module layout, types, and call graph should be if this were built
today — the `principle-redesign-from-first-principles` shape, where the new
requirement reads as if it had been there on day one. Write it down before the
first move, so the moves have something to aim at and you can tell when you have
arrived.

If the right shape is not obvious, do not pick the first one. Sketch two or three
and compare them before committing, per `principle-exhaust-the-design-space`.

## 4. Subtract before you add

Delete dead weight, collapse one-caller wrappers, drop redundant validators, and
remove orphan references **before** introducing the new shape. Deletion shrinks
the surface the reshape has to cover.

The smallest change that reaches the target shape ships. A speculative cleanup
that "might help" gets reverted, not left to ride.

## 5. Move in small behavior-preserving steps

Each step keeps the pin green. Migrate all callers controlled by this change.
Retain compatibility required by deployed clients, persisted data, public APIs,
or callers outside scope. Remove the old path only when evidence shows it is
unused; record the remaining migration boundary when compatibility must stay.

Spot-check every rename against the actual files. Renames silently miss usages
in strings, prose, comments, and back-references, and a type checker will not
catch any of them.

Mechanical edits can be delegated to a subagent, with a specific scope: the file
paths, the exact names being moved, and the behavior to hold. Review the diff
yourself. A delegate's "looks good" is not review.

## 6. Prove behavior is unchanged

On the real artifact, not "it compiles." Run the pin. For a larger reshape, run
an equivalence check: diff old-versus-new outputs, replay a recorded baseline
against the new code, or exercise the actual surface. Prefer a script that
re-runs the comparison over a one-time eyeball, so a reviewer can re-run it too.

Own the verification yourself. A delegate's summary is not proof; inspect the
artifact.

## 7. Confirm the change earned its place

The measure is **reduced reader load**: fewer layers between a question and its
answer, less hidden state, fewer indirections that have only one consumer.

If the diff does not lower reader load somewhere, revert it. A refactor that
leaves the code equally hard to read has spent risk for nothing.

## 8. Commit in ordered slices

When commits and history edits are authorized, arrange small commits that tell the story: the subtraction, then the
reshape, then any follow-on cleanup — so a single revert undoes one slice. Each
slice is behavior-preserving and green before the next begins.

## Reply

The structure that changed, the pin you held it against, the equivalence proof,
the reader-load delta, and what shipped versus what you reverted. No new
behavior.

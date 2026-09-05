---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer."
disable-model-invocation: true
---

# Sequence work into verifiable units

Order work as a sequence of small units, each ending in a state you can check, and don't advance until the current one is green. The same discipline runs at two altitudes, how you execute and how you deliver.

**Why:** A break caught at the unit that caused it is cheap to localize. A break caught after a batch is buried, and you have already built further on a broken base. Sequencing those same units into a delivery a reviewer can replay turns "trust me" into "watch it go red, then green."

**Execution.** Choose a coherent, independently verifiable unit. Independent
mechanical edits may form one unit. Check after each logical unit before building
on it; the unit need not be one line or one file. Preserve unrelated work and
compare against the baseline required by the project's branching conventions.

**Delivery.** Capture failing-before-passing evidence when fixing a bug, without
requiring a broken commit. Follow the project's history and CI rules. When
commits are authorized, order green slices so a reviewer can follow the proof:
baseline before treatment, subtraction before reshape, scaffold before feature.

**Pattern:**
- Pick the smallest unit that ends in a check: an edit plus its test, or a commit that stands alone.
- Verify before advancing. Red to green per unit, never deferred to a final batch.
- Order the units so the sequence builds confidence on its own, for you while executing and for a reviewer reading the stack.

The sequencing complement to `principle-prove-it-works`, which keeps each check real. Reuse a runnable verification helper when it makes the per-unit check cheap.

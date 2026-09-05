---
name: how
description: "Explain code behavior, runtime flow, architecture, or ownership. Use for how/where questions; use why for historical rationale."
---

# How

Explain code behavior, runtime flow, architecture, and ownership from the actual
source. Build a working mental model at the depth the user needs. Use `why` for
historical motivation; code shape alone does not establish intent.

## Investigate in proportion to the question

- For a function, utility, or narrow ownership question, inspect the relevant
  implementation and callers and answer directly. No separate explainer is needed.
- For a cross-service flow, trace the path from trigger to effect. Delegate
  independent slices when separate contexts add value and the host supports them;
  use its supported agent interface and configured available models. Otherwise
  investigate sequentially inline and identify any coverage limitation.
- Give each delegate a distinct scope and source paths. Reuse returned evidence,
  reconcile contradictions, and follow unresolved links yourself. Do not repeat
  an exploration merely to pass the answer through another model.
- State a reasonable interpretation of an ambiguous target and proceed with
  useful reads. Ask only when the missing decision changes the work materially.

The answer is ready when the relevant path is supported by source and remaining
gaps are explicit. Reference the files and symbols that let the reader verify it.

## Explain, then critique when requested

Lead with the behavior and develop the flow, concepts, ownership, and gotchas that
matter to this question. Omit sections that add no value. The explanation should
stand alone, without forcing a critique on a user who only asked how it works.

For requested architectural critique, understand the architecture first, then use
the critique rubric. Independent critics are useful for substantive uncertainty;
use available configured models, not provider-specific tool arguments. If no
subagents exist, apply the rubric inline and do not claim independent review.
Judge findings as act on, consider, noted, or dismissed, with concrete reasons.
Do not edit code during an explanation or critique unless that is also requested.

## References

- [Explorer prompt](references/explorer-prompt.md): when delegating an independent source slice.
- [Explainer prompt](references/explainer-prompt.md): for a substantial subsystem explanation and its presentation style.
- [Critique rubric](references/critique-rubric.md): when architectural critique is requested.
- [Critic prompt](references/critic-prompt.md): when a separate critic would add useful independent judgment.

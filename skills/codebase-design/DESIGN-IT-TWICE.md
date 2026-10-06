# Compare Interface Shapes

Use these lenses when the current design workflow needs alternatives. The
workflow owns exploration and selection; this reference does not start another
bakeoff, require agents, or introduce a user approval gate.

Compare two or three structurally different shapes against the same real callers,
domain terms, invariants, compatibility constraints, and dependency behavior.

- **Smallest caller burden:** concentrate coordination and decisions behind a
  small interface, without hiding failures or important effects.
- **Common caller first:** make the observed default use simple and judge what
  exceptional callers must still know.
- **Real variation:** put substitution where dependencies or supported use cases
  actually differ; do not optimize for hypothetical flexibility.

For each shape, show caller usage, the full contract, what implementation details
it hides, where changes land, and how behavior is verified. Compare leverage,
locality, and seam placement; recommend one base and record the trade-off that
matters. Serial sketches suffice. Use isolated agents only when the host and
scope allow them and independent attempts would resolve meaningful uncertainty.

Reuse a comparison already made in the task. Do not explore alternatives when
one established repository pattern already answers the design question.

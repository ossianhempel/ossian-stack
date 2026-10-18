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

## Compare and decide

The main agent sketches the candidates sequentially. Keep the original
requirements and hard constraints fixed across the comparison. For each shape,
show caller usage, the contract, what it hides, where changes land, and how its
behavior can be verified. Apply the lenses above plus relevant migration,
operating-cost, and implementation-complexity constraints; use evidence and
explicit tradeoffs instead of invented numeric scores.

Use a short comparison in the existing task record:

| Candidate | Caller and owner | Hard constraints | Decisive failure case | Cost and proof |
| --- | --- | --- | --- | --- |
| Each viable shape | Usage and ownership | Met, unmet, or uncertain, with reason | A realistic scenario that challenges its claim | Migration/operation cost and the check needed |

Compare each candidate against the same decisive scenarios. A sketch's predicted
behavior is not observed proof: run a small probe when resolving an uncertainty
could change the choice. Choose one base, state why alternatives lost, and name
the remaining proof obligations. If combining ideas, recheck the combined design
against the original constraints. A design that weakens an agreed product promise
requires an explicit scope decision before implementation; record that tradeoff
instead of silently changing the comparison criteria.

An optional single reviewer can challenge the proposed choice when meaningful
uncertainty remains. Give it the original requirements, alternatives, rationale,
and unresolved questions. The main agent owns the decision and implementation.
Keep the comparison in the current plan or thread; create a separate artifact
only when the project's established decision-record convention calls for one.

Reuse a comparison already made in the task. Do not explore alternatives when
one established repository pattern already answers the design question.

---
name: simplify-code
description: "Simplify working code within the named scope while preserving behavior. Use for readability, unnecessary complexity, and excessive state."
---

# Simplify Code

Take code that works and make it consumable. Not a rewrite of the feature, not a
bug hunt, not a style pass. The output does exactly what the input did, in a
shape a reader can hold in their head.

Run it when a unit has settled — before review, commit, or handoff. Do not run it
while the change is still being shaped; it fights you.

## Scope

Resolve scope in this order, and stop at the first that yields code:

1. A file, directory, or description the user named
2. The branch diff against its base
3. Staged plus unstaged changes
4. Files edited in this conversation
5. Ask

**A named scope is never widened.** Edits stay inside it and the import and
export seams it forces. If the right fix lives outside, say so and leave it.

Stop with "nothing to simplify" on a scope that is only generated files,
lockfiles, vendored code, dependency bumps, or formatting. On a mixed diff, keep
the hand-written code and drop the rest.

## Order of operations

Subtract, then collapse, then polish. This order matters: deletion shrinks the
surface, which usually makes the next simplification obvious, and polishing code
you are about to delete is wasted work.

1. **Subtract.** Remove what is not strictly required — dead paths, unused
   exports, speculative validators and guards, compatibility shims for earlier
   forms of this same unshipped change, comments that restate the identifiers.
   Design for observed usage, not imagined edge cases.
2. **Collapse.** Reduce the number of states the code can be in: fewer
   arguments, narrower types, unions instead of loose combinations.
3. **Polish.** Naming, early returns, line count.

Never polish before you cut. This ordering is the `principle-subtract-before-you-add` skill, restated here because `simplify-code` needs it every run.

## The standard

Rules 1-14 are the standard. Rules 15-17 extend it with the failure modes a
maintainer feels but a fresh reader does not. The numbers are stable; refer to
them by number in your report.

**Cut**

- [7] Remove any change that is not strictly required.
- [8] Bias for fewer lines of code.
- [17] Sweat the small leaks. Remove tiny pass-throughs, representation leaks,
  and duplicated choices before they spread. Small leaks compound into permanent
  coordination costs.

**Reduce the state space**

- [2] Minimize possible states: fewer arguments, remove or narrow any state.
- [3] Use discriminated unions to cut the number of states the code can be in.
- [6] Be highly opinionated about parameters. Assert on load.
- [13] Never pass overrides except where strictly necessary. Keep argument count low.
- [14] Do not make an argument optional if it is actually required.
- [15] Consolidate decisions. Do not repeat the same choice in several places.
  Put it behind one source of truth and pass the result as a simple flag.
- [16] Question the threading. When a change asks you to pass a new signal
  through types, schemas, pipelines, or similar layers, stop and look for a more
  direct path.

**Trust your types**

- [4] Handle every variant of a multi-type value exhaustively. Fail on unknown.
- [5] Do not write defensive code. Assume values are what the types say.
- [12] Use asserts instead of try/catch or default values when you expect
  something to exist.

**Keep it readable**

- [1] Write extremely simple code. It should be skimmable and still understandable.
- [9] No clever code.
- [10] Do not break out into too many functions. That is hard to read. Keep the
  call hierarchy flat: if answering one question means tracing through more than
  three files or layers, flatten it. A rich interface that hides substantial work
  is not a deep call chain.
- [11] Early returns are good.

Rules 5 and 12 are the ones that feel wrong and are not: a default value or a
swallowed exception hides the case where your assumption broke. An assert states
the assumption and fails at the point it stops holding. A guard added to silence
a crash is a symptom fix; it leaves the real cause in place and makes the next
reader believe the condition is expected.

**Fix the pattern, not the instance.** When a finding is a shape rather than a
one-off — the same duplicated decision, the same falsely optional argument, the
same swallowed exception — search the scope for every other occurrence and fix
them in one pass. Fixing one and leaving five teaches the next reader that the
shape is fine.

**The test all seventeen serve:** writing code is cheap for you, which makes
over-engineering easy. Borrow a human maintainer's fatigue instead. If a
developer would find this exhausting to maintain, it is a bad solution, however
correct it is. Be lazy. Stay simple.

## The adversarial pass

Use an adversarial pass when substantive complexity remains or independent review
would resolve uncertainty. A clean reduction with sufficient relevant checks does
not require another review cycle. When needed, dispatch the following independent
lenses through the host's supported agent mechanism, concurrently where available.

| Reviewer | Reads | Rules |
| --- | --- | --- |
| `references/reviewers/skimmability.md` | top to bottom, cold, at reading speed | 1, 7, 8, 9, 10, 11, 17 |
| `references/reviewers/state-space.md` | signatures, types, and call sites | 2, 3, 4, 5, 6, 12, 13, 14, 15, 16 |

Two, because those are the two ways the rules split. One reviewer reads as a
newcomer and reports where it slowed down; the other counts reachable states and
reports which are impossible. They find different things. More lenses than that
just produce overlapping reports of the same rules.

Give each reviewer the persona file's contents as its instructions, plus the
**paths** of the files in scope. Do not paste the file bodies into the prompt;
let it read them. Give it nothing else — no diff, no original, no history, no
account of why anything is the way it is. Anything you add re-anchors it to the
shape you are trying to escape.

Apply the reductions yourself. The reviewers read, you edit. A reviewer that
edits its own findings produces conflicting changes and no coherent view of the
state space.

Where the host cannot run a subagent, read the persona files and apply them
inline as two separate passes — but re-read the files from disk first and judge
only what is on the page, not what you remember writing.

Repeat only for substantive unresolved findings, at most three passes. Stop when
relevant checks and review are clean; repeat verification only when new edits or
evidence invalidate it. Report any remaining material uncertainty.

Neither reviewer can tell you whether behavior changed; they have no baseline.
That is what the tests are for.

## What must not change

Behavior is fixed. Verify, do not assume.

Never relax an assertion, weaken a type signature, delete a test, or skip a
check to make things pass. Never remove a safety check — trust-boundary
validation, data-loss protection, security, accessibility — because a rule above
called it boilerplate. Rule 5 governs values your own types already guarantee,
not input crossing a trust boundary.

A compatibility path may go only when it has no deployed, persisted, public,
external, or in-repo caller outside the scope, and every caller update it forces
still fits inside the scope.

When a rule and a safety check conflict, the safety check wins and you report the
conflict rather than resolving it silently.

## Verify

Run the project's own typecheck, lint, and tests — whatever this repo actually
uses, discovered from its config and scripts, not assumed. Scope the tests to the
blast radius, and widen when a shared helper moved.

If a check fails, fix the regression or revert that one simplification. Never
paper over it. Report which check failed and which way you went.

## Report

Keep it short:

- What changed, by rule number
- Passes run, and what the last one found
- Anything skipped, and why — a rule that would have broken behavior, a fix that
  fell outside the scope, a safety check that outranked a rule
- Checks run and their results

State line counts before and after only when the reduction is large enough to be
the point.

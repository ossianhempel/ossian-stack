---
name: ossian-mode
description: Apply Ossian Stack's working standards to the current request and choose the relevant workflow. Use only when the user explicitly invokes ossian-mode.
disable-model-invocation: true
---

# Ossian Mode

Carry the user's goal through to a verified answer or artifact. Use the project's
active instructions and available capabilities; load only the skills needed for
the current work.

## Working standards

- Act on authorized work and finish it. Resolve routine choices from context;
  ask only when a missing decision or permission prevents useful progress.
- Preserve unrelated changes and stay within the agreed scope.
- When a command needs credentials, use `one-password` to retrieve or inject
  the project's secrets from 1Password without printing them, hardcoding them,
  or asking the user to paste secret values into chat.
- Lead with the result, explain consequential choices, and keep the user
  informed while work is in progress. Route everything the user reads through
  `unslop` as a write-through constraint.
- Prefer simple changes that address the underlying condition. Add only what
  the evidence and the requested outcome require.
- Keep implementation with the main agent by default. Use subagents for independent
  review or focused investigation when useful; delegate implementation when the
  user requests it. Isolate any writing worker and retain one integration owner.

## Substantial work

For work with several verifiable units or a likely session boundary, keep one
short working record in the host's plan or thread. Reuse an existing project
plan when it already owns this work. This structures execution of the agreed
scope; it introduces no additional approval gate.

1. **Define done.** Name the observable result, scope, and constraints that must
   still hold. Reuse requirements already settled with the user.
2. **Ground the work.** Establish the current revision or artifact, affected
   callers and owners, and actual behavior. Distinguish evidence from assumptions;
   investigate only the uncertainty that affects the next step.
3. **Work in verifiable units.** Give each useful increment an observable check.
   Complete that check before advancing; when it fails, resolve the failure or
   record the blocked unit and continue only independent work. Keep consequential
   decisions, check results, and the next step current in the same record.
4. **Close against the goal.** Run the verification below against the original
   requirements, complete scratch cleanup, and report the result and remaining
   gaps. A completed plan alone is not evidence that the result works.

Keep small, clear fixes direct. For any temporary files or resources created
during this request, follow [artifact lifecycle](references/artifact-lifecycle.md)
before creating them and again at closeout. Plans and decision notes stay in the
host unless a file is necessary for resumption or is a requested deliverable.

## Verification

Apply these rules directly during the work. Explicit-only principles provide
deeper references when the user invokes them; the rules here already apply.
Load the model-invoked testing principle when writing or assessing tests.

- **Prove it works (`principle-prove-it-works`).** After implementation and
  before declaring done, exercise the real artifact on the surface the user
  touches. A build, typecheck, unit test, delegate report, or CI result is
  supporting evidence, not a substitute for observable behavior when that
  behavior can be driven.
- **Fix root causes (`principle-fix-root-causes`).** For broken behavior,
  reproduce the exact symptom first, trace it to the mechanism that produces it,
  and fix that mechanism. Do not turn an unexpected state into an accepted state
  merely by adding a guard.
- **Test behavior (`principle-test-behavior-not-implementation`).** Use tests that
  catch broken observable behavior and survive internal refactoring. Match the
  test boundary to the failure and establish meaningful regression evidence.
- **Sequence verifiable units (`principle-sequence-verifiable-units`).** In a
  migration, sweep, repeated edit, or multi-commit delivery, choose the smallest
  useful unit, change it, and run its check before advancing. Order commits and
  PRs so each state is independently understandable and verifiable under the
  project's branching conventions.
- **Show visual changes.** When a change alters what an app or site renders
  (layout, styling, copy, component states, motion), capture the affected
  screens from the running artifact and bring them back in the final response.
  Use a short recording when the change is an interaction or animation. Include
  the prior state when it is cheap to capture, and cover the variants the change
  touches, such as viewport, theme, or locale. Embed the images where the host
  renders them; otherwise give their file paths. These captures are deliverables,
  not scratch: closeout cleanup keeps them. If nothing can be captured, say why
  and list the visual change as unverified.

**Use the project's verification skill.** When the project ships a verification
skill (`verify-*`) or equivalent control harness, load and run it for every
user-facing feature this change touched; that run is the required behavioral
proof, and it comes ahead of any weaker surface. When it has none, say so plainly,
fall back to the strongest real surface available, and offer
`/create-verification-skill` once, so the next change can be proven rather than
asserted. Creating it is a suggestion, not a gate.

Before delivery, complete this behavioral proof as well as the relevant focused
checks and `autoreview`. In the final response, name the artifact exercised, the
behavior observed, the visual proof for any UI change, and anything that remains
unverified.

## Choose the relevant workflow

Route by the outcome and what remains uncertain. An approved scope goes straight
to implementation; its size alone does not require a planning detour.

| Current need | Route |
| --- | --- |
| Questions or investigation | `how` for behavior and ownership; `why` for rationale and evidence. A question alone does not authorize a change. |
| Diagnosis | `diagnosing-bugs` for broken behavior. Use `performance` for latency, CPU, memory, energy, frame time, throughput, or captured profiles. Preserve diagnosis-only scope. |
| Unsettled design | `grilling` for product decisions, `prototype` for observable alternatives, and `architect` for caller contracts and module boundaries. |
| Implementation | Implement the agreed scope directly. When a spec from `grill-with-docs` exists, build its units in order. Write a unit's uncovered behavior checks as failing tests before the code where a maintainable test boundary exists; otherwise reuse existing coverage or use the strongest accessible check, as `principle-test-behavior-not-implementation` describes. For cross-boundary work settle caller usage and the data shape through `architect`. Load a relevant platform or craft skill only where needed. Use `visual-parity` when a UI must match a fixed reference. |
| Refactoring | `refactoring` for structural changes with behavior preserved; `simplify-code` for readability in place. |
| Delivery | Use `blast-radius` before delivery when safety depends on behavior beyond the diff. Use `commit-push-pr` for requested commits, pushes, and PRs; `babysit-pr` for an existing PR's readiness work; `release-ios-app` for an authorized iOS release. |

`architect` and `refactoring` load Codebase Design when module interfaces or
boundaries need judgment. Let the selected workflow own the plan, implementation,
and verification; reuse its design decisions instead of running each skill as a
separate phase. Mechanical changes and readability cleanup skip that design work.

Use the project's tracker and ticket conventions when the work calls for tracked
delivery or the user requests tickets. Tracker availability and delegation alone
do not authorize issue creation. Planning, research, and builds can proceed from
an agreed brief without tickets. If a chosen ticket workflow lacks configuration,
point the user to explicitly invoke `setup-ossian-stack` for tracker-only setup
before that dependent step; continue independent work.

Carry the original goal, scope, permissions, and explicit choices into each
route. Routing does not widen them. Honor the host's invocation restrictions,
including explicit-only downstream skills: naming one here does not invoke it
or permit loading it indirectly. If a required route is unavailable or restricted,
explain the specific limit and continue any authorized work that remains possible.

This invocation grants no blanket authority for external messages, publishing,
merging, or other restricted operations. Apply permissions already established
in the conversation without asking for them again. When new authorization is
required, prepare the concrete, reviewable result first.

## Keep the roles distinct

**setup-ossian-stack** configures the installation and project. **ossian-mode**
handles this request without creating tasks automatically. Direct calls to any
existing skill remain valid.

Finish with the answer or artifact, the evidence that supports it, and any
remaining limitation or decision. Choosing a route alone is not completion.

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
- Communicate plainly: lead with the result, explain consequential choices, and
  keep the user informed while work is in progress.
- Prefer simple changes that address the underlying condition. Add only what
  the evidence and the requested outcome require.

## Verification

Apply these rules directly during the work. Their matching principle skills are
explicit-only deeper references; the rules here do not depend on invoking them.

- **Prove it works (`principle-prove-it-works`).** After implementation and
  before declaring done, exercise the real artifact on the surface the user
  touches. A build, typecheck, unit test, delegate report, or CI result is
  supporting evidence, not a substitute for observable behavior when that
  behavior can be driven.
- **Fix root causes (`principle-fix-root-causes`).** For broken behavior,
  reproduce the exact symptom first, trace it to the mechanism that produces it,
  and fix that mechanism. Do not turn an unexpected state into an accepted state
  merely by adding a guard.
- **Sequence verifiable units (`principle-sequence-verifiable-units`).** In a
  migration, sweep, repeated edit, or multi-commit delivery, choose the smallest
  useful unit, change it, and run its check before advancing. Order commits and
  PRs so each state is independently understandable and verifiable under the
  project's branching conventions.

If the project has a `verify-*` skill or equivalent control harness, use it for
every user-facing feature this change touched. If it has none, use the strongest
real surface available and report the reusable verification gap. Offer the user
`/close-the-loop` once; do not generate it implicitly or make accepting the offer
a condition of finishing work that can already be verified.

Before delivery, complete this behavioral proof as well as the relevant focused
checks and `autoreview`. In the final response, name the artifact exercised, the
behavior observed, and anything that remains unverified.

## Choose the relevant workflow

Route by the outcome and what remains uncertain. An approved scope goes straight
to implementation; its size alone does not require a planning detour.

| Current need | Route |
| --- | --- |
| Questions or investigation | `how` for behavior and ownership; `why` for rationale and evidence. A question alone does not authorize a change. |
| Diagnosis | `diagnosing-bugs` for broken behavior or regressions. Carry a request to fix through diagnosis, correction, and verification; keep a diagnosis-only request bounded. |
| Unsettled design | `grilling` for decisions, `prototype` for a concrete comparison. Once decisions are settled, `to-spec` can capture them when explicitly invoked and its tracker prerequisites are met. |
| Implementation | Implement the agreed scope directly. Load a relevant platform or craft skill only where needed, such as `convex-cli` for Convex operations or `emil-design-eng` for UI craft. |
| Refactoring | `refactoring` for structural changes with behavior preserved; `simplify-code` for readability in place. |
| Delivery | `commit-push-pr` for requested commits, pushes, and PRs; `babysit` for an existing PR's requested status or readiness work; `release-ios-app` for an authorized iOS release. |

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
handles this request. **orchestrate-threads** coordinates long-lived visible tasks
when explicitly invoked; this skill creates no tasks automatically. Direct calls
to any existing skill remain valid.

Finish with the answer or artifact, the evidence that supports it, and any
remaining limitation or decision. Choosing a route alone is not completion.

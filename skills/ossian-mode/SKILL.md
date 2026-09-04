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
- Verify the actual behavior or artifact before claiming success. Use focused
  checks that can expose the failure; report unavailable evidence as unverified.

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

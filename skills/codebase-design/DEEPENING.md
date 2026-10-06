# Deepening

Assess whether related behavior scattered across modules should sit behind one
interface. Use the vocabulary and criteria in [SKILL.md](SKILL.md). Dependencies
constrain the test strategy; their category alone does not justify a merge.

| Dependency | Design and verification |
| --- | --- |
| In-process computation or state | Test the owned behavior directly through its interface. Combine only responsibilities that belong together. |
| Local I/O with a test substitute | Use an existing local database or filesystem substitute when it preserves the relevant semantics. Keep the setup internal; use real integration checks for guarantees the substitute cannot establish. |
| Remote service you own | Keep transport separate from domain decisions where that improves locality. Use an injected adapter when substitution is useful, and retain contract or integration checks against the actual service. |
| Third-party service | Control calls through the project's existing client or adapter seam. Use a fake or mock for local behavior, with provider contract or integration evidence for assumptions that mocks cannot prove. |

Prefer the project's established construction and injection pattern. A fake is
useful when it enables a meaningful behavioral check, not merely because it
counts as a second adapter. Do not expose internal test setup through the public
interface or invent ports around every dependency.

## Preserve behavior while moving tests

Pin the existing behavior before changing structure. Add checks at the new
interface for outcomes and invariants, including errors and effects. Retain
algorithm, integration, compatibility, and regression tests with distinct value.

Remove an old test only when evidence shows that its behavior is covered by the
new checks or its subject is no longer part of the supported contract. Passing
new tests alone is not proof of equivalent coverage. Never drop a failing test
to make the reshape pass. If replacement coverage is uncertain, retain the test
and report the gap. The calling refactor owns migration and equivalence proof;
this reference supplies the design and test-surface judgment.

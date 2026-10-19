---
name: principle-test-behavior-not-implementation
description: "Choose and review tests that protect observable behavior and survive internal refactoring. Use when writing regression tests, assessing test quality, or deciding whether coverage proves a change."
---

# Test Behavior, Not Implementation

For each test, identify the observable contract it protects, the realistic defect
that would make it fail, and an internal refactor it should tolerate. Derive
expected results from the contract, not by copying the production algorithm.

Use the cheapest boundary that reaches the behavior. A public function's unit
test is enough for a self-contained rule; use integration or real-surface checks
when persistence, transport, lifecycle, or user interaction causes the failure.
Test caller-visible results, state, errors, and side effects. Private method
names, collection layout, incidental call order, and copied style constants are
poor assertions unless that detail is itself the agreed contract.

Use representative inputs and state transitions. Exercise the production path;
fixtures that only prove they were constructed correctly do not validate it.
Control time, randomness, and external dependencies when needed. Mocks belong at
external boundaries and must preserve the relevant contract; mocking away the
behavior under test removes the evidence.

For an important regression, run the test against the original defect or a
deliberately broken behavior and confirm it fails for the expected reason, then
passes with the fix. A compile error is not that failure. Use a disposable copy
for deliberate breaks and restore the working implementation before validation.
Do not claim failing-before-passing evidence unless it was observed.

Reuse meaningful existing coverage. Add a test when it protects a distinct
behavior at a maintainable boundary; skip duplicates and assertions that merely
freeze implementation details. If the correct boundary is unavailable, report
what remains unproven and use the strongest accessible check. Passing tests only
support the behavior and boundary they actually exercise.

During review, make a test gap actionable by naming the important changed
behavior that remains unproven and the failure the current check would miss.
Apply the review's normal severity and scope rules. Test counts, coverage
percentages, and preferred test structure alone do not justify another fix cycle.

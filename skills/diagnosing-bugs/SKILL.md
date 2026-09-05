---
name: diagnosing-bugs
description: "Diagnose and fix bugs or performance regressions using a reproducible signal and verified root cause. Preserve diagnosis-only scope."
---

# Diagnosing Bugs

Scale the investigation to the uncertainty. For a narrow bug with a clear failure signal, reuse that evidence, test the cause, fix within scope, and verify the original symptom. Use the full playbook below for uncertain, intermittent, or cross-system failures. Diagnosis-only requests stop at findings and proposed fixes.

**You own this task.** Delegate independent investigation or implementation when useful and supported;
otherwise work inline. Stay in the lead. Reviewing a delegate's diff is yours; so is every decision about what the
evidence means.

## Evidence discipline

Be scientific. Every shipped line traces to runtime evidence.

Belt-and-suspenders that "might help" is a hypothesis, not a fix; it does not
ship. When evidence refutes a hypothesis, revert what it motivated. The smallest
change the evidence justifies ships, nothing more. The same holds for performance
work, where the evidence is a trace rather than a log.

Before exploring, read the project's `GLOSSARY.md` if it has one, for the terms
and mental model of the modules involved, and check any architecture decision
records covering the area you are touching.

## Redact

This skill has you show commands, outputs, and captured artifacts. **Redact every
secret first**: write `<REDACTED>` in its place. Build loops against env vars, so
the credential stays in the environment rather than in what you show. Captured
artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight**
pass/fail signal for the bug (one that goes red on _this_ bug), you will find the
cause; bisection, hypothesis-testing, and instrumentation all just consume it. If
you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give
up.**

**Drive it yourself.** Do not hand the repro to the user. A debugging protocol
that says to ask the user does not override this; you drive the instrumented
runtime. Ask only with a stated, specific reason you cannot reach the target, and
only after driving it as far as it goes. If the project has a verification skill,
that is your surface — reach for `close-the-loop` when it has none and the bug
lives behind a UI, CLI, or service you cannot otherwise drive.

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **Human-in-the-loop script.** Last resort. If a human must click, drive _them_ with the bundled template so the loop is still structured, and feed the captured output back to yourself. Copy it out of the skill directory before editing — set the path inline, in the same command, since shell state does not persist between calls:

    ```
    SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>";
    cp "$SKILL_DIR/scripts/hitl-loop.template.sh" ./hitl-loop.sh
    ```

    It gives you two helpers: `step "<instruction>"` shows an instruction and waits
    for Enter, `capture VAR "<question>"` reads a response back. Captured values
    print as `KEY=VALUE` at the end for you to parse. Leave signing in and other
    actions to `step`; use `capture` for observations only.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one
is tight, a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger
100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake
bug is debuggable; 1% is not, so keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to
whatever environment reproduces it, (b) a redacted captured artifact (HAR file,
log dump, core dump, screen recording with timestamps), or (c) permission to add
temporary production instrumentation. Continue useful read-only source investigation
within scope, labeling hypotheses as unverified. Do not claim a verified fix
without evidence from the affected path.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one
command** (a script path, a test invocation, a curl) that you have **already run
at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human in the loop only via the template above.

Read source as needed to construct the loop and candidate explanations. A theory
is not a confirmed cause: use the failure signal to discriminate before changing
behavior or claiming the bug fixed.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Won't reproduce directly? Force it: synthesize the trigger, tighten conditions, or
instrument until it fires. A bug you cannot reproduce, you cannot prove fixed.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**.
Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop
after each cut, and keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving
parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them
makes the loop go green.

Minimise further only while it helps distinguish plausible causes; a clear, narrow
repro need not be reduced as a separate exercise.

## Phase 3: Hypothesise

When the cause remains uncertain, generate and rank competing hypotheses before
committing to one. For hard bugs, 3–5 candidates can counter anchoring; do not
invent alternatives after direct evidence already establishes the cause.

Use `how` for an unclear mechanism and `why` for relevant regression history.
Delegate independent investigations when useful and supported; reuse established
facts instead of starting both investigators for every bug.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain
knowledge that re-ranks instantly ("we just deployed a change to #3"), or know
hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't
block on it; proceed with your ranking if the user is AFK.

**Eliminate, don't confirm.** Each pass, take the split that cuts the most
remaining problem space, get runtime evidence, and rule candidates out until one
survives.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable
at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the
end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead:
establish a baseline measurement (timing harness, `performance.now()`, profiler,
query plan), then bisect. Measure first, fix second.

**Confirm the mechanism before you design the fix.** A fix grounded on a
plausible-but-unconfirmed cause can be entirely coherent and entirely wrong, while
the real cause sits one subsystem over.

## Phase 5: Fix + regression test

Fix at the root, not the symptom — see `principle-fix-root-causes`. A guard that
silences the crash leaves the bug in place and teaches the next reader that the
condition is expected.

If the fix crosses a function boundary, decide its shape before writing it; when
the shape is not obvious, sketch two and compare rather than taking the first
(`principle-exhaust-the-design-space`). Implementation can go to a subagent with a
specific scope: the files, the mechanism you confirmed, and the behavior to hold.
Review the diff yourself — a delegate's summary is not review.

Write the regression test **before the fix**, but only if there is a **correct
seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it
occurs at the call site. If the only available seam is too shallow (single-caller
test when the bug needs multiple callers, unit test that can't replicate the chain
that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase
architecture is preventing the bug from being locked down. Flag this for the next
phase.

If a correct seam exists:

1. Reuse a test that catches this failure, or turn the minimised repro into one.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

Verify on the same surface the bug appeared on. "Inconclusive" or a different
surface is not a pass; flag it. Unit tests show branch behavior, not bug absence —
the proof is the Phase 1 loop going green (`principle-prove-it-works`).

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro passes; reuse the Phase 5 result unless cleanup or new evidence invalidated it
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes and any copied loop script deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns

Keep failing-before-passing evidence without requiring a broken commit. When
commits are authorized, follow the project's green-history and CI conventions.

## Reply

What was broken, the root cause, the fix, and how you verified it. Paste the
failing-then-passing repro output verbatim.

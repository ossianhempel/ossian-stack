---
name: hillclimb
description: "Improve one measurable thing against a target in a loop: one change, one measurement, keep or revert. Use for sustained metric work (latency, bundle size, eval score, build time); a one-off fix is diagnosing-bugs or performance."
---

# Hillclimb

You own the metric and the experiment's integrity. Supervise and review; the
attempts themselves can be delegated.

The discipline is one change, one measurement, keep or revert. Never stack
untested changes, and never claim a win from code inspection: a win is a number
from the frozen harness (`principle-prove-it-works`).

1. **Ground the workload, then fix the metric.** Trace the target and name the
   realistic workload dimensions that can move the result (data size, history,
   state, concurrency). Pick a case that reproduces the user's complaint; if
   none does, fix the repro before climbing. Then fix one metric, the direction
   that counts as better, and a checkable stop predicate that pairs a target
   with a floor on attempts, so a lucky early win can't end the run ("at least
   50% better than baseline and at least 10 iterations"). Use the user's numbers
   when given; otherwise propose them and proceed.
2. **Build the harness, prove it, freeze it.** Script the measurement rather
   than running it by hand; the script is what a reviewer reruns. Run
   contrasting realistic workloads and confirm the target case reproduces the
   symptom while easier cases separate as expected. If the harness can't tell
   them apart, revise the workload or metric. Vet it with
   [references/benchmark-checklist.md](references/benchmark-checklist.md) and
   make it print its error count and a count of the work done. Frozen means one
   repeatable command that emits the metric, sampled enough to clear noise
   (median of N, not one run). Record the baseline and a green run of the
   regression gate (the tests that must keep passing) before any change.
3. **Open the decision log.** A `decision.tsv` outside the tree (or gitignored),
   one row per attempt: id, hypothesis, change, before, after, delta, tests,
   verdict (kept or reverted), note. Read it before each attempt.
4. **Ground each hypothesis in the architecture from step 1.** Name a specific
   mechanism ("defer X off the boot path because it blocks first paint"), not
   "try memoizing something". For a performance metric, try in this order:
   eliminate unused work, reduce input, cache repeated work with explicit
   invalidation, batch fixed overhead, defer unused work, move required work off
   the interactive path, add an index or queue that removes more cost than it
   adds.
5. **Loop, one hypothesis per iteration** (`principle-sequence-verifiable-units`):
   - Make the change, or hand it to a subagent with a tight scope when the host
     has them, and review the diff. Keep bulk output (logs, traces, long files)
     in subagents and carry summaries in the main thread. Run independent
     hypotheses in parallel only with each attempt in its own worktree, and keep
     yourself as the one integration owner.
   - Measure before and after with the frozen harness and run the regression
     gate.
   - Keep the change only when the metric moves past noise and the gate stays
     green. Otherwise revert it in full; a tweak that "might help" is reverted.
   - One commit per kept change, staging only the files it touched
     (`git add <files>`). Log the row either way.

   Each iteration ends in its check before the next begins. For an unattended
   run, use the host's scheduled wakeup to resume the loop.
6. **Push past the first plateau.** After several rejects in a row, pivot
   category, combine near-misses, re-read the source, or try something more
   radical before calling the hill climbed. Correctness and simplicity outrank
   the number: revert a win that breaks behavior, and keep a simplification
   that holds the number.
7. **Stop** when the predicate is met, or when the remaining ideas are marginal
   and not worth their cost. Keep the predicate fixed, and keep going while
   cheap untried hypotheses remain. If you are stuck, say so with the log rather
   than spinning.
8. **Deliver** the kept commits in the order they landed through
   `commit-push-pr`, when delivery is authorized.

## Reply

The metric and target, baseline to final with the percent delta, iterations run
(kept vs reverted), each kept change on one line, the `decision.tsv` path, and
the best idea you would try next if pushed further.

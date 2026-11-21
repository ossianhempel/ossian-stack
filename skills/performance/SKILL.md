---
name: performance
description: "Diagnose live performance or analyze captured profiles; hands sustained metric improvement to hillclimb."
---

# Performance

Choose the mode from the evidence the user has and preserve diagnosis-only scope.
Every claim rests on a measured workload, not source inspection alone.
Vet each baseline, harness, and reported number with
[references/benchmark-checklist.md](references/benchmark-checklist.md) before
planning from it or reporting it.

## Live diagnosis

Use when the symptom is latency, CPU, memory, energy, frame time, throughput, or
an intermittent runtime glitch.

1. Define the user-visible workload and metric.
2. Capture a baseline on the affected surface with the platform's profiler.
3. Reduce the artifact to a hot path, retainer chain, wait reason, or repeated
work, then map it to source.
4. Confirm the mechanism with focused instrumentation or a controlled change.
5. If a fix is requested, change the dominant cause, capture the same metric
again, and compare equivalent workloads.

## Captured-artifact diagnosis

For an existing trace, profile, memgraph, heap snapshot, or spindump, keep the
artifact fixed. Convert large structured captures into a queryable representation
when useful. Attribute the dominant samples or retainers to symbols and source.
A paired before/after capture can confirm a regression; a single capture supports
a strongest hypothesis, not automatic certainty. Stop at diagnosis unless asked
to fix it.

## Metric improvement

For a sustained target (improve one metric until it meets a threshold), run
`hillclimb`. It owns the frozen harness, the keep-or-revert loop, the decision
log, and the stop predicate. Ground its hypotheses in the trace from a diagnosis
above.

## Reply

Give the workload, metric, baseline, final measurement or diagnosis, delta,
artifact paths, confirmed mechanism, kept and reverted attempts, and remaining
uncertainty.

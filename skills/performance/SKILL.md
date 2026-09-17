---
name: performance
description: "Diagnose live performance, analyze captured profiles, or improve one metric through measured experiments."
---

# Performance

Choose the mode from the evidence the user has and preserve diagnosis-only scope.
Every claim rests on a measured workload, not source inspection alone.

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

For a sustained target, freeze one repeatable measurement command, prove it
separates realistic workloads, sample enough to clear noise, and record the
baseline. Run one hypothesis per iteration:

1. State the mechanism.
2. Make the smallest relevant change.
3. Measure with the frozen harness and run the behavior regression gate.
4. Keep a change only when the metric moves beyond noise and behavior holds.
5. Revert non-wins completely.

One accepted change per
commit when commits are authorized. Never loosen the target to declare success.

Candidate strategies come from the trace: eliminate unused work, reduce input,
cache repeated work with explicit invalidation, batch fixed overhead, defer unused
work, move required work away from the interactive path, or add an index or queue
that removes more cost than it adds.

## Reply

Give the workload, metric, baseline, final measurement or diagnosis, delta,
artifact paths, confirmed mechanism, kept and reverted attempts, and remaining
uncertainty.

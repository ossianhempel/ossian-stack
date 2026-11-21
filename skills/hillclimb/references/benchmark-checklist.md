# Benchmark checklist

Vet every performance number before you report it or act on it: a baseline, a
before/after, a regression claim, a frozen harness, or a choice between options.
Answer each question with evidence from a run, not a guess about the code.

For a quick ballpark the user asked for, one run is enough. Still check
questions 4 and 7, and say that it is one run. A choice between options is never
a ballpark.

## Before you run anything

- Write down the claim you expect to make, in the words you would ship ("export
  is 30% faster at p50 on the 60k-row dataset"). The questions test that sentence.
- Read the measurement script. Note what it times, counts, and ignores.
- Check whether the machine is busy (load average, core count, other processes).
  If you cannot quiet it, interleave the sides so both see the same noise, and
  say so in the report.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you do not report,
   because profilers slow the work down. Use CPU per process, a runtime
   profiler, I/O wait, and syscall counts, then map the hot spot to source. If
   the load generator saturates first, you measured the load generator. If a
   change did not move the number, the limiter explains why.
2. **Was it tuned?** Run every side the way production runs it: release builds,
   production flags and environment, batching, connection pools, caches as warm
   or cold as production sees them, same versions and data. If one side runs on
   defaults, you compared configurations, not implementations. Tune it and
   measure again, or do not pick a winner from that run.
3. **Did it break limits?** Do the arithmetic against disk and network
   bandwidth, cores times cost per operation, and the share of time the changed
   piece took. Removing a piece that takes 10% of the run can make the run at
   most about 11% faster. A result past a limit measured a cache, a no-op, or a
   bug.
4. **Did it error?** Count failures and non-success responses, and check that
   outputs are correct, not just present. Rejections are fast; timeouts and
   retries are slow. If the script does not count errors, add the count.
5. **Does it reproduce?** Run each side at least 5 times, alternating A, B, A, B
   so warmup, caches, and drift favor neither. Report the median and range. A
   gap smaller than run-to-run variation is no measurable difference. When the
   call is close, use a rank-sum test or the harness's own statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a
   user waits on, with realistic data sizes and concurrency, and report the
   micro result as a share of the whole.
7. **Did it even happen?** Confirm the work ran inside the timed region: the
   request reached the server, the rows were written, and the code used the
   result. Lazy code (unconsumed iterators, unawaited promises, results the
   compiler can discard) and timeouts produce numbers for work that never ran.

## Verdict

Lead with faster, slower, no measurable difference, or inconclusive. Give the
number with its unit, run count, range, and limiter, for example "p50 41 ms →
33 ms, median of 7 runs per side, range 32 to 35 ms after, bound by JSON parsing
on one core." Call it inconclusive when you cannot name the limiter, a side ran
untuned, or you could not check questions 4 and 7, and name the gap.

---
name: optimise-github-actions
description: "Explicitly invoked GitHub Actions audit: reconstruct runner usage, diagnose slow or unreliable CI, and rank safe cost/speed changes. Audit requests are read-only."
disable-model-invocation: true
---

# Optimise GitHub Actions

Use only when the user explicitly invokes this skill. Measure execution, feedback
time, and reliability separately, then explain which changes are worth making.
An audit finishes with reproducible evidence and ranked recommendations; it does
not require workflow edits. Carry forward the user's existing action scope when
they also authorize fixes, commits, or shipping. Do not invent an approval gate.

## Establish the evidence

Resolve the requested accounts/repositories and time window from the conversation
and repository context. Report excluded organizations, archived repositories, and
unavailable billing/protection data. Do not infer account-wide coverage from the
current checkout. Use available read interfaces; the optional Python 3 adapter
uses an authenticated GitHub CLI and only GET requests:

```bash
SKILL_DIR="<absolute directory containing the SKILL.md you just read>";
python3 "$SKILL_DIR/scripts/measure.py" OWNER/REPO OTHER/REPO --days 30 --out work/actions-usage.json
```

Read [measurement](references/measurement.md) for window semantics, classification,
custom runner mappings, failure behavior, and equivalent API queries. Save evidence
in the user's workspace, never in the installed skill cache. If collection is
partial, report observed usage as a lower bound and the failed queries; unknown
usage is not zero. Retain run, attempt, job, runner labels, steps, source commit,
and direct URLs so workflow changes cannot silently recategorize historical jobs.

Distinguish runtime, rounded runner minutes, allowance consumption, gross current
list-price equivalents, and actual billed spend. Obtain current pricing and
billing rules from [GitHub's runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)
and [billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions).
Do not hardcode dollar rates or multiply all macOS minutes by an old fixed ratio.
Use billing records when available; reconstructed job histories are not invoices.
Keep storage and self-hosted operating costs separate from hosted compute.

## Understand the checks before cutting work

Read default-branch workflows and the source revisions behind recent relevant
runs. Preserve branch differences and pending simplifications. Trace each job's
dependencies, trigger/path selection, setup/cache behavior, timeout, concurrency,
status identity, and deployment/artifact consumer. Inspect the actual code and
scripts a filter protects, including generated inputs and workflow-layout tests.

Read applicable rulesets, branch protection, required checks, merge/update policy,
and deployment gates. An inaccessible endpoint is unknown protection, not absent
protection. Establish what exact commit or artifact deploys and what verifies it
before recommending removal of post-merge checks. A passing PR head does not prove
the merge result passed. Preserve a required reporting status when work skips.

Rank patterns using measured evidence:

- Failures and retries: inspect failing steps, annotations, logs and test results.
  Separate defects correctly caught from simulator, dependency, or runner faults;
  failed minutes are not automatically waste. Hydrate run detail when run-list
  metadata differs from job attempts. Bind each artifact/result to the failed
  attempt and its timestamps before interpreting it; a surviving result may
  belong to a successful retry.
- Repeated PR/push work: match the final PR head and successful attempt, then
  assess the merge result and deployment contract. Total push usage is not savings.
- Small jobs and matrix legs: replay per-job rounding against consolidation and
  compare the dependency chain. Fewer charged minutes can mean slower feedback;
  preserve independent cases executing/reporting after another case fails.
- Path filters and drafts: replay complete changed-file lists and actual draft
  activity. Account for shared/generated dependencies and skipped status checks.
  Final PR file lists are a weaker approximation of earlier pushes.
- Caches, checkout, and platform choice: measure setup and cache restore/export
  costs; retain history when release/incremental logic uses it. Verify native
  dependency/test parity before substituting Linux for another OS.
- Concurrency and timeouts: measure overlapping allocated attempts before claiming
  cancellation savings. Bound hung work with room for realistic slow runs; keep
  deployment serialization and cleanup. Moving work to self-hosted machines needs
  evidence of capacity, architecture, credentials, isolation, and maintenance.
- Bots, schedules, and storage: identify the actual producer. Dependabot's own
  update runs differ from normal CI on its PRs; dynamic events alone prove neither
  exemption nor waste. Current artifact/cache size does not prove historical cost.

## Make the result reviewable

Lead with scope, measured usage, failure rate, and successful feedback-time median
and p90. Define whether queue wait and earlier attempts are included. Rank findings
with direct evidence links, present configuration, proposed behavior, sample
minute/time effect, and the contract each change must preserve. Label estimates
as measured replay, candidate approximation, or unmeasured. Do not add overlapping
savings or extrapolate unstable activity into a monthly promise.

If implementation is authorized, apply small changes, validate their real safety
contracts and relevant project checks, and follow the inherited delivery scope.
Use an available workflow linter where useful. Verify live outcomes before claiming
successful deployments or realized savings. Leave a concise account of edits,
checks, unresolved evidence, and what would establish success.

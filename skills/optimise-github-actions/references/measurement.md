# Measurement contract

The optional adapter requires Python 3 and an authenticated `gh` with read access.
No packages are installed and no GitHub resources are mutated. Without that CLI,
use a connector or another authenticated GET interface against the same APIs.

`--days N` selects runs created in the N-day rolling UTC window ending at capture
time. Alternatively pass explicit ISO-8601 UTC bounds with `--start` and `--end`;
selection is start-inclusive, end-exclusive. The collector includes every job
attempt available at capture time for those runs, including later retries. This
is a run cohort, not a billing-cycle execution ledger: attempts on an older run
are outside this cohort even if executed during the window. State this limitation
when reconciling billing. Raw records, exact bounds, and capture time are retained.

The runs API limits filtered searches to 1,000 results. The adapter recursively
splits busy windows and deduplicates run IDs, then reads jobs using `filter=all`
and paginates. It hydrates each run's detail: list metadata can still describe an
older failed attempt after a successful retry. Contradictions are recorded as
warnings with both source records. If jobs reveal an attempt newer than the
hydrated detail, capture again rather than trusting that inconsistent snapshot.
Missing, non-integer, or non-positive run/job attempt identities are incomplete
evidence and cause a partial result; boolean values are not attempt numbers.
A failed/incomplete query produces a partial output, exit code 2,
and a null definitive usage total. The observed total remains a lower bound.

Runner classification uses each job attempt's labels and allocation evidence.
Cancelled/skipped jobs with no allocation evidence do not have executed runtime;
timestamps can describe queue wait. Allocated jobs without valid completion times
have unknown duration, not zero. Only positive execution rounds up per job.
In-progress jobs need another capture for completed usage.

Recognized standard hosted labels are classified as standard; `self-hosted`
identifies self-hosted allocation. Custom or larger labels remain unknown unless
verified from runner configuration and mapped explicitly. For example:

```bash
SKILL_DIR="<absolute directory containing the SKILL.md you just read>";
python3 "$SKILL_DIR/scripts/measure.py" OWNER/REPO --days 30 --runner-kind build-pool=larger --out work/actions-usage.json
```

Mappings accept `standard`, `larger`, or `self-hosted`; the standard self-hosted
label takes precedence. Do not map an unknown runner based solely on its OS.

Standard hosted execution is free in public repositories. Larger hosted runners
are chargeable even in public repositories. Dependabot's own update path has its
standard-runner exemption; ordinary CI from Dependabot PRs does not inherit it.
Self-hosted compute has no hosted-minute charge. Chargeable classifications mean
before account allowances, not money actually owed. The helper intentionally
emits no dollar estimate or fixed OS multiplier. Map verified runner size/OS/arch
to current pricing separately and label the date and any unresolved SKUs.

GitHub's official Pages guidance conflicts: the [billing exemption list](https://docs.github.com/en/billing/concepts/product-billing/github-actions#free-use-of-github-actions)
includes Pages, while [Pages creation guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site)
says private/internal Actions usage beyond allowance is charged. Verify the
actual producer and exemption using billing evidence. Recognized GitHub-generated
private Pages runs with a `dynamic/pages/` source path on standard runners remain
unknown in the adapter; public standard, self-hosted, and larger runner rules
still apply. Do not guess custom Pages jobs from a workflow name. Inspect source
and producer, then report unresolved billing classification where material.

For diagnosis and summaries, group by repository/workflow/event/job/attempt and
runner category. Derive successful latest-attempt workflow wall time from first
allocated job start through last completion; queue delay and gaps should be
reported explicitly. Step timings and cancelled/failed durations help locate work
but do not establish that it was avoidable.

## Equivalent read queries

- Repository visibility/default branch: `GET /repos/OWNER/REPO`.
- Runs: `GET /repos/OWNER/REPO/actions/runs?per_page=100&created=START..END`.
- All job attempts: `GET /repos/OWNER/REPO/actions/runs/RUN_ID/jobs?filter=all&per_page=100`.
- Workflow source: contents at the observed run's source revision, plus current
  default branch. Resolve event-specific checkout/merge refs when relevant.
- Protection: rulesets and individual ruleset details, branch protection for
  relevant branches, plus deployment environments/statuses and artifact consumers.
- PR evidence: PR metadata and complete paginated changed files; do not silently
  treat truncated file lists as complete.
- Failure evidence: check-run annotations, job logs, artifacts/test results, and
  runner diagnostics where authorized and available.

Official API contracts: [workflow runs](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository),
[workflow jobs](https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run).

---
name: autoreview
description: "Pre-commit/ship code review: Codex default; optional Claude, Amp, or Pi."
---

# Auto Review

Run the bundled structured review helper as a closeout check. This is code
review, not Guardian `auto_review` approval routing. Supply target, context, and
severity; let the reviewer choose the analysis. Verify findings before acting.

Codex review is the default when no engine is set. It uses `gpt-6.2-sol` with
`high` reasoning and reports account-access errors directly, without switching
models. Claude review is optional and uses `claude-fable-5` by default.

For user-visible behavior, pair autoreview with a check against the user's
behavior contract. Autoreview judges the change bundle; behavior validation
judges the running product or tool. Reuse current proof from the project's
verification workflow. The main agent owns this proof; an independent execution
reviewer is optional. A clean source review does not prove observed behavior.

Use when:

- the user asks for Codex review / Claude review / autoreview / second-model review
- after non-trivial code edits, before final/commit/ship
- reviewing a local branch or PR branch after fixes

Do not require autoreview for a change whose entire diff is prose-only internal
notes or `SKILL.md` documentation. Still inspect the diff directly and run the
repository's lightweight documentation validation, if any. This exception does
not cover user-facing documentation, executable examples, configuration,
scripts, generated files, or behavior changes.

## Run

Use the absolute directory containing the SKILL.md that the host loaded, whether
it is a native plugin cache, project-local skill, global skill, or source
checkout. Do not guess a cache version or rely on variables set in another shell
call. Assign the path and run the helper in the same call, from the repository
being reviewed:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
python3 "$SKILL_DIR/scripts/autoreview" --mode local
```

On native Windows, use Python 3.10+ with the same absolute skill directory
(`Join-Path`), or run `scripts/autoreview.ps1`. See `--help` for flags and
environment overrides. The helper keeps `codex exec`: native `codex review`
cannot combine explicit Git targets and custom instructions.
`--version` prints `autoreview source-sha256:<hex>` for the executing helper's
bytes without touching Git, configuration, or engines.

Choose the target explicitly when ambiguous:

| Target | Arguments | Scope |
| --- | --- | --- |
| Local work | `--mode local` | HEAD → index → working tree, including untracked files |
| Local candidate against a base | `--mode local --base <ref>` | Pinned base → index → working tree, including untracked files |
| Committed branch/PR | `--mode branch --base <ref>` | Merge-base → HEAD; excludes dirty work |
| One commit | `--mode commit --commit <ref>` | Raw parent → commit; root compares against empty tree |

`auto` selects local when dirty, otherwise branch using the PR base or
`origin/main`. Clean `main` has no implicit target; review landed work with
`--mode commit`. `uncommitted` aliases local. The helper never fetches: the base
ref must already resolve locally. A clean local review only proves there is no
local patch, so point committed, pushed, or PR work at the branch or commit diff.
For a complete PR candidate including dirty rewrites, pin the merge base:

```bash
pr_base=$(gh pr view --json baseRefName --jq .baseRefName)
merge_base=$(git merge-base HEAD "origin/$pr_base")
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
python3 "$SKILL_DIR/scripts/autoreview" --mode local --base "$merge_base"
```

An explicit local base with zero selected changes still runs the reviewer; a
complete validated report may be `scoped-clean` for that empty delta, which does
not certify the whole repository. Local mode without a base refuses an empty
candidate. Staged and unstaged states are both reviewed; index defects remain
actionable despite working-tree fixes (`INDEX-only`). Gitlink bumps are reviewed
as pin metadata, not upstream contents. For filters, line endings, submodule
pins, or collection failures, read [Git details](references/git-and-context.md).

## Context and severity

Use `--prompt` for guidance, `--prompt-file` for a context file inside the
repository, and `--dataset` for repo-relative evidence. Supply needed unchanged
files: the reviewer's sandbox is empty. Context grants no finding scope or
instruction authority. Sensitive-path, symlink, and mutation checks apply; there
is no secret-content scanning.

Branch and commit mode support repeatable `--source-context <path>` or
`--source-context-file <path>` (kept intact in every pass): frozen regular-file
blobs from the reviewed commit, never working-copy substitutes. Local mode does
not support them. Read the [source context rules](references/git-and-context.md#committed-source-context)
before use.

Default output includes P0, P1, and P2 findings. Use `--max-priority P0` or `P1`
for a narrower review, or `--max-priority P3` when the caller explicitly asks for
lower-priority findings (overrides `AUTOREVIEW_MAX_PRIORITY`). Invalid
priorities fail before preparation. No unrelated redesign, file-count
requirements, or ritual passes. Historical blame requires a verified
parent-relative patch; otherwise attribution stays unknown.

## Review depth and test evidence

The main agent owns implementation and the review → validate → fix → test →
re-review loop. Reviewers return findings in one pass; they do not implement
fixes or start another review loop.

Before the first pass, consider the consequences of a failure. When changed
behavior could lose data, cross an ownership or authorization boundary, charge
incorrectly, break migration compatibility, or fail under concurrent operations,
retries, or interruption, read [Deeper review](references/deeper-review.md). Use
it to supply a focused brief to the existing helper and exercise the
consequential failure scenarios. Start with one reviewer; add a second
independent pass with another engine only for serious consequences or material
uncertainty. File names and diff size alone do not determine depth.

For every pass, apply `principle-test-behavior-not-implementation` to changed
tests and the evidence for changed behavior. The helper includes the core
criteria in every reviewer prompt. A test gap is actionable when it leaves an
important changed behavior unproven; ordinary priority and scope thresholds
still apply. Test-count, coverage-percentage, and stylistic objections do not
prolong review.

## Engines

- Use Codex CLI by default. Honor explicit engine/model choices and environment
  settings. Use Claude only when requested or Codex is unavailable; explain why.
- Never switch review hosts after launch, or to bypass missing context,
  isolation failures, slowness, or rate limits. If no route is eligible, report
  review unavailable.
- The Codex default is `gpt-6.2-sol`, `high` reasoning, Ultrafast when the model
  catalog lists it (otherwise standard tier). The default model has no model
  retry. Network, rate-limit, capacity, and unsupported-effort errors never
  trigger a model switch. An effort-only override keeps the model.
- `--engine`, `--model`, and `--thinking` override defaults; per-engine
  environment overrides use `AUTOREVIEW_<ENGINE>_*`. `--codex-speed fast`
  selects priority; `default` selects standard.
- `--codex-no-fallback` keeps the selected Codex model and authentication route,
  disabling the access-only retries of explicit older models and
  configured-provider rerouting.
- Codex authenticates through the ChatGPT subscription by default and can retry
  once on an operator-configured command-auth provider after a live
  authentication failure.

Read [engine options](references/engines.md) before selecting another
model/effort, projecting a provider route (`--codex-config
model_provider=...`, `--codex-route`), or using Claude, Amp, or Pi. Kimi is
refused even in dry runs; never bypass that refusal. For `--engine openclaw`,
read [OpenClaw execution](references/openclaw.md).

### Subagent review without Codex CLI

If Codex CLI is unavailable and the user did not choose another helper engine,
the host may run a separate reviewer subagent with an accessible Codex model or
a comparable code-review-capable model. Do not install Codex CLI merely to
satisfy the default.

- Before launch, state why this route is used and the selected host/model. Use
  separate reviewer context, not the implementing agent's self-review; request
  review only, with no edits or publishing.
- Supply the target, full changes, required unchanged context, task
  requirements, and priority range, preserving the target scopes above.
- Require findings with priority, file/line references, impact, and evidence,
  plus an explicit statement of scope coverage and limitations. Missing context,
  truncation, or unfinished assessment means incomplete, never clean.
- Disclose that this route lacks helper-owned isolation, frozen input checks,
  and structured result validation. Report a narrative result, not helper exit
  codes or `scoped-clean`. If the workflow requires those guarantees, report
  review unavailable instead.

Choose this route only for CLI unavailability, never to bypass safety or
isolation failures, evade findings, or replace a failed launched review.

## Image review

Codex branch mode supports added single-frame PNG/JPEG/WebP with Pillow and a
vision-capable CLI/model. Before reviewing images, read
[image limits and prerequisites](references/images.md). Unsupported binary
changes fail closed. Binary deletions are reviewed as deletion metadata.
Materialize partial-clone objects before review; isolated Git disables lazy
network fetching.

## Runtime boundaries

Keep helper-owned isolation, sanitized authentication, process cleanup, Git
scope, and structured validation enabled. Never work around an isolation
failure. Codex receives the validated bundle in an empty workspace with a
read-only sandbox and ignores user config apart from authentication settings;
Claude runs in safe mode with web-only tools; Amp and Pi run without tools.
On macOS, Codex preflight rejects shared `/tmp` and `/var/tmp` roots; unset
shared `TMPDIR`/`TMP`/`TEMP` overrides. Every pass reports suspected real
credentials as P0 without reproducing values. The helper does not run an
external secret scanner; keep approved scanning, such as pull-request CI,
outside it.

Do not edit captured inputs during review; sources are verified before sending.
Text is never truncated. Large inputs are partitioned into complete passes, and
by default every change is reviewed against every evidence batch. Intact
instructions and required context must fit each pass, or preparation fails. A
failed pass never yields a partial clean result. For a large committed branch
with distinct owner contracts, `--review-batches <repo-relative-manifest.json>`
assigns explicit batches; read the [allocation contract](references/git-and-context.md#explicit-branch-allocations)
before building one. Prefer a coherent branch or PR shape whose decision surface
fits one pass for architecture-heavy changes.

- `--dry-run` checks preparation and startup without a reviewer; both dry and
  live runs print planned passes and prompt bytes.
- `--max-prompt-bytes N` sets the UTF-8 budget per prompt (default `512000`).
  Raise it explicitly only when the route accepts the complete context; the
  helper never raises it or changes model token limits.
- `--max-review-passes N` (or `AUTOREVIEW_MAX_REVIEW_PASSES`) rejects an
  over-budget plan before startup. `--engine-timeout-seconds` limits each
  process attempt. These are not token caps.

Be patient with large bundles: structured review can take up to 30 minutes.
Heartbeat lines like `review still running: ... elapsed=... pid=...` are healthy
progress. Use `--stream-engine-output` for live engine text, not extra runs. Do
not kill a review that is quiet for a few minutes; inspect the process only after
several missed heartbeats, after 30 minutes, or after an obvious subprocess
failure.

## Diagnostics and results

Keep `--output`, `--json-output`, and `--status-output` outside the repository,
with distinct destinations and a fresh status path. For path aliases, machine
status, usage, interrupted runs, or the optional `--preflight-output` summary of
a clean committed branch, read [diagnostic details](references/diagnostics-and-results.md).

| Exit | Meaning |
| --- | --- |
| `0` | `scoped-clean`, or a correct verdict with only filtered lower-priority findings |
| `1` | Accepted findings, incorrect provider verdict, or failed review attempt |
| `2` | Unfinished assessment, incomplete scope/attribution, or missing required finding |

Inspect status independently of exit code (`--expect-findings` can alter codes).
`scoped-clean` covers only the selected target and priority; `filtered` is not
clean. Resolve `incomplete` before claiming completion. `reviewer_unavailable`
means a launched reviewer failed or returned invalid output. No status or report
means no published outcome, never clean. `report_produced: true` means a
validated report exists, not that its verdict is clean.

## Contract

- Treat review output as advisory. Never blindly apply it.
- Verify every finding by reading the real code path and adjacent files. Read
  dependency docs, source, or types when the finding depends on external behavior.
- Fix likely defects and rare dangerous ones (data loss, security, money).
  Decline unrealistic or unlikely recoverable edge cases, speculative risks,
  broad rewrites, and fixes that over-complicate the codebase, with a one-line
  reason.
- Prefer small fixes at the right ownership boundary. When an accepted finding
  shows a bug class, inspect the current scope for sibling instances and fix the
  scoped class at once when practical.
- If a review-triggered fix changes code, rerun focused tests and the helper.
  Continue until the helper returns no accepted/actionable findings, only while
  the work stays inside the original task scope.
- For security-audit suppression changes, verify accepted findings remain
  auditable: suppressed findings stay in structured output, active output keeps
  an unsuppressible notice, and aggregate findings cannot hide unrelated risk.
- For regression provenance, keep roles separate: blamed code author, blamed PR
  author, PR merger/committer, current PR author, and PR/date. Without a
  traceable PR, use the blamed commit SHA, date, and author. Do not guess a
  merger.
- Do not invoke built-in `codex review` or nested reviewers from inside the
  review.
- End the source-review loop when the helper exits 0 with no accepted/actionable
  findings, even if the reviewer's output is terse. Do not rerun for a nicer
  verdict, a second opinion, or clearer closeout wording.
- If rejecting a finding as intentional, add an inline comment only when it
  explains a real invariant or ownership decision future reviewers need.
- Do not push just to review. Push only when the user requested push/ship/PR
  update.

## Scope Governor

Autoreview is a closeout gate, not permission to rewrite the task.

Before the first review, freeze a scope baseline: original request or issue,
target branch, intended behavior, owner boundary, changed files, and non-test
LOC. For inherited or already-bloated branches, use the intended PR diff as the
baseline rather than accepting all existing branch drift.

Before patching a finding, classify it:

- **In-scope blocker**: introduced by the current diff, affects the same owner
  boundary, and fixable without changing the task's contract.
- **Follow-up**: real but belongs to an adjacent bug class, sibling surface,
  cleanup, or broader hardening track.
- **Stop-and-escalate**: requires a new protocol/config/storage/public API
  contract, a different owner boundary, a release-process change, or a design
  choice outside the original request.

Stop patching and report the scope break instead of continuing when:

- a narrow PR turns into an architecture change, protocol change, migration, or
  release-process change;
- the diff grows past 2x the original files or non-test LOC without explicit
  approval to expand scope;
- two review-triggered patch cycles have not converged; pause and reclassify
  every remaining finding before another edit;
- the best fix is "define the canonical contract first" rather than another
  local inference layer;
- fixing the accepted finding would make the PR no longer describe the same
  behavior, issue, or owner boundary.

After the two-cycle pause, continue only when every remaining accepted finding
is still an in-scope blocker. Otherwise preserve the useful analysis, identify
the smallest safe landed subset if one exists, and open or request a follow-up
for the larger fix.

When the same failure persists through two fixes based on the same assumption,
use the premise reset in `diagnosing-bugs` before another patch. A finding can
remain in scope while its proposed cause is wrong.

Do not stack or push review-triggered fix commits while scope classification or
focused proof is unresolved. Keep exploratory edits local until the cycle is
proven in scope.

Critical exceptions must be explicit: active data loss, crash, broken
install/upgrade, release blocker, or concrete security exposure.

## Release Branches And Release Process

On release, beta, stable, hotfix, signing, notarization, appcast,
package-publish, or release-check work, use freeze discipline even when the
branch name is not release-like:

- Fix only release blockers, failed release infrastructure, exact backports,
  install/upgrade breakage, data loss, crashes, or concrete security exposure.
- Treat non-blocking findings as follow-ups for `main`, not reasons to broaden
  the release branch.
- Do not introduce new product behavior, config surface, protocol shape,
  migration, plugin ownership, docs narrative, or process policy unless it
  directly unblocks the release.
- Keep proof tied to the release target: exact branch/ref, failing check or
  shipped-risk reason, smallest command/proof, and whether the fix must also
  forward-port to `main`.

## Final Report

Include:

- review command used
- tests/proof run, tied to the checked revision or artifact; distinguish
  source-review results from behavior actually observed and any unverified
  requirements
- findings accepted/rejected, briefly why
- the clean result from the final helper run, or why a remaining finding was
  consciously rejected

Do not run another review solely to improve the final report wording.

## Task references

Read the reference for the task at hand; do not load every one.

- [Deeper review](references/deeper-review.md): consequential changes, focused failure scenarios, evidence, and escalation within the existing loop.
- [Git and context](references/git-and-context.md): Git collection details, source context, review batches, and runtime diagnostics.
- [Engine options](references/engines.md): model/effort overrides, provider routes, and optional engines.
- [Diagnostics and results](references/diagnostics-and-results.md): output paths, machine status, usage, and the preflight summary.
- [Images](references/images.md): image review limits and prerequisites.
- [OpenClaw](references/openclaw.md): `--engine openclaw` execution and integration.

---
summary: Evidence and limitations from a local PR-monitoring history audit, plus the resulting babysit-pr fixes.
read_when:
  - Changing babysit-pr monitoring ownership or readiness gates.
  - Comparing historical polling overhead with host activity subscriptions.
---

# Babysit history audit — 2026-10-13

The manually reviewed sample contains **eight independently composed PR-monitoring
approaches**, executed in **73 tool calls**. All eight have a visible weakness
against the full babysit readiness contract. These are lower bounds from readable
local history, not a machine-wide failure percentage. Repeating one loop is counted
as another invocation of the same approach, not another implementation.

The original October 7 audit was interrupted before any repo changes. This audit
and the fixes below were completed on October 13.

## Confirmed implementations

| Agent / work item | Calls | Visible weakness | Session ID; representative transcript lines |
| --- | ---: | --- | --- |
| Codex / GainsLog PR 240 | 47 | Repeated short loops, hardcoded heads and branch-run reads; some query errors suppressed. Uses paginated comment reads, so pagination is not the finding here. | `019fc479-d6ff-7120-affb-088ab9fb2af4`; 503, 2482, 3677 |
| Codex / GainsLog PR 231 | 4 | Stops at successful CI alone; failed checks and query failures take the same retry branch; no late-review discovery. | `019faf87-76dc-78b0-bd07-09067b523302`; 53, 61, 72, 81 |
| Codex / Middagsro PR 25 | 7 | A bot comment containing “Completed” is accepted without binding it to the current head or observation time. | `01a06e65-6f17-7751-8dd4-976b167d9664`; 4965, 4978, 5045 |
| Codex / GainsLog PR batch | 3 | Open-only rediscovery loses merged members; empty/missing data can resemble no pending CI; review gates absent. | `01a030a8-e185-7a73-970c-6997e4eff796`; 21765, 21830, 22018 |
| Claude / Top of Class PR 85 | 3 | Greps for pending; failed checks and API errors can both stop the wait. Truncated displayed checks and no review gate. | `7ccc2e2b-1506-4f97-9347-0cf38db2adc0`; 767, 960, 1025 |
| Claude / Top of Class PR 87 | 1 | Nonzero total plus zero pending is accepted without testing failed checks; stderr discarded. | `c5c473cd-a780-4146-88fd-d31e9528ed95`; 548 |
| Claude / GainsLog PR 251 | 6 | Repeated blind waits of up to 9m45s, followed by truncated check output; no early reaction to a changed state. | `a10b60b0-5973-41ca-88e6-9b0daf0d5b8f`; 2511, 2528, 2553 |
| Claude / Top of Class Web PR 36 | 2 | Stops when text contains no pending checks, excluding one check; query failures and review state not assessed. | `d6945093-4ec4-4a0a-9e7c-712ef496f117`; 1598, 1671 |

These weaknesses are observable in submitted commands. They do not establish that
each run merged incorrectly. Some runs arose from release or PR follow-through
rather than an explicit “babysit” request. User messages elsewhere explicitly
complain about stopping before CI settled or promising later fixes without a wake;
those messages establish the recurring workflow problem but are not additional
implementation counts.

## Token and cost estimate

The model rounds that emitted the 73 calls carried **17,620,820 tokens**, including
**17,541,717 cached input tokens (99.55%)**. This measures associated round workload;
the round can also contain useful reasoning. Shell-internal polls are not counted
as additional model requests. The avoidable fraction and downstream repair work
cannot be isolated reliably from these records, so there is no defensible total
for “all wasted tokens, including repairs.”

| Recorded model | Calls | Uncached input | Cached input | Cache creation | Output | Current standard API equivalent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-5.6 Sol | 61 | 52,622 | 9,833,728 | 0 | 15,901 | $4.4620 |
| Claude Opus 5 | 12 | 22 | 7,707,989 | 6,282 | 4,276 | $4.0003–4.0238 |
| Total | 73 | 52,644 | 17,541,717 | 6,282 | 20,177 | **$8.46–8.49** |

Rates checked October 13, per million tokens: GPT-5.6 Sol input $4, cached input
$0.40, output $20. All selected Codex inputs were below the 272K long-context
threshold. [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-5.6-sol).
Claude Opus 5 input $5, cache reads $0.50, output $25; cache creation is $6.25 for
five minutes or $10 for one hour, producing the narrow range above.
[Anthropic model pricing](https://platform.claude.com/docs/en/models/opus-5/overview).

This is a current standard API equivalent, not a historical invoice or subscription
cost. Priority/fast modes, historical rates, discounts, result-processing rounds,
and subsequent debugging are excluded. Codex reasoning output is already included
in output tokens and is not added twice. All selected usage events are distinct.

## Coverage and method

Read-only inventory scanned 2,099 Codex JSONL files, 532 Claude files, 328 Copilot
files, and 75 Cursor files; 201 OpenCode SQLite sessions containing 38,446 parts;
2,095 legacy OpenCode part files; 34 Gemini chat files; and T3 user-message mirrors.
T3 mirrors were not counted again as native tool executions. No JSONL read/parse
errors were reported. This does not imply complete content coverage.

Candidate extraction searched message/tool inputs for babysit/watch/monitor,
GitHub status queries, review threads, and check rollups. It then selected loop plus
sleep commands associated with PR reads. Manual review reduced 113 candidates to
73 confirmed monitoring invocations, grouped by session and PR/batch. Exclusions
included deployment-only waits, process recovery, HTTP/mutation retries, tests,
one delayed snapshot, and the audit itself. Raw keyword request matches include
replays, approval prompts and automated messages; they are not a user-request tally.

Events larger than 500,000 bytes were skipped: 118 Codex, 903 Claude, two Copilot,
five Cursor. Commands larger than 20,000 characters were excluded from the loop
candidate pass. Antigravity's 500 binary conversation stores were not decoded.
The loop heuristic can miss other languages, persisted scripts, and monitoring
without a sleep loop. Missing/deleted/offloaded history and native-only activity
also remain gaps. Confirmed commands date from July 26 through September 5.

Evidence is retained in local transcripts, identified above. Codex session IDs
resolve under `~/.codex/sessions/` or `~/.codex/archived_sessions/`; Claude IDs
resolve under `~/.claude/projects/`. Line numbers refer to the original JSONL files.
No raw conversations or credentials are copied into this repository.

## Resulting changes and proof

- One monitoring owner: use a confirmed host PR activity subscription, take shared
  checker snapshots on wakes, and disarm at handback. Status-only JSON includes
  per-PR decisions from the shared policy so the agent need not recreate its gates.
  The bundled polling command
  remains the fallback. Preserve GitHub's review-discovery window across wakes.
- Repair the shared helper rather than writing a per-request watcher. Keep query
  failures visible and readiness unverified when dependencies or access are missing.
- Fix a reproduced shared-checker defect: green CI with `REVIEW_REQUIRED` previously
  emitted READY. It now emits a `review-required` merge gate, including when drafts
  are allowed. The regression failed before the fix and passes afterward.
- Validation: 48 watcher tests pass; TypeScript checking and `bun run check` pass;
  plugin map regenerated. Native wake behavior was not exercised against a live PR.

Changes are local until committed and pushed. Installed skill caches are untouched;
a refreshed runtime session is needed to use the published revision.

# Broad historical investigation

Use this roster when the question calls for broad history or incident analysis,
or when the first sources leave meaningful gaps or contradictions. It describes
what each evidence category can add; it is not a mandatory seven-search checklist.
Discover available connectors and local tools through the current host. A missing
CLI does not prove a capability is absent. Keep investigation read-only, and do
not weaken a permission boundary to imitate another host's agent API.

Choose sources likely to discriminate the remaining explanations. Parallelize
independent source queries or delegate bounded categories when supported and
useful. A single investigator may cover related sources when that preserves
clarity. Inline/sequential investigation is the fallback, without a claim of
independent context. Record what was searched and what could not be reached.
No matching search result means only that the search found no matching record.

## Evidence categories

1. **Source control investigator**. Git history, the available source-control interface for PRs, code comments, tests. Use when local history is available. Best at surfacing *implementation-time rationale captured during review*. PR descriptions stating the problem, review threads debating alternatives, inline comments encoding non-obvious constraints, test names that encode motivating edge cases, and commit messages linking tickets or incidents. Most trustworthy because it ties directly to the diff that shipped.

2. **Issue / ticket tracker investigator** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Tickets, project docs, status updates, spec attachments. Best at surfacing *the product or business forcing function*. Customer requests ("Acme needs X for their SOC2 audit"), compliance deadlines, parent-initiative framing ("Q3 enterprise readiness"), ticket-level scope changes, and labels that categorize the motivation (`customer:*`, `incident-followup`, `compliance`, `perf-regression`). Strongest when the why is external to engineering.

3. **Long-form documents investigator** (e.g. Notion, Confluence, Google Docs, Coda MCP). PRDs, specs, RFCs, design docs, ADRs, postmortems, team pages, meeting notes. Best at surfacing *long-form design rationale*. Problem statements, explicit "alternatives considered" and "rejected approaches" sections, strategy documents that set priorities, ADRs with finalized decisions, and postmortem action items that tie directly to code. Where the why is written out before it becomes code.

4. **Real-time team chat investigator** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Feature-name and symbol searches, PR URL mentions, incident channels (`#sev-*`, `#incident-*`), author-handle activity around the ship date. Best at surfacing *real-time deliberation that never reached a doc*. Fire-drill decisions during incidents, Q&A between the PR author and reviewers, casual "we decided X because Y" threads, and rationale for small changes that didn't warrant a PRD. Especially important when the source control, ticket, and doc paper trail is thin.

5. **Infrastructure observability investigator** (e.g. Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Metrics, monitors, dashboards, logs, APM traces, formal incidents. Infra/runtime view. Best at surfacing *infrastructure and runtime reality that motivated the code*. Monitor thresholds whose numbers match code constants, metric spikes in the window right before a PR merge, dashboards created as postmortem action items, incident timelines that reference the target. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).

6. **Error / exception tracking investigator** (e.g. Sentry, Rollbar, Bugsnag, Airbrake MCP). Issues, events, stack traces, releases. Best at surfacing *the specific exceptions and error trajectories that motivated defensive or corrective code*. Stack traces that pass through the target function, issues whose first-seen/last-seen windows bracket the PR ship date, release correlations that show an error stopping at a specific version. Strongest for catch blocks, null guards, type checks, retries, and other defenses.

7. **Product analytics warehouse investigator** (e.g. Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Product-analytics events, experiment and feature-flag exposure tables, usage and billing events, query history, warehouse telemetry. Product/data view. Complements infrastructure observability by covering *user behavior and data reality* around the ship date rather than infra metrics. Best at surfacing *product and data reality that shaped the code*. Feature-usage trajectories (a step-function ramp from zero is strong evidence that this PR launched it), experiment/flag exposure data tied to ship decisions, pre-ship distributions that reveal where a threshold constant came from (e.g., `limit = 128 * 1024` matching the p99 of an upload-size column), and data-pipeline scale evidence for migrations/backfills. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.


## Delegated investigation

Provide the original question, code paths/symbols, relevant commits/PRs/tickets,
[the investigator prompt](investigator-prompt.md), and the matching category
playbook from [the source index](source-playbook.md). Include the incident
playbook when defensive code may reflect an incident. Use the host's supported
agent interface and configured available models; investigators must not write.

Synthesize directly unless the volume of findings benefits from a separate
context. For delegated synthesis, provide [the synthesizer prompt](synthesizer-prompt.md)
and [epistemics](epistemics.md). Preserve confidence language and verify cited
claims regardless of who drafted them.

# Issue Tracker

Read for tracker-only setup or a requested tracked-delivery workflow. Follow the scope and safety contract in the skill entry point.

## 7. Issue tracker and triage labels

Configure a tracker when the user chooses ticket-based work or the active project
workflow requires tracked delivery. During general setup, an absent tracker is
optional unless that workflow is chosen; report it without forcing configuration.
Configuring a tracker does not authorize creating issues.

`triage`, `to-tickets`, `to-spec`, and `wayfinder` read per-project config that, unlike the
files above, is **not created lazily** — an unconfigured tracker fails on first
use with no hint where the setting lives. Check for:

- `docs/agents/issue-tracker.md` — where issues live, which native hierarchy,
  blocking, assignment, and label operations are available, and whether external
  PRs are a request surface.
- `docs/agents/triage-labels.md` — the mapping from the five canonical triage
  roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
  `wontfix`) to the actual label strings the tracker uses.
- `docs/agents/jira-mapping.md` — optional sparse overrides for an existing Jira
  project that represents an operation differently from this plugin. Do not
  create it for a fresh setup. Copy the table from
  `jira-mapping.md`; a missing row keeps the selected tracker
  template's original behavior.
- `docs/agents/ticket-brief.md` — the shape of every ticket body. Copy
  `ticket-brief.md`, dropping its leading copy-me line; `to-tickets`, `to-spec`, and `triage`
  write it and a cold pickup agent reads it.
- `docs/agents/handoff-comment.md` — when to comment and the concise content
  needed for meaningful updates and ownership recovery. Copy
  `handoff-comment.md`, dropping its introductory copy paragraph.
  Resume from the ticket/spec, relevant handoff records, and linked evidence.
- `docs/agents/pickup-loop.md` — the prompt the user pastes into the host's
  `/loop` or a scheduled routine to have agents take `ready-for-agent` tickets
  autonomously. Copy `pickup-loop.md`, dropping its leading
  copy-me paragraph. There is no pickup
  skill: the runner is a host capability, the operations live in the tracker
  config's "Pickup operations" section.

Supported trackers, each with a ready-to-adapt template bundled with this skill:

| Tracker | Interface | Template (under `trackers/`) |
| --- | --- | --- |
| GitHub Issues | `gh` | `github.md` |
| GitLab Issues | `glab` | hand-write, mirroring the `github.md` shape |
| Local markdown | files under `.scratch/<feature-slug>/issues/` | hand-write, mirroring the `github.md` shape |
| Linear | GraphQL API via `curl` with `LINEAR_API_KEY` | `linear.md` |
| Jira | REST API via `curl`, or a repo-shipped CLI | `jira.md` |
| Azure DevOps Boards | `az` + `azure-devops` extension | `azure-devops.md` |
| Notion | the Notion MCP server (must be connected in the runtime) | `notion.md` |

If both files exist, sanity-check them against the repo: a `git remote` pointing at
GitHub with a GitLab tracker config is a mismatch worth surfacing. For a chosen
ticket workflow, if either is missing, ask where issues actually live — one question, recommended answer
first (GitHub for a GitHub-hosted repo) — and write the file after they confirm.
For a supported tracker, start from the template and fill in the project
specifics; do not improvise the command recipes. For Notion, discover existing task or issue databases with the MCP first
(fetch each hit and dedupe by data source id, since one shared Tasks database
appears as a linked view under every project page), present them, and ask whether to use one of them (shared, scoped by a `Project`
property, or dedicated) or create a new dedicated one; then map the chosen
database's actual property names in the template's table. Notion has no CLI: before
writing its config, confirm the session exposes `notion-*` MCP tools, and if not
tell the user to connect the Notion MCP in every runtime they use — the tracker
skills stop rather than fall back when the tools are absent. Keep both short; they are
configuration the skills parse, not prose. Labels default to the canonical role
names unless the tracker already uses different strings.

### Adopt an existing Jira project

The Jira template remains the default label-based setup. Before applying it to an
existing Jira project, compare repository rules with live Jira data:

1. Inspect repository instructions, existing `docs/agents/` files, contributing
   docs, PR templates, hooks/scripts, and representative branch/commit/PR history
   for Jira keys, lifecycle, hierarchy, labels, command recipes, permissions, and
   reporting rules.
2. Through the configured Jira interface, inspect project issue types and
   hierarchy, create fields, statuses by issue type, transitions on representative
   issues, link types, permissions, and representative issues for actual labels
   and field use. Treat filtered or empty results as unknown.
3. Preserve matching defaults. For each actual difference in a plugin operation,
   add one exact row to `docs/agents/jira-mapping.md`; do not copy defaults into
   the mapping. Preserve repository branch/commit/PR conventions, permissions,
   credentials, API/CLI recipes, and reporting rules directly in
   `issue-tracker.md`.

Show the discovered differences and proposed local configuration diff before
writing. A mapping records existing values and does not change Jira. Introducing
a shared Jira label, issue type, custom field, status,
transition, workflow/schema change, or other persistent Jira vocabulary or
configuration requires explicit user authorization naming that change. Permission
to configure the adapter or create ordinary tickets does not grant it. When no
existing representation fits and no Jira change is authorized, map only that
concept to a portable body fallback. If discovery is blocked, leave the mapping
unknown rather than guessing.

Existing project copies do not update when the plugin refreshes. During requested
project setup or policy refresh, compare the handoff-comment, pickup-loop, tracker
configuration, and optional sparse mapping with these templates and merge the
reporting policy into the selected project. Preserve its property/label mappings,
API recipes, claim arbitration, permissions, and other customizations; do not
overwrite whole files or edit live tickets. Apply the same policy to custom
GitLab/local tracker recipes.

Domain docs (`GLOSSARY.md`, `docs/adr/`) stay lazy — that is the section above,
not this one.

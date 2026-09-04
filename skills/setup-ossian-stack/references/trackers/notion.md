# Template: Notion (via the Notion MCP)

Copy this body into the project's `docs/agents/issue-tracker.md`, fill in the
database, the project scope, and the property mapping, and delete this line.
There is no Notion CLI in this workflow: every operation goes through the
**Notion MCP** server, which the user must connect in each runtime before this
tracker works (Claude Code: `claude mcp add` or the claude.ai connector; Codex
and Cursor: their MCP config). If no `notion-*` tools are available in the
session, stop and say so rather than falling back to local files.

The MCP tool names below (`notion-search`, `notion-fetch`, `notion-query-data-sources`,
`notion-create-pages`, `notion-update-page`, `notion-create-comment`,
`notion-get-comments`, `notion-create-database`) are the ones the official server
exposes today. If the connected server names them differently, map by capability
and record the actual names here.

**Setup decision: which database.** Ask, never assume. First discover
candidates: `notion-search` for databases whose title or schema looks like a
task, issue, or project board, then `notion-fetch` each hit and **dedupe by
data source id**: Notion's Projects & Tasks template shows one shared Tasks
data source as a linked database under every project page, so ten "Tasks"
hits are usually one database. List what remains with a one-line description
each (data source, how tickets are scoped to a project, ticket count). Then ask one
question, recommended answer first, from what you found: use an existing
shared database scoped by a `Project` (or equivalent) property, use an
existing database dedicated to this project, or create a new dedicated one.
Only create when the user chooses it. In every case one **page is one
ticket**: its properties are the state, its body is the brief, its comments
are the working log.

---

# Issue tracker: Notion

Issues and specs for this repo live in the Notion database `<DATABASE_URL>`
(data source id `<DATA_SOURCE_ID>`, from `notion-fetch` on the database URL;
queries need the id, not the URL), scoped to **`Project = <PROJECT>`**. Use the
Notion MCP for all operations. Do not use `gh issue` for tracker work.

## Scope

For a shared database: every query filters on `Project = <PROJECT>` and every
create sets it, so rows for other projects are invisible to this repo's skills.
For a dedicated database: delete this section and the `project` row below.

## Property mapping

The skills need these roles. Map each to the database's actual property and
record the mapping here; the left column is what the skills say, the right is
what the database calls it. Create missing required properties before first use.

| Role (what skills say) | Property here | Type | Required | Values |
| --- | --- | --- | --- | --- |
| title | `Name` | title | yes | ticket title |
| status | `Status` | status | yes | map these four: backlog = `<…>`, in progress = `<…>`, in review = `<…>`, done = `<…>` |
| blocked | `Status` option, or a checkbox such as `Waiting` | status option or checkbox | yes | how a blocked ticket is shown on the board |
| triage | `Triage` | select | yes | the five canonical roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, exactly one |
| project | `Project` | select, or relation to a Projects database | yes (shared db) | `<PROJECT>` as the option name, or the project page URL for a relation (`relation_contains`) |
| id | `Task ID` | auto_increment_id | no | short key for branches and commits when present |
| agent | `Agent` | rich_text | yes | claim marker: `<runtime>:<session-id>`; empty = unclaimed |
| blocked-by | `Blocked by` / `Blocks` | relation, self, two-way | yes | a row is blocked while any `Blocked by` row is not done |
| type | `Type` | select | no | `bug`, `enhancement` |
| labels | `Labels` | multi_select | no | `wayfinder:map`, `wayfinder:<type>`, project tags |
| assignee | `Assignee` | people | no | human owner; agents never set it |
| parent | `Parent item` / `Sub-items` | relation, self (Notion sub-items) | no | wayfinder map and tickets, epic and tickets |
| pr | `PR` | url | no | the pull request an agent opened |
| last-update | `Last edited time` | built-in | — | stale-claim checks |
| created | `Created time` | built-in | — | ordering |

When an optional property is missing, fall back to a line at the top of the page
body: `Blocked by: <URL>, <URL>`, `Part of: <URL>`, `PR: <URL>`. When `Type` or
`Labels` are missing, put them in `Triage`'s neighbour select if one exists, else
in the body's first line.

The **page body** is the ticket brief (`docs/agents/ticket-brief.md`). Comments
follow `docs/agents/handoff-comment.md`. Keep accepted technical decisions in
the body or a linked spec; link detailed evidence and keep execution logs out of
the durable brief.

## Reading

- **One ticket**: `notion-fetch` on the page URL or id returns title, properties,
  body, and sub-items. `notion-get-comments` for the log.
- **List**: `notion-query-data-sources` with the data source id, the project
  filter, and the role filter, sorted by created time ascending. Every list
  operation is one of these queries; `notion-search` is full-text and unranked,
  so never use it to enumerate.
- **Identifier**: the page URL. When the database has an auto-increment id
  property, branches and commits use it (`<prefix>-<id>-slug`); otherwise a
  slug of the title plus the last 8 characters of the page id.

## Writing

Only when the user explicitly asked, or a skill's contract says so.

- **Create**: `notion-create-pages` with `parent` = the data source id, the
  properties above including `Project`, and the brief as the body. New rows
  start at status backlog and `Triage: needs-triage` unless the skill says
  otherwise.
- **Comment**: `notion-create-comment` on the page, following the handoff-comment policy,
  with the project-required AI disclosure.
- **Update state or roles**: `notion-update-page`. `Triage` is single-valued, so
  a write replaces it. `Labels` is read-merge-write.
- **Close**: set status to the done value. Never delete or archive a row.

## Pull requests as a triage surface

**PRs as a request surface: no.** Notion is not a code-review surface. Record the
git platform's commands here (see the `github.md` template) if set to `yes`.
When an agent opens a PR for a ticket, set `PR` and move status to in review.

## When a skill says "publish to the issue tracker"

Create a row in the database above, scoped to the project, with the brief as
the body.

## When a skill says "fetch the relevant ticket"

`notion-fetch` the page, `notion-get-comments` for the log, then summarise parent,
sub-items, `Blocked by`, relevant ownership/handoff history, and linked evidence
before coding; the latest comment alone is not the complete context.

## Reporting

Follow `docs/agents/handoff-comment.md`: comment only on meaningful progress,
a new or changed blocker, a decision needed, or completion. Use a few sentences
with evidence links and no empty sections. Do not repeat unchanged blockers or
mirror HQ/agent coordination. Preserve the minimal claim/release/resume records
required below; those ownership transitions still need their protocol evidence.
The blocked/paused/done operations apply on state transitions, not on every poll.
Keep durable technical decisions in the ticket body or linked spec, and link
detailed evidence. Resolution comments summarize the outcome and point there.

## Pickup operations

Used by the pickup loop (`docs/agents/pickup-loop.md`) and by any agent told to
"take the next ticket". Resolve every triage role through
`docs/agents/triage-labels.md`; the role names below are the canonical defaults
for a fresh setup (if this database already uses different triage strings, the
mapping governs and the queries use the mapped values).

- **Frontier query**: `Project = <PROJECT>`, `Triage = <agent-ready role (default ready-for-agent)>`, `Agent`
  empty, status backlog or in progress, no `Blocked by` row that is not done; created
  ascending. The frontier includes unclaimed in-progress work so a paused ticket
  (claim released, status kept) resurfaces.
- **Claim**: post the claim handoff comment stating `<runtime>:<session-id>` with
  `notion-create-comment` first, then `notion-update-page` setting `Agent` to `<runtime>:<session-id>` and
  status to in progress; the comment is the session's first write. The `Agent` field alone is
  last-writer-wins, so re-fetch comments and `Agent`: the winner is the earliest claim comment,
  not the field value. On loss, clear `Agent` and take the next row.
- **Blocked**: set the blocked marker, `Triage` to the mapped `needs-info` role (the reporter can answer)
  or `ready-for-human` (judgment, access, or design), a blocked handoff comment
  with the precise question and necessary context, then clear `Agent`.
- **Paused**: a paused handoff comment, clear `Agent`, keep status in progress.
  The ticket re-enters the frontier (unclaimed in-progress work is eligible).
- **Done**: set `PR`, status in review, a done handoff comment. A human, or a
  merge-triggered hook, sets done.
- **Abandoned claim**: `Agent` set and last edited older than one working day.
  Report it; never silently reclaim.

## Wayfinding operations

Used by `/wayfinder`. The **map** is one row with sub-items as tickets.

- **Map**: one row with `wayfinder:map` in `Labels`, holding the Notes /
  Decisions-so-far / Fog body.
- **Child ticket**: a row whose `Parent item` is the map, labelled
  `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Without
  sub-items, `Part of: <map URL>` at the top of the child body.
- **Blocking**: the `Blocked by` relation, or the body-line fallback. A ticket is
  unblocked when every blocker is done.
- **Frontier query**: rows with `Parent item` = the map and status not done, drop
  any with an unfinished `Blocked by` row or with `Agent` set; created ascending,
  first wins.
- **Claim**: set `Agent`; the session's first write.
- **Resolve**: comment with the concise outcome and durable-answer link, set status done, then append a context
  pointer to the map's Decisions-so-far.

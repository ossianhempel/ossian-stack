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
ticket**: its properties are the state, its body is the description, its comments
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
| project | `Project` | select, or relation to a Projects database | yes (shared db) | `<PROJECT>` as the option name, or the project page URL for a relation (`relation_contains`) |
| id | `Task ID` | auto_increment_id | no | short key for branches and commits when present |
| agent | `Agent` | rich_text | yes | claim marker: `<runtime>:<session-id>`; empty = unclaimed |
| blocked-by | `Blocked by` / `Blocks` | relation, self, two-way | yes | a row is blocked while any `Blocked by` row is not done |
| type | `Type` | select | no | `bug`, `enhancement` |
| labels | `Labels` | multi_select | no | project tags |
| assignee | `Assignee` | people | no | human owner; agents never set it |
| parent | `Parent item` / `Sub-items` | relation, self (Notion sub-items) | no | epic and tickets |
| pr | `PR` | url | no | the pull request an agent opened |
| last-update | `Last edited time` | built-in |, | stale-claim checks |
| created | `Created time` | built-in |, | ordering |

When an optional property is missing, fall back to a line at the top of the page
body: `Blocked by: <URL>, <URL>`, `Part of: <URL>`, `PR: <URL>`. When `Type` or
`Labels` are missing, put them in another existing select property if one fits,
else in the body's first line.

The **page body** is the ticket description. Comments
follow `docs/agents/handoff-comment.md`. Keep accepted technical decisions in
the body or a linked spec; link detailed evidence and keep execution logs out of
the durable record.

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
  properties above including `Project`, and the description as the body. New
  rows start at status backlog unless the calling skill says otherwise.
- **Comment**: `notion-create-comment` on the page, following the handoff-comment policy,
  with the project-required AI disclosure.
- **Update state or roles**: `notion-update-page`. A select property is
  single-valued, so a write replaces it. `Labels` is read-merge-write.
- **Close**: set status to the done value. Never delete or archive a row.

## When a skill says "publish to the issue tracker"

Create a row in the database above, scoped to the project, with the ticket
description as the body.

## When a skill says "fetch the relevant ticket"

`notion-fetch` the page, `notion-get-comments` for the log, then summarise parent,
sub-items, `Blocked by`, relevant ownership/handoff history, and linked evidence
before coding; the latest comment alone is not the complete context.

## Reporting

Follow `docs/agents/handoff-comment.md`: comment only on meaningful progress,
a new or changed blocker, a decision needed, or completion. Use a few sentences
with evidence links and no empty sections. Do not repeat unchanged blockers or
mirror HQ/agent coordination. Preserve the minimal claim/release/resume records
the project's own protocol requires; those ownership transitions still need their
protocol evidence. Blocked, paused, and done updates are state transitions, not
routine polls.
Keep durable technical decisions in the ticket body or linked spec, and link
detailed evidence. Resolution comments summarize the outcome and point there.

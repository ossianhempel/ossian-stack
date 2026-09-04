# Template: Jira (via REST API or a repo-shipped CLI)

Copy this body into the project's `docs/agents/issue-tracker.md`, fill in the
site URL and project key, and delete this line. If the repo ships its own Jira
CLI, prefer it and record its commands here instead of the REST recipes.

---

# Issue tracker: Jira

Issues and specs for this repo live in **Jira**, project `<KEY>`, at
`<https://<SITE>.atlassian.net>`. Do not use `gh issue` for tracker work.

## Credentials

`JIRA_BASE_URL` / `JIRA_EMAIL` / `JIRA_API_TOKEN` (API token from
id.atlassian.com). If they are not exported in the shell, check the repo root for
a `.env` file before asking the user. Never commit or echo them.

## Reading

```bash
# One issue with the fields the skills need
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/<KEY>-123?fields=summary,status,issuelinks,parent,subtasks,assignee,labels" | jq

# Search (JQL)
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search/jql?jql=project%20%3D%20<KEY>%20AND%20statusCategory%20!%3D%20Done&fields=summary,status" | jq

# Comments
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issue/<KEY>-123/comment" | jq
```

Issue bodies use Atlassian Document Format (ADF) — build descriptions as
`{"type":"doc","version":1,"content":[...]}`, not plain strings.

## Writing

Only when the user explicitly asked for a ticket to be created or mutated.

- **Create**: `POST /rest/api/3/issue` with `{"fields":{"project":{"key":"<KEY>"},"issuetype":{"name":"Story"},"summary":"...","description":<ADF>}}`.
  Read the live issue types first — projects differ (`Story` may not exist; `Task`
  is the usual fallback). Honour an explicitly requested type.
- **Comment**: `POST /rest/api/3/issue/<KEY>-123/comment` with an ADF body.
- **Transition (never a field write)**: transition IDs are workflow-specific —
  discover per issue with `GET /rest/api/3/issue/<KEY>-123/transitions`, then
  `POST /rest/api/3/issue/<KEY>-123/transitions` with `{"transition":{"id":"<id>"}}`.
- **Labels**: Jira replaces the whole label array on update — read the current
  labels, merge, write back. Labels are a shared project-wide vocabulary: a new
  string becomes permanent the moment a write succeeds. Check existing labels
  before inventing one.
- **Close**: transition to the project's Done-category status.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs
as feature requests.)_ Jira has no native PR state machine; record the actual
review surface (GitHub/GitLab/Bitbucket) and its commands here when set to `yes`.

## Ticket keys downstream

Branches, commits, and PR titles carry the key: `<key>/aiescp-1234-slug` style,
e.g. `feature/KEY-1234-slug` and `KEY-1234: Title Case Description` — adapt to the
project's git conventions.

## When a skill says "publish to the issue tracker"

Create a Jira issue in project `<KEY>`.

## When a skill says "fetch the relevant ticket"

Fetch the issue plus its comments (and attachments listing) as above, and
summarise parent, children, and linked issues before coding.

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
"take the next ticket". Comments follow the policy in `docs/agents/handoff-comment.md`.
Resolve every triage role through `docs/agents/triage-labels.md`; the role names
below are the canonical defaults for a fresh setup.

- **Frontier query**: JQL `project = <KEY> AND labels = <agent-ready label (default ready-for-agent)> AND assignee IS EMPTY AND statusCategory IN ("To Do", "In Progress")`, then drop any with an inward `Blocks` link from an unresolved issue; `created ASC`. The frontier includes unclaimed `In Progress` work so a paused ticket (claim released, status kept) resurfaces.
- **Claim**: post the claim handoff comment stating `<runtime>:<session-id>` first, then `PUT /rest/api/3/issue/<KEY>-n` with the viewer's `accountId` as assignee and a transition to the in-progress status; the comment is the session's first write. The assignee field alone is last-writer-wins, so re-read comments and assignee: the winner is the earliest claim comment. On loss, set assignee to null and take the next ticket.
- **Blocked**: read-merge-write labels replacing the agent-ready label with the mapped `needs-info` or `ready-for-human` label, post a blocked handoff comment, set assignee to null.
- **Paused**: a paused handoff comment, set assignee to null, keep the status. The ticket re-enters the frontier (unclaimed `In Progress` work is eligible).
- **Done**: put the PR link in the done handoff comment (or the dev-status panel if the git integration is connected), transition to the review status. The human moves it to Done.
- **Abandoned claim**: an assignee with `updated` older than one working day. Report it; never silently reclaim.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single Jira issue (type `Epic` where the
project has one) with child issues as tickets.

- **Map**: one issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far /
  Fog body. `POST /rest/api/3/issue` with type `Epic` and label `wayfinder:map`.
- **Child ticket**: a subtask (`subtasks` field, type `Sub-task`) where the project
  supports them, otherwise a standard issue linked to the map. Where hierarchy
  isn't available, put `Part of: <map key>` at the top of the child description.
  Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: the native **Blocks** issue link — link each child to its blocker
  with type `Blocks` (the child then shows the inward "is blocked by" link):
  `POST /rest/api/3/issue/<KEY>-child/issuelinks` with
  `{"links":[{"type":{"name":"Blocks"},"inwardIssue":{"key":"<KEY>-blocker"}}]}`.
  Where issue links aren't available, fall back to a `Blocked by: <KEY>-n, <KEY>-n`
  line at the top of the child description.
- **Frontier query**: fetch the map's open children (`parent = <KEY>-map AND
  statusCategory != Done`), then drop any whose `issuelinks` contain an open
  inward `Blocks` link from an unresolved issue, or that already have an assignee;
  first in map order wins.
- **Claim**: `PUT /rest/api/3/issue/<KEY>-n` with
  `{"fields":{"assignee":{"accountId":"<account-id>"}}}` (the viewer's `accountId`
  from `GET /rest/api/3/myself`) — the session's first write.
- **Resolve**: comment with the concise outcome and durable-answer link, transition to Done, then append a context
  pointer to the map's Decisions-so-far.

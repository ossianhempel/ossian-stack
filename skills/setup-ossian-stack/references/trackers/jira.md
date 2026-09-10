# Template: Jira (via REST API or a repo-shipped CLI)

Copy this body into the project's `docs/agents/issue-tracker.md`, fill in the
site URL and project key, and delete this line. If the repo ships its own Jira
CLI, prefer it and record its commands here instead of the REST recipes.

---

# Issue tracker: Jira

Issues and specs for this repo live in **Jira**, project `<KEY>`, at
`<https://<SITE>.atlassian.net>`. Do not use `gh issue` for tracker work.

This template defines the default Jira behavior.

## Existing-system evidence

Omit this section for a fresh/default setup. For an adopted Jira project, record:

- repository sources checked for keys, hierarchy, lifecycle, labels, branch,
  commit, PR, permission, command, credential, and reporting conventions;
- Jira project metadata checked, the account/integration identity, and the date;
- unknown or permission-filtered facts; and
- the path to the sparse mapping, when differences exist.

Use the repo's existing Jira CLI or wrapper when it has read commands. With the
REST interface, the read-only discovery set is:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/project/<KEY>" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/project/<KEY>/statuses" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issue/createmeta/<KEY>/issuetypes" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issue/createmeta/<KEY>/issuetypes/<TYPE_ID>" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issueLinkType" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/mypermissions?projectKey=<KEY>&permissions=BROWSE_PROJECTS,CREATE_ISSUES,EDIT_ISSUES,ASSIGN_ISSUES,TRANSITION_ISSUES,LINK_ISSUES,ADD_COMMENTS" | jq
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issue/<REPRESENTATIVE_KEY>/transitions?expand=transitions.fields" | jq
```

Also read representative recent issues to observe actual labels, custom fields,
parent/child use, links, and workflow paths. Preserve the repository's documented
interface and recipes. Do not create or change shared Jira vocabulary or schema
without explicit user authorization naming the persistent change.

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

Issue bodies use Atlassian Document Format (ADF), build descriptions as
`{"type":"doc","version":1,"content":[...]}`, not plain strings.

## Writing

Only when the user explicitly asked for a ticket to be created or mutated.

- **Create**: `POST /rest/api/3/issue` with `{"fields":{"project":{"key":"<KEY>"},"issuetype":{"name":"Story"},"summary":"...","description":<ADF>}}`.
  Read the live issue types first, projects differ (`Story` may not exist; `Task`
  is the usual fallback). Honour an explicitly requested type.
- **Comment**: `POST /rest/api/3/issue/<KEY>-123/comment` with an ADF body.
- **Transition (never a field write)**: transition IDs are workflow-specific,
  discover per issue with `GET /rest/api/3/issue/<KEY>-123/transitions`, then
  `POST /rest/api/3/issue/<KEY>-123/transitions` with `{"transition":{"id":"<id>"}}`.
- **Labels**: Jira replaces the whole label array on update, read the current
  labels, merge, write back. Labels are a shared project-wide vocabulary: a new
  string becomes permanent the moment a write succeeds. Check existing labels
  first and obtain explicit user authorization naming any new value before its
  first write.
- **Close**: transition to the project's Done-category status.

Creating or changing a shared issue type, custom field, status, transition,
workflow/schema element, or other persistent Jira configuration likewise requires
explicit user authorization naming that change. Ordinary issue-write permission
does not grant administrative vocabulary or schema changes.

## Ticket keys downstream

Branches, commits, and PR titles carry the key: `<key>/aiescp-1234-slug` style,
e.g. `feature/KEY-1234-slug` and `KEY-1234: Title Case Description`, adapt to the
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
the project's own protocol requires; those ownership transitions still need their
protocol evidence. Blocked, paused, and done updates are state transitions, not
routine polls.
Keep durable technical decisions in the ticket body or linked spec, and link
detailed evidence. Resolution comments summarize the outcome and point there.

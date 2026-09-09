# Template: Linear (via GraphQL API)

Copy this body into the project's `docs/agents/issue-tracker.md`, fill in the
team, and delete this line. Linear has no official CLI — use the GraphQL API with
`curl`. Written from the API without a local reference install; verify field
names against <https://studio.apollographql.com/public/Linear/variant/current>
before scripting unfamiliar ones.

---

# Issue tracker: Linear

Issues and specs for this repo live in **Linear**, team `<TEAM>`. Use the GraphQL
API at `https://api.linear.app/graphql` with a personal API key
(`Settings → API → Personal API keys`).

## Credentials

`LINEAR_API_KEY` in the environment or the repo's `.env`. Send it as
`Authorization: <key>`. Never commit or echo it.

## Reading

```bash
lq() { curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" \
  -d "{\"query\":$(jq -Rs . <<<"$1")}"; }

# Who am I (claiming needs this id)
lq 'query { viewer { id name } }'

# One issue with everything the skills need
lq 'query { issue(id: "ENG-123") { id identifier title description
  state { name } assignee { name } labels { nodes { name } }
  children { nodes { identifier title state { name } } }
  relations { nodes { type relatedIssue { identifier state { name } } } } } }'

# Open issues for the team
lq 'query { team(id: "<team-uuid>") { issues(filter: { state: { type: { nin: ["completed","canceled"] } } }) { nodes { identifier title } } } }'
```

Issue identifiers (`ENG-123`) work directly as the `id` argument on `issue` queries.

## Conventions

- **Create an issue**: `issueCreate(input: { teamId: "<team-uuid>", title: "...", description: "markdown" })`.
  Resolve `teamId` with `query { teams { nodes { id name } } }`. Optional:
  `parentId` (sub-issue), `assigneeId`, `labelIds`, `projectId`.
- **Comment**: Linear has no first-class comment mutation in the public API usable
  for this workflow — record answers in the issue description or as a sub-issue
  per the resolve step below. (Re-check `issueCommentCreate` availability; the API
  has been adding it.)
- **Apply / remove labels**: `issueLabelCreate(name: "<label>")` once per
  workspace, then attach via `labelIds` on `issueCreate`, or read-modify-write via
  `issueUpdate` (the input replaces the label set).
- **Change state**: `issueUpdate(id: "ENG-123", input: { stateId: "<uuid>" })` —
  resolve state UUIDs from `workflowStates(filter: { team: { id: { eq: "<team-uuid>" } } })`.
- **Close**: transition to a `completed` (or `canceled`) state.

## When a skill says "publish to the issue tracker"

Create a Linear issue on team `<TEAM>`.

## When a skill says "fetch the relevant ticket"

Run the single-issue query above (description, state, labels, children, relations)
and summarise before coding.

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

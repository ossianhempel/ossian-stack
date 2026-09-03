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
- **Apply / remove labels**: `issueLabelCreate(name: "ready-for-agent")` once per
  workspace, then attach via `labelIds` on `issueCreate`, or read-modify-write via
  `issueUpdate` (the input replaces the label set).
- **Change state**: `issueUpdate(id: "ENG-123", input: { stateId: "<uuid>" })` —
  resolve state UUIDs from `workflowStates(filter: { team: { id: { eq: "<team-uuid>" } } })`.
- **Close**: transition to a `completed` (or `canceled`) state.

## Pull requests as a triage surface

**PRs as a request surface: no.** Linear is not a code-review surface; if the repo
connects a git platform, record its CLI commands here when set to `yes`.

## When a skill says "publish to the issue tracker"

Create a Linear issue on team `<TEAM>`.

## When a skill says "fetch the relevant ticket"

Run the single-issue query above (description, state, labels, children, relations)
and summarise before coding.

## Pickup operations

Used by the pickup loop (`docs/agents/pickup-loop.md`) and by any agent told to
"take the next ticket". Comments follow `docs/agents/handoff-comment.md`.
Resolve every triage role through `docs/agents/triage-labels.md`; the role names
below are the canonical defaults for a fresh setup.

- **Frontier query**: team issues with the agent-ready label (default `ready-for-agent`), `assignee` null, state type `backlog`, `unstarted`, or `started`, and no `blocked_by` relation to an issue in a non-done state; `createdAt` ascending. The frontier includes unclaimed `started` work so a paused ticket (claim released, state kept) resurfaces.
- **Claim**: post the claim handoff comment (or description note) stating `<runtime>:<session-id>` first, then `issueUpdate(id, input: { assigneeId: <viewer id>, stateId: <started state> })`; the comment is the session's first write. The assignee field alone is last-writer-wins, so re-read comments and assignee: the winner is the earliest claim comment. On loss, clear `assigneeId` and take the next ticket.
- **Blocked**: replace the agent-ready label with the mapped `needs-info` or `ready-for-human` label in the label set, post a blocked handoff comment, clear `assigneeId`.
- **Paused**: a paused handoff comment, clear `assigneeId`, keep the state. The ticket re-enters the frontier (unclaimed `started` work is eligible).
- **Done**: attach the PR (Linear links it from the branch name, or `attachmentLinkGitHubPR`), post a done handoff comment, transition to the review state. The merge, or the human, completes it.
- **Abandoned claim**: an assignee with `updatedAt` older than one working day. Report it; never silently reclaim.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single Linear issue with sub-issues as tickets.

- **Map**: one issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far /
  Fog body as its description.
- **Child ticket**: a sub-issue via `parentId` on `issueCreate` (or `issueUpdate`).
  Where sub-issues aren't available, put `Part of: <map identifier>` at the top of
  the child description. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: the native **issue relation** — `issueRelationCreate(issueId:
  "<child-uuid>", relatedIssueId: "<blocker-uuid>", type: blocked_by)` so the UI
  shows the dependency. Where relations aren't available, fall back to a
  `Blocked by: ENG-n, ENG-n` line at the top of the child description.
- **Frontier query**: the map's `children` (open only), dropping any whose
  `relations` contain a `blocked_by` related issue in a non-done state, or that
  have an assignee; first in map order wins.
- **Claim**: `issueUpdate(id: "...", input: { assigneeId: <viewer id> })` — the
  session's first write.
- **Resolve**: update the child description with the answer (or the comment
  mutation if available), transition to a completed state, then append a context
  pointer to the map's Decisions-so-far.

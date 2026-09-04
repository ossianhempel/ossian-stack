# Template: Azure DevOps Boards (via `az`)

Copy this body into the project's `docs/agents/issue-tracker.md`, fill in the
organization/project, and delete this line. Verify command shapes against the
installed `azure-devops` extension version before scripting against them.

---

# Issue tracker: Azure DevOps Boards

Issues and specs for this repo live as Azure DevOps work items in project
`<PROJECT>` at `<https://dev.azure.com/<ORG>>`. Use the `az` CLI with the
`azure-devops` extension.

## Setup (one-time per machine)

```bash
az extension add --name azure-devops
az login
az devops configure --defaults organization=https://dev.azure.com/<ORG> project=<PROJECT>
```

## Work item types and states

Types: `User Story`, `Task`, `Bug`, `Feature`, `Epic`. Confirm against the live
project before relying on a type for a write: `az boards work-item create --help`
does not enumerate types — list them from a query instead.

States are process-template specific (`New`, `Active`, `Closed` on Agile; `Done`
on Scrum). Discover the valid states from an existing item before transitioning.

## Conventions

- **Create a work item**:
  `az boards work-item create --title "..." --type "Task" --description "..."`.
  Tags go through fields: `--fields "System.Tags=ready-for-agent"`. Use a file for
  long descriptions: `--description @/tmp/body.md` is not supported — pass `--fields`
  with `System.Description` read from a file via `az boards work-item create ... --fields "System.Description=$(cat body.md)"`, or write the description after create.
- **Read a work item**: `az boards work-item show --id <id> --expand all` (fields +
  relations). Comments are separate: `az rest --method get --url "<ORG>/_apis/wit/workItems/<id>/comments?api-version=7.1"`.
- **List / query**: `az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC"`.
  Useful WIQL fields: `System.Id`, `System.Title`, `System.State`,
  `System.AssignedTo`, `System.WorkItemType`, `System.Tags`, `System.IterationPath`,
  `System.AreaPath`; macros `@Me`, `@Today`, `@CurrentIteration`.
- **Comment**: `az boards work-item update --id <id> --discussion "..."`.
- **Tags (the label surface)**: `System.Tags` is a semicolon-joined string, replaced
  wholesale on write — read, modify, write back: `--fields "System.Tags=ready-for-agent;wayfinder:task"`.
- **Change state**: `az boards work-item update --id <id> --state "In Progress"`.
- **Close**: `az boards work-item update --id <id> --state "Closed"` (or the
  process's done state).

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs
as feature requests.)_ PR commands: `az repos pr list`, `az repos pr show --id <id>`,
`az repos pr create`, `az repos pr update --id <id> --status abandoned`.

## When a skill says "publish to the issue tracker"

Create a work item (`az boards work-item create`).

## When a skill says "fetch the relevant ticket"

`az boards work-item show --id <id> --expand all` plus the comments REST call above.

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
Resolve every triage role through `docs/agents/triage-labels.md`; the tag names
below are the canonical defaults for a fresh setup.

- **Frontier query**: `az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.Tags] CONTAINS '<agent-ready tag (default ready-for-agent)>' AND [System.AssignedTo] = '' AND [System.State] IN ('New','To Do','Active') ORDER BY [System.CreatedDate] ASC"`, then drop any with an open predecessor (relations from `work-item show --expand all`). The frontier includes unclaimed `Active` work so a paused ticket (assignee cleared, state kept) resurfaces.
- **Claim**: post the claim `--discussion` handoff comment stating `<runtime>:<session-id>` first, then `az boards work-item update --id <id> --assigned-to <me> --state "Active"`; the comment is the session's first write. The assignee field alone is last-writer-wins, so re-read discussion and `AssignedTo`: the winner is the earliest claim comment. On loss, clear the assignee and take the next ticket.
- **Blocked**: replace the agent-ready tag with the mapped `needs-info` or `ready-for-human` tag (tags are read-merge-write on `System.Tags`), a blocked `--discussion` comment, clear `--assigned-to ""`.
- **Paused**: a paused `--discussion` comment, clear the assignee, keep the state. The ticket re-enters the frontier (unclaimed `Active` work is eligible).
- **Done**: link the PR (`relation add --relation-type "ArtifactLink"` or the PR's work-item link), a done `--discussion` comment, `--state "Resolved"`. The human closes it.
- **Abandoned claim**: an assignee with `System.ChangedDate` older than one working day. Report it; never silently reclaim.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single work item (type `Epic` or `Feature`)
with child work items as tickets.

- **Map**: one work item tagged `wayfinder:map`, holding the Notes / Decisions-so-far /
  Fog body. `az boards work-item create --title "<destination>" --type "Epic" --fields "System.Tags=wayfinder:map"`.
- **Child ticket**: a child work item via the tree hierarchy —
  `az boards work-item relation add --id <child> --relation-type parent --target-id <map>`
  (verify the exact `relation add` syntax against the installed extension with
  `az boards work-item relation add --help`). Where relations aren't available,
  put `Part of: <map link>` at the top of the child description. Labels:
  `wayfinder:<type>` tag (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: the native **predecessor/successor** dependency link —
  `az boards work-item relation add --id <child> --relation-type predecessor --target-id <blocker>`
  (child's predecessor is the blocker). Where dependencies aren't available, fall
  back to a `Blocked by: <id>, <id>` line at the top of the child description.
- **Frontier query**: children of the map with no open blockers. List children with
  a link query — `az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItemLinks WHERE [Source].[System.Id] = <map-id> AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward' MODE (MustContain)"`
  — then drop any with an open predecessor or an assignee (check the child's
  relations from `work-item show --expand all`). First in map order wins.
- **Claim**: `az boards work-item update --id <id> --assigned-to <me>` — the
  session's first write.
- **Resolve**: `az boards work-item update --id <id> --discussion "<concise outcome + durable-answer link>"`, then
  `--state "Closed"`, then append a context pointer to the map's Decisions-so-far
  field.

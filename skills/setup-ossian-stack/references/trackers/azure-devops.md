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
  Tags go through fields: `--fields "System.Tags=<tag>"`. Use a file for
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
  wholesale on write — read, modify, write back: `--fields "System.Tags=<tag>;<tag>"`.
- **Change state**: `az boards work-item update --id <id> --state "In Progress"`.
- **Close**: `az boards work-item update --id <id> --state "Closed"` (or the
  process's done state).

## When a skill says "publish to the issue tracker"

Create a work item (`az boards work-item create`).

## When a skill says "fetch the relevant ticket"

`az boards work-item show --id <id> --expand all` plus the comments REST call above.

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

# Template: GitHub Issues (via `gh`)

Copy this body into the project's `docs/agents/issue-tracker.md` and delete this
line plus anything the project does not use. Keep it configuration, not prose.

---

# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v`, `gh` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

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

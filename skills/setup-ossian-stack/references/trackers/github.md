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

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` then keep only `authorAssociation` of `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` (drop `OWNER`/`MEMBER`/`COLLABORATOR`).
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either — resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

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

- **Frontier query**: `gh issue list --state open --label <agent-ready label (default ready-for-agent)> --json number,title,body,assignees,createdAt` then drop any with an assignee or an open issue in the body's `Blocked by` line; for each survivor, `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by` and drop it when the count is above zero; oldest first.
- **Claim**: post the claim handoff comment stating `<runtime>:<session-id>` first, then `gh issue edit <n> --add-assignee @me`; the comment is the session's first write. Assignees are a set and the field alone cannot serialize overlapping runs, so re-read with `gh issue view <n> --json assignees,comments`: the winner is the earliest claim comment, not the field value. On loss, remove the assignee and take the next ticket.
- **Blocked**: swap the agent-ready label for the mapped `needs-info` or `ready-for-human` label, post a blocked handoff comment, `gh issue edit <n> --remove-assignee @me`.
- **Paused**: a paused handoff comment, remove the assignee, keep the label. The ticket re-enters the frontier (open, mapped label, unclaimed).
- **Done**: open the PR with `Closes #<n>` in the body, post a done handoff comment. The merge closes the issue.
- **Abandoned claim**: an assignee whose last handoff comment is older than one working day. Report it; never silently reclaim.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `gh issue create --label wayfinder:map`.
- **Child ticket**: an issue linked to the map as a GitHub sub-issue (`gh api` on the sub-issues endpoint). Where sub-issues aren't enabled, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies** — the canonical, UI-visible representation. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _not_ the `#number` or `node_id`). GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only — the live gate). Where dependencies aren't available, fall back to a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children (`gh issue list --state open`, scoped to the map's sub-issues / task list), drop any with an open blocker (`issue_dependencies_summary.blocked_by > 0`, or an open issue in the `Blocked by` line) or an assignee; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me` — the session's first write.
- **Resolve**: `gh issue comment <n> --body "<concise outcome + durable-answer link>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.

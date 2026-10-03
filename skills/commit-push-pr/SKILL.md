---
name: commit-push-pr
description: "Simplify and review, then commit and push completed work directly on main or develop, or create, update, and drive a PR for other branches or when project policy requires it. Route verified merged branches and worktrees to targeted cleanup."
argument-hint: "[optional: --push-only | --update | --description-only | --pr-only | --branch-only | --draft | --base <branch> | --title \"...\" | --work-items <id>]"
---

# Commit, Push, PR

Deliver completed local work through the repository's selected path. Direct-branch
delivery commits and pushes a checked-out `main` or `develop` without creating a
branch, worktree, or pull request. PR delivery opens or updates a pull request, then
continues to merge-ready through `babysit-pr` in `drive` mode. Invoking this skill
with ship intent authorizes commit and push within the user's scope. It authorizes
PR creation and follow-through only when the user requested a PR or the project's
active branching policy or branch selection requires one; it never authorizes
merging. Preserve explicit stop boundaries and narrower modes. Handoff defines when
to start or resume a PR drive.

**Every push is gated on `simplify-code` and `autoreview` (Step 3).** This holds on
every path that pushes, and most of all on a direct push to `main` or `develop`:
that push has no PR, bot, or reviewer after it, so the gate is the only review the
change gets. A session habit, a small diff, or an earlier green test run does not
waive it.

Resolve the forge from the explicit URL or selected project remote/configuration
before PR calls. GitHub/GHE uses the gh examples below with the actual host. Azure
DevOps Services uses `references/azure-devops.md` for every forge operation in
Steps 1, 6, and 7, then the same babysit follow-through. Read it first; gh commands
below do not apply to Azure. On GitLab use glab; other unsupported follow-through
providers get an explicit limitation. If no forge interface is available, push and
report the compare/create URL instead of inventing a PR or readiness. Never mix
providers or assume Azure DevOps Server support.

## Modes

- **Default**, select the delivery path from the user's request and the project's
  active branching policy. On a checked-out `main` or `develop`, commit complete
  local changes (if needed) and push that branch when policy permits. On every
  other branch, use PR delivery unless the user explicitly requests a direct push.
  When a PR was requested or is required, open or update it and follow through to
  merge-ready (see Handoff).
- `--push-only`, run the Step 3 gate, commit complete local changes (if needed),
  and push the checked-out branch, then stop. A project rule that forbids direct
  pushes still applies; report that conflict instead of bypassing it.
- `--update`, refresh an existing PR's title/body for the current branch. Requires an
  open PR; if none, report and stop. Metadata only; no commit, push, or new babysit.
- `--description-only` (add `--body-only` to print just the body), compose the title
  and body and print them. Read-only: no branch, commit, push, or PR mutation.
- `--pr-only`, open or update the PR for already-committed work. Leave uncommitted
  changes in the tree and out of the description. No review fixes or new babysit
  unless the enclosing request already includes drive follow-through.
- `--branch-only`, establish branch safety, then stop. No commit, push, or PR.
- `--draft`, open the PR as a draft. Default is ready for review; a draft is for
  deliberately early feedback.
- `--base <branch>`, target a non-default base. Without it, preserve an existing
  open PR's base rather than retargeting.

Dispatch only the steps needed by the mode; description-only and metadata-only
requests do not enter branch, commit, or push steps. A helper's narrower mode limits
that call, not an existing higher-level drive goal: return to its owner afterward.
Every step inherits that owner's action limits, including bans on rebase or retarget.

## Asking the user

When a step says "ask", use the harness's blocking question tool when one exists;
fall back to a chat question only when no tool exists or the call errors. Never
silently skip an ask.

## Step 1: Gather context at runtime

Run each as its own shell call and read exit status as data (shell state does not
persist between calls):

```bash
git status --short && git branch --show-current
git --no-pager log --oneline -10
git remote get-url origin
git rev-parse --git-dir --git-common-dir
git rev-parse --verify --quiet origin/develop
```

Resolve the default branch from `git rev-parse --abbrev-ref origin/HEAD` (strip the
`origin/` prefix, fall back to `main`). The checkout is a **linked worktree** when
the git-dir and common-dir paths differ. The repository **uses develop** when
`origin/develop` resolves. Select the delivery path before forge calls:

- Choose direct-branch delivery by default only when the checked-out branch is
  exactly `main` or `develop` and project policy permits direct pushes.
- A detached HEAD in a linked worktree selects PR delivery (Step 2). In any linked
  worktree, a new PR without an explicit `--base` targets `develop` when the
  repository uses develop, else the default branch.
- Choose PR delivery for every other branch, when the user explicitly requests a
  PR, when a PR-specific mode is used, or when the project's active branching rule
  requires changes to land through a PR.
- An explicit `--push-only`, "push this branch without a PR", or equivalent request
  selects direct delivery for another branch when project policy permits it.
- A skill name, prior habit, forge availability, or absence of a project rule does
  not override this branch routing.

Only for PR delivery, resolve the forge and check for an open PR on the current
branch (GitHub command below; Azure uses its reference):

```bash
gh pr list --head "$(git branch --show-current)" --state open --json number,title,state,isDraft,baseRefName
```

A "no pull requests" result means NO_OPEN_PR, that is normal for new work. Treat any
other `gh` failure as a blocking error, not as NO_OPEN_PR. In `--description-only`,
stay read-only: no branch switch, no fetch that mutates, no PR calls unless a PR
URL/id was supplied.

## Step 2: Delivery path and branch safety

**First read the project's own branching rule** from the project's active
instructions already in your context, then apply the selected path:

- **Direct branch.** Stay on the checked-out branch and use it as the push target.
  The default path is available only for exact `main` or `develop`; another branch
  needs explicit direct-push intent. If the user explicitly named a different
  branch, verify that it is checked out or ask before moving completed work. Do not
  create a branch or worktree. Verify that the branch is the intended work and that
  its upstream, when configured, matches the selected remote branch. Then continue
  to Steps 3-5 and stop. If project policy forbids direct pushes to that branch,
  report the policy conflict; do not silently convert an explicit no-PR request
  into a PR.

- **PR required or requested.** When the checked-out branch is the protected base,
  create a feature branch off a freshly fetched origin default:

  ```bash
  git fetch --no-tags origin <default>
  ```

  If local `<default>` has unpushed commits (`git log origin/<default>..HEAD --oneline`
  while on it), show them and ask: carry them onto the new branch, or leave them on
  local `<default>`? Never default silently, carrying foreign commits into a PR is
  worse than asking again. Then `git checkout -b <branch> "$BASE_REF"`. If checkout
  fails on uncommitted changes, `git stash push -u`, branch, `git stash pop`; surface
  pop conflicts rather than auto-resolving. If the fetch failed, branch from local HEAD
  and say base freshness was not verified.

- **Detached HEAD in a linked worktree**, do not ask. Agent harnesses create
  worktrees detached, so this is the normal shape of worktree work, not an
  ambiguity. Name a branch from the change content (the project's convention, else
  the harness's branch prefix when it has one, else `feature/<slug>`), create it at
  the current HEAD with `git switch -c <branch>` so local commits and uncommitted
  work come along, and continue with PR delivery to the worktree base from Step 1.
  The alignment check below still applies: if the detached commits are not this
  work, or carry commits outside it relative to that base, stop and ask.
- **Detached HEAD in the primary checkout**, explain a branch is required and ask;
  never commit detached.

Branch naming follows the project's convention; otherwise `feature/<slug>` from the
change content.

**Branch/task alignment before pushing.** Verify that the selected branch belongs to
this work from its name, upstream, and recent commits. For PR delivery, also compare
the PR title. If they do not align, stop and ask; pushing into an unrelated shared
branch or someone else's PR is the one unrecoverable mistake here. In autonomous
closeout, do not push into an unverified existing PR at all.

In `--branch-only` mode, stop here and report the branch state.

## Step 3: Simplify and review before committing

Mandatory whenever this invocation will push commits: default delivery on either
path, `--push-only`, and `--pr-only` when it pushes unpushed commits. Modes that
push nothing (`--update`, `--description-only`, `--branch-only`) skip it. Run it
before Step 4 so its fixes land in the commits being shipped. Under `--pr-only`,
the scope is the unpushed commits; commit gate fixes on their own and leave the
pre-existing uncommitted changes alone.

Scope is everything the push will deliver: the complete uncommitted work plus local
commits not yet on the push target (`git log @{upstream}..HEAD`, or
`origin/<default>..HEAD` when the branch has no upstream).

1. **Simplify.** Run `simplify-code` over that scope and keep its
   behavior-preserving edits.
2. **Review.** Then run `autoreview` over the same scope, including the simplify
   edits. Follow its contract: verify each finding, fix the accepted ones, rerun
   focused tests, and rerun review until no accepted actionable findings remain.

The gate is already satisfied only when both passes ran in this session over exactly
the content being pushed and nothing has changed since. A pass that declares the
scope outside its own remit (simplify's "nothing to simplify" scopes, autoreview's
prose-only exception) counts as run; record which exception applied. Skip a pass
only when the user explicitly says to in this request.

If a pass cannot run (engine unavailable, auth or tool failure), stop before
committing and report the blocker. Push unreviewed work only after the user
explicitly accepts that.

## Step 4: Commit complete work

Survey `git status`, `git diff`, and `git diff --staged`. Group the changes into
coherent logical units, one commit per unit; not one giant commit, not one per file;
2-3 commits at most, grouped at file level only (no `git add -p`). Commit only
**complete** work: leave in-progress or unrelated changes unstaged and say so.

**Never `git add .` or `git add -A`**, they sweep in `.env`, build artifacts, and
generated files. Stage explicit paths per unit:

```bash
git add path/to/file path/to/other && git commit -m "type(scope): summary"
```

Messages follow the project's commit conventions (active instructions first, else
recent commits, else Conventional Commits). Where `fix:` and `feat:` both seem to fit,
default to `fix:`, remedying broken or missing behavior is a fix even when
implemented by adding code. The summary states what changed and why it matters, not
the file list. One subject line; a short body only when the why is not obvious. ASCII
messages. Never commit secrets or large data files, flag them instead.

If the repo has pre-commit hooks, let them run and fix what they flag; `--no-verify`
only when the user asks. If a hook rejects the commit, fix and create a new commit,
do not amend the failed one. If the branch implements a plan or spec with a tracked
status, update that status to match what is shipping **before** the push.

## Step 5: Push

```bash
git push -u origin HEAD
```

If the tree is clean and everything is already pushed, this is a no-op. Never
force-push a shared branch. If the remote moved, follow the enclosing action scope:
a babysit helper reports the needed rebase to its owner and returns; outside that
restriction, fetch and rebase rather than force.

## Step 6: Compose the title and body for PR delivery

Skip Steps 6-7 entirely for direct-branch delivery.

**You MUST read `references/pr-description.md`** (in this skill's directory) in full,
its core principle governs the writing: the diff is already visible; the description
explains what the diff cannot show. Size the description to the change, use the
`## Why` / `## Scope` / `## Change outline` / `## Tradeoffs` / `## Blast Radius` /
`## Verification` section order, dropping empty sections; small PRs are a single value-led
sentence with no headers. The `## Change outline` is expected for medium/large PRs and any
change whose shape is the story: load the `show-me` skill and emit at least one concrete
fenced structural block (diff, code, tree, or table). On Azure, use those blocks rather
than mermaid, which an Azure PR body does not render.

Title: `type(scope): summary` per the reference, matching the project's conventions.
State how each check was run and its outcome; label anything you could not verify as
unverified rather than implying it passed. Then run the `unslop` pass over the title
and body, the description is user-facing prose and gets the same treatment as any
other writing.

**Tracker links are opt-in only.** Do not ask about, infer, or nag for an issue. Link
one only when the user explicitly passed `--work-items <id>` (or handed you an issue
id), then use the host's reference syntax (`Closes #<id>`); otherwise open the PR
unlinked and say nothing about it.

If `--title` was supplied, use it; otherwise compose. ASCII only.

## Step 7: Apply and report

For GitHub, write the body to a temp file and pass it by file reference, never inline
`--body "$(cat ...)"`, which can silently produce an empty body while the CLI exits 0:

```bash
BODY_FILE=$(mktemp "${TMPDIR:-/tmp}/commit-push-pr.XXXXXX") && cat > "$BODY_FILE" <<'__PR_BODY_END__'
<the composed body markdown, verbatim>
__PR_BODY_END__
```

The quoted sentinel keeps `$VAR`, backticks, and literal `EOF` inside the body from
expanding.

- **New PR** (no open PR from Step 1): `gh pr create --base "$BASE" --title "<TITLE>"
  --body-file "$BODY_FILE"`. Add `--draft` only when requested.
- **Existing PR** (default, `--pr-only`, or `--update`): preview
  before overwriting, ask: new title, the first sentence or two of the body, total
  line count. On confirmation, `gh pr edit <number> --title "<TITLE>" --body-file
  "$BODY_FILE"`. In autonomous closeout, apply directly and report what changed. If
  `--base` was given and differs from the PR's base, retarget with
  `gh pr edit <number> --base "$BASE"`; otherwise preserve the existing base.
- **`--description-only`**: print the title and body. Stop.
- Clean up the temp file.

Never merge (`gh pr merge`, `glab mr merge`, Azure `--auto-complete`) and never arm
auto-merge, landing is the user's call.

**Report:** for direct-branch delivery, report the pushed branch, commits included,
the Step 3 outcome (what simplify and review changed, or the exception that applied),
and what stayed unstaged and why. For PR delivery, report the PR URL, target branch,
the commits included, the Step 3 outcome, what stayed unstaged and why, and whether
the PR is draft or ready. In `--update` mode report the title/body changes applied;
in `--pr-only` note that uncommitted changes were left alone.

## Handoff

- **Completed, non-draft PR delivered by the default flow:** invoke `babysit-pr` in
  `drive` mode with the full PR URL and inherited action scope. Continue until
  merge-ready or a reported human/access blocker; PR creation alone is not the
  completion condition. A green CI snapshot is not the handoff: let the watcher
  complete its review-discovery window and any detected Codex, Copilot, or other
  review automation before accepting `READY`. The handoff mode is `drive` for
  every PR size; a `check` snapshot is not follow-through. Tell the user you will
  follow the PR only as far as `babysit-pr` reports its watch armed, and end the
  report with its CI/review state and watch state.
- **Build phase still open:** finish the agreed stack or batch first, then drive its
  lowest unmerged PR (the frontier). Do not block on each intermediate PR.
- **An existing drive owns the work:** return the PR URL, changed head, and outcome
  to that owner and resume its watcher. Never recursively start a second babysitter,
  including after a follow-up PR or a narrow helper call.
- **No PR delivery:** direct-branch deliveries end after the verified push. Explicit
  stop-at-PR/no-babysit, drafts, and standalone narrow modes end at their requested
  result. Do not mark a draft ready to trigger follow-through.
- On a forge unsupported by `babysit-pr`, report the delivered PR and unverified
  follow-through limitation; never claim merge-ready from creation alone.
- After a merge, use the targeted post-merge cleanup below.

## Targeted post-merge cleanup

PR creation and merge-ready status are too early for cleanup. Before handing off a
PR, retain the exact repository, PR URL or stable ID, target branch, PR head commit,
local source branch, and auxiliary worktree path when one exists. Report cleanup as
pending when the flow stops at merge-ready. Do not poll indefinitely to wait for a
human merge.

When this workflow, its HQ, or a later invocation observes the PR as merged, verify
the merge and refresh those exact identities. Then invoke `git-cleanup` for that one
branch and worktree. Never pass a repository-wide cleanup request from this flow.
The cleanup call may remove only the recorded local branch and recorded auxiliary
worktree. It never removes `main`, `develop`, or the repository's configured default
branch, and it does not delete the remote branch without separate explicit
authorization.

If the feature branch is checked out in the primary checkout, targeted cleanup may
switch to the verified PR target only when the checkout is clean and that target is
`main` or `develop`. A dirty checkout, missing merge proof, identity mismatch, moved
branch, unexpected target, or unverified worktree keeps cleanup pending with the
exact blocker.

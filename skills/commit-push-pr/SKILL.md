---
name: commit-push-pr
description: >-
  Turn completed local work into a review-ready pull request: survey the changes,
  group them into clean conventional commits, push, and open the PR with a value-first
  description. Use when the user says "commit this", "ship this", "open a PR",
  "push and PR", or at the closeout of a unit of work. Commits locally before pushing;
  opening a PR never starts a babysit.
argument-hint: "[optional: --update | --description-only | --pr-only | --branch-only | --draft | --base <branch> | --title \"...\" | --work-items <id>]"
---

# Commit, Push, PR

Take completed local work to a review-ready pull request against the project's default
branch. Local commits are safe; the push and PR are the outward-facing act — invoking
this skill with ship intent authorizes them. Opening a PR does **not** start a babysit:
post the URL and hand back (see Handoff).

GitHub (`gh`) is the default forge. On GitLab use `glab` (merge requests); on Azure
DevOps use `az repos`; if no forge CLI exists, push and print the remote's
compare/create URL instead of failing silently. Never mix providers.

## Modes

- **Default** — commit complete local changes (if needed), push, open a PR.
- `--update` — refresh an existing PR's title/body for the current branch. Requires an
  open PR; if none, report and stop.
- `--description-only` (add `--body-only` to print just the body) — compose the title
  and body and print them. Read-only: no branch, commit, push, or PR mutation.
- `--pr-only` — open or update the PR for already-committed work. Leave uncommitted
  changes in the tree and out of the description.
- `--branch-only` — establish branch safety, then stop. No commit, push, or PR.
- `--draft` — open the PR as a draft. Default is ready for review; a draft is for
  deliberately early feedback.
- `--base <branch>` — target a non-default base. Without it, preserve an existing
  open PR's base rather than retargeting.

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
```

Resolve the default branch from `git rev-parse --abbrev-ref origin/HEAD` (strip the
`origin/` prefix, fall back to `main`). For any mode that touches the forge, check for
an open PR on the current branch:

```bash
gh pr list --head "$(git branch --show-current)" --state open --json number,title,state,isDraft,baseRefName
```

A "no pull requests" result means NO_OPEN_PR — that is normal for new work. Treat any
other `gh` failure as a blocking error, not as NO_OPEN_PR. In `--description-only`,
stay read-only: no branch switch, no fetch that mutates, no PR calls unless a PR
URL/id was supplied.

## Step 2: Branch safety

**First read the project's own branching rule** — the project's active instructions
already in your context, else recent branch names. Two shapes:

- **Default branch protected, everything lands via PR** (the common shape). Create a
  feature branch off a freshly fetched origin default:

  ```bash
  git fetch --no-tags origin <default>
  ```

  If local `<default>` has unpushed commits (`git log origin/<default>..HEAD --oneline`
  while on it), show them and ask: carry them onto the new branch, or leave them on
  local `<default>`? Never default silently — carrying foreign commits into a PR is
  worse than asking again. Then `git checkout -b <branch> "$BASE_REF"`. If checkout
  fails on uncommitted changes, `git stash push -u`, branch, `git stash pop`; surface
  pop conflicts rather than auto-resolving. If the fetch failed, branch from local HEAD
  and say base freshness was not verified.

- **Trunk-direct project** (commits land on the default branch directly). Skip branch
  creation and the PR: commit and push per Steps 3-4, then stop and report. Do not
  open a PR against a repo that does not use them.

- **Detached HEAD** — explain a branch is required and ask; never commit detached.

Branch naming follows the project's convention; otherwise `feature/<slug>` from the
change content.

**Branch/task alignment before pushing.** If the branch already exists on origin or has
an open PR, verify it belongs to this work (branch slug, recent commits, PR title vs
the current task). If it does not, stop and ask — pushing into an unrelated or
someone else's PR is the one unrecoverable mistake here. In autonomous closeout, do
not push into an unverified existing PR at all.

In `--branch-only` mode, stop here and report the branch state.

## Step 3: Commit complete work

Survey `git status`, `git diff`, and `git diff --staged`. Group the changes into
coherent logical units — one commit per unit; not one giant commit, not one per file;
2-3 commits at most, grouped at file level only (no `git add -p`). Commit only
**complete** work: leave in-progress or unrelated changes unstaged and say so.

**Never `git add .` or `git add -A`** — they sweep in `.env`, build artifacts, and
generated files. Stage explicit paths per unit:

```bash
git add path/to/file path/to/other && git commit -m "type(scope): summary"
```

Messages follow the project's commit conventions (active instructions first, else
recent commits, else Conventional Commits). Where `fix:` and `feat:` both seem to fit,
default to `fix:` — remedying broken or missing behavior is a fix even when
implemented by adding code. The summary states what changed and why it matters, not
the file list. One subject line; a short body only when the why is not obvious. ASCII
messages. Never commit secrets or large data files — flag them instead.

If the repo has pre-commit hooks, let them run and fix what they flag; `--no-verify`
only when the user asks. If a hook rejects the commit, fix and create a new commit —
do not amend the failed one. If the branch implements a plan or spec with a tracked
status, update that status to match what is shipping **before** the push.

## Step 4: Push

```bash
git push -u origin HEAD
```

If the tree is clean and everything is already pushed, this is a no-op. Never
force-push a shared branch; if the push is rejected because the remote moved, fetch
and rebase rather than force.

## Step 5: Compose the title and body

**You MUST read `references/pr-description.md`** (in this skill's directory) in full —
its core principle governs the writing: the diff is already visible; the description
explains what the diff cannot show. Size the description to the change, use the
`## Why` / `## Scope` / `## Tradeoffs` / `## Blast Radius` / `## Verification` section
order, dropping empty sections; small PRs are a single value-led sentence with no
headers.

Title: `type(scope): summary` per the reference, matching the project's conventions.
State how each check was run and its outcome; label anything you could not verify as
unverified rather than implying it passed. Then run the `unslop` pass over the title
and body — the description is user-facing prose and gets the same treatment as any
other writing.

**Tracker links are opt-in only.** Do not ask about, infer, or nag for an issue. Link
one only when the user explicitly passed `--work-items <id>` (or handed you an issue
id), then use the host's reference syntax (`Closes #<id>`); otherwise open the PR
unlinked and say nothing about it.

If `--title` was supplied, use it; otherwise compose. ASCII only.

## Step 6: Apply and report

Write the body to a temp file and pass it by file reference — never inline
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
- **Existing PR** (default or `--update`): the commits are already pushed; preview
  before overwriting — ask: new title, the first sentence or two of the body, total
  line count. On confirmation, `gh pr edit <number> --title "<TITLE>" --body-file
  "$BODY_FILE"`. In autonomous closeout, apply directly and report what changed. If
  `--base` was given and differs from the PR's base, retarget with
  `gh pr edit <number> --base "$BASE"`; otherwise preserve the existing base.
- **`--description-only`**: print the title and body. Stop.
- Clean up the temp file.

Never merge (`gh pr merge`, `glab mr merge`, Azure `--auto-complete`) and never arm
auto-merge — landing is the user's call.

**Report:** the PR URL, target branch, the commits included, what stayed unstaged and
why, and whether the PR is draft or ready. In `--update` mode report the title/body
changes applied; in `--pr-only` note that uncommitted changes were left alone.

## Handoff

- The PR is merge-ready only when the project's checks agree — green is not the same
  as safe. When the user asks to get it green, watch CI, or address review bots, hand
  to `babysit`. Do not start one because a PR now exists.
- Reviewers comment → `resolve-pr-feedback`.
- The work has not had a review pass this session and the push is about to happen →
  suggest `autoreview` before Step 4, not after.
- After a merge, branch cleanup is `git-cleanup`.

---
name: git-cleanup
description: "Remove one verified merged local branch and its exact worktree, or audit repository-wide Git clutter when explicitly requested. Protect long-lived branches, dirty work, and unique commits."
argument-hint: "[branch, worktree, or PR | --all] [--dry-run] [--delete-remote]"
---

# Git Cleanup

Close one delivered Git allocation without losing work. Targeted cleanup is the
default: act only on the exact branch and worktree named by the user or supplied by
the delivery owner. A bare invocation does not authorize a repository-wide sweep.
Use the broad inventory only for `--all` or an explicit request to clean the whole
repository.

This skill is pure Git and works in any repository. It may receive merge evidence
from a delivery workflow, but it independently verifies the current repository
state before deletion.

## Invariants

- Never remove local or remote `main` or `develop`.
- Never remove the repository's configured default branch, regardless of its name.
- Preserve every additional protected branch named by active project instructions.
- Never remove a dirty worktree, unknown ignored local data, a moved branch, or a
  commit whose delivery cannot be verified.
- Never infer ownership from a branch name, worktree location, PR title, or clean
  status. Match the exact identities supplied by the user or delivery owner.
- Targeted mode never expands into other branches, worktrees, or stale metadata.
- Do not delete a remote branch unless the user separately and explicitly requests
  that exact remote deletion.
- Re-read destructive preconditions immediately before each removal. A changed
  branch, worktree, or merge result cancels cleanup.

## Select the mode

- **Targeted:** a branch, worktree, PR, or delivery allocation was named. Inspect and
  close only that allocation.
- **Repository-wide:** `--all` or plain language explicitly asks to inventory or
  clean the whole repository. Use the broad workflow below.
- `--dry-run` performs the selected inspection and reports the plan without deleting.
- `--delete-remote` applies only when the user explicitly authorized deletion of the
  exact remote branch. It never overrides protected-branch rules.

If targeted mode has no exact branch or worktree identity, report what is missing.
Do not substitute a repository-wide scan.

## Targeted post-merge cleanup

### 1. Resolve exact identity

Record:

- repository root and primary worktree;
- local source branch and its current commit;
- auxiliary worktree path, or `primary checkout` when the branch is checked out
  there;
- target branch;
- PR URL or stable ID, merged state, and PR head commit when a PR exists; and
- remote and upstream branch.

Inspect current state:

```bash
git status --short --untracked-files=all
git branch --show-current
git remote -v
git worktree list --porcelain
git show-ref --verify refs/heads/<source-branch>
git ls-remote --symref <remote> HEAD
```

Require the live remote query to return `ref: refs/heads/<default> HEAD`. Derive the
configured default by stripping only the exact `refs/heads/` prefix. Preserve the
rest of the name, including paths such as `release/stable`. Do not rely on the
cached local `<remote>/HEAD`. If the live result is unavailable or ambiguous, resolve
the default through the forge or stop before deleting anything.

### 2. Verify delivery and branch identity

Refresh the relevant remote refs. For PR delivery, read the exact PR from its forge
and require `merged`, its target branch, and its head commit. Require the local source
branch tip to equal the recorded and current PR head. For a targeted branch without
a PR, require an explicit target and prove the exact source tip is an ancestor of the
fresh remote target:

```bash
git fetch --no-tags <remote> refs/heads/<target-branch>
git merge-base --is-ancestor <expected-source-commit> FETCH_HEAD
```

Reject cleanup when the branch moved after delivery, the PR is only open or
merge-ready, the recorded remote cannot be refreshed, the merge cannot be verified,
the fetched target is ambiguous or stale, or the target identity changed. Use the
freshly written `FETCH_HEAD` from this exact fetch as ancestry evidence; do not
substitute a cached remote-tracking ref. `main`, `develop`, the configured default
branch, and project-protected branches stop here.

### 3. Verify the exact worktree

Find whether the source branch is checked out and require that location to match the
recorded allocation. For an auxiliary worktree, verify:

```bash
git -C <worktree-path> status --short --untracked-files=all
git -C <worktree-path> branch --show-current
git -C <worktree-path> rev-parse HEAD
git -C <worktree-path> ls-files --others --ignored --exclude-standard
```

Tracked or untracked changes block removal. Ignored files also need evidence that
they are reproducible disposable output or have been preserved; do not infer that a
database, environment file, cache, or dependency directory can be lost. Require the
checked-out branch, worktree HEAD, local branch tip, and verified delivered head to
match. Ensure no other owner or worktree uses the allocation when that information is
available.

If the source branch is checked out in the primary checkout, require a clean tracked
and untracked state and inventory ignored paths with the same command used for an
auxiliary worktree. Verify those paths are preserved or disposable, and compare them
with the target tree; any ignored path that the target would track blocks the switch
until its disposition is explicit. Cleanup may switch away only to the verified
target branch, and only when that target is exactly `main` or `develop`. An auxiliary
worktree must be removed from the primary repository context, not by deleting its
directory.

### 4. Remove only the verified allocation

If `--dry-run` was requested, report the exact worktree and branch that would be
removed and stop.

For a verified auxiliary worktree, re-read its branch, HEAD, tracked, untracked, and
ignored state, then remove that exact registered worktree:

```bash
git -C <primary-worktree> worktree remove <worktree-path>
```

For a clean primary checkout on the source branch, switch to the verified `main` or
`develop` target:

```bash
git switch <target-branch>
```

Immediately re-read the local source ref. Delete it only if it still equals the
verified delivered head, using an expected-old-value ref update so a concurrent move
is preserved:

```bash
git update-ref -d refs/heads/<source-branch> <expected-source-commit>
```

When exact remote deletion was separately authorized, re-check merge and protection
state and read the current remote source tip immediately before deletion:

```bash
git ls-remote --exit-code --heads <remote> refs/heads/<source-branch>
```

Require that tip to equal the verified delivered head. Delete with an expected-tip
lease so a concurrent push makes the deletion fail instead of losing new commits:

```bash
git push --force-with-lease=refs/heads/<source-branch>:<expected-source-commit> <remote> :refs/heads/<source-branch>
```

If the remote branch is already absent, report it as absent. Otherwise preserve it
when authorization, identity, or the conditional deletion is missing.

### 5. Verify closeout

```bash
git branch --list <source-branch>
git worktree list --porcelain
```

Report the removed local branch and worktree, whether the remote branch was preserved,
and any exact blocker. Partial cleanup remains explicit: if worktree removal succeeds
but the branch moves before compare-and-delete, preserve the moved branch and report
that result.

## Explicit repository-wide cleanup

Use this workflow only after `--all` or an explicit whole-repository cleanup request.
It does not run after normal PR delivery.

1. Inspect `git status --short`, the current branch, remotes, `git branch -vv`,
   merged and unmerged branches, and `git worktree list --porcelain`.
2. Run `git fetch --prune` for the relevant remotes. If network or authentication
   fails, continue as a dry inventory and label remote freshness unverified.
3. Classify each candidate:
   - **Safe local deletion:** merged into its fresh target, not protected, not
     current, not checked out, and `git branch -d` accepts it.
   - **Safe worktree removal:** exact auxiliary worktree, verified delivered branch,
     clean tracked and untracked state, and reviewed ignored-file disposition.
   - **Review first:** gone upstream but unmerged, no upstream, unique commits,
     unknown ownership, dirty state, or unknown ignored data.
   - **Protected:** `main`, `develop`, configured default, project-protected, current,
     or shared allocations.
4. Report the grouped plan. A dry run stops. An explicit cleanup request may remove
   the safe set without asking again; ambiguous and destructive candidates remain.
5. Use `git branch -d` for safe broad-mode branch deletions and `git worktree remove`
   for exact safe worktrees. Force deletion requires explicit abandonment authority
   for the named work.
6. Verify with `git branch --list` and `git worktree list --porcelain`, then report
   what was removed and what was preserved.

Use Git commands for registered worktrees. Use `trash` only for separate filesystem
artifacts that Git does not own and whose deletion was authorized.

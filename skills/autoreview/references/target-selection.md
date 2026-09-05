# Target Selection

Read for choosing dirty, branch/PR, or committed review scope. Follow the scope and safety contract in the skill entry point.
In commands and code examples, resolve bundled paths from the directory containing the loaded SKILL.md; do not use the caller's working directory.

## Pick Target

Dirty local work:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --mode local
```

Use this only when the patch is actually unstaged/staged/untracked in the
current checkout. `--mode uncommitted` is accepted as an alias for `--mode local`.
For committed, pushed, or PR work, point the helper at the commit
or branch diff instead; do not force dirty modes just
because the helper docs mention dirty work first. A clean local review
only proves there is no local patch.

Branch/PR work:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --mode branch --base origin/main
```

Optional review context is first-class. Prompt files and datasets must be repo-relative so review bundles cannot pull arbitrary host files:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --mode branch --base origin/main --prompt-file review-notes.md --dataset evidence.json
```

If an open PR exists, use its actual base:

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --mode branch --base "origin/$base"
```

Committed single change:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --mode commit --commit HEAD
```

Use commit review for already-landed or already-pushed work on `main`. Reviewing
clean `main` against `origin/main` is usually an empty diff after push. For a
small stack, review each commit explicitly or review the branch before merging
with `--base`.

# Optimise GitHub Actions

An explicit-user-invoked audit of Actions usage, feedback speed, and reliability.
The Python 3 adapter collects read-only evidence; audits do not authorize edits.

Inspired by [enesgules/dotfiles](https://github.com/enesgules/dotfiles/tree/a94d573e88056df6ca45eaf2f1813145ffc7ef03/skills/optimise-github-actions),
pinned at `a94d573e88056df6ca45eaf2f1813145ffc7ef03`. The upstream skill and
measurement script were inspected. No license file was found in the pinned tree
and GitHub's license endpoint returned 404 on 2026-10-04, so no upstream prose or
executable is copied here. This directory is an original implementation of the
audit approach, with current GitHub billing/API documentation as the authority.

Refresh by inspecting that upstream path and current official documentation, then
manually updating this implementation. Do not overwrite it with upstream files.
Preserve both explicit invocation gates, audit-only scope, per-attempt accounting,
and unknown/partial-data handling.

Run deterministic checks:

```bash
SKILL_DIR="<absolute directory containing this README>";
python3 -m unittest discover -s "$SKILL_DIR/tests" -v
```

The invocation metadata and repo checks cover the portable policy declarations.
Live triggering in Claude Code, Codex, Cursor, Copilot, and Antigravity has not
been tested for this addition; a new plugin session is needed after publication.

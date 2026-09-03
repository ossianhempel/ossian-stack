# PR Description Writing

## The core principle

The diff is already visible in the PR. The description exists to explain what the
diff cannot show: what was impossible before and is now possible, what was broken and
is now fixed, what shape changed. Cut any sentence a reader could reconstruct from the
diff itself.

- Bad: "Adds `ingest_orders.py`, modifies the pipeline to call it, and updates two tests."
- Good: "Orders now land in Bronze on the nightly run; the pipeline picks them up
  automatically. Backfill of the 2024 history is included and row-count reconciled."

If the lead sentence describes what was moved, renamed, or added rather than what's
now possible or fixed, rewrite it. This applies to every section, not just the
opening — restating the diff is the failure mode this guide exists to prevent.

## Resolve the range

- **Current-branch mode** (default) — describe `HEAD` against the resolved base
  (default branch, or the open PR's `baseRefName` when one exists and `--base` was
  not given):

  ```bash
  git fetch --no-tags origin "$BASE"
  git log --oneline "origin/$BASE..HEAD"
  git diff "origin/$BASE...HEAD"
  ```

  Empty commit list → report "No commits to describe" and stop. In
  `--description-only`, prefer the best available range without mutating: remote
  qualified, then local `$BASE...HEAD`, then the visible diff with a note that no
  base ref was available.
- **PR mode** — describe a specific PR (a URL/id was passed). Fetch metadata first:
  `gh pr view <id> --json title,state,headRefName,baseRefName,url`. If the PR is not
  open, report and stop — do not invent a description. Use its `baseRefName` as
  `<BASE>` and `headRefName` as `<HEAD>`.

Subtract fix-up commits (review fixes, lint, rebase resolutions) when reading the
range — they are invisible to the reader.

## Size the description

Match weight to weight. When in doubt, shorter wins. Large PRs need more selectivity,
not more content.

| Change profile | Description approach |
|---|---|
| Small + simple (typo, config, dep bump) | 1-2 sentences, no headers. Under ~300 characters. |
| Small + non-trivial (bugfix, behavioral change) | 3-5 sentences. No headers unless two distinct concerns. |
| Medium feature or refactor | The section order below, with empty sections dropped. Call out design decisions. |
| Large or architecturally significant | Section order below + a Summary table when many mechanisms compete; do not create an H3 per mechanism. Target ~100 lines, cap ~150. |
| Data / model / migration change | Add a verification line: what was validated against real data (row-count parity, key uniqueness, null rates, before/after parity, tests green). For migrations and backfills also state risk and rollback. |
| Performance improvement | Include before/after measurements as a markdown table. |

For small + simple PRs, the value-led sentence is the entire description.

## The body sections

When the body uses headings, use these in order. Drop a section when it is empty.
Name real symbols and paths, not abstractions.

- `## Why` — the intent and why this approach fits. This is where the core principle
  lives; lead with what is now possible or fixed.
- `## Scope` — facts from the diff. Name both sides of a rename or retarget. State
  what is in and out when the boundary matters.
- `## Tradeoffs` — real choices only. Skip when there are none.
- `## Blast Radius` — who and what the change touches, and why it is safe or risky.
  If the default branch is red without the fix, name the continuing cost.
- `## Verification` — how you ran each check and its rigor: the real command, test
  file, or surface, and the outcome of each. Never present an unverified claim as
  verified; label results you could not check.

Do not use `## Summary` or `## Test plan` boilerplate. On small PRs the value-led
opening is the whole body; no orphaned paragraph above a first heading. A visual
(mermaid diagram or markdown table) only when it conveys the change faster than prose;
prose is authoritative when they conflict.

## Title

`type: description` or `type(scope): description`.

- Type by intent, not file extension. When `fix` and `feat` both seem to fit, default
  to `fix` — adding code to remedy missing behavior is `fix`. Reserve `feat` for
  capabilities the user could not previously accomplish. Use `refactor`/`docs`/
  `chore`/`perf`/`test` when more precise.
- Scope: the narrowest useful label. Omit when no single label adds clarity.
- Description: imperative, lowercase, under 72 chars, no trailing period.
- Match the project's conventions (active instructions, else recent commits).
- Never use `!` or `BREAKING CHANGE:` without explicit user confirmation — they can
  trigger automated major-version bumps.

## Tracker links

Only when an id was explicitly supplied. Use the host's syntax — GitHub/GitLab
`Closes #<id>`, Azure Boards `AB#<id>`. Never invent one. ASCII only throughout the
title and body; keep emojis out of anything that could reach console or log output.

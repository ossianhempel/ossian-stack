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
opening, restating the diff is the failure mode this guide exists to prevent.

## Provider scope

GitHub commands below apply only to GitHub/GHE. For Azure DevOps Services, use
`azure-devops.md` for PR metadata, preserving the same diff and writing principles.

## Resolve the range

- **Current-branch mode** (default), describe `HEAD` against the resolved base
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
- **PR mode**, describe a specific PR (a URL/id was passed). Fetch metadata first:
  `gh pr view <id> --json title,state,headRefName,baseRefName,url`. If the PR is not
  open, report and stop, do not invent a description. Use its `baseRefName` as
  `<BASE>` and `headRefName` as `<HEAD>`.

Subtract fix-up commits (review fixes, lint, rebase resolutions) when reading the
range, they are invisible to the reader.

## Size the description

Match weight to weight. When in doubt, shorter wins. Large PRs need more selectivity,
not more content.

| Change profile | Description approach |
|---|---|
| Small + simple (typo, config, dep bump) | 1-2 sentences, no headers. Under ~300 characters. Add one compact inline visual when it clarifies the change (required for any UI change); otherwise use the escape path below. |
| Small + non-trivial (bugfix, behavioral change) | 3-5 sentences plus one compact rendered visual inline (screenshot for UI; diagram, table, or fenced block for non-UI). No headers unless two distinct concerns. |
| Medium feature or refactor | The section order below, with empty sections dropped. Call out design decisions. |
| Large or architecturally significant | Section order below + a Summary table when many mechanisms compete; do not create an H3 per mechanism. Target ~100 lines, cap ~150. |
| Data / model / migration change | Add a verification line: what was validated against real data (row-count parity, key uniqueness, null rates, before/after parity, tests green). For migrations and backfills also state risk and rollback. |
| Performance improvement | Include before/after measurements as a markdown table. |

## Rendered visual evidence

Every PR carries at least one piece of **rendered** visual evidence inline in the PR
body — visible directly on the PR page, never a bare link, external reference, or
unuploaded local file path.

| Change kind | Required inline visual |
|---|---|
| UI, styling, layout, copy, or interaction change (any size) | Real screenshot(s) captured from the running surface — or a short video/GIF for motion or multi-step interactions (GIF or screenshot sequence on Azure, which does not render inline MP4 players) — uploaded and rendered inline. Use synthetic data or redact credentials and private records before uploading (hosted attachments can outlive edits to the PR body). Use a Before/After markdown table for image comparisons, and put each video on its own standalone paragraph so GitHub renders an inline player rather than a link. A diagram, code block, or prose does not substitute for real UI captures. |
| Non-UI change (logic, API, schema, refactor, workflow, data, perf) | Load `show-me` and render the smallest concrete inline view that makes the change scannable: a Mermaid diagram (GitHub only; Azure DevOps PR bodies do not render Mermaid), a Before/After markdown table, or a fenced block (`diff`, code shape, tree, or compact output). |

**Escape path** — omit the visual only when one of these two conditions genuinely holds:

1. **Non-visual change:** a visual would add zero signal beyond the diff itself (for
   example, a typo fix, copy-only doc tweak, or trivial one-line dependency/config bump).
   Skip rather than inventing a decorative diagram, and note the reason in one short
   line in `## Verification` (or at the end of a headerless small PR).
2. **Capture or inline upload blocked (or unsafe to upload):** the running surface
   cannot be exercised, a safe capture free of secrets or private data cannot be
   produced, or the forge/CLI cannot upload media inline (for example, `gh` older than
   `v2.99.0` without `--attach`, an unsupported host, or missing upload permissions).
   Strip any local file paths from the PR body so nothing renders broken, state the
   exact blocker in `## Verification`, label visual verification as unverified, and
   include the local capture in the final chat response when one exists and is safe to
   share.

## The body sections

When the body uses headings, use these in order. Drop a section when it is empty.
Name real symbols and paths, not abstractions.

- `## Why`, the intent and why this approach fits. This is where the core principle
  lives; lead with what is now possible or fixed.
- `## Scope`, facts from the diff. Name both sides of a rename or retarget. State
  what is in and out when the boundary matters.
- `## Visual evidence`, inline rendered screenshots, recordings, or a Before/After
  image table for changes that alter rendered UI or produce visual artifacts. Drop on
  non-UI PRs where `## Change outline` provides the rendered visual.
- `## Change outline`, expected for non-UI PRs and any change whose shape is the
  story: schema or contract changes, key data structures or types, module or component
  boundaries, call-tree, control-flow, or data-flow. Load `show-me` and emit at least
  one concrete rendered view per the table above; prefer a `diff` block for a changed
  shape and a complete block for a mostly-new one. A one-line prose description is not
  the outline. Omit categories that did not change. Drop only when `## Visual evidence`
  already carries the story or the escape path applies.
- `## Tradeoffs`, real choices only. Skip when there are none.
- `## Blast Radius`, who and what the change touches, and why it is safe or risky.
  If the default branch is red without the fix, name the continuing cost.
- `## Verification`, how you ran each check and its rigor: the real command, test
  file, or surface, and the outcome of each. Never present an unverified claim as
  verified; label results you could not check, including any blocked visual capture or
  upload with its exact blocker.

Do not use `## Summary` or `## Test plan` boilerplate. On small PRs the value-led
opening plus its compact inline visual (or one-line escape reason) is the whole body;
no orphaned paragraph above a first heading. When a view and prose disagree, prose is
authoritative — but rendered visual evidence is the default for every PR, not an
optional extra.

## Title

`type: description` or `type(scope): description`.

- Type by intent, not file extension. When `fix` and `feat` both seem to fit, default
  to `fix`, adding code to remedy missing behavior is `fix`. Reserve `feat` for
  capabilities the user could not previously accomplish. Use `refactor`/`docs`/
  `chore`/`perf`/`test` when more precise.
- Scope: the narrowest useful label. Omit when no single label adds clarity.
- Description: imperative, lowercase, under 72 chars, no trailing period.
- Match the project's conventions (active instructions, else recent commits).
- Never use `!` or `BREAKING CHANGE:` without explicit user confirmation, they can
  trigger automated major-version bumps.

## Tracker links

Only when an id was explicitly supplied. Use the host's syntax, GitHub/GitLab
`Closes #<id>`, Azure Boards `AB#<id>`. Never invent one. ASCII only throughout the
title and body; keep emojis out of anything that could reach console or log output.

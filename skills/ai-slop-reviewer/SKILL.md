---
name: ai-slop-reviewer
description: >-
  Detect and remove AI-generated writing tells from existing copy or prose.
  Runs a deterministic linter, reviews structural and tonal patterns the
  linter cannot catch, and returns a cleaned rewrite. Use whenever the user
  asks to check for AI slop, make writing sound human, remove AI tells, audit
  ChatGPT-like copy, or review a draft for robotic language. This is a review
  and cleanup skill, not the default skill for generating marketing copy.
---

# AI-Slop Reviewer

Review existing writing for mechanical and judgment-based AI tells, then fix
the draft without flattening its voice.

## Boundary

- Use this skill when the primary job is auditing or cleaning existing text.
- Use `copywriter` when the primary job is generating or rewriting marketing
  and product copy for conversion.
- Use `online-writing` when the primary job is writing, structuring, or
  auditing editorial long-form - blog posts, essays, newsletters, threads that
  teach or argue. Run this skill as its final pass, not instead of it: that
  skill decides headline, structure, and Main Points; this one only removes
  AI tells from the resulting draft.
- A generation skill may use this as its final quality gate, but this skill
  does not invent the underlying positioning, argument, or campaign.

## Workflow

1. Get the exact draft. Preserve intentional brand terms, factual claims,
   formatting constraints, and the writer's point of view.
2. Read `references/ai-slop-checklist.md`. It is the canonical rule set.
3. Run the mechanical gate:

   ```bash
   python3 <ai-slop-reviewer-skill>/scripts/ai_slop_lint.py path/to/draft.md
   # or pipe text through stdin
   pbpaste | python3 <ai-slop-reviewer-skill>/scripts/ai_slop_lint.py -
   ```

   Resolve `<ai-slop-reviewer-skill>` from the installed skill path shown by
   the active agent runtime; do not assume the current project is
   `ossian-stack`.

4. Fix every mechanical hit unless the term is a required proper noun or an
   exact quotation. State any justified exception.
5. Review the judgment rules manually: repeated structures, fake suspense,
   inflated tone, uniform rhythm, unnecessary formatting, and manufactured
   endings.
6. Rewrite locally. Keep strong sentences and the author's natural rough
   edges; do not replace one generic voice with another.
7. Run the linter again on the revised draft. A clean mechanical result is
   necessary, but the judgment review still decides whether it sounds human.

## Output

Return:

1. **Verdict:** one sentence naming the dominant problem, or saying the draft
   is already clean.
2. **Findings:** only meaningful issues, quoting the smallest useful fragment
   and naming the tell.
3. **Revised draft:** the full cleaned version when changes are needed.
4. **Mechanical gate:** `clean`, or the remaining justified exceptions.

Do not produce a giant checklist when the user only needs the cleaned copy.
Lead with the revised draft when they explicitly ask for a rewrite rather than
an audit.

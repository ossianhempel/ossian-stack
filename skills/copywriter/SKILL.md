---
name: copywriter
description: "Write or improve marketing copy and product UI text: listings, landing pages, ads, social scripts, onboarding, and microcopy. Editorial long-form belongs to online-writing."
---

# Copywriter

Choose the job of the text first:

- **Utility:** errors, settings, permissions, destructive confirmations, and
  routine controls need accurate consequences, clear actions, and calm reassurance
  where useful. Emotional persuasion is not required. Read the in-app reference.
- **Acquisition and conversion:** earn attention from the intended audience and
  sell the outcome with real product proof. Use the persuasion principles and
  lever catalogue; never fabricate scarcity, claims, or social proof.
- **Editorial:** a piece that teaches, argues, or tells without a sales purpose
  belongs to `online-writing`.

Match the user's voice, medium, audience awareness, and requested scope. Preserve
meaning and verified product facts when rewriting. Keep routine UI text useful
rather than forcing it through the cold-stranger acquisition test.



## Reference Files

Open the file that matches the medium before writing. Each reference file
contains format rules, character limits, structural patterns, and examples.

- `references/swipe-file.md` - **Read for acquisition or voice matching.** Curated copy Ossian saved
  from apps, ads, and posts that worked. Append new examples here when
  Ossian pastes inspiration. All in-repo; no external systems.
- `references/appstore-screenshots.md` - App Store screenshot headlines, the
  pain → shift → proof → features sequence, the 8-word rule, the hand test.
- `references/appstore-descriptions.md` - App Store name, subtitle, promotional
  text, full description, What's New, character limits, opening hooks.
- `references/in-app-copy.md` - Consumer mobile in-app copy. Craft-vs-conversion
  split (utility surfaces vs hype moments), UX craft rules (voice, i18n,
  errors, toggles, review format), the "dumb it down" principles (3-second
  value, 3rd-grader language, can't-get-lost buttons), plus buttons, empty
  states, error messages, onboarding strings, permission prompts, push
  notifications, confirmations, and the hype-moment rewrite pattern (account
  creation, paywall reveal, plan summary). Open whenever the target is a B2C
  mobile app surface.
- `references/persuasion-skeleton.md` - The 5-step long-form arc (Hook →
  Agitate → Empathize → Solve → Payoff). Open for landing pages, App Store
  descriptions, long captions, carousels, and any multi-beat persuasive
  narrative. Not for in-app microcopy or single headlines, and not for
  editorial long-form - see the boundary below.
- `references/landing-pages.md` - Hero, headline + subhead, feature sections,
  social proof, CTAs, above-the-fold structure. Map sections to
  `persuasion-skeleton.md` when writing the full page arc.
- `references/ig-captions.md` - Caption / post description copy for IG and
  TikTok posts. Hook structure, body, closing line, CTA, hashtags. Pairs
  with either short-form video or slideshow/carousel.
- `references/short-form-video.md` - Reels and TikTok video. Two modes:
  UGC/native ("the tool, not the pitch") and 7-second hook-overlay loop.
  Native moment structure, anti-pitch checklist, mode selection.
- `references/social-profiles.md` - Profile copy across platforms (IG, X,
  TikTok, LinkedIn). Display name, bio structure, what to cut, before/after
  examples.
If the medium isn't covered, fall back to the core principles below and ask
Ossian whether to add a new reference file or a section in `swipe-file.md`.

## Boundary: editorial long-form belongs to `online-writing`

Threads, newsletters, long posts and multi-paragraph pieces are claimed by both
skills. **Intent decides, not format:**

| The piece exists to... | Skill |
|---|---|
| Sell, convert, drive signups or downloads | **This skill** |
| Teach, argue, or tell - building the library and the audience | `online-writing` |

That skill runs Nicolas Cole's editorial arc (Headline → Intro → Main Points →
no conclusion), buries the CTA inside a Main Point rather than giving it the
spotlight, and treats a closing recap as optional - the deliberate opposite of
this skill's mandatory Payoff. Both are correct inside their own arc. Don't
blend them: if a piece has no thing to sell, the Agitate beat has nothing to
agitate about.

Hooks are covered in both. Use this skill's Hook Gut Check and awareness stages
when the hook has to sell; use `online-writing` when it has to open an essay.

## Workflow

1. **Get context.** Is this utility, acquisition, or editorial? Who is the audience? What problem? What
   medium / format? If you don't know, ask.
2. **Read relevant saved examples.** For acquisition or a voice-matching task, open `references/swipe-file.md` for relevant
   section(s). Match medium and product context before inventing from scratch.
3. **Open the right reference file.** Match the medium. For multi-beat
   persuasive copy (landing page, long caption, App Store
   description), also open `references/persuasion-skeleton.md` and draft beat
   by beat. If none fits, fall back to the core principles.
4. **Choose the standard.** For acquisition, name the lever and user outcome.
   For utility, name the action, actual consequences, and recovery or next step.
5. **Draft to the format.** Use the selected reference's structure and limits.
6. **Check the result.** For acquisition, apply the Hand Test and emotional pull
   test. For utility, verify accuracy, clear labels, calm tone, and usable recovery.

7. **Cut.** Remove every word that isn't earning its place.
8. **Run the AI-slop gate.** Use the sibling `unslop` skill as the
   final review: apply its judgment checklist (`references/ai-slop-checklist.md`)
   and fix every hit.
9. **Offer 2–3 variants** when there's a clear creative choice (tone, angle,
   length). Don't drown Ossian in 10 options - give the strongest 2–3 with a
   one-line note on what each is optimizing for.
10. **Persist winners.** When Ossian pastes inspiration or greenlights copy
    worth reusing, append it to `references/swipe-file.md` in the entry format
    defined there. Skip if he says draft-only.

## Output Format

Adapt to the medium. In general:

- Show the **draft** clearly, separated from commentary.
- If multiple variants, label them by what each is optimizing for ("punchy",
  "specific", "playful", "direct").
- Note character counts when limits matter (description fields, push, button
  labels).
- Flag anything you're unsure about and what would unblock you.

## Anti-Patterns (don't do these)

- Don't start with "Welcome to..." or "Introducing..."
- Don't use "powerful", "seamless", "intuitive", "robust", "best-in-class",
  "revolutionary" - they're filler.
- Don't pile on emojis. One per section max, and only if it earns its place.
- Don't write headlines that need a subhead to make sense.
- Don't claim "#1" or "best" without proof.
- Don't write copy that only makes sense to someone who already uses the
  product.
- Don't ship copy that "sounds professional" but triggers nothing. Competent,
  brand-safe, feature-descriptive copy is the most common failure mode: it reads
  fine and converts no one who wasn't already sold.
- Don't write a first line that only informs. If it doesn't pull a lever, it's
  not a hook - it's a caption.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Acquisition principles](references/acquisition-principles.md): persuasive acquisition copy and its craft tests.
- [Persuasion levers](references/persuasion-levers.md): acquisition levers, human desires, hooks, and rewrite examples.

---
name: online-writing
description: >-
  Write, audit, or revise editorial long-form writing - blog posts, Medium and
  LinkedIn pieces, newsletter essays, Substack posts, X threads - using
  Nicolas Cole's Art and Business of Online Writing method: Form + Idea +
  Audience, headline first, 1/3/1 structures, Main Point skeletons, Rate of
  Revelation. Use this whenever the user asks to write an article or blog post
  from scratch, review or audit a draft, fix a headline or title, fix an
  introduction, restructure a piece, decide what to write about, or asks "is
  this any good?" about long-form prose. Intent decides against copywriter:
  editorial pieces that teach, argue, or tell belong here; a thread,
  newsletter, or post whose job is to sell, convert, or drive signups belongs
  to copywriter and its persuasion-skeleton. Not for UI microcopy, App Store
  metadata, or ad copy - use copywriter for those.
---

# Online Writing

Write articles people actually finish. The method is Nicolas Cole's, from *The
Art and Business of Online Writing*, extended with Ossian's vault notes.

**The governing constraint:** a reader on the internet is one tap from
somewhere better. Every sentence is a bid for the next one. Cole's name for
this is **Rate of Revelation** - every sentence must advance the story or
reveal something new, or the reader leaves. Clarity is necessary and not
sufficient; a clear-but-slow sentence still loses the skim.

## Boundary

- **This skill:** long-form articles, essays, threads, newsletters. Structure,
  headline, introduction, Main Points, endings, topic selection.
- `unslop`: final pass for AI tells. Run it *after* this skill on
  anything drafted or heavily rewritten by a model.

### Split with `copywriter` - by intent, not by format

Threads, newsletters, long captions and multi-paragraph posts are claimed by
both skills. **Intent decides:**

| The piece exists to... | Skill |
|---|---|
| Get someone to buy, sign up, download, or click | `copywriter` + its `references/persuasion-skeleton.md` |
| Teach, argue, or tell - and build the library and the audience | **This skill** |

The two arcs are different machines, and they conflict on purpose:

```
persuasion-skeleton:  Hook → Agitate → Empathize → Solve → Payoff → CTA
online-writing:       Headline → Intro → Main Points → (no conclusion)
```

**The known contradiction:** `persuasion-skeleton.md` says *never skip the
Payoff*. This skill says *conclusions are optional*. Both are correct inside
their own arc. A sales arc has to close, because the close is the point. An
editorial arc has already discharged the PROMISE in the Main Points, so a
recap is the fourth one the reader has been handed. **Do not blend them.** If
you find yourself writing an Agitate beat in an editorial piece, you picked
the wrong skill.

Same split governs the CTA: `copywriter` gives it the spotlight, this skill
buries it inside a relevant Main Point merged with the credibility claim (see
`references/forms-and-topics.md`).

## Modes

Pick the mode from the request, then follow that section.

| User asks | Mode |
|---|---|
| "write an article about X", "draft a post on Y" | **Write** |
| "review this", "audit this draft", "is this good?" | **Audit** |
| "fix my headline / intro / structure" | **Targeted fix** |
| "what should I write about?" | **Topic selection** |

---

## Mode: Write

Write backwards. Never open a blank document and start at the first sentence.

**1. Fix the three variables before writing anything.**
Read `references/forms-and-topics.md`.

- **Form** - Actionable Guide, Opinion, Curated List, Story, or Credible
  Talking Head. Pick one. Mixing forms is the single most common failure: a
  title promising an Actionable Guide over a body that is secretly a Curated
  List leaves the reader confused and unfulfilled.
- **Idea** - Explanation, Habits, Mistakes, Lessons, Tips, or Stories.
- **Audience** - one named reader, as narrow as you can stand.

State all three back to the user in one line before drafting. If the user
hasn't given you enough to fix them, ask - this is the one place worth a
question, because everything downstream inherits the answer.

**2. Write the headline first.**
Read `references/headlines.md` and run the four-step rewriting process. The
headline must answer three things simultaneously: what this is about, who it
is for, and the PROMISE.

Cole's compression test: *if you can't say it clearly in a twelve-word
headline, you won't say it clearly in an 800-word post.* The loop has a
reject - if the final headline isn't strong, restart, or don't write the
piece. That is a feature.

Offer the user 3-5 headline candidates and your pick, with one line on why.

**3. Skeleton the Main Points before the introduction.**
Read `references/main-points-and-endings.md`.

The sweet spot is **800-1,200 words**, and more Main Points does not mean a
longer piece - it means less real estate each. So the point count decides the
depth template:

| Main Points | Per-point template |
|---|---|
| ≤3 | 1/2/5/3/1 (the twelve-sentence deep form) |
| 4 | 1/3/1 - five sentences |
| 5+ | The point itself plus 1-3 sentences |

Write every Main Point as a **statement, not a label**. Single-word subheads
fail: a reader skimming nothing but the bolded subheads must still feel they
got it. Draft the points together as a set and read them in isolation -
parallel phrasing across subheads is itself a credibility signal, and it is
invisible while writing them one at a time.

**4. Write the introduction against the skeleton.**
Read `references/introductions.md`. Default shape is **1/3/1**: one opening
sentence, three description sentences, one conclusion sentence. Every valid
intro structure opens on a single sentence and closes on a single sentence -
that part is invariant; the middle is a variable the density of the point
selects.

The intro's job is to hook, not to summarize. Open at the height of the
story. If the piece gets better four paragraphs in, delete the first four
paragraphs.

**5. Draft the body.** Apply the rhythm rules in
`references/main-points-and-endings.md` - never three long paragraphs in a
row, resolve a long paragraph with a single declarative sentence.

**6. End without a conclusion section, by default.** Conclusions are optional.
The final Main Point is the climax. See the three permitted endings in the
reference.

**7. Gate before delivering.** Run the linter (below) and the
`references/audit-rubric.md` checklist on your own draft. Report anything you
knowingly left failing.

---

## Mode: Audit

Do not rewrite first. Diagnose, then rewrite.

1. Get the exact draft. Ask for the intended audience and platform if not
   obvious - the rubric can't score a PROMISE without knowing who it's for.
2. Run the mechanical gate:

   ```bash
   python3 <online-writing-skill>/scripts/online_writing_lint.py path/to/draft.md
   # or pipe text in
   pbpaste | python3 <online-writing-skill>/scripts/online_writing_lint.py -
   ```

   Resolve `<online-writing-skill>` from the installed skill path in the
   active agent runtime; do not assume the current project is `ossian-stack`.
   The linter catches shape only - word budget, paragraph runs, label
   subheads, headline length. It cannot see Form/Idea mismatch or a weak
   PROMISE.
3. Read `references/audit-rubric.md` and score every gate. Read the other
   reference files as each gate needs them.
4. Report in the output format below.
5. Only then rewrite, if the user wants a rewrite. Preserve their voice,
   their examples, and their rough edges.

### Diagnostic shortcuts

These map a symptom to the one fix, so you don't run every pass on every
problem:

- **Paragraph over ~5 sentences** - one of exactly two failures. Too many
  points (fix: split) or too much description per point (fix: cut words, not
  ideas). Check what precedes it first: a long paragraph after a run of
  single-sentence paragraphs is a deliberate decrescendo, not a defect.
- **Two adjacent short sections making one point between them** - the chunk
  was split when it should have been cut. Test: "does this really warrant its
  own section?"
- **Can't write a subhead for a block** - the block has no single point. That
  is the diagnosis, not a formatting inconvenience.
- **Title clear, piece unsatisfying** - Form mismatch. The body is a
  different form than the title promised. Fix is to split into two pieces, not
  to write longer.
- **Headline clear but nobody clicks** - the PROMISE isn't emotional enough.
  Escalate by adding specificity, never by withholding the answer. If the line
  got more compelling while saying *less*, it failed and it's clickbait.

---

## Mode: Targeted fix

Open only the relevant reference and work the loop in it:

- Headline/title - `references/headlines.md`
- Introduction/hook - `references/introductions.md`
- Structure, subheads, length, endings - `references/main-points-and-endings.md`
- What to write about, CTA placement, credibility - `references/forms-and-topics.md`

---

## Mode: Topic selection

Read `references/forms-and-topics.md`. Work the three content buckets
(General / Niche / Company-Industry), then run each candidate through Form +
Idea + Audience before proposing it. Prefer evergreen over timely: a timely
piece collects its entire return on day one and can never be re-shared.

---

## Output format

**When auditing:**

1. **Verdict** - one sentence naming the dominant problem, or saying the draft
   is sound.
2. **Gate scores** - the rubric table, pass/fail per gate, failures first.
3. **Findings** - only what matters. Quote the smallest useful fragment, name
   the rule, give the fix.
4. **Revised draft** - full text, when the user wants one.

**When writing:** deliver Form/Idea/Audience in one line, then headline
candidates, then the skeleton, then the full draft. Don't ask for approval
between each - deliver the whole thing and flag the decisions you made.

## References

| File | Read when |
|---|---|
| `references/headlines.md` | Writing or fixing any title, subhead, or thread hook |
| `references/introductions.md` | Writing or fixing the opening |
| `references/main-points-and-endings.md` | Skeletoning, structure, rhythm, length, endings |
| `references/forms-and-topics.md` | Choosing form/idea/topic, credibility, CTA placement |
| `references/audit-rubric.md` | Any audit or self-gate |

Source notes live in Ossian's vault: `3. Resources/Notes/Online writing.md`
and its linked notes; primary highlights in
`3. Resources/Readwise/The Art and Business of Online Writing (highlights).md`.
Use the `obsidian` skill to open them when a question goes past these files.

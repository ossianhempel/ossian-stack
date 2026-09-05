---
name: prototype
description: "Build a disposable UI or logic prototype to compare alternatives and answer a design question."
---

# Prototype

A prototype is **throwaway code that answers a question.** The question decides
its shape.

**You own the design decision, not the code.** The artifact is an instrument. The
real build follows afterwards, from the decision this settled.

## The inversion

This is the one place where the usual bias toward the smallest change, and the
usual verification bar, both invert. Speed over polish. Code quality does not
matter. No planning.

The rigor is in picking the right design cheaply — not in the code that gets you
there. Be bold: propose variations the user didn't ask for, throw an approach
away and try another.

## 1. Scope the decision it exists to make

Which layout, which interaction, which density. Or for an empirical fork: which
behavior, which timing, which approach.

**No decision means no prototype.** If there is nothing to settle, this is
ordinary implementation work, and building a throwaway first just costs a day.

This is also the move when you would otherwise ask the user a question that a
quick sketch could answer for you.

## 2. Pick a branch

Identify which question is being answered, from the user's prompt, the
surrounding code, or by asking if they are around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). A single
  shareable HTML file — free-play buttons plus tabbed guided walkthroughs — that
  pushes the state machine through cases that are hard to reason about on paper,
  and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Several radically different
  UI variations on a single route, switchable via a URL search param and a
  floating bottom bar.

The two branches produce very different artifacts, so getting this wrong wastes
the whole prototype. If the question is genuinely ambiguous and the user isn't
reachable, default to whichever branch better matches the surrounding code (a
backend module → logic; a page or component → UI) and state the assumption at the
top of the prototype.

## 3. Gather references when the design space is open

Search for prior art, summarize a moodboard of themes, palettes, and layouts, and
let the user pick directions before you build. Skip this entirely when the
direction is already set.

## 4. Build it throwaway

1. **Throwaway from day one, and clearly marked.** Put it close to where it will
   actually be used, so the context is obvious, but name it so a casual reader can
   see it is a prototype and not production. For throwaway UI routes, obey the
   project's existing routing convention; don't invent a new top-level structure.
   For a purely exploratory sketch with no home yet, an isolated scratch directory
   outside production source is fine.
2. **Trivial to run.** A UI prototype starts from one command in the project's own
   task runner. A logic demo is a single HTML file the user double-clicks. No
   thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing
   a prototype *checks*, not something it should depend on. If the question
   explicitly involves a database, hit a scratch DB or a local file named clearly
   enough to delete — "PROTOTYPE, wipe me".
4. **Skip the polish.** No tests, no abstractions, no error handling beyond what
   makes it runnable. Vanilla HTML/CSS/JS or the lightest stack that renders the
   idea; CDN dependencies and a hot-reloading dev server are fine here. No
   production framework.

## 5. Put the alternatives behind one switcher

When comparing, build every variant behind a single switcher — buttons or a
keypress — each labeled so the user can name the one they mean. Flipping between
them in one place is what makes the comparison honest; two separate artifacts get
compared from memory.

This is `principle-exhaust-the-design-space` made cheap.

## 6. Surface the state

After every action (logic) or on every variant switch (UI), print or render the
full relevant state, so the user can see what changed rather than infer it.

## 7. Verify by observing, not asserting

On the matching surface. For a visual decision, screenshot each variant and drive
the interaction — the eye is the test. For a behavioral or timing decision,
observe the thing you are deciding: log the timing, print the output, watch the
render.

**The observation is the test here**, not an assertion. If the project has no
scripted way to drive its own surface, `close-the-loop` builds one.

## 8. Present, then capture

Present the variants, the tradeoffs, and a recommendation. The output is the
decision plus the throwaway artifact — not shippable code.

Then capture both, because a prototype answers a question once and the answer
outlives the code:

- Fold the validated decision into the real code.
- Commit the prototype itself to a throwaway branch, off main, and leave a pointer
  to that branch wherever the implementation work is tracked.
- Record the verdict *and the question it settled* alongside it. Main keeps only
  the validated decision.

## Reply

The variants you explored, the evidence (screenshots for a visual decision, the
observed output or timing for a behavioral one), the tradeoffs, your
recommendation, and the path to the throwaway artifact.

Say plainly that the prototype is throwaway.

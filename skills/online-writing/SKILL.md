---
name: online-writing
description: "Audit and research for editorial writing published online - blog posts, newsletters, Substack, LinkedIn, X. Three jobs: score a draft (or someone else's post that performed) against the six persuasion elements, research what is already working on a topic before writing, and pick the week's topic by mining the last two weeks of reading and notes. Diagnosis and research only - it never drafts or rewrites prose."
---

# Online Writing

Two jobs sit outside drafting and get skipped: finding out what the market
already rewards *before* writing, and checking afterwards whether the piece is
persuasive rather than merely correct. This skill does those two and nothing
else.

**It never writes or rewrites prose.** When a draft needs to move, hand it to
the drafting workflow the writer's own project points at. The value here comes
from staying diagnostic — a reviewer that rewrites stops reporting what was
wrong and starts hiding it.

**Everything this skill hands back goes through `mannered-prose` first.** An
audit that says a hook "doesn't earn its keep" has performed the exact failure
it is complaining about, and a finding the writer has to decode is a finding
they will not act on. Read that skill and apply it to your own output before
sending — findings, frames, headlines, and the swipe-file entries alike.

## Modes

| The ask | Mode |
|---|---|
| "audit this", "is this good?", "why won't this land?" | **Audit** |
| "why did this post do well?", "add this to the swipe file" | **Audit**, reverse direction |
| "what's working on X right now?", "research this before I write" | **Research** |
| "what should I write about this week?" | **Topic** |

---

## Mode: Audit

Score the piece against six elements. Every one of them is about whether a
stranger keeps reading — not whether the piece is true, useful, or well
argued. Those belong to the writer's own style guide and are already covered
elsewhere; do not re-litigate them here.

| # | Element | Passes when |
|---|---|---|
| **1** | **Hook** | The first sentence earns the second. Judge the *rendered* opening — line breaks, whitespace, and what survives the platform's preview cut are part of the hook, not decoration around it |
| **2** | **Problem** | A problem is stated or implied that the named reader recognizes as theirs. Concrete beats high-level; "your agents produce mediocre code" lands where "AI adoption is hard" does not |
| **3** | **Solution** | Something actionable, ideally done by the writer rather than collected from others |
| **4** | **Benefit** | A desirable outcome is visible. It can be implied, but the reader must be able to name what they get |
| **5** | **Stance** | The piece picks a side and stays on it. Hedges, "it depends", and both-sides endings fail this — not because confidence is a virtue, but because a reader cannot follow someone who has not decided |
| **6** | **Novelty** | A perspective or framing the reader has not already met this week. The test is whether it advances their understanding, not whether it is contrarian |

Read the whole piece before scoring anything. Elements 1 and 2 gate the rest:
if nobody gets past the opening, findings about element 6 are unreachable, so
say so and rank the fix order accordingly.

### Then run the slop pass

The six elements say nothing about whether the sentences sound like a person
wrote them, and a draft that a model touched can pass all six and still read as
generated. So run `unslop` over the same text and fold its findings in.

Take its findings, not its rewrite. That skill cleans text end to end, which is
the right default when someone asks it directly and the wrong one here — an
audit that hands back a cleaned draft has stopped reporting what was wrong.
Ask it for the tells and the lines they sit on, and report those.

Keep them in their own section rather than mixed into the six. They are a
different kind of problem: the elements are about whether the piece works on a
reader, the tells are about whether the writer sounds like themselves, and a
piece can fail one while passing the other. When the prose is clean, say so in
a line and move on.

### Output

```
Verdict: <one sentence naming the dominant problem, or saying it is sound>

| Element | Verdict | Evidence |
|---|---|---|
| Hook | fail | "<smallest useful quote>" |
...

Findings, worst first:
  <Element> — <what specifically fails> → <the fix, named>

AI tells: <none, or the tells with the lines they sit on>
```

Name the fix; do not perform it. "The hook opens on setup — the real opening
is the sentence about the rejected build, four paragraphs down" is a finding.
Rewriting the hook is not. If the writer then asks for a rewrite, that is a
drafting request — route it rather than absorbing it.

### Reverse direction: auditing what worked

The same six elements read backwards turn someone else's post into a reusable
pattern, which is the whole reason to keep a swipe file: the elements only
become instinct once they have been spotted in the wild.

Score the post, then record only the transferable part — the structure and the
framing, never the topic. Append to the swipe file of the piece it is research
for (see below) as:

```
## <working title of the post> — <platform>, <date seen>
Link: <url>
Why it worked: <the one or two elements that did most of the work>
The reusable frame: <the structure, with the topic stripped out>
```

"The Notebook System That Saved My Brain" is stored as *`<System> that saved
my <faculty>` — possession-under-threat, rescue framing*, not as a note about
notebooks. Stripped that way it can carry a topic it was never written for.

---

## Mode: Research

The point is to find what the market has *already signaled it wants*, then
merge that with the topic the writer wants to write about. Neither half alone
is enough: chasing what performs produces work someone else should have
written, and writing purely from the inside produces work nobody finds.

1. **Read the existing swipe files first.** They are the highest-signal source
   because every entry was already filtered by hand. They live per piece, so
   read across all of them — a frame recorded for one piece is exactly the thing
   that should carry a different topic later.
2. **Search the open web** for the topic — recent newsletters, blog posts, and
   discussion that circulated. Be straight about the ceiling: X, LinkedIn, and
   Instagram largely cannot be read programmatically, so engagement numbers
   from those platforms come from the writer pasting posts in, not from you.
   Do not present inferred popularity as measured popularity.
3. **Report the frames, not the links.** A list of URLs is not research. What
   transfers is the recurring angle, the headline shapes that keep appearing,
   and the question everyone is answering badly.

Write findings into the piece's own `research.md` under a `## What's working`
heading, alongside whatever interview or source material is already there.
Where a per-piece working folder does not exist yet, ask before creating one —
the writer's project defines that layout.

---

## Mode: Topic

Two filters, applied in this order:

1. **Is it worth sharing, in the writer's judgement?** Filtering an idea
   through a specific identity is what makes it unique — so do not propose
   topics chosen to fit an audience the writer does not have.

   **A topic falling outside the writer's usual subjects is not a reason to
   reject it.** Niching down is not the goal. A declared territory describes
   what has been written so far, which is a record and not a boundary, so
   "this sits outside the stated territories" is an observation to hand over,
   never a verdict you reach on the writer's behalf. Propose the candidate and
   note that it would be new ground. Where a topic genuinely fails, say which
   filter it failed and why.
2. **Is it framed so it gets attention?** An idea that passes filter 1 and
   fails filter 2 goes unread. This is what the swipe file is for: take the
   topic from filter 1 and the packaging from a frame that already worked.

### Mine the last two weeks

What the writer has actually been reading and thinking about is the best
available evidence of what they can write with conviction *now*.

```bash
SINCE_TS=$(date -u -v-14d +%Y-%m-%dT%H:%M:%SZ)

# Reading. Note the flag names differ between the two commands.
readwise reader-list-documents --updated-after "$SINCE_TS" \
  --category article --limit 50 --response-fields title,author,site_name,summary
readwise readwise-list-highlights --highlighted-at-gt "$SINCE_TS" --page-size 100
```

Highlights are the stronger signal — a saved document is an intention, a
highlight is a reaction.

For the notes side, resolve the vault and filter on the `created:` frontmatter
date, not on file mtime. Obsidian Sync rewrites modification times, so `find
-mtime` reports notes from years ago as touched this week:

```bash
VAULT=$(for d in ~/ossians-second-brain-sync ~/Developer/ossians-second-brain-sync; do [ -d "$d/.obsidian" ] && echo "$d" && break; done)
SINCE=$(date -v-14d +%Y-%m-%d)

grep -r --include='*.md' -m1 -H '^created:' "$VAULT/Notes" "$VAULT/Writing" 2>/dev/null \
  | awk -F'created: *' -v s="$SINCE" '$2 >= s {sub(/:$/,"",$1); print $2, $1}' \
  | grep -E '^[0-9]' | sort -r

# Daily notes are named YYYY-MM-DD, so select them by filename
for i in $(seq 0 13); do d=$(date -v-${i}d +%Y-%m-%d); [ -s "$VAULT/daily-notes/$d.md" ] && echo "$d"; done
```

A topic that shows up in *both* the reading and the notes is the strongest
candidate: it means the writer read about it and then had a thought of their
own, which is exactly the raw material an original piece needs.

### Propose

Three to five candidates, each in this shape:

```
<Topic>
  Evidence: <what in the last two weeks points here — highlights, notes, drafts>
  Borrowed frame: <the swipe-file pattern being applied, or "none found">
  Working headline: <the merge of the two>
  Draws on: <existing notes it would be built from>
```

Then recommend one and say why. One topic per week is the operating
constraint: the long-form piece is the source, and the posts, scripts, and
clips are re-cuts of it rather than separate efforts. Proposing two topics for
one week is proposing two weeks of work.

Landing the pick as an idea file, with the frontmatter and folder conventions
that implies, belongs to the writer's project — follow its documented
conventions rather than inventing a layout.

---

## The swipe file

`swipefile.md`, in the piece's own folder, next to `research.md` and
`outline.md` — the same support-file convention those follow, so it is
referenced by path and never wikilinked.

It is a pattern library rather than a clipping service. An entry is kept
because the *frame* transfers, so one that cannot be restated with its topic
removed does not belong in it. That is also what separates it from
`research.md`: findings about this topic go there, and only the reusable shape
comes here.

Keeping it per piece rather than in one central file means the frames stay next
to the work that found them. The cost is that they are spread out, so **read
across every piece's swipe file** when researching or picking a topic — a frame
recorded months ago for something else is the most likely one to carry a new
topic well:

```bash
find "$VAULT/Writing" -name swipefile.md
```

When none exists yet, say so plainly rather than quietly substituting a weaker
signal. Titles the writer merely clicked or saved are evidence the *headline*
worked on them, not that the post performed — usable as a stand-in, but label
it as one, and offer to start the file from what the pass turned up.

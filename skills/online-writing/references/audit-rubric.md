# Audit Rubric

Score every gate. Report failures first. A gate is **fail** unless you can
point at the specific text that passes it.

Gates are ordered by blast radius: a G1 failure makes G6-G12 irrelevant, so
stop diagnosing detail once an early gate fails and say so.

## Structural gates

| # | Gate | Pass condition | Fix if failed |
|---|---|---|---|
| **G1** | **Form** | The piece is exactly one of: Actionable Guide, Opinion, Curated List, Story, Credible Talking Head - and the title promises that same form | Split into two pieces. Never "write longer" |
| **G2** | **Idea** | One of the six idea types is identifiable: Explanation, Habits, Mistakes, Lessons, Tips, Stories | Pick one and cut what serves another |
| **G3** | **Audience** | You can name the single reader in one phrase, narrowly | Narrow it until it excludes people |
| **G4** | **Scope** | Not cramming multiple ideas into one piece | Split |

## Headline gates

| # | Gate | Pass condition | Fix if failed |
|---|---|---|---|
| **G5** | **Three questions** | The title says what it's about, who it's for, and the PROMISE | Run the 4-step rewriting process |
| **G6** | **Position** | First 2-3 words name the thing; the final words carry the PROMISE; no preamble | Delete leading words, move outcome to the end |
| **G7** | **Twelve words** | Says it clearly in ~12 words | If it can't compress, the *thinking* is unfocused - restart the piece |
| **G8** | **Honest gap** | Compelling by adding specificity, not by withholding the answer | If it got more compelling while saying less, it's clickbait - rewrite |

## Introduction gates

| # | Gate | Pass condition | Fix if failed |
|---|---|---|---|
| **G9** | **Standalone** | Cover the headline - the intro alone still answers the three questions | Rewrite the intro against the skeleton |
| **G10** | **Height of the story** | The piece does not get better four paragraphs in | Delete everything before the good part |
| **G11** | **Shape** | Opens on one sentence, ends on one sentence; middle is 3-5 | Restore the bookends |
| **G12** | **Skepticisms** | Superficial, irrelevant, sloppy, implausible and untrustworthy are each countered | Add the missing counter (see introductions.md) |
| **G13** | **Promise payment** | The first ~5 sentences visibly begin paying the headline's PROMISE | Lower the headline's promise, or raise the intro |

## Body gates

| # | Gate | Pass condition | Fix if failed |
|---|---|---|---|
| **G14** | **Skim test** | Reading *only* the bolded subheads, the reader gets it | Rewrite each subhead as the finding, not a label |
| **G15** | **Budget** | 800-1,200 words, and the per-point depth matches the point count | Re-template: ≤3 → 1/2/5/3/1, 4 → 1/3/1, 5+ → point + 1-3 sentences |
| **G16** | **Chunk test** | Each section has one singular point, and each earns its own section | Split, or merge and cut |
| **G17** | **Paragraph ceiling** | No paragraph past ~5 sentences unless braced and earned | Route via the diagnostic tree in main-points-and-endings.md |
| **G18** | **Rhythm** | Never three long paragraphs in a row; long blocks resolve into a single sentence | Vary internal rhythm; insert resolving sentences |
| **G19** | **Parallelism** | Subheads read as a deliberate set when listed in isolation | Rewrite the set together, not one at a time |
| **G20** | **Rate of Revelation** | Every sentence advances or reveals; nothing is summarizable away | Delete. If removing words costs no idea, they were fluff |

## Ending and business gates

| # | Gate | Pass condition | Fix if failed |
|---|---|---|---|
| **G21** | **Ending** | One of: in-structure final point, Extended Final Main Point, or Summary. No separate recap section by default | Cut the conclusion into the last Main Point |
| **G22** | **Golden Intersection** | Personal material gives the reader necessary context; the product is not the main character | Rewrite around the reader's mistakes/lessons, with yours as proof |
| **G23** | **CTA placement** | The CTA is embedded inside a relevant Main Point and merged with the credibility claim; not a signature block; no "Enter: <Company>" | Merge credential + offer into one sentence, inside a point |
| **G24** | **Evergreen** | The piece can be re-shared in a year, or its timeliness is a deliberate choice | Note the tradeoff; don't over-polish a timely piece |

## Reporting template

```
Verdict: <one sentence naming the dominant problem>

Failed gates:
  G<n> <name> - <what specifically fails> → <fix>

Passed: G<n>, G<n>, ...

Findings:
  "<smallest useful quote>"
  Rule: <name>
  Fix: <concrete rewrite>
```

Do not list all 24 gates in the output. Name the failures, then list the
passing gate numbers on one line.

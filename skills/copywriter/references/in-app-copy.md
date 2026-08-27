# In-App Copy

For everything inside a consumer mobile product: UI strings, buttons, empty
states, errors, onboarding, permission prompts, push notifications,
confirmations, toasts, paywall transitions, account creation prompts. Read
SKILL.md first — the core principles all apply.

In-app copy is where users *already chose you*. The job is no longer to sell —
it's to keep them moving, make them feel competent, and at key moments
re-sell them on the value they're getting. Every string is either moving
them forward, making them stop and think, or wasting a moment that could
have hyped them up. Aim for the first or third.

## Craft vs conversion: which rules apply

In-app copy serves two jobs. Don't mix them on the same string.

| Surface | Lead with | Examples |
| --- | --- | --- |
| Errors, validation, destructive confirms | **UX craft** (below) | Form errors, failed saves, delete dialogs |
| Settings, toggles, links, placeholders | **UX craft** | Toggle labels, help links, field hints |
| Routine buttons, empty states, toasts | **UX craft** + simplicity rules | Save, Cancel, "No projects yet" |
| Account creation after onboarding | **Hype moment** | Post-quiz account prompt |
| Paywall reveal, plan summary | **Hype moment** | "Here's your personalized program" |
| End-of-onboarding payoff | **Hype moment** | Value reframe before the CTA |
| Push notifications | **Conversion** (specific, earns tap) | Re-engagement, feature nudges |

**The split in one line:** craft copy helps users succeed; hype copy helps them feel the win was worth keeping. Never apply psychological levers, scarcity, or playful tone to errors.

For deep interface-copy reviews (audit existing strings in code), use the **Review output format** at the bottom of this file. The standalone `better-writing` skill covers the same craft bar if you want a dedicated review pass.

## The Three Foundational Rules (consumer mobile)

Sophistication loses. Obviousness wins. The product can be sophisticated under
the hood — the surface has to be brain-dead simple.

### 1. Show value in 3 seconds or less

Any user-facing surface — screenshot, empty state, paywall, onboarding screen,
push preview — has to communicate the value in under 3 seconds. If a user
can't tell what they get out of it before their thumb moves, it's dead.

Test it: glance for 3 seconds, look away. Can you say what it does for you?
If not, cut, simplify, or rewrite.

### 2. Write for a 3rd grader

Short words. Short sentences. No jargon, no industry language, no clever
phrasing that requires a second read. If a 9-year-old wouldn't understand it,
rewrite it.

This isn't about treating users as stupid. It's about removing every
millisecond of friction between seeing the words and getting the point.
Smart people scrolling fast read like 3rd graders.

| Too smart                          | 3rd-grader version              |
|------------------------------------|---------------------------------|
| "Optimize your nutrition"          | "Eat better"                    |
| "Track macronutrients effortlessly"| "Snap a photo. See the calories."|
| "Maximize your training output"    | "Lift more. Every week."        |

### 3. Buttons so obvious you can't get lost

Button labels tell the user exactly what happens when they tap. No
cleverness. No branded verbs. No ambiguity. If a user has to think about
which button to tap, the button has failed. The path through the app
should feel like the only possible path.

When in doubt, dumb it down further than feels comfortable. You will almost
never go too simple.

## UX craft rules

System UX writing: consistency, recovery, and translation safety. Apply these
on every utility surface unless the craft-vs-conversion table above says
otherwise.

### 1. Recon the existing voice

Before rewriting, inspect nearby strings, terminology, localization files,
and any style guide. Preserve intentional brand character when it stays clear.
Only flag a deviation when it creates inconsistency, ambiguity, translation
risk, or wrong tone for the stakes.

### 2. One voice, flexible tone

One product voice; tone flexes with stakes:

| Context | Tone |
| --- | --- |
| Success, onboarding, empty states | Warm; light is OK |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain; zero playfulness |
| Data loss, security | Serious, explicit |

No "Oops!", no exclamation marks in errors. If the same error keeps firing
for many users, redesign the interaction instead of rewording it.

### 3. Address the reader directly

Use "you" in instructional copy, not "the user". Avoid "we" when it
deflects: prefer "Unable to load content" over "We're having trouble
loading this content." Possessives sparingly ("Favorites" over "Your
Favorites"). Never switch perspective mid-flow.

### 4. i18n-safe strings

Never build copy by concatenating fragments around variables
(`"You have " + n + " new messages"`). Word order and plural rules change
per language. Use full templated strings with proper pluralization
(`{count, plural, one {# message} other {# messages}}` or your i18n
library's equivalent). Match input device when relevant: "tap" on touch,
"click" with a pointer, "select" when both apply.

### 5. Verb-first buttons and flow vocabulary

Button labels start with a verb naming the action: "Save draft", "Delete
project". Multi-step flows pick one advance word ("Continue" *or* "Next",
not both). Destructive confirmation buttons repeat the consequence:
"Delete project" and "Cancel", never bare "Yes" / "No" / "OK".

### 6. Links describe the destination

Link text must make sense out of context. "Read the billing docs", never
"Click here". If several "Learn more" links appear on one page, suffix each:
"Learn more about exports".

### 7. One capitalization policy

Pick title case or sentence case per element type (all buttons, all
headings) and apply consistently. Sentence case is the safer default.
"Save Changes" beside "Discard changes" reads as sloppiness.

### 8. Settings describe the ON state

Label a toggle for what happens when it's on: "Send read receipts". Never
label the negative ("Don't send read receipts"). Link directly to a
referenced setting ("Notification settings") instead of describing the path
("Go to Settings > Notifications > Email").

### 9. Errors say how to fix, next to where it broke

An error is an instruction, adjacent to the failing field. Phrase hints
positively ("Use only letters", not "Don't use numbers or symbols"). Show
validation hints before the mistake when you can.

| Bad | Good |
| --- | --- |
| That password is too short | Choose a password with at least 8 characters |
| Invalid name | Use only letters for your name |
| Oops! Something went wrong. | Unable to save. Check your connection and try again. |

### 10. Placeholders are examples, not labels

Placeholders show expected format (`name@example.com`, `DD/MM/YYYY`). Every
field keeps a visible label; placeholders vanish on input.

### Common craft mistakes

| Mistake | Fix |
| --- | --- |
| Local rewrite ignores established terminology | Recon nearby copy first |
| "We're having trouble…" | Direct status + next step |
| `OK` / `Yes` on a delete dialog | "Delete project" |
| "Continue" on step 2, "Next" on step 3 | One flow vocabulary |
| Bare "Learn more" | "Learn more about exports" |
| "Don't send read receipts" toggle | "Send read receipts" |
| `"You have " + n + " messages"` | Full templated plural string |
| Crucial info only in an empty state | Persistent UI or help, not empty-only |

## Universal Rules

1. **Use the user's verbs.** "Save" beats "Persist". "Done" beats "Confirm".
2. **One job per string.** A button label, an error message, a toast — each
   says one thing.
3. **Direct status, present tense.** "Unable to save your changes" beats
   "We're having trouble saving" or passive "Your changes were unable to be
   saved".
4. **Plain English. Or plain Swedish.** No jargon. No product team words.
5. **Fail without blaming the user.** Errors should explain what happened and
   what to do next, not "Invalid input".
6. **Match the tone of the product.** Most of Ossian's apps are direct,
   confident, slightly dry. Don't get cute unless the product is cute — and
   never get cute in errors (see UX craft rules).

## Buttons & CTAs

- **Verb + outcome**, not category. "Start tracking" not "Continue". "Log a set"
  not "Submit".
- **Destructive confirms repeat the action**: "Delete workout" and "Cancel",
  not "Yes" / "No" / "OK".
- **One advance word per flow**: pick "Continue" or "Next" and stick with it.
- **Primary CTA = the thing you want them to do.** Secondary CTA = the escape
  hatch. Don't make both look equal.

| Bad         | Good                       |
|-------------|----------------------------|
| Submit      | Save workout               |
| Continue (step 2) + Next (step 3) | Continue throughout, or Next throughout |
| OK          | Got it (dismiss only) / Delete project (confirm) |
| Confirm     | Delete workout             |
| Learn more  | See how exports work       |
| Get Started | (still fine) — beats "Begin Your Journey" |
| New Entry   | Log Workout                |

## Hype-Moment Copy (account creation, paywall reveal, plan summary)

Most in-app strings are utility. A handful of moments are *not* utility —
they're the moment the user sees what they're getting. Account creation
prompts, paywall transitions, "here's your personalized plan" reveals,
end-of-onboarding summaries.

**This is the single thing agents get wrong most often.** They write
neutral, descriptive copy at moments that should be making the user feel
like they're getting away with something. The user has just done work
(answered questions, picked goals, waited for generation). Reward them.

### Rules for hype moments

1. **Highlight the value they're getting**, not the action they need to take.
   The CTA is the small part. The reframe of what they already have is
   the big part.
2. **Anchor against cost / effort / time saved.** What would this have
   cost them with a PT, a coach, a nutritionist, hours of research? Name
   it. Make the free thing feel expensive.
3. **Make them feel grateful, not pitched at.** Frame it like they got
   lucky, not like you're selling. "You're the one getting a great deal
   here" energy.
4. **Reframe generic features as personalized outcomes.** "Weekly schedule"
   is a feature. "A complete program built around the answers you just gave"
   is a personalized outcome.
5. **Add scarcity or urgency when it's honest.** "Save it before you lose
   it", "We built this just now — create an account so it's still here when
   you come back". Never invent fake countdowns.

### Before / After

These are real examples from a Swedish fitness app at the account-creation
prompt right after onboarding. The "before" copy is correct but flat. The
"after" copy hypes up the value the user just received.

**Account creation headline**

Before:
> We built it around your answers. Create an account so it's still here
> when you start lifting.

After:
> A program like this would cost thousands at a personal trainer.
>
> Create an account so we can save it for you now.

Swedish original (for reference):
> "Ett sådant här skräddarsytt program hade kostat tusentals kronor hos
> en PT. Skapa ett konto så vi kan spara det åt dig nu."

**Plan summary bullets**

| Flat (feature-named)              | Hyped (value-framed)                                             |
|-----------------------------------|------------------------------------------------------------------|
| Weekly schedule and start date    | Complete training program covering the next {N} weeks            |
| The exercises you picked or were recommended | Exercises picked specifically to grow muscle as fast as possible |
| Goals and progression for the first block    | Personal goals that adapt to what you can actually handle        |

Swedish originals:
- "Veckoschema och startdatum" → "Komplett träningsprogram som sträcker
  sig {antal veckor} veckor"
- "Övningarna du valde eller fick rekommenderade" → "Övningar specifikt
  utvalda för att maximera muskeltillväxt så snabbt som möjligt"
- "Mål och progression för första blocket" → "Personliga mål som anpassar
  sig efter vad du klarar av"

### The pattern

Flat copy names *what the screen contains*. Hyped copy names *what the user
walked away with and what it would have cost otherwise*. Same data, totally
different feeling.

When you see flat in-app copy at a hype moment, default to this rewrite:

1. What did the user just receive? (Be concrete: a 12-week program, a
   personalized macro target, a custom routine.)
2. What would that have cost in the real world? (A PT session, a
   nutritionist, hours of research, a $200 plan.)
3. What's the urgency to act now? (Save it before it's gone, lock it in,
   come back to it later.)

Then write the copy. The CTA is almost an afterthought.

## Empty States

The empty state is the most important screen in your app — it's the first
impression of every feature. Treat it like a screenshot.

Structure:
- **One-line outcome** (what this screen will look like once it has content)
- **One-line action** (what to do to get there)
- **One CTA** (the verb)

Search/filter empty states name the query and offer an exit: "No results
for 'quarterly'. Clear filters". Never park crucial persistent information
only in an empty state; it disappears once content exists.

Example (workout log, empty):
> No workouts yet.
> Log your first set and we'll start tracking your progress automatically.
> [ Log a set ]

Bad:
> Nothing here yet.
> [ Add ]

## Error Messages

Three parts: **what happened**, **why** (only if useful), **what to do next**.
Prefer inline copy next to the failing field over a vague toast.

- Don't blame the user. "Invalid email" → "That doesn't look like an email
  address — check for typos?"
- Don't show error codes unless the user is supposed to send them somewhere.
- Don't apologize three times. Once is enough.
- No "Oops", no humor, no exclamation marks.
- Offer the next action as a button if you can.

| Bad                        | Good                                              |
|----------------------------|---------------------------------------------------|
| Error 401                  | You're signed out. Sign in to keep going. [Sign in] |
| Invalid input              | Choose a password with at least 8 characters.     |
| Something went wrong       | Unable to save. Check your connection and try again. |
| We couldn't process your request (toast) | Inline: Unable to save. Check your connection and try again. |

## Onboarding Strings

- **Each screen = one promise.** Same rule as App Store screenshots.
- **Skip the welcome screen.** Or replace it with a working screen.
- **Don't explain features. Show outcomes.** Same rules as App Store.
- **Permission prompts come *after* the user understands why** they're needed.
  Pre-prompt with a one-line reason; don't trigger the system dialog cold.
- **End of onboarding is a hype moment, not a summary.** See the Hype-Moment
  section above. The user just did work — make the payoff feel huge.

Pre-permission pattern:
> To remind you about your next workout, we need to send notifications.
> [ Sounds good ]   [ Not now ]

(Then trigger the OS prompt only if they tap "Sounds good".)

## Push Notifications

- **Specific > generic.** "You haven't logged in 3 days" > "We miss you!"
- **Earn the tap.** What does the user get if they open it?
- **One job per push.** Don't bundle.
- **Respect the user.** No fake urgency. No fake personalization. No "🚨".

| Bad                          | Good                                              |
|------------------------------|---------------------------------------------------|
| We miss you!                 | Your last workout was 6 days ago. Quick set?      |
| New features available!      | You can now log supersets in two taps.            |
| Don't forget to log!         | Yesterday's leg day is still unfinished.          |

## Confirmations & Toasts

- **Past tense for success.** "Workout saved." not "Workout will be saved."
- **Skip the toast if the UI already shows the result.** A toast saying "Set
  added" when the set just appeared in the list is noise.
- **Toasts are for invisible success.** When the result isn't visually
  obvious, confirm it.

## System Strings (loading, syncing, retrying)

- **Be honest about what's happening.** "Syncing your last 3 workouts…" >
  "Loading…"
- **Show progress when you can.** A progress bar with a number beats a spinner.
- **If it's slow, say what's slow.** "Uploading photos — this can take a
  minute on a slow connection."

## Sign-In / Auth

- **Be clear about what you're asking for and why.**
- **Don't say "create account" if "sign in" works.** Account creation is
  friction; phrase it like a step, not a commitment.
- **Forgot password should be visible, not buried.**
- **If the account-creation moment comes right after onboarding, treat
  it as a hype moment** (see above). Don't waste it on "Create your account
  to continue."

## Localization Notes

- Most of Ossian's apps default to Swedish (i18n via i18next, `sv.ts` /
  `en.ts`). Write source strings English-first if asked, but **always think
  about how they'll feel in Swedish** — Swedish is more direct, less salesy,
  shorter. Don't write English copy that only works because of marketing fluff
  the Swedish version will strip.
- The hype-moment examples above are Swedish-native. The pattern (anchor
  against cost, name what they received, add urgency) translates cleanly —
  it isn't a hype-up-with-adjectives pattern, it's a reframe-the-value
  pattern, which survives translation.
- German and Finnish run long — leave room in buttons.
- **Never concatenate localized strings** around variables; use full templates
  with pluralization (see UX craft rules §4).

## Review output format

Use when the user asks to **review** or **audit** existing in-app copy in
source files (not when drafting new marketing strings).

### Findings

Group confirmed issues by category (errors, buttons, empty states, etc.).
Use a markdown table with **Severity**, **Location**, **Before**, **After**,
and **Why** columns.

- **Severity**: `HIGH` misleads, hides a consequence, or blocks recovery;
  `MEDIUM` makes a task harder; `LOW` voice or consistency polish.
- **Location**: `path/to/file:line`, or exact screen + component if no files.
- **Before / After**: quote current copy and complete replacement.
- **Why**: name the violated rule (craft or conversion) and the user cost.

Consolidate repeated systemic issues into one row; list every affected
location. Omit categories with no findings.

### Verdict

After findings:

1. **Verification**: checks run (full flow, pluralization, narrow-width wrap,
   capitalization consistency). Note anything not verified.
2. **Verdict**: `Block` if any `HIGH` remains; `Needs changes` if only
   `MEDIUM`/`LOW`; `Approve` when no actionable findings remain.

When clean: omit tables, state "No actionable in-app copy findings", report
verification, end with `Approve`.

## Quick Checklist

- [ ] 3-second value test: glance, look away, can you say what it does?
- [ ] 3rd-grader test: would a 9-year-old understand every word?
- [ ] Recon done: matches existing terminology and voice
- [ ] Buttons are verbs + outcomes; one advance word per flow
- [ ] No bare "Submit", "OK", "Yes"/"No" on consequential actions
- [ ] Destructive confirms repeat the action ("Delete project")
- [ ] Empty states orient + one next action; no persistent info empty-only
- [ ] Errors inline, positive hints, no "Oops" or deflection
- [ ] Toggles label the ON state; links describe destination
- [ ] i18n uses templated plural strings, not concatenation
- [ ] Onboarding screens each carry one message
- [ ] Push notifications are specific and earn the tap
- [ ] Toasts only fire when success isn't already visible
- [ ] Hype moments (account creation, paywall, plan reveal) reframe value
      against cost/effort, don't just describe what's on screen
- [ ] No jargon, no apology spirals, no fake urgency
- [ ] Reads naturally in the target language (not just translated)

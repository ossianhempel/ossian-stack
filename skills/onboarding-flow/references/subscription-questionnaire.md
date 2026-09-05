# Subscription Questionnaire

Read for the selected questionnaire subscription preset, including permissions, demo, and conditional monetization. Follow the scope and safety contract in the skill entry point.

## PHASE 3: ONBOARDING BLUEPRINT

Use this blueprint when a questionnaire subscription funnel is the selected product form. Adapt it to the app's complexity, activation goal, and actual monetization. The archetype requirements below apply within that chosen preset, not to every onboarding revision.

### The Onboarding Framework

The flow uses 11 screen archetypes. You MUST include screens marked [REQUIRED]. Others are [RECOMMENDED] or [OPTIONAL] based on fit.

#### Screen 1: WELCOME [REQUIRED]
**Objective:** Hook — show the end state, create desire.
- Bold headline stating the transformation outcome (not the app name)
- Show the app in use — **strongly prefer a short looping motion video over a static screenshot**. A 3–6 second clip of the core feature actually working (a workout being logged, a recipe being swiped, a meal being scanned) outperforms any still image. Static fallback only if video isn't feasible yet.
- "Get Started" primary CTA
- "Log in" text link (only if user wants sign-in)
- Progress bar at top (shows throughout entire flow)

**Pattern:** "Welcome to your new [transformation outcome]" + autoplaying muted loop of the app's core action.

**Producing the video:** Don't storyboard the clip here. Write a one-line brief ("show the calorie-scan flow: photo → result card"), gather 2–4 stills of the relevant screen, and hand both to the project's motion tooling. What comes back is an MP4, plus a portrait variant, ready to embed.

#### Screen 2: GOAL QUESTION [REQUIRED]
**Objective:** Get the user to self-identify their primary goal. This creates psychological investment — they've now told the app what they want, which makes them feel the app owes them a solution.
- "What are you trying to achieve?" (or domain-appropriate question)
- Single-select list of 5-7 goals relevant to the app's domain
- Each option has an emoji icon + short label
- Selection highlights with accent colour, reveals "Continue" button

**Key principle:** The options must be specific enough that users think "yes, that's exactly me" — not generic. Derive these from the app's actual feature set and target audience segments.

#### Screen 3: PAIN POINTS [REQUIRED]
**Objective:** Surface the user's frustrations. This does two things: (1) makes them feel understood, (2) gives you ammunition for the solution screen later.
- "What prevents you from [achieving their goal]?" (reference their Screen 2 answer if possible)
- Multi-select list of 5-7 pain points
- Checkbox-style selection (multiple allowed)
- "Continue" button always visible

**Key principle:** Pain points should be emotionally resonant and specific. "Lack of time" works. "Suboptimal workflow" does not. Use the language real users would use.

#### Screen 4: SOCIAL PROOF [RECOMMENDED]
**Objective:** Reduce risk perception. "Others like me have succeeded with this."
- "We've helped thousands of others like you" (adapt number if the app has real stats)
- 2-3 testimonial cards
- Each testimonial has: name/initials, persona tag (e.g. "Busy professional", "Beginner"), review text
- Tags should match the audience segments from Screen 2

**Key principle:** If the app doesn't have real testimonials yet, suggest the user writes aspirational ones based on the transformation they want users to experience. Mark these as placeholder content to be replaced with real reviews later.

#### Screen 5: PAIN AMPLIFICATION — TINDER CARDS [RECOMMENDED]
**Objective:** Deepen emotional engagement through interactive self-identification.
- "Which statements do you relate to?"
- Large card with a pain/frustration statement in quotes
- Swipe right (✓) to agree, swipe left (✗) to dismiss
- 3-5 cards, each stating a common frustration in the user's domain
- Feels playful and interactive, not like a survey

**Key principle:** These statements should be things the user will nod along to. They're designed to make the user think "this app really gets me." Use first-person language: "I spend too much time on..." not "Users often struggle with..."

#### Screen 6: PERSONALISED SOLUTION [REQUIRED]
**Objective:** Mirror back their pain points and show how the app specifically solves each one. This is the "bridge" moment — "you told us your problems, here's exactly how we fix them."
- "Welcome to a smarter way to [domain activity]"
- List of 3-4 items, each showing:
  - Their stated pain point (greyed/small text)
  - The app's solution with a compelling stat or promise (bold text)
- Each item has a relevant icon/illustration

**Key principle:** The stats should be specific and credible. "Users save an average of 25% on X" is better than "Save money." If the app is new and has no stats, use industry benchmarks or logical projections.

#### Screen 6b: FEATURE VIDEO BEATS [OPTIONAL — INSERT WHERE A SCREEN NEEDS PROOF, NOT JUST A CLAIM]
**Objective:** Show, don't describe. After the personalised solution screen makes a claim ("we re-plan your week automatically"), follow it with a 4–8 second video proving it. Motion video raises both completion and conversion, because the user *sees* the feature working before they're asked to commit.

**When to insert a feature-video beat:**
- Any time the personalised solution screen (Screen 6) lists a feature whose value isn't obvious from text
- Between the comparison table and preference configuration, to make the "with us vs. without" contrast visceral
- Right before the processing moment, to set expectations for what the demo will produce
- As a polish layer on top of static screens that test as "fine but flat"

**Screen layout:**
- One headline naming the outcome ("Re-plans your week in 2 seconds")
- Autoplaying muted looping video — 4–8 seconds, single feature, no narration text on top of UI
- Optional one-line caption under the video for accessibility / sound-off viewers
- "Continue" CTA below

**Producing the video:** One feature, one video. Keep it to cropped UI pieces in motion — never a full screen recording, never a tutorial. The intake is the same as above: a one-line brief plus 2–4 stills of the screen the beat lives on.

**Don't:**
- Stack three feature videos in a row — pick the one feature most worth proving
- Use long videos (>10s) — completion drops sharply
- Add voiceover or background music — onboarding videos play with sound off
- Skip the static fallback for users on slow connections

#### Screen 7: COMPARISON TABLE [OPTIONAL]
**Objective:** Make the with/without contrast visceral and obvious.
- Bold stat headline: "[X]% of people struggle with [problem]"
- Comparison table: App Name vs "Without"
- 3-4 rows comparing outcomes (green ✓ vs red ✗)
- Simple, scannable, no ambiguity about which side wins

#### Screen 8: PREFERENCE CONFIGURATION [RECOMMENDED]
**Objective:** Functional personalisation — collect preferences that make the upcoming demo relevant to them. Also deepens investment (they're customising "their" experience).
- "What do you like?" or domain-appropriate preference question
- Grid of options with images/icons (2-column grid works well)
- Multi-select with visual highlight on selection
- Can be 1-2 screens depending on how many preference dimensions matter

**Key principle:** Only ask for preferences that will visibly affect the demo in the next phase. Don't ask questions that go nowhere — users notice.

#### Screen 9: PERMISSION PRIMING [AUTO-DETECTED]
**Objective:** Pre-sell the user on granting permissions BEFORE the system dialog appears. A cold system prompt ("App wants to send you notifications") converts at ~40%. A primed request with context converts at 70-80%+.

**How to determine which permissions to prime:**
1. **Auto-detect from the codebase** — scan Info.plist (iOS), AndroidManifest.xml (Android), or framework-equivalent for declared permissions: notifications, location, camera, microphone, health data, contacts, photos, motion, tracking (ATT), etc.
2. **If no permissions are detected**, skip this screen entirely.
3. **If multiple permissions are needed**, show one priming screen per permission. Order them by how essential they are to the core experience — most important first.

**Screen layout for each permission:**
- Headline explaining the VALUE of the permission, not the permission itself
  - Notifications: "Never miss [the thing they care about]" — not "Enable notifications"
  - Location: "Find [things] near you" — not "Allow location access"
  - Camera: "Scan/capture [the thing]" — not "Allow camera access"
  - Health: "Track your [metric] automatically" — not "Allow health access"
- 2-3 bullet points showing what they'll get by granting the permission
- An illustration or icon representing the benefit (not a phone settings screenshot)
- "Enable" primary CTA → triggers the actual system permission dialog
- "Not now" secondary text link → skips without asking (never punish this choice)

**Key principles:**
- NEVER trigger the system permission dialog without priming first. You only get one shot — if the user denies, you're stuck with Settings deep-linking forever.
- Frame every permission around the USER's benefit, never the app's need.
- If a permission isn't essential to the core experience, consider deferring it to an in-context moment later in the app (e.g., ask for camera permission when they first tap "Scan", not during onboarding).
- Only prime permissions that are genuinely needed. Asking for permissions the app doesn't use erodes trust.
- For notifications specifically: prime AFTER the user has experienced the app demo (Screen 11) if possible — they'll better understand what they'd be notified about. However, if the notification permission is needed for the demo itself, prime it here before the processing moment.

**Platform considerations:**
- iOS: Notification permission is one-shot via UNUserNotificationCenter. ATT (App Tracking Transparency) must be prompted separately and has specific Apple guidelines.
- Android 13+: Notification permission requires runtime prompt (POST_NOTIFICATIONS). Below 13, notifications are granted by default.
- React Native / Flutter: Use the appropriate permission library (react-native-permissions, permission_handler, etc.)

#### Screen 10: PROCESSING MOMENT [CONDITIONAL]
**Objective:** Communicate real progress while personalization work is running.
- Show a loading state and accurate task text when real work is happening.
- Reveal the result promptly when it is ready; do not add a fake processing delay.
- Deliberate pacing is an optional, explicitly chosen design treatment, not a claim that nonexistent work is happening.

#### Screen 11: APP DEMO [REQUIRED — THIS IS THE HARDEST AND MOST IMPORTANT SCREEN]
**Objective:** Let the user actually USE the core app mechanic inside the onboarding. This is not a tour or a screenshot — it's a functional mini-version of the app's primary interaction.

**How to identify the demo:**
1. Look at the app's core loop — what's the ONE thing users do repeatedly?
2. Reduce it to its simplest form — pick 3 items, make 1 choice, complete 1 action
3. The demo must produce a TANGIBLE OUTPUT the user can see/share

**Examples by app type:**
- Recipe app → Swipe to pick 3 recipes → generates a shopping list
- Fitness app → Choose 3 exercises → generates a workout plan
- Finance app → Categorise 5 transactions → shows spending summary
- Learning app → Answer 3 questions → shows skill level assessment
- Task app → Add 3 tasks → shows organised daily plan

**Implementation approach:**
- Build this as a real, functional screen using the app's actual data models and UI components
- Use Tinder-style swipe cards or simple tap-to-select mechanics — keep interaction dead simple
- Show progress: "Pick 2 more" → "Pick 1 more" → "Done!"
- The output screen after the demo is the **viral moment** — design it to be shareable

**Key principle:** The user must DO something, not just watch. And they must get something back — a result, a list, a plan, a score. This creates the sunk cost that drives conversion at the paywall.

**Persist what they make.** Whatever the user creates in this demo (the picked recipes, the logged workout, the categorised transactions, the chosen goals, the selected exercises) MUST be written into the real app's data store before the paywall closes. This is what kills blank-page syndrome on first real-app launch — the user lands inside a populated app, not an empty one. See [first-session handoff, Strategy A](first-session-handoff.md) for the implementation pattern. If you can't persist it for some reason, **say so explicitly to the user during Phase 3** so they can choose a different demo that produces persistable output.

#### Screen 12: VALUE DELIVERY + VIRAL MOMENT [REQUIRED]
**Objective:** Show the tangible output from their demo interaction. This is the thing they created, and it should be impressive enough that they'd want to share it or keep it.
- Processing animation first: "[Generating/Building] your [output]..."
- Then reveal the output (list, plan, summary, result)
- Include a share button or "Send to a friend" option — this is the virality hook
- The output should feel real, not placeholder

**Key principle:** The output is gated behind the next screen (account creation or paywall). The user has invested time and created something — now they need to sign up to keep it. This is ethical because the app genuinely delivers this value; the onboarding just gave them a preview.

**Critical:** Whatever the user creates here MUST persist into the real app. If they made a workout, it's waiting for them in the workouts tab. If they picked recipes, their shopping list is already populated. Breaking this continuity — making them re-do the work, or landing them on an empty screen — is the single most jarring moment in most onboarding flows. See [first-session handoff](first-session-handoff.md).

#### Screen 13: ACCOUNT CREATION [OPTIONAL — based on user preference]
**Objective:** Soft gate — "Create a free account to unlock [the thing you just made]"
- Show thumbnails of what they created/selected
- "Create Free Account to unlock your [output]"
- List 1-2 additional features they get with an account
- Sign-in options: Apple, Google, email
- "Already have an account? Log in" at bottom
- Skip option if the app allows anonymous usage

#### Screen 14: PAYWALL [CONDITIONAL ON THE SELECTED MONETIZATION]
**Objective:** Convert to paid subscriber.
- App logo + headline restating the transformation: "Your [goal] sorted with [App Name]"
- One featured testimonial/review with star rating
- Pricing: actual available products, prices, offers, and eligibility
- Use a trial CTA only when the configured product and this user's eligibility support it; otherwise state the actual purchase action
- "More options" or "Restore purchases" secondary link
- If no paywall exists, propose monetization only when in scope. Create a clearly marked non-purchasable placeholder only when the user requests that prototype.

---

### Step 2: Present the Blueprint

Present the full screen sequence as a numbered list, showing:
- Screen number
- Screen type (from archetypes above)
- Specific headline/question for THIS app
- What it contains (brief)
- Which archetype screens were skipped and why

Ask for decisions on new or unresolved screen choices. If the blueprint is already specified or approved, proceed within that scope.

---
## IMPORTANT GUIDELINES

### For the Questionnaire Questions
- Questions must feel natural and conversational, not like a survey
- Each question should make the user think "yes, they get me"
- Options should cover the major user segments without being exhaustive
- Use emoji icons to make lists feel lighter and more scannable
- The order matters: start with aspiration (goals), then pain, then proof, then preference

### For the App Demo
- Keep it to ONE core interaction — don't try to demo the whole app
- The interaction should take 30-60 seconds maximum
- It must produce a visible, tangible result
- That result is the viral moment — design it to be worth sharing
- Use real data from the app's models where possible, sample data where necessary

### For Copy and Tone
- Write for someone who has never heard of the app
- Use "you" and "your" — it's their experience, not yours
- Headlines: bold, short, transformation-focused
- Body text: conversational, specific, no filler
- Stats: specific numbers feel more credible than round ones (83% > 80%)

### For the Paywall
- The paywall should feel like a natural conclusion, not an ambush
- By this point the user has: identified their goal, felt understood, seen proof, configured preferences, and used the app — the paywall is just the final step
- Include a trial only when the configured product supports it and the user is eligible
- Show one strong testimonial — social proof at the moment of purchase decision

---

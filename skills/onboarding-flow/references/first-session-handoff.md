# First Session Handoff

Read for preserving real demo output and delivering the first-session transition. Follow the scope and safety contract in the skill entry point.

## PHASE 6: FIRST SESSION HANDOFF

The onboarding flow ends at the paywall (or account screen). But the job isn't done — the very next thing the user sees is the real app, and that first real-app moment is still part of the onboarding experience from the user's perspective. If you let them land on an empty screen, every conversion you just won is at risk.

### The empty-state trap

Most apps drop new users into a blank screen:
- "No workouts yet"
- "No projects yet"
- "No data yet"
- …plus a button the user has to discover and tap

This adds friction at the worst possible moment. The user just paid (or committed to a trial) and now has to:
1. Figure out what they're looking at
2. Find the right button
3. Decide to tap it

Every extra decision is a drop-off. The fix is to remove the empty state entirely and put the user *into* the core action immediately — no hunting, no interpreting, no discovery.

### Step 1: Audit the empty states

Scan the app's main screens for "No X yet" / "Get started" / "Create your first [thing]" states. These are what a fresh user would see. For each one:
- Does the user NEED to see this screen on first launch, or can it be bypassed?
- What is the single primary action this screen exists to prompt?
- Can that action be auto-started instead of shown as a button?

### Step 2: Pick a handoff strategy

Choose ONE based on the app. They're listed in order of preference.

**A. Persist the onboarding demo output (STRONGLY PREFERRED)**
If the APP DEMO (Screen 11) produced real data — a workout, a shopping list, a task plan, a habit — persist it into the real app's data model. When the user lands in the main screen, their demo output is already there waiting. No empty state, and the continuity between onboarding and real app is preserved.

This is the strongest option because the user already did the work during onboarding; the app just has to honour it. **It also turns the entire interactive demo into setup-for-the-real-app at zero perceived cost** — the user thought they were "trying it out", and now their first real session opens with their own data already in place.

**Concrete examples of what to persist:**
| Onboarding demo output | What lands in the real app |
|---|---|
| Picked 3 recipes for the week | Shopping list pre-populated with combined ingredients; meal plan tab shows those 3 slotted into the next 3 days |
| Selected fitness goal + 3 starter exercises | Today's workout screen shows those 3 as round 1, ready to log |
| Categorised 5 transactions | Spending dashboard shows the categorised history; categorisation rules saved so future imports auto-tag |
| Chose preferred meditation themes | Today's recommended session is one of those themes; library is filtered to match |
| Answered skill-level questions | Lessons start at the matched difficulty; review queue is seeded with relevant cards |
| Set a daily step / calorie / habit target | Today's progress ring is already showing the target; first entry slot is unlocked |

If the demo's output **can't** be persisted (e.g. the demo is purely informational, or uses a sandbox separate from real models), pick strategy B or C — never let the gap show up as a blank screen.

**B. Auto-launch the core flow**
If there's no demo output to persist, launch the core creation flow automatically on first real-app open. Example: a workout app opens directly into "Create your first workout" full-screen — no tab bar, no home screen in between. The user is in the action before they can ask what to do.

**C. Prefilled first template**
Seed the account with one sensible default — a starter workout, a first project, a welcome habit. The home screen is no longer empty; it has one item the user can tap into, edit, or complete immediately.

**D. Guided first-use wizard**
For more complex apps, run a short in-app wizard on first load with coach marks or a focused overlay walking through the core action. Only use this when A/B/C don't fit.

If nothing else is possible, at minimum the empty screen should auto-open the creation flow after landing — never leave the user staring at a blank list waiting to find the button.

### Step 3: Implement the handoff

1. **Detect first session** — after onboarding completes, set both `hasCompletedOnboarding = true` and `hasSeenFirstSession = false`
2. **Branch on first real-app launch** — check the flag and route to the chosen handoff strategy before the main screen mounts
3. **Persist demo output** (strategy A) — write the data from Screens 11/12 into the real data store during the paywall/account transition so it's present when the main screen first renders
4. **Auto-navigate** (strategy B) — push the creation flow on top of the root view on first launch
5. **Mark complete** once the user finishes one core action in the real app — not just when they land on the screen

### Key principles

- Never show a blank empty state to a user on their first session
- The first action should be the CORE action of the app — not a settings screen, not a dashboard tour, not a feed browse
- Reduce decision-making to zero in the first 30 seconds
- If the user completed the app demo during onboarding, that output MUST land in the real app — breaking that continuity is the most jarring part of most onboarding flows
- The handoff is over when the user has completed ONE real action in the real app, not when they've seen the home screen

---

# Discovery And Transformation

Read for unresolved product context or transformation choices in a build. Follow the scope and safety contract in the skill entry point.

## PHASE 1: APP DISCOVERY

Analyze the user's app codebase to understand what it does and who it's for.

### Step 1: Read the active project conventions and codebase

Look at:
- The project's active instructions already in context, README, marketing copy or App Store metadata
- UI files, views, screens, components — what can the user DO in this app?
- Models and data structures — what domain does this operate in?
- Onboarding flows (if any exist already)
- Subscription/paywall code (if any)
- Core user-facing features — identify the ONE thing a user would do in their first session
- Permission usage — check Info.plist (iOS), AndroidManifest.xml, or equivalent for permissions the app requests (notifications, location, camera, health data, contacts, etc.)

Build a mental model of:
- **What the app does** (core functionality in one sentence)
- **Who it's for** (target audience)
- **The core loop** (the repeated action that makes the app valuable)
- **The "aha moment"** (when a new user first experiences value)
- **Existing paywall/subscription** (present or not, type, pricing)
- **Permissions required** (notifications, location, camera, health, etc. — detected from the codebase)

### Step 2: Ask the User Clarifying Questions

Present what you've learned and ask targeted questions. Only ask what the code doesn't already answer:

- "Based on the code, this is [X]. Is that right?"
- "Who is your target user? What's their skill level?"
- "What's the #1 reason someone downloads this app?"
- "What problem does this solve that other apps don't?"
- "Do you want to include sign-in/account creation in onboarding? (optional)"
- If monetization is in scope, confirm any prices, offers, or eligibility that the configured product does not establish. Do not add a paywall by default.

---
## PHASE 2: USER TRANSFORMATION

This is the most important conceptual step. Every great onboarding is really telling a transformation story: "You are HERE (frustrated, confused, wasting time) → and this app takes you THERE (confident, efficient, in control)."

### Step 1: Define the Before & After

Work with the user to articulate:

**BEFORE (without the app):**
- What frustrations does the user have?
- What are they doing instead? (the "bad alternatives")
- What pain points drive them to search for this app?
- What negative emotions are they feeling?

**AFTER (with the app):**
- What can they now do that they couldn't before?
- What feelings replace the frustrations?
- What tangible outcome do they get?
- What would they tell a friend about why they use this app?

### Step 2: Extract the Core Benefit Statements

From the transformation, extract 3-5 benefit statements. These must:
1. **Be specific and measurable where possible** — "Save 2 hours a week on meal planning" not "Save time"
2. **Address a real pain point from the BEFORE state**
3. **Lead with what the USER gets**, not what the app does
4. **Be believable** — stretch goals are fine, fantasy is not

Present this for confirmation only when the transformation story is a new unresolved design choice:

```
Here's the transformation story I'd recommend:

BEFORE: [1-2 sentences describing the frustration]
AFTER: [1-2 sentences describing the outcome]

Core benefits:
1. [Benefit] — addresses [pain point]
2. [Benefit] — addresses [pain point]
3. [Benefit] — addresses [pain point]
```

---

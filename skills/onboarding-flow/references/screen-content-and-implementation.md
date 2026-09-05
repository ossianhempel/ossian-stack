# Screen Content And Implementation

Read for drafting approved screens or implementing the chosen flow. Follow the scope and safety contract in the skill entry point.

## PHASE 4: SCREEN CONTENT

For each screen in the confirmed blueprint, draft the full content:

- **Headline** (bold, short, action-oriented)
- **Subheadline** (if needed — one line of supporting text)
- **Options/items** (with emoji icons where appropriate)
- **CTA button text**
- **Any stats or social proof copy**

Present related screens together. Ask only for unresolved new content choices; use already specified or approved content without repeated confirmation.

**Key content principles:**
- Write like a human, not a marketer. Short sentences. No jargon.
- Every headline should pass the "would I say this to a friend?" test
- Options should use the user's language, not technical terms
- Stats should feel specific and credible — round numbers feel fake
- CTAs should describe what happens next: "Pick my first [items]" not "Continue"

---
## PHASE 5: IMPLEMENTATION

Build the onboarding flow in the user's app.

### Step 1: Understand the Codebase Architecture

Before writing any code, understand:
- Framework and UI toolkit (SwiftUI, UIKit, React Native, Flutter, Jetpack Compose, etc.)
- Navigation pattern (NavigationStack, UINavigationController, React Navigation, etc.)
- Existing onboarding code (if any — extend or replace?)
- Design system (colours, fonts, component library, spacing conventions)
- State management approach
- How the app currently handles first-launch detection

### Step 2: Build Screen by Screen

For each screen in the blueprint:

1. **Create the view/screen** following the app's existing code patterns and conventions
2. **Wire up navigation** — screens should flow forward with back button support
3. **Add the progress bar** — shows position in the total flow
4. **Store user responses** — questionnaire answers should be persisted (these inform personalisation and can be sent to analytics)
5. **Implement interactions** — tinder swipes, grid selection, multi-select checkboxes, etc.

### Step 3: Build the App Demo Screen

This is the hardest screen. Approach:

1. Identify the core UI component from the app that will be used in the demo
2. Create a simplified version that works standalone (no dependencies on app state the user hasn't created yet)
3. Feed it with sample/curated data that matches the user's questionnaire preferences
4. Implement the interaction (swipe, tap, select) with a clear completion target ("Pick 3")
5. Generate the output from their selections
6. The output view should include a share mechanism (share sheet / export)

### Step 4: Connect monetization when selected

- Connect the existing paywall only when monetization belongs in the chosen flow.
- Use actual configured products, prices, offers, and eligibility. Include a trial
  only when supported for this user.
- A missing paywall does not authorize adding one. Create a clearly marked,
  non-purchasable placeholder only for an explicitly requested prototype.

### Step 5: Wire Up First-Launch Detection

- Add logic so the onboarding only shows on first launch (or when reset)
- Store completion state appropriately for the platform (UserDefaults, SharedPreferences, AsyncStorage, etc.)
- Ensure the app launches into onboarding when state is fresh, and into the main app when complete

### Step 6: Implement the First-Session Handoff

Onboarding isn't done when the paywall closes — it's done when the user completes their first real action inside the app. Implement the handoff strategy chosen in Phase 6 before calling the flow complete. Read [first-session handoff](first-session-handoff.md) for details.

---

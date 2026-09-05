---
name: onboarding-flow
description: "Design or audit mobile onboarding. Use for activation, questionnaire flows, first-session handoff, permission timing, and paywall placement."
---

# Onboarding Flow

Design around the app's activation goal and the user's requested scope: audit,
revise, or build. The long questionnaire and paywall arc is a subscription-app
preset, selected when the task calls for it. Do not rebuild an existing short
flow merely to satisfy that preset.

Use decisions already supplied in the request, code, or session. Ask only for
missing choices; reuse approved designs without repeating approval unless scope
changes. References describe available recipes, not authority to expand the task.

The onboarding demo must create real usable output. Persist that result and carry it into the first session; do not discard it after conversion or replace it with an empty state. Read the first-session handoff reference for any change to demo generation, persistence, or the transition into the app. Use real available prices and offers; trials and paywalls depend on the configured product and chosen flow. Show progress for real work; reveal completed results promptly.

## When to Audit Instead of Rebuild

If the user already has an onboarding flow and wants to diagnose drop-off rather than rebuild, switch to audit mode: read `references/audit-existing-flow.md`. It covers activation event identification, the screen-by-screen scorecard, permission timing matrix, sign-up friction patterns, funnel benchmarks (% targets per step), paywall placement timing, and the audit output format.

Use audit mode when there's a measurable funnel and the user asks "why are users dropping at step X?" An audit remains an audit. Propose structural changes when you find them; implement only when requested or approved.

---

## Companion Skills

Onboarding works best when it combines static screens, **short motion videos** demonstrating core value, and **interactive demos** the user can touch. This skill owns the flow; the sections below say what each asset has to be, so whoever produces it has a spec rather than a vibe.

- **Onboarding videos** — short (3–8s per beat) and punchy, showing a single feature in action by animating cropped UI pieces (a button being tapped, a row reordering, a sheet sliding up). Reach for one whenever a screen needs motion instead of (or above) a static screenshot: the Welcome hook, a feature-spotlight beat, the processing-to-result reveal, a paywall preview. Render to MP4 so it drops cleanly into a SwiftUI or React Native video player. The input is 2–4 stills of the screen plus a one-line brief saying what the beat must communicate — produce it with whatever motion tooling the project already uses. **Write the brief here; do not storyboard frames here.**
- **`copywriter`** (load its in-app and short-form video references) — for headlines, button labels, video on-screen overlay text, and CTA copy on every screen. Invoke it when drafting screen content in Phase 4.

The pattern: this skill owns the **flow architecture** (which screens, in what order, with what psychological purpose). The companion skills own the **assets** that go inside each screen.

---

## Credit

Adapted from [adamlyttleapps/claude-skill-app-onboarding-questionnaire](https://github.com/adamlyttleapps/claude-skill-app-onboarding-questionnaire) (MIT).

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Discovery and transformation](references/discovery-and-transformation.md): unresolved product context or transformation choices in a build.
- [Subscription questionnaire](references/subscription-questionnaire.md): the selected questionnaire subscription preset, including permissions, demo, and conditional monetization.
- [Screen content and implementation](references/screen-content-and-implementation.md): drafting approved screens or implementing the chosen flow.
- [First session handoff](references/first-session-handoff.md): preserving real demo output and delivering the first-session transition.

---
name: ios-marketing-capture
description: "Automate SwiftUI iOS marketing screenshots across locales, devices, and appearances. Triggers: App Store assets, locale screenshots, widget renders, simctl, fastlane alternative."
---

# iOS Marketing Capture

For an existing suitable harness, reuse the supplied screen paths, locales, device, appearance, seed data, and approved design, then capture and verify. Ask only for missing choices; batch independent questions. For a new or changed harness, read capture planning plus the implementation references that match the required features. Keep capture code DEBUG-only and marketing data isolated from real user data. Check the gotchas relevant to the actual app before running.

## Overview

Automate reproducible marketing screenshot capture for a SwiftUI iOS app across multiple locales, with two parallel output streams:

1. **Full-screen captures** — every marketing-relevant screen, with deterministic seeded data, real status bar / safe-area chrome
2. **Element captures** — isolated renders of specific components (cards, widgets, charts) at any scale, with natural background inside rounded corners and transparency outside

This skill is the **capture** step. If the user also wants Apple-style marketing pages composited around the shots (device mockups, headlines, gradients), that compositing is a separate post-processing step.

## Core Approach

**In-app capture mode**, not XCUITest. This is a hard decision that trades off against Fastlane snapshot / XCUITest conventions, and it wins for almost every real project.

Why in-app over XCUITest:

- **No new test target.** Adding a UI test target to an existing Xcode project is fragile pbxproj surgery. Many projects have zero test targets and no xcodegen — adding one by hand is error-prone.
- **Faster iteration.** A UI test takes 30s+ to launch per run. In-app capture is just a relaunch of the installed binary.
- **No `xcodebuild test`.** The whole flow is `xcodebuild build` once, then `simctl launch` per locale. No test-bundle overhead.
- **Access to real app state.** You can call ViewModels, SwiftData, ImageRenderer, and `UIWindow.drawHierarchy` directly. XCUITest can only tap and read accessibility elements.
- **Element renders need in-process anyway.** `ImageRenderer` on widget views or isolated components must run inside the app process — there's no XCUITest equivalent.

How it works:

1. A DEBUG-only `MarketingCapture.swift` file lives in the main app target
2. When launched with `-MarketingCapture 1`, the app seeds data, then a coordinator walks a list of `CaptureStep`s — each step navigates, waits for settle, snapshots, and cleans up
3. PNGs are written to the app's sandbox `Documents/marketing/<locale>/` directory
4. A shell script builds once, installs, then loops locales by relaunching with `-AppleLanguages (xx) -AppleLocale xx`, pulling files out via `simctl get_app_container`

## Output Layout

```
marketing/
    <locale>/           e.g. en, de, es, fr, ja
        01-home.png
        02-<screen>.png
        ...
        NN-<screen>.png
        elements/
            card-<name>.png
            widget-<family>-<size>.png
            chart-<name>.png
```

Put `marketing/` in `.gitignore`. These are outputs, not source.

## Verification Checklist

Before declaring the capture pipeline done, verify:

- [ ] All locales produced N files (where N = screens + elements)
- [ ] File sizes differ between locales (confirms translations actually render — if `en/settings.png` and `de/settings.png` are byte-identical, locale switching didn't take effect)
- [ ] Read 2-3 screens visually for the primary locale and confirm they show the expected content
- [ ] Read the same screens for at least one other locale and confirm localized strings are present
- [ ] Read at least one widget render and one card render to verify backgrounds and corners look right
- [ ] No screenshot shows a screen from a *different* step (the most common bug — an undismissed sheet from the previous step)

## Templates

- `templates/MarketingCapture.swift.template` — skeleton of the capture file with step-based coordinator. Reference the body of this skill for the patterns to apply.
- `templates/capture-marketing.sh.template` — skeleton of the shell script. Replace the bundle ID, scheme name, and simulator name for each project.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Capture planning](references/capture-planning.md): new or changed harness requirements, exploration, design, and implementation planning.
- [Capture architecture](references/capture-architecture.md): building the step coordinator or capturing non-default state.
- [Demo data](references/demo-data.md): missing or inadequate marketing seed data.
- [Element rendering](references/element-rendering.md): isolated transparent elements, cards, or widgets.
- [Capture gotchas](references/capture-gotchas.md): the relevant SwiftData, CloudKit, navigation, widget, or Live Activity capture hazard.

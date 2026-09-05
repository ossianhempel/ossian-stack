# Capture Planning

Read for new or changed harness requirements, exploration, design, and implementation planning. Follow the scope and safety contract in the skill entry point.

## Process

Use the existing capture harness when it meets the request. Build or revise a harness only as needed. Reuse supplied inputs and approved designs; the steps below fill missing information and implementation, not mandatory repeat intake.

### Step 1: Gather requirements

Determine these inputs from the request, session, and code. Ask only for missing choices; batch independent questions and defer only those that depend on an unanswered choice:

1. **Screens to capture** — "Which screens do you want? Give me the navigation path or the tab name for each." Get a concrete list, not "the main flows".
2. **Isolated elements** — "Any components you want rendered independently with transparent backgrounds? (carousel cards, widgets, hero tiles, charts, etc.)"
3. **Locales** — "Which locales? (a) all locales in your `Localizable.xcstrings`, (b) an App Store subset I'll specify, or (c) let me give you an explicit list." If (a), grep the `.xcstrings` file for locale codes:
   ```bash
   python3 -c "import json; d=json.load(open('<path>/Localizable.xcstrings')); langs=set(); [langs.update(v.get('localizations',{}).keys()) for v in d['strings'].values()]; print(sorted(langs))"
   ```
4. **Device** — "Which simulator? (6.1\" iPhone 17 recommended for iOS 26 design features)" — verify the device is available via `xcrun simctl list devices available`.
5. **Appearance** — "Light only, dark only, or both?"
6. **Seed data** — "How is demo data populated today? (a) fresh install seeds it automatically, (b) there's a debug 'Load Demo Data' button, (c) you add it manually, (d) no demo data exists yet." Then: "Is the existing data exhaustive enough that every screen you listed looks populated for marketing? Audit it with the user."

### Step 2: Exploration

Before writing any code, explore the codebase enough to answer:

- Does the project use **Xcode synchronized folder groups** (Xcode 16+, `PBXFileSystemSynchronizedRootGroup`)? If yes, new files auto-include in their target — no pbxproj edits needed. Check with `grep -c PBXFileSystemSynchronized <proj>.xcodeproj/project.pbxproj`.
- **What is the root navigation pattern?**
  - `TabView(selection:)` — most common. You need: the `@State selectedTab` binding, tab indices, and which tabs have nested `NavigationStack`.
  - `NavigationStack` (single stack with a router) — you need: the path binding or router object, plus the set of `NavigationLink(value:)` / `.navigationDestination` types.
  - `NavigationSplitView` — you need: the sidebar selection binding, detail column's navigation state.
  - Custom coordinator / UIKit host — you need: the coordinator's `navigate(to:)` method or equivalent.
- How are **deep links** routed? Find the `onOpenURL` handler and the enum/switch that maps URLs to navigation state.
- Where are **demo data seeders** defined? Trace the code path from the debug button (if any) to the function that actually writes to `ModelContext`. If no seeder exists, see "Creating a demo data seeder" below.
- Do **widgets** live in a separate target? Are the widget view files and entry types in the main app target too? (Almost certainly no — they need to be added if you want to render them via ImageRenderer.)
- Does the app use **Live Activities** / ActivityKit? If yes, flag this as a known gotcha (see below).
- Does the app use **SwiftData + CloudKit sync** (`cloudKitDatabase: .automatic`)? If yes, flag as a known gotcha.
- Does any view need to be **captured in a non-default state**? (e.g. a timer mid-countdown, a form partially filled, a chart with specific values). If yes, each needs a `static var` priming mechanism (see "Priming view state" below).

### Step 3: Present design to user

Summarize a new capture design in this structure. Ask for approval only for unresolved consequential design choices or a scope change; an already specified or approved capture request can proceed:

1. Architecture (in-app capture mode, single file, DEBUG-gated)
2. File list (exact paths you'll create / modify)
3. Screen-by-screen capture plan (how each screen is reached — tab index, navigation path, sheet trigger)
4. Capture ordering rationale (which screens must come before others — see gotcha #5)
5. Element rendering approach (which components, how they'll be wrapped)
6. Output layout (folder structure, naming convention)
7. Known gotchas relevant to this project (flagged from Step 2)
8. Primed states needed (which views, what static vars)

### Step 4: Implement

Use the templates in `../templates/` as starting points. They are **reference patterns**, not copy-paste scaffolding — every project has different navigation, models, and views. The templates show the building blocks; you compose them for the target app.

Key files to produce:

- `<AppName>/Debug/MarketingCapture.swift` — the whole capture system, DEBUG-only. Contains:
  - `MarketingCapture` enum (launch arg parsing, output helpers, window snapshot, priming vars)
  - `MarketingCaptureCoordinator` class (walks `[CaptureStep]` and snapshots each)
  - `MarketingElementHarness` enum (ImageRenderer renders of cards, widgets, charts)
- `<AppName>/ContentView.swift` (or wherever the root view lives) — DEBUG hook that seeds data and runs the coordinator.
- Any views that need primed states — DEBUG-gated `.onAppear` hooks and `.onReceive` dismiss listeners.
- `scripts/capture-marketing.sh` — build + install + per-locale loop.
- `.gitignore` — add `marketing/`.

### Step 5: Verify iteratively

Do **not** hand the script to the user and wait. Run it yourself against a simulator and verify at least one locale before declaring done. Read the output PNGs with the Read tool to visually verify each screen shows what you expect. Common runtime issues are listed in "Known Gotchas" below.

When you find an issue, fix it, rerun the whole script (not just the failing locale — fixes can regress earlier locales), and re-verify visually.

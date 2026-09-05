# Capture Architecture

Read for building the step coordinator or capturing non-default state. Follow the scope and safety contract in the skill entry point.

## Architecture: Step-Based Capture

The coordinator drives capture by walking a list of `CaptureStep` values. Each step is self-contained: it knows how to navigate to its screen, how long to wait, and how to clean up afterward.

```swift
struct CaptureStep {
    let name: String                        // output filename, e.g. "01-home"
    let navigate: @MainActor () -> Void     // put the app in the right state
    let settle: Duration                    // wait for animations/loads
    let cleanup: (@MainActor () -> Void)?   // tear down before next step
}
```

The coordinator is a simple loop:

```swift
for step in steps {
    step.navigate()
    try? await Task.sleep(for: step.settle)
    if let image = MarketingCapture.snapshotKeyWindow() {
        MarketingCapture.writePNG(image, name: step.name)
    }
    step.cleanup?()
    try? await Task.sleep(for: .milliseconds(400))  // cleanup animation
}
```

### Building steps for different navigation patterns

**TabView app** (most common):
```swift
// Simple tab switch — just set the index
CaptureStep(name: "01-home", navigate: { setTab(0) }, settle: .milliseconds(1800), cleanup: nil)

// Tab + presented sheet
CaptureStep(
    name: "05-timer-setup",
    navigate: {
        setTab(3)
        pendingBrewRecipe = someRecipe
    },
    settle: .milliseconds(2000),
    cleanup: {
        NotificationCenter.default.post(name: MarketingCapture.dismissSheetNotification, object: nil)
        pendingBrewRecipe = nil
    }
)
```

**NavigationStack + router app:**
```swift
// Push a route onto the stack
CaptureStep(
    name: "02-detail",
    navigate: { router.push(.itemDetail(item)) },
    settle: .milliseconds(1800),
    cleanup: { router.popToRoot() }
)
```

**NavigationSplitView app:**
```swift
// Select sidebar item, then detail
CaptureStep(
    name: "03-detail",
    navigate: {
        sidebarSelection = .recipes
        detailSelection = recipes.first
    },
    settle: .milliseconds(1800),
    cleanup: { detailSelection = nil }
)
```

### Ordering: the stacking rule

**Capture any screen that needs a "clean" navigation state BEFORE screens that push onto the same stack.** Nested `NavigationPath` / `@State` inside child views can't be popped from the coordinator. So:

```
Good:  Shelf (clean list) → Coffee Detail (pushes onto shelf's stack)
Bad:   Coffee Detail → Shelf (stack still has detail pushed)
```

If two screens share a NavigationStack, capture the root-level view first.
## Priming View State

Some screens need to be captured in a specific non-default state — a timer mid-countdown, a chart with particular values, a form half-filled. The pattern:

1. Add a `static var` to `MarketingCapture` for each priming value:
   ```swift
   /// Set by the coordinator before presenting the timer view.
   /// The view reads this in .onAppear to jump to a specific elapsed time.
   static var pendingElapsedSeconds: Int?

   /// Set to true to show the assessment overlay on the timer.
   static var pendingShowAssessment: Bool = false
   ```

2. In the target view, add a DEBUG-gated `.onAppear` that reads the priming value:
   ```swift
   .onAppear {
       #if DEBUG
       if MarketingCapture.isActive, let elapsed = MarketingCapture.pendingElapsedSeconds {
           phase = .active
           timerVM.elapsedTime = TimeInterval(elapsed)
           timerVM.start()
           DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) { timerVM.pause() }
       }
       #endif
   }
   ```

3. In the coordinator, set the var before navigating:
   ```swift
   CaptureStep(
       name: "06-timer-midway",
       navigate: {
           MarketingCapture.pendingElapsedSeconds = 75
           openTimerSheet(someRecipe)
       },
       settle: .milliseconds(2400),
       cleanup: {
           MarketingCapture.pendingElapsedSeconds = nil
           NotificationCenter.default.post(name: MarketingCapture.dismissSheetNotification, object: nil)
       }
   )
   ```

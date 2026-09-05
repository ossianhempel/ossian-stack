# Capture Gotchas

Read for the relevant SwiftData, CloudKit, navigation, widget, or Live Activity capture hazard. Follow the scope and safety contract in the skill entry point.

## Known Gotchas

These are all real bugs that bit a real project. Treat this list as load-bearing.

### 1. Live Activities persist across app launches

ActivityKit Live Activities **outlive process termination**. If your app starts a Live Activity during capture (e.g. via a timer's `start()`), then the next locale's relaunch will inherit it. Combined with a fresh seed that deletes the models the stale LA references, you get SwiftData persisted-property assertions.

Fix: call `<ActivityManager>.shared.endImmediately()` at the very start of the marketing capture block, before touching data. Also call `timerVM.stop()` (or whatever properly ends the LA) in the view's `onDisappear` when in capture mode.

### 2. Don't re-seed on every locale

Seeding SwiftData + CloudKit per locale causes sync churn and crashes. The SwiftData store persists across relaunches — the data is locale-agnostic demo content, so seed **once** on the first run and skip subsequent runs:

```swift
contentVM.fetchItems()
if contentVM.allItems.isEmpty {
    DemoDataSeeder.seedIfEmpty(in: modelContext)
    contentVM.fetchItems()
}
```

### 3. ViewModels that setup before the seed hold stale snapshots

If the root view's `onAppear` calls `someVM.setup(modelContext:)` **before** the marketing seed runs, the VM holds a snapshot of the empty store. After seeding, call `someVM.refresh()` (or its equivalent fetch method) for every VM whose data you need.

### 4. Setting a trigger binding to nil does NOT dismiss a sheet

If a parent view presents a `.fullScreenCover(item: $request)` and `request` is driven by an internal `@State`, then setting the *trigger* binding (e.g. `pendingItem = nil`) does nothing to the cover. The cover stays up, and your next screenshot captures it instead of the screen you navigated to.

Fix: broadcast a dismiss signal via NotificationCenter, and have the presented view listen:

```swift
// MarketingCapture.swift
static let dismissSheetNotification = Notification.Name("MarketingCapture.dismissSheet")

// In presented view body
.onReceive(NotificationCenter.default.publisher(for: MarketingCapture.dismissSheetNotification)) { _ in
    dismiss()
}
```

Then in the step's `cleanup`, post the notification and allow **at least 900ms** for the cover animation to complete before the next step begins.

### 5. NavigationPath can't be popped from outside

If a child view holds `@State private var navigationPath = NavigationPath()` and a deep link pushes onto it, the coordinator can't reach in to pop. Solution: **reorder your capture sequence** so screens that push onto a stack come AFTER screens that need a clean stack. Example: capture Shelf first, then push into Coffee Detail — don't do it the other way around.

### 6. Widget views normally live in the extension target only

If the user's widget views are only in the widget extension target, you can't reference them from `MarketingCapture.swift` in the main app target. You need to either:

- **(a)** Add the widget view files (and their entry types and any shared helpers) to the main app target's membership. If the project uses synchronized folder groups, this means editing `PBXFileSystemSynchronizedBuildFileExceptionSet.membershipExceptions`. **CRITICAL GOTCHA: `membershipExceptions` is an INCLUSION list, not an exclusion list.** Files listed there ARE members of the target, not excluded from it. Read this twice before editing.
- **(b)** Skip widget rendering from the capture harness and let the user do them manually.

You'll also need to exclude `<App>WidgetBundle.swift` from the main app target (it has `@main` and conflicts with the app's `@main`).

### 7. `ImageRenderer` + `ProgressView(value:total:)` = prohibited symbol

Without an explicit style, `ProgressView` determinate renders as a red circle-with-slash when composited through ImageRenderer. Fix: `.progressViewStyle(.linear)` on the ProgressView. It's a no-op in normal rendering and fixes the render glitch.

### 8. `.containerBackground(for: .widget)` is a no-op outside widget context

When you render a widget view via ImageRenderer in the app, its `.containerBackground` does nothing — the widget's background is transparent, and pixels outside the content are bare. You must wrap the widget render with an explicit background color + rounded rect clip:

```swift
content()
    .padding(16)  // widget container normally provides this
    .frame(width: size.width, height: size.height)
    .background(theme.background)
    .clipShape(RoundedRectangle(cornerRadius: 22, style: .continuous))
```

Home-screen widget corner radius on iPhone: ~22pt. Lock-screen accessory radius: ~8pt.

### 9. iPhone 8 Plus is gone on iOS 26

If the user asks for a "6.5\" iPhone" (legacy App Store size), note that iOS 26+ simulators don't include iPhone 8 Plus / iPhone 11 Pro Max. Options: (a) install an older iOS runtime via Xcode > Settings > Platforms, or (b) fall back to a modern 6.1\" like iPhone 17 for iOS 26 design features.

### 10. Locale launch arguments

Pass `-AppleLanguages (xx) -AppleLocale xx` at every `simctl launch`. The parens around the language code are mandatory (it's a plist array literal). Use `Locale.current.language.languageCode?.identifier` for folder naming — it's more robust than `Locale.current.identifier` which may include region suffixes like `en_US`.

### 11. SwiftUI animations in ImageRenderer

`ImageRenderer` captures a single frame — it doesn't wait for animations. If your component has an `.onAppear` animation (chart drawing, number counting up), the render may capture the initial state. Either disable the animation in capture mode or add an explicit delay before rendering:

```swift
try? await Task.sleep(for: .milliseconds(500))  // let onAppear animations finish
let renderer = ImageRenderer(content: view)
```

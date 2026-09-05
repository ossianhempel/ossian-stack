# Practice Inventory

Read for inventorying actual SDK/data practices and missing document or regional choices. Follow the scope and safety contract in the skill entry point.

## Pre-Generation Checks

Before generating documents, gather context from the project.

### 1. Look for Existing Legal Documents

```
Glob: **/privacy*.md, **/privacy*.html, **/privacy*.txt
Glob: **/terms*.md, **/terms*.html, **/terms*.txt
Glob: **/eula*.md, **/eula*.html, **/eula*.txt
Glob: **/legal/**
```

If existing documents found, ask user whether to replace or update them.

### 2. Check for Third-Party SDK Usage

```
Grep: "Firebase" or "GoogleAnalytics" or "Crashlytics"
Grep: "Mixpanel" or "Amplitude" or "PostHog"
Grep: "AdMob" or "AppLovin" or "UnityAds"
Grep: "FacebookSDK" or "GoogleSignIn" or "SignInWithApple"
Grep: "Sentry" or "Bugsnag" or "DataDog"
Grep: "RevenueCat" or "Adapty" or "Qonversion"
Grep: "TelemetryDeck" or "Plausible" or "CountlySDK"
```

Note detected SDKs to auto-populate data collection sections.

### 3. Detect Data Collection Patterns in Code

```
Grep: "UserDefaults" -- Local preferences storage
Grep: "CoreData" or "SwiftData" or "NSPersistentContainer" -- Local database
Grep: "CloudKit" or "CKContainer" -- Cloud sync
Grep: "URLSession" or "Alamofire" -- Network calls
Grep: "HealthKit" or "HKHealthStore" -- Health data
Grep: "CLLocationManager" or "CoreLocation" -- Location data
Grep: "AVCaptureSession" or "PHPhotoLibrary" -- Camera/photos
Grep: "Contacts" or "CNContactStore" -- Contacts access
Grep: "ATTrackingManager" -- App Tracking Transparency
Grep: "ASAuthorizationAppleIDProvider" -- Sign in with Apple
```

### 4. Check Info.plist for Permission Usage Descriptions

```
Grep: "NSCameraUsageDescription" or "NSPhotoLibraryUsageDescription"
Grep: "NSLocationWhenInUseUsageDescription" or "NSLocationAlwaysUsageDescription"
Grep: "NSHealthShareUsageDescription" or "NSHealthUpdateUsageDescription"
Grep: "NSContactsUsageDescription" or "NSMicrophoneUsageDescription"
Grep: "NSUserTrackingUsageDescription"
```
## Configuration Questions

Ask the user via AskUserQuestion:

### 1. What documents do you need?

- Privacy Policy only
- Terms of Service only
- EULA only
- All three (recommended for App Store apps)

### 2. What data does your app collect?

- No user data (fully offline, no accounts)
- Anonymous analytics only (usage events, crash data)
- Account with email (sign-in required)
- Account with personal info (name, email, profile, preferences)
- Health or financial data (triggers additional compliance sections)

### 3. What third-party services does your app use?

- None
- Analytics only (e.g., TelemetryDeck, Firebase Analytics)
- Analytics + crash reporting (e.g., Sentry, Crashlytics)
- Advertising (e.g., AdMob, AppLovin)
- Social login (e.g., Sign in with Apple, Google Sign-In)
- Multiple of the above (list them)

### 4. Does your app target or allow children under 13?

- No
- Yes (triggers COPPA section and stricter data practices)

### 5. Where will you host these documents?

- GitHub Pages (free, Markdown to HTML)
- In-app (Settings screen with WKWebView or Text view)
- Personal/company website
- All of the above (recommended -- Apple requires a publicly accessible URL)

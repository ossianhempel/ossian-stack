---
name: asc
description: "Operate App Store Connect with asc: metadata, pricing, builds, TestFlight, signing, submissions, analytics, and release automation."
---

# App Store Connect

Use this skill for App Store Connect work through the `asc` CLI. Select the smallest reference that covers the request. Read [`references/cli-usage.md`](references/cli-usage.md) when command syntax, authentication, output, pagination, or feature discovery is uncertain.

## Route the request

| Intent | Reference |
|---|---|
| Resolve app, build, version, TestFlight, or submission IDs | [`references/id-resolver.md`](references/id-resolver.md) |
| Pull, validate, preview, and push canonical listing metadata | [`references/metadata-sync.md`](references/metadata-sync.md) |
| Localize app and version metadata | [`references/localize-metadata.md`](references/localize-metadata.md) |
| Audit ASO fields and keyword coverage | [`references/aso-audit.md`](references/aso-audit.md) |
| Draft, localize, review, and upload What's New text | [`references/whats-new-writer.md`](references/whats-new-writer.md) |
| Set subscription or IAP prices by territory | [`references/ppp-pricing.md`](references/ppp-pricing.md) |
| Reconcile App Store products with RevenueCat | [`references/revenuecat-catalog-sync.md`](references/revenuecat-catalog-sync.md) |
| Localize subscriptions, groups, and IAP versions | [`references/subscription-localization.md`](references/subscription-localization.md) |
| Inspect build processing, distribution, or cleanup | [`references/build-lifecycle.md`](references/build-lifecycle.md) |
| Build, archive, export, or upload an IPA or PKG | [`references/xcode-build.md`](references/xcode-build.md) |
| Manage signing certificates, profiles, devices, or shared identities | [`references/signing-setup.md`](references/signing-setup.md) |
| Manage TestFlight groups, testers, builds, and What to Test notes | [`references/testflight-orchestration.md`](references/testflight-orchestration.md) |
| Diagnose crashes, beta feedback, hangs, disk writes, or launch issues | [`references/crash-triage.md`](references/crash-triage.md) |
| Diagnose submission readiness, review state, cancellation, or retry | [`references/submission-health.md`](references/submission-health.md) |
| Stage and submit an App Store release | [`references/release-flow.md`](references/release-flow.md) |
| Define or run `.asc/workflow.json` automation | [`references/workflow.md`](references/workflow.md) |
| Download App Analytics reports | [`references/analytics-reports.md`](references/analytics-reports.md) |
| Notarize and staple a macOS artifact | [`references/notarization.md`](references/notarization.md) |
| Create an ad hoc private distribution package | [`references/ad-hoc-distribution.md`](references/ad-hoc-distribution.md) |
| Create an app record when the public API cannot do it | [`references/app-create-ui.md`](references/app-create-ui.md) |
| Operate Apple Ads campaigns and reports | [`references/apple-ads.md`](references/apple-ads.md) |
| Inspect, resize, validate, or upload App Store screenshots | [`references/screenshot-resize.md`](references/screenshot-resize.md) |
| Install or diagnose Xcode Cloud marketing-version and build-number guards | [`references/version-guard.md`](references/version-guard.md) |

For automated multi-locale Simulator capture and framing, use `ios-marketing-capture`, then return here for validation and upload. For keyword and competitor research outside App Store Connect, use `app-store-optimization`.

## Release boundary

For a requested iOS release whose next action depends on a repository promotion PR, use `release-ios-app` to satisfy its release PR gate first. Continue here when that gate is complete or when the request is an independent App Store Connect operation.

Before a mutation, inspect the current remote state and produce the exact plan. Use dry-run or preview commands when available. Apply only the scope the user authorized, then read the affected resource back from App Store Connect. Keep upload, internal TestFlight distribution, external beta review, App Review submission, and public release as separate states.

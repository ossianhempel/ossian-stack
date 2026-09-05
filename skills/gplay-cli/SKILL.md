---
name: gplay-cli
description: Operate Google Play Console with the `gplay` CLI across Android builds, releases and staged rollouts, store metadata and screenshots, subscriptions and in-app products, pricing, testers, reviews, vitals, reports, purchases, users, preflight checks, and Fastlane migration. Use this skill whenever work touches Google Play Console or publishing an Android app.
---

# Google Play Console CLI

Use `gplay` as the Google Play counterpart to the plugin's App Store Connect
skills. This is one public entrypoint: select and read only the playbooks needed
for the current task.

Read [`references/local-conventions.md`](references/local-conventions.md) first
for any authenticated or mutating operation. It defines credential handling,
discovery, previews, authorization boundaries, and release evidence. Then read
[`references/cli-usage.md`](references/cli-usage.md) when constructing commands.

## Pick the playbook

| Task | Read |
| --- | --- |
| Build, sign, or package an APK/AAB | [`references/gradle-build.md`](references/gradle-build.md) |
| Upload or release to internal, beta, or production | [`references/release-flow.md`](references/release-flow.md) |
| Promote, halt, resume, or complete a staged rollout | [`references/rollout-management.md`](references/rollout-management.md) |
| Validate an artifact offline before upload | [`references/preflight.md`](references/preflight.md) |
| Run authenticated readiness and policy checks | [`references/submission-checks.md`](references/submission-checks.md) |
| Sync listings, localizations, release notes, or screenshots | [`references/metadata-sync.md`](references/metadata-sync.md) and, for images, [`references/screenshot-automation.md`](references/screenshot-automation.md) |
| Create subscriptions, base plans, offers, or one-time products | [`references/iap-setup.md`](references/iap-setup.md) |
| Set regional or PPP prices | [`references/ppp-pricing.md`](references/ppp-pricing.md) |
| Manage tester groups | [`references/testers-orchestration.md`](references/testers-orchestration.md) |
| Inspect vitals or respond to reviews | [`references/vitals-monitoring.md`](references/vitals-monitoring.md) or [`references/review-management.md`](references/review-management.md) |
| Verify purchases from a backend | [`references/purchase-verification.md`](references/purchase-verification.md) |
| Download financial or statistics reports | [`references/reports-download.md`](references/reports-download.md) |
| Manage developer users or app grants | [`references/user-management.md`](references/user-management.md) |
| Migrate Fastlane metadata | [`references/migrate-fastlane.md`](references/migrate-fastlane.md) |

## Release spine

For a release, combine the focused playbooks in this order:

1. Build and sign the artifact.
2. Run offline preflight before credentials or uploads are involved.
3. Run authenticated submission checks and inspect the existing tracks.
4. Preview the intended mutation with `--dry-run` when supported.
5. Confirm the concrete production publication or rollout change is authorized
   by the current request or existing session context.
6. Execute the release through the CLI's high-level workflow or its explicit
   edit lifecycle: create, modify, validate, commit.
7. Read back the target track and report the observed version, status, and
   rollout fraction. An upload alone is not release proof.

For an Expo release routed from the iOS release workflow, preserve its version and
artifact decisions and use this skill for the Google Play half. Do not rebuild
or resubmit the iOS half.

## Done

The requested Google Play state is observed after the operation. Report the
package, track, version code, release status, rollout fraction when applicable,
checks performed, and any Console-only action that remains.

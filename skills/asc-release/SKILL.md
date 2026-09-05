---
name: asc-release
description: "Build and upload iOS/macOS artifacts, check ASC readiness, submit releases, and define asc workflows."
---

# asc release

Everything for getting a build from Xcode into App Store Connect and submitted for review, plus the `asc` CLI conventions and repo-local automation harness that underpin it. Read the focused reference file for the task at hand — each is self-contained.

## Pick the reference

| You are... | Read |
|---|---|
| Running or designing any `asc` command (flags, output, auth, pagination, discovery) | [`reference/cli-usage.md`](reference/cli-usage.md) |
| Building / archiving / exporting an IPA or PKG, or editing Xcode version & build numbers | [`reference/xcode-build.md`](reference/xcode-build.md) |
| Deciding if the app is ready and driving the submission flow (first-time availability/IAP/subscription/Game Center/App Privacy blockers) | [`reference/release-flow.md`](reference/release-flow.md) |
| Defining/validating/running `.asc/workflow.json` multi-step automations for local + CI | [`reference/workflow.md`](reference/workflow.md) |

For a requested iOS release whose next action depends on a repository promotion PR,
use `release-ios-app` to satisfy its release-PR gate first: create/reuse the manifest's
PR, invoke or resume its babysit drive, then wait for the manual merge confirmation.
If that gate was already satisfied by the caller, continue here without restarting
it. Standalone ASC metadata, upload, readiness, or submission work with no required
repository PR stays on its focused reference; do not invent or wait on an unrelated PR.

## Typical end-to-end order

1. **Build** — archive + export the artifact and set a unique build number (`reference/xcode-build.md`).
2. **Verify readiness** — `asc submit preflight` / `asc release stage`, resolve blockers (`reference/release-flow.md`).
3. **Submit** — `asc release run --dry-run` then `--confirm` (`reference/release-flow.md`).
4. **Automate** — capture the repeatable parts in `.asc/workflow.json` (`reference/workflow.md`).

`reference/cli-usage.md` is the conventions layer the other three assume (verb choice, `--confirm` on destructive ops, JSON output, auth/timeout env vars). Skim it once if you're new to `asc`.

> Related: version/build-number collision prevention as an installable CI standard lives in the separate **asc-version-guard** skill. App-pricing and RevenueCat catalog work lives in **asc-pricing**. Metadata, ASO, and release notes live in **asc-metadata**.

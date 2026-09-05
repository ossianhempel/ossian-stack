---
name: asc-pricing
description: "Set App Store subscription and IAP prices by territory, or reconcile the ASC catalog with RevenueCat."
---

# asc pricing

Two related but distinct jobs on the subscription/IAP catalog: setting **prices** per territory, and keeping the **catalog** in sync with RevenueCat. Different scopes and execution models (shell/CSV vs. MCP) — read the one you need.

## Pick the reference

| You are... | Read |
|---|---|
| Setting territory-specific or PPP pricing (setup, pricing summary, CSV import with dry-run, scheduled price changes, price points) | [`reference/ppp-pricing.md`](reference/ppp-pricing.md) |
| Reconciling ASC subscriptions/IAPs with RevenueCat (products, entitlements, offerings, packages) — bootstrap or two-way sync | [`reference/revenuecat-catalog-sync.md`](reference/revenuecat-catalog-sync.md) — with [`revenuecat-examples.md`](reference/revenuecat-examples.md) and [`revenuecat-references.md`](reference/revenuecat-references.md) |

## Key boundaries

- **Pricing** changes settings on products that already exist. **Catalog sync** is product lifecycle: RevenueCat MCP configures RevenueCat only — you must `asc ... create` the ASC products *first*.
- Cross-system primary key: ASC `productId` == RevenueCat `store_identifier`. Keep it stable once live; never key off display names.
- Both default to safe/audit-first: start read-only, require explicit confirmation, never auto-delete, and prefer CSV `--dry-run` before applying bulk price changes.

> Related: build/submit flow lives in **asc-release**; ASO, localization, and release notes live in **asc-metadata**.

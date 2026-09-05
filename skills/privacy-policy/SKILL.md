---
name: privacy-policy
description: Generate app privacy policies, terms, EULAs, App Store data disclosures, Privacy Nutrition Label mapping, SDK/data collection checks, region-specific legal docs.
---

# Privacy Policy & Legal Document Generator

Generate ready-to-use privacy policies, terms of service, and EULAs tailored to your app's data practices, third-party services, and target markets.

> **Disclaimer:** This skill generates template legal documents based on common indie app scenarios. Consult a qualified lawyer for apps handling sensitive data (health, financial, children's data), apps with complex data sharing arrangements, or apps operating in highly regulated industries. These templates are a strong starting point -- not a substitute for legal counsel.

Start with the practice inventory. Choose only the requested documents and applicable regions; confirm missing facts instead of inventing data practices. Reuse decisions in the request. Keep draft, publication, and App Store submission scope distinct. Verify current authoritative requirements before legal guidance or final disclosures.

## When This Skill Activates

Use this skill when the user:
- Needs a privacy policy for their app
- Needs terms of service or EULA
- Apple requires a privacy policy for App Store submission
- Is adding analytics, ads, or crash reporting and needs to update their privacy policy
- Asks about data collection disclosure or privacy compliance
- Mentions GDPR, CCPA, DPDP, or COPPA requirements for their app
- Wants to know what to declare in Apple's Privacy Nutrition Labels

## Output Format

After generation, provide:

### Files Created

```
docs/
 ├── privacy-policy.md     # Privacy policy with region-specific sections
 ├── terms-of-service.md   # Terms of service (if requested)
 └── eula.md               # End-user license agreement (if requested)
```

### Apple Privacy Nutrition Label Checklist

Provide a checklist the user can follow in App Store Connect.

### Integration Checklist

- [ ] Host documents at a publicly accessible URL
- [ ] Add privacy policy URL to App Store Connect
- [ ] Add legal links to app Settings or About screen
- [ ] Complete Privacy Nutrition Labels in App Store Connect
- [ ] If using ATT, add `NSUserTrackingUsageDescription` to Info.plist
- [ ] Test that privacy policy URL loads correctly
- [ ] Set a calendar reminder to review documents annually

## References

- **templates.md** -- Full legal document templates with placeholders
- Related: `generators/consent-flow` -- GDPR/CCPA consent UI generation
- Related: `generators/account-deletion` -- Account deletion flow (App Store requirement)
- Related: `generators/permission-priming` -- Pre-permission UI for ATT
- Related: `monetization/` -- Subscription terms and pricing disclosures
- Apple App Review Guidelines Section 5.1 (Privacy)
- Apple App Store Connect Privacy Details documentation

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Practice inventory](references/practice-inventory.md): inventorying actual SDK/data practices and missing document or regional choices.
- [Document generation](references/document-generation.md): writing the selected policies, terms, or EULA.
- [Apple disclosures](references/apple-disclosures.md): Privacy Nutrition Labels and Apple-required disclosures.
- [Hosting and integration](references/hosting-and-integration.md): requested hosting and app integration.

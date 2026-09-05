# Apple Disclosures

Read for Privacy Nutrition Labels and Apple-required disclosures. Follow the scope and safety contract in the skill entry point.

## Apple-Required Privacy Disclosures

### App Store Connect Privacy Questions

When submitting to the App Store, Apple asks about data practices. Map generated privacy policy to these questions:

| Apple Question | Where to Find Answer |
|---------------|---------------------|
| Do you or your third-party partners collect data? | "Information We Collect" section |
| Data types collected | Privacy Nutrition Label mapping (Step 4) |
| Is data linked to user identity? | "How We Use Information" section |
| Is data used for tracking? | "Third-Party Services" section |

### Privacy Nutrition Labels

Declare these data types based on your app's practices:

| If Your App... | Declare These Types |
|----------------|-------------------|
| Has user accounts | Contact Info, Identifiers |
| Uses analytics | Usage Data (Product Interaction) |
| Has crash reporting | Diagnostics (Crash Data, Performance Data) |
| Shows ads | Identifiers (Device ID), Usage Data |
| Uses location | Location (Precise or Coarse) |
| Accesses photos | Photos or Videos |
| Accesses health data | Health & Fitness |
| Uses Sign in with Apple | Contact Info (Email), Identifiers (User ID) |

### When ATT (App Tracking Transparency) Is Required

ATT is required when your app:
- Accesses the IDFA (Identifier for Advertisers)
- Links user data with third-party data for advertising
- Shares user data with data brokers

ATT is NOT required for:
- First-party analytics that stays on your server
- Crash reporting
- Fraud detection
- Attribution that does not use IDFA (e.g., SKAdNetwork)

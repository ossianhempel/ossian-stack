# Document Generation

Read for writing the selected policies, terms, or EULA. Follow the scope and safety contract in the skill entry point.

## Generation Process

### Step 1: Select Template Sections

Read `templates.md` for the document templates.

Based on configuration answers, include or exclude sections:

| Answer | Sections Added |
|--------|---------------|
| No user data | Minimal privacy policy (no collection, no sharing) |
| Anonymous analytics | Analytics disclosure, third-party services list |
| Account with email | Account data, authentication, data retention |
| Personal info | Full data collection, user rights, data portability |
| Health/financial | Sensitive data handling, enhanced security, additional consent |
| Children under 13 | COPPA section, parental consent, limited data collection |

### Step 2: Fill in App-Specific Details

Replace template placeholders with detected or user-provided values:
- `[APP_NAME]` -- App display name
- `[DEVELOPER_NAME]` -- Developer or company name
- `[CONTACT_EMAIL]` -- Privacy contact email
- `[EFFECTIVE_DATE]` -- Document effective date
- `[WEBSITE_URL]` -- Developer website or privacy page URL

### Step 3: Add Region-Specific Sections

Include sections based on target markets:

**GDPR (European Union users):**
- Data controller identification
- Lawful basis for processing (consent, legitimate interest, contract)
- Data subject rights (access, rectification, erasure, portability, objection)
- Data Protection Officer contact (if applicable)
- Data retention periods
- Right to lodge complaint with supervisory authority

**CCPA (California users):**
- Categories of personal information collected
- Business purposes for collection
- "Do Not Sell or Share My Personal Information" notice
- Right to know, delete, and opt-out
- Non-discrimination for exercising rights
- Financial incentive disclosure (if applicable)

**DPDP (India users):**
- Data fiduciary identification
- Purpose of data processing
- Consent mechanism
- Data principal rights (access, correction, erasure, grievance redressal)
- Data retention limitations
- Processing of children's data (under 18)

**COPPA (children under 13):**
- Parental consent requirement
- Limited data collection (only what is strictly necessary)
- No behavioral advertising to children
- Parental rights (review, delete, refuse further collection)
- Safe harbor program compliance (if applicable)

### Step 4: Generate Apple Privacy Nutrition Label Mapping

Based on detected data practices, generate a mapping for App Store Connect:

```
Apple Privacy Nutrition Label Mapping
=====================================

Data Types to Declare:
- [ ] Contact Info: Email Address -- Used for: App Functionality, Account
- [ ] Identifiers: User ID -- Used for: App Functionality
- [ ] Usage Data: Product Interaction -- Used for: Analytics
- [ ] Diagnostics: Crash Data -- Used for: App Functionality
- [ ] Diagnostics: Performance Data -- Used for: Analytics

Data Linked to User: [List items linked to user identity]
Data Used to Track: [List items used for cross-app tracking, if any]

Tracking: [Yes/No -- triggers ATT requirement if Yes]
```

### Step 5: Output Documents

Generate documents in Markdown format. Place files based on user's hosting preference:

- **GitHub Pages**: `docs/privacy-policy.md`, `docs/terms-of-service.md`, `docs/eula.md`
- **In-app**: `Resources/Legal/privacy-policy.md`, etc.
- **Website**: Output to clipboard/file for manual upload
- **All**: Generate in `docs/` with guidance for in-app integration

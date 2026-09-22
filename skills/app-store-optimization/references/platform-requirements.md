# Platform Requirements Reference

Technical specifications and metadata requirements for Apple App Store and Google Play Store.

---

## Table of Contents

- [Apple App Store Requirements](#apple-app-store-requirements)
- [Google Play Store Requirements](#google-play-store-requirements)
- [Visual Asset Specifications](#visual-asset-specifications)
- [Localization Requirements](#localization-requirements)
- [Compliance Guidelines](#compliance-guidelines)

---

## Apple App Store Requirements

### Metadata Character Limits

| Field | Character Limit | Notes |
|-------|----------------|-------|
| App Name (Title) | 30 characters | Visible in search results |
| Subtitle | 30 characters | iOS 11+ only, appears below title |
| Promotional Text | 170 characters | Editable without app update |
| Description | 4,000 characters | Not indexed for search |
| Keywords Field | 100 bytes | Comma-separated, no spaces after commas; non-Latin scripts (Arabic, CJK) use 2-3 bytes per char |
| IAP Name | 35 characters | Indexed for search |
| IAP Description | 55 characters | Not indexed |
| In-App Event Name | 30 characters | Indexed; title case required |
| In-App Event Short Description | 50 characters | Indexed; sentence case |
| In-App Event Long Description | 120 characters | Not indexed |
| What's New | 4,000 characters | Release notes for updates |
| Developer Name | 255 characters | Company or individual name |
| Support URL | Required | Must be valid HTTPS URL |
| Privacy Policy URL | Required | Must be valid HTTPS URL |

### Keyword Field Optimization Rules

1. **No duplicates** - Words in title are already indexed
2. **No plurals** - Apple indexes both singular and plural forms
3. **No spaces after commas** - Wastes character space
4. **No brand names** - Violates App Store guidelines
5. **No category names** - Already indexed via category selection

**Example - Efficient keyword field:**
```
task,todo,checklist,reminder,productivity,organize,schedule,planner,goals,habit
```

**Example - Inefficient keyword field (avoid):**
```
task manager, todo list, productivity app, task tracking
```

### App Store Connect Metadata Fields

| Category | Field | Required |
|----------|-------|----------|
| **App Information** | Name | Yes |
| | Subtitle | No |
| | Category | Yes |
| | Secondary Category | No |
| | Content Rights | Yes |
| | Age Rating | Yes |
| **Version Information** | Description | Yes |
| | Keywords | Yes |
| | Promotional Text | No |
| | What's New | Yes (for updates) |
| | Support URL | Yes |
| | Marketing URL | No |
| **Pricing** | Price Tier | Yes |
| | Availability | Yes |

### Age Rating Content Descriptors

| Content Type | None | Infrequent | Frequent |
|--------------|------|------------|----------|
| Cartoon Violence | 4+ | 9+ | 12+ |
| Realistic Violence | 9+ | 12+ | 17+ |
| Sexual Content | 12+ | 17+ | 17+ |
| Profanity | 4+ | 12+ | 17+ |
| Alcohol/Drug Reference | 12+ | 17+ | 17+ |
| Gambling | 12+ | 17+ | 17+ |
| Horror/Fear | 9+ | 12+ | 17+ |

---

## Google Play Store Requirements

### Metadata Character Limits

| Field | Character Limit | Notes |
|-------|----------------|-------|
| App Title | 30 characters | Reduced from 50 in Sept 2021; strongest search signal |
| Short Description | 80 characters | Visible on store listing |
| Full Description | 4,000 characters | Indexed for search keywords |
| Developer Name | 64 characters | Organization or individual |
| Developer Email | Required | Public support contact |
| Privacy Policy URL | Required | Must be valid HTTPS URL |

### Description Keyword Strategy

Google Play has no separate keyword field. Keywords are extracted from:

1. **App Title** - Highest weight, most important
2. **Short Description** - High weight, visible in search
3. **Full Description** - Medium weight, use naturally throughout
4. **Developer Name** - Low weight but indexed

**Keyword Density Guidelines:**
- Primary keyword: 2-3% density in full description
- Secondary keywords: 1-2% each
- Avoid keyword stuffing (>5% triggers spam detection)

### Google Play Console Metadata

| Category | Field | Required |
|----------|-------|----------|
| **Store Listing** | Title | Yes |
| | Short Description | Yes |
| | Full Description | Yes |
| | App Icon | Yes |
| | Feature Graphic | Yes |
| | Screenshots | Yes (min 2) |
| | Video | No |
| **Store Settings** | App Category | Yes |
| | Tags | No |
| | Contact Email | Yes |
| | Privacy Policy | Yes |
| **Content Rating** | IARC Questionnaire | Yes |

### Content Rating (IARC)

| Rating | Age | Description |
|--------|-----|-------------|
| PEGI 3 / Everyone | 3+ | Suitable for all ages |
| PEGI 7 / Everyone 10+ | 7+ | Mild violence, comic mischief |
| PEGI 12 / Teen | 12+ | Moderate violence, mild language |
| PEGI 16 / Mature 17+ | 16+ | Intense violence, strong language |
| PEGI 18 / Adults Only | 18+ | Extreme content |

---

## Visual Asset Specifications

### App Icon Requirements

**Apple App Store:**

| Device | Size | Format |
|--------|------|--------|
| iPhone | 1024x1024 px | PNG, no alpha |
| iPad | 1024x1024 px | PNG, no alpha |
| App Store | 1024x1024 px | PNG, no alpha |
| Spotlight | 120x120 px | PNG |
| Settings | 87x87 px | PNG |

**Google Play Store:**

| Asset | Size | Format |
|-------|------|--------|
| App Icon | 512x512 px | PNG, 32-bit |
| Feature Graphic | 1024x500 px | PNG or JPG |
| Promo Graphic | 180x120 px | PNG or JPG |
| TV Banner | 1280x720 px | PNG or JPG |

### Screenshot Requirements

**Apple App Store:**

| Device | Portrait | Landscape |
|--------|----------|-----------|
| iPhone 6.9" | 1320x2868 px | 2868x1320 px |
| iPhone 6.5" | 1290x2796 px | 2796x1290 px |
| iPhone 5.5" | 1242x2208 px | 2208x1242 px |
| iPad Pro 12.9" | 2048x2732 px | 2732x2048 px |
| iPad 10.5" | 1668x2224 px | 2224x1668 px |

- Minimum: 2 screenshots per device
- Maximum: 10 screenshots per device
- Format: PNG or JPG, no alpha channel
- First 3 screenshots are critical (most users don't scroll)

**Google Play Store:**

| Device | Dimensions | Notes |
|--------|------------|-------|
| Phone | 320-3840 px | Min 2:1 aspect ratio |
| 7" Tablet | 320-3840 px | Min 2:1 aspect ratio |
| 10" Tablet | 320-3840 px | Min 2:1 aspect ratio |
| Chromebook | 320-3840 px | Optional |
| TV | 320-3840 px | For TV apps only |

- Minimum: 2 screenshots
- Maximum: 8 screenshots
- Format: PNG or JPG
- No transparency or borders

### App Preview Video

**Apple App Store:**
- Duration: 15-30 seconds
- Resolution: Match device screenshot size
- Format: M4V, MP4, MOV
- Frame rate: 30 fps
- Audio: Optional but recommended

**Google Play Store:**
- YouTube video link only
- No duration limit (recommend under 2 minutes)
- Landscape orientation preferred
- Must not contain age-restricted content

---

## Localization Requirements

### Priority Markets by Revenue

| Rank | Market | Language Code |
|------|--------|---------------|
| 1 | United States | en-US |
| 2 | Japan | ja |
| 3 | United Kingdom | en-GB |
| 4 | Germany | de-DE |
| 5 | China | zh-Hans (iOS), zh-CN (Android) |
| 6 | South Korea | ko |
| 7 | France | fr-FR |
| 8 | Canada | en-CA, fr-CA |
| 9 | Australia | en-AU |
| 10 | Russia | ru |

### Apple App Store Localization

Supported localizations: 40+ languages

| Language | Locale Code |
|----------|-------------|
| English (US) | en-US |
| English (UK) | en-GB |
| Spanish | es-ES |
| Spanish (Mexico) | es-MX |
| French | fr-FR |
| German | de-DE |
| Japanese | ja |
| Korean | ko |
| Simplified Chinese | zh-Hans |
| Traditional Chinese | zh-Hant |

### Google Play Store Localization

Supported localizations: 75+ languages

Each locale requires:
- Title (50 chars)
- Short description (80 chars)
- Full description (4,000 chars)
- Screenshots (can reuse or localize)

---

## Compliance Guidelines

### Apple App Store Review Guidelines Summary

| Category | Key Requirements |
|----------|-----------------|
| **Safety** | No objectionable content, privacy protection |
| **Performance** | App must work as described, no crashes |
| **Business** | Accurate app description, clear pricing |
| **Design** | Follow Human Interface Guidelines |
| **Legal** | Comply with local laws, proper licensing |

**Common Rejection Reasons:**
1. Bugs and crashes (50%+ of rejections)
2. Broken links or placeholder content
3. Misleading app descriptions
4. Privacy policy missing or incomplete
5. In-app purchase issues

### Google Play Developer Policies

| Policy Area | Requirements |
|-------------|--------------|
| **Restricted Content** | No hate speech, violence, gambling (without license) |
| **Privacy** | Data collection disclosure, privacy policy |
| **Monetization** | Clear pricing, compliant IAPs |
| **Ads** | No deceptive ads, proper disclosure |
| **Store Listing** | Accurate description, no keyword stuffing |

**Common Suspension Reasons:**
1. Policy violation (content, ads, permissions)
2. Repetitive content (clone apps)
3. Impersonation (fake apps)
4. Intellectual property infringement
5. Malicious behavior

### Privacy Requirements

**Apple (App Tracking Transparency):**
- ATT prompt required for tracking
- Privacy nutrition labels mandatory
- Data collection disclosure required

**Google (Data Safety):**
- Data safety section mandatory
- Data collection and sharing disclosure
- Security practices declaration

---

## Apple: Indexing & Recent Changes

What Apple actually indexes (and what it does not):

| Field | Indexed for search? | Notes |
|-------|--------------------|-------|
| Title | Yes | Strongest signal |
| Subtitle | Yes | |
| Keywords field | Yes (hidden) | 100 bytes |
| Description | **No** | Conversion only — Apple confirmed |
| Promotional Text | **No** | Apple confirmed; editable without a release |
| Screenshot captions | **Yes (since June 2025)** | AI extraction of caption text |
| In-app events | Yes | Appear in search |
| IAP names | Yes | |
| Developer name | No | |

- **Screenshot captions indexed since June 2025** — caption copy is now a ranking surface, not just conversion copy.
- **Custom Product Pages appear in organic search since July 2025** — up to 70 CPPs (plus the default page); each keyword combination must be unique to one CPP.
- **In-app events:** max 15 approved in App Store Connect, max 10 published simultaneously, max 31 days each, up to 14 days of pre-event promotion.
- **App preview video:** up to 3 per app, 15-30 seconds, max 500 MB.
- **SKStoreReviewController:** max 3 rating prompts per 365-day period; the system may show fewer. Never use a custom button to request a review.
- **Product Page Optimization (A/B test):** up to 3 treatments vs the original; icon, screenshots, and preview video are testable — title, subtitle, description, and keywords are **not**; one test at a time; max 90 days; cannot be modified once started.

## Apple: Metadata Rejection Triggers

| Guideline | Rejection trigger |
|-----------|-------------------|
| 2.3.1 | Hidden features, misleading marketing, false pricing |
| 2.3.2 | Not disclosing IAPs in description/screenshots |
| 2.3.3 | Screenshots that don't show the app in use (splash/login only) |
| 2.3.4 | Preview videos using non-app content |
| 2.3.5 | Wrong category selected |
| 2.3.7 | Keyword stuffing: trademarks, competitor names, pricing, irrelevant terms |
| 2.3.8 | Metadata not appropriate for all audiences (must be 4+ rated) |
| 2.3.10 | Other platform names/imagery (Android, etc.) in metadata |
| 2.3.12 | Generic What's New for significant changes |
| 2.3.13 | Inaccurate in-app event metadata |

## Google Play: Prohibited Metadata Content

Enforced since Sept 2021. Applies to **title, icon, and developer name** unless
the term is a registered brand:

- Emojis, emoticons, repeated special characters
- ALL CAPS
- Performance claims: "top", "best", "#1", "free", "no ads"
- Misleading store performance or endorsement
- Calls to action: "update now", "download now"

The same performance claims and CTAs are prohibited in the **short description**,
along with unattributed testimonials. **Screenshots, feature graphic, and video**
must not carry time-sensitive taglines or CTAs, and must authentically show app
functionality.

## Google Play: Android Vitals Ranking Thresholds

Apps exceeding these thresholds get **reduced visibility** in search and
recommendations, plus warning labels on the listing.

| Metric | Overall threshold | Per-device threshold |
|--------|-------------------|----------------------|
| User-perceived crash rate | **1.09%** | 8% |
| User-perceived ANR rate | **0.47%** | 8% |
| Excessive partial wake locks | 5% | N/A |

Google evaluates a 28-day rolling average, checked daily. Recovery is automatic
once the rate falls back under threshold.

**Google Play confirmed ranking factors:** metadata relevance (title carries the
most weight; NLP scans title + short + full description), app quality (Android
Vitals), ratings and reviews (85% of featured apps are 4.0+), install volume and
velocity, engagement/retention, update frequency, and localization.

## Experiments & Custom Pages (Both Stores)

| Capability | Apple | Google Play |
|------------|-------|-------------|
| A/B testing | Product Page Optimization | Store Listing Experiments |
| Treatments | 3 vs original | 3 vs control |
| Concurrent tests | 1 | 1 default-graphics experiment |
| Testable | Icon, screenshots, preview video | Icon, feature graphic, screenshots, video, short + full description |
| Not testable | Title, subtitle, description, keywords | — |
| Min duration | — | 7 days (weekday/weekend variance) |
| Custom pages | 70 CPPs (organic since July 2025) | 50 CSLs (100 for partners) |
| Custom-page targeting | Keyword-specific | Country/region, install state, ad campaigns, churned users (28+ days) |

---

## Quick Reference Card

### Apple vs Google Comparison

| Attribute | Apple App Store | Google Play Store |
|-----------|-----------------|-------------------|
| Title Length | 30 chars | 30 chars |
| Subtitle | 30 chars | N/A |
| Short Description | N/A | 80 chars |
| Full Description | 4,000 chars | 4,000 chars |
| Keywords Field | 100 chars | N/A (in description) |
| Promotional Text | 170 chars | N/A |
| Icon Size | 1024x1024 px | 512x512 px |
| Min Screenshots | 2 | 2 |
| Max Screenshots | 10 | 8 |
| Review Time | 24-48 hours | 1-7 days |
| Metadata Update | Requires review | 1-2 hours to index |

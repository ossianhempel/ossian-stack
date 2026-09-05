# Google Play

Read for Android-specific listing research and examples. Follow the scope and safety contract in the skill entry point.

## Google Play (Android) Specifics

Google Play's algorithm differs fundamentally from iOS: the full description is indexed, there is no hidden keyword field, and ratings are continuous (never reset per version). Use this section whenever you're working on a Play Store listing.

### Indexing Model

| Field | Indexed | Notes |
|-------|---------|-------|
| Title (30 chars) | ✓ | Highest weight |
| Short description (80 chars) | ✓ | High weight; first thing in search results |
| Full description (4000 chars) | ✓ | Medium weight — keyword density matters |
| Developer name | ✓ | Low weight |
| Reviews and replies | ✓ | Common review words feed keyword signals |

No equivalent to the iOS 100-char keyword field. Keywords live in the description itself.

### Full Description Structure (Indexed)

```
[Hook — 2–3 sentences]
Lead with the core value prop. Primary keyword in the first 167 chars (above the fold).

[Feature bullets — 5–8 items]
• [Feature]: [Benefit]
Use keywords naturally. Vary phrasing — don't repeat exact phrases.

[Social proof]
"Trusted by X million users" / awards / press mentions

[Call to action]
Download [App Name] today — [value prop].

[Keyword-rich closing paragraph]
Variants, synonyms, and long-tail terms. Natural sentences, not lists.
```

**Keyword density rule:** Primary keyword 3–5 times across the full description (exact + variants). Never stuff.

### Feature Graphic (1024×500px)

Required for the Play Store. Appears at the top of the listing when no video is set.

- Show the core use case in a single image
- Legible text — no tiny copy
- Brand-consistent with screenshots
- Must work without text (text may be truncated on some surfaces)

### Ratings Strategy (Continuous Model)

Unlike iOS, Play ratings are **never reset** — every rating ever given counts toward your average.

To improve a rating:
1. Respond to every 1–3 star review (boosts the algorithmic signal)
2. Replies invite re-rating — users can update their review
3. Fix issues mentioned in low ratings, then reply: "Fixed in version X.X"
4. Use the Play In-App Review API: `ReviewManager.requestReviewFlow()` — prompt after a clear success moment, not on cold open

### Play Store Experiments (Native A/B)

Access: Play Console → Store listing experiments. Supports up to 3 variants for:

- Icon
- Feature graphic
- Screenshots
- Short description
- Full description

Rules: test one element at a time; run for minimum 7 days or until ~1,000 impressions per variant.

### Localization

Google Play indexes descriptions per language. Every locale is a fresh keyword opportunity — translate and localize, don't just auto-translate.

### Pre-Launch (Early Access)

Use Early Access to collect reviews before public launch, get indexed by Google before launch, and get editorial consideration from Google Play.

### Play Listing Audit Template

Score each field 1–10:

```
Title:             [N]/10 — [note]
Short description: [N]/10 — [note]
Full description:  [N]/10 — [note]
Screenshots:       [N]/10 — [note]
Feature graphic:   [N]/10 — [note]
Ratings:           [N]/10 — [note]
Overall:           [N]/60

Top 3 improvements:
1. [specific change with expected impact]
2. [specific change with expected impact]
3. [specific change with expected impact]
```

---

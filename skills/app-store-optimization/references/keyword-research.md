# Keyword Research

Read for keyword discovery, scoring, and prioritization. Follow the scope and safety contract in the skill entry point.

## Keyword Research Workflow

Discover and evaluate keywords that drive app store visibility.

### Workflow: Conduct Keyword Research

1. Define target audience and core app functions:
   - Primary use case (what problem does the app solve)
   - Target user demographics
   - Competitive category
2. Generate seed keywords from:
   - App features and benefits
   - User language (not developer terminology)
   - App store autocomplete suggestions
3. Expand keyword list using:
   - Modifiers (free, best, simple)
   - Actions (create, track, organize)
   - Audiences (for students, for teams, for business)
4. Evaluate each keyword:
   - Search volume (estimated monthly searches)
   - Competition (number and quality of ranking apps)
   - Relevance (alignment with app function)
5. Score with Opportunity formula, then bucket into Primary / Secondary / Long-tail / Aspirational (see below)
6. Map keywords to metadata locations
7. Document keyword strategy for tracking
8. **Validation:** Keywords scored; placement mapped; no competitor brand names included; no plurals in iOS keyword field

### Keyword Evaluation Criteria

| Factor | Weight | High Score Indicators |
|--------|--------|-----------------------|
| Relevance | 35% | Describes core app function |
| Volume | 25% | 10,000+ monthly searches |
| Competition | 25% | Top 10 apps have <4.5 avg rating |
| Conversion | 15% | Transactional intent ("best X app") |

### Opportunity Score

Combine the signals into a single score per keyword to rank candidates:

```
Opportunity = (Volume × 0.4) + ((100 − Difficulty) × 0.3) + (Relevance × 0.3)
```

All three inputs on a 0–100 scale. Difficulty is inverted so lower competition raises the score. Use this to sort the keyword list before bucketing.

### Keyword Grouping (Strategic Buckets)

Group candidates into four buckets — placement and priority flow from the bucket:

| Bucket | Count | Where it lives | Notes |
|--------|-------|----------------|-------|
| **Primary** | 3–5 | Title or subtitle | Highest Opportunity Score; defines positioning |
| **Secondary** | 5–10 | Subtitle + keyword field (iOS) / short description (Android) | Good opportunity; rotate based on performance |
| **Long-tail** | 10–20 | Keyword field / full description | Lower volume, specific intent, easier to rank |
| **Aspirational** | 3–5 | Tracked only — not in metadata yet | High volume + high difficulty; long-term targets, don't sacrifice primary for these |

### Keyword Placement Priority

| Location | Search Weight |
|----------|---------------|
| App Title | Highest |
| Subtitle (iOS) | High |
| Keyword Field (iOS) | High |
| Short Description (Android) | High |
| Full Description | Medium |

### Keyword Strategy Output

When delivering a keyword research result, format as:

```
Top Keywords by Opportunity

| Keyword | Volume | Difficulty | Relevance | Opportunity | Current Rank | Bucket |
|---------|--------|------------|-----------|-------------|--------------|--------|
| ...     | 0–100  | 0–100      | 0–100     | computed    | rank or —    | Primary/Secondary/Long-tail/Aspirational |

Proposed placement:
  Title (30):     [primary keywords]
  Subtitle (30):  [secondary keywords]
  Keyword field (100): [remaining keywords, comma-separated, no spaces]

Tracking only:
  [aspirational keywords]
```

See: [references/keyword-research-guide.md](keyword-research-guide.md)

---

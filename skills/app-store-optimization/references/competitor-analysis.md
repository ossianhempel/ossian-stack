# Competitor Analysis

Read for competitor positioning and comparison. Follow the scope and safety contract in the skill entry point.

## Competitor Analysis Workflow

Analyze competitors to identify keyword gaps and positioning opportunities. Most data can be pulled via OpenASO MCP (`list_competitors`, `get_app_overview`, `list_reviews`, `list_screenshots`, rankings); fall back to manual lookup otherwise.

### Identifying Competitors

If the user doesn't already have a list, find them through:

1. **Category chart** — top apps in the same category/country
2. **Keyword overlap** — apps ranking for the same keywords (OpenASO's shared-keyword evidence)
3. **Similar apps** — Apple's "You Might Also Like" section on the listing
4. **User perception** — ask: "What would your users use if your app didn't exist?"

Aim for a **3–5 app mix**: 2 direct competitors + 1–2 aspirational (larger, more mature) + 1 emerging (rising fast). Avoid analyzing only the category leader — their playbook may not apply at your stage.

### Workflow: Analyze Competitor ASO Strategy

1. Build the competitor set using the mix above.
2. Extract competitor keywords from titles, subtitles, the first 100 words of descriptions, and OpenASO keyword rankings.
3. Build a competitor keyword matrix — which keywords each app targets, coverage % per keyword.
4. Identify keyword gaps:
   - Keywords competitors rank for that you don't
   - Keywords you rank for that competitors don't (your moat — protect)
   - Keywords where you're outranked (close the gap)
5. Analyze visual assets: icon, screenshots (count, first-3 strategy, text overlays), preview video.
6. Compare ratings and review patterns — themes, response practice.
7. Compare growth signals and monetization (see tables below).
8. Document positioning opportunities and threats.
9. **Validation:** 3+ competitors analyzed; keyword matrix complete; visual + ratings + monetization compared; gaps surfaced with volume evidence.

### Side-by-Side Comparison Tables

**Metadata**

| Element | You | Comp 1 | Comp 2 | Comp 3 |
|---------|-----|--------|--------|--------|
| Title | | | | |
| Subtitle | | | | |
| Title keywords | | | | |
| Title char usage | /30 | /30 | /30 | /30 |
| Subtitle char usage | /30 | /30 | /30 | /30 |
| Description hook (first line) | | | | |

**Keyword Gap**

| Keyword | Volume | Difficulty | Your Rank | Comp 1 | Comp 2 | Comp 3 | Priority |
|---------|--------|------------|-----------|--------|--------|--------|----------|

**Ratings & Reviews**

| Metric | You | Comp 1 | Comp 2 | Comp 3 |
|--------|-----|--------|--------|--------|
| Average rating | | | | |
| Total reviews | | | | |
| Recent trend (30d) | | | | |
| Top complaint | | | | |
| Top praise | | | | |
| Dev responds to 1–3★? | | | | |

**Growth Signals**

| Signal | You | Comp 1 | Comp 2 | Comp 3 |
|--------|-----|--------|--------|--------|
| Chart position (category) | | | | |
| Update frequency | | | | |
| In-App Events active? | | | | |
| Custom Product Pages? | | | | |
| Apple Search Ads presence? | | | | |
| Downloads / revenue (est) | | | | |

Downloads and revenue estimates are unsupported by OpenASO — label as estimates from third-party tools or omit.

**Monetization**

| Aspect | You | Comp 1 | Comp 2 | Comp 3 |
|--------|-----|--------|--------|--------|
| Price model | | | | |
| Subscription price | | | | |
| Free trial length | | | | |
| IAP count | | | | |
| Paywall timing | | | | |

### Gap Analysis Template

| Opportunity Type | Example | Action |
|------------------|---------|--------|
| Keyword gap | "habit tracker" — comp ranks #3, you don't rank | Add to keyword field |
| Feature gap | Competitor lacks widget | Highlight in screenshots |
| Visual gap | No videos in top 5 | Create app preview |
| Messaging gap | None mention "free" | Test free positioning |
| Review pain | Top complaint: "ads too aggressive" | Position as ad-light |

### Competitive Position Map

Plot the user vs competitors on visibility (chart position / install velocity) × ratings:

```
                    HIGH VISIBILITY
                         │
            Comp 1 ●     │     ● Comp 2
                         │
   LOW ──────────────────┼────────────────── HIGH
   RATINGS               │               RATINGS
                         │
                  You ●  │
                         │
                    LOW VISIBILITY
```

### Output Structure

1. **Executive Summary** — 2–3 paragraphs: landscape, your position, biggest opportunities.
2. **Comparison tables** — metadata / keyword gap / ratings / growth / monetization.
3. **Position map** — ASCII 2×2.
4. **Top Opportunities** — Quick Win, Keyword Gap, Creative Edge, Feature Gap, Market Gap.
5. **Threats to Monitor** — competitor moves to watch, market trends.

---

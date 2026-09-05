---
name: "app-store-optimization"
description: "Research App Store and Google Play keywords, competitors, listing performance, and ASO experiments. Use for discovery and strategy; use asc-metadata for ASC listing edits."
triggers:
  - ASO
  - app store optimization
  - app store ranking
  - app keywords
  - app metadata
  - play store optimization
  - app store listing
  - improve app rankings
  - app visibility
  - app store SEO
  - mobile app marketing
  - app conversion rate
---

# App Store Optimization (ASO)

---

Choose the platform and research question first. Use `asc-metadata` for App Store Connect listing edits; use `gplay-cli` for Play Console operations. Verify current platform limits and source claims; label estimates and avoid inventing rankings or performance data. Deliver the requested research or plan without treating it as approval to publish metadata.

## Tools and References

### References

| Document | Content |
|----------|---------|
| [platform-requirements.md](references/platform-requirements.md) | iOS and Android metadata specs, visual asset requirements |
| [aso-best-practices.md](references/aso-best-practices.md) | Optimization strategies, rating management, launch tactics |
| [keyword-research-guide.md](references/keyword-research-guide.md) | Research methodology, evaluation framework, tracking |

---

## Platform Notes

| Platform / Constraint | Behavior / Impact |
|-----------------------|-------------------|
| iOS keyword changes | Require app submission |
| iOS promotional text | Editable without an app update |
| Android metadata changes | Index in 1-2 hours |
| Android keyword field | None — use description instead (see Google Play Specifics) |
| Android ratings | Continuous, never reset per version |
| Android A/B testing | Play Store Experiments, up to 3 variants, 7-day min |
| Keyword volume data | Estimates only; no official source |
| Competitor data | Public listings only |

**When not to use this skill:** web apps (use web SEO), enterprise/internal apps, TestFlight-only betas, or paid advertising strategy.

---

## Proactive Triggers

- **No keyword optimization in title** → App title is the #1 ranking factor. Include top keyword.
- **Screenshots don't show value** → Screenshots should tell a story, not show UI.
- **No ratings strategy** → Below 4.0 stars kills conversion. Implement in-app rating prompts.
- **Description keyword-stuffed** → Natural language with keywords beats keyword stuffing.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "ASO audit" | Full app store listing audit with prioritized fixes |
| "Keyword research" | Keyword list with search volume and difficulty scores |
| "Optimize my listing" | Rewritten title, subtitle, description, keyword field |

## Communication

All output passes quality verification:
- Self-verify: source attribution, assumption audit, confidence scoring
- Output format: Bottom Line → What (with confidence) → Why → How to Act
- Results only. Every finding tagged: 🟢 verified, 🟡 medium, 🔴 assumed.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Keyword research](references/keyword-research.md): keyword discovery, scoring, and prioritization.
- [Metadata optimization](references/metadata-optimization.md): listing strategy and concrete metadata examples.
- [Competitor analysis](references/competitor-analysis.md): competitor positioning and comparison.
- [Launch planning](references/launch-planning.md): pre-launch and launch planning.
- [Experiments](references/experiments.md): a listing experiment and success criteria.
- [Google play](references/google-play.md): Android-specific listing research and examples.

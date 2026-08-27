# grill-me

Vendored from [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/productivity/grilling`).

Upstream splits a thin `grill-me` router and a `grilling` body skill. This install merges both into one skill so `/grill-me` works without a second dependency.

Pairs with compound-engineering's `ce-brainstorm` (shape the WHAT) and `ce-plan` (implementation plan after grilling).

To update:

```bash
npx skills add mattpocock/skills -y --skill grilling
cp .agents/skills/grilling/SKILL.md /tmp/grilling-upstream.md
# Merge grilling body into skills/grill-me/SKILL.md (keep name grill-me, disable-model-invocation)
```

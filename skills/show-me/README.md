# show-me

Vendored from [humanlayer/skills](https://github.com/humanlayer/skills)
(`plugins/show-me/skills/show-me`). SKILL.md is upstream verbatim; the skill is a
visual presentation lens, called in by `how`, `teach`, and `commit-push-pr` rather
than routing out to anything.

Refresh with:

```bash
npx skills add humanlayer/skills -y --skill show-me && cp -R .agents/skills/show-me/* skills/show-me/ && trash .agents/skills/show-me
```

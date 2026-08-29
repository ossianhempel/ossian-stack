# how

Vendored from [cursor/plugins](https://github.com/cursor/plugins) (`pstack/skills/how`).

Explains how a subsystem works: runtime flow, architecture, placement and
ownership questions. Fans out parallel explorers over slices of the code, then an
explainer weaves the findings into one walkthrough. Can also critique the
architecture it just mapped. Companion to `why`, which covers motivation.

To update:

```bash
npx skills add cursor/plugins -y --skill how
cp -R .agents/skills/how/. skills/how/
```

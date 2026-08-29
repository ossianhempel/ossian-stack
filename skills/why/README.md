# why

Vendored from [cursor/plugins](https://github.com/cursor/plugins) (`pstack/skills/why`).

Investigates why code is shaped the way it is: design rationale, rejected
alternatives, the constraints behind a threshold. Enumerates available MCPs at run
time, maps them to seven evidence categories (source control, issue tracker,
long-form docs, team chat, observability, error tracking, product analytics), and
queries all of them in parallel before synthesizing with explicit confidence
calibration. Companion to `how`, which covers runtime behavior.

To update:

```bash
npx skills add cursor/plugins -y --skill why
cp -R .agents/skills/why/. skills/why/
```

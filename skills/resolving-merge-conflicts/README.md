# resolving-merge-conflicts

Vendored verbatim from [mattpocock/skills](https://github.com/mattpocock/skills)
(`skills/engineering/resolving-merge-conflicts`).

Five steps for an in-progress merge or rebase: read the current state, find the
primary sources behind each conflicting change, resolve every hunk preserving
both intents where possible, run the project's checks, then finish the
merge/rebase.

Its sharp edges are the two prohibitions: never invent new behaviour while
resolving, and never `--abort`. Both are the failure modes an agent reaches for
when a conflict gets hard.

`agents/openai.yaml` is Codex display metadata and ships as-is.

To update:

```bash
npx skills add mattpocock/skills -y --skill resolving-merge-conflicts
cp -R .agents/skills/resolving-merge-conflicts/. skills/resolving-merge-conflicts/
```

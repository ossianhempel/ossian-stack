# diagnosing-bugs

Vendored verbatim from [mattpocock/skills](https://github.com/mattpocock/skills)
(`skills/engineering/diagnosing-bugs`), including `agents/openai.yaml` and
`scripts/hitl-loop.template.sh`.

Six phases for a hard bug. Its thesis is phase 1: **build a tight, red-capable
feedback loop before forming any theory**. Ten ranked ways to construct one, a
completion criterion (one command, already run, deterministic, seconds not
minutes, agent-runnable), and an explicit stop — "if you catch yourself reading
code to build a theory before this command exists, stop."

Pairs with `bug-fix`, which owns running the task around this loop.

## Caveats

- Upstream referenced the HITL template by bare relative path, which does not
  resolve from the user's working directory. Now anchored through `SKILL_DIR`
  with an explicit copy-then-edit step.
- Upstream read a domain-model document under its own filename convention. This
  copy reads `GLOSSARY.md`, which is this plugin's convention.

To update:

```bash
npx skills add mattpocock/skills -y --skill diagnosing-bugs
cp -R .agents/skills/diagnosing-bugs/. skills/diagnosing-bugs/
```

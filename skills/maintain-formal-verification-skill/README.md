# maintain-formal-verification-skill

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/maintain-formal-verification-skill`).

The upkeep pass for a formal verify skill: read every commit that touched covered
code since the recorded sync commit, update the model or harness from the code (not
from what makes it pass), rerun, and say for each check whether it is `in sync`,
`updated`, `bug`, or `blocked`. A pass on a stale model is the dangerous case, so
every updated check is shown failing on a deliberate break before it is trusted.

Paired with `create-formal-verification-skill`.

## What changed

- Looks for the target under `.agents/skills/verify-*-formal/` first; copies under
  `.claude/skills/` or `.cursor/skills/` are drift to report.
- Treats a verify skill that hands raw model-checker traces to the user as drift,
  since this plugin does not ship pstack's `/statechart`.
- `agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
  policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill maintain-formal-verification-skill
# hand-merge this adapted copy; never overwrite it
```

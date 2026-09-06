# create-verification-skill

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/create-verification-skill`).

Generates a project-local verification skill: launch the real app, health-check
it, drive a feature the way a user would, capture evidence, tear down. It also
creates a feature map so later runs know what else needs proving. It runs its own
output end to end once before handoff because an unexecuted generated skill is
still a draft.

Paired with `maintain-verification-skill`, which keeps the map honest as the app
changes.

## What changed

Upstream hardcodes `.cursor/skills/verify-<app>/`. A new step 0 resolves the
project's own skills directory instead: first existing of `.agents/skills/`,
`.claude/skills/`, `.cursor/skills/`; otherwise it creates `.agents/skills/` and
symlinks `.claude/skills` to it when Claude Code support is needed.

`agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill create-verification-skill
# hand-merge this adapted copy; never overwrite it
```

# maintain-verification-skill

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/maintain-verification-skill`).

The upkeep pass for a verification skill: one read-only subagent per feature file
reading source concurrently, then one live pass where the coordinator drives every
feature itself, then at most one PR of proven corrections. It always names the
outcome: `clean`, `changed`, or `blocked`.

Its sharpest rule is the edit scope: never touch product code during a run. A
behavior the map describes that the app no longer does is either doc drift to fix
in the map or a product regression to report.

Paired with `create-verification-skill`, which generates the skill this one
maintains.

## What changed

Target discovery resolves the skills directory the project uses instead of
assuming `.cursor/skills/verify-*/`. The local workflow also preserves inherited
edit boundaries, supports sequential source review when subagents are unavailable,
and tightens live evidence, retry, cleanup, and unreachable-path requirements.

`agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill maintain-verification-skill
# hand-merge this adapted copy; never overwrite it
```

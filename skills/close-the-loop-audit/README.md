# close-the-loop-audit

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/maintain-verification-skill`).

The upkeep pass for a verification skill: one read-only subagent per feature file
reading source concurrently, then one live pass where the coordinator drives every
feature itself, then at most one PR of proven corrections. Outcome is always named
— `clean`, `changed`, or `blocked`.

Its sharpest rule is the edit scope: never touch product code during a run. A
behavior the map describes that the app no longer does is either doc drift (fix
the map) or a product regression (report it) — never something to paper over in
docs.

Paired with `close-the-loop`, which generates the skill this one maintains.

## What changed

Renamed from `maintain-verification-skill` to match `close-the-loop`; see that
skill's README for the reasoning. Target discovery no longer assumes
`.cursor/skills/verify-*/` — it looks under whichever skills directory the repo
actually uses. Cross-references now point at `/close-the-loop`.

`agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill maintain-verification-skill
# hand-merge; this copy is renamed and adapted, never overwrite
```

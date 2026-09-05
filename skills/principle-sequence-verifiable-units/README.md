# principle-sequence-verifiable-units

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/principle-sequence-verifiable-units`).

Break migrations, sweeps, repeated edits, commits, and PRs into units that each
end in a checked state. Verify one unit before advancing, and order delivery so
a reviewer can understand and verify each state independently.

## What changed

The upstream requirement to rebase onto clean trunk before every sequence is
expressed through the project's own branching conventions. Ossian Stack also
supports direct work on trunk, where an unconditional rebase would be wrong.

`agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill principle-sequence-verifiable-units
# hand-merge the branching adaptation; never overwrite
```

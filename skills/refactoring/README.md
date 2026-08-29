# refactoring

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/poteto-mode/playbooks/refactoring.md`), extracted from the
`poteto-mode` skill as a standalone skill.

Structural change that holds behavior fixed: pin the contract first, name the
target shape, subtract, move in green steps, prove equivalence, commit in slices.

## What changed from upstream

The playbook cites twelve sibling skills that this plugin does not ship
(`figure-it-out`, `architect`, `principle-prove-it-works`,
`principle-model-the-domain`, `principle-foundational-thinking`,
`principle-redesign-from-first-principles`,
`principle-migrate-callers-then-delete-legacy-apis`,
`principle-minimize-reader-load`, `sequence-verifiable-units`,
`principle-subtract-before-you-add`, `principle-laziness-protocol`, and an
`Opening a PR` playbook). Each citation was replaced with the principle it stood
for, stated inline, so nothing routes to a skill that does not exist.

Kept: the `how` skill reference, which this plugin does ship.

Also dropped: a hardcoded default refactoring model, since model availability is
not something a skill should assume.

Boundary with the sibling skills here — `simplify-code` makes settled code
readable without moving it; this skill moves modules, APIs, and call graphs.

To update:

```bash
npx skills add cursor/plugins -y --skill poteto-mode
# then hand-merge playbooks/refactoring.md from .agents/skills/poteto-mode/
# this copy is adapted, do not overwrite
```

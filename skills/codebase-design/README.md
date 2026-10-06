# Codebase Design

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design).
The pinned upstream revision is recorded in `skills/sources.json`.

Refresh from the plugin source checkout:

```sh
npx skills add mattpocock/skills -y --skill codebase-design && echo 'Hand-merge .agents/skills/codebase-design/ into skills/codebase-design/; preserve local ownership, routing, terminology, proportional exploration, and test-coverage safeguards, then: trash .agents/skills/codebase-design'
```

Hand-merge the scratch copy in `.agents/skills/codebase-design/` into this
directory, then `trash .agents/skills/codebase-design` and run
`scripts/check-upstream.sh --record codebase-design`.

Preserve the local ownership split, reuse of existing design work, project
terminology, proportional exploration, dependency semantics, and evidence required
before removing tests. Architect and Refactoring load the skill when module
design requires judgment. It supplies criteria without starting another workflow.

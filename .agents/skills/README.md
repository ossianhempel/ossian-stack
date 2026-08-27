# Internal skills

Skills that help you *work on this repo* but must not ship in the plugin.

`.agents/skills/` is the source of truth. `.claude/skills` is a **symlink** to it,
so Claude Code, Codex, and Cursor all load the same directory from one copy — add a
skill once and every runtime that opens this repo sees it.

| Tier | Loaded when | Ships | `sources.json` entry | Version bump |
| --- | --- | --- | --- | --- |
| `skills/<name>/` | wherever the plugin is installed | yes | required | yes |
| `.agents/skills/<name>/` | cwd is this repo | no | no | no |

Same layout either way: one directory per skill, `SKILL.md` as the entry point,
kebab-case name matching the directory. `bun run validate` checks both tiers and
fails if a name exists in both.

Good candidates for this tier: maintenance work on the skill collection itself —
vendoring, drift triage, manifest bumps, changelog hygiene, install auditing. Work
that is meaningless outside this checkout.

To promote one to the plugin: `git mv` it into `skills/`, add a `sources.json` entry
with `"origin": "local"`, add its name to the README group table and bump the counts,
and bump the three manifests.

## Careful: this is also the vendoring scratch path

`npx skills add …` writes its download to `.agents/skills/<name>/`. That is why every
refresh command in `skills/sources.json` ends by copying the download into `skills/`
and trashing the scratch copy. A leftover directory here shows up as untracked in
`git status` — trash it; do not commit it.

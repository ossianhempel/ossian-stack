# babysit

Vendored from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/poteto-mode/playbooks/babysit.md`), extracted from the
`poteto-mode` skill as a standalone skill and adapted.

Drives a PR or a stacked chain to merge-ready: declares a mode, works the lowest
unmerged PR, classifies CI failures before retriggering, triages review-bot
comments skeptically, and stops where the human's call begins.

## What changed from upstream

| Upstream | Here |
| --- | --- |
| A playbook inside `poteto-mode` | A standalone skill with its own frontmatter |
| `../references/bugbot-triage.md` | `references/bugbot-triage.md`, vendored alongside |
| `scripts/watch-pr/watch-pr` in the parent skill | Vendored into this skill, invoked through an anchored `SKILL_DIR` path |
| Routes to `playbooks/shipping.md` (3×) | Stops at merge-ready and hands the merge decision back |
| `/loop` in dynamic mode | Described as a capability, since `/loop` is Claude Code only |

## Runtime dependency

`scripts/watch-pr` is Bun-only TypeScript. On first run it executes
`bun install --frozen-lockfile` into `scripts/node_modules/`, then restarts
itself. Two consequences worth knowing:

- **It needs `bun` on the user's PATH.** Every other executable this plugin
  ships is Python. The skill degrades to reporting status through the project's
  own GitHub interface when `bun` is absent.
- **It installs into wherever the skill is installed.** For a plugin install
  that is the versioned cache directory, which is replaced on every update, so
  the install repeats after each one.

It also assumes `gh`, and Graphite (`gt`) for stack topology.

To update:

```bash
npx skills add cursor/plugins -y --skill poteto-mode
# then hand-merge playbooks/babysit.md, references/bugbot-triage.md, and scripts/
# from .agents/skills/poteto-mode/ — this copy is adapted, do not overwrite
```

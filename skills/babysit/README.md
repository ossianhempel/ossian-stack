# babysit

Vendored from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/poteto-mode/playbooks/babysit.md`), extracted from the
`poteto-mode` skill as a standalone skill and adapted.

Drives GitHub/GHE and Azure DevOps Services PRs to merge-ready: declares a mode, works the lowest
unmerged PR, routes all review feedback through `resolve-pr-feedback` in pipeline
mode before CI work, and stops at merge-ready or a human blocker. Mode follows the
requested outcome regardless of PR size; status checks stay read-only. Default
`commit-push-pr` follow-through starts the drive once the agreed build phase is
complete, or resumes its existing owner. Babysitting never merges.

## What changed from upstream

| Upstream | Here |
| --- | --- |
| A playbook inside `poteto-mode` | A standalone skill with its own frontmatter |
| Bugbot-specific fixer pipeline | `resolve-pr-feedback` owns all feedback; `references/bugbot-triage.md` retains historical context |
| `scripts/watch-pr/watch-pr` in the parent skill | Vendored into this skill, invoked through an anchored `SKILL_DIR` path |
| Routes to `playbooks/shipping.md` (3×) | Stops at merge-ready and hands the merge decision back |
| Small/docs-only PRs forced to check | Requested outcome selects the mode; drive remains drive |
| `/loop` in dynamic mode | Described as a capability, since `/loop` is Claude Code only |

## Azure DevOps Services

`references/azure-devops.md` routes the existing modes through a Python 3 REST
watcher. It checks current refs/merge/iteration, policy coverage and freshness,
required reviewers, live discussions, and the owning validation build. The feedback
resolver owns Azure discussion replies and resolution. GitHub's Bun watcher is
unchanged because its types and readiness rules are provider-specific.

Azure support is scoped to same-repository Services PRs and one verified frontier
at a time. Automated Azure queues, fork mutation, and Server/custom hosts are not
supported. Missing build/policy binding blocks READY. Authentication uses an
existing az Entra session or supplied AZURE_DEVOPS_EXT_PAT, not stored CLI PATs.
The two skills carry identical client.py primitives to remain self-contained; keep
both copies aligned. No live Azure verification is claimed by the offline fixtures.

Focused offline checks:

```bash
python3 -m unittest discover -s skills/babysit/scripts/azure -p 'test_*.py'
python3 -m unittest discover -s skills/resolve-pr-feedback/scripts/azure -p 'test_*.py'
bun test skills/babysit/scripts/watch-pr
```

## GitHub runtime dependency

`scripts/watch-pr` is Bun-only TypeScript. On first run it executes
`bun install --frozen-lockfile` into `scripts/node_modules/`, then restarts
itself. Two consequences worth knowing:

- **It needs `bun` on the user's PATH.** Every other executable this plugin
  ships is Python. The skill degrades to reporting status through the project's
  own GitHub interface when `bun` is absent.
- **It installs into wherever the skill is installed.** For a plugin install
  that is the versioned cache directory, which is replaced on every update, so
  the install repeats after each one.

It also needs `gh`. Stack mode discovers the connected open chain directly from
GitHub by matching each pull request's base branch to another pull request's head
branch; it does not require a separate stack service or CLI.

To update:

```bash
npx skills add cursor/plugins -y --skill poteto-mode
# then hand-merge playbooks/babysit.md, references/bugbot-triage.md, and scripts/
# from .agents/skills/poteto-mode/ — this copy is adapted, do not overwrite
```

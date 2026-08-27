# Changelog

## 2026-08-27

### Added
- Initial `ossian-stack` plugin. Repackages the skill collection from
  `agent-scripts` as a Claude Code / Codex plugin that hosts its own marketplace,
  replacing the `sync-agent-scripts.sh` symlink fan-out.
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and
  `.codex-plugin/plugin.json` at version 1.0.0.
- `docs/plugin-workflow.md` — install, edit → publish loop, version-bump rules.
- 50 skills carried over verbatim from `agent-scripts/skills/`.
- `bin/docs-list` + `scripts/docs-list.ts` ship with the plugin. The resolver now
  prefers `./docs` from the current working directory (or an explicit path
  argument) over the script's own sibling `docs/`, so the copy inside the plugin
  cache indexes the repo you are working in. Missing `docs/` prints a message and
  exits 0 instead of throwing.

### Changed
- `AGENTS.md` drops the sync/audit section; adds plugin source-of-truth and
  version-bump rules, and points at `agent-scripts` as the archived predecessor.
  It is repo-local guidance only — nothing injects it into other repos, and the
  downstream pointer lines are not part of this migration.
- Skill prose that referenced `agent-scripts` paths now points at `ossian-stack`.

### Removed
- `hetzner-vm` skill is not part of this plugin. It named the VM's public address
  alongside a full inventory of the services running on it, which does not belong
  in a public repo. It remains in `agent-scripts`.

### Fixed
- `release-ios-app/references/manifest.md` — `IOS_RELEASE_CONTACT_EMAIL` corrected
  to `hemposse@hotmail.com`.

### Not carried over
- `archived-skills/`, `profiles/`, `plugins.json`, `profile-assignments.json`,
  `tools/` (skill-benchmark, agent-readiness), `test/`, `automation/`, `work/`,
  `.githooks/`, and the sync/audit scripts. These stay in `agent-scripts`.
  `bin/docs-list` and `scripts/docs-list.ts` are the exception — they ship here.

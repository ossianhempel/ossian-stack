---
summary: How to install, edit, and publish the ossian-stack plugin — the edit → publish loop and why edits are not live immediately.
read_when:
  - Installing ossian-stack on a new machine or a remote dev box.
  - Editing a skill and wondering why the runtime still sees the old version.
  - Bumping the plugin version or cutting a release.
---

# Plugin Workflow

`ossian-stack` is one plugin, hosted in this repo, which is also its own
marketplace (`.claude-plugin/marketplace.json` declares a single plugin with
`"source": "./"`).

## The one thing to internalise

**Plugins are copied, not symlinked.** On install, the runtime copies this repo
into `~/.claude/plugins/cache/ossian-stack/ossian-stack/<version>/`. Editing a
skill here does **not** change what Claude sees until you refresh the
marketplace. This is the opposite of the old `agent-scripts` symlink sync.

Verify what the runtime is actually reading:

```bash
ls -la ~/.claude/plugins/cache/ossian-stack/ossian-stack/
```

## Install

Two ways to register the marketplace. The repo is on GitHub either way — this
only decides which path *this machine* reads from.

### GitHub source — for remote dev boxes and any fresh machine

```
/plugin marketplace add ossianhempel/ossian-stack
```

Then `/plugin install ossian-stack@ossian-stack`. **This is the setup to use**,
on every machine including the one you author on. Edits require commit + push;
after that each runtime refreshes on its own, or immediately with
`/plugin marketplace update ossian-stack`.

The manifests declare **no version**, so the commit SHA is the release — there is
nothing to bump. Claude Code shows the short SHA where a version would go.

The same repo is registered natively in all three:

```
claude  plugin marketplace add ossianhempel/ossian-stack
codex   plugin marketplace add ossianhempel/ossian-stack
copilot plugin marketplace add ossianhempel/ossian-stack
```

### Directory source — avoid, including on the Mac you author on

```
/plugin marketplace add ~/Developer/ossian-stack
```

This re-copies straight off local disk, so the edit loop needs no commit or push
— and that convenience is what costs you automatic updates. Measured 2026-08-30:

| Runtime | Local directory source | Git source |
| --- | --- | --- |
| Claude Code 2.1.250 | refuses to update when the version is unchanged; no `--force` in this build | auto-updates on version change; commit SHA if `version` is omitted |
| Codex 0.151.0-alpha | `plugin marketplace upgrade` reports "No configured Git marketplaces to upgrade" | `plugin marketplace upgrade` refreshes it |
| Copilot CLI 1.0.80 | `plugin update` re-copies, but nothing refreshes on its own | auto-updates at session start in a trusted directory |

Use it only to test something you genuinely cannot push.

Use the directory source on the authoring Mac and the GitHub source everywhere
else. Same plugin name in both places.

## Edit loop

1. Edit under `skills/<name>/`.
2. Bump `version` in **all three** manifests if the change should reach other
   machines (see below). Skip the bump for a local directory-source refresh.
3. `/plugin marketplace update ossian-stack`
4. Restart the session (or start a new one) so skill descriptions reload.

## Version bumps

Three manifests carry a `version` and they must agree:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json` (inside the `plugins[0]` entry)
- `.codex-plugin/plugin.json`

Semver: PATCH for a skill fix, MINOR for a new skill, MAJOR for removing or
renaming skills (their namespaced ids change).

Check they agree:

```bash
grep -h '"version"' .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json
```

## Namespacing

Plugin skills are addressed as `ossian-stack:<skill-name>` — e.g.
`ossian-stack:asc-release`. Bare `<skill-name>` still works when nothing else
claims it, but the namespaced form is unambiguous and is what shows up in the
skills list.

## Codex

`.codex-plugin/plugin.json` mirrors the Claude manifest and points at the same
`skills/` tree.

```
codex plugin marketplace add ossianhempel/ossian-stack
```

Then enable it in `~/.codex/config.toml`:

```toml
[plugins."ossian-stack@ossian-stack"]
enabled = true
```

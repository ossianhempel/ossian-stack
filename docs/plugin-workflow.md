---
summary: How to install, edit, and publish the ossian-stack plugin — the edit → publish loop and why edits are not live immediately.
read_when:
  - Installing ossian-stack on a new machine or a remote dev box.
  - Editing a skill and wondering why the runtime still sees the old version.
  - Publishing a plugin change or cutting a release.
---

# Plugin Workflow

`ossian-stack` is one plugin, hosted in this repo, which is also its own
Claude Code marketplace (`.claude-plugin/marketplace.json` declares a single
plugin with `"source": "./"`) and Cursor Git marketplace
(`.cursor-plugin/marketplace.json` declares the root plugin with `"source": "."`).
The native plugin manifests point at the same `skills/` tree.

## The one thing to internalise

**Plugins are copied, not symlinked.** On install, the runtime copies the plugin
into its own cache. Editing a skill here does **not** change what an installed
runtime sees until that runtime refreshes the plugin. This is the opposite of
the old `agent-scripts` symlink sync.

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

The native manifests declare **no version**, so the commit SHA is the release —
there is nothing to bump. Cursor's plugin version field is optional.

The same repo exposes native plugin manifests to all three supported hosts:

```
claude plugin marketplace add ossianhempel/ossian-stack
codex  plugin marketplace add ossianhempel/ossian-stack
cursor-agent plugin marketplace add https://github.com/ossianhempel/ossian-stack
```

In Cursor, finish the install from the plugin UI at user scope:

```
/plugin
```

The `.cursor-plugin/marketplace.json` catalog lets Cursor index this Git repository;
`.cursor-plugin/plugin.json` describes the plugin itself. Refresh the catalog with
`cursor-agent plugin marketplace update ossian-stack`. Cursor's official public
Marketplace and Team Marketplaces are separate channels. Do not use
`/add-plugin https://github.com/ossianhempel/ossian-stack` for the normal install:
that direct GitHub import is currently pinned.

When a user gives an agent this repository URL and asks it to install the plugin or
skills, the agent should detect the harness and use the native plugin route first.
For Gemini CLI, Windsurf, and Antigravity, which do not use this repo's native
plugin manifests, install only the public `skills/` tree through the shared skills
installer and target the current harness's global skill scope. Never install the
checkout-local `.agents/skills/` tree.

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

Use it only to test something you genuinely cannot push.

Use the directory source only for Claude Code or Codex testing. Cursor local
testing uses `~/.cursor/plugins/local/ossian-stack`; use a pushed GitHub source
for the normal Cursor install.

## Edit loop

1. Edit under `skills/<name>/`.
2. Commit and push the change. The commit is the release identifier; this repo's
   native manifests intentionally omit `version`.
3. Refresh the marketplace or plugin in the target runtime.
4. Restart the session (or start a new one) so skill descriptions reload.

## Versioning

This repo intentionally ships without a `version` field in its native manifests:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json` (inside the `plugins[0]` entry)
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.cursor-plugin/marketplace.json` (inside the `plugins[0]` entry)

The git commit is the release. Do not add a version to one manifest: `bun run
validate` checks that the five native manifest files remain versionless.

```bash
bun run validate
```

## Namespacing

Claude Code and Codex address plugin skills as `ossian-stack:<skill-name>` — e.g.
`ossian-stack:asc-release`. Cursor exposes the same skills by their individual
skill names, such as `/asc-release`, and can also auto-invoke them from their
trigger descriptions.

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

## Cursor

`.cursor-plugin/plugin.json` points at the same `skills/` tree. Cursor discovers
the skills from that manifest and keeps the installed copy under its plugin
storage. Register the repository as a Git marketplace before installing:

```
cursor-agent plugin marketplace add https://github.com/ossianhempel/ossian-stack
```

For a local test install, copy the checkout into
`~/.cursor/plugins/local/ossian-stack`, reload Cursor, and confirm the plugin in
Customize → Plugins. For a normal install, open `/plugin`, select the repository's
`ossian-stack` marketplace entry, and choose User scope. Refresh it later with
`cursor-agent plugin marketplace update ossian-stack`.

---
summary: Canonical list of agent runtimes this repo targets — their skill install roots and which keep usable session transcripts.
read_when:
  - Adding a new agent runtime to the plugin manifests or to an auditing skill.
  - Making a skill or script "work across all the agents we support".
  - Discovering session logs or scanning skill roots from a tool.
---

# Supported Agents

Canonical list of the agent runtimes this repo targets. `ossian-stack` reaches
Claude Code, Codex, Cursor, and Copilot through their plugin systems; the other
runtimes read one of the global skill roots below. Any skill that scans skill
installs or agent session logs (`skill-cleaner`, `agent-transcript`) should align
with this table.

## Native plugin manifests

| Runtime | Manifest |
| --- | --- |
| Claude Code | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` |
| Codex | `.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` and `.cursor-plugin/marketplace.json` |
| Copilot | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (Copilot checks `.claude-plugin/` in its manifest search order) |

## Installation routing

When an agent receives this repository URL with a request to install the plugin or
its skills, it should detect the current harness and use this order:

| Runtime | Primary route | Update path |
| --- | --- | --- |
| Claude Code | Git marketplace, then `ossian-stack@ossian-stack` | Claude marketplace update |
| Codex | Git marketplace, then `ossian-stack@ossian-stack` | auto-upgrades the Git marketplace at plugin startup and `plugin/list`; `codex plugin marketplace upgrade` forces a refresh |
| Cursor | Git marketplace, then `ossian-stack` at User scope | `cursor-agent plugin marketplace update ossian-stack` |
| Copilot CLI / app | Git marketplace, then `ossian-stack@ossian-stack`; opt in via `autoUpdate: true` on the marketplace's `extraKnownMarketplaces` entry in `~/.copilot/settings.json`. A repo can also enable it declaratively via `.github/copilot/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`) — the only route for the Copilot cloud agent | auto-updates at session start once opted in; otherwise `copilot plugin update ossian-stack` |
| OpenCode | Shared skills installer, global opencode scope (`~/.config/opencode/skills`) | `npx skills update` |
| Gemini CLI | Shared skills installer, global Gemini scope | `npx skills update` |
| Windsurf | Shared skills installer, global Windsurf scope | `npx skills update` |
| Antigravity CLI | Shared skills installer, global Antigravity scope | `npx skills update` |

Cursor's `/add-plugin <repo-url>` direct GitHub import is not the Git marketplace
route and is currently pinned. The public Cursor Marketplace and Team Marketplaces
are separate channels. For skill-only runtimes, install the directories under
`skills/`, never the checkout-local `.agents/skills/` directory.

## Skill install roots

The repo's `skills/` is the single source of truth. Claude Code, Codex, and Cursor
get it as a plugin — each runtime manages its own installed copy:

| Runtime | Installed copy |
| --- | --- |
| Claude Code | `~/.claude/plugins/cache/ossian-stack/ossian-stack/<version>/skills` |
| Codex | `~/.codex/plugins/cache/…` |
| Cursor | Cursor-managed plugin copy (local testing: `~/.cursor/plugins/local/ossian-stack`) |
| Copilot | `~/.copilot/installed-plugins/ossian-stack/ossian-stack` (marketplace-managed) |

These are direct skill roots outside the native plugin installs. They are listed
because auditing skills scan them, not because this repo installs into them:

| Agent | Skill root | Notes |
| --- | --- | --- |
| Claude Code | `~/.claude/skills` | Claude Code only |
| Codex | `~/.agents/skills` (also reads `~/.codex/skills`) | cross-tool standard |
| Gemini CLI | `~/.agents/skills` | cross-tool standard |
| Cursor | `~/.agents/skills` | standalone skills; native plugin support is listed above |
| OpenCode | `~/.config/opencode/skills` (also reads `~/.claude/skills` and `~/.agents/skills` globally) | the cross-tool roots are listed for completeness; native plugin installs of other runtimes live in versioned caches those roots never see, so OpenCode needs its own `npx skills add` copy |
| Copilot CLI / app | `~/.copilot/skills` (legacy skills-installer copies), `~/.agents/skills` (cross-tool) | plugin installs are marketplace-managed; this root only holds leftovers from the old `npx skills add` route |
| Windsurf | `~/.agents/skills` | cross-tool standard |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills` | separate root |

Repo source of truth: `~/Developer/ossian-stack/skills` (this machine) or
`~/repos/ossian-stack/skills` (varies by machine — see AGENTS.md).

Per-project scoping of the *plugin* is done by enabling or disabling it in a
project's `.claude/settings.json`.

Runtimes also read a **project** skill tier relative to the cwd: Claude Code reads
`.claude/skills/`, while Codex and Cursor read `.agents/skills/`. This repo keeps its
internal maintenance skills in `.agents/skills/` and symlinks `.claude/skills` to it,
so one copy serves every runtime that opens the checkout (see
`.agents/skills/README.md`). Those skills reach no one outside this repo — anything
users need belongs in `skills/`.

## Session / transcript logs

Where each runtime keeps conversation logs, and whether they can produce a usable
agent transcript (assistant decisions + tool summaries, not just user prompts):

| Agent | Log location | Format | Transcript-capable |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/projects/**/*.jsonl` | JSONL, full turns | ✅ yes |
| Codex | `~/.codex/sessions/**/*.jsonl` | JSONL, full turns | ✅ yes |
| Gemini CLI | `~/.gemini/tmp/<hash>/logs.json` | JSON array, **user prompts only** | ❌ no assistant content |
| Antigravity CLI | `~/.gemini/antigravity-cli/conversations/*.pb` | binary protobuf | ❌ not plain text |
| Antigravity CLI | `~/.gemini/antigravity-cli/history.jsonl` | JSONL, prompt display only | ❌ no assistant content |
| Cursor | `~/.cursor/projects/...` | opaque/internal | ❌ |
| Copilot CLI | `~/.copilot/session-store.db` | SQLite | ❌ not plain text |
| Windsurf | n/a | — | ❌ |

**Practical consequence:** the `agent-transcript` and `session-viewer` skills can only
render Claude Code and Codex sessions. The other supported runtimes either log only
user prompts or store conversations in binary/SQLite formats that carry no sanitizable
assistant transcript. When a new runtime gains a plain-text full-turn log, add it here
and wire it into those skills.

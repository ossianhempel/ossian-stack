# ossian-stack

Ossian's personal agent skills, packaged as one plugin for Claude Code, Codex, and Cursor.

![skills](https://img.shields.io/badge/skills-55-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![runtimes](https://img.shields.io/badge/runtimes-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-8957e5)

## Install

If a user gives an agent this repository URL and says “install the plugin” or
“install the skills”, detect the current harness and follow this routing. Prefer
the native plugin path whenever the harness supports one. Do not silently install
only the `skills/` directory when a native plugin path is available.

**Claude Code** — register the GitHub marketplace, then install the plugin:

```
/plugin marketplace add ossianhempel/ossian-stack
/plugin install ossian-stack@ossian-stack
```

**Codex** — register the Git marketplace, then install the named plugin:

```
codex plugin marketplace add ossianhempel/ossian-stack
codex plugin add ossian-stack@ossian-stack
```

**Cursor** — register this repository as a native Git marketplace:

```
cursor-agent plugin marketplace add https://github.com/ossianhempel/ossian-stack
```

Then open Cursor's `/plugin` Marketplace UI (or Customize → Plugins), choose
`ossian-stack`, and install it at **User** scope. The current Cursor CLI can add and
refresh the marketplace, but does not provide a non-interactive plugin-install
subcommand:

```
cursor-agent plugin marketplace update ossian-stack
```

Do not substitute `/add-plugin https://github.com/ossianhempel/ossian-stack` for the
marketplace flow: direct GitHub imports are pinned. Cursor's public Marketplace and
Team Marketplaces are separate distribution channels.

For Gemini CLI, Copilot, Windsurf, and Antigravity, there is no native plugin
manifest in this repository. Install the public `skills/` tree with the shared
skills installer, targeting the current harness and global scope:

```
npx skills add https://github.com/ossianhempel/ossian-stack \
  --global --agent <current-harness> --skill '*' --yes
```

Use `npx skills update` for later skill refreshes. Do not install `.agents/skills/`;
that directory is checkout-local maintenance content. If the shared installer does
not know the current harness, follow that harness's documented global skill root
and install only the directories under `skills/`.

For local Cursor testing, copy the repository to
`~/.cursor/plugins/local/ossian-stack`, reload Cursor, and open Customize → Plugins.
Local copies are development installs and do not update from GitHub.

Claude Code and Codex address skills as `ossian-stack:<name>` — or you can just
describe the task in plain language. Cursor exposes the same skills by their
individual names and trigger descriptions.

**Authoring machine.** Register the GitHub repo here too, rather than the local
clone — a local-directory marketplace is what disables automatic updates. The
trade is that pushing is what publishes: an unpushed edit reaches no runtime.

## Philosophy

One repo, one install, every runtime. These skills previously lived in a private
repo that fanned them out to each runtime's skill directory by symlink — a
`sync-agent-scripts.sh` that had to be re-run on every machine after every edit.
The plugin model replaces that: the runtime owns install, update, versioning, and
removal, and `skills/` here is the single source of truth.

Skills are collected, not invented. Roughly half are vendored from other people's
repos, and `skills/sources.json` records where each one came from and which
upstream commit it is pinned to — so a borrowed skill can be traced, diffed, and
refreshed instead of quietly rotting.

## Skills at a glance

55 skills, grouped by what they are for.

| Group | Covers | Skills |
| --- | --- | --- |
| **Ship an app** | App Store Connect, iOS releases, store metadata, legal | `asc-metadata` · `asc-pricing` · `asc-release` · `asc-version-guard` · `ios-marketing-capture` · `release-ios-app` · `privacy-policy` |
| **Design & frontend** | Accessibility, UI craft and motion, decks, onboarding, throwaway prototypes | `better-accessibility` · `emil-design-eng` · `grill-design` · `frontend-slides` · `onboarding-flow` · `prototype` |
| **Words** | Marketing copy, editorial, slop removal | `copywriter` · `online-writing` · `unslop` |
| **Backend & infra** | Convex, Clerk, RevenueCat, secrets, Post Queue | `convex-cli` · `clerk-cli` · `revenuecat-api` · `one-password` · `post-queue-cli` |
| **Agent workflow** | Review, routing, simplification, refactoring, debugging, verification, conventions enforcement, issue triage and ticketing, PR babysitting, git hygiene, install and skill maintenance | `autoreview` · `babysit` · `continual-learning` · `codify-conventions` · `setup-ossian-stack` · `diagnosing-bugs` · `domain-modeling` · `close-the-loop` · `close-the-loop-audit` · `codex-first` · `git-cleanup` · `grill-me` · `handoff` · `refactoring` · `resolving-merge-conflicts` · `resolve-pr-feedback` · `simplify-code` · `triage` · `to-spec` · `to-tickets` · `bro` · `skill-creator` |
| **Principles** | Short, explicitly-invoked rules for how to work — verification, design exploration, debugging posture, domain modeling | `principle-encode-lessons-in-structure` · `principle-exhaust-the-design-space` · `principle-fix-root-causes` · `principle-model-the-domain` · `principle-prove-it-works` · `principle-redesign-from-first-principles` · `principle-subtract-before-you-add` |
| **Understand code** | Codebase walkthroughs, design rationale, explaining a change | `how` · `why` · `teach` |
| **Personal tooling** | Notes and tasks | `obsidian` · `things` |

Each skill's own `SKILL.md` frontmatter carries its full description and trigger
conditions — that is the one place a description is maintained.

## Repo layout

| Path | What |
| --- | --- |
| `skills/` | **The plugin.** One directory per skill, `SKILL.md` entry point |
| `skills/sources.json` | Upstream origin, pinned rev, and refresh command for every skill |
| `hooks/` | `hooks.json` + scripts; Claude Code, Codex, and Cursor read this format |
| `commands/` | Slash commands (currently empty) |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest |
| `.claude-plugin/marketplace.json` | Marketplace manifest (this repo hosts itself) |
| `.codex-plugin/plugin.json` | Codex plugin manifest, same `skills/` tree |
| `.cursor-plugin/plugin.json` | Cursor plugin manifest, same `skills/` tree |
| `.cursor-plugin/marketplace.json` | Cursor Git marketplace catalog |
| `bin/docs-list` | Docs indexer — lists `./docs` for whatever repo you run it in |
| `.agents/skills/` | Internal skills — loaded only in this checkout, never shipped |
| `.claude/skills` | Symlink to `.agents/skills` so Claude Code sees the same tier |
| `scripts/` | Repo-local dev tooling, not plugin surface |
| `docs/` | Repo docs — run `bun run docs:list` |
| `AGENTS.md` | Agent instructions for this repo (`CLAUDE.md` symlinks to it) |

## Working on it

```bash
bun run check            # validate + plugin:validate
bun run validate         # manifest/skill/sources/README consistency
bun run plugin:validate  # Claude's own schema check (needs `claude` on PATH)
bun run check:upstream   # which vendored skills have moved upstream
bun run docs:list        # index docs/
```

Bun is a dev-time task runner only — the plugin itself ships no code that needs it.

The edit → publish loop, and why an edit is not live until the marketplace is
refreshed, is in [`docs/plugin-workflow.md`](docs/plugin-workflow.md).

## Conventions

- Skills go in `skills/<name>/` with a `SKILL.md`. Kebab-case names, frontmatter
  `name` matching the directory.
- Every skill needs a `skills/sources.json` entry; vendored ones also get a
  `README.md` carrying the refresh one-liner.
- The native manifests intentionally omit `version`; the git commit is the release
  identifier, and Cursor treats its manifest version as optional.
- Skills are self-contained: never reference a file outside the skill's own directory.
- Skills that only make sense while working *on this repo* go in `.agents/skills/`,
  not `skills/`. They ship with nothing and need no `sources.json` entry.
  `.claude/skills` symlinks there, so one copy serves Claude Code, Codex, and Cursor.
- Never edit the installed copy under `~/.claude/plugins/cache/` — it is overwritten
  on every update.

## Limitations

- **Native plugin hosts.** Claude Code, Codex, and Cursor have native plugin
  manifests. Gemini CLI, Copilot, Windsurf, and Antigravity consume the shared
  skill directories instead — see [`docs/supported-agents.md`](docs/supported-agents.md).
- **Internal skills are checkout-local.** They load for any runtime that opens this
  repo and reach no one else.
- **Vendored skills are not polled.** They drift until `bun run check:upstream`
  says so and someone refreshes them.

## FAQ

**Do I need Bun to use the plugin?** No. Bun runs the repo's own checks. Installing
and using the plugin needs neither Bun nor Node.

**Where does an installed skill actually live?**
`~/.claude/plugins/cache/ossian-stack/ossian-stack/<version>/skills`. Read it, never
edit it — the next update overwrites it.

**Why is my edit not showing up?** Skills are copied into that cache, not symlinked.
Refresh the marketplace and restart the session; see `docs/plugin-workflow.md`.

## Documentation

| Doc | What |
| --- | --- |
| [`docs/plugin-workflow.md`](docs/plugin-workflow.md) | Install, edit → publish loop, version-bump rules |
| [`docs/skills-sources.md`](docs/skills-sources.md) | Upstream map, origin types, drift checking |
| [`docs/supported-agents.md`](docs/supported-agents.md) | Runtimes, skill roots, transcript support |
| [`docs/mcp-keys.md`](docs/mcp-keys.md) | MCP server keys |

## License

MIT

# Global Agent Instructions
- Start: run docs list (docs:list script, or bin/docs-list here if present; open docs before coding.
- Default web stack: TanStack Start, PGlite/SQLite → PG when needed OR Convex, single-container fullstack, deploy to Coolify. Avoid Next.js (Vercel lock-in).
 -New iOS apps from scratch: start from `ios-app-template` (`~/Developer/ios-app-template`, https://github.com/ossianhempel/ios-app-template) via `./scripts/new-app.sh "<Name>" <bundle-id>`.
- If I say "check my notes", "read what I've written about this", "research this in my notes", or similar, search the Obsidian vault first. Use web search or other sources second unless I explicitly ask for them.
- Workspace: ~/Developer or ~/repos. Missing ossianhempel repo: clone https://github.com/ossianhempel/<repo>.git. (it can differ between Developer or repos depending on machine)
- For web apps, work directly on `main` by default. Create or switch to a feature branch only when Ossian explicitly asks. For mobile apps we use `develop` as our default development branch and save `main` for releases. Feature branches (if asked for) branch from `develop`.
- I'm a single developer — no team to coordinate with.
- Guardrails: use `trash` for deletes; never `rm`.
- Secrets live in .env* files and/or 1Password (`op` CLI).

## Output style
Replies must be clear and succinct — actionable, not essay-length.
1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes, if anything is open.
4. Finish the current issue before raising a new one.
5. Restate progress on multi-step work ("step 3 of 5 done").
6. After a change, show what now works.
7. Errors: location, cause, fix. No drama.
8. No preamble, recaps, or closers ("Great question", "Hope this helps", "Let me know if…").

## Important Locations
- Personal Website repo: ~/Developer/ossianhempel_com
- Obsidian vault: /Users/ossianhempel/ossians-second-brain-sync OR /Users/ossianhempel/Developer/ossians-second-brain-sync

## Docs
- Start: run docs list; open docs before coding. In order of preference: the repo's
  own `docs:list` script, its `bin/docs-list`, or the copy this plugin ships:
  `${CLAUDE_PLUGIN_ROOT}/bin/docs-list`. The shipped copy lists `./docs` from the
  current working directory, so it works in any repo — pass a path to point it
  elsewhere. It prints a message and exits 0 when there is no `docs/`.
- Repos with Node scripts can still vendor `scripts/docs-list.ts` and expose
  `docs:list` in `package.json` for a dependency-free local entry point.
- Add read_when hints on cross-cutting docs.

### Changelog
`CHANGELOG.md` at the repo root logs meaningful changes (skills added/removed/renamed, manifest/version changes, AGENTS guidance). When you ship something another agent or future-you needs to know about, add a date-stamped section.

## This repo is a plugin
`ossian-stack` is a Claude Code / Codex **plugin**, not a sync target. There is no
`sync-agent-scripts.sh` here — the runtime installs and updates the plugin itself.

- **Source of truth:** add and edit skills in `skills/` only. Never edit the
  installed copy under `~/.claude/plugins/cache/ossian-stack/…` — it is
  overwritten on every update.
- **Skills are copied, not symlinked.** An edit in this repo is not live until the
  marketplace is refreshed. See `docs/plugin-workflow.md` for the edit → publish loop.
- **Version bumps:** any change that should reach an installed runtime needs the
  `version` field bumped in **all three** manifests
  (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.codex-plugin/plugin.json`). They must agree.
- **Upstream map:** [`skills/sources.json`](skills/sources.json) lists every skill's
  origin (local, vendored, adapted, companion, derived), upstream repo/path, and
  refresh command. Read [`docs/skills-sources.md`](docs/skills-sources.md) before
  vendoring or refreshing. **When adding any skill, add a `sources.json` entry.**
  Vendored skills also get a `README.md` with the refresh one-liner.
- **Cross-runtime work:** read `docs/supported-agents.md` before making tooling
  work across runtimes.

### Predecessor
`~/Developer/agent-scripts` (private) is where these skills came from. It holds the
git history, the `sync-agent-scripts.sh` fan-out, `archived-skills/`, and the
maintenance tooling under `tools/`. Once the cutover is done it stops being the
source of truth for skills — add and edit skills here instead.

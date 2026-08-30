# Agent Instructions

This repository is the root of the `ossian-stack` plugin and the marketplace
metadata used to distribute it. It ships one thing: the skill tree under `skills/`.
There is no CLI, no runtime code, and no `sync-agent-scripts.sh` — the agent runtime
installs and updates the plugin itself.

`AGENTS.md` is the canonical repo instruction file. Root `CLAUDE.md` is a **symlink**
to it so Claude Code finds it at the expected path. Keep the symlink: this checkout
is also the plugin root, and a regular-file `CLAUDE.md` at a plugin root is not
loaded as end-user project context. `bun run validate` fails if the symlink is
replaced by a regular file.

## Quick Start

```bash
bun run check            # validate + plugin:validate — run before committing
bun run validate         # manifest/skill/sources/README consistency (no network)
bun run plugin:validate  # Claude's own schema check, --strict (needs `claude` on PATH)
bun run check:upstream   # which vendored skills moved upstream (needs `gh` + `jq`)
bun run docs:list        # index docs/ — do this before coding
```

Bun is a **dev-time task runner** for this repo's own checks. Skills may bundle
executables, but only in a runtime the user is likely to already have: Python 3 is
the default, and several skills ship `.py` helpers. Do not reach for Bun or Node in
a skill without a reason worth writing down.

One skill breaks this: `babysit` vendors `scripts/watch-pr`, a Bun-only TypeScript
CLI, because it is the mechanism the playbook is built around and rewriting it on
`gh` would lose its merge-state verdict. It runs `bun install` into its own
directory on first use — under a plugin install that is the versioned cache, which
is replaced on every update. The skill degrades to plain status reporting when
`bun` is absent. Any further exception needs the same kind of justification in
`skills/sources.json`.

## Local plugin development

Skills are **copied** into every runtime's cache, not symlinked, so an edit here is
never live until that runtime refreshes.

**Register the GitHub repo, not the local clone**, on the authoring machine too:

```
/plugin marketplace add ossianhempel/ossian-stack
```

A local-directory marketplace looks convenient and costs you automatic updates.
Measured on Claude Code 2.1.250, Codex 0.151.0-alpha and Copilot CLI 1.0.80:
Codex's `plugin marketplace upgrade` refreshes **git marketplaces only** and
reports "No configured Git marketplaces to upgrade" for a local path, and Claude
Code refuses to update a directory source whose version is unchanged, with no
`--force` in that build. Pointing at GitHub restores auto-refresh on all three.

The trade is that **pushing is what publishes**. An unpushed edit reaches no
runtime, which is also why `bun run check` runs as a pre-commit hook.

Plugin skills cache at session start, so invoking an edited skill in the session
that edited it tests stale content — restart the session. To know which copy is
loaded, diff the cache file against the working tree file; a matching version
segment proves only that the cache came from this release, not that it captured
your latest edit. Never edit `~/.claude/plugins/cache/` or
`~/.claude/plugins/marketplaces/` to force a reload: that is user machine state,
it gets overwritten on update, and it is the wrong layer to test from.

Full loop: `docs/plugin-workflow.md`.

## Working Agreement

- **Branching:** work directly on `main`. Branch only when Ossian explicitly asks.
  Single developer, no PR gate, no branch protection.
- **Safety:** use `trash` for deletes, never `rm`. Do not touch installed plugin
  caches or other repos' checkouts.
- **Validation:** run `bun run check` after any change to `skills/`, the manifests,
  `sources.json`, or `README.md`. It is fast and offline. `.githooks/pre-commit`
  runs `bun run validate` automatically; enable it once per clone with
  `git config core.hooksPath .githooks`.
- **Version bumps:** any change that should reach an installed runtime bumps
  `version` in **all three** manifests (`.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`). They must agree —
  `bun run validate` enforces it. Repo-tooling and docs-only changes do not need a bump.
- **Secrets:** `.env*` files and/or 1Password (`op` CLI). Never commit one.

## Repo Layout

```
skills/                 The plugin. One directory per skill, SKILL.md entry point
hooks/                  hooks.json + scripts; read by Claude Code and Codex alike
skills/sources.json     Upstream origin, pinned rev, refresh command per skill
commands/               Slash commands (currently empty)
.claude-plugin/         Claude Code plugin manifest + marketplace catalog
.codex-plugin/          Codex plugin manifest, same skills/ tree
bin/docs-list           Docs indexer — ships with the plugin
scripts/                Repo-local dev tooling — NOT plugin surface
.agents/skills/         Internal skills — loaded only in this checkout, never shipped
.claude/skills          Symlink to .agents/skills so Claude Code loads the same tier
docs/                   Repo docs
```

## Repo Surfaces

A change here touches one of three surfaces. Do not assume which without checking:

- **Plugin content** — `skills/`, `commands/`, `bin/docs-list`, and the three
  manifests. This is what reaches users; changes need a version bump.
- **Repo tooling** — `scripts/`, `package.json`, `.agents/skills/`. Runs only in a
  checkout. No version bump.
- **Docs** — `docs/`, `README.md`, `AGENTS.md`.

## Two skill tiers

| Where | Loaded when | Ships | `sources.json` entry | Version bump |
| --- | --- | --- | --- | --- |
| `skills/<name>/` | wherever the plugin is installed | yes | required | yes |
| `.agents/skills/<name>/` | cwd is this checkout | no | no | no |

`.agents/skills/` is the source of truth for internal skills; `.claude/skills` is a
**symlink** to it, so Claude Code, Codex, and Cursor all load one copy. Add a skill
once, every runtime that opens this repo sees it. `bun run validate` fails if that
symlink is replaced by a real directory, or if a name exists in both tiers.

`.agents/skills/<name>/` is also where `npx skills add` drops its download, which is
why every `refresh` command in `sources.json` ends by trashing the scratch copy. An
untracked directory there with no `SKILL.md` is leftover scratch — trash it.

Layout is identical in both tiers, so promoting a skill is a `git mv` plus a
`sources.json` entry with `"origin": "local"`. See `.agents/skills/README.md`.

## Plugin Maintenance

- **Source of truth is `skills/`.** Never edit the installed copy under
  `~/.claude/plugins/cache/ossian-stack/…` — it is overwritten on every update.
- **Every skill needs a `skills/sources.json` entry** recording its origin (`local`,
  `vendored`, `adapted`, `companion`, `derived`). Vendored and adapted skills also
  carry `repo`, `upstreamPath`, and `upstreamRev` — the commit the local copy is
  pinned to. Read `docs/skills-sources.md` before vendoring or refreshing.
- **Refreshing a vendored skill:** `bun run check:upstream` to see what moved, run
  the entry's `refresh` command, diff (adapted skills are merge-by-hand), then
  `scripts/check-upstream.sh --record <name>` to pin the new rev. Vendored skills
  also get a `skills/<name>/README.md` with the refresh one-liner.
- **Adding a skill:** create `skills/<name>/SKILL.md`, add the `sources.json` entry,
  add the name to the right group row in `README.md` and bump the two skill counts
  (badge + "Skills at a glance" lead), and bump the manifests.
  `bun run validate` enforces the README inventory: every skill name appears in it
  exactly once, no unknown names, counts match `skills/`. Choosing the right group
  is a judgment call it will not make for you.
- **Removing a skill:** delete the directory, its `sources.json` entry, and its
  README row in the same change, and bump the counts. `bun run validate` catches
  whichever one you forget.

## Working on Skills

A skill states the goal, the done condition, the safe failure direction, and the
facts the agent cannot derive from the repo in front of it — then gets out of the
way. It is not a state machine.

- **State conditions, not cases.** When a block keeps absorbing "handle the case we
  just hit", the representation is wrong: restate the condition and delete the
  accretions, then re-verify against every path they served.
- **Self-contained directories.** A `SKILL.md` may only reference files inside its
  own directory tree, by relative path. No `../other-skill/…`, no absolute path into
  a checkout or an install cache — installed plugins live at versioned cache paths
  that change every release, and the skill runs from the *user's* working directory,
  not the skill directory. If two skills need the same file, duplicate it.
  `bun run validate` greps for the broken patterns.
- **Cross-runtime by default.** Skills are authored once and loaded by both Claude
  Code and Codex. Avoid Claude-only constructs: inside a **skill**,
  `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}` are empty on Codex, so a call
  guarded on one silently never fires there — derive the path from the SKILL.md
  you just read instead. Inside a **hook** the opposite holds: Codex exports both
  `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT`, so `${CLAUDE_PLUGIN_ROOT}` is the correct
  and portable way to locate a bundled script. It does not export `extensionPath`,
  so an `${extensionPath:-.}` fallback silently resolves to the user's cwd there.
  When a platform variable is genuinely unavoidable, resolve it in one shell call
  and state what to do when it comes back empty.
- **Executed bundled scripts get an anchor.** The Bash tool's working directory is
  the user's project, so `bash scripts/x.sh` in a fenced block resolves to
  `<project>/scripts/x.sh` and exits 127. Set the path inline in the same command —
  shell state does not persist between calls:

  ```
  SKILL_DIR="<absolute path of the directory containing the SKILL.md you just read>";
  bash "$SKILL_DIR/scripts/my-script.sh" ARG
  ```

  Keep the trailing `;` — some hosts flatten the block onto one line, and without it
  the assignment becomes an env-var prefix that expands to empty. A script needing
  its *own* directory derives it from `BASH_SOURCE`, not `SKILL_DIR`.
- **No `!`cmd`` load-time pre-resolution.** It runs only on Claude Code, is inert
  text elsewhere, and a non-zero exit aborts skill load. Gather context at runtime
  with one argv-style command per shell call and read the exit status as data.
- **Reference conventions, not instruction filenames.** When a skill needs a project
  convention at runtime, say "the project's active instructions already in your
  context" rather than "read `AGENTS.md`/`CLAUDE.md`" — the filename differs per
  harness and the content is already loaded. Name a concrete file only when writing
  a convention back, or when a fresh subagent (which inherits nothing) must open it.
- **`GLOSSARY.md` is this plugin's name for a project's shared vocabulary.** Vendored
  skills arrive using other conventions and must be converted on the way in;
  `bun run validate` fails on `CONTEXT.md`, `CONCEPTS.md`, or `VOCABULARY.md`
  anywhere under `skills/`.
- **A skill may only name a sibling this plugin ships.** Pruning a skill leaves
  inbound references behind in the ones that pointed at it. `bun run validate`
  fails on each: every backticked kebab token in a `SKILL.md` must be a shipped
  skill, a path bundled with that skill, or listed in `NON_SKILL_TOKENS`. Adding
  a new CSS property or model id means adding it to that list — deliberate
  friction, because the earlier heuristic silently missed real dead links.
- **Describe the capability, not the tool.** "the project's issue tracker (GitHub
  Issues, Linear, Jira)" and "whatever interface it exposes" — never assume a
  specific CLI exists, and never treat a missing binary as proof the capability is
  unavailable.

## Runtime vs Authoring Context

`AGENTS.md` and `CLAUDE.md` are authoring context for **this** repo. Skills run in
end-user environments against *their* instruction files, not these. A rule that must
affect a skill at runtime belongs in that skill's `SKILL.md` or its `references/`,
never here.

## Commit Conventions

- **Classify by intent, not file type.** Files under `skills/` and the manifests are
  product code even though they are Markdown and JSON. Reserve `docs:` for files
  whose sole purpose is documentation (`README.md`, `docs/`).
- Where `fix:` and `feat:` both seem to fit, default to `fix:` — remedying broken or
  missing behavior is a fix even when implemented by adding code.
- **Scope is the narrowest useful label:** a skill name (`copywriter`,
  `check-upstream`), or an area (`manifests`, `docs`). Never scope with
  `ossian-stack` — that is the whole plugin and tells the reader nothing.

## Docs

- Run `bun run docs:list` before coding — it prints `summary` + `read_when` for every
  doc. In other repos, prefer that repo's own `docs:list` or `bin/docs-list`, then the
  copy this plugin ships at `${CLAUDE_PLUGIN_ROOT}/bin/docs-list`, which lists `./docs`
  from the current working directory and exits 0 when there is none.
- Add `read_when` hints to cross-cutting docs.

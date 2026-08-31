---
name: setup-ossian-stack
description: "Install this plugin on a machine and migrate off whatever preceded it: register the marketplace, install for each runtime present, retire superseded plugins and stale skill symlinks, approve the session-start hook where a runtime gates it, and report which optional CLIs are missing and which skills degrade without them. Use for /setup-ossian-stack, set up my skills, or migrate to ossian-stack."
disable-model-invocation: true
---

# Setup ossian-stack

Get this plugin installed, get what it replaces out of the way, and say plainly
what still will not work.

Prompt-driven, not a script: explore first, show the user what you found, confirm,
then act. **Every step that removes something waits for a yes.**

## 1. Explore before touching anything

Report what is actually there. Do not assume any of it.

- **Which runtimes are on this machine**, and where each keeps plugin state.
- **Which plugins are registered and enabled** in each, and their versions.
- **Whether this plugin is already installed**, and at which version.
- **Skill directories the user maintains by hand** — a global skills folder full
  of symlinks into another checkout is the pattern this plugin exists to replace,
  and it will keep shadowing the installed copy until it is cleared.
- **Superseded plugins.** Anything shipping a skill name this plugin also ships is
  a collision: whichever the runtime resolves first wins, and it will not be
  obvious which.
- **Optional CLIs**, checked by asking the shell, never assumed from a config file.

Present this as a short table before proposing anything.

## 2. Install

Detect the current runtime before installing. Prefer the native plugin route when
one exists, and use the GitHub repository rather than a local directory for normal
user installs so the runtime can refresh it.

- **Claude Code:** add `ossianhempel/ossian-stack` as a Git marketplace and install
  `ossian-stack@ossian-stack`.
- **Codex:** add `ossianhempel/ossian-stack` as a Git marketplace and install
  `ossian-stack@ossian-stack`.
- **Cursor:** add this repository as a Git marketplace with
  `cursor-agent plugin marketplace add <repo-url>`, then use Cursor's `/plugin`
  Marketplace UI to install `ossian-stack` at user scope. The CLI can refresh the
  catalog with `cursor-agent plugin marketplace update ossian-stack`, but current
  Cursor builds do not expose a non-interactive plugin-install subcommand. Do not
  substitute `/add-plugin <repo-url>`: that direct GitHub import is pinned. Local
  plugin copies are for testing only.
- **Gemini CLI, Copilot, Windsurf, and Antigravity:** use the shared skills
  installer against this repository, targeting the current runtime's global skill
  scope. Install directories under `skills/` only; `.agents/skills/` is internal
  checkout content. Tell the user that these runtimes refresh through the skills
  installer rather than a native plugin marketplace.

Install for every runtime found, not just the one you are running in.

## 3. Retire what it replaces

One confirmation per item, each naming exactly what disappears.

- **Superseded plugins**: uninstall through the runtime's own interface. Never
  delete a plugin's cache directory by hand — that is runtime-owned state and it
  comes back on the next update.
- **Hand-maintained symlinks**: list them, say what each points at, and remove
  only the ones this plugin now supersedes. A symlink pointing somewhere this
  plugin does not cover is not yours to remove.
- Anything the user says to keep, keep. Note the collision instead, so a later
  surprise has an explanation.

## 4. Approve the session-start hook

This plugin ships one hook: a session-start nudge for `continual-learning`. It
reads transcript counts and writes nothing the user owns.

Some runtimes ship plugin hooks **disabled** and pin them to a content hash,
requiring explicit approval before they run. Where that is the case, the hook is
silently inert until approved — say so, show the user what it does, and point them
at the runtime's own approval flow. Do not edit trust state by hand.

The hook needs `jq`. Without it, it exits silently and nothing else breaks.

## 5. Report what will not work

Check each of these by asking the shell, and name the ones that are missing
alongside what stops working. Degradation is per-skill, not global — a missing
tool disables a few skills, not the plugin.

| Binary | Needed by | Missing means |
| --- | --- | --- |
| `asc` | `asc-metadata`, `asc-pricing`, `asc-release`, `asc-version-guard`, `release-ios-app` | No App Store Connect work at all |
| `gh` | `autoreview`, `babysit`, `why`, `release-ios-app` | No PR, CI, or issue-history access |
| `jq` | `clerk-cli`, **and the session-start hook** | The hook exits silently — continual learning never nudges |
| `op` | `one-password`, `post-queue-cli` | No secret retrieval |
| `xcodebuild` | `ios-marketing-capture`, `release-ios-app` | No native builds or simulator captures |
| `gt`, `bun` | `babysit` | `watch-pr` cannot run; PR status falls back to plain reporting |
| `clerk` / `convex` / `rc` | `clerk-cli` / `convex-cli` / `revenuecat-api` | That backend's skill is unusable |
| `trash` | `git-cleanup` | Deletions have no recoverable path |
| `npx` | `clerk-cli`, `convex-cli`, `frontend-slides` | Skill-vendoring and scaffolding commands fail |

`jq` deserves its own line in the report: without it the hook fails **silently and
by design**, so nothing looks broken and continual learning simply never happens.

Say all of this plainly rather than burying it. A skill that fails on first use
because a binary was never installed reads as a broken plugin.

## 6. Project prerequisites — check, do not scaffold

When run inside a project, some skills expect a file the repo owns. **Most are
created lazily on purpose; pre-creating them is a mistake**, because an empty
`GLOSSARY.md` is a file that gets read, believed, and found empty.

- `GLOSSARY.md`, `GLOSSARY-MAP.md`, `docs/adr/` — `domain-modeling` creates these
  the moment it has something real to write, and `diagnosing-bugs` reads whichever
  exists. Do not create them here. Do not create them empty ever.
- A project-local skills directory — `close-the-loop` resolves or creates it when
  it generates a verifier. Leave it alone until then.
- `.env`, `.env.local` and friends — the project's own, never ours to write.
- **`.ios-release.env` is the exception.** `release-ios-app` reads it first and
  assumes it exists, so an iOS repo without one cannot use that skill. If this
  looks like an iOS app repo and the manifest is absent, say so and point at that
  skill's own `references/manifest.md`, which documents every key. Do not guess
  values — the manifest carries app IDs and branch names only its owner knows.

Report what is missing and who creates it. Create nothing in this step.

## 7. Verify

Confirm the installed copy is the one that answers. A skill list that still shows
the old source means step 3 did not finish, or the runtime needs a restart —
plugin skills are cached at session start, so an install is not live in the
session that performed it.

Say which runtime you verified in, and which you could not.

## Reply

What you found, what you installed, what you retired, what needs the user's
approval, and what still will not work and why.

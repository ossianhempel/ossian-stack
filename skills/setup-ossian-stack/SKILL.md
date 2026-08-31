---
name: setup-ossian-stack
description: "Configure a machine and project after this plugin is installed: retire superseded plugins and stale skill symlinks, approve the session-start hook where a runtime gates it, check the project-owned documents and structure the skills use, configure the issue tracker and triage labels the triage skills read, and report which optional CLIs are missing and which skills degrade without them. Use for /setup-ossian-stack, configure the plugin's prerequisites, or migrate an existing installation."
disable-model-invocation: true
---

# Set up ossian-stack

This skill assumes `ossian-stack` is already installed and loaded. Configure the
runtimes and current project for the plugin's skills, get what it replaces out of
the way, and say plainly what still will not work.

If the plugin is not installed, stop and use the repository's harness-specific
installation instructions first. This skill cannot bootstrap itself.

Prompt-driven, not a script: explore first, show the user what you found, confirm,
then act. **Every step that removes something waits for a yes.**

## 1. Explore before touching anything

Report what is actually there. Do not assume any of it.

- **Which runtimes are on this machine**, and where each keeps plugin state.
- **Which plugins are registered and enabled** in each, and their versions.
- **Whether this plugin is loaded and enabled** in each detected runtime, and at
  which version.
- **Skill directories the user maintains by hand** — a global skills folder full
  of symlinks into another checkout is the pattern this plugin exists to replace,
  and it will keep shadowing the installed copy until it is cleared.
- **Superseded plugins.** Anything shipping a skill name this plugin also ships is
  a collision: whichever the runtime resolves first wins, and it will not be
  obvious which.
- **Optional CLIs**, checked by asking the shell, never assumed from a config file.

Present this as a short table before proposing anything.

## 2. Confirm plugin readiness

Do not install the plugin in this step. If this skill is loaded, the current
runtime already has it. Confirm that it is enabled and identify the loaded copy.
For other runtimes, report whether a usable copy is present. If one is missing,
point the user to the repository's harness-specific installation instructions;
do not bootstrap that runtime from this skill.

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

## 7. Issue tracker and triage labels

`triage`, `to-tickets`, and `to-spec` read per-project config that, unlike the
files above, is **not created lazily** — an unconfigured tracker fails on first
use with no hint where the setting lives. Check for:

- `docs/agents/issue-tracker.md` — where issues live: GitHub (via `gh`), GitLab
  (via `glab`), local markdown under `.scratch/`, or a described workflow
  (Linear, Jira, …). Also records whether external PRs are a request surface.
- `docs/agents/triage-labels.md` — the mapping from the five canonical triage
  roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
  `wontfix`) to the actual label strings the tracker uses.

If both exist, sanity-check them against the repo: a `git remote` pointing at
GitHub with a GitLab tracker config is a mismatch worth surfacing. If either is
missing, ask where issues actually live — one question, recommended answer
first — and write the file after they confirm. Keep both short; they are
configuration the skills parse, not prose. Labels default to the canonical role
names unless the tracker already uses different strings.

Domain docs (`GLOSSARY.md`, `docs/adr/`) stay lazy — that is the section above,
not this one.

## 8. Verify

Confirm the installed copy is the one that answers. A skill list that still shows
the old source means step 3 did not finish, or the runtime needs a restart —
plugin skills are cached at session start, so an install is not live in the
session that performed it.

Say which runtime you verified in, and which you could not.

## Reply

What you found, what you installed, what you retired, what needs the user's
approval, and what still will not work and why.

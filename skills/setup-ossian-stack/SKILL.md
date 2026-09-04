---
name: setup-ossian-stack
description: "Configure a machine and project after this plugin is installed: retire superseded plugins and stale skill symlinks, approve the session-start hook where a runtime gates it, check project-owned prerequisites and issue-tracker config, and audit each skill's real execution paths without mistaking a non-global CLI for a missing capability. Use for /setup-ossian-stack, configure the plugin's prerequisites, or migrate an existing installation."
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

Match the setup scope to the request. For tracker-only setup, go directly to
section 7 and verify the resulting project configuration; skip machine, plugin,
and hook audits. A missing tracker is only a prerequisite gap for a chosen
ticket-based workflow, not a blocker for ordinary planning or delegation.

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
- **Skill execution paths**: global commands, current-project commands, package
  runners, active runtime tools/MCPs, and bundled fallbacks. A command absent from
  the current `PATH` is one observation, not proof that the capability is missing.

Present this as a short table before proposing anything.

## 2. Confirm plugin readiness

Do not install the plugin in this step. If this skill is loaded, the current
runtime already has it. Confirm that it is enabled and identify the loaded copy.
For other runtimes, report whether a usable copy is present. If one is missing,
point the user to the repository's harness-specific installation instructions;
do not bootstrap that runtime from this skill.

Record the registered marketplace source separately from the loaded cache. A
native runtime copies plugins; a marketplace pointing at a checkout does not make
that checkout live. Treat a local-directory marketplace as an unmanaged testing
source, not a ready normal install. Unless the user explicitly chose local testing,
offer one confirmed migration through the runtime's own interface: remove that
marketplace registration, register `ossianhempel/ossian-stack` as a Git marketplace,
install or refresh the named plugin, then start a new session. Never edit or delete
the runtime's cache by hand.

Auto-update is the default posture on every runtime. On Copilot this needs an
explicit opt-in: confirm the `ossian-stack` entry under `extraKnownMarketplaces`
in the user's `~/.copilot/settings.json` carries `"autoUpdate": true`, and add it
when it is missing. Only leave it off when the user explicitly declines.

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

Check the two independent runtime gates in order:

1. **Hooks feature enabled.** Some runtimes disable plugin hooks globally. When
   disabled, no trust prompt can appear. Point the user at the runtime's supported
   feature/configuration flow, enable it only with their approval, then restart.
2. **Hook approved.** Some runtimes pin hooks to a content hash and require explicit
   trust approval. Show the user what the hook does and use the runtime's approval
   flow. Do not edit trust state by hand.

Report these separately. “Hook valid” does not mean active when the feature is
disabled, and “feature enabled” does not mean the shipped hash is trusted.

The hook needs `jq`. Without it, it exits silently and nothing else breaks.

## 5. Report what will not work

Run the bundled read-only probe from the current project. Resolve its path from
the `SKILL.md` you just read; the runtime executes commands from the user's cwd:

```sh
SKILL_DIR="<absolute path of the directory containing this SKILL.md>";
python3 "$SKILL_DIR/scripts/check-capabilities.py"
```

The probe checks bare commands on this process's `PATH`, current-project
`node_modules/.bin` entries, and installed package runners. It does not download,
install, authenticate, or scan unrelated repositories. Combine that output with
the active runtime tools already available to you; a shell script cannot see MCPs
or other host-provided interfaces.

Classify each capability by the best execution path that actually exists:

- **Ready** — a global command, current-project command, active runtime tool/MCP,
  or bundled fallback can perform the work now.
- **On demand** — the owning skill supports an installed package runner, but its
  package is neither global nor current-project-local. Say which runner will fetch
  it on first use and that network access may be required. Do not call it missing.
- **Degraded** — the preferred path is absent but a narrower fallback works. Name
  only the lost surface.
- **Blocked** — no supported execution path remains. Only this state belongs in a
  “missing” list.

“Installed somewhere on the computer” is not the same as ready in the current
project. If an unrelated project owns a local binary, report it as **present
elsewhere**, not global, current-project-ready, or missing from the machine.

Use the owning skill's invocation contract instead of assuming every capability
is a bare binary:

| Capability | Supported paths | What absence actually means |
| --- | --- | --- |
| App Store Connect | `asc` | Without it, App Store Connect CLI work is blocked. |
| GitHub | `gh`, or a host-provided GitHub interface where the owning skill permits one | Missing `gh` blocks commands and bundled scripts that specifically require it; do not erase host-tool coverage. |
| GitLab | `glab`, or a host-provided interface where the owning skill permits one | Missing `glab` matters only where the tracker config names GitLab. |
| Jira | `curl`/`python3` against the REST API with `JIRA_*` credentials, or a repo-shipped Jira CLI | Missing credentials env vars is a configuration gap, not a missing capability — point at the tracker config's credentials section. |
| Linear | `curl` against the GraphQL API with `LINEAR_API_KEY`, plus `jq` for response shaping | A missing key is a configuration gap, not a missing capability. |
| Azure DevOps Boards | `az` with the `azure-devops` extension (`az extension add --name azure-devops`) | `az` without the extension covers nothing here; the extension is a one-time add. |
| Session-start hook | `jq` | Without it, the hook exits silently and continual learning never nudges. |
| Secret retrieval | `op` | Without it, `one-password` cannot retrieve secrets; already-materialized environment values are separate. |
| Native Apple tooling | `xcodebuild` | Without it, native builds and Simulator captures are blocked. |
| PR watcher | `bun` | Without it, `babysit` cannot run `watch-pr` and falls back to plain status reporting. |
| Clerk | global/project-local `clerk`, or `bunx`, `npx`, `pnpm dlx`, or `yarn dlx` | A package runner makes Clerk available on demand; lack of a global binary alone is not a failure. |
| Convex | current-project `convex` through `npx`/`bunx`, or a latest-package runner fallback | A package runner makes Convex available on demand; prefer the project's pinned package when present. |
| RevenueCat | active RevenueCat MCP, optional verified RevenueCat `rc`, or the bundled Python API helper with `python3` and `RC_API_KEY` | Missing `rc` alone is not degradation and never makes `revenuecat-api` unusable. A command named `rc` is only a candidate until its help identifies the RevenueCat CLI; the unrelated npm configuration package uses the same name. |
| Recoverable deletion | `trash` | Without it, `git-cleanup` must not delete. |
| Node package execution | `npx`, `bunx`, `pnpm dlx`, or `yarn dlx`, according to the owning skill | Report the runners that exist. Do not treat `npx` as universally required when a supported alternative is ready. |

`jq` deserves its own line in the report: without it the hook fails **silently and
by design**, so nothing looks broken and continual learning simply never happens.

Say all of this plainly rather than burying it. Report the evidence and the
execution path selected, not a guessed machine-wide installation state.

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

Configure a tracker when the user chooses ticket-based work or the active project
workflow requires tracked delivery. During general setup, an absent tracker is
optional unless that workflow is chosen; report it without forcing configuration.
Configuring a tracker does not authorize creating issues.

`triage`, `to-tickets`, `to-spec`, and `wayfinder` read per-project config that, unlike the
files above, is **not created lazily** — an unconfigured tracker fails on first
use with no hint where the setting lives. Check for:

- `docs/agents/issue-tracker.md` — where issues live, which native hierarchy,
  blocking, assignment, and label operations are available, and whether external
  PRs are a request surface.
- `docs/agents/triage-labels.md` — the mapping from the five canonical triage
  roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
  `wontfix`) to the actual label strings the tracker uses.
- `docs/agents/ticket-brief.md` — the shape of every ticket body. Copy
  `references/ticket-brief.md`, dropping its leading copy-me line; `to-tickets`, `to-spec`, and `triage`
  write it and a cold pickup agent reads it.
- `docs/agents/handoff-comment.md` — when to comment and the concise content
  needed for meaningful updates and ownership recovery. Copy
  `references/handoff-comment.md`, dropping its introductory copy paragraph.
  Resume from the ticket/spec, relevant handoff records, and linked evidence.
- `docs/agents/pickup-loop.md` — the prompt the user pastes into the host's
  `/loop` or a scheduled routine to have agents take `ready-for-agent` tickets
  autonomously. Copy `references/pickup-loop.md`, dropping its leading
  copy-me paragraph. There is no pickup
  skill: the runner is a host capability, the operations live in the tracker
  config's "Pickup operations" section.

Supported trackers, each with a ready-to-adapt template bundled with this skill:

| Tracker | Interface | Template (under `references/trackers/`) |
| --- | --- | --- |
| GitHub Issues | `gh` | `github.md` |
| GitLab Issues | `glab` | hand-write, mirroring the `github.md` shape |
| Local markdown | files under `.scratch/<feature-slug>/issues/` | hand-write, mirroring the `github.md` shape |
| Linear | GraphQL API via `curl` with `LINEAR_API_KEY` | `linear.md` |
| Jira | REST API via `curl`, or a repo-shipped CLI | `jira.md` |
| Azure DevOps Boards | `az` + `azure-devops` extension | `azure-devops.md` |
| Notion | the Notion MCP server (must be connected in the runtime) | `notion.md` |

If both files exist, sanity-check them against the repo: a `git remote` pointing at
GitHub with a GitLab tracker config is a mismatch worth surfacing. For a chosen
ticket workflow, if either is missing, ask where issues actually live — one question, recommended answer
first (GitHub for a GitHub-hosted repo) — and write the file after they confirm.
For a supported tracker, start from the template and fill in the project
specifics; do not improvise the command recipes. For Notion, discover existing task or issue databases with the MCP first
(fetch each hit and dedupe by data source id, since one shared Tasks database
appears as a linked view under every project page), present them, and ask whether to use one of them (shared, scoped by a `Project`
property, or dedicated) or create a new dedicated one; then map the chosen
database's actual property names in the template's table. Notion has no CLI: before
writing its config, confirm the session exposes `notion-*` MCP tools, and if not
tell the user to connect the Notion MCP in every runtime they use — the tracker
skills stop rather than fall back when the tools are absent. Keep both short; they are
configuration the skills parse, not prose. Labels default to the canonical role
names unless the tracker already uses different strings.

Existing project copies do not update when the plugin refreshes. During requested
project setup or policy refresh, compare the handoff-comment, pickup-loop, and
tracker configuration with these templates and merge the reporting policy into
the selected project. Preserve its property/label mappings, API recipes, claim
arbitration, permissions, and other customizations; do not overwrite whole files
or edit live tickets. Apply the same policy to custom GitLab/local tracker recipes.

Domain docs (`GLOSSARY.md`, `docs/adr/`) stay lazy — that is the section above,
not this one.

## 8. Verify

Confirm the installed copy is the one that answers. A skill list that still shows
the old source means step 3 did not finish, or the runtime needs a restart —
plugin skills are cached at session start, so an install is not live in the
session that performed it.

Say which runtime you verified in, and which you could not.

## Reply

Lead with the runtime invoking this skill. If it is not fully ready, its first
unresolved prerequisite is the single **Next action**. Put actions for other
runtimes in a separate secondary list; never make another runtime's restart the
primary action while the invoking runtime remains blocked.

Report what you found, what you installed, what you retired, what needs the
user's approval, and what is ready, on demand, degraded, or blocked and why. Name
the exact probe behind every blocked claim. Never describe a plugin as live from
a checkout merely because its marketplace points there: native runtimes copy
plugins into caches, so identify the loaded cached copy and the source separately.

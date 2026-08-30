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

Register this repository as a marketplace and install the plugin, through
whatever interface each runtime exposes for that. On the authoring machine,
register the **local clone** rather than the remote, so an edit is live after a
marketplace refresh instead of after a push.

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

Name each missing CLI, the skills that depend on it, and what happens without it.
Degradation is per-skill, not global — a missing tool disables a few skills, not
the plugin.

Say this plainly rather than burying it. A skill that fails on first use because
a binary was never installed reads as a broken plugin.

## 6. Verify

Confirm the installed copy is the one that answers. A skill list that still shows
the old source means step 3 did not finish, or the runtime needs a restart —
plugin skills are cached at session start, so an install is not live in the
session that performed it.

Say which runtime you verified in, and which you could not.

## Reply

What you found, what you installed, what you retired, what needs the user's
approval, and what still will not work and why.

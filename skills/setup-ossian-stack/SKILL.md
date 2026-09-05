---
name: setup-ossian-stack
description: "Verify plugin installation and configure approved machine or project prerequisites, hooks, migrations, and issue-tracker integration."
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

Match the setup scope to the request. For tracker-only setup, read the issue-tracker reference directly and verify the resulting project configuration; skip machine, plugin,
and hook audits. A missing tracker is only a prerequisite gap for a chosen
ticket-based workflow, not a blocker for ordinary planning or delegation.



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

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Machine migration](references/machine-migration.md): machine-wide setup or approved retirement of superseded installs.
- [Session start hook](references/session-start-hook.md): hook feature readiness and host trust approval.
- [Dependencies and project](references/dependencies-and-project.md): capability probes and current-project prerequisites.
- [Issue tracker](references/issue-tracker.md): tracker-only setup or a requested tracked-delivery workflow.

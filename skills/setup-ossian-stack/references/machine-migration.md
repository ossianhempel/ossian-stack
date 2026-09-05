# Machine Migration

Read for machine-wide setup or approved retirement of superseded installs. Follow the scope and safety contract in the skill entry point.

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

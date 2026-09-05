# Dependencies And Project

Read for capability probes and current-project prerequisites. Follow the scope and safety contract in the skill entry point.
In commands and code examples, resolve bundled paths from the directory containing the loaded SKILL.md; do not use the caller's working directory.

## 5. Report what will not work

Run the bundled read-only probe from the current project. Resolve its path from
the `../SKILL.md` you just read; the runtime executes commands from the user's cwd:

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

If the project has no `verify-*` skill or equivalent harness that can drive the
real product surface, offer once: "Want a project-local verification skill so
agents can exercise the app like a user and prove changes work? Invoke
`/close-the-loop` and I will generate one." This is optional setup. On no, move
on without asking again or treating the missing verifier as a general blocker.

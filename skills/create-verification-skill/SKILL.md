---
name: create-verification-skill
description: "Create and prove a project-local verification skill that launches and drives the real app, CLI, or service."
disable-model-invocation: true
---

# Create Verification Skill

Every serious project needs a scripted way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. Without it an agent can tell you it finished, never that it worked, repeated prompting rather than a loop. This skill generates the missing check as a project-local skill (`<skills-dir>/verify-<app>/`) tailored to the repo, plus one control CLI (`control-<app>`) that is the only way that skill touches the app. You write the generator's output for the next agent, not for a human: it will be read cold, mid-task, by an agent that has never seen the app.

## 0. Resolve where project-local skills live

Do not assume a path. Look for a skills directory the repo already uses, in this
order, and write into the first that exists: `.agents/skills/`, `.claude/skills/`,
`.cursor/skills/`. If none exists, create `.agents/skills/`, Codex and Cursor
both read it. Claude Code does not, so when the project is also used with Claude
Code, add `.claude/skills` as a symlink to `.agents/skills` rather than a second
copy, so one tree serves every runtime.

Everything below writes `<skills-dir>/verify-<app>/`. Say which directory you
resolved, once, before you write.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth, and which test accounts exist locally and in any preview environment.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first, Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Inventory:** can the user-facing surfaces be listed from source? A generated route tree, a router config, a CLI command registry, an OpenAPI spec. This decides whether the map gets a mechanical check (step 4).
- **Deploy:** does the app deploy somewhere an agent can reach (preview per PR, production), and does it expose the running build's commit (a health or version endpoint)? Note it; it decides whether the CLI gets `health`.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout doesn't build or start as-is, fix that first (or report it precisely) before generating; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config), the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

## 2. Build the control CLI

Write one command, `control-<app>`, in the project's own tooling: its existing runtime and task runner (a package script, a Makefile target, `scripts/control-<app>`), not a new toolchain. It lives in the project rather than the skill directory because CI runs it too. Subcommands cover every action the skill needs, at minimum:

- `doctor`: read-only answer to "is this instance worth driving?": process up, right version/build, port owned by us, auth valid. When setup is missing (unmigrated database, no seed data) it prints the exact command that fixes it.
- `dev` (or `launch`): start the app for verification and wait until it is ready; `stop` tears down what it started.
- `login`: sign in as a seed account and keep the session where the other subcommands find it. Credentials and cookies never pass through the agent's own shell commands.
- Drive subcommands for the surface: `request <METHOD> <path>` with body assertions (`--contains`, `--dump`) for HTTP, `browse --path` with `--screenshot` for UI, a PTY/tmux runner for CLI/TUI. Reuse existing harnesses underneath.
- `map` and `map --check` (step 4).
- `health --sha <commit>` when the interview found a reachable deploy that reports its build: it passes only when that origin runs the given commit or a descendant of it. Skip it otherwise.

Each subcommand exits non-zero on failure and prints what it checked. Make it executable and runnable from the project root.

## 3. Generate the skill

Write `<skills-dir>/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, the surface, and when to reach for it, without frontmatter the skill never registers) and these sections, each grounded in what the interview actually found (no placeholders left):

- **Opening:** the `control-<app>` command list, then the rule that the CLI is the only way in: no throwaway curl or scripts, no copying session cookies or tokens into other tools, no rediscovering routes or commands from source. When the CLI lacks an action the task needs, add a subcommand and document it here instead of working around it.
- **Launch:** the exact command that starts the app for verification, and how to tell it's ready (a log line, a port answering, a prompt). Include teardown. For a short-lived CLI or TUI there is no server to keep alive: launch means build the binary (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** `control-<app> doctor`. An agent runs it first, and again whenever anything looks off.
- **Seed accounts:** which test accounts exist where (local, preview), what each can and cannot reach, and where the password comes from (a committed test-only value, or a secret-manager reference). Never write a real credential into the skill.
- **Drive:** the `control-<app>` invocations with real selectors, paths, and commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name: some dry-runs still touch the network or open a browser.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill what you started. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names. Devices are instances: a run that creates or clones a simulator or emulator deletes it before it ends, on failure as well as success, and a run that boots an existing one shuts it down. For iOS, copy [`scripts/sim-ledger.py`](scripts/sim-ledger.py) into the generated skill and wire it in: `begin` before the first build, devices created through it (which also catches `xcodebuild`'s parallel-test clones), `end` in Cleanup. Never delete a device the run did not create.
- **Proof ladder:** local first. Name the cases that need a preview or deployed instance (third-party callbacks, platform bindings, deploy config), and, when `health` exists, that a shipped change is proven only once `control-<app> health --sha <merge-commit>` passes against production.
- **Helpers:** anything the skill ships beyond the CLI is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper.

## 4. Seed the feature map

Create `<skills-dir>/verify-<app>/features/README.md` plus one file per user-facing feature you can identify (aim for the top 3-5 to start, from routes, commands, menus, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others. The skill tells the reader to load only the feature file for the surface it is changing, not the whole map.

When the interview found a source inventory, `control-<app> map` prints it and `map --check` fails when a feature file cites a route or command that does not exist, an inventoried user-facing surface has neither a feature file nor a recorded exemption, or a feature file is missing from or orphaned by the README index. Derive the inventory from source on every run; a hand-kept copy rots like the map it checks. Add `map --check` to the project's CI or its existing check command. When surfaces cannot be listed from source, say so in the skill: that map is kept honest only by `/maintain-verification-skill`.

## 5. Prove the generated skill before handing it over

Run its own instructions end to end once: `map --check` where it exists, launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location, a cleanup that eats the proof fails this step. Also compare the simulator, emulator, and process lists with a snapshot taken before launch: anything the run added that is still there fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable.

## 6. Offer the maintenance loop

Point the user at `/maintain-verification-skill` for keeping the map honest as the app changes. Suggest a cadence only if they ask.

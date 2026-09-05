---
name: clerk-cli
description: "Manage Clerk auth, users, organizations, sessions, configuration, impersonation, webhooks, and API requests with the Clerk CLI."
license: MIT
---

# Clerk CLI

The `clerk` binary is a pre-authenticated gateway to Clerk's Backend API and Platform API, plus project-level tooling (auth, linking, env pulls, instance config). When the user asks anything that touches a Clerk resource, reach for `clerk` first instead of hand-rolling `curl`.

> This skill targets clerk `latest`. If `clerk --version` disagrees with the latest available CLI, refresh it with `clerk skill install` or a package runner such as `bunx clerk@latest`. The binary is always the source of truth, so run `clerk <command> --help` to verify anything this skill claims.

Establish the actual account, app, and instance before acting. Read execution-and-auth for the command/auth setup and when host-state access may explain a failure. Reuse working secure authentication; resolve access through the host's supported permission mechanism. Discover commands and endpoints from live help. Keep mutations within the user's requested target and scope.

## The mental model

| Layer                           | What it does                                                                                 | Commands                                                       |
| ------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Session / project**           | Auth, link a repo to a Clerk app, pull env keys                                              | `auth login`, `link`, `unlink`, `whoami`, `env pull`, `doctor` |
| **Instance config**             | Manage the configuration (social providers, session lifetimes, etc.) for a specific instance | `config pull`, `config schema`, `config patch`, `config put`   |
| **Backend API (default)**       | Runtime data: users, orgs, sessions, invitations, JWT templates, webhooks                    | `clerk api <path>`                                             |
| **Platform API (`--platform`)** | Account-level: applications, instances, billing                                              | `clerk api --platform <path>`                                  |
| **Frontend API (`--fapi`)**     | The instance's public client-facing API (what clerk-js calls)                                | `clerk api --fapi <path>`                                      |

A project is "linked" to an application via `clerk link`. Once linked, most commands auto-resolve the target app and dev instance from the repo's git remote. To target something else, pass `--app <id>` and/or `--instance dev|prod|<instance_id>`. See [references/auth.md](references/auth.md) for the full resolution order.

## Discover endpoints - don't memorize them

The CLI ships with the Clerk OpenAPI catalog. Always discover endpoints dynamically instead of guessing paths:

```sh
clerk api ls                  # list every Backend API endpoint
clerk api ls users            # filter by keyword (matches path, summary, tag, operationId)
clerk api ls --platform apps  # list Platform API endpoints
```

Use this before `clerk api <path>`. If you don't see the endpoint you expected, it probably isn't exposed.

## Inspecting large outputs (do not flood your context)

`users list`, `apps list`, `config pull`, and most `clerk api` GETs return payloads that can be many kilobytes or megabytes. Production tenants commonly have thousands of users; an instance config can be hundreds of fields deep. Reading those responses into the conversation costs context window for no benefit. Save the response to a file first, then query just what you need with `jq`:

```sh
# 1. Persist the response. Use --limit 250 to maximize page size for users list.
clerk users list --json --limit 250 > /tmp/users.json
clerk apps list --json                > /tmp/apps.json
clerk api /users/user_abc123          > /tmp/user.json

# 2. Inspect only what you need.
jq '.data | length'                       /tmp/users.json   # current page size
jq '.hasMore'                             /tmp/users.json   # are more pages available?
jq '.data[0] | keys'                      /tmp/users.json   # discover the user shape once
jq '.data[] | {id, email_addresses}'      /tmp/users.json   # project to a few fields
jq '[.data[] | select(.banned)] | length' /tmp/users.json   # aggregate without reading rows
```

**If `jq` is not available**, fall back to Python or Node - both can stream the file without printing it whole:

```sh
python3 -c 'import json; d=json.load(open("/tmp/users.json")); print(len(d["data"]), d["hasMore"])'
node -e 'const d=require("/tmp/users.json"); console.log(d.data.length, d.hasMore)'
```

`cat` / `head` the file only when you genuinely need to see the raw structure for one-off debugging. When walking pages, write each page to its own file (e.g. `page-${offset}.json`) so individual pages stay independently inspectable.

## Agent-mode behavior (important)

The CLI auto-detects agent mode when stdout is not a TTY, or when `--mode agent` / `CLERK_MODE=agent` is set. In agent mode:

- **Interactive prompts are disabled.** Commands that would normally show pickers (`link` without `--app`, `unlink` without `--yes`, `users` without a subcommand) either auto-resolve or exit with a usage error. `clerk api` with no args prints usage guidance and exits 0; pass an endpoint (or `ls`) explicitly. Always pass explicit flags (`--app`, `--yes`) in scripted calls.
- **Host-sensitive operations emit a sandbox warning once per invocation.** Home-directory Clerk state, keychain access, networked Clerk calls, browser launch, and localhost OAuth callback setup can trigger the warning shown above. If it appears, rerun the same command on the host before trusting the result.
- **If your harness does not clearly present as agent mode, force it.** Use `--mode agent` or `CLERK_MODE=agent` when you want the CLI's non-interactive behavior and sandbox warning path to apply deterministically.
- **`link` supports deterministic agent flows.** In agent mode, `clerk link --app <id>` links directly. Without `--app`, the CLI will try silent key-based autolink first; if it cannot determine the app unambiguously, it exits and tells you to pass `--app`.
- **`init` never selects or creates a real Clerk app for you in agent mode unless authenticated or given a target.** Pass `--app <id>` (or pre-link the project) to authenticate and link a real app, or pass `--keyless` to use auto-generated temporary development keys when bootstrapping a new project on a keyless-capable framework. Without either, agent mode prints manual setup guidance and exits cleanly.
- **`unlink` requires `--yes` in agent mode.** This preserves the same safety bar as other destructive commands while still letting an agent complete the unlink non-interactively.
- **Mutations still require `--yes`** unless you accept per-call confirmation is impossible.
- **`impersonate` requires the `[user]` positional in agent mode.** If a search term matches multiple users, it exits `2` listing candidate user IDs — retry with a specific `user_...` ID. Output is a JSON object (`{url, id, userId, actor, ...}`); surface `url` to the user and capture `id` — it is the only chance to record the revoke handle.
- **`webhooks listen` is long-running.** Run it in the background. In agent mode (or with `--json`) it emits NDJSON: one `ready` line (`{type:"ready", relay_url, forward_to}`), then one `event` line per delivery — each event line can be fed back to `clerk webhooks verify --delivery`.
- **`doctor --fix` is ignored.** Parse `doctor --json` output's `remedy` field and act on it yourself.
- **`apps list` and `apps create` default to JSON** when piped.
- **`users` defaults to JSON when piped, like `apps`.** `clerk users list` and `clerk users create` emit JSON in agent mode. Bare `clerk users` (no subcommand) is a usage error in agent mode - pass `list`, `create`, or `open` explicitly. `clerk users open` requires the `user-id` positional in agent mode and prints a JSON descriptor instead of launching a browser.
- **`deploy` has an agent handoff plus a verification gate.** In agent mode, bare `clerk deploy` is read-only and emits a JSON handoff. It never drives the interactive wizard. Do not tell Claude or another agent to run `! clerk deploy`, because the wizard needs interactive stdin prompts. Ask the human to run `clerk deploy` in a new terminal window when needed, then run `clerk deploy status --mode agent` to verify completion. See [references/agent-mode.md](references/agent-mode.md#deploy-handoff-and-verification).
- **`--input-json <json|@file|->`** expands JSON into flags on any command (e.g. `clerk init --input-json '{"framework":"next","yes":true}'`). Stdin needs the explicit `-` marker (`echo '{"yes":true}' | clerk init --input-json -`); bare piped stdin is **not** auto-detected, so shell loops and self-reading commands (`cat body.json | clerk api …`) are untouched. Place `--input-json` after the leaf subcommand. Full rules in [references/agent-mode.md](references/agent-mode.md#passing-options-as-json---input-json).

Full matrix and sandbox details in [references/agent-mode.md](references/agent-mode.md).

## Output format and errors

- **JSON output:** `--json` on `apps list` and `doctor`. For `clerk api`, the response body is the raw API JSON, so pipe into `jq` freely.
- **Exit codes:** `0` success, `1` runtime error, `2` usage/validation error. `doctor` returns `1` if any check failed.
- **Error format:** User-facing errors print a single line to stderr and set a non-zero exit code. Use `--verbose` for stack traces when debugging.

## Safety rules for autonomous use

1. **Discover before acting:** `clerk api ls <keyword>` before `clerk api <path>`.
2. **Preview mutations:** `--dry-run` on every `config patch`, `config put`, `api -X POST/PATCH/PUT/DELETE`.
3. **Target explicitly in production:** pass `--instance prod` rather than relying on defaults, and confirm with the user before any production mutation.
4. **Never commit secrets:** `env pull` writes to `.env.local` (which should be gitignored). Don't paste secret keys into code or chat.
5. **Use `doctor --json`** to diagnose before assuming the CLI is broken.

## References

- [references/auth.md](references/auth.md) - auth flow, key resolution order, host-vs-sandbox behavior, `--app`/`--instance` targeting, Backend vs Platform API.
- [references/recipes.md](references/recipes.md) - copy-pasteable recipes for common Clerk tasks.
- [references/agent-mode.md](references/agent-mode.md) - agent-mode behavior matrix, sandbox warning semantics, exit codes, error format.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Execution and auth](references/execution-and-auth.md): binary selection, action-time authentication, project linking, or sandbox-related failures.
- [Api and commands](references/api-and-commands.md): an API request or command catalogue.

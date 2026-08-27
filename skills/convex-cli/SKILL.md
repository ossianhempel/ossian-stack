---
name: convex-cli
description: >-
  Operate the Convex CLI (`npx convex`) for dev sync, deploy, codegen, run/query
  functions, inspect tables, env vars, logs, export/import, insights, and
  deployment management. Use this skill whenever the user touches Convex backend
  operations from the terminal — even if they never say "CLI" — including deploy
  to prod or preview, `convex dev` / one-shot sync, push schema or function
  changes, run a mutation or query from shell, list or dump table data, set
  Convex env vars, tail logs, check OCC/insights, seed data via `convex run`, or
  debug "Convex not syncing" / types out of date. Also trigger on npx convex,
  CONVEX_DEPLOYMENT, deploy key, preview deployment, or requests to inspect or
  fix production Convex data. Prefer `npx convex` over raw HTTP or dashboard-only
  workflows; it handles auth, deployment targeting, and codegen. Do not use for
  authoring new Convex functions in code — use convex-function-creator instead.
---

# Convex CLI

The `convex` npm package ships the CLI. In a project with `convex` installed, run `npx convex <command>`. When the repo pins an older CLI or a command is missing, use `npx -y convex@latest <command>`.

Docs: https://docs.convex.dev/cli — run `npx convex docs` to open them.

## Invoking the CLI

Pick one invocation style per session and stick to it:

| Context | Invocation |
| --- | --- |
| Project has `convex` in `package.json` | `npx convex …` |
| No local install / stale CLI / missing subcommand | `npx -y convex@latest …` |
| Bun project | `bunx convex …` or `bunx convex@latest …` |

Before unfamiliar commands: `npx convex <command> --help`.

## Prerequisites

From the project root (where `convex/` and `.env.local` live):

```sh
npx convex --version
test -d convex && test -f .env.local && grep -q CONVEX_DEPLOYMENT .env.local
```

If `convex/` or `CONVEX_DEPLOYMENT` is missing, use `convex-quickstart` first — do not guess deployment URLs.

## Deployment targeting

| Variable / flag | Meaning |
| --- | --- |
| `CONVEX_DEPLOYMENT` in `.env.local` | Personal **dev** deployment while developing |
| `CONVEX_DEPLOY_KEY` | CI / preview / prod deploy key (overrides dev targeting on `deploy`) |
| `--prod` | Target production deployment (on `run`, `logs`, `data`, `env`, `insights`, …) |
| `--preview-name <name>` | Target a preview deployment |
| `--deployment-name <name>` | Target a specific deployment |
| `--env-file <path>` | Override env file for deployment selection |

**Mental model:** `npx convex dev` syncs to your **dev** deployment. `npx convex deploy` pushes to **prod** (or preview when `CONVEX_DEPLOY_KEY` is a preview key). Never deploy to prod without explicit user intent.

### Production inspection contract

Production conclusions need stronger target proof than ordinary development
commands. A repo may have an anonymous/local deployment in `.env.local`, more
than one production deployment, or an older CLI whose environment-variable
precedence differs from current releases.

For production `data`, `run`, `logs`, `env`, `insights`, `function-spec`, and
`export` operations:

1. Resolve the intended deployment name from an authoritative source such as
   the shipped client configuration, CI/EAS configuration, or the Convex
   dashboard. If multiple regions or deployments exist, name the exact target.
2. Inspect the repo's local selector shape without printing secrets. Treat
   `anonymous:*`, localhost URLs, self-hosted URLs, and unexpected project names
   as evidence that default or environment-based selection is unsafe.
3. When local/anonymous mode is configured, use
   `npx -y convex@latest ... --deployment-name <exact-name>` on every production
   read. Older project-pinned CLIs may keep routing to localhost even when an
   environment override or `--deployment-name` appears to select cloud. Do not
   rely on `CONVEX_DEPLOYMENT=...`, `--prod`, or the repo's default selector for
   a serious production conclusion.
4. Start with a small known-table sample and state the selected deployment in
   the result. `--limit` is a sample limit, not a count operation; avoid huge
   values that can exceed the CLI query cap.
5. Cross-check surprising empty, sparse, or destructive-looking results in the
   dashboard or through a second explicit-target read before reporting data
   loss, reset, migration failure, or wrong-environment writes.

Safe inspection example:

```sh
deployment_name="adjective-animal-123"
npx -y convex@latest data tasks \
  --deployment-name "$deployment_name" \
  --limit 20 \
  --format json
```

Outside local/anonymous mode, the project-pinned CLI remains preferable for
version compatibility, but keep the explicit deployment name and target proof.
An environment override that appears correct is not target proof.

## Agent execution (read this first)

`npx convex dev` is a **long-running watcher** and may require browser OAuth on first setup. Agents should **not** start it as a background daemon unless the user explicitly asks.

Prefer these agent-safe patterns instead:

| Goal | Command |
| --- | --- |
| One-shot sync + codegen to dev | `npx convex dev --once` |
| Retry sync until push succeeds | `npx convex dev --until-success` |
| Regenerate types only | `npx convex codegen` |
| Run a function without watching | `npx convex run …` (add `--push` to push first) |
| Inspect data / env / logs | `npx convex data`, `env`, `logs` |
| Headless / sandbox dev (no OAuth) | `CONVEX_AGENT_MODE=anonymous npx convex dev --once` |

See [references/agent-mode.md](references/agent-mode.md) for sandbox, auth, and CI details.

## Core commands

| Command | Purpose |
| --- | --- |
| `dev` | Watch `convex/`, push to dev, regenerate `_generated/` |
| `deploy` | Push to prod or preview; optional `--cmd` to build frontend |
| `run <fn> [args]` | Run query/mutation/action; JSON args; `--watch` for live query |
| `run --inline-query '…'` | Evaluate a readonly inline query (sandboxed) |
| `codegen` | Regenerate `convex/_generated/` without full dev loop |
| `data [table]` | List tables or print rows (`--limit`, `--order`) |
| `env list\|get\|set\|remove` | Read/write deployment env vars |
| `logs` | Tail deployment logs (`--prod` for production) |
| `insights [--details]` | OCC conflicts and resource-limit health (last 72h) |
| `export --path …` | Export DB (+ optional file storage) to zip/dir |
| `import --table … <path>` | Import data from file or zip |
| `dashboard` | Open Convex dashboard in browser |
| `deployment` | Manage deployments |
| `function-spec` | List function metadata from deployment |
| `login` / `logout` | Manage Convex credentials on this machine |
| `update` | Print instructions for updating the `convex` package |
| `mcp` | Manage Convex MCP server (beta) |

## Common recipes

### Run a function

```sh
# Public function with JSON args
npx convex run messages:send '{"body": "hello", "author": "me"}'

# Push local code first, then run
npx convex run tasks:list --push

# Live-updating query
npx convex run tasks:list --watch

# Production (explicit)
npx convex run tasks:list --prod
```

Function identifiers: `file:functionName` or `api.module.function` style depending on export — check `convex/_generated/api`.

### Inspect database

```sh
npx convex data                    # list tables
npx convex data tasks --limit 20   # sample rows
npx convex data _storage           # system tables work too
```

For complex filters, write a temporary query or use `--inline-query`.

### Environment variables

```sh
npx convex env list
npx convex env get API_KEY
npx convex env set API_KEY          # interactive / stdin-safe
pbpaste | npx convex env set API_KEY
npx convex env set --prod SOME_FLAG value   # production
```

Never commit secrets. Never paste deploy keys or secret env values into chat.

### Deploy

```sh
# Dev sync (agent-safe one-shot)
npx convex dev --once

# Production — only with explicit user approval
npx convex deploy

# CI pattern: build frontend with deployment URL injected
npx convex deploy --cmd "npm run build"

# Preview (requires preview deploy key in env)
npx convex deploy --preview-create my-branch-name
```

### Debug performance

```sh
npx convex insights --details
npx convex insights --prod --details
```

If `insights` is missing locally, retry with `npx -y convex@latest insights --details`.

## Safety rules for autonomous use

1. **Read before write.** Use `data`, `run`, or `env list` before mutations or env changes.
2. **Prefer `--once` over `dev`.** Do not leave watchers running unless the user asked.
3. **Confirm prod.** For reads, resolve and pass the exact `--deployment-name`; for `deploy` or production writes, confirm the target and user intent separately.
4. **Preview destructive ops.** For `import`, `env remove`, or prod `deploy`, state the target deployment first.
5. **Commit `_generated/`.** Codegen output belongs in git; run `dev --once` or `codegen` after backend edits.
6. **Auth failures in sandboxes are inconclusive.** Rerun on the host before reporting "not logged in".

## Relationship to other Convex skills

| Skill | Use when |
| --- | --- |
| `convex-quickstart` | New project, provider wiring, first-time setup |
| `convex-function-creator` | Writing queries, mutations, actions in code |
| `convex-schema-builder` | Designing tables and indexes |
| `convex-setup-auth` | Auth integration |
| `convex-cli` (this skill) | Operating deployments, data, env, logs, deploy/run from terminal |

## References

- [references/agent-mode.md](references/agent-mode.md) — headless dev, anonymous mode, CI deploy keys, sandbox pitfalls

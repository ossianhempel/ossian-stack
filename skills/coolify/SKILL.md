---
name: coolify
description: "Inspect and manage Coolify applications, databases, services, deployments, domains, environment variables, and infrastructure."
---

# Coolify CLI

Coolify is an open-source, self-hostable PaaS. The `coolify` CLI wraps the Coolify REST API (`/api/v1`) for terminal-based management.

**Two surfaces:**
- **v4 API CLI** (default) — talks to a running Coolify instance via API token.
- **v5 alpha** — `coolify init` and `coolify firewall` manage a WireGuard mesh / Podman control plane over SSH; no Coolify API. See [references/commands.md](references/commands.md#v5-alpha-control-plane).

For the full command tree, see [references/commands.md](references/commands.md). Upstream source of truth: [coolify-cli llms-full.txt](https://github.com/coollabsio/coolify-cli/blob/v4.x/llms-full.txt). OpenAPI: [openapi.json](https://github.com/coollabsio/coolify/blob/v4.x/openapi.json).

Identify the actual instance/context and resource UUID before any operation. Read workflows for the selected operation; use setup-and-auth only when context, tooling, or authentication needs attention. Preserve read-only requests and existing secure credentials. Deployment, destructive operations, and configuration changes stay within inherited authorization; verify the resulting state without exposing secrets.

## Key Patterns

- **UUIDs everywhere** except teams (numeric IDs). Extract with `list --format json | jq`.
- **`--format json|pretty|table`** — prefer JSON in scripts.
- **`--show-sensitive` / `-s`** — reveal passwords, tokens, connection strings.
- **`--context`, `--token`, `--host`** — target instances without editing config.
- **Aliases** — `app`/`apps`, `db`/`database`, `svc`/`service`, `gh`/`github`.
- **`app start` = deploy** — accepts `--force`, `--instant-deploy`.
- **Regenerate local command docs** — `go run ./coolify docs llms` in coolify-cli repo.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Setup and auth](references/setup-and-auth.md): a missing CLI, context setup, REST authentication, or MCP configuration.
- [Workflows](references/workflows.md): resource discovery, deployment, env changes, databases, services, backups, or infrastructure recipes.

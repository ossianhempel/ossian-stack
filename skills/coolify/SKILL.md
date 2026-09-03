---
name: coolify
description: >-
  Manage Coolify self-hosted PaaS instances via the coolify CLI and REST API.
  Deploy applications, databases, and one-click services; sync env vars; manage
  backups, domains, storage, servers, GitHub apps, teams, and deployments.
  Use when working with Coolify infrastructure, CI/CD, or the Coolify API.
  Triggers: deploy to coolify, coolify app, manage my coolify server, sync env
  vars to coolify, create a database on coolify, coolify backup, coolify MCP.
---

# Coolify CLI

Coolify is an open-source, self-hostable PaaS. The `coolify` CLI wraps the Coolify REST API (`/api/v1`) for terminal-based management.

**Two surfaces:**
- **v4 API CLI** (default) — talks to a running Coolify instance via API token.
- **v5 alpha** — `coolify init` and `coolify firewall` manage a WireGuard mesh / Podman control plane over SSH; no Coolify API. See [references/commands.md](references/commands.md#v5-alpha-control-plane).

For the full command tree, see [references/commands.md](references/commands.md). Upstream source of truth: [coolify-cli llms-full.txt](https://github.com/coollabsio/coolify-cli/blob/v4.x/llms-full.txt). OpenAPI: [openapi.json](https://github.com/coollabsio/coolify/blob/v4.x/openapi.json).

## Prerequisites

```bash
coolify version   # verify installed
```

Install if missing:

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# Homebrew
brew install coollabsio/coolify-cli/coolify-cli

# Go
go install github.com/coollabsio/coolify-cli/coolify@latest
```

Update: `coolify update`. Shell completion: `coolify completion bash|zsh|fish|powershell`.

## Configuration

Config: `~/.config/coolify/config.json` (Windows: `%APPDATA%\coolify\config.json`). Each **context** is a named Coolify instance (URL + API token).

### First-time setup

API tokens: Coolify dashboard → Security → API Tokens (`/security/api-tokens`).

```bash
# Coolify Cloud (predefined "cloud" context)
coolify context set-token cloud <api-token>

# Self-hosted
coolify context add prod -d
coolify context update prod --url https://coolify.example.com --token "$TOKEN"
coolify context verify
coolify context version    # instance version for this context
```

### Multiple environments

```bash
coolify context add staging
coolify context update staging --url https://staging.coolify.io --token "$TOKEN"
coolify context use production
coolify server list --context staging   # one-off without switching default
```

Override per command: `--context <name>`, `--token <token>`, or `--host <url>`.

## API auth (when calling REST directly)

Base URL: `https://<instance>/api/v1` (exceptions: `/api/health`, `/api/feedback`).

| Permission | Access |
|------------|--------|
| `read` | View resources |
| `read:sensitive` | View secrets, env vars, logs |
| `write` | Create/update/delete resources |
| `deploy` | Trigger deployments |
| `root` | Full access (enable/disable API, MCP) |

Tokens are team-scoped and rate-limited (default 200 req/min). Use `--show-sensitive` in CLI to reveal redacted fields. Docs: [API authorization](https://coolify.io/docs/api-reference/authorization).

```bash
curl -H "Authorization: Bearer $TOKEN" "https://coolify.example.com/api/v1/teams"
curl -X POST "https://coolify.example.com/api/v1/deploy?uuid=$APP_UUID&force=true" \
  -H "Authorization: Bearer $TOKEN"
```

**CLI vs API:** Prefer CLI when a command exists. Use REST for scheduled tasks, resource moves, tags, destinations, cloud tokens, and other API-only operations — see OpenAPI.

## MCP (AI agents)

Coolify exposes an MCP server at `https://<instance>/mcp` (Streamable HTTP). Enable with a `root` token: `POST /api/v1/mcp/enable`. Read-heavy resource discovery plus limited lifecycle (deploy/stop/restart) when the token has `deploy`. Docs: [MCP integration](https://coolify.io/docs/integrations/mcp).

## Common Workflows

### Discover resources

Most commands need UUIDs. Teams are the exception — they use **numeric IDs**.

```bash
coolify server list
coolify project list
coolify resource list                 # all apps, services, databases
coolify app list --format json
coolify server get <server-uuid> --resources
coolify server domains <server-uuid>
```

Use `--destination-uuid` on creates when a server has multiple destinations.

### Deploy an application

**Create** (pick one source type):

```bash
# Public git repo
coolify app create public \
  --server-uuid <server> --project-uuid <project> --environment-name production \
  --git-repository "https://github.com/user/repo" --git-branch main \
  --build-pack nixpacks --ports-exposes 3000

# GitHub App (after coolify github create)
coolify app create github \
  --server-uuid <server> --project-uuid <project> --environment-name production \
  --github-app-uuid <gh-app-uuid> --git-repository owner/repo --git-branch main \
  --build-pack nixpacks --ports-exposes 3000

# Deploy key + private repo
coolify app create deploy-key \
  --server-uuid <server> --project-uuid <project> --environment-name production \
  --private-key-uuid <key-uuid> --git-repository git@github.com:user/repo.git \
  --git-branch main --build-pack nixpacks --ports-exposes 3000

# Dockerfile or pre-built image
coolify app create dockerfile --server-uuid <server> --project-uuid <project> \
  --environment-name production --dockerfile "FROM node:20\n..." --ports-exposes 3000

coolify app create dockerimage --server-uuid <server> --project-uuid <project> \
  --environment-name production --docker-registry-image-name nginx:latest --ports-exposes 80
```

**Deploy / lifecycle:**

```bash
coolify deploy uuid <app-uuid> [--force] [--instant-deploy] [--docker-tag <tag>]
coolify deploy name <app-name> --force
coolify deploy batch api,worker,frontend --force
coolify deploy list
coolify deploy get <deployment-uuid>
coolify deploy cancel <deployment-uuid>

coolify app start <uuid> [--force] [--instant-deploy]   # alias: app deploy
coolify app stop|restart <uuid>
coolify app logs <uuid> [--follow] [-n 200] [--show-timestamps]
coolify app deployments list <uuid>
coolify app deployments logs <deployment-uuid> [--follow]
coolify app previews delete <uuid> <preview-id>
```

Preview deploys: `coolify deploy uuid <uuid> --pull-request-id <pr-number>`.

### Domains and SSL

App domains (Traefik/proxy handles SSL termination):

```bash
coolify app update <uuid> --domains "https://app.example.com,https://www.example.com"
```

Docker Compose apps: `--compose-domain` on `app update`. Server-level domain inventory: `coolify server domains <uuid>`. Database SSL modes are configured in the UI — [Database SSL docs](https://coolify.io/docs/databases/ssl).

### Environment variables

```bash
coolify app env list <app-uuid>
coolify app env get <app-uuid> <env-uuid-or-key>
coolify app env create <app-uuid> --key DATABASE_URL --value "postgres://..."
coolify app env update <app-uuid> <env-uuid-or-key> --value "new"
coolify app env delete <app-uuid> <env-uuid>
coolify app env sync <app-uuid> --file .env.production [--build-time] [--preview]
```

`env sync` diffs a local file against remote: updates changed keys, creates missing ones, **does not delete** remote-only vars. Same pattern exists for `database env` and `service env`.

Shared env vars (project/server/team scope): `coolify shared-env` — see command reference.

### Storage / volumes

```bash
coolify app storage list <app-uuid>
coolify app storage create <app-uuid> --type persistent --mount-path /data --name my-volume
coolify app storage create <app-uuid> --type file --mount-path /app/config.yml --content "key: value"
coolify app storage update|delete <app-uuid> <storage-uuid>
```

Database and service storage: `coolify database storage *`, `coolify service storage *`.

### Databases

```bash
coolify db create postgresql \
  --server-uuid <server> --project-uuid <project> --environment-name production \
  --postgres-user myuser --postgres-db mydb --instant-deploy
```

Types: `postgresql`, `mysql`, `mariadb`, `mongodb`, `redis`, `keydb`, `clickhouse`, `dragonfly`.

```bash
coolify db list|get|update|delete|start|stop|restart|logs <uuid>
coolify db env sync <uuid> --file .env.db
```

**Scheduled backups** (cron + optional S3):

```bash
coolify db backup list <db-uuid>
coolify db backup create <db-uuid> \
  --frequency "0 2 * * *" --enabled --save-s3 --retention-days-s3 30
coolify db backup trigger <db-uuid> <backup-uuid>
coolify db backup executions <db-uuid> <backup-uuid>
coolify db backup update|delete <db-uuid> <backup-uuid>
```

### One-click services

```bash
coolify service create --list-types
coolify service create <type> \
  --server-uuid <server> --project-uuid <project> --environment-name production \
  --instant-deploy
coolify service list|get|start|stop|restart|delete <uuid>
coolify service env sync <uuid> --file .env
coolify service logs <uuid> [--sub-service-name <name>]
```

### Servers, keys, GitHub apps

```bash
coolify server add --name prod --ip 203.0.113.1 --private-key-uuid <key-uuid>
coolify server validate|remove <uuid>
coolify server get <uuid> --resources

coolify private-key add my-key ~/.ssh/id_ed25519   # or paste key content
coolify private-key list
coolify private-key remove <uuid>

coolify github list|get|create|update|delete <uuid>
coolify github repos <github-app-uuid>
coolify github branches <github-app-uuid> --repo owner/repo
```

Cloud provisioning (Hetzner, DigitalOcean, Vultr): API + `coolify cloud-token` / `coolify server hetzner|digitalocean|vultr` — see command reference.

### Teams

```bash
coolify teams list
coolify teams get <team_id>          # numeric ID, not UUID
coolify teams current
coolify teams members list [team_id]
```

Each API token is scoped to the team active when it was created.

### CI/CD integration

```bash
APP_UUID=$(coolify app list --format json | jq -r '.[] | select(.name=="myapp") | .uuid')
coolify deploy uuid "$APP_UUID" --format json --force
```

Use a token with `read` + `deploy` for pipelines. `--format json` for all scripted output.

## Key Patterns

- **UUIDs everywhere** except teams (numeric IDs). Extract with `list --format json | jq`.
- **`--format json|pretty|table`** — prefer JSON in scripts.
- **`--show-sensitive` / `-s`** — reveal passwords, tokens, connection strings.
- **`--context`, `--token`, `--host`** — target instances without editing config.
- **Aliases** — `app`/`apps`, `db`/`database`, `svc`/`service`, `gh`/`github`.
- **`app start` = deploy** — accepts `--force`, `--instant-deploy`.
- **Regenerate local command docs** — `go run ./coolify docs llms` in coolify-cli repo.

# Setup And Auth

Read for a missing CLI, context setup, REST authentication, or MCP configuration. Follow the scope and safety contract in the skill entry point.

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

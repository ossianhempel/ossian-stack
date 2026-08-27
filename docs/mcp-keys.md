---
summary: Wiring RevenueCat and PostHog MCP servers with plain Bearer keys from 1Password into gitignored project config (no browser OAuth)
read_when:
  - Configuring revenuecat or posthog MCP servers in a project's .mcp.json or .codex/config.toml
  - A project MCP triggers a browser OAuth flow for RevenueCat or PostHog
  - Fetching the RevenueCat v2 secret key or PostHog project token from 1Password
---

# MCP keys: RevenueCat & PostHog

Agents wire these up themselves — never ask the user to connect via browser OAuth
or to paste keys. Both MCP servers accept a plain Bearer key in the gitignored
project config.

## Server configs

```json
{
  "mcpServers": {
    "revenuecat": {
      "type": "http",
      "url": "https://mcp.revenuecat.ai/mcp",
      "headers": { "Authorization": "Bearer sk_..." }
    },
    "posthog": {
      "type": "http",
      "url": "https://mcp.posthog.com/mcp",
      "headers": { "Authorization": "Bearer phc_..." }
    }
  }
}
```

- RevenueCat uses the **API v2 secret key** (`sk_…`, ~32 chars).
- PostHog uses the **project API token** (`phc_…`, ~48 chars). Works for the MCP
  (no personal `phx_` key needed).
- Same shape for `.codex/config.toml`:
  `type = "http"`, `url = "..."`, `headers = { Authorization = "Bearer <key>" }`.

## Finding the key (1Password)

List titles in the Development vault (metadata only):

```bash
op item list --vault Development --format json   # titles, never values
```

Convention — `op://Development/<Item>/<field>`:

| App | RevenueCat (v2 secret `sk_…`) | PostHog (project token `phc_…`) |
|-----|-------------------------------|---------------------------------|
| GainsLog | `RevenueCat - GainsLog/credential` | `PostHog - GainsLog/credential` |
| PlateSnap | `RevenueCat - PlateSnap/credential` | — (not stored) |
| Middagsro | `RevenueCat - Middagsro/credential` | `Middagsro Production Configuration/posthog_project_token` |
| TopOfClass | `RevenueCat - TopOfClass/credential` | — (not stored) |

Per-app config items may also carry `revenuecat_api_key` /
`posthog_project_token` fields (e.g. `Middagsro Production Configuration`).

Read a key without printing it:

```bash
op read "op://Development/RevenueCat - <App>/credential"
```

If an app has no key stored, **omit the server entirely** from `.mcp.json` —
do not fall back to `mcp-remote` OAuth. Store the key first
(`op item create --vault Development --category "API Credential" --title "RevenueCat - <App>" "credential[password]=…"`).

## Where to write

The config files are gitignored and must stay that way (they hold plain secrets):

- `.mcp.json` at the project root
- `.codex/config.toml` (if present) — same servers in `[mcp_servers.*]` form

Both are already gitignored in every project that uses them. Never commit them.
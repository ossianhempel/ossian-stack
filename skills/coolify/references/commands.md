# Coolify CLI Command Reference

Curated reference. **Authoritative upstream catalog:**
https://github.com/coollabsio/coolify-cli/blob/v4.x/llms-full.txt

Regenerate from source: `go run ./coolify docs llms` in [coollabsio/coolify-cli](https://github.com/coollabsio/coolify-cli).

**REST API:** https://github.com/coollabsio/coolify/blob/v4.x/openapi.json  
**Auth docs:** https://coolify.io/docs/api-reference/authorization

## Global Flags

| Flag | Description |
|------|-------------|
| `--context` | Use a specific context by name |
| `--token` | Override context token for this command |
| `--host` | Override instance URL |
| `--format` | `table` (default), `json`, `pretty` |
| `--show-sensitive`, `-s` | Show sensitive values (tokens, passwords) |
| `--debug` | Enable debug output |
| `-f`, `--force` | Force (context overwrite, deploy, cancel confirm skip) |

## Utility

```
coolify version
coolify update
coolify config
coolify completion bash|zsh|fish|powershell
```

## context — Manage Coolify instances

```
coolify context add <name> [-d] [--force]     # then set url/token via update
coolify context update <name> [--url] [--token] [--name]
coolify context set-token <name> <token>        # e.g. cloud <token>
coolify context list|get|use|delete|set-default|verify|version
```

Self-hosted bootstrap:

```bash
coolify context add prod -d
coolify context update prod --url https://coolify.example.com --token "$TOKEN"
coolify context verify
```

## app (aliases: apps, application, applications)

```
coolify app list|get|update|delete
coolify app start|stop|restart <uuid> [--force] [--instant-deploy]
coolify app logs <uuid> [--follow] [-n lines] [--show-timestamps] [--service]
coolify app deployments list <uuid>
coolify app deployments logs <deployment-uuid> [--follow] [-n] [--debuglogs]
coolify app previews delete <uuid> <preview-id>
```

Notable `app update` flags: `--domains`, `--compose-domain`, `--git-repository`, `--git-branch`, `--docker-image`, `--docker-tag`, `--build-command`, `--start-command`, `--health-check-*`.

### app create

```
coolify app create public|github|deploy-key|dockerfile|dockerimage ...
```

Common flags: `--server-uuid`, `--project-uuid`, `--environment-name`, `--destination-uuid`, `--ports-exposes`, `--build-pack`, `--instant-deploy`.

### app env (aliases: envs, environment)

```
coolify app env list <app-uuid>
coolify app env get <app-uuid> <env-uuid-or-key>
coolify app env create <app-uuid> --key <KEY> --value <VALUE> [--is-build-time] [--is-preview]
coolify app env update <app-uuid> <env-uuid-or-key> [--key] [--value] [--is-build-time] [--is-preview]
coolify app env delete <app-uuid> <env-uuid>
coolify app env sync <app-uuid> --file <.env> [--build-time] [--preview]
```

### app storage (aliases: storages)

```
coolify app storage list|create|update|delete <app-uuid> [storage-uuid]
```

Types: `persistent` (volume), `file` (inline content).

## database (aliases: databases, db, dbs)

```
coolify db list|get|update|delete|start|stop|restart|logs <uuid>
```

Types for `db create`: `postgresql`, `mysql`, `mariadb`, `mongodb`, `redis`, `keydb`, `clickhouse`, `dragonfly`.

### db env / storage

```
coolify db env list|get|create|update|delete|sync <db-uuid> ...
coolify db storage list|create|update|delete <db-uuid> ...
```

### db backup

```
coolify db backup list <db-uuid>
coolify db backup create <db-uuid> [--frequency cron] [--enabled] [--save-s3] [--retention-days-s3 N] ...
coolify db backup update|delete <db-uuid> <backup-uuid>
coolify db backup trigger <db-uuid> <backup-uuid>
coolify db backup executions <db-uuid> <backup-uuid>
coolify db backup delete-execution <db-uuid> <backup-uuid> <execution-uuid>
```

## service (aliases: services, svc)

```
coolify service list|get|create|delete|start|stop|restart
coolify service create --list-types
coolify service create <type> --server-uuid ... --project-uuid ... [--instant-deploy]
coolify service env list|get|create|update|delete|sync <svc-uuid> ...
coolify service storage list|create|update|delete <svc-uuid> ...
coolify service logs <uuid> [--sub-service-name <name>] [--follow]
```

## deploy

```
coolify deploy uuid <resource-uuid> [--force] [--docker-tag] [--pull-request-id]
coolify deploy name <resource-name> [--force] [--docker-tag] [--pull-request-id]
coolify deploy batch <name1,name2,...> [--force] [--docker-tag] [--pull-request-id]
coolify deploy list|get <deployment-uuid>|cancel <deployment-uuid> [--force]
```

## server (aliases: servers)

```
coolify server list|get|add|remove|validate
coolify server get <uuid> --resources
coolify server domains <uuid>
coolify server add --name <name> --ip <ip> --private-key-uuid <uuid>
```

Cloud server create (requires cloud tokens): `coolify server hetzner|digitalocean|vultr|...`

## project (aliases: projects)

```
coolify project list|get|create
```

## resource (aliases: resources)

```
coolify resource list
```

## destination (aliases: destinations)

```
coolify destination list|get|create|update|delete
```

## github (aliases: gh, github-app, github-apps)

```
coolify github list|get|create|update|delete <uuid>
coolify github repos <github-app-uuid>
coolify github branches <github-app-uuid> --repo owner/repo
```

## gitlab (aliases: gl, gitlab-app, gitlab-apps)

```
coolify gitlab list|get|create|update|delete <app-id-or-uuid>
```

## private-key (aliases: private-keys, key, keys)

```
coolify private-key list
coolify private-key add <name> <private-key-or-file-path>
coolify private-key remove <uuid>
```

## teams (aliases: team)

```
coolify teams list
coolify teams get <team_id>              # numeric ID, not UUID
coolify teams current                    # alias: teams me
coolify teams members list [team_id]
```

## tag (aliases: tags)

```
coolify tag list|create|update|delete
```

Resource-level tags: `coolify app tag add|remove`, `coolify database tag *`, `coolify service tag *`.

## cloud-token (aliases: cloud-tokens)

```
coolify cloud-token list|get|create|update|delete|validate <uuid>
```

Used with Hetzner/DigitalOcean/Vultr server provisioning.

## shared-env (aliases: shared-envs, sharedenv)

Shared variables at project, server, environment, or team scope:

```
coolify shared-env project|server|environment|team list|create|update|delete ...
```

## s3 (aliases: s3-storage, s3-storages)

```
coolify s3 list|get|create|update|delete|validate
```

Backup destination storage for database backup schedules.

## notification (aliases: notifications)

```
coolify notification get|update
```

## cloud-init (aliases: cloudinit, cloud-init-script)

```
coolify cloud-init list|get|create|update|delete
```

## v5 alpha control plane

SSH-based; **no Coolify API**. Separate from v4 instance management.

```
coolify init plan|bootstrap|extend|upgrade
coolify firewall allow|list|revoke|containers
```

See [CONTROL_PLANE.md](https://github.com/coollabsio/coolify-cli/blob/v4.x/CONTROL_PLANE.md).

## API-only (no CLI command yet)

Use REST (`/api/v1/...`) or MCP when CLI lacks coverage:

- Application/database/service **scheduled tasks** — `POST .../scheduled-tasks`
- Resource **move** between projects/servers — `POST .../{uuid}/move`
- **Enable/disable API and MCP** — `POST /enable`, `/disable`, `/mcp/enable`, `/mcp/disable` (root token)
- **Deploy webhook** — `POST /deploy?uuid=&tag=&force=&pr=`

MCP endpoint: `https://<instance>/mcp` — https://coolify.io/docs/integrations/mcp

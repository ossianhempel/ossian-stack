---
name: post-queue-cli
description: "Operate the Post Queue command surfaces effectively. Use for the postq CLI, local Next.js and Convex development, production-safe reads, Convex deployment inspection, tests, lint, typecheck, builds, and scheduler verification."
---

# Post Queue CLI

## Purpose

Use this skill to choose and run the right repo command without rediscovering the scripts in `package.json`.

Post Queue has two command surfaces:

- `postq`, the user-workflow CLI at `src/cli/postq.ts` (exposed as the `postq` bin and the `npm run postq` script). It talks to the app over HTTP with a Personal API Token and never touches the database directly.
- The package scripts for Next.js development, Convex development/codegen, verification, and builds.

Read `docs/postq-cli.md` before using `postq`.

## First Steps

1. Work from the repo root: `/Users/ossianhempel/Developer/post-queue`.
2. Read `AGENTS.md` before changing code.
3. Run `pnpm run docs:list` when starting substantive work, then read the docs whose topic matches the task.
4. Check current scripts before relying on this skill if `package.json` changed recently:
   ```bash
   node -e "const p=require('./package.json'); console.log(JSON.stringify(p.scripts,null,2))"
   ```

## Secrets

Use the 1Password item `op://Development/Post Queue/...` for PostQueue secrets. The item should be tagged `repo:post-queue`, `project:post-queue`, and `environment:production` so agents do not confuse it with other repo secrets.

Recommended sections/fields:

- `PostQueue production`: `APP_URL`, provider OAuth credentials and redirects, UploadThing credentials, Clerk credentials, `TOKEN_ENCRYPTION_KEY`, `TOKEN_ENCRYPTION_MODE`, `IDENTITY_HASH_PEPPER`, and `CONVEX_SERVER_ADAPTER_SECRET`.
- `PostQueue local dev`: local-only values such as `DEV_SEED_CLERK_ID`.

Production data and scheduling are owned by Convex. OAuth tokens are encrypted in the Next.js server runtime before storage; keep `TOKEN_ENCRYPTION_MODE=strict` and never expose the encryption key to client components.

## Command Map

### postq User CLI

`postq` runs signed-in user workflows against the HTTP API. Configure it before use:

```bash
export POSTQUEUE_API_URL=https://postqueue.social
export POSTQUEUE_API_TOKEN="$(op read 'op://Development/Post Queue/postq-token')"
```

Post Queue runs in production at `https://postqueue.social`. Target that unless a local dev server is deliberately running.

Precedence is flags (`--api-url`, `--token`), then env, then `.postqrc.json`, then `~/.config/postq/config.json`, then `http://localhost:3000`. That last default is a dev-only fallback; if a command fails with connection refused on localhost, the URL is the bug. Never pass a token inline in a command an agent logs.

Read-only inspection:

```bash
pnpm --silent postq -- auth status --json
pnpm --silent postq -- accounts list --json
pnpm --silent postq -- media list --json
pnpm --silent postq -- drafts list --json
pnpm --silent postq -- posts list --status queued --json
pnpm --silent postq -- posts recent --range 24h --json
pnpm --silent postq -- posts recent --range 7d --status failed --json
pnpm --silent postq -- posts scheduled --limit 25 --json
pnpm --silent postq -- posts show <postId> --json
pnpm --silent postq -- metrics list --json
```

`posts scheduled` is the queue view: every post the scheduler still owes work to, oldest scheduled time first. It returns posts whose targets are `queued`, `uploading`, or `publishing`, with provider, account, format, target status, `scheduledFor`, `nextAttemptAt`, and attempt counts nested per post. `--limit` (default 50, max 200) caps posts, not targets, so a multi-account post is never half-listed. Backed by `GET /api/cli/scheduled-posts`.

Use `posts list --status queued` when only post-level rows matter, and `targets retry-failed` / `targets reschedule-failed` for the failed side of the queue.

`posts recent` is the read-only delivery check. It defaults to the last `24h`;
use duration ranges such as `1h`, `7d`, or `30d`, plus `--status successful`
or `--status failed` when only one outcome is needed. It returns unique posts,
counts, and matching per-target outcomes from `GET /api/cli/posts/recent`.

Mutations require `--yes` (and reach real platforms when the API URL is production):

```bash
pnpm --silent postq -- posts create --title "Launch" --caption "Ready" --media <mediaAssetId>
pnpm --silent postq -- posts schedule <postId> --from schedule.json --yes
pnpm --silent postq -- posts cancel <postId> --yes
pnpm --silent postq -- targets retry <targetId> --yes
pnpm --silent postq -- targets reschedule <targetId> --at 2026-08-01T08:00:00Z --yes
pnpm --silent postq -- media delete <mediaAssetId> --yes [--force]
```

Use `--from -` for payloads with multiline captions or shell-sensitive text, and `--dry-run` with `posts schedule` to run server-side compliance checks without scheduling.

`media delete` refuses with a 409 when the asset is attached to a post, listing
the posts in `error.details`. That guard is not a formality: the delete is a
**soft** delete (`status: "deleted"`, `deletedAt` set), so the `post_media`
foreign-key cascade never fires. Deleting an attached asset leaves the join row
pointing at bytes that are gone from UploadThing, which surfaces as a publish
failure days later rather than an error now. `--force` overrides it; reach for
`posts cancel` first unless you genuinely intend to orphan the post.

A batch upload that fails partway leaves orphans, and `media list` gives no way
to tell which set an orphan belongs to: `metadata.originalName` is only the bare
filename (`slide_01.jpg`), identical across every set. Match on `sizeBytes`
against the local files, or upload with distinct filenames in the first place.

When adding a user-facing action, add it to both the HTTP route under `src/app/api/cli/**` and `src/cli/postq.ts`, then document it in `docs/postq-cli.md` and here. AGENTS.md requires CLI/API parity for anything a human can do in the app.

### Local App

- Start the normal HTTPS dev server:
  ```bash
  pnpm run dev
  ```
- Start an HTTP dev server:
  ```bash
  pnpm run dev:http
  ```
- Run the configured Convex development deployment and regenerate types:
  ```bash
  pnpm run convex:dev
  ```

Convex scheduled functions and crons own publishing. Local Next.js development does not require a local database container or an app-side scheduler loop.

### Verification

- Typecheck after significant TypeScript changes:
  ```bash
  pnpm run typecheck
  ```
- Lint:
  ```bash
  pnpm run lint
  ```
- Unit/integration test suite:
  ```bash
  pnpm test
  ```
- Convex function and scheduler tests:
  ```bash
  pnpm run test:convex
  ```
- Production build:
  ```bash
  pnpm run build
  ```
- Legacy-runtime absence check:
  ```bash
  pnpm run verify:no-postgres
  ```

Prefer the narrowest meaningful check while iterating. Before commits or broad changes, run the relevant full gate, usually typecheck, lint, affected tests, the Convex suite, and the production build.

### Scheduler

Read these before scheduler changes or ops:

- `docs/scheduler/overview.md`
- `docs/scheduler/how-the-scheduler-runs.md`
- `convex/publishing.ts`
- `convex/publishingActions.ts`
- `convex/crons.ts`

Scheduling persists an immutable execution identity and generation before calling `ctx.scheduler.runAt`. The due mutation revalidates control state, target generation, account status, and connection generation. Provider actions obtain a mutation-issued call permit immediately before external I/O, and reconciliation crons recover only from persisted provider evidence.

Use `convex-test` with fake provider mode for deterministic local proof. Do not add an app-side polling endpoint, worker, or alternate scheduler.

## Common Workflows

### Make a Convex Schema Change

1. Edit `convex/schema.ts` and the owning Convex domain functions.
2. Regenerate types:
   ```bash
   pnpm run convex:codegen
   ```
3. Run the Convex tests and typecheck:
   ```bash
   pnpm run test:convex
   pnpm run typecheck
   ```

## Safety Rules

- Never print `.env.local`, OAuth secrets, personal API tokens, Convex deploy keys, server-adapter secrets, or token-encryption keys.
- Target production Convex operations with the exact deployment name and perform read-before-write checks.
- Treat production scheduler mutations as potentially publishing real queued content.
- Commit Convex generated types after schema or function changes.
- If command output references account tokens, OAuth payloads, or provider responses, summarize safely and redact sensitive fields.

## Troubleshooting Pointers

- Convex generated types are stale: run `pnpm run convex:codegen` against the intended development deployment.
- A queued target is not running: inspect its generation, scheduled invocation, account/connection state, publishing control, and reconciliation logs.
- A provider result is ambiguous: preserve acceptance evidence and use account recovery/operator review; do not issue an unclassified retry.

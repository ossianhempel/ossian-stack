---
name: one-password
description: "Fetch secrets and env vars from 1Password with the `op` CLI, using a service account or Touch ID. Use whenever a command needs an API key, token, password, or `.env` value. Triggers: op read/run/inject, op://, 1Password, fetch secret, inject env vars."
metadata: {"requires":{"bins":["op"]},"install":[{"id":"brew","kind":"brew","formula":"1password-cli","bins":["op"],"label":"Install 1Password CLI (brew)"}]}
---

# 1Password CLI (`op`)

Fetch secrets and environment variables from 1Password so commands run with real
credentials without hardcoding them, printing them, or asking the user to paste.

## Auth model (Ossian's Mac)

**Primary — service account (no human in the loop).** A service-account token is
exported as `OP_SERVICE_ACCOUNT_TOKEN` in `~/.zshenv`, so every shell (including
non-interactive agent shells) can run `op` with **no Touch ID prompt**. The token
is scoped to **`Development`, `H&M`, and `Rebtech`** — that is the blast radius if
it leaks. It has `read_items` and `write_items` in each vault so agents can both
retrieve and maintain secrets without a manual 1Password handoff.

- Default account: `my.1password.com`.
- Service account name: `mac-mini-agents-multi`.
- The service account can **read and write items** in `Development`, `H&M`, and
  `Rebtech`. It cannot see `Personal` (built-in vault; service accounts cannot
  access it).
- Multi-vault auth: the vault is in the `op://` ref for `op read`; for
  `op item get`/`op item list`/`op item create`/`op item edit` always pass
  `--vault <name>` (quote `"H&M"` in the shell). `H&M` cannot appear in an
  `op://` ref at all — use its UUID `jppnx6odwrvy62mr2brqap552y` (see below).
- Service-account writes should stay vault-scoped and intentional: use existing app/repo
  items when possible, add clear repo tags/sections, and inspect the target item
  structure before broad rewrites.

**Fallback — Touch ID (interactive).** To reach `Personal` (or any vault outside
the service account's scope), unset the token for that one command so `op` uses
desktop app integration and prompts Touch ID:

```bash
env -u OP_SERVICE_ACCOUNT_TOKEN op read "op://Personal/SomeItem/field"
```

This requires the user present to approve — use it only when the secret genuinely
isn't (and can't be) in `Development`.

## Core operations

Reference syntax is `op://<vault>/<item>/<field>`. Pick the vault that owns the
secret: `Development` for personal/agent projects, `H&M` or `Rebtech` for work.

**`H&M` cannot be named in an `op://` ref.** `&` is not a legal character in a
secret reference, so `op read "op://H&M/Item/field"` fails with
`invalid character in secret reference: '&'` — this is a parse error, not an auth
error, and no amount of shell quoting fixes it. Use the vault UUID instead:

```bash
op read "op://jppnx6odwrvy62mr2brqap552y/ATLASSIAN_API_TOKEN/username"   # H&M by UUID
op vault list --format json                                              # look up UUIDs
```

Or bypass references entirely with the item API, which takes the name directly:

```bash
op item get "ATLASSIAN_API_TOKEN" --vault "H&M" --fields credential --reveal
```

`--reveal` is required for concealed fields, otherwise the value comes back masked.

### Read one secret

```bash
op read "op://Development/OpenAI/api_key"
```

Inline for a single command so the value never lands in a variable or log:

```bash
OPENAI_API_KEY="$(op read 'op://Development/OpenAI/api_key')" some-tool --run
```

### Run a command with secrets injected (preferred for many vars)

Keep a `.env` of `op://` references (safe to commit — they're pointers, not values):

```bash
# .env
OPENAI_API_KEY=op://Development/OpenAI/api_key
DATABASE_URL=op://Development/AppDB/connection_string
```

```bash
op run --env-file=.env -- npm run dev
```

`op` resolves every `op://` ref into the child process's environment and nowhere else.

### Inject secrets into a config template

```bash
echo "db_password: {{ op://Development/AppDB/password }}" | op inject
op inject -i config.tpl.yml -o config.yml      # render a whole file
```

### Special field attributes

```bash
op read "op://Development/SomeItem/one-time password?attribute=otp"   # TOTP code
op read "op://Development/server/private key?ssh-format=openssh"      # SSH key
op read --out-file ./key.pem "op://Development/server/ssh/key.pem"    # write to file
```

## Adding a new secret for agents to use

Pick the owning vault (`Development`, `H&M`, or `Rebtech`). Use repo-specific
item names, tags, and sections so secrets do not get mixed across projects:

```bash
op item create --vault Development \
  --category "API Credential" --title "Some Service" \
  --tags "repo:some-repo,project:some-project" \
  "api_key[password]=…"
```

Then agents read it non-interactively via `op read "op://Development/Some Service/api_key"`.

For sensitive values, prefer JSON templates or `op run`/`op inject` over command-line
assignment statements so secrets do not appear in process arguments. For `Personal`,
unset the service account token and use the Touch ID fallback.

## Finding the right reference

Prefer asking the user for the exact `op://` path, or copy it from the app
(right-click a field → "Copy Secret Reference"). If you must discover it, stay
metadata-only and vault-scoped — list titles, never field values:

```bash
op item list --vault Development --format json        # titles/ids/categories only
op item get "OpenAI" --vault Development --format json # inspect field LABELS, not values
```

Do not enumerate other vaults by default. Search only when the user asks.

## Guardrails

- **Never print or log secret values or the token.** No `echo $TOKEN`, no `set -x`
  around `op`, no `cat` of rendered output. To sanity-check a read, print shape
  only (length, prefix), never the value.
- **Prefer `op run` / `op inject`** over writing secrets to disk. If a file is
  unavoidable (`--out-file`), delete it as soon as the command that needs it is done.
- **No broad enumeration.** Don't run `env`, `export -p`, or list every vault to
  "find" a secret — query the exact item/field in the vault that owns it.
- Use the Touch ID fallback deliberately for `Personal` only.
- If `op read` returns the wrong field (items with duplicate/legacy fields), read
  the item as JSON and pick the exact label rather than guessing.

## Operations

- Token lives in `~/.zshenv` (`OP_SERVICE_ACCOUNT_TOKEN`). Scoped to `Development`,
  `H&M`, and `Rebtech` with `read_items` and `write_items` in each.
- Rate limits: `op service-account ratelimit` shows usage if reads start failing.
- Rotate/replace: vault access is immutable — create a new service account with
  `env -u OP_SERVICE_ACCOUNT_TOKEN op service-account create <name> \
  --vault Development:read_items,write_items \
  --vault "H&M:read_items,write_items" \
  --vault Rebtech:read_items,write_items --raw`, update `~/.zshenv` and the
  credential item. Delete the old account in the 1Password web UI (CLI has no delete).

## Service Account Credential

The service-account token itself is stored in
`op://Development/1Password Service Account — mac-mini-agents/credential`. That
item should be tagged `tool:1password`, `service-account`, `mac-mini-agents`,
`vault:development`, `vault:hm`, `vault:rebtech`, and `permission:read-write`. If
the token is rotated, update
both that 1Password item and `~/.zshenv`, then verify `op item edit` works without
unsetting `OP_SERVICE_ACCOUNT_TOKEN`.

## Service-specific credentials

Keep service-specific auth (which item, which fields) in the owning skill or the
project's `.env` of `op://` refs. This skill owns only the generic rules:
service-account-first, targeted reads, no enumeration, never print values.

RevenueCat (`sk_…`, `RevenueCat - <App>/credential`) and PostHog (`phc_…`,
`PostHog - <App>/credential`) MCP keys follow the convention in
`~/Developer/ossian-stack/docs/mcp-keys.md` — agents wire those MCP servers
into gitignored project config themselves, never via browser OAuth.

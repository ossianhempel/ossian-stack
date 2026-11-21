---
name: one-password
description: "Retrieve missing secrets and environment values securely with the 1Password op CLI. Use before asking the user for any credential: an auth or push failure, or a missing token, PAT, API key or deploy key. Use existing secure authentication when it already meets the task."
metadata: {"requires":{"bins":["op"]},"install":[{"id":"brew","kind":"brew","formula":"1password-cli","bins":["op"],"label":"Install 1Password CLI (brew)"}]}
---

# 1Password CLI (`op`)

Fetch secrets and environment variables from 1Password so commands run with real
credentials without hardcoding them, printing them, or asking the user to paste.

## Auth model (Ossian's Mac)

**Primary, service account (no human in the loop).** A service-account token is
exported as `OP_SERVICE_ACCOUNT_TOKEN` in `~/.zshenv`, so every shell (including
non-interactive agent shells) can run `op` with **no Touch ID prompt**. The token
is scoped to **`Development`, `H&M`, and `Rebtech`**, that is the blast radius if
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
  `op://` ref at all, use its UUID `jppnx6odwrvy62mr2brqap552y` (see below).
- Service-account writes should stay vault-scoped and intentional: use existing app/repo
  items when possible, add clear repo tags/sections, and inspect the target item
  structure before broad rewrites.

**Fallback, Touch ID (interactive).** To reach `Personal` (or any vault outside
the service account's scope), unset the token for that one command so `op` uses
desktop app integration and prompts Touch ID:

```bash
env -u OP_SERVICE_ACCOUNT_TOKEN SERVICE_TOKEN='op://Personal/SomeItem/field' \
  op run -- some-tool
```

This requires the user present to approve, use it only when the secret genuinely
isn't (and can't be) in `Development`.

## Core operations

Reference syntax is `op://<vault>/<item>/<field>`. Pick the vault that owns the
secret: `Development` for personal/agent projects, `H&M` or `Rebtech` for work.

The `H&M` vault uses its UUID in a secret reference because the reference
parser rejects `&`. Item metadata commands accept the vault name directly.

```bash
SERVICE_TOKEN='op://jppnx6odwrvy62mr2brqap552y/SomeItem/credential' op run -- some-tool
```

### Run a command with secrets injected

Pass references in the environment. Choose a command that consumes the secret
without printing it.

```bash
OPENAI_API_KEY='op://Development/OpenAI/api_key' op run -- some-tool
```

For several variables, use a local env file containing references:

```dotenv
OPENAI_API_KEY=op://Development/OpenAI/api_key
DATABASE_URL=op://Development/AppDB/connection_string
```

```bash
op run --env-file=.env -- npm run dev
```

### Write a private file only when the consumer needs one

Use paths within a task-owned directory with mode `0700`. Set `umask 077`,
keep rendered files out of the checkout, and remove them after use, including
after failure.

```bash
op inject -i config.tpl.yml -o "$PRIVATE_CONFIG_PATH" --file-mode 0600
op read --out-file "$PRIVATE_KEY_PATH" --file-mode 0600 'op://Development/server/private key?ssh-format=openssh'
```

For a one-time password, use the reference's `?attribute=otp` with a consumer
that can receive the code securely.

## Adding a new secret for agents to use

Pick the owning vault (`Development`, `H&M`, or `Rebtech`). Use repo-specific
names, tags, and sections. If authorized to create the item, pass its fields
through a private JSON template and discard the command's stdout. Remove the
private template when finished.

```bash
op item create --vault Development \
  --category "API Credential" --title "Some Service" \
  --tags "repo:some-repo,project:some-project" \
  --template "$PRIVATE_ITEM_TEMPLATE" >/dev/null
```

## Finding the right reference

Use the supplied reference or a reference copied from the app. For authorized
vault-scoped discovery, list item titles and IDs. Project item details to field
IDs, labels, and section IDs before returning any output. If a projection tool
is unavailable, use the exact reference or ask for it.

```bash
op item list --vault Development --format json | jq '[.[] | {id, title}]'
op item get "OpenAI" --vault Development --format json |
  jq '[.fields[] | {id, label, section: .section.id}]'
```

When field names are duplicated, use the matching section and field IDs to
resolve the reference. Agents use the `op` CLI. The desktop app handles any
interactive approval.

## Guardrails

- Keep secret values, prefixes, and service-account tokens out of tool output,
  logs, shell traces, and process arguments. Verify success through the consumer
  or report only whether a value is present.
- Use the exact owning vault. Keep discovery limited to the user's requested
  item or vault.
- Use Touch ID for credentials outside the service account's scope through the
  fallback above.

## Operations

- Token lives in `~/.zshenv` (`OP_SERVICE_ACCOUNT_TOKEN`). Scoped to `Development`,
  `H&M`, and `Rebtech` with `read_items` and `write_items` in each.
- Rate limits: `op service-account ratelimit` shows usage if reads start failing.
- Vault access is immutable. For an authorized rotation, create the replacement
  from a desktop-authenticated session and redirect the raw token to a private
  file under the same file-handling rules above.

```bash
env -u OP_SERVICE_ACCOUNT_TOKEN op service-account create "$ACCOUNT_NAME" \
  --vault Development:read_items,write_items \
  --vault "H&M:read_items,write_items" \
  --vault Rebtech:read_items,write_items --raw >"$PRIVATE_TOKEN_PATH"
```

Update `~/.zshenv` and the credential item through secure inputs and verify
that the replacement works before retiring the old account in the 1Password web UI.

## Service Account Credential

The service-account token itself is stored in
`op://Development/1Password Service Account, mac-mini-agents/credential`. That
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
`~/Developer/ossian-stack/docs/mcp-keys.md`, agents wire those MCP servers
into gitignored project config themselves, never via browser OAuth.

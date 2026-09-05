# Execution And Auth

Read for binary selection, action-time authentication, project linking, or sandbox-related failures. Follow the scope and safety contract in the skill entry point.

## Execution environment (prefer the host, understand the sandbox warning)

Most AI coding agents default to running shell commands in a sandbox where the
user's home directory, OS keychain, browser launch, localhost callback
binding, or network access may be blocked. The Clerk CLI depends on all of
those host capabilities:

- **OS credential store**: `clerk auth login` stores the OAuth token in the
  system keychain. A sandbox without keychain access reports "not logged in"
  even when the host is authenticated.
- **Home-directory Clerk state**: saved config, cached metadata, and fallback
  credentials live under the user's Clerk config/data directories.
- **Linked project metadata**: resolved from the repo's git remote plus Clerk
  config. Sandboxes with stripped repo state or blocked home-dir reads can
  misreport "not linked".
- **Local `.env*` files**: publishable and secret keys materialized by
  `clerk env pull`.
- **Outbound network access to Clerk**: every Backend and Platform API call.
- **Browser + localhost OAuth callback**: `clerk auth login` needs both.

In agent mode, the CLI now does a **best-effort warn-once check** at the
host-sensitive library boundaries. When it detects that host-only Clerk state
or system capabilities are unavailable, it emits:

```text
Host-only Clerk state or system capabilities may be unavailable in agent mode. This may be a sandboxed run.
Re-run this command on the host shell before trusting auth, link, env, or API failures.
```

Treat that warning as authoritative. The command may continue, but any auth,
link, env, config, API, browser, or OAuth callback failure from that
invocation is untrusted until you rerun the same command on the host.

**Prefer these commands on the user's host shell, not in a sandbox:**

`clerk doctor`, `clerk whoami`, `clerk auth login`, `clerk link`, `clerk env pull`,
`clerk apps ...`, `clerk config ...`, `clerk api ...`.

If a command was accidentally run in a sandbox and it reports `Not logged in`,
`auth_required`, `not linked`, missing env, keychain/file permission errors,
or network failures, **do not treat the result as authoritative**. Rerun it on
the host before acting on it or reporting it to the user.
## Invoking the CLI

Before running any `clerk` command, figure out which binary to invoke and bind that choice for the rest of the session:

```sh
# 1. Prefer a globally installed binary when it matches the skill's target version.
command -v clerk >/dev/null 2>&1 && clerk --version
```

If that prints `latest` or any version you trust, use bare `clerk` for the rest of the session.

Otherwise fall back to a package runner, in this order (matches the CLI's own `preferredRunner` logic, which prefers the runner that matches the project's lockfile):

| Project package manager   | Invocation                       |
| ------------------------- | -------------------------------- |
| bun (`bun.lock*`)         | `bunx clerk@latest`     |
| npm (`package-lock.json`) | `npx -y clerk@latest`   |
| pnpm (`pnpm-lock.yaml`)   | `pnpm dlx clerk@latest` |
| yarn >= 2 (`yarn.lock`)   | `yarn dlx clerk@latest` |

Yarn Classic (v1) has no `dlx`; treat those projects as "no preferred runner" and fall back to the first runner from the list above that's on PATH.

The published npm package is **`clerk`**, not `@clerk/cli`. Never teach `npm install -g clerk` as the primary path. If the global CLI is stale or behaves differently from this skill, either upgrade the global install or fall back to the `latest` runner form above.

Keep the selected invocation for the rest of the session. Every later example that
starts with bare `clerk` means that exact bound invocation; do not silently switch
back to a missing global binary.
## Prerequisites (run at session start)

Before running any other Clerk command in a session, verify the CLI is authenticated, linked, and healthy:

```sh
<selected-clerk-invocation> --version
<selected-clerk-invocation> doctor --json
```

**Always run `doctor --json` through the selected invocation first.** It catches the common setup failures (not logged in, project not linked, missing keys, stale CLI version) up front, so later commands don't fail with confusing errors. In agent mode it also includes a `Host execution` check that warns when Clerk's host-side config / credential directories are not writable, which is the canonical signal that the current invocation is likely sandboxed.

Each result has `name`, `status` (`pass`/`warn`/`fail`), `message`, optional `detail`, optional `remedy` (how to fix it), and optional `fix` (label for auto-fixable issues). Parse that and act on it, or surface it to the user. If `Host execution` warns, rerun the command on the host before trusting any auth/link/env/API failures from the same sandboxed run. Rerun `clerk doctor --json` whenever a later command starts misbehaving.

If the selected invocation reports a newer CLI than this skill covers, trust its
`<command> --help` first and refresh this skill bundle from its source.

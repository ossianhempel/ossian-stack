---
name: hetzner-vm
description: "Read container logs, status, and resource usage on the Hetzner VM that hosts Coolify and its deployed apps. Use when diagnosing a deployed service — a container that is restarting, unhealthy, exited, or failing to start; a self-hosted GitHub Actions runner that will not register; disk or memory pressure on the host. Access is deliberately read-only. Triggers: hetzner, the VM, the server, container logs, docker logs, why is X restarting, is the runner up, coolify container, deployed app logs."
---

# Hetzner VM access

The Hetzner VM runs Coolify and every app deployed through it — the apps, their databases, and the self-hosted GitHub Actions runners. Its IP address is a credential-adjacent fact, so it is not written down here: it lives in 1Password as `op://Development/Hetzner VM/ip` (see the `one-password` skill). Day-to-day access never needs it — connections go through the `hetzner-agent` SSH alias below.

Agents reach it through a **restricted, read-only account**. Use it to answer "what is this container doing?" without touching anything.

## Connect

```bash
ssh hetzner-agent "<verb>"
```

`hetzner-agent` is defined in `~/.ssh/config` and pins the dedicated key `~/.ssh/id_ed25519_agent`. Nothing else is needed — no sudo, no password, no prompt. If the alias is missing, see **Bootstrap** below.

## Verbs

| Verb | What you get |
|---|---|
| `help` | the verb list, straight from the server |
| `ps` | every container: name, status, image |
| `logs <container> [n]` | last `n` log lines with timestamps (default 100, max 2000) |
| `state <container>` | status, exit code, **restart count**, health, image, mounts |
| `stats` | one-shot CPU and memory per container |
| `disk` | filesystem usage |
| `uptime` | load average |

Container names come from `ps` and must match `[A-Za-z0-9][A-Za-z0-9_.-]*`.

Typical diagnosis — a container that will not stay up:

```bash
ssh hetzner-agent "ps"                          # find the name and status
ssh hetzner-agent "state <runner-container>"    # restart count + exit code
ssh hetzner-agent "logs <runner-container> 50"
```

A high `restarts:` with a nonzero `exit code:` means a crash loop, and the logs will repeat the same failure — read the *oldest* lines in the window, not the newest, since the tail is usually the loop rather than the cause.

## What this account cannot do — by design

The key is pinned in `authorized_keys` with `command="/usr/local/bin/agent-shell"`, so sshd runs that script **whatever the client sends**. The request arrives as `$SSH_ORIGINAL_COMMAND` and is treated as data: matched against the verb list, executed via argv arrays, never passed to a shell.

```
rm -rf /            -> denied — unknown command: rm
docker rm -f x      -> denied — too many arguments
bash                -> denied — unknown command: bash
sudo -i             -> denied — unknown command: sudo
logs x; rm -rf /    -> denied — shell metacharacters are not permitted
```

Three independent layers: the forced command (no other binary runs), sudo scoped to `docker ps/logs/inspect/stats` only (so `docker rm` fails even if the script were bypassed), and **no mutating verb exists at all**.

`state` returns curated fields rather than raw `docker inspect`, because `.Config.Env` carries container secrets — API tokens, deploy keys, database URLs. Do not add a verb that exposes it.

Every invocation is logged to `/var/log/agent-shell.log` on the VM with source IP, allowed and denied alike.

## When you need more than read-only

Restarting a container, editing a service, changing env vars — **use the Coolify API**, not SSH. See the `coolify` skill. Almost everything operational is reachable there, and it is the right tool: a Coolify-managed container restarted underneath Coolify will drift from its declared state.

If a task genuinely needs root on the VM, stop and ask the user. Do not attempt to widen this account, edit `agent-shell`, or reach for their personal full-sudo account to work around a denial. A denial here is the design functioning, not an obstacle to route around.

## Bootstrap on a new machine

The private key lives at `~/.ssh/id_ed25519_agent` on the Mac mini. For a machine that does not have it:

1. Preferred — store the key in 1Password as an SSH Key item and enable the 1Password SSH agent (Settings → Developer → *Use the SSH agent*). The private key then never touches disk on any machine, and `IdentityAgent` in `~/.ssh/config` serves it. See the `one-password` skill.
2. Otherwise, copy `~/.ssh/id_ed25519_agent` across and add the `hetzner-agent` block to `~/.ssh/config`.

The VM's IP for the ssh config block comes from 1Password:

```bash
op read "op://Development/Hetzner VM/ip"
```

To rebuild the server side from scratch — new VM, or after a rebuild — `scripts/install-vm-agent-access.sh` creates the locked `agent` account, installs `scripts/agent-shell` root-owned, writes the scoped sudoers with `visudo -c` validation, pins the key, and then verifies containment by attempting `rm -rf /`, `docker rm`, and `bash`. It fetches the IP from 1Password itself (override with `VM_HOST`), connects as the admin user with sudo, and touches nothing else — not Coolify, not `/root`, not that admin account.

## Adding a verb

Edit `scripts/agent-shell`, reinstall with the installer, and keep the invariants: validate every argument against a regex before use, execute through `exec` with an argv array (never build a command string), and never expose container environment variables. A read-only verb is a small decision; a mutating one is not — take that to the user.

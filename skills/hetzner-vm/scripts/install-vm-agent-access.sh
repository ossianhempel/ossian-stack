#!/usr/bin/env bash
# Install restricted agent SSH access on the Hetzner VM.
#
# Run this from the Mac mini. It connects as your own admin account (which has
# sudo) and creates a SEPARATE, heavily restricted `agent` account:
#
#   - no password, no sudo except three read-only docker subcommands
#   - its authorized_keys pins the key to /usr/local/bin/agent-shell, so the key
#     cannot run anything else — not a shell, not rm, not docker rm
#   - no port forwarding, no agent forwarding, no PTY
#
# Nothing here touches Coolify, /root, docker state, or the admin account.
set -euo pipefail

# The VM IP is deliberately not committed anywhere: fetch it from 1Password,
# or override with VM_HOST.
VM_HOST="${VM_HOST:-$(op read 'op://Development/Hetzner VM/ip')}"
VM_ADMIN="${VM_ADMIN:-dev}"
AGENT_USER="${AGENT_USER:-agent}"
PUBKEY_FILE="${PUBKEY_FILE:-$HOME/.ssh/id_ed25519_agent.pub}"
SHELL_SRC="${SHELL_SRC:-$(dirname "$0")/agent-shell}"

[ -f "$PUBKEY_FILE" ] || { echo "Missing public key: $PUBKEY_FILE" >&2; exit 1; }
[ -f "$SHELL_SRC" ]   || { echo "Missing agent-shell: $SHELL_SRC" >&2; exit 1; }

PUBKEY="$(cat "$PUBKEY_FILE")"

echo "==> Installing restricted agent access on $VM_ADMIN@$VM_HOST"

# Ship agent-shell to a staging path the admin user can write.
scp -q "$SHELL_SRC" "$VM_ADMIN@$VM_HOST:/tmp/agent-shell.staged"

ssh "$VM_ADMIN@$VM_HOST" "bash -s '$AGENT_USER' '$PUBKEY'" <<'REMOTE'
set -euo pipefail
AGENT_USER="${1:?agent user missing}"
PUBKEY="${2:?public key missing}"
DOCKER_BIN="$(command -v docker || echo /usr/bin/docker)"

# 1. Locked account: no password login, nologin-adjacent. The forced command
#    means its login shell is never used interactively anyway.
if ! id "$AGENT_USER" >/dev/null 2>&1; then
  sudo useradd --create-home --shell /bin/bash "$AGENT_USER"
  sudo passwd -l "$AGENT_USER" >/dev/null
  echo "  created user $AGENT_USER (password login locked)"
else
  echo "  user $AGENT_USER already exists — reusing"
fi

# 2. The gatekeeper script, owned by root so the agent cannot edit its own jail.
sudo install -o root -g root -m 0755 /tmp/agent-shell.staged /usr/local/bin/agent-shell
rm -f /tmp/agent-shell.staged
echo "  installed /usr/local/bin/agent-shell (root:root 0755)"

# 3. Audit log, writable by the agent, readable by you.
sudo touch /var/log/agent-shell.log
sudo chown "$AGENT_USER":adm /var/log/agent-shell.log
sudo chmod 0640 /var/log/agent-shell.log

# 4. Narrow sudo: only the read-only docker subcommands agent-shell calls.
#    Note these are subcommand-scoped — `docker run`/`rm`/`exec` do not match,
#    so even a bypass of agent-shell cannot mutate containers through sudo.
sudo tee /etc/sudoers.d/agent-readonly >/dev/null <<EOF
$AGENT_USER ALL=(root) NOPASSWD: $DOCKER_BIN ps *, $DOCKER_BIN ps
$AGENT_USER ALL=(root) NOPASSWD: $DOCKER_BIN logs *
$AGENT_USER ALL=(root) NOPASSWD: $DOCKER_BIN inspect *
$AGENT_USER ALL=(root) NOPASSWD: $DOCKER_BIN stats *
$AGENT_USER ALL=(root) NOPASSWD: $DOCKER_BIN images *
EOF
sudo chmod 0440 /etc/sudoers.d/agent-readonly
sudo visudo -cf /etc/sudoers.d/agent-readonly

# 5. The pinned key. command= wins over whatever the client sends; the
#    restrictions block tunnelling and interactive sessions.
AGENT_HOME="$(getent passwd "$AGENT_USER" | cut -d: -f6)"
sudo install -d -o "$AGENT_USER" -g "$AGENT_USER" -m 0700 "$AGENT_HOME/.ssh"
printf 'command="/usr/local/bin/agent-shell",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty,no-user-rc %s\n' \
  "$PUBKEY" | sudo tee "$AGENT_HOME/.ssh/authorized_keys" >/dev/null
sudo chown "$AGENT_USER":"$AGENT_USER" "$AGENT_HOME/.ssh/authorized_keys"
sudo chmod 0600 "$AGENT_HOME/.ssh/authorized_keys"
echo "  pinned agent key to agent-shell"

echo "==> Server-side install complete"
REMOTE

echo
echo "==> Verifying (these should succeed)"
ssh -i "${PUBKEY_FILE%.pub}" -o IdentitiesOnly=yes "$AGENT_USER@$VM_HOST" help || true
echo
echo "==> Verifying containment (these MUST be denied)"
for probe in "rm -rf /" "docker rm -f runner" "bash" "logs foo; rm -rf /"; do
  printf '  %-28s -> ' "$probe"
  ssh -i "${PUBKEY_FILE%.pub}" -o IdentitiesOnly=yes "$AGENT_USER@$VM_HOST" "$probe" 2>&1 | head -1
done

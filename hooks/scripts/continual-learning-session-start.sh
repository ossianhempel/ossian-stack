#!/usr/bin/env bash
# ossian-stack — continual learning, SessionStart nudge.
#
# Stays silent until enough unmined transcript material has accumulated for this
# project, then injects one line of additionalContext asking the session to run
# the continual-learning skill. It never mines anything itself and never edits a
# file the user owns.
#
# SessionStart, not Stop, is deliberate: Codex's Stop hook cannot inject a
# follow-up prompt (its output wire is continue/stopReason/suppressOutput/
# systemMessage, with no followUpMessage), while additionalContext on
# SessionStart is supported by both Claude Code and Codex.
#
# Only POSIX-portable find predicates are used. -newermt "@<epoch>" is GNU-only
# and fails on BSD find with "Can't parse date/time", so timestamps are carried
# by marker files and compared with -newer and -mmin instead.
#
# Tunables (env):
#   OSSIAN_CL_MIN_TRANSCRIPTS  new transcripts before nudging   (default 5)
#   OSSIAN_CL_MIN_HOURS        hours since last mine            (default 24)
#   OSSIAN_CL_COOLDOWN_HOURS   min hours between nudges         (default 6)
#   OSSIAN_CL_DISABLE          set to 1 to stay silent always
set -uo pipefail

exit_silent() { exit 0; }
[ "${OSSIAN_CL_DISABLE:-0}" = "1" ] && exit_silent
command -v jq >/dev/null 2>&1 || exit_silent   # no jq, no opinion

input="$(cat 2>/dev/null || true)"
[ -n "$input" ] || exit_silent

transcript="$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null)"
cwd="$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)"
[ -n "$transcript" ] || exit_silent

# The runtime hands us its own transcript path, so we never guess between
# ~/.claude/projects, ~/.codex/sessions and ~/.cursor/projects.
transcript_dir="$(dirname "$transcript")"
[ -d "$transcript_dir" ] || exit_silent

state_dir="${CLAUDE_PLUGIN_DATA:-${XDG_STATE_HOME:-$HOME/.local/state}/ossian-stack}/continual-learning"
slug="$(printf '%s' "${cwd:-$transcript_dir}" | tr -c 'A-Za-z0-9' '-' | sed 's/--*/-/g; s/^-//; s/-$//')"
slug="${slug:-default}"
mkdir -p "$state_dir" 2>/dev/null || exit_silent
mined="$state_dir/$slug.mined"     # mtime = last time the skill mined
nudged="$state_dir/$slug.nudged"   # mtime = last time we nudged

min_transcripts="${OSSIAN_CL_MIN_TRANSCRIPTS:-5}"
min_hours="${OSSIAN_CL_MIN_HOURS:-24}"
cooldown_hours="${OSSIAN_CL_COOLDOWN_HOURS:-6}"

# Cooldown: silent unless the last nudge is older than the window.
if [ -f "$nudged" ] && [ -z "$(find "$nudged" -mmin +$(( cooldown_hours * 60 )) 2>/dev/null)" ]; then
  exit_silent
fi

count_newer() {
  if [ -f "$mined" ]; then
    find "$transcript_dir" -maxdepth 1 -type f -newer "$mined" ! -path "$transcript" 2>/dev/null | wc -l
  else
    find "$transcript_dir" -maxdepth 1 -type f ! -path "$transcript" 2>/dev/null | wc -l
  fi
}
new_count="$(count_newer | tr -d '[:space:]')"
case "$new_count" in ''|*[!0-9]*) new_count=0 ;; esac
[ "$new_count" -gt 0 ] || exit_silent   # nothing new is nothing to mine

# Nudge when there is enough material, or when it has simply been long enough.
stale=0
if [ ! -f "$mined" ]; then
  stale=1
elif [ -n "$(find "$mined" -mmin +$(( min_hours * 60 )) 2>/dev/null)" ]; then
  stale=1
fi
if [ "$new_count" -lt "$min_transcripts" ] && [ "$stale" -eq 0 ]; then
  exit_silent
fi

: > "$nudged" 2>/dev/null || true

jq -n --arg n "$new_count" --arg dir "$transcript_dir" --arg mined "$mined" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: (
      "\($n) transcript(s) in \($dir) have not been mined for durable memory. "
      + "If the user is starting fresh work, offer to run the continual-learning skill; "
      + "do not run it unprompted mid-task. After a successful mine, touch \($mined) "
      + "so this stops repeating."
    )
  }
}'

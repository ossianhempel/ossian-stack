#!/usr/bin/env bash
# Report which vendored/adapted skills have moved upstream since we last synced.
#
# Repo-local dev tool — NOT part of the shipped plugin. Requires `gh` (authed) and `jq`.
#
#   scripts/check-upstream.sh                 # show drifted skills
#   scripts/check-upstream.sh --all           # include up-to-date skills
#   scripts/check-upstream.sh --record NAME   # after refreshing NAME, pin the new rev
#   scripts/check-upstream.sh --record-all    # pin every current upstream rev (careful)
set -euo pipefail

cd "$(dirname "$0")/.."
SOURCES="skills/sources.json"
TODAY="$(date +%F)"

command -v gh >/dev/null || { echo "need the gh CLI (brew install gh)" >&2; exit 1; }
command -v jq >/dev/null || { echo "need jq (brew install jq)" >&2; exit 1; }

SHOW_ALL=0 RECORD=() RECORD_ALL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) SHOW_ALL=1 ;;
    --record) shift; RECORD+=("$1") ;;
    --record-all) RECORD_ALL=1 ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
  shift
done

# fields are \x1f-separated (tab would collapse empty fields in `read`)
entries="$(jq -r '
  .skills | to_entries[]
  | select(.value.origin == "vendored" or .value.origin == "adapted")
  | select(.value.upstreamRev != null)
  | [ .key,
      (.value.repo | sub("^https://github.com/"; "") | sub("/$"; "")),
      (.value.upstreamPath // ""),
      .value.upstreamRev,
      .value.origin,
      (.value.refresh // "") ] | join("\u001f")' "$SOURCES")"

drifted=0 checked=0
declare -a NEW_REVS=()

while IFS=$'\x1f' read -r name repo upath rev origin refresh; do
  [[ -n "$name" ]] || continue
  checked=$((checked + 1))
  q="repos/$repo/commits?per_page=1"
  [[ -n "$upath" ]] && q="$q&path=$upath"
  head_sha="$(gh api "$q" --jq '.[0].sha' 2>/dev/null || true)"

  if [[ -z "$head_sha" ]]; then
    printf '\033[33m?  %-32s\033[0m upstream unreachable (%s)\n' "$name" "$repo"
    continue
  fi

  if [[ "$head_sha" == "$rev" ]]; then
    (( SHOW_ALL )) && printf '\033[32mok %-32s\033[0m %s\n' "$name" "${rev:0:8}"
  else
    drifted=$((drifted + 1))
    printf '\033[31mDRIFT %-29s\033[0m %s  %s..%s\n' "$name" "$origin" "${rev:0:8}" "${head_sha:0:8}"
    printf '      https://github.com/%s/compare/%s...%s%s\n' \
      "$repo" "$rev" "$head_sha" "${upath:+ (path: $upath)}"
    [[ "$origin" == "adapted" ]] && printf '      \033[33madapted — merge by hand, do not overwrite\033[0m\n'
    [[ -n "$refresh" ]] && printf '      %s\n' "$refresh"
  fi
  NEW_REVS+=("$name:$head_sha")
done <<< "$entries"

record_one() {
  local name="$1" sha="$2"
  local tmp; tmp="$(mktemp)"
  jq --arg n "$name" --arg s "$sha" --arg d "$TODAY" \
    '.skills[$n].upstreamRev = $s
     | .skills[$n].upstreamCheckedAt = $d
     | .skills[$n].lastSynced = $d
     | .updated = $d' "$SOURCES" > "$tmp"
  mv "$tmp" "$SOURCES"
  echo "recorded $name -> ${sha:0:8}"
}

for pair in "${NEW_REVS[@]:-}"; do
  [[ -n "$pair" ]] || continue
  n="${pair%%:*}"; s="${pair#*:}"
  if (( RECORD_ALL )); then
    record_one "$n" "$s"
  else
    for want in "${RECORD[@]:-}"; do
      [[ "$want" == "$n" ]] && record_one "$n" "$s"
    done
  fi
done

echo
echo "$checked checked · $drifted drifted"
(( drifted == 0 )) && exit 0 || exit 1

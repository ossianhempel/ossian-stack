#!/usr/bin/env bash
# Screenshot docs/plugin-map/index.html with headless Chrome at 2000px wide,
# sized to the board (no crop needed: the page reports its own height in
# shot mode), and save the README images.
#
#   scripts/render-plugin-map.sh            # writes docs/plugin-map/map.png + map-expanded.png
#   CHROME=/path/to/chrome scripts/render-plugin-map.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PAGE="$ROOT/docs/plugin-map/index.html"
OUT_DIR="$ROOT/docs/plugin-map"
WIDTH=2000

find_chrome() {
  if [ -n "${CHROME:-}" ]; then echo "$CHROME"; return; fi
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "$(command -v google-chrome || true)" \
    "$(command -v chromium || true)" \
    "$(command -v chromium-browser || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return; }
  done
  echo "render-plugin-map: no Chrome/Chromium found — set CHROME=/path/to/binary" >&2
  exit 1
}
CHROME_BIN="$(find_chrome)"

bun "$ROOT/scripts/build-plugin-map.js" >/dev/null

# Chrome 15x on macOS keeps running after --screenshot / --dump-dom because it
# spawns its updater, so each run is: start in the background, wait for the
# output to land, kill it.
run_chrome() { # $1 = output file to wait for, rest = chrome args
  local out="$1"; shift
  local tmp; tmp="$(mktemp -d)"
  "$CHROME_BIN" --headless=new --disable-gpu --hide-scrollbars --no-first-run \
    --disable-background-networking --disable-component-update \
    --user-data-dir="$tmp/profile" --force-device-scale-factor=1 "$@" >"$tmp/stdout" 2>/dev/null &
  local pid=$!
  local i=0
  while [ $i -lt 60 ]; do
    if [ -s "$out" ] || [ -s "$tmp/stdout" ]; then sleep 1; break; fi
    kill -0 "$pid" 2>/dev/null || break
    sleep 0.5; i=$((i + 1))
  done
  kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true
  [ -s "$out" ] || cp "$tmp/stdout" "$out"
}

render() { # $1 = query string, $2 = output file
  local url="file://$PAGE?shot=1&$1"
  local dom; dom="$(mktemp)"
  run_chrome "$dom" --window-size="$WIDTH,1000" --dump-dom "$url"
  local height
  height="$(sed -n 's/.*name="board-height" content="\([0-9]*\)".*/\1/p' "$dom" | head -1)"
  [ -n "$height" ] || { echo "render-plugin-map: page did not report board-height (JS error?)" >&2; exit 1; }
  rm -f "$2"
  run_chrome "$2" --window-size="$WIDTH,$height" --screenshot="$2" "$url"
  [ -s "$2" ] || { echo "render-plugin-map: screenshot not written" >&2; exit 1; }
  echo "wrote ${2#$ROOT/} (${WIDTH}x${height})"
}

render "expanded=0" "$OUT_DIR/map.png"
render "expanded=1" "$OUT_DIR/map-expanded.png"

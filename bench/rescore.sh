#!/usr/bin/env bash
# Re-score benchmark runs with the render, locally. Runs made in the Fly sandbox are scored
# preflight-only (no browser there); this reruns `caxgauge check` on each run's part.stl with
# its brief's bounds and the four-view render. Reads only STL data — runs no model code.
#
# Usage: bench/rescore.sh [RUN_GLOB]     e.g. bench/rescore.sh 'bim-*'
# Env: CAXGAUGE_POLYFETCH_DIR (required).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
[ -d "${CAXGAUGE_POLYFETCH_DIR:-}" ] || { echo "rescore.sh: set CAXGAUGE_POLYFETCH_DIR"; exit 2; }
uv run --directory "$CAXGAUGE_POLYFETCH_DIR" polyfetch doctor

field() { sed -n "s/^$2: *//p" "$1" | head -n1; }

for out in "$repo"/site/bench/${1:-*}/; do
	out="${out%/}"
	[ -s "$out/part.stl" ] || continue
	run="$(basename "$out")"            # <brief>-<tool>-<n>
	brief="$repo/bench/briefs/${run%-*-*}.md"
	[ -f "$brief" ] || { echo "rescore.sh: no brief for $run"; continue; }
	args=(check "$out/part.stl" --out "$out")
	envelope="$(field "$brief" envelope)"
	band="$(field "$brief" volume_band)"
	[ -n "$envelope" ] && args+=(--envelope "$envelope")
	[ -n "$band" ] && args+=(--volume-band "$band")
	echo "== $run"
	uv run --directory "$repo" caxgauge "${args[@]}" || true
done

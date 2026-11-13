#!/usr/bin/env bash
# Re-score benchmark runs with the render, locally. Runs made in the Fly sandbox are scored
# preflight-only (no browser there); this reruns `caxgauge check` on each run's part.stl with
# its brief's bounds and the four-view render, and writes the new verdict into that run's
# row of site/bench/runs.tsv (the last row for that brief/tool/run). Reads only STL data —
# runs no model code.
#
# Usage: bench/rescore.sh [RUN_GLOB]     e.g. bench/rescore.sh 'bim-*'
# Env: CAXGAUGE_POLYFETCH_DIR (required).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
[ -d "${CAXGAUGE_POLYFETCH_DIR:-}" ] || { echo "rescore.sh: set CAXGAUGE_POLYFETCH_DIR"; exit 2; }
uv run --directory "$CAXGAUGE_POLYFETCH_DIR" polyfetch doctor

field() { sed -n "s/^$2: *//p" "$1" | head -n1; }

ledger="$repo/site/bench/runs.tsv"

# Set column 5 (verdict) of the last ledger row for brief $1, tool $2, run $3 to $4.
set_verdict() {
	[ -f "$ledger" ] || return 0
	awk -F'\t' -v OFS='\t' -v b="$1" -v t="$2" -v n="$3" -v v="$4" '
		NR == FNR { if ($1 == b && $2 == t && $3 == n) last = FNR; next }
		FNR == last { $5 = v } { print }
	' "$ledger" "$ledger" > "$ledger.tmp" && mv "$ledger.tmp" "$ledger"
}

for out in "$repo"/site/bench/${1:-*}/; do
	out="${out%/}"
	[ -s "$out/part.stl" ] || continue
	run="$(basename "$out")"            # <brief>-<tool>-<n>
	n="${run##*-}"; tool="${run%-*}"; tool="${tool##*-}"
	brief="$repo/bench/briefs/${run%-*-*}.md"
	[ -f "$brief" ] || { echo "rescore.sh: no brief for $run"; continue; }
	args=(check "$out/part.stl" --out "$out")
	for s in part.py part.scad part.json; do  # the agent's script, beside its renders
		[ -f "$out/$s" ] && { args+=(--source "$out/$s"); break; }
	done
	envelope="$(field "$brief" envelope)"
	band="$(field "$brief" volume_band)"
	[ -n "$envelope" ] && args+=(--envelope "$envelope")
	[ -n "$band" ] && args+=(--volume-band "$band")
	echo "== $run"
	rc=0; uv run --directory "$repo" caxgauge "${args[@]}" || rc=$?
	case "$rc" in  # same mapping as run.sh
	0) verdict=review ;;
	1) verdict=fail ;;
	3) verdict=preflight-only ;;
	*) verdict="error-exit-$rc" ;;
	esac
	set_verdict "${run%-*-*}" "$tool" "$n" "$verdict"
done

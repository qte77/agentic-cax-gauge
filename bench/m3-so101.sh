#!/usr/bin/env bash
# M3 review campaign (plan §8): run `caxgauge check --source` on every so101 part that has an
# exported STL, into site/m3/<part>/, and list each part's verdict. No bounds are declared in
# so101, so bbox and volume report SKIP; the render is the gate and the owner reviews it.
# Reads so101's committed STLs and CAD scripts as data — runs none of its code.
#
# Usage: bench/m3-so101.sh [SO101_DIR]   (relative to this repo; default ../so101-biolab-automation,
#        kept relative so the published reports carry no local absolute paths)
# Env: CAXGAUGE_POLYFETCH_DIR (required — without a render a part is only preflight-only).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo"
so101="${1:-../so101-biolab-automation}"
[ -d "${CAXGAUGE_POLYFETCH_DIR:-}" ] || { echo "m3-so101.sh: set CAXGAUGE_POLYFETCH_DIR"; exit 2; }
uv run --directory "$CAXGAUGE_POLYFETCH_DIR" polyfetch doctor

out_root="site/m3"
mkdir -p "$out_root"
list="$out_root/parts.tsv"
printf 'part\tstatus\tverdict\tstl\tsource\n' > "$list"
echo "so101 commit $(git -C "$so101" rev-parse --short HEAD)" > "$out_root/so101.txt"

# name, status, stl, cad — one tab-separated line per part.
python3 -c '
import json, sys
for p in json.load(open(sys.argv[1])):
    print("\t".join([p["name"], p.get("status", ""), p["stl"], p.get("cad") or ""]))
' "$so101/src/hardware/parts.json" |
	while IFS=$'\t' read -r name status stl cad; do
		mesh="$so101/hardware/stl/$stl"
		if [ ! -s "$mesh" ]; then
			printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$status" "no-stl" "$stl" "$cad" >> "$list"
			continue
		fi
		args=(check "$mesh" --out "$out_root/$name")
		[ -n "$cad" ] && [ -f "$so101/src/hardware/$cad" ] && args+=(--source "$so101/src/hardware/$cad")
		echo "== $name"
		rc=0; uv run caxgauge "${args[@]}" < /dev/null || rc=$?
		case "$rc" in
		0) verdict=review ;;
		1) verdict=fail ;;
		3) verdict=preflight-only ;;
		*) verdict="error-exit-$rc" ;;
		esac
		printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$status" "$verdict" "$stl" "$cad" >> "$list"
	done
echo "m3-so101.sh: done — site/m3/parts.tsv"

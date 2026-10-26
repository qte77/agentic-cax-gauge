#!/usr/bin/env bash
# CAD-generation benchmark pilot (plan §5 BENCH). For each brief × tool × run: an agent
# (`claude -p`) writes a CAD script and exports part.stl in a clean temp dir; then
# `caxgauge check` scores it with the brief's pre-declared bounds into site/bench/. No model
# judges anything — the human reviews the renders afterwards.
#
# Usage: bench/run.sh [BRIEF_GLOB] [TOOLS] [RUNS]
#   e.g. bench/run.sh '01-*' build123d 1        # dry run
#        bench/run.sh '*' 'build123d openscad' 3
#        bench/run.sh 'bim-*' ifcopenshell 3       # BIM track: IFC, tessellated for scoring
# Env: CAXGAUGE_POLYFETCH_DIR (for the render), BENCH_MODEL, BENCH_RUN_USD,
#      BENCH_TOTAL_USD (stop once the summed estimated cost reaches it), BENCH_TMP (scratch
#      root), BENCH_NO_RENDER=1 (preflight only — the Fly sandbox has no browser; render
#      afterwards with bench/rescore.sh).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
brief_glob="${1:-*}"
tools="${2:-build123d openscad}"
runs="${3:-3}"
model="${BENCH_MODEL:-claude-sonnet-5-5}"
run_usd="${BENCH_RUN_USD:-1.00}"
total_usd="${BENCH_TOTAL_USD:-20}"
tmp="${BENCH_TMP:-/tmp/claude-1000}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-$tmp/uv-cache}"  # /workspaces disk is near-full
mkdir -p "$tmp"

render=()
if [ "${BENCH_NO_RENDER:-}" = 1 ]; then
	render=(--no-render)
else
	[ -d "${CAXGAUGE_POLYFETCH_DIR:-}" ] || { echo "run.sh: set CAXGAUGE_POLYFETCH_DIR"; exit 2; }
	uv run --directory "$CAXGAUGE_POLYFETCH_DIR" polyfetch doctor
fi

ledger="$repo/site/bench/runs.tsv"
mkdir -p "$repo/site/bench"
[ -f "$ledger" ] || printf 'brief\ttool\trun\tstl\tverdict\tcost_usd\tturns\tmodel\n' > "$ledger"

spent() { awk -F'\t' 'NR > 1 { s += $6 } END { printf "%.4f", s + 0 }' "$ledger"; }

# Front-matter value, e.g. `envelope: 21,16,11`.
field() { sed -n "s/^$2: *//p" "$1" | head -n1; }

# The prompt is the brief body without front matter, its `# heading`, or the `Bounds:` notes.
prompt_of() { awk '/^---$/ { fm++; next } fm >= 2 && /^Bounds:/ { exit } fm >= 2 && !/^# /' "$1"; }

system_for() {
	case "$1" in
	build123d)
		echo "You are a CAD engineer. Use the Write tool to create a build123d Python script named part.py in the current directory that builds the part described by the user, in millimetres, Z up, as a single solid, and exports it with export_stl to part.stl in the current directory. Then run exactly this one shell command, on its own: uv run --with build123d python part.py — it is the only shell command you are allowed; any other command, including combined commands with && or heredocs, is denied. If it fails, fix part.py with Edit or Write and run the same command again. Use Read to check part.stl exists. Do not ask questions; make reasonable assumptions and state them in comments." ;;
	openscad)
		echo "You are a CAD engineer. Use the Write tool to create an OpenSCAD file named part.scad in the current directory that models the part described by the user, in millimetres, Z up, as a single solid. Then run exactly this one shell command, on its own: openscad -o part.stl part.scad — it is the only shell command you are allowed; any other command, including combined commands with && or heredocs, is denied. If it fails, fix part.scad with Edit or Write and run the same command again. Do not ask questions; make reasonable assumptions and state them in comments." ;;
	ifcopenshell)
		echo "You are a BIM engineer. Use the Write tool to create a Python script named part.py in the current directory that uses the IfcOpenShell API (ifcopenshell 0.9: ifcopenshell.api.<module>.<function>(file, keyword=...)) to author the building element described by the user as an IFC4 model — project, site, storey, the element with a body representation, and any openings — and writes it to part.ifc in the current directory. Lengths in the brief are millimetres; Z is up. Then run exactly this one shell command, on its own: uv run --with ifcopenshell python part.py — it is the only shell command you are allowed; any other command, including combined commands with && or heredocs, is denied. If it fails, fix part.py with Edit or Write and run the same command again. Use Read to check part.ifc exists. Do not ask questions; make reasonable assumptions and state them in comments." ;;
	solidcraft)
		echo "You are a CAD engineer. Use the Write tool to create a SolidCraft script named part.json in the current directory — a JSON object {\"commands\": [{\"command\": ..., \"params\": {...}}, ...]} of SolidCraft commands — that builds the part described by the user, in millimetres, Z up, as a single solid. You may run exactly two shell commands, each on its own: solidcraft-cli commands — lists the available commands and their parameters — and solidcraft-cli run part.json --out part.stl — builds the part and exports it. Any other command, including combined commands with && or pipes, is denied. If the build fails, fix part.json with Edit or Write and run it again. Do not ask questions; make reasonable assumptions." ;;
	*) echo "run.sh: unknown tool $1" >&2; exit 2 ;;
	esac
}

allowed_for() {
	case "$1" in
	build123d) echo "Read,Write,Edit,Bash(uv run --with build123d python part.py)" ;;
	openscad) echo "Read,Write,Edit,Bash(openscad -o part.stl part.scad)" ;;
	ifcopenshell) echo "Read,Write,Edit,Bash(uv run --with ifcopenshell python part.py)" ;;
	solidcraft) echo "Read,Write,Edit,Bash(solidcraft-cli commands),Bash(solidcraft-cli run part.json --out part.stl)" ;;
	esac
}

for brief in "$repo"/bench/briefs/$brief_glob.md; do
	name="$(basename "$brief" .md)"
	envelope="$(field "$brief" envelope)"
	band="$(field "$brief" volume_band)"
	for tool in $tools; do
		for n in $(seq 1 "$runs"); do
			if awk -v s="$(spent)" -v t="$total_usd" 'BEGIN { exit !(s >= t) }'; then
				echo "run.sh: estimated spend $(spent) USD reached the $total_usd USD cap — stopping"
				exit 0
			fi
			out="$repo/site/bench/$name-$tool-$n"
			work="$(mktemp -d "$tmp/bench-XXXXXX")"
			echo "== $name / $tool / run $n"
			(cd "$work" && claude -p "$(prompt_of "$brief")" \
				--model "$model" --restricted --tools "Read,Write,Edit,Bash" \
				--allowedTools "$(allowed_for "$tool")" --permission-prompts none \
				--system-prompt "$(system_for "$tool")" --max-budget-usd "$run_usd" \
				--no-session-persistence --output-format json > run.json) || true
			mkdir -p "$out"
			cp "$work/run.json" "$out/run.json" 2>/dev/null || echo '{}' > "$out/run.json"
			cp "$work"/part.py "$work"/part.scad "$work"/part.ifc "$work"/part.json "$out/" 2>/dev/null || true
			# The BIM track writes IFC; the gauge scores its tessellated STL like any part.
			if [ -s "$work/part.ifc" ]; then
				uv run --no-project --with ifcopenshell --with trimesh python "$repo/bench/ifc_to_stl.py" \
					"$work/part.ifc" "$work/part.stl" || true
			fi
			cost="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("total_cost_usd", 0))' "$out/run.json" 2>/dev/null || echo 0)"
			turns="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("num_turns", ""))' "$out/run.json" 2>/dev/null || echo)"
			if [ -s "$work/part.stl" ]; then
				cp "$work/part.stl" "$out/part.stl"
				args=(check "$out/part.stl" --out "$out" "${render[@]}")
				for s in part.py part.scad part.json; do  # the agent's script, beside its renders
					[ -f "$out/$s" ] && { args+=(--source "$out/$s"); break; }
				done
				[ -n "$envelope" ] && args+=(--envelope "$envelope")
				[ -n "$band" ] && args+=(--volume-band "$band")
				rc=0; uv run --directory "$repo" caxgauge "${args[@]}" || rc=$?
				verdict="$([ "$rc" -eq 0 ] && echo review || echo fail)"
				stl=yes
			else
				verdict="no-output"; stl=no
			fi
			printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$tool" "$n" "$stl" "$verdict" "$cost" "$turns" "$model" >> "$ledger"
			rm -rf "$work"
		done
	done
done
echo "run.sh: done — estimated spend $(spent) USD; ledger: site/bench/runs.tsv"

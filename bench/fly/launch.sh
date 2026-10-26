#!/usr/bin/env bash
# Run a benchmark round on a throwaway Fly Machine, fetch the results, destroy the Machine.
# Model-written scripts execute only there. Then score locally with the render:
#   bench/fly/launch.sh 'bim-*' ifcopenshell 3 && bench/rescore.sh 'bim-*'
#
# Needs: `fly auth login` (browser) and the app secret CLAUDE_CODE_OAUTH_TOKEN, set once by
# the owner (bench/fly/README.md). Env: BENCH_APP (default caxgauge-bench), BENCH_REGION.
set -euo pipefail

repo="$(cd "$(dirname "$0")/../.." && pwd)"
app="${BENCH_APP:-caxgauge-bench}"
name="bench-$(date +%Y%m%d-%H%M%S)"
cd "$repo"

# Build + push with a fixed label, then run from it. `fly machine run .` built fine but its
# pushes failed (unexpected EOF on the large layer; a 404 on the fresh tag via Depot).
fly deploy . --build-only --push --image-label bench -c bench/fly/fly.toml --depot
fly machine run "registry.fly.io/$app:bench" bash bench/fly/remote.sh \
	"${1:-*}" "${2:-build123d openscad}" "${3:-3}" \
	-a "$app" --region "${BENCH_REGION:-fra}" \
	--vm-memory 2048 --vm-cpus 2 --restart no --name "$name" --detach
id="$(fly machine list -a "$app" --json | python3 -c \
	'import json,sys; print(next(m["id"] for m in json.load(sys.stdin) if m["name"] == sys.argv[1]))' "$name")"
trap 'fly machine destroy --force -a "$app" "$id" || true' EXIT
echo "launch: machine $id ($name) — waiting for the round to finish"

deadline=$(( $(date +%s) + ${BENCH_MAX_WAIT:-14400} ))
until fly ssh console -q -a "$app" --machine "$id" -C "cat /tmp/done" 2>/dev/null | grep -q done; do
	[ "$(date +%s)" -lt "$deadline" ] || { echo "launch: gave up waiting"; exit 1; }
	sleep 60
done
fetched="$(mktemp -d "${BENCH_TMP:-/tmp/claude-1000}/fly-XXXXXX")"
fly ssh sftp get -a "$app" --machine "$id" /tmp/out.tgz "$fetched/out.tgz"
tar -xzf "$fetched/out.tgz" -C "$fetched"
# Run dirs are new; the ledger is appended to, never replaced (it holds earlier rounds).
mkdir -p "$repo/site/bench"
ledger="$repo/site/bench/runs.tsv"
[ -f "$ledger" ] || head -n1 "$fetched/site/bench/runs.tsv" > "$ledger"
tail -n +2 "$fetched/site/bench/runs.tsv" >> "$ledger"
rm "$fetched/site/bench/runs.tsv"
cp -r "$fetched/site/bench/." "$repo/site/bench/"
rm -rf "$fetched"
echo "launch: results in site/bench/ — now run bench/rescore.sh"

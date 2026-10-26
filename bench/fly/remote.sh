#!/usr/bin/env bash
# Runs inside the Fly Machine: the benchmark (preflight only — no browser here), then packs
# site/bench/ for bench/fly/launch.sh to fetch, and waits a bounded time before exiting so
# the Machine is never left running. Args are passed straight to bench/run.sh.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 2

# Model-written scripts run under Claude Code's Bash tool; keep the subscription token out
# of their environment. The docs list what the scrub removes but not CLAUDE_CODE_OAUTH_TOKEN
# by name, so check it here before the round and abort if a subprocess can still see it.
export CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1
[ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] || { echo "remote: CLAUDE_CODE_OAUTH_TOKEN not set"; exit 2; }
# BENCH_CANARY proves the command really ran; the token must not appear beside it.
export BENCH_CANARY=canary-ok
cmd="printenv BENCH_CANARY CLAUDE_CODE_OAUTH_TOKEN"
seen="$(cd /tmp && claude -p "Run this exact shell command and reply with its output only: $cmd" \
	--model "${BENCH_MODEL:-claude-sonnet-5-5}" --restricted --tools Bash \
	--allowedTools "Bash($cmd)" --permission-prompts none \
	--max-budget-usd 0.10 --no-session-persistence --output-format json || true)"
if ! printf '%s' "$seen" | grep -qF canary-ok; then
	echo "remote: the leak check did not run — aborting the round"; exit 3
fi
if printf '%s' "$seen" | grep -qF "$CLAUDE_CODE_OAUTH_TOKEN"; then
	echo "remote: the token is visible to Bash subprocesses — aborting the round"; exit 3
fi
echo "remote: token not visible to subprocesses"

BENCH_NO_RENDER=1 BENCH_TMP=/tmp bash bench/run.sh "$@"
tar -czf /tmp/out.tgz site/bench
echo finished > /tmp/done
echo "remote: packed /tmp/out.tgz; waiting up to ${BENCH_FETCH_WAIT:-3600}s for the fetch"
sleep "${BENCH_FETCH_WAIT:-3600}"

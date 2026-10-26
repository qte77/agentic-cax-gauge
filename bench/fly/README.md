# Benchmark sandbox on Fly.io

Model-written scripts (`part.py`, `part.scad`, `part.json`) execute on a throwaway Fly
Machine, never in the Codespace: `bwrap` can't create user namespaces there, which the plan
(§5 BENCH) requires before scaling past the pilot. The Machine has no ports or services; its
image is built by Fly's remote builder from the repo root (`Dockerfile` here).

| File | Runs where | Does |
|---|---|---|
| `fly.toml` | Codespace | App config, only so `fly deploy --build-only` can build and push the image |
| `Dockerfile` | Fly builder | Node 22 + uv + OpenSCAD + SolidCraft CLI (release checksum) + Claude Code (exact version) + this repo |
| `probe.sh` | Machine | One-machine proof: each tool builds a box we wrote, `caxgauge check` scores it. No model |
| `remote.sh` | Machine | Token-leak check, then `bench/run.sh` preflight-only, then packs `site/bench/` |
| `launch.sh` | Codespace | Starts the Machine, waits, fetches results, appends the ledger, destroys the Machine |

## Once (owner)

1. `fly auth login` (browser). The app `caxgauge-bench` exists (`fly apps create`).
2. `claude setup-token` (browser) prints a one-year subscription token. In your own
   terminal (not through an agent session, which would keep it in the transcript), store it
   as an app secret:

   ```bash
   fly secrets set -a caxgauge-bench --stage CLAUDE_CODE_OAUTH_TOKEN=<token>
   ```

## A round

```bash
bench/fly/launch.sh '0[6-9]-*' 'build123d openscad' 1   # or 'bim-*' ifcopenshell 3
CAXGAUGE_POLYFETCH_DIR=../polyfetch-scrape bench/rescore.sh   # add the render locally
```

`launch.sh` destroys the Machine on exit, also on error; `remote.sh` exits on its own after
`BENCH_FETCH_WAIT` (3600 s) so nothing is left running. Spend caps are `bench/run.sh`'s
(`BENCH_RUN_USD`, `BENCH_TOTAL_USD`), counted per round.

## Residual risk

`remote.sh` sets `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` and aborts unless a probe command can
see a canary variable but not the token. That keeps the token out of the scripts'
environment, but a script running as the same user could still read Claude Code's own
process environment. The Machine is throwaway and the briefs are ours, so the exposure is the
subscription token for the length of a round — use a dedicated token for the benchmark.

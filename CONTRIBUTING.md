# Contributing

Technical workflows and coding standards for agentic-cax-gauge.
For AI agent behavioral rules, see [AGENTS.md](AGENTS.md).

## Instant Commands

| Command | Purpose |
|---------|---------|
| `make setup` | Install runtime + dev + test dependencies (`uv sync`) |
| `make setup_cad` | Install build123d (optional `cad` extra) |
| `make validate` | **The gate** — ruff format check + ruff lint (incl. security) + pyright strict + pytest + complexipy. CI runs exactly this |
| `make autofix` | Auto-format and fix lint issues |
| `make test` / `make test_cov` | Tests (cad/browser-marked tests excluded by default) / with coverage |
| `make test_browser` | Browser-marked tests against real Chromium (render, load check, view orientation, edges). Needs `CAXGAUGE_POLYFETCH_DIR` set to a polyfetch-scrape checkout whose Chromium is installed (`make -C <it> doctor`); prints `SKIP` otherwise. Not in CI — run before changing `src/caxgauge/viewer/`, `render.py` or `browser.py` |
| `make audit` | Scan resolved dependencies for known vulnerabilities (`pip-audit`, needs network). Not in `validate` or CI — Dependabot security updates cover CI. Run before a release |
| `make site` | Regenerate the sample reports in `site/` (deployed to GitHub Pages by `pages.yml`). Needs `CAXGAUGE_POLYFETCH_DIR` with Chromium and the so101 checkout beside this repo (`SO101=` to override); refuses to write if any part gets an unexpected verdict. Commit `site/` after regenerating |
| `bench/run.sh [GLOB] [TOOLS] [RUNS]` | CAD-generation benchmark: `claude -p` writes each brief in each tool, `caxgauge check` scores it into `site/bench/` (ledger `runs.tsv`). Needs `CAXGAUGE_POLYFETCH_DIR`; spends your Claude usage — `BENCH_TOTAL_USD` (default 20) stops it, `BENCH_RUN_USD` caps each run, `BENCH_MODEL` pins the model. Tools: `build123d`, `openscad`, `solidcraft`, `ifcopenshell` (BIM briefs `bim-*`). `BENCH_TMP` sets the scratch root; `BENCH_NO_RENDER=1` scores preflight-only (no polyfetch needed). Model-written scripts execute, so run it in the Fly sandbox (`bench/fly/launch.sh`, see `bench/fly/README.md`) rather than on your machine. Each run's `provenance.json` records the harness commit, a hash of the brief, and the tool and Claude Code versions (`bench/provenance.py`). Dry-run first: `bench/run.sh '01-*' build123d 1` |
| `bench/rescore.sh [RUN_GLOB]` | Re-score benchmark runs locally with the four-view render, from each run's `part.stl` and its brief's bounds; passes the agent's script as `--source`. Reads only STL data — runs no model code. Needs `CAXGAUGE_POLYFETCH_DIR` |
| `bench/m3-so101.sh [SO101_DIR]` | M3 review campaign: `caxgauge check --source` on every so101 part with an exported STL, into `site/m3/<part>/`, plus `site/m3/parts.tsv` (verdict per part) and the so101 commit. Needs `CAXGAUGE_POLYFETCH_DIR` and the so101 checkout beside this repo; reads its STLs and scripts, runs none of its code. The owner records defects per part in `bench/m3-review.csv` |
| `python3 bench/blind.py make` / `unblind` | Blind labelling of the benchmark pilot: `make` copies each run's renders under a random ID into `site/bench-blind/` with only the brief (no tool, script or check results) and writes the sheet `bench/labels-blind.csv` (`accept` yes/no/unsure, `reject_reason` as reason codes from `bench/rubric.md`, the one rubric for every human judgement here) and the key `bench/blind-key.csv` (don't open it until the sheet is filled); `unblind` copies the answers into `bench/labels.csv` |
| `make check_docs` | Markdown lint — prints `SKIP` if `markdownlint-cli2` is not installed |
| `make check_links` | Link check (needs network) — prints `SKIP` if `lychee` is not installed |
| `make help` | List all recipes |

**Emergency fallback** (if make commands fail):

```bash
uv run ruff format . && uv run ruff check . --fix
uv run pyright src
uv run pytest
```

## Testing Strategy

- **Strict TDD, behavior-level, no Gherkin/BDD** (plan §2).
  **RED** a failing test that defines the behavior → **GREEN** minimal code →
  **REFACTOR** only when duplication warrants it.
- Mirror `src/` in `tests/`. Only non-trivial tests; no tests for declarative config.
- **Stub-mode is mandatory** for every external-tool wrapper — CI has no build123d or
  Chromium. Tests needing them are marked `@pytest.mark.cad` / `@pytest.mark.browser` and
  excluded by default.
- The headline and honesty tests are specified in plan §7.3 and §10.

## Code Style

- **Python 3.12** exactly, full type hints, pyright strict
- **Google-style docstrings**, absolute imports only
- Add `# Reason:` comments for non-obvious logic (the *why*)
- **Never repair** an input mesh or model in a check path — it hides the defect

## Pre-commit Checklist

1. `make validate` passes
2. `CHANGELOG.md` updated under `## [Unreleased]` for non-trivial changes
3. Conventional commit message (template: `.gitmessage` — `git config commit.template .gitmessage`)

## Conventional Commits

Types: `feat | fix | build | chore | ci | docs | style | refactor | perf | test`
Scopes: `preflight | render | report | cli | bim | ci | docs | tests`

## Documentation Hierarchy

Each document has one authority. Reference it; don't duplicate it.

| Document | Authority | Audience |
|----------|-----------|----------|
| [README.md](README.md) | What and why, status | Humans |
| [AGENTS.md](AGENTS.md) | Agent rules, decision framework | AI agents |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Commands, testing, style (this file) | Both |
| [docs/plans/001-v0.md](docs/plans/001-v0.md) | Plan + handoff: design, milestones, remaining work | Both |
| [docs/reference/](docs/reference/) | Research evidence (informational) | Both |
| [CHANGELOG.md](CHANGELOG.md) | Version history (Keep a Changelog) | Both |
| [AGENT_LEARNINGS.md](AGENT_LEARNINGS.md) / [AGENT_REQUESTS.md](AGENT_REQUESTS.md) | Patterns / escalations | AI agents |
| `.claude/rules/*.md` | Always-loaded session rules | AI agents |

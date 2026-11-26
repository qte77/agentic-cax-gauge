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
| `make test` / `make test_cov` | Tests (cad/browser/ifc-marked tests excluded by default) / with coverage |
| `make test_ifc` | IFC-marked tests: `bench/ifc_facts.py` measures IfcOpenShell-built reference and known-bad models of the plumbing and wiring briefs, in millimetres and metres, and `bench/ifc_checks.py` decides them; also reads each brief's system types from the installed IFC4 schema. Borrows `ifcopenshell==0.9.0.post1` through `uv run --with` (not a package dependency) and fails if it can't import it. Not in CI — run before changing either script |
| `make test_browser` | Browser-marked tests against real Chromium (render, load check, view orientation, edges). Needs `CAXGAUGE_POLYFETCH_DIR` set to a polyfetch-scrape checkout whose Chromium is installed (`make -C <it> doctor`); prints `SKIP` otherwise. Not in CI — run before changing `src/caxgauge/viewer/`, `render.py` or `browser.py` |
| `make audit` | Scan resolved dependencies for known vulnerabilities (`pip-audit`, needs network). Not in `validate` or CI — Dependabot security updates cover CI. Run before a release |
| `make release_smoke` | Before a minor or major tag: loads `site/index.html` and a `--source` report on a desktop viewport and on iPhone 13, Pixel 7 and iPad Mini (portrait and landscape) in polyfetch's Chromium, and lists findings: load failures, browser errors and failed requests, horizontal overflow, missing view images, standalone touch targets under 44×44 CSS px, missing screenshots. Screenshots land in `reports/release-smoke/` — look at them; no findings is necessary, not sufficient. Exit 0: no findings; 1: findings, or the probe broke; 2: `CAXGAUGE_POLYFETCH_DIR` with Chromium is missing, so nothing was checked. Other paths: `uv run python scripts/release_smoke.py --site <dir> --out <dir>` (`--out` keeps PNGs it did not write). Not in `validate` or CI; patch releases skip it |
| `make site` | Regenerate the sample reports in `site/` (deployed to GitHub Pages by `pages.yml`). Needs `CAXGAUGE_POLYFETCH_DIR` with Chromium and the so101 checkout beside this repo (`SO101=` to override); refuses to write if any part gets an unexpected verdict. Commit `site/` after regenerating |
| `bench/run.sh [GLOB] [TOOLS] [RUNS]` | CAD-generation benchmark: `claude -p` writes each brief in each tool, `caxgauge check` scores it into `site/bench/` (ledger `runs.tsv`). Needs `CAXGAUGE_POLYFETCH_DIR`; spends your Claude usage — `BENCH_TOTAL_USD` (default 20) stops it, `BENCH_RUN_USD` caps each run, `BENCH_MODEL` pins the model. Tools: `build123d`, `openscad`, `solidcraft`, `ifcopenshell` (BIM briefs `bim-*`). `BENCH_TMP` sets the scratch root; `BENCH_NO_RENDER=1` scores preflight-only (no polyfetch needed). Model-written scripts execute, so run it in the Fly sandbox (`bench/fly/launch.sh`, see `bench/fly/README.md`) rather than on your machine. Each run's `provenance.json` records the harness commit, a hash of the brief, and the tool and Claude Code versions (`bench/provenance.py`). For every run, `bench/ifc_checks.py` decides the brief's IFC-level bounds (`ifc_checks.json`) from the facts `bench/ifc_facts.py` measures on `part.ifc` (`ifc_facts.json`): a failed bound turns `review` or `preflight-only` into `fail`, and an unreadable brief, or a failed `uv`, logs `error-ifc-checks-exit-2` unless the gauge logged an error first. The facts are measured into a directory made after the agent exits, never into its work directory. Dry-run first: `bench/run.sh '01-*' build123d 1` |
| `bench/rescore.sh [RUN_GLOB]` | Re-score benchmark runs locally with the four-view render, from each run's `part.stl` and its brief's bounds; passes the agent's script as `--source`. Decides the IFC-level bounds again from the run's saved `ifc_facts.json` and merges them into the verdict as `bench/run.sh` does. Reads only STL and JSON data — runs no model code. Needs `CAXGAUGE_POLYFETCH_DIR` |
| `bench/m3-so101.sh [SO101_DIR]` | M3 review campaign: `caxgauge check --source` on every so101 part with an exported STL, into `site/m3/<part>/`, plus `site/m3/parts.tsv` (verdict per part) and the so101 commit. Needs `CAXGAUGE_POLYFETCH_DIR` and the so101 checkout beside this repo; reads its STLs and scripts, runs none of its code. The owner records defects per part in `bench/m3-review.csv` |
| `python3 bench/blind.py make` / `unblind` | Blind labelling of the benchmark pilot: `make` copies each run's renders under a random ID into `site/bench-blind/` with only the brief (no tool, script or check results) and writes the sheet `bench/labels-blind.csv` (`accept` yes/no/unsure, `reject_reason` as reason codes from `bench/rubric.md`, the one rubric for every human judgement here) and the key `bench/blind-key.csv` (don't open it until the sheet is filled); `unblind` copies the answers into `bench/labels.csv` |
| `python3 -I bench/provenance.py --brief BRIEF.md --tool TOOL --model MODEL` | Prints one run's provenance JSON: harness commit and dirty flag, the brief's SHA-256, the tool version (for build123d also its OCP version), Claude Code version, model. `bench/run.sh` calls it per run; a missing tool prints `unavailable: …`, never an error |
| `uv run python -I bench/ifc_checks.py BRIEF.md FACTS.json` | Decides the IFC-level bounds of the plumbing and wiring briefs (`bim-05`…`bim-09`) from a facts JSON (schema in the module docstring), standard library only. Prints one result per check as JSON. Exit 0: no check failed (necessary, not sufficient); 1: a check failed, or the facts are missing or unreadable, which fails every declared bound; 2: the brief declares an unknown or malformed bound |
| `uv run --no-project --with ifcopenshell==0.9.0.post1 python -I bench/ifc_facts.py IN.ifc OUT.json` | Measures an IFC model into that facts JSON, in millimetres whatever the file's unit: elements with their systems and body centres, ports, connections, and clashes between distribution elements and walls (touching counts). Measures, never decides. Exit 0: facts written; 1: the IFC can't be read, nothing written; 2: usage. Blind spots in its docstring |
| `make check_docs` | Markdown lint — prints `SKIP` if `markdownlint-cli2` is not installed |
| `make check_links` | Link check, `#section` anchors included (`lychee.toml`; needs network) — prints `SKIP` if `lychee` is not installed. `lychee --offline --no-progress '**/*.md'` checks only local links and anchors, fast |
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
  excluded by default; tests needing IfcOpenShell are marked `@pytest.mark.ifc`.
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

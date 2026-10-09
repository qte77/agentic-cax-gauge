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

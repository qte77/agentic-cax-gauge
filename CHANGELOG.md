# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/), [Semantic Versioning](https://semver.org/).

<!-- scriv-insert-here -->

## [Unreleased]

## [0.1.0] - 2026-10-09

### Added

- **M1 scaffold (#15)**: `caxgauge` package (Python 3.12, uv), `trimesh` as a core
  dependency, `build123d` behind an optional `cad` extra. `make validate` runs ruff (format,
  lint incl. security), pyright strict, pytest and complexipy — the exact gate CI runs
  (`validate.yaml`). Markdown and link checks run the same `make` targets in CI with pinned, checksum-verified tools (the estate reusable workflow is blocked by this repo's Actions policy);
  `make check_docs` / `make check_links` print `SKIP`, never pass, when their tool is absent.
- `caxgauge` CLI entry point as an honest stub: exits 2 and states that nothing was checked
  until M2 ships.
- Governance: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `AGENT_LEARNINGS.md`,
  `AGENT_REQUESTS.md`, `.gitmessage`, and `.claude/rules/` (estate rules plus the new
  `verification-honesty.md`).

### Fixed

- One markdown defect in the plan found by the new lint (an unlabelled code block without
  blank lines).

## Docs arc (pre-0.1.0, PRs #1-#28)

Planning and research only, no code. Kept here so the history isn't lost:

- **Design and setup** (#1-#6, #10): README + licence, v0 scoping, the red-team that killed the "authoritative spec
  oracle" design and adopted render-first; a single plan of record with the handoff merged
  in, and an M2 parallel-worktree execution model.
- **Research** (#9, #13, #14, #19, #24, #28): CAx/BIM landscape — world models, specialized
  and fine-tuned LLMs, autoregressive generation, VLMs, the Fusion/Revit MCP ecosystem,
  LEAP71/PicoGK, IFC toolchain and standards (empirically verified), code-compliance
  ingestion, and a first-hand agentic-CAD case study. Citations checked against primary
  sources; anything that couldn't be is labelled unverified in place.
- **Plan corrections** (#21, #23, #26, #27): the reused `struct` check is file-integrity
  only, so trimesh is the real manifold check; CAx scope with the gate/inform inclusion test
  and a data-gated BIM milestone; merge mechanics and polyfetch notes brought up to date.
- **CI** (#11, #12, #20, #22): Dependabot with security grouping, CodeQL — guarded so it
  skips visibly, rather than failing, until Python files exist.
- **Tracking** (#18): milestone issues #15-#17, later #25 (BIM).

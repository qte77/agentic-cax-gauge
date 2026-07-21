---
title: P0b scaffold + P1 preflight — executable build plan
purpose: Turn the reframed render-first design into concrete, test-first tasks for the first two build phases
created: 2026-07-21
updated: 2026-07-21
validated_links: 2026-07-21
status: ready to build
---

**Status**: Ready. Depends on [`001-v0-scoping.md`](001-v0-scoping.md) (design, code/file map)
and [`002-polyfetch-integration.md`](002-polyfetch-integration.md) (render substrate
constraints). This plan sequences **P0b** (scaffold) and **P1** (the load-bearing
survivor) into executable tasks. Strict TDD, behaviour-level, no Gherkin.

## Why these two phases first

P1 is the piece that survived the red-team ([`../reviews/001-wedge-red-team.md`](../reviews/001-wedge-red-team.md)):
a cheap deterministic preflight that is *necessary-not-sufficient*, plus a browser-load
check. It needs no agent and no VLM, is testable from fixture STLs, and delivers value
standalone. P0b is the minimum scaffold to build P1 under the estate's quality gates.

## P0b — Scaffold (no product code)

| File | Content | Notes |
|---|---|---|
| `pyproject.toml` | Python `==3.12.*` (hard constraint, plan 001 §2), `uv`, ruff (incl. `S`/`ANN`/`D`), pyright strict, pytest + pytest-cov + hypothesis, complexipy (max 15). `build123d` and slicer behind an optional `cad` extra; polyfetch env-borrowed, **not** a dep | Mirror `../so101-biolab-automation/pyproject.toml` structure |
| `Makefile` | `setup`, `lint`, `type`, `test`, `validate` targets | Mirror estate |
| `.github/workflows/` | `lint` (ruff + markdownlint + lychee), `test` (pytest, stub-mode, no network) | Makes the merge gate meaningful; note the required-check name (see Risks) |
| `AGENTS.md` + `CLAUDE.md` (redirect) | Governance; copy *structure* from so101, not content | |
| `.claude/rules/` | `core-principles`, `context-management`, `compound-learning` (estate SoT) **+ a new `verification-honesty.md`** | See rule below |
| `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | Estate standard | scriv or Keep-a-Changelog |
| `src/caxgauge/__init__.py`, `tests/` | Package skeleton mirroring `src/` 1:1 | |
| `.gitignore`, `.markdownlint.jsonc`, `lychee.toml` | Copy estate configs; include the bwrap phantom-file `.gitignore` block | plan 001 §7 / ai-agents-research learning |

**New rule `verification-honesty.md`** (day-one guardrail, encodes the red-team kill
conditions): green is *necessary, not sufficient*; the system never emits a
"verified/correct" verdict from deterministic checks alone; the VLM annotates and never
gates; no bounded auto-critique loop with revert-on-break; clearances are two-sided
windows, never min-only.

## P1 — Preflight + viewer + browser-load (test-first)

### Modules

| File | Responsibility |
|---|---|
| `src/caxgauge/verify/preflight.py` | `preflight(mesh) -> PreflightResult`. Checks: **build-ok** (input parses to a solid/mesh), **watertight/manifold**, **bbox within envelope**, **volume/mass within band**. Returns a structured per-check pass/fail, explicitly labelled necessary-not-sufficient. Pure, no agent, no network |
| `viewer/index.html` | Static three.js + STLLoader. Loads a mesh from `?mesh=` query param; named camera presets (front/iso/top/right). On load failure it must **throw** (fire `pageerror`) — do not rely on a readable success flag (isolated-world caveat) |
| `src/caxgauge/verify/browser.py` | `browser_load_check(mesh) -> BrowserResult`. Serve the viewer on **`localhost`** (not `127.0.0.1` — polyfetch SSRF guard, plan 002 §2), load the mesh via env-borrowed polyfetch `render_session`, capture `console_errors` + `network_failures` + `pageerror`. A mesh that won't parse is a **hard fail**. Stub/SKIP when polyfetch/Chromium absent |

### Deterministic checks — implementation notes

- **Watertight/manifold**: dependency-free binary-STL integrity via `struct` (reuse the
  pattern in `../so101-biolab-automation/src/hardware/slicer/validate.py:98-184` and
  `../i3mega-pipettebot/tools/slicer/validate.py`), plus OCCT `is_valid()` when
  build123d is installed.
- **Silent boolean-fusion feature loss** (the headline value): caught deterministically
  only via a **topology-count / volume-band** assertion against expectation. P1 scope: a
  fixture where a feature was absorbed must fail either the volume band or a face/edge
  count assertion. Full manifest-diff regression is P4 (`verify/regression.py`), not here.
- **bbox / volume**: compute from the mesh; assert within the spec's envelope/band. Two
  sided where applicable.

### Reuse (do not rebuild) — from plan 001 §7

- Binary-STL struct integrity check and the `SKIP`-when-tool-absent contract.
- Stub-mode-by-default pattern (`../so101-biolab-automation/src/so101/arms.py:70-73`) so
  CI exercises all control flow with no build123d/Chromium installed.

## Verification (acceptance for this plan)

Fixture-driven, no agent, no VLM. Fixtures under `tests/fixtures/`:

1. **Good part** — passes all preflight checks; browser-load clean.
2. **Non-manifold mesh** — fails the watertight check; other checks may still run.
3. **Feature-absorbed mesh** (silent fusion loss) — fails the volume-band or
   topology-count assertion. *This is the headline test.*
4. **Oversize part** — fails the bbox/envelope assertion.
5. **Un-parseable mesh** — `browser_load_check` returns a hard fail via `pageerror`;
   assert the failure is caught (per plan 002: force the failure to confirm listeners
   fire; never assert three.js state via `page.evaluate`).
6. **Honesty test** — a part that passes preflight but is visibly wrong must NOT yield a
   "verified" verdict; `PreflightResult` is labelled necessary-not-sufficient.
7. **Stub-mode CI (primary gate)** — full path runs with no build123d, no Chromium;
   asserts the result shape and the necessary-not-sufficient labelling; `SKIP`s the
   tool-dependent legs cleanly.

Property tests (Hypothesis): a generated box of size X passes its own bbox assertion and
fails a deliberately perturbed one.

## Risks / preconditions

- **Ruleset required-check name is stale** (`codefactor.io` vs the actual `CodeFactor`);
  until corrected, PRs merge only via admin bypass. Track fixing it at the
  repo-baseline/template level (plan 001 §11 follow-ups).
- **polyfetch in-scope answer pending** — [polyfetch#144](https://github.com/qte77/polyfetch-scrape/issues/144)
  asks whether E2E of one's own app is supported. If "no", `browser.py` rests on an
  unsupported surface — but P1's preflight (non-browser) is unaffected, so build that
  first and treat `browser.py` as separable.
- **CAE leg still unresearched** — out of scope here; `verify/sim.py` stays an empty seam.

## Out of scope (later phases)

Generation, the human-driven loop, `DesignSpec`, regression diffing, slicer gate, VLM
annotation, GUI-driven CAD. Those are P2-P6 in plan 001 §9.

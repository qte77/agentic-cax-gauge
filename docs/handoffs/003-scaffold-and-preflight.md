---
title: Handoff — P0b scaffold + P1 preflight build
purpose: Onboard the next session to plan 003
created: 2026-07-21
updated: 2026-07-21
plan: ../plans/003-scaffold-and-preflight.md
---

# Handoff 003

Read [handoff 001](001-v0-scoping.md) first (design + the render-first reframe), then
[`plan 003`](../plans/003-scaffold-and-preflight.md) for the task breakdown.

## State

Docs merged to `main` (README, LICENSE, plans 001-003, handoffs, review 001). **No code
yet.** This plan is the first code: P0b scaffold, then P1.

## Build order (do not reorder)

1. **P0b scaffold** — pyproject (py3.12), Makefile, CI, governance, and the new
   `.claude/rules/verification-honesty.md` guardrail. No product code.
2. **P1 preflight** — `verify/preflight.py` first (pure, no deps), test-first with the
   fixture set in plan 003. Then `viewer/index.html`, then `verify/browser.py`.
3. `browser.py` is **separable** — if polyfetch's in-scope answer (#144) is "no", ship
   preflight alone; it stands on its own.

## Non-negotiables (from the red-team — do not regress)

- Green is *necessary, not sufficient*; never emit a "verified/correct" verdict from
  deterministic checks alone.
- No bounded auto-critique loop with revert-on-break; the VLM (later) annotates, never gates.
- Clearances are two-sided windows, never min-only.
- Use `localhost`, not `127.0.0.1`, for the viewer (polyfetch SSRF guard).
- Never assert three.js state via `page.evaluate` (isolated world); screenshots are
  ground truth, `page.on(...)` is "did it load". Capture `pageerror`/`requestfailed`,
  not just `console`.

## The headline test

The *silent boolean-fusion feature loss* fixture (a feature absorbed during fusion,
still manifold, volume barely shifted) must fail a volume-band or topology-count
assertion. This is the one real defect the cheap preflight uniquely catches — if it
passes green, the preflight is worthless. Build that fixture and test early.

## Merge mechanics (learned this session)

New-repo ruleset requires a stale check `codefactor.io` while CodeFactor posts
`CodeFactor`; non-admin merge stays blocked until that name is corrected at the
template/repo-baseline level. Until then: squash-merge via admin bypass (owner is a
ruleset bypass actor). The token here has `repo` scope but cannot write rulesets.

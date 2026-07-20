---
title: Handoff — agentic-cax-gauge v0 scoping
purpose: Onboard the next session to plan 001 and how to execute it
created: 2026-07-20
updated: 2026-07-20
plan: ../plans/001-v0-scoping.md
---

# Handoff 001

## Read this first

1. [`docs/plans/001-v0-scoping.md`](../plans/001-v0-scoping.md) — the approved plan. It
   contains a **complete code, file and source map**. You should not need to re-research
   the landscape or re-locate estate files. If you find yourself grepping sibling repos
   for CAD/slicer code, stop and read §7 of the plan instead.
2. This file — where things stand and what to do next.

## What this repo is

A harness that makes agent-generated CAx **verifiable**. An agent writes parametric CAD
code; a deterministic verifier gates it against a pre-declared, machine-checkable
`DesignSpec`; a bounded VLM critique runs only as a secondary pass.

One-line thesis: *coding agents write code well and reason about 3D space badly, so make
the geometry assert itself instead of asking the model to look at it.*

## State as of 2026-07-20

| Item | State |
|---|---|
| Remote | `https://github.com/qte77/agentic-cax-gauge` — public, `main`, one commit (`README.md`) |
| Local | `/workspaces/qte77/agentic-cax-gauge` — `origin` wired, `main` tracks `origin/main` |
| Branch | `docs/research-findings` — holds these two docs only |
| Code | **None.** No `src/`, no `pyproject.toml`, no scaffold, no CI |
| README | Untouched, still the GitHub initial commit |

Phase P0a is complete. Nothing else has been started.

## Next actions, in order

1. **Settle complement-vs-compete first — human decision, blocks P0b.** Analysis of
   [`earthtojake/text-to-cad`](https://github.com/earthtojake/text-to-cad) (plan §6.4.1)
   found an 8.6k-star, actively developed agent-skill package on the *same* build123d
   backend. The wedge survives — it has no pre-declared machine-checkable spec, no
   manifold/volume/interference checks, and no deterministic-gate-over-VLM ordering — but
   verification is its weakest area, the author has publicly said benchmarks are in
   progress, and that is the most plausible thing they ship next. Decide whether this repo
   is a rival harness, a verification layer that plugs into their pipeline, or an upstream
   contribution. This changes P3/P6 scope substantially.
2. **Then run `adversarial-distillation` on the surviving wedge.** Partial validation is
   done (§6.4.1) but not a full red-team. If it does not survive, rescope before P1 rather
   than after P3.
3. **P0b — scaffold.** `pyproject.toml` (Python 3.12 exactly — hard constraint, see plan
   §2), `Makefile`, CI, quality gates, governance files copied *in structure* from
   `../so101-biolab-automation`.
4. **P1 — `spec.py` + `verify/geometry.py`, test-first.** This is the load-bearing
   contribution. Build it before anything agentic; it is testable with fixture STLs and no
   LLM at all.

Do not start at P3 because it is the interesting part. The verifier is what makes the rest
meaningful.

## How to handle the plan

- **Phases are independently shippable.** Stop after any one and the repo still has value.
- **Deterministic before agentic.** P1 needs no LLM. If you are wiring an agent loop before
  the geometry asserts work, you are out of order.
- **Do not build a second VLM integration.** P5 is a thin adapter over `../vlm-toolkit`,
  which already exists and already names this estate's repos as consumers. Pin it — it is
  pre-`v0.1.0` with an unstable API.
- **Do not extract a shared CAD package** across so101/i3mega/this repo yet. The pattern
  has two instances; AHA says wait until it is stable here first (plan §11.4).
- **Stub-mode is mandatory, not optional.** Every backend and external-tool wrapper must
  degrade to an in-memory stub that logs what it would have done. This is what keeps CI
  green with no build123d/OpenSCAD/slicer installed, and it is the primary test gate.
- **TDD, behavior-level, no Gherkin.** Skip trivial tests on declarative models.

## Blockers and traps

- **CAE research is owed and must not be faked.** `docs/outlook-cae.md` does not exist
  because the research sweep failed twice — once off-task, once on a weekly rate limit
  resetting **2026-07-22 21:00 UTC**. Plan §11.1 lists exactly what to research. Writing
  that doc from memory would put unsourced claims into the corpus. Leave the gap until the
  sweep runs.
- **Coordinate frames.** CAD-frame vs machine-frame `+Y` already bit `i3mega-pipettebot`
  once and became an enforced rule there. Adopt that rule on day one, not after it bites
  again — plan §7.
- **P6 (GUI leg) is the weakest part.** No vendor claims unattended reliability; general
  computer-use agents sit at 47-82% on OSWorld and nobody has publicly done CAD GUIs. Keep
  it sandboxed, non-gating, and be willing to delete it.
- **Verify subagent findings before acting.** Estate experience is that sweeps return false
  negatives. This session had two research agents die on rate limits and one return
  off-task meta-text that looked like a result. Cross-check before trusting.

## Decisions already made — do not relitigate

Name (`agentic-cax-gauge` / `caxgauge`), standalone-repo relationship to the estate, v0
scope (CAD + deterministic + bounded VLM critique), CAE documented-only, GUI leg included
as experimental, Python 3.12, strict TDD. Rationale for each is in plan §2. Reopen only
with a concrete reason.

## Open question for the human

The plan assumes so101 and i3mega adopt this at P7, including rewriting
`so101-biolab-automation/docs/roadmap.md:47-58` to point here. That is a cross-repo change
to a repo with its own roadmap and should be confirmed before P7 lands, not assumed.

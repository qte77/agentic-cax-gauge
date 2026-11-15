---
title: Benchmark practice — what the literature and RDI ask of a benchmark, and where ours stands
purpose: Evidence behind plan §5 BENCH-3 and the 2026-11-13 re-gating of the benchmark rows; not needed to build
created: 2026-11-13
updated: 2026-11-15
validated_links: 2026-11-15
status: reference
---

# Benchmark practice

What published work and the AgentBeats organisers (Berkeley RDI) say a good benchmark needs,
compared with this repo's `bench/`. The decisions this informs live in
[`plans/001-v0.md`](../plans/001-v0.md) §5 (rows BENCH, BENCH-2, BENCH-BIM, BENCH-3), not
here. Everything below was read at its source unless marked "abstract only". Summaries are
in this project's own words. Quotes are short and marked.

## 1. Cornerstones

| # | Principle | Source |
|---|---|---|
| 1 | **Task validity:** a task is solvable "if and only if the agent possesses the target capability" | [ABC, arXiv 2507.02825](https://arxiv.org/abs/2507.02825) |
| 2 | **Outcome validity:** the check's verdict "truly indicates task success". In ABC's audit of ten agentic benchmarks, seven had flaws here, seven had task-validity flaws, and all had gaps in how they reported results | ABC |
| 3 | **Trivial baseline:** in ABC's audit, an agent returning empty answers scored 38% on one benchmark. A score means little without a measured floor | ABC |
| 4 | **Construct validity:** the score must be evidence for the claim made. Of 445 LLM benchmarks reviewed, 21.7% leave the measured phenomenon undefined | ["Measuring what Matters", arXiv 2511.04703](https://arxiv.org/abs/2511.04703) |
| 5 | **Statistics:** only 16% of those 445 report uncertainty or a statistical test | "Measuring what Matters"; [BetterBench, arXiv 2411.12990](https://arxiv.org/abs/2411.12990) (46 criteria across design, implementation, documentation and maintenance) |
| 6 | **Contamination:** score only on items a model can't have trained on, e.g. items released after its cutoff | [LiveCodeBench, arXiv 2403.07974](https://arxiv.org/abs/2403.07974); [LiveBench, arXiv 2406.19314](https://arxiv.org/abs/2406.19314) (abstract only) |
| 7 | **Coverage stated honestly:** pick a feasible subset and name what is missing | [HELM, arXiv 2211.09110](https://arxiv.org/abs/2211.09110) (abstract only) |
| 8 | **Run hygiene:** each run starts from a fresh state and is isolated; one config fully describes a run; the benchmark is a lightweight verifier that checks the participant's artifact itself; baseline participants ship with it; participants "may be tested on held-out tasks" | Berkeley RDI: [AgentBeats tutorial README, tag v1](https://github.com/RDI-Foundation/agentbeats-tutorial/tree/v1), [competition page](https://rdi.berkeley.edu/agentx-agentbeats.html) |
| 9 | **Documentation:** a datasheet stating motivation, composition, collection and intended use | [Datasheets for Datasets, arXiv 1803.09010](https://arxiv.org/abs/1803.09010) (abstract only) |

RDI publishes no rubric for judging benchmarks. Its example benchmark judges a debate with an
LLM, which this project's rule forbids (`.claude/rules/verification-honesty.md`), so only its
run-hygiene principles carry over.

## 2. CAD benchmarks

| Benchmark | Reference answers | Scoring |
|---|---|---|
| [Text2CAD, arXiv 2409.17106](https://arxiv.org/abs/2409.17106) | DeepCAD models with prompts written by a vision model and an LLM from renders; no human annotation | F1 on primitives, Chamfer distance, invalidity ratio, GPT-4V pairwise, a user study |
| [CAD-Recode, arXiv 2412.14042](https://arxiv.org/abs/2412.14042) | 1M procedurally generated sequences, checked for validity by a geometry kernel | Chamfer distance, IoU, invalidity ratio |
| [CADPrompt, arXiv 2410.05340](https://arxiv.org/abs/2410.05340) | 200 references hand-written by one CAD expert, checked against the target in Blender, mismatches returned to the expert | Point-cloud distance, compile rate; its authors call distance metrics "noisy" |
| [CADTests, arXiv 2605.07807](https://arxiv.org/abs/2605.07807) (abstract only) | — | Executable tests of the prompt's geometric and topological requirements |

Most CAD benchmarks score shape distance against one reference. This project has no reference
model. Its oracle is a closed-form bound plus a human looking at the render, which is closer
to CADTests' requirement checks.

## 3. Where this repo stands (2026-11-14)

- **Met:**
  - bounds are declared in each brief before any run, and are two-sided
  - no model judges; the human labels blind (`bench/blind.py`)
  - a fresh scratch directory per run; pinned model; spend caps
  - each artifact is checked directly
  - control parts on all 18 bounded briefs, known-good parts for 3 of them
    (`tests/test_bench_controls.py`)
  - a fixed review rubric (`bench/rubric.md`)
  - every band recomputed from its closed form (`tests/test_bench_bands.py`)
  - per-run provenance (`bench/provenance.py`), from the next run on
- **Open:** construct and task validity (every brief states its dimensions), no held-out
  briefs, no second rater, no uncertainty reported, no datasheet. The 30 pilot runs have no
  provenance, and it can't be backfilled.
- **An independent review (Fable, 2026-11-13)** judged the benchmark the wrong priority while
  no labels exist. It also argued that the plan's own target case is a part regenerated
  against a stable contract (plan §3.1 ICP), not one-shot briefs. Its sharpest point: blind
  labelling hides the design source, yet the real defects so far were found by reading it.
  Hence the rubric's `unsure`.

## 4. ArchLang's evaluation, the most developed one we found (read 2026-11-15)

[ArchLang](https://github.com/ChanMeng666/archlang) (see [landscape §3.7](landscape.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate))
measures whether a model writes valid, sound and intent-matching floor plans from a brief.
This is read from its `eval/` and `dataset/` READMEs and `eval/results.md`. What it does that
we don't yet do:

- **Version the ruler.** Every result is stamped with the judge's version. A rate is never
  compared across a judge change: fixing the judge alone moved its one-shot intent rate from
  9% to 50%, with no model change.
- **Separate the tool's dividend from the model's.** Tier L0 scores the model's first
  output; L1 re-scores it after deterministic fix and repair, with no model involved.
  Feedback loops (L2) are compared against equal-token-budget resampling, with the analysis
  pre-registered before the one live run.
- **Use infeasible briefs.** Some briefs can't be satisfied, and the correct answer is to
  say so and name the conflicting requirements. A plan that passes the validator anyway scores
  0, because it has quietly changed the user's numbers ("constraint laundering"). The
  conflict set is derived arithmetically, not asserted in prose.
- **Plant faults in CI.** Plans with known defects (a blocked doorway, an off-wall door,
  furniture through a wall) must be caught.
- **Be honest about contamination.** The eval briefs have been public in the repo, so they're
  called "a public regression fixture, not a holdout". A synthetic dataset (CC0) carries a
  fixed canary string so leakage into training data can be detected.
- **Fix the rubric before the grades,** keep a pre-registered second rater with human
  adjudication, and report Wilson intervals.

Its offline scorecard (judge v2, 26 briefs): 26/26 compile, 23/26 match intent, 4/26 are
lint-clean.

**Ideas this suggests here, recorded only:**

- an infeasible brief (bounds no part can meet) among the controls
- a gauge-version stamp in each run's provenance, so verdicts aren't compared across gauge
  changes
- planted-defect parts in the blind sheet
- calling the current public briefs a regression fixture, not a held-out set

Not read at source, not cited: the SWE-bench Verified announcement, CAD-Coder,
CAD-Assistant. An anonymous unpublished submission seen during the search is deliberately
left out.

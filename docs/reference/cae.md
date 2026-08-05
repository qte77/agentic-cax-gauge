---
title: CAE outlook — feasibility, trust boundary, and why the seam stays empty
purpose: The owed CAE research, so the deferred verify/sim.py seam rests on evidence rather than assumption
created: 2026-07-25
updated: 2026-07-25
validated_links: 2026-07-25
status: reference — research complete, no CAE work authorised
---

This is the research the plan owed (`001-v0.md` §12.1). It had failed twice — once off-task,
once on a rate limit — and the standing rule was that writing it from memory would put
unsourced claims in the corpus. Every claim below carries its source; claims that could not
be verified are labelled, not smoothed over.

**Read this before touching `verify/sim.py`.** Its headline finding contradicts the reason
the seam was reserved.

## 1. The verdict: the plan's hypothesis was wrong

Plan §4 reserved `verify/sim.py` on this reasoning:

> a CAE acceptance check ("peak stress under yield") is structurally identical to a geometry
> check ("bbox under 80mm") — a bound on a measured scalar.

**That is false, and the difference is exactly the one this project exists to respect.**

A bbox check measures the artifact directly: the mesh *is* the thing being measured, so
"passes" and "is within envelope" are the same statement modulo export bugs. A stress check
measures a scalar at the end of a chain of independent human judgements — mesh density,
boundary conditions matching the real load case, unit consistency across the input deck,
solver convergence, and material/turbulence model choice. **Any one of them can be wrong
while the solver exits 0 and returns a plausible number.**

This is not a hedge; it is why formal V&V standards exist. ASME V&V 20-2009 requires a
documented grid-convergence study across at least three mesh densities before a CFD or
heat-transfer result may be called validated ([V&V 20][vv20]), and the Method of
Manufactured Solutions exists because "the solver ran" does not establish that the
discretisation is even correct for the equation class ([MMS][mms]).

**So CAE sits on the render side of this project's trust boundary, not the preflight side.**
A geometry preflight is cheap, deterministic and trustworthy for what it covers. A CAE
result needs a human to judge whether the *setup* was valid before its number means
anything. Same relationship the render has to the human: it informs a decision, it does not
make one.

A CAE check can still be *reproducible* — same inputs, same number, that is just numerics —
and there are honest CAE-shaped checks that fit this project's stance: "did residuals
converge", "did the grid-convergence index stay under X%". Those are necessary-not-
sufficient checks about *the simulation*, not claims about the part. What does not fit is
`peak_stress < yield` as a pass/fail gate. That is the §3.1 false-confidence failure with
extra steps, and it would be the most dangerous instance of it in the project, because a
stress number carries far more unearned authority than a bounding box.

**Consequence for the seam:** keep `verify/sim.py` reserved — it still costs nothing — but
the rationale in plan §4 is corrected, and anything built there reports into the human
review artifact, never into the pass/fail verdict.

## 2. Solver feasibility — which are CI-viable

The good news: headless, licence-free CAE in CI is genuinely practical. Six of eight run on
a stock GitHub Actions Linux runner with no licence gate.

| Solver | Licence | Headless from Python | Install weight | CI-viable |
|---|---|---|---|---|
| [Gmsh][gmsh] | GPL-2.0+ w/ linking exception | Official API, `pip install gmsh` | ~36-42 MB wheel | **Yes — easiest by far** |
| [CalculiX][calculix] | GPL-2.0+ | `ccx` is a headless CLI; [`pycalculix`][pycalculix] adds model building | conda-forge, tens of MB | **Yes** (skip the CGX GUI) |
| [FEniCSx][fenicsx] | LGPL-3.0+ (Basix MIT) | Pure Python API, no GUI at all | conda-forge + PETSc/MPI | **Yes** — its own CI uses GH Actions |
| [OpenFOAM][openfoam] | GPL-3.0 | [`foamlib`][foamlib] (modern) or PyFoam (legacy) | Docker `-run` ~300 MB | **Yes** — upstream runs GH Actions |
| [SU2][su2] | LGPL-2.1 | Official `pysu2` SWIG wrapper | meson/ninja source build | **Yes**, with a build step |
| [Elmer][elmer] | LGPL-2.0 core, GPL-2.0 GUI/modules | [`pyelmer`][pyelmer] wraps solver + grid | Source build, standard toolchain | **Yes**, with a build step |
| [code_aster][codeaster] | GPL-3.0 / CECILL-C / Apache-2.0 / LGPL-3.0 | Python module since v15.4, but the practical path is the GUI-oriented Salome-Meca bundle | conda-forge exists; heavy | **Marginal** — no lightweight recipe found |
| [PyMAPDL][pymapdl] | Wrapper MIT; **MAPDL proprietary** | Yes, gRPC | Large container **plus a licence server** | **No** — [Ansys Student terms][ansysterms] do not permit this |

Note the licence split on Elmer (LGPL core, GPL GUI) — only the core matters headlessly.
PyMAPDL is the single hard stop: the wrapper being MIT is irrelevant when the solver needs a
paid licence.

**If CAE is ever built, start with Gmsh + CalculiX.** Smallest install, no build step, no
licence, and together they cover mesh generation plus linear-elastic FEA — which is the only
regime the literature below shows agents handling with any consistency.

## 3. LLM-driven CAE — what the reliability numbers actually say

Capability is real and improving. Reliability is the problem, and the two papers that
specifically measured it found the same failure shape this project was built around.

**The linchpin finding** ([arXiv:2408.13406][fea], verified directly — 1,120 controlled
trials, 7 role configurations × 4 tasks, AutoGen, linear-elastic FEA):

- The rebuttal/critic agent **endorsed rather than challenged outputs, agreeing 85-92% of
  the time, including on errors.**
- A **"verification-validation gap where executable but physically incorrect code passed
  undetected."**
- **"No agent combination successfully validated constitutive relations in complex tasks."**
- Adding reviewer agents *reduced* success via premature consensus; the best configuration
  was a minimal three-agent team.

Read that against plan §3.1. The red-team killed the bounded auto-critique loop on
first-principles reasoning about Goodhart selection. This is independent empirical
confirmation from a different domain: **LLM critics endorse rather than catch.** It is the
strongest external evidence the project has for its own core design decision, and it belongs
in the argument.

Reported capability, for calibration — note every benchmark is small:

| System | Result | Benchmark size | Source |
|---|---|---|---|
| MetaOpenFOAM | 85% pass rate | **8 tasks** | [arXiv:2407.21320][metafoam] (verified) |
| Foam-Agent 2.0 | 88.2% (vs 55.5% for MetaOpenFOAM on the same set) | 110 tasks | [arXiv:2509.18178][foamagent] |
| CAX-Agent | 92.7% completion, 84% zero-intervention | 50 tasks, explicitly "structurally simple geometries" — no nonlinear materials, no assemblies, no multiphysics | [arXiv:2605.15218][caxagent] |
| ALL-FEM | 71.8% correct code | 39 problems | [arXiv:2603.21011][allfem] |
| OpenFOAMGPT | **No quantitative benchmark** — qualitative case studies only. Authors state "human oversight remains crucial" | — | [arXiv:2501.06327][ofgpt] |

**Pattern:** 8-110 task benchmarks, 55-93% success depending on how simple the tasks are and
how many self-correction turns are allowed, and *not one* claims unsupervised production
reliability. Several explicitly disclaim it. Treat any future "agentic CAE" claim against
this baseline.

## 4. Guardrails practitioners actually use

Named, citable practice — useful if honest CAE-shaped checks are ever built:

- **Grid Convergence Index / Richardson extrapolation** — coarse/medium/fine triplet,
  residuals dropped ≥3 orders of magnitude, prism-layer settings held constant across grids
  ([GCI][gci]).
- **ASME V&V 20-2009** — the standard requiring the above before calling a result validated
  ([V&V 20][vv20]).
- **Method of Manufactured Solutions** — solve a modified PDE with a known exact solution,
  confirm the theoretical order of accuracy under refinement; catches solver bugs
  independent of the application case ([MMS][mms]).
- **ERCOFTAC Best Practice Guidelines** — industry-consensus coverage of numerical error,
  turbulence-model choice, user error, and required sensitivity tests ([ERCOFTAC][ercoftac]).

**Gap, stated rather than filled:** no named, citable methodology was found for
unit-consistency checking or boundary-condition auditing — only generic advice. If CAE is
built, that is an unsolved area, not an oversight in this sweep.

## 5. Agent-facing simulation tooling

Thin and immature — none is a dependency candidate.

| Project | State |
|---|---|
| [FEA-MCP][feamcp] | MIT, Windows-only, ETABS/LUSAS. Its own roadmap admits materials, loads, BCs and analysis execution are missing — geometry only |
| [openfoam-mcp-server][ofmcp] | ~75% operational by its own notes; OpenFOAM 12 integration incomplete; framed as education, not production |
| [CFD-copilot][cfdcopilot] | Peer-reviewed; MCP used to separate LLM reasoning from tool execution |
| Marketplace "CFD/FEA skills" (mcpmarket, SkillsMP, skills.rest) | **UNVERIFIED** whether these execute a solver or are prompt scaffolding — a fetch was rate-limited before confirmation |

Method note, consistent with [`landscape.md`](landscape.md) §3.0: marketplace listings
surfaced FEA/CFD tools that arXiv and GitHub searches did not. Search them every time.

## 6. Topology optimisation and DoE

Active 2026 arXiv cluster, all proof-of-concept: [TO-Master][tomaster] (LLM agent over
JAX-FEM sensitivity analysis), [TopOptAgents][topopt] (six-agent self-refinement), and
[LLM-as-SIMP-controller][simp]. **No benchmark sizes or success rates were surfaced for any
of the three** — abstracts only. Nothing here is decision-relevant yet.

## 7. Unverified — do not cite these as settled

- **FoamGPT**'s reported numbers — repo and title confirmed, paper content not fetched
  ([repo][foamgpt]).
- **PDE-Agents** ~60% one-shot rising to 97.8% with self-correction — secondary summary
  only, primary PDF 404'd.
- **code_aster / Salome-Meca** container size — no figure found.
- Whether **marketplace CFD/FEA skills** run a solver or only scaffold prompts — fetch
  rate-limited.
- **TO-Master / TopOptAgents / SIMP-controller** benchmark sizes and success rates.

[vv20]: https://www.osti.gov/servlets/purl/1368927
[mms]: https://inis.iaea.org/records/2z3a8-jfr18
[gci]: https://cfd.university/blog/how-to-manage-uncertainty-in-cfd-the-grid-convergence-index/
[ercoftac]: https://www.ercoftac.org/publications/ercoftac_best_practice_guidelines/
[gmsh]: https://pypi.org/project/gmsh/
[calculix]: https://www.calculix.de/
[pycalculix]: https://pypi.org/project/pycalculix/
[fenicsx]: https://github.com/FEniCS/dolfinx
[openfoam]: https://openfoam.org/licence/
[foamlib]: https://github.com/gerlero/foamlib
[su2]: https://su2code.github.io/docs/Python-Wrapper-Build/
[elmer]: https://github.com/ElmerCSC/elmerfem/blob/devel/license_texts/ElmerLicensePolicy.md
[pyelmer]: https://github.com/nemocrys/pyelmer
[codeaster]: https://github.com/conda-forge/code-aster-feedstock
[pymapdl]: https://github.com/ansys/pymapdl
[ansysterms]: https://www.ansys.com/academic/terms-and-conditions
[fea]: https://arxiv.org/abs/2408.13406
[metafoam]: https://arxiv.org/abs/2407.21320
[foamagent]: https://arxiv.org/pdf/2509.18178
[caxagent]: https://arxiv.org/html/2605.15218
[allfem]: https://arxiv.org/abs/2603.21011
[ofgpt]: https://arxiv.org/abs/2501.06327
[foamgpt]: https://github.com/csml-rpi/FoamGPT
[feamcp]: https://github.com/GreatApo/FEA-MCP
[ofmcp]: https://github.com/webworn/openfoam-mcp-server
[cfdcopilot]: https://arxiv.org/html/2512.07917v1
[tomaster]: https://arxiv.org/pdf/2607.01812
[topopt]: https://arxiv.org/abs/2605.23273
[simp]: https://arxiv.org/html/2603.25099

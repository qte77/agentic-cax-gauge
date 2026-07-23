---
title: Landscape — evidence, competitors, backend choice, contribution stance
purpose: The research behind the design decisions, split out of plan 001 so the plan stays a plan
created: 2026-07-20
updated: 2026-07-23
validated_links: 2026-07-20
status: reference — dated, not needed to build
---

Extracted from [`../plans/001-v0.md`](../plans/001-v0.md) (§6, §12) on
2026-07-23 so the plan holds the design and this holds the evidence. Verdicts here were
**re-checked against the render-first reframe** — several entries previously recorded
adoptions that the red-team (distilled in [`../plans/001-v0.md`](../plans/001-v0.md) §3.1)
later killed. Where a source's technique was rejected, that is now stated.

Landscape sweeps are dated. Treat the competitive picture (§3) as provisional — the
original sweep missed an 8.6k-star direct competitor.

## 1. Why VLM spatial judgment cannot be trusted

This is the load-bearing evidence for the whole project: it is why the model is advisory
and the human decides.

| Finding | Evidence | ID |
|---|---|---|
| VLMs fail elementary geometry | 58% on overlapping shapes; failure is in the language decoder, not vision encoder | [arXiv:2407.06581][blind] |
| Near-chance on visual perception | Humans 95.7% vs best VLM (GPT-4V) 51.3% across 14 CV tasks | [arXiv:2404.12390][blink] |
| Generic CoT does not help | Standard CoT/self-consistency/ToT fail on spatial; explicit cognitive maps do help | [arXiv:2412.14171][vsi] |
| Root cause is data, not architecture | 2B synthetic 3D-VQA examples beat GPT-4V on distance/size | [arXiv:2401.12168][spatialvlm] |
| Tokenization mismatch | Continuous 3D geometry tokenized sequentially — prohibitive token counts or lossy encodings | [arXiv:2504.05786][tokensurvey] |
| No mental rotation ability | VLMs lack analog imagery-based rotation entirely, unlike humans | [Hyperphantasia][hyper] |

## 2. Mitigations — what we adopt, and what the red-team rejected

**Corrected 2026-07-23.** The pre-red-team version of this table recorded "Yes" against
the bounded auto-critique loop, the revert-on-break guard and the iteration cap. All three
were killed: a deterministic gate that is authoritative-but-blind, with revert-on-break,
*selects for gaming* (an honest fix that risks a deterministic regression gets discarded;
a numerically-safe hack survives). See [`../plans/001-v0.md`](../plans/001-v0.md) §3.1.

| Technique | Result | Verdict |
|---|---|---|
| Render + VLM verify loop | CADCodeVerify +7.3% geometric accuracy; CADPrompt benchmark | **Split.** Render adopted — and *promoted* to the primary gate (M2). The VLM *verify loop* rejected; the VLM annotates only — [arXiv:2410.05340][cadcodeverify] |
| Visual self-refinement | Query2CAD 53.6% -> 76.7% success, training-free | **Adopted human-driven only.** Iteration is a human looking at the render, not an autonomous refine loop — [arXiv:2406.00144][query2cad] |
| Revert-on-break guard | 3DCodeBench restores last-good state if a fix breaks executability | **REJECTED.** Selects for gaming against a blind gate. Retained only as regression *reporting* (`verify/regression.py` diffs vs last-good and surfaces it; it never auto-reverts) — [arXiv:2606.01057][3dcodebench] |
| Iteration cap = 3 | Quality plateaus/degrades after ~3 iterations without human-in-loop | **Moot.** There is no auto-loop to cap. The finding still supports keeping the human in the loop — [Planner-Actor-Critic][pac] |
| Solver-grounded validation | LLM proposes, parametric constraint solver verifies geometric validity | **Downgraded from "the core thesis" to one cheap layer.** Deterministic checks are necessary, not sufficient — they are blind to the dominant defect class — [arXiv:2606.31252][embodiedcad] |
| Constraint-status post-training | Autodesk scores sketch constraint status to fix under-constrained output | Assess later — [Autodesk][autodesk] |
| Retrieval of parametric templates | Seek-CAD retrieves from 10K-model corpus as in-context examples | Assess later — [arXiv:2505.17702][seekcad] |
| Correction accuracy | CADReview/ReCAD 73% vs 41.5% raw GPT-4o | Reference — [arXiv:2505.22304][cadreview] |
| Simulation in the loop | Physics-in-the-Loop embeds FEA in Generate-Simulate-Refine | Defer to CAE leg — [arXiv:2605.19717][physicsloop] |

## 3. Competitive landscape

### 3.1 Backend decision

| Tool | Verdict | Why |
|---|---|---|
| **build123d** | **Adopt — primary** | Apache-2.0, headless, Pythonic; already the estate standard in both consumer repos |
| **OpenSCAD** | **Adopt — fallback** | Headless CLI export; already the fallback in `so101` |
| CadQuery | Assess | Apache-2.0, larger LLM training corpus than build123d — revisit if codegen quality disappoints |
| FreeCAD Python API | Assess | `FreeCADCmd --console` headless; verbose, less training data |
| pythonocc-core | Assess | Low-level OCCT escape hatch |
| Onshape API | Assess | REST is tool-calling friendly; FeatureScript is niche/proprietary |
| Blender bpy | Hold | Mesh/procedural, not parametric BREP — wrong domain for manufacturing CAD |
| SolidPython | Hold | Transpiles to OpenSCAD; no advantage over using build123d directly |
| Fusion 360 API | Hold | Desktop-app dependent; new Automation API is metered and thin on training data |

Sources: [CadQuery][cadquery], [build123d][build123d], [OpenSCAD][openscad],
[FreeCAD][freecad], [pythonocc][pythonocc], [Onshape][onshape], [bpy][bpy],
[SolidPython][solidpython], [Fusion Automation][fusion].

### 3.2 Adjacent projects

| Project | What it does | Overlap |
|---|---|---|
| [Zoo / KittyCAD][zoo] | Text-to-CAD to parametric B-rep, own KCL geometry engine, Design Studio OSS. Most mature commercial. Publicly discloses **no** formal render/solver/simulation verification loop — thumbs-up/down only | High on capability, low on verification |
| [AdamCAD][adam] | YC W25, OSS CADAM (WASM/OpenSCAD backend), $4.1M seed | Medium |
| [Backflip AI][backflip] | Scan-to-parametric-CAD, $30M raised, ex-Markforged | Medium, adjacent problem |
| [CAD-Assistant][cadassistant] | Tool-augmented VLLM driving FreeCAD Python API | High conceptual overlap |
| [cad-agent][cadagent] | build123d + MCP, VTK-rendered PNG self-correction | **Highest overlap** |
| [openscad-agent][openscadagent] | Claude-Code-powered generate/render/self-correct + STL manifold validation | **Highest overlap** |
| [BlenderLLM][blenderllm] | Fine-tuned Qwen2.5-Coder-7B + CADBench | Low |
| [ScadLM][scadlm] | Hackathon agentic text-to-OpenSCAD; authors report feedback approaches underperformed | Low, but a cautionary data point |
| [MecAgent][mecagent] | NL to CAD macros for SolidWorks/CATIA/Fusion — API/macro, not vision | Medium |

**Honest read, corrected 2026-07-23.** `cad-agent` and `openscad-agent` already do
generate-render-self-correct. The pre-red-team version of this section claimed the
differentiator was "the pre-declared machine-checkable spec and deterministic gate
ordering" — **that claim is dead** (plan §3). What remains is not a moat: a correct,
honest internal instrument that refuses to overclaim. That is fine, because positioning is
estate-first (plan §2) and this is not competing with text-to-cad.

### 3.3 `earthtojake/text-to-cad` — the closest existing project

Analysed 2026-07-20. **The initial research sweep missed it.** Treat it as the primary
competitive reference.

| Attribute | Value |
|---|---|
| Scale | 8.6k stars, 984 forks, 314 commits, MIT, release 0.3.9 on 2026-07-10 |
| Form | A **Claude Code / Codex agent-skill package**, not an app or MCP server (`npx skills install earthtojake/text-to-cad`) |
| Backend | **build123d over OpenCascade** — real B-rep, same primary backend this plan chose |
| Scope | CAD + DXF drawings + URDF/SDF/SRDF robotics + part sourcing (`step.parts`, 12k+ STEP catalog) + G-code slicing + SendCutSend fabrication upload + local `cad-viewer` |
| Trajectory | ~1.1k stars April 2026 to 8.6k July 2026. Solo-authored, actively developed |

Its SKILL.md mandates a 10-step workflow including a prose "CAD brief" (dims, units,
coordinate convention, validation targets), source-of-truth discipline (edit Python, never
exported artifacts), geometric validation via `scripts/inspect`, and a mandatory PNG/GIF
snapshot after every STEP change.

**What it already has deterministically** (`cadpy/analysis.py`, `cadpy/validators.py`):
`assert_close(actual, expected, tol, label)`, `assert_bbox_coordinate`, `assert_bbox_span`,
`assert_selector_count` (face/edge/shape counts), axis-alignment facts, and
`selector_manifest_diff` for topology drift between versions. This is genuine non-LLM
geometric checking.

**What it does not have:** manifold/watertight as a coded check ("watertight" appears only
as ungraded checklist prose in `benchmarks/*.md`), volume/mass bounds, interference between
bodies, or slicer printability as a blocking gate (only an isolated manual `--dry-run` in a
separate `gcode` skill, explicitly "diagnostic only").

> **Read this gap carefully.** Pre-red-team, these absences were written up as *our wedge*.
> They are not. The red-team showed a pre-declared spec does not deliver broad correctness,
> and that the "independent spec" is fiction when one intelligence authors both spec and
> geometry. The absences are still real, and the cheap ones (watertight, volume band) are
> worth having — as a necessary-not-sufficient preflight, not as a claim to beat them.

**External corroboration of the real defect class:** an HN commenter reported generated
parts where "gussets overlap the holes and make a part that cannot be used" and questioned
whether through-holes actually pass through — precisely the local/unforeseen class that
*no* deterministic check catches, and the reason the render is the primary gate. Author's
reply: *"Working on benchmarks at the moment!"* ([HN][hn]).

**Adopt from it:**

- `selector_manifest_diff` — cheap deterministic regression check for unintended topology
  change between iterations. Directly reusable in `verify/regression.py` (M4).
- `assert_close` / `assert_bbox_coordinate` / `assert_bbox_span` — clean tolerance-assertion
  shape to mirror in `verify/preflight.py` (M2). *(Pre-reframe this said `verify/geometry.py`,
  a module the reframe deleted.)*
- "Edit source, never exported artifacts" — single-source-of-truth discipline; enforced here
  by `.gitignore`.
- Catalog-check-before-generate (`step.parts`) — do not model what you can buy.
- Their `benchmarks/*.md` format (prose prompt + explicit checklist with dims, counts,
  "exactly one watertight solid") is a good template for authoring regression specs.
- The HN failure modes are concrete target cases — for the *render*, not the preflight.

### 3.4 CAD MCP servers

| Server | Stars | Note |
|---|---|---|
| [ahujasid/blender-mcp][blendermcp] | 23.1k | Most adopted CAD-adjacent MCP; mesh domain |
| [neka-nat/freecad-mcp][freecadmcp] | ~1.4k | Document CRUD, code exec, FEM/CalculiX |
| [quellant/openscad-mcp][openscadmcp] | 116 | FastMCP, 80%+ coverage |
| [hedless/onshape-mcp][onshapemcp] | 109 | 45 tools, 471 tests |
| [pzfreo/build123d-mcp][build123dmcp] | 31 | **Closest to our stack** — AST-sandboxed exec, render/measure/printability tools |
| [daobataotie/CAD-MCP][cadmcp] | 451 | AutoCAD/GstarCAD/ZWCAD, Windows-only |

No CAD servers exist in the official MCP servers repo — the ecosystem is entirely
third-party.

### 3.5 GUI automation state of the art (context for the deferred GUI leg)

| System | Benchmark | ID |
|---|---|---|
| Claude computer use | OSWorld ~82.3% reported for Opus 4.7; vendor recommends sandboxed VM | [docs][ccu] |
| OpenAI CUA / Operator | 38.1% OSWorld at launch; folded into ChatGPT agent Aug 2025 | [openai][cua] |
| UI-TARS-2 | 47.5% OSWorld, 88.2% Online-Mind2Web; screenshot-only | [arXiv:2509.02544][uitars2] |
| Agent S3 | 66% OSWorld, 72.6% with Behavior Best-of-N | [github][agents] |
| OmniParser v2 | 39.5% ScreenSpot Pro grounding; pure-vision, no DOM | [github][omniparser] |

**Gap confirmed:** no mature publicly documented screenshot-vision agent drives FreeCAD,
Fusion or SolidWorks GUIs. Commercial CAD AI uses native API/macro hooks. This is why the GUI leg, if ever built,
would target to *browser*-based CAD via DOM selectors, which removes the pixel-guessing
failure mode entirely. The GUI leg is deferred outright — plan §5.

## 4. Upstream contribution stance

**Decided 2026-07-20: issue-first probe, commit no code yet.** Ask
`earthtojake/text-to-cad` what would actually help before writing anything. Rationale:
solo maintainer already carrying 12 open PRs, so unsolicited large PRs likely stall; their
answer informs scope; costs nothing.

**Offerable today (exists, battle-tested):**

| Asset | Source | Their gap |
|---|---|---|
| Headless slicer printability gate | `../so101-biolab-automation/src/hardware/slicer/validate.py:1-275`, `../i3mega-pipettebot/tools/slicer/validate.py:77-132` | Their `gcode` skill has only a diagnostic `--dry-run`, explicitly not wired as a gate |
| ~20 real parametric parts with engineering constraints (payload budget, Z-envelope) | `../so101-biolab-automation/src/hardware/parts.json`, `../i3mega-pipettebot/tools/cad/parts.json` | Their `benchmarks/` are 10 synthetic prompts |
| Coordinate-frame inversion writeup (CAD `+Y` vs machine `+Y`) | `../i3mega-pipettebot/.claude/rules/cad-script-conventions.md`, `AGENT_LEARNINGS.md:7-18` | Relevant to their URDF/robotics output |

**Deliberately withheld: the benchmark grader.** Their `benchmarks/*.md` carry test-case
checklists with no grading script, and the author has publicly said benchmarks are in
progress. Reconsider only as a deliberate strategic choice, not as incidental goodwill.

**Not contributable:** the qte77 operating model, governance scaffolding, and `gha-*`
actions. Pushing estate governance into a third-party OSS project reads as self-promotion,
not help.

**License note:** estate repos are Apache-2.0; `text-to-cad` is MIT. Any contribution means
relicensing our own code to MIT. Permissible as copyright holder, but must be deliberate
and stated in the PR.

## Sources

| Source | Content |
|---|---|
| [arXiv:2407.06581][blind] | VLMs fail elementary geometric tasks |
| [arXiv:2404.12390][blink] | BLINK — humans 95.7% vs GPT-4V 51.3% |
| [arXiv:2412.14171][vsi] | VSI-Bench — CoT does not fix spatial reasoning |
| [arXiv:2401.12168][spatialvlm] | SpatialVLM — synthetic 3D-VQA data |
| [arXiv:2504.05786][tokensurvey] | 3D geometry tokenization mismatch survey |
| [Hyperphantasia][hyper] | Mental rotation absent in VLMs |
| [arXiv:2410.05340][cadcodeverify] | CADCodeVerify — render feedback, +7.3% |
| [arXiv:2406.00144][query2cad] | Query2CAD — 53.6% to 76.7% |
| [arXiv:2606.01057][3dcodebench] | 3DCodeBench — revert-on-break guard (rejected here) |
| [Planner-Actor-Critic][pac] | Quality plateaus after ~3 iterations |
| [arXiv:2606.31252][embodiedcad] | Embodied CAD — solver-grounded verification |
| [arXiv:2505.22304][cadreview] | CADReview/ReCAD — 73% correction accuracy |
| [arXiv:2504.13178][autodesk] | Autodesk constraint-solver post-training |
| [arXiv:2505.17702][seekcad] | Seek-CAD — retrieval of parametric templates |
| [arXiv:2605.19717][physicsloop] | Physics-in-the-Loop — FEA in agent loop |
| [arXiv:2505.08137][cadsurvey] | Survey: LLMs for CAD |
| [arXiv:2409.17106][text2cad] | Text2CAD — NeurIPS 2024 |
| [arXiv:2505.19713][cadcoder] | CAD-Coder — text to CadQuery, CoT+RL |
| [arXiv:2412.13810][cadassistant] | CAD-Assistant — VLLM driving FreeCAD API |
| [arXiv:2412.19663][cadgpt] | CAD-GPT — spatial-reasoning-enhanced MLLM |
| [arXiv:2105.09492][deepcad] | DeepCAD — foundational dataset |
| [arXiv:2411.04954][cadmllm] | CAD-MLLM — multimodal to CAD |
| [earthtojake/text-to-cad][texttocad] | Closest existing project — 8.6k-star build123d agent-skill package |
| [HN discussion][hn] | User-reported geometry failures (gusset/hole overlap); author confirms benchmarks unfinished |
| [zoo.dev][zoo] | Most mature commercial text-to-CAD |
| [cad-agent][cadagent] | build123d + MCP render self-correction |
| [openscad-agent][openscadagent] | Claude-Code generate/render/correct + manifold check |
| [build123d-mcp][build123dmcp] | Closest MCP to our stack |
| [UI-TARS-2][uitars2] | 47.5% OSWorld, screenshot-only |
| [Claude computer use][ccu] | Vendor docs, sandboxing guidance |

[blind]: https://arxiv.org/abs/2407.06581
[blink]: https://arxiv.org/abs/2404.12390
[vsi]: https://arxiv.org/abs/2412.14171
[spatialvlm]: https://arxiv.org/abs/2401.12168
[tokensurvey]: https://arxiv.org/abs/2504.05786
[hyper]: https://arxiv.org/pdf/2507.11932
[cadcodeverify]: https://arxiv.org/abs/2410.05340
[query2cad]: https://arxiv.org/abs/2406.00144
[3dcodebench]: https://arxiv.org/abs/2606.01057
[pac]: https://dl.acm.org/doi/10.1145/3772363.3798904
[embodiedcad]: https://arxiv.org/abs/2606.31252
[cadreview]: https://arxiv.org/abs/2505.22304
[autodesk]: https://arxiv.org/pdf/2504.13178
[seekcad]: https://arxiv.org/abs/2505.17702
[physicsloop]: https://arxiv.org/abs/2605.19717
[cadsurvey]: https://arxiv.org/abs/2505.08137
[text2cad]: https://arxiv.org/abs/2409.17106
[cadcoder]: https://arxiv.org/abs/2505.19713
[cadassistant]: https://arxiv.org/abs/2412.13810
[cadgpt]: https://arxiv.org/abs/2412.19663
[deepcad]: https://arxiv.org/abs/2105.09492
[cadmllm]: https://arxiv.org/abs/2411.04954
[texttocad]: https://github.com/earthtojake/text-to-cad
[hn]: https://news.ycombinator.com/item?id=47970497
[cadquery]: https://github.com/CadQuery/cadquery
[build123d]: https://github.com/gumyr/build123d
[openscad]: https://github.com/openscad/openscad
[freecad]: https://github.com/FreeCAD/FreeCAD
[pythonocc]: https://github.com/tpaviot/pythonocc-core
[onshape]: https://onshape-public.github.io/docs
[bpy]: https://docs.blender.org/api/current
[solidpython]: https://github.com/SolidCode/SolidPython
[fusion]: https://aps.autodesk.com/apis-and-services/fusion-automation-api
[zoo]: https://zoo.dev
[adam]: https://github.com/Adam-CAD/CADAM
[backflip]: https://backflip.ai
[cadagent]: https://github.com/Svetlana-DAO-LLC/cad-agent
[openscadagent]: https://github.com/iancanderson/openscad-agent
[blenderllm]: https://github.com/FreedomIntelligence/BlenderLLM
[scadlm]: https://github.com/KrishKrosh/ScadLM
[mecagent]: https://mecagent.com
[blendermcp]: https://github.com/ahujasid/blender-mcp
[freecadmcp]: https://github.com/neka-nat/freecad-mcp
[openscadmcp]: https://github.com/quellant/openscad-mcp
[onshapemcp]: https://github.com/hedless/onshape-mcp
[build123dmcp]: https://github.com/pzfreo/build123d-mcp
[cadmcp]: https://github.com/daobataotie/CAD-MCP
[ccu]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
[cua]: https://openai.com/index/computer-using-agent/
[uitars2]: https://arxiv.org/abs/2509.02544
[agents]: https://github.com/simular-ai/Agent-S
[omniparser]: https://github.com/microsoft/OmniParser

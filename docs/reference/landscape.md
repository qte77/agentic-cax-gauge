---
title: Landscape — evidence, competitors, backend choice, contribution stance
purpose: The research behind the design decisions, split out of plan 001 so the plan stays a plan
created: 2026-07-20
updated: 2026-09-10
validated_links: 2026-09-10
status: reference — dated, not needed to build
---

Extracted from [`../plans/001-v0.md`](../plans/001-v0.md) (§6, §12) on
2026-07-23 so the plan holds the design and this holds the evidence. Verdicts here were
**re-checked against the render-first reframe** — several entries previously recorded
adoptions that the red-team (distilled in [`../plans/001-v0.md`](../plans/001-v0.md) §3.1)
later killed. Where a source's technique was rejected, that is now stated.

Landscape sweeps are dated. The competitive picture (§3) was **re-swept 2026-07-25** across
agent-skill and plugin marketplaces — the channel the original sweep never searched, which
is how it missed a then-8.6k-star direct competitor. That gap is now closed and §3.0 records
what was searched. Star counts still rot; the verdicts are the durable part.

**Extended 2026-09-10** across four technique dimensions this plan had not surveyed —
world models, specialized/fine-tuned LLMs, autoregressive generation, and VLM applications —
each checked against both CAx and BIM. New CAx findings landed in §3.2 and §3.5. BIM had no
prior coverage at all; §3.7 is the first pass and reframes "BIM" as three separate
verification problems rather than one adjacent domain.

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

**Cross-domain corroboration, 2026-09-10.** Text2BIM (§3.7) — a different domain entirely,
BIM generation checked by a deterministic rule engine, not a VLM — independently caps its
automated Reviewer/Programmer fix loop at 3 iterations before falling back to a human. Same
number, same reason, unrelated codebase. The iteration-cap finding is now corroborated
twice, not a CAx-specific artifact.

## 3. Competitive landscape

### 3.0 Sweep coverage — what was searched, and what was not

Recorded so the next sweep does not redo the same ground. Re-swept 2026-07-25.

**Searched, productive:** agent-skill and plugin marketplaces — skills registries (`npx
skills`), `lobehub.com/skills`, `skillsmp.com`, `mcpmarket.com`, `claudemarketplaces.com`,
`claudeskills.info`, `explainx.ai`, the OpenClaw skills registry, NVIDIA `skills`,
`cursor.directory`, awesome-list aggregators, Product Hunt. This channel produced every new
finding below. **It is the channel that matters** — parametric-CAD agent tooling now ships
predominantly as agent skills, not as apps, libraries, or MCP servers, which is precisely
why an arXiv+GitHub+MCP-registry sweep misses it.

**Searched, empty:** `cursor.directory` (no CAD verification plugin); NVIDIA `skills` (only
a format converter); no marketplace has a geometry-verification category distinct from the
generate-and-render skills. `cadskills.xyz` is `text-to-cad`'s own marketing site, not a
separate project.

**Known gap:** `clawd-maf/cad-agent` on the OpenClaw registry could not be diffed against
the already-catalogued `Svetlana-DAO-LLC/cad-agent` — it lives inside a monorepo with no
standalone source. Assume duplicate until shown otherwise. Two entries below
(`drawing-agent.com`, CADSmith) are recorded from marketing copy and an abstract
respectively, not from source, and are labelled as such.

**2026-09-10 technique sweep.** Searched arXiv + GitHub (not marketplaces this time) across
four dimensions — world models, specialized/fine-tuned LLMs, autoregressive generation,
VLMs — each against both CAx and BIM, plus a direct check of the Autodesk/Fusion vendor
ecosystem (official Claude connector + community MCP servers). **Searched, empty:** "world
model" as a named technique inside any CAD or BIM verification pipeline — the term stays
confined to robotics/embodied AI (Genie, NVIDIA Cosmos, per search results — not
independently fetched from DeepMind's or NVIDIA's own pages this session); no CAD/BIM-specific
instantiation found. New findings in §3.2, §3.5, §3.7.

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

Added by the 2026-07-25 marketplace sweep. All of these ship as agent skills:

| Project | What it does | Overlap |
|---|---|---|
| [jdilla1277/agentcad][agentcad] | build123d/CadQuery CLI + MCP. OCCT validity + free-edge count, four-view PNG every run, human-only review viewer | **Highest — see §3.4** |
| [flowful-ai/cad-skill][cadskill] | CadQuery skill; `--strict` fails on non-watertight via trimesh; 4-6 view PNG shown to the user before finalising | High |
| [drawing-agent.com][drawingagent] | 2D drawing/DXF to build123d; 8-angle + cross-section render, Gemini compares render to source drawing, up to 10 auto-iterations. No documented watertight/mass check. *Marketing copy only — no public source* | Medium |
| [CADSmith][cadsmith] | Academic. OCCT bbox/volume/solid-validity checks **plus** an independent VLM "judge" for holistic assessment | Medium-high conceptually |
| [rawwerks/VibeCAD][vibecad] · [mfranzon/render][mfrender] · [mitsuhiko/agent-stuff][mitsuhiko] | build123d/OpenSCAD skills with render-to-PNG visual verification; mitsuhiko's mandates human visual confirmation. None check watertight/volume | Medium |
| [EdwinjJ1/3d-print-skill][printskill] | manifold3d watertight/normals/volume/degenerate/size checks — **and no render step at all**. The mirror image of the skills above | Low-medium |

**Honest read, corrected 2026-07-25.** The differentiator is now **one thing, and it is
thin**: the epistemic framing. Generate-render-self-correct is commodity — `cad-agent`,
`openscad-agent` and half the skills above do it. Deterministic geometry checking is
commodity — `agentcad`, `cad-skill` and `3d-print-skill` do it. **Nobody found in two sweeps
labels a passing check as necessary-but-not-sufficient, and nobody reports an unsupplied
bound as `SKIP` rather than silently passing.** That is the whole remaining delta.

Note the population splits cleanly into render-only skills and check-only skills, with
`agentcad` and `cad-skill` the only two doing both. That combination — not the checks, not
the render — is the thesis, and it is now occupied. The consequence is not "stop": it is
that *the honesty is the product*, so weakening it (plan §3.1 LOSES-IFF) does not leave a
weaker tool, it leaves a redundant one. Positioning stays estate-first (plan §2).

**Added by the 2026-09-10 technique sweep** (specialized/fine-tuned LLMs and autoregressive
generation, verified live against arXiv/GitHub — see §3.0):

| Project | What it does | Overlap |
|---|---|---|
| [microsoft/CADFusion][cadfusion] | ICML 2025. LLaMA3 SFT alternating with a visual-feedback model; text→CAD (`.step`/`.stl`/`.obj` + point clouds). MIT, 90★ | Generation-side. Its visual-feedback loop is train-time, same shape as the already-rejected CADCodeVerify/Query2CAD auto-loop pattern (§2) — a second data point, not a new consideration |
| [CAD-Judge][cadjudge] | SFT + KTO preference-optimized model for *grading/verifying* text-to-CAD output, not generating it | **Highest relevance found this sweep** — first verification-side specialized model, i.e. this project's own lane. Code/weight availability unconfirmed from the abstract; check before relying on it |
| [AutoBrep][autobrep] | SIGGRAPH Asia 2025. Autoregressive B-Rep generator — unified token sequence over geometry + topology, BFS over face-adjacency graph. Reports improved *watertightness* as a metric | Generation-side, not usable directly, but confirms the field is chasing the same defect class this project's preflight checks |
| [CAD-Llama][cadllama] | LLM SFT on hierarchical-annotated parametric CAD sequences, text→CAD | Generation-side |
| [CADmium][cadmium] (TMLR 2026) | Fine-tunes code-LLMs for text→sequential-CAD design | Generation-side |
| [OpenECAD][openecad] | LoRA-tuned VLM (OpenELM-CLIP base) for CAD code generation from images | Generation-side; confirms LoRA is a proven technique here, but no LoRA model exists yet for CAD *verification* specifically |
| [GeoCAD][geocad] | Local geometry-controllable CAD generation with LLMs | Generation-side |

None of the above change the backend choice (§3.1) or reopen the rejected auto-loop verdict
(§2) — they're additional confirmation that the field is generation-heavy and
verification-thin, which is this project's actual differentiation (see the "Honest read"
paragraph above).

### 3.3 `earthtojake/text-to-cad` — the largest adjacent project

Analysed 2026-07-20, figures re-verified 2026-07-25. **The initial research sweep missed
it.** Largest by adoption; see §3.4 for the one closest to this project's thesis.

| Attribute | Value |
|---|---|
| Scale | **10,319 stars, 1,125 forks** (was 8.6k / 984 on 2026-07-20), 314 commits, MIT, release 0.3.9 on 2026-07-10 |
| Form | A **Claude Code / Codex agent-skill package**, not an app or MCP server (`npx skills install earthtojake/text-to-cad`) |
| Backend | **build123d over OpenCascade** — real B-rep, same primary backend this plan chose |
| Scope | CAD + DXF drawings + URDF/SDF/SRDF robotics + part sourcing (`step.parts`, 12k+ STEP catalog) + G-code slicing + SendCutSend fabrication upload + local `cad-viewer` |
| Trajectory | ~1.1k stars April 2026 to 10.3k July 2026 — but **no commits since 2026-07-11**. Stars are still climbing while the code has not moved for two weeks; do not read adoption as active development |

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
reply: *"Working on benchmarks at the moment!"* ([HN][hn]). **Re-checked 2026-07-25: still
no grader in the repo.** Two claims in this section were re-verified by grepping a fresh
clone rather than trusting search — the absence of watertight/volume/interference checks
holds, and the `gcode` skill's `--dry-run` is weaker than first recorded: it prints the
planned slicer command without ever invoking the slicer, so it is not diagnostic of
printability at all.

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

### 3.4 `jdilla1277/agentcad` — the closest on thesis

Found by the 2026-07-25 marketplace sweep; stats and technical claims verified directly
against the GitHub API and the repo's own README, not from search results.

| Attribute | Value |
|---|---|
| Scale | 79 stars, 12 forks, Apache-2.0, Python. Created 2026-06-02, pushed 2026-07-24 — small but moving daily |
| Form | CLI **and** MCP server, "CAD CLI and MCP server for AI agents" |
| Backend | **build123d default, CadQuery optional** — the same primary backend this plan chose |

**It already does the shape of this project's v0.** `agentcad inspect` is a topology
deep-dive over shells, free edges and validity; `agentcad run` emits volume, dimensions,
validity and face/edge counts; `--preview` produces a four-view PNG plus a turntable GIF;
and successful runs open a `viewer.html` for human review, with A/B overlay against the
previous version. Deterministic checks, automatic multi-view render, human decides — the
same three moves in the same order.

Two things it does differently, and one of them matters:

- **OCCT `is_valid` / free-edge counting runs pre-mesh on the B-rep**, which is arguably a
  stronger check than mesh-level watertightness. Worth adopting when build123d is present
  (plan §7.2 already reaches for `is_valid()`; this confirms the instinct).
- **No necessary-not-sufficient caveat anywhere.** Checked the README explicitly: there is
  no statement that passing does not mean correct. It also has no volume/mass *band*, no
  interference check, and no `SKIP` semantics for an unsupplied bound.

**What this means, stated plainly.** The technical wedge is gone — someone else is on the
same backend doing the same three moves, and doing them well. What is left is the framing
this project treats as load-bearing and they do not state at all. That is a real difference
in an instrument whose failure mode is false confidence, but it is a *thin* one, and it is
worth being honest that it is thin. It does not change v0: the plan is estate-first, the
consumers are real, and the §3.1 red-team already concluded there is no moat here. It does
raise the cost of ever weakening the honesty rules — see §3.2.

**Adopt from it:** the pre-mesh `is_valid` / free-edge check (M2), and the A/B-against-last-
version viewer, which is a cheaper regression UX than the manifest diff planned for M4.

### 3.5 CAD MCP servers

| Server | Stars | Note |
|---|---|---|
| [ahujasid/blender-mcp][blendermcp] | 23.1k | Most adopted CAD-adjacent MCP; mesh domain |
| [neka-nat/freecad-mcp][freecadmcp] | ~1.4k | Document CRUD, code exec, FEM/CalculiX |
| [quellant/openscad-mcp][openscadmcp] | 116 | FastMCP, 80%+ coverage |
| [hedless/onshape-mcp][onshapemcp] | 109 | 45 tools, 471 tests |
| [pzfreo/build123d-mcp][build123dmcp] | 31 | **Closest to our stack** — AST-sandboxed exec, render/measure/printability tools |
| [daobataotie/CAD-MCP][cadmcp] | 451 | AutoCAD/GstarCAD/ZWCAD, Windows-only |

No CAD servers exist in the official MCP servers repo — the ecosystem is entirely
third-party — **except one, found 2026-09-10:** Autodesk itself shipped an official
Anthropic↔Autodesk **Claude for Fusion** MCP connector on 2026-04-28, one of nine simultaneous
creative-tool connectors — confirmed directly via [Anthropic's own announcement][claudecreative],
which names all nine (Ableton, Adobe, Affinity by Canva, Autodesk Fusion, Blender, Resolume
Arena, Resolume Wire, SketchUp, Splice). Mechanism confirmed via
[Autodesk Platform Services' own blog][apsfusion]: natural language → Fusion design actions,
iterative refinement, execution stays inside Fusion. No verification/validation capability is
described in either announcement — generation and editing only. First-party status makes this
the most significant CAD-MCP entry in this table, but it doesn't change the verdict: it's the
same generation-only shape as everything else here.

The same sweep found **8+ independent community Fusion-MCP servers**, all generation/
control-only (e.g. [frankhommers/autodesk-fusion-mcp][fusionmcp1],
[Joe-Spencer/fusion-mcp-server][fusionmcp2], [jaskirat1616/fusion360-mcp][fusionmcp3] — the
last has trivial sanity checks like `dimensions_positive`/`units_valid`, nothing resembling a
render-gate; all three repos fetched directly, but their creation dates were not confirmed —
"2026" is an inference from the surrounding ecosystem, not a verified per-repo fact). This
reinforces the existing Fusion 360 API "Hold" verdict (§3.1, desktop-app dependent) and the
differentiation argument above: even Autodesk's own first-party AI tooling ships zero
verification philosophy.

### 3.6 GUI automation state of the art (context for the deferred GUI leg)

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

### 3.7 BIM — evaluated, not adopted

Raised 2026-09-10 as a scope question (broaden this project to Building Information
Modeling for "synergies"). Investigated across two research passes rather than answered from
intuition. Verdict: **BIM is not one verification problem, it is three, and they don't
share this project's shape.**

**Regime 1 — spatial clash detection** (walls/MEP/structural interference). Solved
authoritatively by Solibri/Navisworks-style deterministic geometric-intersection checking
directly on the IFC semantic model — industry-standard, ubiquitous, and treated as
*sufficient*, not necessary-but-not-sufficient the way this project's mesh preflight is. Two
research sweeps for a render+VLM advisory-gate analogue (the AEC equivalent of CADCodeVerify/
`agentcad`) found **none**. The closest hits were all shaped differently: Sketch2BIM
([arXiv:2510.20838][sketch2bim], verified directly) gates *input* parsing (hand-drawn
floorplan → layout) with human correction each iteration, not output verification of a
generated design; [Text2BIM][text2bim] checks a generated IFC model with a deterministic
rule engine (Solibri), not a VLM, and independently caps its auto-fix loop at 3 iterations
(§2 corroboration). **Why the gap exists:** the defect class your render step fills for CAx
— local, unforeseen geometry a blind deterministic check can't see (a hole that isn't
actually through) — doesn't obviously exist in BIM, because BIM's deterministic layer is
already authoritative there. This regime needs nothing from this project.

**Regime 2 — fabrication/CAM (design-build, DfMA, prefab, CNC-cut components).** Plausible,
and if real it's your existing problem in disguise, not a new one — but this needs a caveat
the first pass didn't carry. BIM workflows are widely described as exporting **LOD 400
models to STEP/DXF for CAM toolpathing** (CNC G-code generation for sheet metal, precast,
timber connections); this reflects general BIM/CAM industry practice, not a specific
primary source independently fetched this session. Two supporting citations from the first
pass did not survive a falsification check: the two ScienceDirect papers on "preassembly
analysis"/assembly-deviation research 403'd on direct fetch and were only ever title-matched
via search, and the MDPI paper (2071-1050/15/15/11990) also 403'd — what could be confirmed
about it (Rhino/Grasshopper parametric structural generation, embodied-environmental-impact
assessment) does not include the IFC-export claim originally attributed to it, so that
detail is dropped rather than repeated unverified. **If the general premise holds** — a
fabricable BIM component exported as STEP/mesh — it has the identical defect class (a hole
that isn't actually through, a mating feature off its datum) that motivates this project's
render-gate, and `build123d` already reads/writes STEP. If a BIM-driven fabrication consumer
ever existed in the estate, v0's architecture plausibly applies with no new backend — but
treat this whole regime as a plausibility argument, not a verified one, until a specific
primary source is fetched. No such consumer currently exists (§4 lists only
`so101`/`i3mega`), so this stays a landscape note, not a trigger.

**Regime 3 — building code / regulatory compliance.** A third, distinct regime, and
structurally **not** like a bbox check — it's the same shape [`cae.md`](cae.md) §1
already named for `peak_stress < yield`: a scalar (or pass/fail) at the end of a chain of
independent judgements (correct rule retrieval, correct interpretation of ambiguous code
text, correct classification of building elements), any of which can be wrong while it
returns a plausible pass. Every code-compliance paper found used **generic prompted LLMs**,
none fine-tuned specifically for this (arXiv:2506.20551, arXiv:2407.21060, door-detection
arXiv:2509.17283, [BIM-Edit benchmark][bimedit]) — no Solibri-equivalent authoritative gate
exists for code compliance. Gating on "code-compliant" would be the CAE false-confidence
failure with extra steps, not a safe preflight. The same caution `cae.md` applies to stress
checks applies here without modification — and generalizes further: footing/foundation
design checks (base pressure vs. allowable soil bearing, stability, strength design) are
*also* CAE-shaped rather than bbox-shaped, since allowable bearing pressure depends on a
geotechnical report's assumptions, not a direct measurement of the artifact.

**Adjacent, checked and dismissed:**

- **Specialized/fine-tuned LLMs for BIM** exist but cluster on generation/retrieval/
  enrichment (Eplus-LLM — Jiang et al. 2024, and a Forth & Borrmann semantic-enrichment
  paper — both found via search summary only, exact source not independently fetched this
  session; domain-tuning-vs-prompting study arXiv:2508.05676) — nothing fine-tuned for
  verification. [Qwen-BIM][qwenbim]
  (generation) and [MCP4IFC][mcp4ifc] (a tool-use framework, not itself a fine-tune) round out
  the generation side. [BIMScript][bimscript] is the closest real IFC bridge (validated Revit
  add-in, IFC4 export end-to-end) — its "validity check" parses against deterministic entity
  schemas, not a render, reinforcing Regime 1's conclusion.
- **World models** — not a real category yet in CAD or BIM verification; confined to
  robotics/embodied AI (§3.0). BIM has been reported to use applied ML for
  clash-*prediction*/triage (ranking existing deterministic clashes rather than generating),
  which would be prediction, not a generative world model — the specific source found for
  this (Buildings 16(4):690) 403'd on direct fetch and did not survive independent
  verification, so treat the clash-prediction sub-claim as unconfirmed rather than cited.
- **LoRA fine-tuning** — proven technique (HF PEFT, [OpenECAD][openecad]/[GeoCAD][geocad]
  above), but no BIM- or CAx-verification-specific LoRA model exists yet. Owning one means
  owning training data, weights, and hosting — the opposite of this project's "works with no
  model configured" design (plan §3).
- **Agent-harness routers** (`joshuaboys/harness-router`, `HarnessRouter/harnessrouter`) —
  checked directly, wrong problem domain. Both route full coding-agent CLI sessions/accounts;
  this project's only model touchpoint is a single stateless call to "any OpenAI-spec
  endpoint" for optional VLM annotation. No multi-harness problem to route.
- **CSI MasterFormat** — a construction-spec classification standard, sits alongside
  UniFormat/OmniClass (confirmed directly against CSI's own site, csiresources.org). The
  commonly-cited "50 divisions, 6-digit codes" specifics are corroborated only by
  third-party explainer sites, not CSI's own numbering document — likely accurate, not
  independently confirmed this session. Documentation/metadata plumbing either way, not a
  verification mechanism.

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
| [microsoft/CADFusion][cadfusion] | ICML 2025 — LLaMA3 + visual-feedback text-to-CAD |
| [CAD-Judge][cadjudge] | Fine-tuned model for grading/verifying text-to-CAD (verification-side) |
| [AutoBrep][autobrep] | SIGGRAPH Asia 2025 — autoregressive B-Rep gen, watertightness metric |
| [CAD-Llama][cadllama] | LLM SFT on hierarchical parametric CAD sequences |
| [CADmium][cadmium] | TMLR 2026 — fine-tuned code-LLMs, text-to-sequential-CAD |
| [OpenECAD][openecad] | LoRA-tuned VLM, image-to-CAD-code |
| [GeoCAD][geocad] | Local geometry-controllable CAD generation with LLMs |
| [Sketch2BIM][sketch2bim] | Hand-drawn floorplan → BIM via multi-agent MLLM, human-gated |
| [Text2BIM][text2bim] | BIM generation + Solibri rule-check, 3-iteration auto-fix cap |
| [Qwen-BIM][qwenbim] | Fine-tuned LLM for BIM design + eval benchmark |
| [MCP4IFC][mcp4ifc] | MCP tool-use framework for LLMs manipulating IFC |
| [BIMScript][bimscript] | Structured BIM commands, validated Revit add-in + IFC4 export |
| [BIM-Edit benchmark][bimedit] | Benchmark for LLMs editing IFC data |

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
[agentcad]: https://github.com/jdilla1277/agentcad
[cadskill]: https://github.com/flowful-ai/cad-skill
[drawingagent]: https://drawing-agent.com/
[cadsmith]: https://arxiv.org/abs/2603.26512
[vibecad]: https://github.com/rawwerks/VibeCAD
[mfrender]: https://github.com/mfranzon/render
[mitsuhiko]: https://github.com/mitsuhiko/agent-stuff
[printskill]: https://github.com/EdwinjJ1/3d-print-skill
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
[cadfusion]: https://github.com/microsoft/CADFusion
[cadjudge]: https://arxiv.org/abs/2508.04002
[autobrep]: https://arxiv.org/abs/2512.03018
[cadllama]: https://arxiv.org/abs/2505.04481
[openecad]: https://arxiv.org/pdf/2406.09913
[geocad]: https://arxiv.org/pdf/2506.10337
[fusionmcp1]: https://github.com/frankhommers/autodesk-fusion-mcp
[fusionmcp2]: https://github.com/Joe-Spencer/fusion-mcp-server
[fusionmcp3]: https://github.com/jaskirat1616/fusion360-mcp
[cadmium]: https://arxiv.org/abs/2507.09792
[claudecreative]: https://www.anthropic.com/news/claude-for-creative-work
[apsfusion]: https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work
[sketch2bim]: https://arxiv.org/abs/2510.20838
[text2bim]: https://arxiv.org/html/2408.08054v1
[qwenbim]: https://arxiv.org/abs/2602.20812
[mcp4ifc]: https://arxiv.org/abs/2511.05533
[bimscript]: https://arxiv.org/html/2608.21447
[bimedit]: https://arxiv.org/abs/2606.20146

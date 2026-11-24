---
title: Landscape — evidence, competitors, backend choice, contribution stance
purpose: The research behind the design decisions, split out of plan 001 so the plan stays a plan
created: 2026-07-20
updated: 2026-11-23
validated_links: 2026-11-15
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

**Ranking (owner 2026-11-14):** entries adjacent to the project's scope are kept, marked
**Rank: adjacent (low)**. Only an entry that changes a plan decision ranks high.

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

**2026-09-19 — the technique exists, the CAD/BIM application still doesn't.** Asked
separately: could PEFT/LoRA adapt an *open* physics-surrogate model into a manufacturability
or structural-behavior predictor (the digital-twin instance of a "world model" named above)?
Verified directly: yes, PEFT/LoRA-style adaptation of a physics surrogate is a real,
demonstrated technique — [arXiv:2605.27968][autoaero] adapts a transformer/operator-learning
aerodynamics surrogate to new vehicle families via parameter-efficient transfer learning,
with less data than training from scratch. Fast, physically-consistent GNN-based structural
surrogates are also real and active (steel-frame response, vehicle-panel crashworthiness
papers, 2026) — but GNNs are encoder-processor-decoder architectures, not transformers, so
classic LoRA (built for attention layers) does not directly transfer; an adapter-style PEFT
analog would need to be built, not borrowed as-is. **Still true: nobody has applied any of
this to CAD/BIM manufacturability or structural prediction specifically** — the aerodynamics
paper is the closest real precedent, not an existing instance. A PDE-Transformer LoRA claim
surfaced by search could not be independently verified (fetch exceeded size limits) —
unconfirmed, not cited as fact.

**Why this stays a landscape note, not a build candidate, even if built:** a learned
surrogate is *more* CAE-shaped than a numerical solver, not less — [`cae.md`](cae.md) §1's
chain-of-judgement argument (mesh density, boundary conditions, load-case assumptions can
all be wrong while a solver exits 0) still applies in full, plus the surrogate's own
training-distribution coverage on top, with no grid-convergence-index analog to sanity-check
against. This would belong on the render/human-judged side of the trust boundary, same as
CAE — never a gate — if it is ever built at all.

**2026-11-12 — owner-screenshot leads, first-party re-sourced.** 15 social-media leads swept;
findings landed in §3.2 (BenchCAD 2.0, NVIDIA SimReady Central, MeltFlex, Kyrall) and
[`vendor-ai.md`](vendor-ai.md) PTC section (two first-party Onshape blog posts). **Searched,
empty or dropped:** AW-0 (UC Berkeley/NVIDIA robotics world-action model, arXiv:2610.30136 —
confirmed robot-manipulation only, no CAD/OpenUSD tie despite a direct check); Nominal.io
(confirmed as a real hardware test/telemetry platform, but its claimed agent-driven
CAD↔HPC↔surrogate loop-closure was not stated on its own site); "Generative Engineering"
(Joe Griston), "Facade Studio" (Chiang Ning), and a PTC/Onshape × Gemma/AAS/dataspace claim —
no first-party source found for any of the three despite a direct search. **Already
covered, not re-added:** two of the leads were duplicates of case studies already in this
file — the 222M-token/472-call run matches [Steenken, 2026-10-07][steenkencase] exactly, and
the Pi4-housing/missing-draft-angles run matches [Steenken, 2026-09-29][steenkenrun1]
exactly. **Checked and not confirmed:** an "Astra builds Rhino models, called vibe
modelling" lead lacked a URL; the one Astra+BIM article found on this topic
([AEC Magazine, 2026-10-11][aecastra], read directly) covers Rhino/Grasshopper tests but
neither a facade example nor the term "vibe modelling" — that term is already recorded in
this file from an unrelated 2026-10-26 `rhino-mcp` entry, so the lead may be the same meme
recurring, not new evidence. A Molitor knowledge-graph lead also lacked a URL and could not
be matched to a specific first-party source — **resolved 2026-11-12:** it is his whitepaper's
context-management chapter (§3.2, the Molitor entries).

### 3.1 Backend decision

| Tool | Verdict | Why |
|---|---|---|
| **build123d** | **Adopt — primary** | Apache-2.0, headless, Pythonic; already the estate standard in both consumer repos |
| **OpenSCAD** | **Adopt — fallback** | Headless CLI export; already the fallback in `so101` |
| CadQuery | Assess | Apache-2.0, larger LLM training corpus than build123d — revisit if codegen quality disappoints |
| FreeCAD Python API | Assess | `FreeCADCmd --console` headless; verbose, less training data |
| pythonocc-core | Assess | Low-level OCCT escape hatch |
| Onshape API | Assess | REST is tool-calling friendly; FeatureScript is niche/proprietary |
| Blender bpy | Hold | Mesh/procedural, not parametric BREP — wrong domain for manufacturing CAD. Headless is not the blocker (checked 2026-11-11, §3.2) |
| Rhino (rhino3dm / Compute) | Hold | No free headless path: Rhino 8 does not support Linux, Compute is billed per core-hour (checked 2026-11-11, §3.2) |
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
| [MecAgent][mecagent] | Copilot app attached to an open CAD session, building native, editable features, assemblies and drawings from text, spec sheets, STEP files or PDF drawings. **Re-read 2026-11-14 (vendor pages):** only SolidWorks (2024–2026) is listed as available; Inventor, CATIA V5, 3DEXPERIENCE, Fusion, NX, Solid Edge, Onshape and Creo are listed as "soon"/end of 2026. Its home and about pages describe no check on generated geometry; no benchmark is cited | Medium. Rank: adjacent (low) |
| [Leo AI][leoai] | Closed, enterprise-priced agent for mechanical engineers: answers questions with cited sources, generates parametric CAD from text, sketches or images, and reviews assemblies and STEP files (its "Inspector"). Its home page and FAQ list different CAD and PLM integrations (SolidWorks, Inventor, NX, Fusion and others). **Read at source 2026-11-24 (two LinkedIn posts, home page, FAQ, one blog guide):** a "Leo Simulation Agent" was announced that day for static, modal, buckling, harmonic and thermal analysis "within minutes", naming no solver and no validation, while the [FAQ][leofaq] still said Leo "does not run FEA or CFD simulation itself". A "96% accuracy" figure is a customer quote with no method. Its [own guide][leocheck] (2026-11-05) tells readers to grade an AI solver on 10 problems solved by hand, checking its output against four known-wrong results: the same move as this repo's closed-form bands and known-bad controls (plan §5 BENCH-3), so nothing new to adopt. Any simulation result it gives would be inform-only here: CAE sits on the render side of the trust boundary (plan §12 item 1) | Medium. Rank: adjacent (low) |

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
*Scoped 2026-11-23:* the idea behind it, that a tool's "ok" is no evidence of the right part,
is not ours alone — The Stack Underflow concludes it (§3.8, paraphrased). The delta is
applying it to the gauge's own passing checks and to unsupplied bounds, as found in the
sweeps up to 2026-07-25; no full sweep has run since, and whether that channel labels its
own checks this way was not checked.

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

**Added 2026-09-19, corrected 2026-11-11 — [LEAP71][leap71].** "Computational Engineering":
algorithmic design of complex hardware (rocket engines, heat exchangers, electric motors)
for advanced manufacturing. Their kernel **PicoGK** (C#, Apache-2.0) plus an ecosystem —
`LEAP71_ShapeKernel`, `PicoGKRuntime`, `LEAP71_HelixHeatX`, `LEAP71_LatticeLibrary`,
`LEAP71_QuasiCrystals`, `LEAP71_RoverWheel`, `PicoGKInstaller`, `PicoGKUnitTests` (MIT) and
examples. **Correction:** the 2026-09-19 note said three of these "did not reappear" on the
org page; the GitHub API lists all three (`users/leap71/repos`, 2026-11-11) — a search-scope
error then, not a fact about the repos.

**Restructure, as of 2026-11-11.** [`PicoGK.Legacy`][picogklegacy] (created that day) wraps
the PicoGK 2.x library and its native runtime as submodules behind a new automated build;
its README puts PicoGK 2.x "into maintenance mode while developing its successor, PicoGK.Core"
and lists Windows x64 and macOS ARM64 as build targets (an experimental Linux package landed
in a commit the same day). It had no root licence file then; one (Apache-2.0) was added on
2026-11-13. [`PicoGK.Core`][picogkcore] is a ground-up kernel
rewrite (sparse signed-distance voxels, immutable meshes, a C ABI, .NET 10 / C# 14), the
basis for PicoGK 3.x, and is marked "Early development — do not use yet"; `PicoGK.Geometry`
and `PicoGK.Viewer` split off geometry interchange and viewing. None has a Python binding or
CLI. LEAP71's commercial engineering model, Noyron, is proprietary and built on PicoGK
([leap71.com/noyron][noyron]); no first-party agent or MCP tooling was found.

**The whole account, as of 2026-11-22: 21 public repos** (`users/leap71/repos`). Beyond the
ones named above: `PicoGK_Examples` (licence detected as "Other"), `PicoGK_SimulationExample`,
the `leap71` profile repo and the `leap71.github.io` blog (no licence detected for those three),
and four new Apache-2.0 C# repos:

- **Chondrite** (`Chondrite.Core`, `Chondrite.Store`, `Chondrite.Compile`, all created
  2026-11-22, .NET 10, the Store and Compile READMEs say early development): a data store
  with a schema compiler. Schemas in `.chondrite` files compile at
  build time into C# record types, binary codecs and canonical schema outputs. Its tests
  include a `Pascals` record, a unit carried in the type rather than in a bare `double`.
- **`LEAP71.Semantics`** (created 2026-11-16): marker interfaces only, no implementation.
  `IQuantityValue` tags a strongly typed quantity (their convention: a `u` prefix) and
  `IIdentityValue` a typed identity.

**Our reading, not LEAP71's claim:** a quantity whose type carries its unit is the structural
fix for the unitless-`8` slip in §3.8 (a bare number that a tool took in the wrong unit).
Nothing here is a Python dependency candidate (C#, §2); it is a design note for any future
brief or check that takes parameters with units. **Rank: adjacent (low).**

**Two findings for this project.** (1) `PicoGKUnitTests` asserts measured voxel volumes
against closed-form values (a sphere's) — the same oracle pattern as our briefs' bounds.
(2) PicoGK's own volume measurement is wrong for closed hollow bodies:
[Discussion #118][picogk118] (2026-09-25, unanswered) reports a hollow sphere measured at
the solid sphere's volume (+14.26 %), while the triangle mesh itself is correct — so a
representation that is watertight by construction can still report a wrong number.

**The one finding worth keeping past the "not a build candidate" filter.** PicoGK is
**voxel-field/signed-distance-field based, not B-Rep** — confirmed by reading the actual
source (`PicoGK_Voxels.cs`, `PicoGK_ScalarField.cs`), cross-checked against a founder blog
post (Lissner & Kayser, jlk.ae). Surfaces come from marching-cubes-style extraction off the
SDF zero-crossing — categorically different from build123d/OCCT's B-Rep. No built-in
watertight/manifold validation API was found in source or discussions, but marching-cubes
meshing is watertight-by-construction as a property of the representation itself, not a
claim LEAP71 makes. **This doesn't make verification unnecessary — it changes what needs
checking**: a voxel/SDF pipeline trades this project's headline defect (silent
boolean-fusion non-manifold loss) for a different one (voxel-resolution/aliasing loss at the
extraction step). STL export/import is confirmed working (`ExportVoxelsToSTLFile`,
`mshFromStlFile()`, per GitHub Discussions #63/#19), so it's format-compatible with this
project's input contract in principle — C# and this project's locked Python 3.12 constraint
(§2) rule it out as an actual backend regardless. Kept as a landscape note: evidence that
"watertight by construction" is representation-dependent, not a property this project can
assume in general.

**Added 2026-10-09 — a first-hand agentic-CAD case study ([Steenken, 2026-10-07][steenkencase]),
read in full and re-checked at source.** Claude Opus 5.5 drove a live CAD session over MCP
from one brief and produced a two-part ABS injection-molded housing for a Raspberry Pi 4
room-booking sign: two STEP parts, 5 drawing sheets, a 15-line BOM, a 9-page assembly guide,
a DFM check against the molder's rules, and a snap-fit strain calculation. Reported effort:
3 h 9 min active agent time, 472 calls, 222M tokens (98.8% re-reading its own context, about
730k newly written), plus 1 h of the author's time. **The CAD tool is not named**, so the
setup can't be reproduced or attributed. Human review caught three defects: the
documentation said seven snap hooks while the model had eight (the docs hadn't followed a
revision); the top part had no draft on its outer surfaces, so it would not eject cleanly;
and excess corner material, a likely sink-mark source. The article states explicitly only
that the agent "will not flag" the hook-count mismatch itself; that its own DFM pass also
missed the draft and sink-mark issues is implied, not stated.

**Why it matters here:** it's generation-side, but it is independent real-world evidence for
this project's thesis (plan §3.1) — the defects that mattered were local and unforeseen, and a
human looking at the part caught them. Two of the three would fit the plan's gate/inform
inclusion test as **future** deterministic checks, not current scope: *draft angle* is
measurable from face normals once the pull direction is declared (a declared bound, so no
direction → `SKIP`), and *document/model consistency* (e.g. declared vs. counted features)
is a direct measurement. Sink-mark risk depends on wall-thickness thresholds and material
judgement, so it would stay inform-only. Neither is triggered until a consumer actually
ships molded parts.

The author's [LinkedIn post on the same project][steenkenpost] (read at source 2026-10-09)
adds a **fourth** finding the blog doesn't list: "the ribs against the pole could break if
the clamps get fastened too hard" — a load-case judgement, so inform-only under the inclusion
test. It also claims Opus 5.5 "removed 95% of the time I would have spent on modelling" (the
author's own estimate; the physical molding test was still pending). Commenters pointed to
Leo AI ([getleo.ai][leoai], a mechanical-engineering copilot for SOLIDWORKS/Inventor/NX —
generation-side) and PicoGK (already covered above).

**Added 2026-10-11 — the same author's earlier run ([Steenken, 2026-09-29][steenkenrun1]),
re-checked at source.** A Raspberry Pi 4 housing, again Claude Opus 5.5 over MCP, and this
post **does name the tool**: a live Fusion session. One human correction (the model moved
hundreds of bodies one by one instead of the component). The finding that matters here: the
snap-fits looked fine, yet would likely break on first assembly if printed, and there were no
draft angles for injection molding — both missed by the author's own visual read, and traced
to a missing constraint rather than a geometry bug: "I never communicated which manufacturing
process it was designing for." Same lesson as above from the other direction: a render can
look finished while the part is wrong for its process, so the human decides, and
process-dependent checks stay future, declared-bound work.

**Added 2026-10-19 — [SolidCraft][solidcraft], an open-source parametric CAD app with an MCP
server; re-checked at source.** Pure Rust (desktop, web, headless CLI), licensed "MIT OR
Apache-2.0, at your option"; `solidcraft-cli mcp` lets agents model, measure and look at
parts, and it exports STEP and STL among other formats. It is **generation-side**: its
[reference tests][solidcraftoracle] replay recipes through its own kernel and compare against
hand-derived analytic values or an independent FreeCAD build ("83 / 83 cases pass" on the day
read; the README still said "75 of 76", so its own figures drift fast). That validates *its
kernel*, not whether an agent's design matches intent — and the README says so itself: "These
checks do not establish complete geometric or workflow equivalence." Nothing to adopt; if a
consumer ever models with it, `caxgauge check` takes its exported STL unchanged.

**Added 2026-10-23 — the incumbents' AI race ([Molitor, LinkedIn, 2026-10-23][molitor]).** The
post's thesis, read at source: "Engineering AI is becoming a vendor war", naming Siemens, PTC,
Dassault Systèmes, MathWorks, Cadence, Synopsys/Ansys and Autodesk. Its video is a
Jan 2025 – Oct 2026 timeline of about 35 in-suite AI launches (copilots, MCP servers, agents),
tagged PLM/ALM/CAD/CAE/V&V. *Read from the video's frames by a research agent; dates are
approximate and were not re-checked per vendor.* On that reading, the few V&V entries are chip
and software verification (EDA, static analysis), not checks of CAD geometry — consistent with
this section's generation-heavy, verification-thin picture. One entry re-checked at source:
PTC's [Onshape FeatureScript MCP Server][onshapefsmcp] (2026-08-13), where AI "automatically helps
build, test, debug, and refine the custom feature in FeatureScript until it works as intended" —
generation, with the model iterating on its own code; no independent geometry check is
described. Commenters' additions (SimScale, CoLab, Synera, Istari Digital) are CAE, design
review, workflow automation and data lineage respectively — none verify CAD geometry. The
vendors' features themselves — what shipped, usage patterns, and what checks the output — are
in [`vendor-ai.md`](vendor-ai.md).

**Added 2026-11-12 — same author, follow-up ([Molitor, LinkedIn, 2026-11-11][molitor2]).** A
partnership map, "Who Builds Engineering AI With Whom?" — 273 collaborations among 247
companies, with NVIDIA at the centre — recasting the vendor war as an ecosystem race. Its
video is a silent 65 s sequence of network-diagram cards (frames read here; no software runs,
nothing is generated or checked). Two partnerships not logged before, confirmed on the
vendors' own pages: [PhysicsX with Microsoft Discovery][physicsxmsft] (2025-05-19, AI-accelerated
physics simulation) and [Neural Concept with Antolin][neuralantolin] (2026-02-24, "AI design
copilots" scaling from a 2024 pilot into Antolin's existing simulation environment). Both are
simulation-side; neither checks CAD geometry. The post's line about "results engineers can
validate" names no method. Nothing to adopt.

**Added 2026-11-12 — [PhysicsX Ai.rplane][physicsxairplane]** (the page is dated 04/12/2024
and retires the demo). A web tool, not a built aircraft: a generative geometry model (LGM-Aero)
proposes aircraft shapes, a deep-learning surrogate trained on CFD and FEA results predicts
pressure, lift-to-drag, stability and stress in seconds, and the shape exports as STL. The only
check is that surrogate, with a stated uncertainty; independent validation is left to the user
(conventional calculation, or print it and see whether it flies), and no flight test is
reported. The design and its check both come from the vendor's own models, the pattern
`vendor-ai.md` records for CAD vendors. Nothing to adopt.

**Added 2026-11-12 — the map's in-scope names, audited.** A read-only audit read all 26 video
frames and grepped about 205 legible names against this file, `vendor-ai.md` and `cae.md`:
the CAD/CAE incumbents were already covered; most other names are cloud, LLM, robotics,
automotive, life-science or chip companies — context, out of scope (all 204, with the reason
per category and their homepages, in [`engineering-ai-map.md`](engineering-ai-map.md)). The in-scope gaps,
checked at the vendors' own sites (AVEVA, Hexagon and the sale re-checked here; the rest
agent-checked, not re-read): **[AVEVA][avevaai]** — in Unified Engineering E3D, "Generative
AI produces multiple clash-free options in minutes" for plant layouts, and "Point Cloud
Intelligence" classifies and tags laser scans; **[Hexagon][hexagonmentor]** (2025-06-16) —
"Metrology Mentor" "automatically generates ISO- and ASME-compliant inspection programmes
directly from CAD" (the page does not call this AI), and Hexagon
[agreed to sell][hexagoncadence] its Design & Engineering business (ex-MSC Software) to
Cadence for about €2.7bn (2025-09-04), and Cadence [completed it][cadencehexagon] on
2026-02-23 (also in Cadence's [10-Q][cadence10q] for Q3 2026: "On February 23, 2026, we
completed our acquisition of the design and engineering ('D&E') business of Hexagon") — so
MSC Nastran and Adams now sit in an EDA vendor's simulation portfolio. **Deterministic part checks, no AI label:** Paperless Parts (feature detection and
"manufacturability warnings" on uploaded part files), Materialise MiniMagics (free STL/3MF
viewer to "verify part printability"). **Adjacent, no AI on CAD geometry:** Lumafield (AI on
CT scan data), nTop ("Physics AI" evaluates generated variants), Flexcompute ("GeometryAI"
prepares geometry for simulation), CADDi (drawing and CAD search), Akselos (reduced-basis FE
marketed as "Physics AI"), AVL, CoreTechnologie, Monolith.

**Added 2026-11-12 — Molitor's own whitepaper (Molitor et al., Accenture / DFKI / Fraunhofer
ISST, 2025, [PDF][molitorwp], read at source).** "AI in New Product Development: Connecting
Data & Unlocking Knowledge" — 125 pages, Molitor first of six authors — proposes a
five-pillar framework for scaling AI in engineering (data quality, interoperability, AI
platform, context management, federated governance) with use cases from requirements to
release. Its context-management chapter (pp. 25–27) builds on knowledge graphs that an LLM
assembles from engineering artifacts — the knowledge-graph lead noted in §3.0 — used for
retrieval and traceability, not for checking geometry. The one concrete output check is an
Accenture case on p. 48: a Technical Drawing Assistant that "integrates 2D and 3D drawing
checks directly into the engineering workflow", combining image processing with
"rule-based validation techniques to automatically identify design errors and formal
inconsistencies" — rule-based checking of engineering output, the same family as this
project's preflight. Its model-generation survey (p. 49) cites CAD-Coder, CAD-Judge, LLM4CAD
and a five-agent framework (Panta et al. 2025: design expert, script writer, executor,
script-execution reviewer, CAD-image reviewer) that refines its own CAD scripts from visual
feedback — reviewer agents inside the generating system, the auto-critique pattern
`.claude/rules/verification-honesty.md` rejects. Other posts listed on his LinkedIn profile
could not be read at source and are not cited.

**Added 2026-11-12 — OpenAI on AI for hardware engineering ([OpenAI, 2026-11-03][openaieng]),
read at source.** OpenAI reports that GPT‑6 Astra designed a test device — enclosure, PCB
and firmware — "without any direct human edits", and a contract manufacturer built
prototypes within a month; but readying it for production took several review rounds,
because "Astra did not consistently account for the manufacturer's production limits,
tolerances, or details required for assembly". Its benchmark BenchCAD 2.0 (reconstructing 3D
parts and assemblies, circuit-board connections) scores an internal model at 0.875 against
Astra's 0.594, and industry partners' engineers "review model outputs for accuracy and
practical use". The model vendor itself documents the gap this project targets: generated
geometry that looks complete and still misses manufacturing constraints, caught by humans.

**Added 2026-10-26 — [tanishqbhattad/rhino-mcp][rhinomcp], from a LinkedIn "vibe modelling"
post; repo checked via the GitHub API.** MIT, created 2026-05-12, last pushed 2026-10-12. A
Rhino 8 MCP server for architectural modelling ("128 tools") with post-condition checks —
`assert_geometry` ("bbox / envelope / count / count_delta / watertight / supported") and
`validate_objects` ("separates *real corruption* from *intentionally open shells*") — and its
README states this project's own premise: "Valid geometry is not correct geometry", since
arithmetic and wiring errors still produce "a perfectly closed, valid solid". It is
generation-side, with the generating model checking its own work. **Not a benchmark track
here:** Rhino itself is commercial (McNeel), and the owner's bar for now is free tools. The
post itself is a near-verbatim copy of an earlier one by another author, so it is not cited as
first-hand evidence.

**Added 2026-11-11 — Rhino beyond rhino-mcp: no free headless path.** Researched by a
read-only agent; the load-bearing claims re-checked at source. Rhino 8's
[system requirements][rhino8req] list Linux and Windows Server (any version) as not
supported. [`rhino3dm`][rhino3dm] (MIT, active) reads, writes and creates `.3dm` geometry on
Linux, but its README sends "operations that need Rhino" to Rhino.Compute, and
[Compute][rhinocompute] is billed at $0.10 per core-hour with no free tier (a Linux beta
exists, on that billing). The evaluation download (now Rhino 9) is "one-time", and saving and
plug-ins stop after 90 days.
McNeel now ships its own agent plugin, [`mcneel/rhinoai`][rhinoai] (MIT, created 2026-04-25),
connecting Rhino and Grasshopper to Claude, Codex and others; nothing found says it checks
the geometry it produces (its forum announcement was read only through a search summary —
unverified at first hand). Verdict: not a benchmark track under the free-tools bar.

**Added 2026-11-11 — Blender: headless is easy, the domain is still wrong.** The `bpy`
package on PyPI (GPL-3.0, 5.3.0, a Linux x86-64 wheel, Python 3.13 only) runs Blender's
Python API with no GUI, and `blender --background --python` does the same. That does not
move the §3.1 Hold: Blender builds meshes, not exact solids, and CAD Sketcher (GPL-3.0) is
2D and self-labelled experimental. The 3D-Print Toolbox is now a separate extension with a
bad-geometry check close to our watertight check. **BIM correction to §3.7:** Bonsai's own
CI runs its tool and BIM test suites under `blender --background`
(`.github/workflows/test-bonsai.yml`), so headless Bonsai is further along than the
2026-10-26 note implied; whether an agent can create a wall that way is still unprobed.
[blender-mcp][blendermcp] (MIT) has the model check its own renders — self-checking, not an
independent gate.

A second source the user supplied, a LinkedIn Pulse article on an Opus 5.5 + Blender
timelapse workflow, **could not be read**: LinkedIn returned its own "page not found" both
to a plain fetch and to a real headless browser (polyfetch, patchright tier), and no copy was
found elsewhere. Not documented.

**Added 2026-10-09 — [Trace][trace] (buildwithtrace.com): a different domain, the same trust
model.** Researched by a read-only agent; its load-bearing claims re-checked at source. Trace
is an AI-native **PCB** design tool (WishEDA Inc., public launch Feb 2026, Pro $29.99/mo,
7-day trial, no free tier) built on a GPLv3 fork of KiCad: natural language → schematic,
component sourcing, autorouting. It outputs board manufacturing data (Gerber/ODB++/IPC-2581),
not solids. [`trace-public`][tracepublic] is GPLv3 for the KiCad-derived editor, but the
`trace/` AI modules are "All Rights Reserved … provided for reference only" and the backend
is not included.

**Can we use it?**

- **As a consumer this gauge verifies — no.** Board files have no meaning for an STL/IFC
  preflight; out of scope unless the project ever expands to PCB.
- **As a component — no.** Wrong domain, and the AI and backend are proprietary. Its local
  ERC/DRC need no sign-in but do need the Trace desktop app and its libraries
  ([CLI docs][tracecli]), so there is no headless library for Linux CI.
- **As prior art — yes, three ideas:**
  1. Its deterministic checks — ERC on connectivity, DRC against declared design rules — are
     exactly gate-eligible under the inclusion test, and its DFM docs say presets "do not
     guarantee fabrication yield … or assembled function": this project's
     necessary-not-sufficient framing, reached independently.
  2. Its AI "Design Review" is kept advisory, in its own words: "Severity expresses the
     check's concern, not a certain prediction of physical failure" and "Inspect the actual
     tool findings … not only the assistant's summary" ([docs][tracereview]). The page
     claims no gating at all. Independent corroboration that an LLM judgement layer should
     inform, not gate — the same verdict as plan §3.1.
  3. `trace-cli … --format json --exit-code-violations` — a machine-readable report plus a
     CI-failing exit code — is a clean pattern for `caxgauge check` to mirror in M2.

**Added 2026-11-11 — PCB beyond Trace: KiCad clears the free-headless bar, Fusion does not.**
Researched by a read-only agent; KiCad and the Fusion API claims re-checked at source.
Trace's `--format json --exit-code-violations` pattern is upstream KiCad's own:
[`kicad-cli`][kicadcli] has `pcb drc` and `sch erc` with both flags from KiCad 8.0, and
`pcb export stl` from 9.0 (STEP and VRML earlier), so a board's 3D solid can go straight into
`caxgauge check`. KiCad is GPL-3.0-or-later, so it runs as a separate tool, never imported.
The most active agent bridge is [`mixelpixx/kicad-mcp-server`][kicadmcp] (MIT); this project
would use the CLI. **Autodesk Fusion's electronics workspace** (EAGLE's successor — EAGLE
access was "scheduled to end on June 7, 2026", per [Autodesk's blog][eagleeol]) fails the bar:
its [electronics API][fusionelectron] is in preview, and Fusion's
[system requirements][fusionsysreq] (2026-10-20) list Windows, macOS and a web browser — no
Linux. **Updated 2026-11-23:** the API page has moved and no longer calls the API read-only.
Most properties are now writable, and a script can run a batch of native Electronics
commands against a board. The page doesn't say whether the design-rule check is one of them,
and we haven't checked the command reference. The free [personal-use tier][fusioncompare] includes PCB design capped at 2 sheets per
schematic and 4 signal layers, board area unlimited (both re-fetched with polyfetch's headed
browser, which Autodesk's bot block lets through). **Verdict:** a PCB track is feasible free and headless on KiCad alone — the
DRC/ERC exit code as the deterministic check, the exported STL through the existing
preflight (e.g. board-in-enclosure fit). Not started: no trigger yet.

**Added 2026-11-12 — [BenchCAD 2.0][benchcad2], a benchmark for exactly this question,
scored differently.** Verified directly against its two GitHub repos — the scoring harness
[BenchCAD-org/benchcad-2-main][benchcad2] and the data pipeline [BenchCAD-org/benchcad-2][benchcad2data]
— not from marketing copy. Six tasks, 100 "Core" cases: a model gets a part drawing, STEP
parts plus an assembly drawing, rendered views, or PCB photos, and writes CadQuery code or a
schematic in a sandbox; scoring is "executed geometry against the reference, deterministic,
with no LLM judge" (per-task metrics `part_v1`/`asm_v1`/`ecad_v2`, the PCB task literally
named `t6_pcb2schematic` in the repo). The dataset pipeline and v1 scoring repos both state
Code MIT / released dataset artifacts CC BY 4.0; the 2.0 harness repo's own `LICENSE` file
404'd via the GitHub API, so that specific repo's licence was not independently confirmed.
The Core case set itself is gated behind a Hugging Face access request, so the benchmark is
not fully open.

This is the closest sibling to this project's own `bench/`: same target task (agentic
programmatic CAD generation), same no-LLM-judge principle, a different verification shape —
execution-grounded geometric similarity (voxel IoU) against a reference answer, rather than
render+human-decides against unstated intent. Its published reference line
(`results/core_reference.json`, read directly) scores `openai/gpt-6-astra` at **0.5943** and
`anthropic/claude-opus-5-5` at **0.5662**, both at "max" reasoning effort (3 reps and 1 rep
respectively). The same repo's README flags that this exact line has one Task-6 cell scored
by a since-retired fallback rule, and that under the corrected scoring rule (applied to runs
from 2026-11-05 on, not retroactively) "its T6 column would read 0.4222 and its line
0.5893" — the measurer correcting its own published number, a small instance of this
project's own thesis that scoring is never done once.

**Corrected 2026-11-12 — read directly, not search synthesis.** A plain fetch of the OpenAI
post 403s (consistent with this file's existing `openai.com` lychee exclusion), but a
browser-TLS-fingerprint fetch returns HTTP 200 for the same URL — the 403 is a bot-block, not
a dead or access-gated page. [OpenAI's 2026-11-03 blog post][openaiphysical] does name
"BenchCAD 2.0" and states, verbatim: "BenchCAD 2.0 tests whether models can reconstruct 3D
parts and assemblies and identify connections in circuit boards. A newer internal model
achieved an average score of 0.875, compared with 0.594 for GPT‑6 Astra at its highest
reasoning setting." The 0.594 figure matches BenchCAD's own measured `gpt-6-astra` "max" line
(0.5943) above almost exactly. The 0.875 figure, for an unnamed, unreleased internal OpenAI
model, still does not appear in BenchCAD's own `core_reference.json` (which lists only Claude
and `gpt-6-astra` lines) — but, checked this session, the **live leaderboard at benchcad.com**
does list it: "OpenAI internal model · setting 4 · Codex · 0.875 · credit to OpenAI, from its
post; unreleased, placed at the post date," with a News item dated 2026-11-03, "OpenAI on
BenchCAD 2.0: a newer internal model scores 0.875." BenchCAD's own leaderboard convention
(its sibling v1 repo `BenchCAD/BenchCAD-main`'s `LEADERBOARD.md`, read directly) names exactly
this situation with a `†`: "self-reported by the provider, not re-graded by us" — the 2.0
site's own attribution text ("credit to OpenAI, from its post") carries the same meaning
without the symbol. **That OpenAI's post cites BenchCAD 2.0, and that BenchCAD's own site
acknowledges the 0.875 figure, are both now confirmed by direct read; the figure itself
remains self-reported by OpenAI, not independently re-graded by BenchCAD. Treat 0.5943/0.5662
as BenchCAD-measured, read directly from its own repo; treat 0.875 as OpenAI-measured, listed
on BenchCAD's site with that self-reported caveat, read directly from both.**

Also confirmed by the same direct read: the post describes GPT-6 Astra designing the
enclosure, PCB and software integrations for a hardware device used to talk to Codex —
"Two team members designed this test device with Astra in under a week while working on it
as a side project. A contract manufacturer built a small batch of prototypes in under a
month" — but "Getting the device ready for manufacturing still required several rounds of
review and iteration. Astra did not consistently account for the manufacturer's production
limits, tolerances, or details required for assembly" — the same DFM/tolerance failure class
as the Steenken case studies above, from a different vendor and a different tool.

**Added 2026-11-12 — [NVIDIA-Omniverse/simready-central][simready], a render+physics gate on
agent-submitted assets, verified directly via the GitHub API.** Apache-2.0. NVIDIA's intake
pipeline for OEM-contributed "SimReady" OpenUSD assets (robotics/digital-twin simulation
props), published alongside [Hugging Face's SimReady Central Library blog post][hfsimready]
(NVIDIA-authored, 2026-10-21, read directly): "more than 2,000 simulation-ready (SimReady)
OpenUSD assets on Hugging Face," and Hugging Face "integrated USD Search into their platform
search" — the post does **not** say the Hub added native OpenUSD viewing, and states no
licence for the library as a whole, nor does it name specific OEM dataset repos. Two OEM
repos were confirmed directly instead: [`LGElectronics/simready-assets`][lgsimready]
(CC BY 4.0, 21 USD assets, 539 MB, empty README) and [`Vertiv/simready-assets`][vertivsimready]
(CC BY 4.0, 41 USD assets, 1.52 GB — "NVIDIA SimReady packages for Vertiv datacenter
equipment ... source of the packages submitted to SimReady Central").

The `simready-central` repo ships its own `CLAUDE.md`/`AGENTS.md` and expects an agent to
drive submission through a documented skill. Its acceptance criteria
(`docs/acceptance-criteria.md`, read directly) are mostly package/licence/metadata linting
(`SUB.*`, `SCAN.*`) — but one rule, **REVIEW.006**, is a genuine geometry+physics check: "The
root USD must open and render in an RTX renderer such as Isaac Sim, and an asset with physics
must survive a simple drop onto the ground with the PhysX engine without falling apart,
exploding or passing through the ground." **Why it matters here:** different domain
(robotics sim assets, not mechanical CAD; OpenUSD, not STEP/STL/IFC — out of this project's
scope, no action triggered), but it is a second real-world instance (after this project's
own design) of a load+physics gate on agent-produced 3D content, independent of an LLM
judge. Worth knowing exists, not worth building toward.

**Added 2026-11-12 — [MeltFlex][meltflex] (MeltFlex s.r.o.), generation-only,
Claude-Code-native.** Verified directly via the npm registry (`npm view meltflex-mcp`):
`meltflex-mcp@0.6.0`, MIT licensed, published by `meltflexai`, depending on the official
`@modelcontextprotocol/sdk`. Its own registry description: "MeltFlex AI — generate
photorealistic interior designs from your AI agent. MCP server + CLI." The `meltflexai.com`
`/cli` page (read directly) confirms the CLI turns a room photo into a redesign, installed
with `npm install -g meltflex-mcp` exactly as the page states; the same domain's `/mcp` page
(the page this entry links) confirms the same binary also runs as an MCP server for Claude
Code and Cursor — among others; the page's own client tabs name eight, including Codex, VS
Code and Windsurf, so this is a representative pair, not the full list — a thin client over
the paid MeltFlex API; the website itself states no licence for the service (the MIT licence
above is the npm package metadata, not a site claim), and its only public GitHub link is the
companion skills repo, `MeltFlexDevs/skills`.

A separate product, MeltFlex's AI-BIM-software page (read directly), builds a BIM model and
"exports as IFC4" — **corrected 2026-11-12**: the page's own words are "the generator is for
the concept stage" (not "concept stage only," which over-quoted it) — with no automated model
checking: "It does not check building permits." Generation-side only, same shape as
everything else in this table.

**Added 2026-11-12 — Kyrall (Munich), intent-to-parametric-CAD, one claim corrected.** An
owner lead described Kyrall as parametrizing STL meshes into editable CAD feature trees
exported to Onshape; neither a Xometry interview with co-founder Osama Atwi (its page
403s to automated link checks, so it is cited in prose, not linked; **re-read 2026-11-12**
via the site's own public WordPress REST endpoint,
`xometry.pro/en/wp-json/wp/v2/articles?slug=ai-interviews-kyrall`, which does not 403) nor
[DEVELOP3D's launch coverage][kyralld3d] (trade press, already a source elsewhere in this
file) describes Kyrall itself taking an STL mesh, scan, or point cloud as generation input —
the claim does not hold. **Corrected 2026-11-12:** the original wording here ("mentions STL,
mesh, scan, or point-cloud input anywhere") overstated the absence — the Xometry interview
does mention STL once, as the input to a hypothetical third-party app built on Kyrall's API
("an app that takes an STL file of a tool and builds a shadow box around it"), not as
Kyrall's own mesh-to-CAD path; that distinction, not a blanket absence, is what rules the
owner lead's claim out. What is confirmed instead, from Atwi's own words in the Xometry
interview: the product aims to preserve what Atwi calls "design intent" — the sequence of
decisions behind a part, which he says a STEP or STL export loses — by generating a script
that generates the model (code-gen, not scan-to-CAD); "as of now we can read and write in
Onshape," and can additionally *read* (not yet write) CATIA, NX, SolidWorks and Creo. Its
"Context Manager" (per DEVELOP3D) lets a user upload specs/rules so output follows house
data; Atwi says Kyrall is "embedding DFM tests right now, focusing first on three-axis
milling and FDM, SLA, and SLS printing," where "the user chooses the
manufacturing method, and the part is altered to meet the checks" — an auto-correct-to-pass
loop, the same shape as the CADCodeVerify/Query2CAD pattern this project's own red-team
already weighed and rejected for itself (§2), not a new consideration, but worth knowing
another vendor is building toward it. **Medium overlap** — same shelf as AdamCAD/Backflip
above, generation-side, no independent (human- or render-gated) verification described.

**Added 2026-11-23 — two owner leads: SOMA and an MIT-funded interview study.**

**[SOMA][soma]** (Rank: adjacent (low); [repo][somagh], GPL-3.0, TypeScript/Electron, 520★
on 2026-11-23, read at commit `cf8e629` of 2026-11-22). A desktop app in which an agent writes a CadQuery
model. The agent is either its built-in SOMA AI or a CLI agent (Claude Code, Codex CLI and
others) in the app's terminal. The app rebuilds the model on every change and shows it in a 3D
viewer. What it checks, from the README, the home page, the [agent template][somaagents] and
the [analysis skill][somaanalysis] (two of its 21 skill files read):

- The agent runs `soma build` after every change and fixes build errors itself.
- `soma render` writes a picture, and the template tells the agent to open it and look at it
  to check its work. The model judges its own render, inside its own loop.
- `soma analyze overhang | thickness | clearance` gives a value at every spot of the surface
  and flags critical ones. The thresholds come from the active skill, or default to above 45°,
  below 1.2 mm and below 0.5 mm. Clearance has one threshold, a minimum.
- FEM with CalculiX, and the person: the home page says "You are the designer: you decide
  what to build, check the result and point at what is wrong." The viewer has section and
  explode tools.

Our reading. SOMA joins `agentcad` and `cad-skill` in doing both render and checks (the
"Honest read" above). Its checks, though, are printability fields (overhang, wall, gap), not
the watertight, volume and bounds checks those two and this gauge run. Three contrasts with
this project's rules, limited to the files read:

- the agent's look at its own render sits in the loop, where plan §3.1 keeps a model
  advisory and outside any gate;
- an analysis with no threshold from a skill falls back to a default rather than reporting
  `SKIP`;
- the clearance check is minimum-only, where `.claude/rules/verification-honesty.md` asks for
  two-sided windows. Its tolerances skill wasn't read, so fits may be covered there.

Its section tool is prior art for row VIEWS (plan §5), if the M3 table calls for a section
view. **Effect on the plan:** none. It checks its own output, so like ArchLang (§3.7) it isn't
a consumer, and it hasn't asked (ADOPT's trigger). Being GPL-3.0, nothing is copied from it
into this Apache-2.0 repo.

**[Agentic AI in Engineering and Manufacturing][agenticmfg]** (Rank: adjacent (low);
arXiv:2604.09633, Edwards, Bauer, Jacquillat, Hart and Ahmed, funded by the MIT Initiative for
New Manufacturing; CC BY-NC-ND 4.0, so paraphrased here). A qualitative study of 33
interviews across 28 companies: large enterprises, small and medium firms, AI developers, and
CAD/CAM/CAE vendors. It evaluates no agent-made CAD, and the authors call their sample limited
and non-random. What interviewees report:

- in safety-critical work, AI stays advisory and people validate its suggestions;
- organisations say they can't deploy AI for mission-critical work until verification
  methods mature;
- 3D CAD models "remain largely opaque to current foundation models", and some teams hand
  geometric queries to CAD kernels, which the authors call exploratory;
- a defence contractor's engineering manager runs AI designs through the same review
  checkpoints as human ones: "If it passes the logic reviews, it gets approved."

The authors suggest dedicated validation checkpoints for AI output as its volume grows. Our
reading: it's interview evidence for the plan's premise that checking, not generating, is the
gap. "Passes review, so approved" is the step where a necessary check gets read as a
sufficient one, which is the reading this gauge's wording rules out. **Effect on the plan:**
none. It supports §3.1's framing and names no tool to check against.

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

**Added 2026-11-14 — [Claude for Manufacturing][claudemfg]** (Rank: adjacent (low)), Anthropic's plugin (v1.0.0, a
reference implementation marked not actively maintained; [announced][claudemfgpost]
2026-11-12). It has 17 skills, mostly plant work: RFQ intake, quoting, NCR and 8D write-ups,
breakdown diagnosis, the morning production report, and sourcing. Two skills touch CAD, both
through the Fusion MCP connector, the only connector the plugin declares:

- `design-space-explore` changes parameters on an engineer's existing Fusion model to make
  a batch of variants, never designing from scratch or overwriting the base. Before
  generating, it checks that the chosen parameters drive the geometry. Per variant it
  checks only that the model regenerated, then records mass, volume and bounding box.
- `trade-study-report` ranks the variants against the engineer's requirements, with a
  sensitivity analysis.
- The quote chain can build a part in Fusion from a drawing and shows the model for a yes.

Read from its [`SKILL.md`][claudemfgdse]. Its checks are the same class as this repo's
preflight: the part regenerated, and envelope, mass and volume fit. Nothing checks that the
variant's features still do their job, and every skill ends with a person approving. It is
*not* plan §3.1's target case: a parameter sweep makes parts that differ on purpose, so
there's no fixed acceptance contract, and any per-variant band would come from the same
model that made the variant. **Effect on the plan:** none. Relevant only if the owner has a
Fusion model they would sweep and would review every variant's render.

**Added 2026-09-19 — the same pattern recurring on Revit, not just Fusion.** Autodesk's own
Revit 2026-2027 "what's new" blog (403'd on direct fetch, recovered via search + third-party
corroboration — Hagerman, BARVEA, goto.archi — medium confidence, not directly fetched)
reports Revit 2027 makes its **own MCP server publicly available** (six tool groups: model
queries, sheets, rooms, schedules, exports, element ops). This is the second confirmed
instance of Autodesk opening first-party MCP access across its product line, not a one-off.

Alongside it, a real community ecosystem exists, all generation/execution, not verification:

| Project | What it does | Verification capability |
|---|---|---|
| `revit-mcp` / `revit-mcp-server` (multiple forks: 3d-mcp, ahmedovelyor-ai, GenproMM, Demolinator) | pyRevit-based MCP, 48 tools — design, editing, analysis, MEP, interop, documentation | Lists a `check_clashes` tool ("hard clashes between disciplines"). **Mechanism unconfirmed** — checked the README directly; it does not say whether this wraps Revit's own native Interference Check engine or is separate logic. Not verified either way |
| Mira ([pirros.com](https://www.pirros.com/)) | Natural-language Revit automation (place walls, tag elements, set up sheets), trained on firm-specific workflows | None — generation/automation only. Notable: confirmed built on **Claude + MCP** (third confirmed instance of the Claude/MCP/Autodesk-product pattern, after Fusion's official connector and Revit 2027's native MCP) |
| BIBIM ([SquareZero-Inc/bibim-revit](https://github.com/SquareZero-Inc/bibim-revit)) | Open-source, BYOK across 4 LLMs (Claude Sonnet 4.6/Opus 4.7, GPT-5.5, Gemini 3.1 Pro), natural-language → C# code for Revit/ArchiCAD | None on the *generated design* — but has a genuinely good safety pattern worth noting separately from the verification question: multi-step planner, dry-run mode, one-click rollback, confirmation before applying changes |
| ArchiLabs ([archilabs.ai](https://archilabs.ai/sdk)) | Code-first Python SDK ("Studio Mode") mirroring every UI action; claims workflow checks beyond geometry clashes — computing derived metrics (Mechanical/Electrical Load Component) and generating compliance reports | **The one real exception found, still unconfirmed.** This is the most substantive verification-adjacent claim in the entire Revit ecosystem — but sourced from marketing-adjacent blog copy, not primary technical documentation. Whether the MLC/ELC computation is deterministic math over model data or LLM-estimated was not established. Flag for a follow-up technical-docs fetch before treating as settled — do not cite as a confirmed render+VLM-style analogue yet |

**Net effect on the standing verdict:** unchanged. No render+VLM output-verification analogue
was found for Revit either — ArchiLabs is a genuine open question, not a counter-example yet.

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

### 3.7 BIM — three regimes; IFC adopted behind a data gate

Raised 2026-09-10 as a scope question (broaden this project to Building Information
Modeling for "synergies"). Investigated across two research passes rather than answered from
intuition. Verdict: **BIM is not one verification problem, it is three, and they don't
share this project's shape.**

**Updated 2026-10-06, on the premise that a BIM user with real project data exists.** Two
verdicts below change; §3.7.1 holds the evidence. Regime 1: the conclusion that BIM "needs
nothing from this project" was about a *render+VLM* gate, and still holds — but deterministic
clash detection is now an open, headless tool (IfcClash), so the gauge can report it as a
**gate** cheaply. Regime 3: compliance **splits** — requirements already encoded as IDS are a
deterministic gate; interpreting legal text stays inform-only. The plan carries this as a
data-gated milestone (plan §13).

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
returns a plausible pass. The first sweep found only **generic prompted LLMs**
(arXiv:2506.20551, arXiv:2407.21060, door-detection arXiv:2509.17283,
[BIM-Edit benchmark][bimedit]). **Corrected 2026-10-06 — that was incomplete:** fine-tuned
systems exist and beat prompting. [P4IR][p4ir] (SFT then GRPO) beats frontier models
zero-shot on code-compliance generation, and a National Building Code of Canada QA system
([arXiv:2505.04666][nbcqa]) finds fine-tuning plus retrieval beats either alone. Both
fine-tune *behaviour* (output structure, judgement), not the code text itself — consistent
with the general finding that retrieval beats fine-tuning for injecting facts
([arXiv:2312.05934][ragvsft]). No Solibri-equivalent authoritative gate exists for
*interpreted* compliance, and gating on "code-compliant" would be the CAE false-confidence
failure with extra steps. The exception is requirements someone has already encoded as IDS:
those are a deterministic data check (§3.7.1), and [CORENET X][corenetx]'s own checker
claims only the "straightforward" geometric/spatial subset is machine-checkable. The same caution `cae.md` applies to stress
checks applies here without modification — and generalizes further: footing/foundation
design checks (base pressure vs. allowable soil bearing, stability, strength design) are
*also* CAE-shaped rather than bbox-shaped, since allowable bearing pressure depends on a
geotechnical report's assumptions, not a direct measurement of the artifact.

**Added 2026-10-26 — free alternatives to Revit for an agent BIM track** (owner bar: free
tools only). Researched by read-only agents; the load-bearing claims re-checked by the lead
at source. **The free, headless route is IfcOpenShell itself:** its Python API authors real
geometry — `ifcopenshell.api.geometry` has `create_2pt_wall` and wall/slab/door/window
representations — so an agent can write IFC with no Blender or FreeCAD (IfcOpenShell is
LGPL-3.0). The same repo ships official CLIs — [`ifcedit`][ifcedit] ("exposes all 350+
`ifcopenshell.api` mutation functions as shell commands", e.g. `ifcedit run model.ifc
root.create_entity --ifc_class IfcWall`) and `ifcquery` (inspect, validate, clash, render) —
and an MCP server, [`src/ifcmcp`][ifcmcp] (last commit 2026-10-25). This project prefers the
CLIs where both exist. The GUI-based options are weaker for a
headless agent: Bonsai (GPL-3.0, in the same repo) runs inside Blender, and its two agent
integrations found (`Show2Instruct/ifc-bonsai-mcp`, MIT; `ProfRino/bonsai-bim-skills`,
GPL-3.0) both document a GUI step; FreeCAD's BIM workbench creates walls under the headless
`FreeCADCmd`, but its IFC exporter imports `FreeCADGui` unconditionally
(`src/Mod/BIM/importers/exportIFC.py`, line 48), so headless IFC export likely fails —
read from source, not run. Commercial tools offer no free headless Linux path: Archicad,
Vectorworks and Allplan offer education or trial licences (agent-reported), and BricsCAD,
the one with a Linux build, discontinued its free Shape tier in V26 ([Bricsys][bricsshape]).
Other IFC libraries — web-ifc (MPL-2.0, read/write, no documented authoring API) and IFC++
(MIT, active) — are readers/writers rather than authoring tools. **Independence caveat:** a
track that authors with IfcOpenShell and is scored by the IfcOpenShell-based checker (§13)
shares one library on both sides, so a library bug can pass its own output; such a track
needs an independent cross-check (e.g. web-ifc tessellation or the buildingSMART validator).
The strongest candidate found is [ifc-lite][ifclite] (MPL-2.0, pushed 2026-10-26): "parse,
view, query, edit, validate, and export" with a CLI and its own "Rust/WASM core with
exact-arithmetic geometry kernel" — a second kernel, not IfcOpenShell's. The bench BIM track
(`bench/run.sh … ifcopenshell`) scores only the IfcOpenShell-tessellated STL so far; the
cross-check is not wired.

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
- **Ingestion for building codes / logs — checked 2026-09-19, one hit, one miss.**
  [Jev/TypeSafe][jev] is **not** an ingestion tool — it's a proprietary fast
  calibrated-decision API (pick-one-of-255, a 0-10 score, or a yes/no probability) over
  context already provided, no extraction/structuring capability at all; wrong fit for
  parsing raw building codes or CAD-tool log files. [GLiFormer][gliformer] (Knowledgator) is
  the real match — Apache-2.0, `pip install gliformer`, released 2026-09-16, encoder-only
  (fast, no token generation), with dedicated heads for NER, classification, relation
  extraction, and nested structured-record (Pydantic) extraction. Confirmed directly against
  its own repo: it explicitly handles **PDF-with-layout** ("extract fields from a PDF using
  both text and word bounding boxes") — a direct fit for building codes/laws, typically
  PDFs with section hierarchy. Plain-text logs (AutoCAD/Revit) would use its standard
  NER/relation-extraction heads instead — pulling structured entities (error codes, element
  IDs, operations, timestamps) out of log text. One honest gap: the repo doesn't explicitly
  claim table or technical-drawing extraction, which matters if a given code leans on
  tabular clearance/occupancy data — untested, not confirmed either way. This is the
  preprocessing/ETL layer the hybrid fine-tune+RAG verdict above (Regime 3) needs, not an
  alternative to it: it would turn raw PDFs/logs into the structured, retrievable records
  that retrieval layer requires, nothing more.

**Added 2026-11-14 — [Constor][constor]** (Rank: adjacent (low)) ([YC Fall 2026][constoryc], team of 3) does
quantity takeoffs for construction subcontractors, starting with HVAC and insulation trades.
It reads PDF drawings, extracts piping, duct, surface and equipment quantities into a table
for a quote or ERP, and lifts the checked systems into 3D. Planned next: bidding, GC revision
coordination and supplier pricing. It works on 2D PDFs, not IFC. The only check described is
the user reviewing the quantities against the plans; no accuracy figure is published. Its
LinkedIn page wasn't readable, so it isn't cited. **Effect on the plan:** none. One company
is no trend, but it prompts a question for MB's data gate (§5): does the BIM user we'd ask
have IFC files at all, or only PDFs?

**Added 2026-11-15 — [ArchLang][archlang]** (Rank: adjacent (low); [repo][archlanggh], MIT,
TypeScript, single maintainer, release v1.62.0 on 2026-11-15). It's a text DSL for 2D floor
plans: an agent writes `.arch` source, and a deterministic compiler draws a dimensioned plan
(SVG, DXF, PDF) and reports what's wrong.

- **Checks:** reachability and area are errors; everything else is advisory lint, e.g. a
  bedroom with no window, or a blocked doorway.
- **3D:** a separate package extrudes the plan to a GLB and checks it before writing: closed
  shells, every 3D element traceable to the plan, glTF-Validator clean.
- **Limits it states itself:** no BIM or IFC, no permit drawings, no image reading.
- **Where it ships:** CLI, MCP server, agent skill, VS Code extension, a
  [playground][archlangplay], an 11-plan [gallery][archlanggallery] that is explicitly "not
  a benchmark", and a [guide][archlangguide].

It's the same shape as this repo: an agent generates, deterministic checks report, a human
decides. It's for a different artefact, though: 2D plans, not meshes. Its evaluation method
is the most developed we've seen, and is summarised in
[`benchmarking.md`](benchmarking.md) §4. **Effect on the plan:** none. It isn't a consumer,
since it checks its own output, and the gauge would duplicate its GLB checks.

#### 3.7.1 IFC toolchain and standards — verified 2026-10-06

Researched by four read-only subagents against primary sources, then the open questions
verified a second time. **E** = verified empirically by installing the packages on Python
3.12/Linux and running them; **S** = fetched from the primary source.

| Finding | Evidence |
|---|---|
| [IfcOpenShell][ifcopenshell] 0.9.0 installs from cp312 manylinux wheels; `ifcopenshell.geom` turns each IFC element into triangles that **trimesh** checks directly. A synthetic IFC4 wall (5 × 3 × 0.2 m) came out watertight with volume exactly 3.0 | E |
| `ifcopenshell.validate` (schema) runs headless; IfcClash 0.9 source has `intersection`, `collision`, `clearance`, `allow_touching`, `tolerance` modes; IfcTester 0.9 targets IDS 1.0 (`1.0/ids.xsd`) | E |
| Quantity-takeoff consistency needs no extra tool: `ifcopenshell.util.shape` ships `get_volume`, `get_area`, `get_side_area` etc. (`get_volume` matched trimesh at 3.0). `ifc5d` is a separate package | E |
| Licences: ifcopenshell, ifcclash, ifctester are **LGPLv3+**; **ifctester hard-depends on `bcf-client` (GPLv3) and Flask**. Compatibility with this repo's Apache-2.0 is an owner decision, not settled here | E (package metadata) |
| trimesh: only hard dep `numpy`, MIT; `body_count` needs `scipy` at runtime | E |
| [IDS][ids] 1.0 is a final buildingSMART standard (v1.0.0, 2024-06-03). It expresses information requirements only — no geometry or rule logic | S |
| [buildingSMART Validation Service][bsivalidate]: MIT, Docker self-hostable, REST API — schema + normative rules | S |
| Revit exports IFC4.3: [`Autodesk/revit-ifc`][revitifc] ships IFC4x3 entity code; release IFC_v25.4.40 (2026-01-14) adds IFC4.3 Reference View. The exporter is LGPLv2 + a proprietary DLL, with many open issues — exporter bugs surface as model "defects" | S |
| Native `.rvt`: APS Model Derivative converts `.rvt` → IFC2x3/IFC4 over plain REST, no C# or Windows ([APS blog][apsifc]); APS Design Automation **requires** a compiled C# add-in; [`rvt-rs`][rvtrs] (Apache-2.0, Python bindings) is an open reader for Revit 2024–25, young and partial | S |
| [`web-ifc-three`][webifcthree] is **deprecated** (pins three ^0.128); its successor `@thatopen/components` needs three ≥ 0.182. Exporting IFC → `.glb` for the existing three.js viewer avoids that constraint | S |
| APS pricing: **no caps or prices published as text**. Only figure found: Model Derivative "Basic Interactions" cost 1 Flex token per 300,000 calls, minimum 100 tokens ([APS blog][apsbiz]) | S, incomplete |
| [CODE-ACCORD][codeaccord]: 862 annotated sentences (England + Finland codes), CC BY 4.0 — training data for rule extraction | S |

**Still unverified:** the Flex token price and Free-tier caps; whether ISO 19650-5 explicitly
covers disclosure to third parties (only its general scope was confirmable — the standard is
paywalled); ICC Code Connect pricing (not publicly priced); and behaviour on **real exported
project data** — every empirical check above used a synthetic model.

#### 3.7.2 AutoCAD and Revit logs as evidence — researched 2026-11-15

**Rank: adjacent (low).** The owner asked how to handle and evaluate the logs AutoCAD and
Revit write while DWG/DXF or IFC files are created, especially by an agent or a script with
no user present. Two read-only subagents searched for this. **R** = read at the source,
**S** = search snippet only. Licences marked **V** were checked on GitHub.

##### AutoCAD

- **Command-history log:** `LOGFILEMODE` turns it on, and it's off by default
  ([R][acadlogmode]). `LOGFILEPATH` sets its folder ([S][acadlogpath]). Autodesk documents
  no format; it's the command-line text.
- **AUDIT:** it "corrects some errors" but not all; for the rest, use RECOVER
  ([R][acadaudit]). With `AUDITCTL` = 1 it writes a `.adt` report of each problem and the
  action taken ([S][acadauditctl]).
- **Action Recorder:** records macros, not diagnostics ([S][acadactrec]).
- **Headless runs with Core Console (`accoreconsole`):** commands that need a dialog are
  unsupported, so use dash forms like `-LAYER`. Scripts must supply every input. `/l` pins
  the language. Autodesk tells developers to log progress and failure points themselves
  ([R][acadcore]). **No Autodesk source documents its exit codes**, so treat them as
  unknown.
- **Autodesk Platform Services Design Automation (AutoCAD):** runs `accoreconsole` in the
  cloud. A work item returns a status and a `reportUrl` to `report.txt`
  ([R][apscallbacks], [R][apsfield]). The report's errors look like
  `ERROR: … ErrorStatus=434` and map to `Acad::ErrorStatus` ([R][apsacaderr]). A failure may
  show only in the report (one forum thread, snippet only, not cited).
- **Checking the file without AutoCAD:**
  - [ezdxf][ezdxfrecover] (MIT **V**, pure Python, Linux): `recover.readfile` returns the
    drawing plus an auditor's findings, for DXF only.
  - [LibreDWG][libredwg] (GPL-3.0 **V**): `dwgread` and `dwg2dxf` command-line tools.
  - [ODA File Converter][odafc]: DWG/DXF with an audit flag, Linux builds ([S]). Its licence
    wasn't found and one index lists it as unfree, so check its EULA first.

##### Revit

- **Journals:** one per session, in a hidden per-user folder, recording "the actions taken by
  the software during a session" ([R][rvtjournal]). Autodesk publishes no format and
  supports journals only as "a replay mechanism for testing or reporting issues". Expect
  "incompatibilities between versions", and a modal dialog can block replay
  ([R][rvtreplay]). The folder path includes the user name. Whether the file itself holds
  personal data wasn't checked.
- **IFC export:** Revit writes "a log file for the export process" next to the IFC
  ([R][rvtifclog]). Its name and content aren't documented.
- **Design Automation (Revit):** documented statuses are `pending`, `inprogress`,
  `cancelled`, `failedLimitProcessingTime`, `failedDownload`, `failedInstructions`,
  `failedUpload`, `failedUploadOptional` and `success`. The `reportUrl` is valid for 24
  hours, and status is kept for 3 days ([R][apsworkitem]). `success` doesn't say the output
  is right, and `failedUploadOptional` means some outputs may be missing.

**Published practice:** none found that's specific to CAD or BIM, either for treating tool
logs as evidence or for evaluating agent sessions from AutoCAD or Revit logs. Near
neighbours are generic MCP benchmarks, an IFC MCP framework and IFC Copilot (all [S]).
OpenTelemetry's conventions for agent tool calls exist but are still in development, and
only vendor summaries were read ([S]).

**What it means here (our inference, applying existing rules):**

- **A log is advisory evidence and never a gate** (`.claude/rules/verification-honesty.md`).
  Gate on the artifact: it exists, isn't empty, parses (ezdxf or IFC), and passes preflight.
- **Exit 0 without output is FAIL** (§11 of the plan, the i3mega/PrusaSlicer precedent).
  Neither `accoreconsole` exit codes nor a `success` status prove a good file. Have the
  script write its own end marker, and treat a missing marker as FAIL.
- **A log that wasn't produced is SKIP, not PASS,** e.g. `AUDITCTL` or `LOGFILEMODE` off.
- **Parse loosely:** pin the language (`/l en-US`), match `ERROR`/`ErrorStatus` lines,
  record unparseable lines as "unparsed", not clean, and never infer success from the
  absence of an error line. The §3.7 extraction note (GLiFormer) is one option for turning
  log text into records.
- **Keep logs per run in a unique path,** with a SHA-256 and the tool version (as
  `bench/provenance.py` does). Save Design Automation reports before their 24-hour link
  expires. Redact user names and paths before keeping anything.

**Effect on the plan:** none. No plan row consumes DWG or Revit output today. MB (IFC) would
gain the export-log and `failedUploadOptional` points if it activates.

[acadlogmode]: https://help.autodesk.com/cloudhelp/2022/ENU/AutoCAD-LT/files/GUID-C0C25385-F210-4834-B7D4-B29C2592D36A.htm
[acadlogpath]: https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-LT/files/GUID-0E2D4DF2-4C26-48AC-ACBC-819E3C46CE59.htm
[acadaudit]: https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-LT/files/GUID-62DDB935-61B1-49DA-8238-3EF1CC45259B.htm
[acadauditctl]: https://help.autodesk.com/cloudhelp/2022/ENU/AutoCAD-LT/files/GUID-05A7363C-4A43-4984-8262-DA7BEE7B860C.htm
[acadactrec]: https://help.autodesk.com/cloudhelp/2022/ENU/AutoCAD-Core/files/GUID-6254B281-6523-4C56-AC9E-CDEE32A27606.htm
[acadcore]: https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Core-Console/files/AUTOCAD_CORE_CONSOLE.html
[apscallbacks]: https://aps.autodesk.com/en/docs/design-automation/v3/developers_guide/callbacks
[apsfield]: https://aps.autodesk.com/en/docs/design-automation/v3/developers_guide/field-guide
[apsacaderr]: https://aps.autodesk.com/blog/autocad-design-automation-error-codes
[ezdxfrecover]: https://ezdxf.readthedocs.io/en/stable/drawing/recover.html
[libredwg]: https://github.com/LibreDWG/libredwg
[odafc]: https://www.opendesign.com/faq/question/are-there-command-line-examples-support-windows-and-linux-operating-systems-deb.md
[rvtjournal]: https://help.autodesk.com/cloudhelp/2014/ENU/Revit/files/GUID-477C6854-2724-4B5D-8B95-9657B636C48D.htm
[rvtreplay]: https://blog.autodesk.io/journal-file-replay/
[rvtifclog]: https://help.autodesk.com/cloudhelp/2025/ENU/Revit-DocumentPresent/files/GUID-14037C31-EBAD-41A8-9099-E6DD65BB626E.htm
[apsworkitem]: https://aps.autodesk.com/en/docs/design-automation/v3/reference/http/workitems-id-GET

### 3.8 Videos, transcripts and model repositories — researched 2026-11-22

**Rank: adjacent (low).** The owner asked what can be learned from videos of agents doing
CAD, how to get their transcripts, and whether model sites such as Thingiverse help. Read-only
subagents and polyfetch tests from this Codespace. **R** = read at source, **S** = search
snippet only.

#### Agent-CAD videos on YouTube

YouTube blocks this Codespace ("Sign in to confirm you're not a bot") for playback and
captions. That holds on polyfetch's browser tier, both headless and headed, and on yt-dlp
2026.10.26. Title and channel still come from YouTube's oEmbed endpoint, and the watch page
still gives the description and chapters. So these are judged from **title, description and
chapters only**:

- **Six Claude + FreeCAD (MCP) videos the owner supplied:** Make Form `6trAkQY5_kc` and
  `xh-VzN6aqV4`, Joseph Wu `6rDDWx1hXH8`, `MrOUIC1TJGY`, CAD Creatives `Vk5udhBfj4w`, and
  The Stack Underflow `afRByXEssXk`. Only the last, with 771 views, shows the part being
  checked ("Check it with FreeCAD's numbers"; "8 is not 8 mm").
- **Ten more found by search** (oEmbed-confirmed). The most relevant:
  - The Stack Underflow `868tnyHR_ks`: "SolidCraft vs FreeCAD in Claude Code: Same Bracket,
    Two Different Failures"
  - Türkişi Engineering `hIVY_jWk_I8`: five agentic tools build one design in FreeCAD,
    Fusion and build123d, with volumes compared (S)
  The others are Fusion, Zoo, MecAgent, Revit (pyRevit MCP), an STL-to-parametric video, and
  a Japanese FreeCAD video whose title says "not yet time to delegate everything".
- **What the two Stack Underflow transcripts say** (read via QuickTube, paraphrased):
  - FreeCAD called the cable clip "valid" after a unitless `8` was typed into its parameter
    spreadsheet, and the part stayed at the old 6 mm. "Valid" meant one solid piece, not the
    size asked for.
  - SolidCraft answered "okay" to a cut that went through empty space; only an unchanged face
    count and volume showed it.
  - The channel's own conclusion is to measure the exported file, not the tool's report. It
    measures every export with its own code in Docker.
  This is this repo's thesis, demonstrated independently.
- **What 12 more transcripts show** (fetched via QuickTube on 2026-11-22, auto-captions,
  summarised by a subagent and paraphrased here; the transcripts aren't in the repo):
  - **Checking is mostly looking.** The agent's own viewport screenshot plus a human glance
    is the usual check. Real measurement is rare: one Measure-tool pass (`6trAkQY5_kc`), and
    a blind cross-check that booleaned five agents' parts against each other at 0.000 mm³
    difference (`hIVY_jWk_I8`). The author of the latter says his own scoring rubric was too
    coarse to tell the agents apart.
  - **Wrong but plausible parts are the usual failure, and a human catches them:**
    - a pegboard pattern asked for as 10 × 10 came out at half density (`33H-3WURC80`)
    - a pattern feature was left outside the body (`33H-3WURC80`)
    - a CAM finish pass was put on the wrong side of a wall (`IZ__MZeZ-F4`)
  - **Tool reports misled:**
    - FreeCAD's IFC exporter silently dropped an upper floor slab, which only showed when the
      file was opened in a second tool (`QlppsgdSW-Q`)
    - a Fusion mass-property tool misbehaved (`hIVY_jWk_I8`)
    - a fillet call timed out, then "looked fine" (`Vk5udhBfj4w`)
  - **Stated limits:** the authors say constraint-heavy mechanical parts and drawings as input
    are weak spots, while patterned or organic shapes come easily (`xp52dUrZfiM`,
    `MrOUIC1TJGY`).
  - **Known-bad candidates, adopted as controls (owner 2026-11-22,
    `tests/test_bench_controls.py`):**
    - a half-density hole pattern (brief 10 with 6 of 12 holes): watertight with the right
      bbox, and the volume band catches it
    - a part missing one feature (brief 03 with no holes): the band can't see it, so it
      passes preflight and is asserted as the render's job
    - an export that drops an element: only an analogue fits, brief bim-02's wall with its
      door opening dropped, which the band catches; no brief has two elements to drop one of
    - the old size handed in after "change one number" (the 80 mm bracket for brief 17's
      100 mm one), after the cable clip that kept its old size: the band catches it
    - The Stack Underflow's lid and loft cases are deferred: brief 04 (the snap lid) has no
      volume band and no brief has a loft, so no bounded brief can host them
  - **Two videos have no transcript:** `6rDDWx1hXH8` and `Gen8rG40ntA`. A retry on
    2026-11-22 showed why: QuickTube reports that the uploader turned captions off. They
    stay judged from title, description and chapters.
- **Pattern:** many generation demos and almost no checking. No conference talk was found;
  FOSDEM 2026's CAD room had no AI talk.

#### Transcripts

- **The official YouTube Data API is no route.** `captions.list` and `captions.download`
  need OAuth. Download also needs "permission to edit the video", and list returns metadata
  only ([R][ytcapdl]).
- **[youtube-transcript-api][yttapi]** (MIT) calls YouTube's undocumented web endpoint. Its
  README says YouTube "has started blocking most IPs that are known to belong to cloud
  providers" (**R**). It supports proxies.
- **Hosted APIs fetch existing captions for public videos; only the URL leaves the machine:**
  - Supadata: 100 free credits a month, 1 credit per existing transcript (**R**).
  - SearchAPI.io: 100 free requests (**R**).
  Neither one's terms were read.
- **Speech-to-text** (local Whisper, or hosted services that receive the audio) needs the
  video file, so it doesn't help where YouTube blocks the download.
- **[QuickTube][quicktube]** worked from this Codespace (tried 2026-11-22). Its web form
  (no login) returned YouTube's auto-generated English transcripts for `afRByXEssXk` and
  `868tnyHR_ks`. Its REST API needs a key from a signed-in account. Only the video URL
  leaves the machine; its terms weren't read.
- **New uploads can be tracked without a login.** A channel's RSS feed
  (`feeds/videos.xml?channel_id=UC…`) and its uploads-playlist feed (`playlist_id=UU…`)
  each returned the latest 15 videos with HTTP 200, from this Codespace and from a
  GitHub-hosted runner (one probe run, 2026-11-22). oEmbed answered from the runner too.
  This finds new videos only; transcripts still need a route above. A shared monitor
  workflow is tracked, gated on a second caller, in [qte77/.github#75][gh-monitor].
- **[media.ccc.de][mediaccc]** is the clean route for talks. It has an open API, CDN
  downloads allowed under each talk's licence (often CC BY 4.0), and SRT/WebVTT subtitles
  where c3subtitles made them (**R**).

#### Model repositories (licences decide everything in an Apache-2.0 repo)

- **[Thingi10K][thingi10k]:** a pip package filters by per-model licence. It's STL only,
  meshes with real defects (S). This is the cleanest source of mesh fixtures; use only the
  CC BY and CC0 subset in the repo.
- **Thingiverse:**
  - The only bulk source of OpenSCAD source + STL pairs, and of "remix fixes X" known-bad
    cases (S).
  - Its terms and developer pages returned 403, so they weren't read.
  - Hand-picked, licence-checked models only.
- **Printables:** per-model licences chosen by the uploader, and no official API (**R**/S).
- **Not for committing to this repo:** the repo is public under Apache-2.0, which lets anyone
  use its contents commercially. A file under a non-commercial or no-redistribution licence
  must stay out of git even though this project itself is non-commercial. Local use, fetched
  at test time into a git-ignored cache, is a separate question; per source:
  - [Fusion 360 Gallery][f360gallery]: non-commercial research only, no redistribution (**R**).
    Local use for this project's non-commercial research fits those terms.
  - ABC (copyright stays with the creators, under Onshape's terms) and DeepCAD (no stated data
    licence, derived from ABC) (**R**).
  - Onshape public documents: automated data mining is barred (S).
- **CC BY-NC and CC BY-ND files never go in the repo.** Keep a manifest of each file's
  licence and attribution.

**Effect on the plan:** none. Thingi10K (CC BY/CC0) is a candidate source of real defective
meshes for the control tests (BENCH-3 item 2), recorded as a suggestion.

[ytcapdl]: https://developers.google.com/youtube/v3/docs/captions/download
[yttapi]: https://github.com/jdepoix/youtube-transcript-api
[mediaccc]: https://media.ccc.de/about.html
[thingi10k]: https://pypi.org/project/thingi10k/
[quicktube]: https://quicktube.ai/api-docs
[gh-monitor]: https://github.com/qte77/.github/issues/75
[f360gallery]: https://raw.githubusercontent.com/AutodeskAILab/Fusion360GalleryDataset/1084b881f3bb710267801d812d6e9286b8667059/LICENSE.md

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
| [BenchCAD-org/benchcad-2-main][benchcad2] | BenchCAD 2.0 scoring harness, read directly (tasks, metrics, license, reference lines) |
| [BenchCAD-org/benchcad-2][benchcad2data] | BenchCAD 2.0 data pipeline repo, read directly (license) |
| [OpenAI — accelerating engineering for the physical world][openaiphysical] | OpenAI's own BenchCAD 2.0 claim (0.594/0.875) and Codex test-device case study, read directly (plain fetch 403s; TLS-fingerprint block, not access-gated); the 0.875 figure cross-checked live on benchcad.com's own leaderboard, also read directly |
| [NVIDIA-Omniverse/simready-central][simready] | SimReady Central intake pipeline, read directly (acceptance criteria, REVIEW.006) |
| [Hugging Face — SimReady Central Library][hfsimready] | NVIDIA's own HF blog post, read directly |
| [LGElectronics/simready-assets][lgsimready] | HF dataset, read directly (CC BY 4.0, 21 assets) |
| [Vertiv/simready-assets][vertivsimready] | HF dataset, read directly (CC BY 4.0, 41 assets) |
| [MeltFlex AI — MCP server + CLI][meltflex] | `meltflex-mcp` package (npm registry) and the CLI/AI-BIM pages, read directly |
| [DEVELOP3D — Kyrall launch coverage][kyralld3d] | Trade press, read directly; a separate Xometry co-founder interview is cited in prose only — its page 403s to lychee, so it was re-read via `xometry.pro/en/wp-json/wp/v2/articles?slug=ai-interviews-kyrall`, which does not |
| [AEC Magazine — GPT-6 Astra and BIM modelling][aecastra] | Read directly |
| [SOMA][soma] · [repo][somagh] | Home page, README, agent template and analysis skill, read directly (repo at `cf8e629`) |
| [arXiv:2604.09633][agenticmfg] | Agentic AI in engineering and manufacturing: 33 industry interviews, read directly |

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
[claudemfg]: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-for-manufacturing
[claudemfgdse]: https://raw.githubusercontent.com/anthropics/claude-plugins-official/65adb96f26deb662f6a993f74347d0ccd1a61a52/plugins/claude-for-manufacturing/skills/design-space-explore/SKILL.md
[claudemfgpost]: https://claude.com/resources/articles/claude-for-manufacturing
[constor]: https://constor.ai/landing/en
[constoryc]: https://www.ycombinator.com/companies/constor
[archlang]: https://archlang.uk/
[archlanggh]: https://github.com/ChanMeng666/archlang
[archlangguide]: https://archlang.uk/guide
[archlangplay]: https://playground.archlang.uk/
[archlanggallery]: https://archlang.uk/gallery
[sketch2bim]: https://arxiv.org/abs/2510.20838
[text2bim]: https://arxiv.org/html/2408.08054v1
[qwenbim]: https://arxiv.org/abs/2602.20812
[mcp4ifc]: https://arxiv.org/abs/2511.05533
[bimscript]: https://arxiv.org/html/2608.21447
[bimedit]: https://arxiv.org/abs/2606.20146
[autoaero]: https://arxiv.org/pdf/2605.27968
[leap71]: https://github.com/leap71
[picogklegacy]: https://github.com/leap71/PicoGK.Legacy
[picogkcore]: https://github.com/leap71/PicoGK.Core
[picogk118]: https://github.com/leap71/PicoGK/discussions/118
[noyron]: https://leap71.com/noyron/
[jev]: https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e
[gliformer]: https://github.com/Knowledgator/GLiFormer
[p4ir]: https://arxiv.org/html/2606.22402v1
[nbcqa]: https://arxiv.org/abs/2505.04666
[ragvsft]: https://arxiv.org/abs/2312.05934
[corenetx]: https://info.corenet.gov.sg/
[ifcopenshell]: https://github.com/IfcOpenShell/IfcOpenShell
[ids]: https://github.com/buildingSMART/IDS
[bsivalidate]: https://github.com/buildingSMART/validate
[revitifc]: https://github.com/Autodesk/revit-ifc
[apsifc]: https://aps.autodesk.com/blog/export-ifc-rvt-using-model-derivative-api
[rvtrs]: https://github.com/DrunkOnJava/rvt-rs
[webifcthree]: https://github.com/ThatOpen/web-ifc-three
[apsbiz]: https://aps.autodesk.com/blog/aps-business-model-evolution
[codeaccord]: https://arxiv.org/abs/2403.02231
[steenkencase]: https://engineer-your-idea.com/en/blog/agentic-cad-room-booking-sign/
[steenkenrun1]: https://engineer-your-idea.com/en/blog/agentic-cad-pi4-housing/
[solidcraft]: https://github.com/tangency-labs/solidcraft
[solidcraftoracle]: https://raw.githubusercontent.com/tangency-labs/solidcraft/769bea6b0b1c0e765b44e3053e421b8b1ef6fa4e/docs/oracle.md
[molitor]: https://www.linkedin.com/posts/dirk-molitor_engineering-ai-is-becoming-a-vendor-war-activity-7519290174040809475-23Qp
[molitor2]: https://www.linkedin.com/posts/dirk-molitor_the-race-to-reshape-product-development-is-ugcPost-7526214240760692736-AiIf/
[physicsxairplane]: https://www.physicsx.ai/newsroom/welcome-to-airplane
[physicsxmsft]: https://www.physicsx.ai/resources/physicsx-forges-strategic-collaboration-with-microsoft-to-accelerate-engineering-innovation-with-ai-for-science-platform
[neuralantolin]: https://www.neuralconcept.com/industry-stories/antolin-neural-concept-automotive-interior
[avevaai]: https://www.aveva.com/en/solutions/digital-transformation/artificial-intelligence/industrial-ai-for-engineering/
[hexagonmentor]: https://hexagon.com/company/newsroom/press-releases/2025/hexagon-unveils-autonomous-metrology-suite-to-deliver-manufacturing-quality-at-speed
[hexagoncadence]: https://hexagon.com/company/divisions/manufacturing-intelligence/msc-software
[cadencehexagon]: https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-completes-acquisition-of-hexagons-design-and-engineering.html
[cadence10q]: https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000121/cdns-20260930.htm
[molitorwp]: https://www.isst.fraunhofer.de/content/dam/isst/publikationen/whitepaper/AI-in-New-Product_Development_Whitepaper.pdf
[openaieng]: https://openai.com/index/accelerating-engineering-for-the-physical-world/
[onshapefsmcp]: https://www.ptc.com/en/news/2026/onshape-launches-featurescript-mcp-server
[rhinomcp]: https://github.com/tanishqbhattad/rhino-mcp
[rhino8req]: https://www.rhino3d.com/8/system-requirements
[rhino3dm]: https://github.com/mcneel/rhino3dm
[rhinocompute]: https://developer.rhino3d.com/guides/compute/core-hour-billing/
[rhinoai]: https://github.com/mcneel/rhinoai
[ifcmcp]: https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.9.0/src/ifcmcp
[ifcedit]: https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.9.0/src/ifcedit
[ifclite]: https://github.com/LTplus-AG/ifc-lite
[bricsshape]: https://www.bricsys.com/news/bricscad-shape-discontinued
[steenkenpost]: https://www.linkedin.com/posts/anton-steenken_ai-cad-demos-are-full-of-sht-sound-familiar-ugcPost-7513887143623319553-qmVG/
[leoai]: https://www.getleo.ai/
[leofaq]: https://www.getleo.ai/faq
[leocheck]: https://www.getleo.ai/blog/solve-engineering-problems-in-seconds-with-96-accuracy
[trace]: https://buildwithtrace.com/
[tracepublic]: https://github.com/buildwithtrace/trace-public
[tracecli]: https://docs.buildwithtrace.com/resources/cli/
[tracereview]: https://docs.buildwithtrace.com/concepts/design-review/
[kicadcli]: https://docs.kicad.org/9.0/en/cli/cli.html
[kicadmcp]: https://github.com/mixelpixx/kicad-mcp-server
[eagleeol]: https://www.autodesk.com/products/fusion-360/blog/eagle-to-autodesk-fusion-transition/
[fusionelectron]: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ElectronicsIntro_UM.htm
[fusionsysreq]: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/System-requirements-for-Autodesk-Fusion-360.html
[fusioncompare]: https://www.autodesk.com/products/fusion-360/personal/compare
[benchcad2]: https://github.com/BenchCAD-org/benchcad-2-main
[benchcad2data]: https://github.com/BenchCAD-org/benchcad-2
[openaiphysical]: https://openai.com/index/accelerating-engineering-for-the-physical-world/
[simready]: https://github.com/NVIDIA-Omniverse/simready-central
[meltflex]: https://www.meltflexai.com/mcp
[hfsimready]: https://huggingface.co/blog/nvidia/simready-central-assets-robotics-ai-factories
[lgsimready]: https://huggingface.co/datasets/LGElectronics/simready-assets
[vertivsimready]: https://huggingface.co/datasets/Vertiv/simready-assets
[kyralld3d]: https://develop3d.com/cad/kyrall-launches-its-ai-automated-cad-modeller/
[aecastra]: https://aecmag.com/bim/gpt-6-astra-and-the-future-of-bim-modelling/
[soma]: https://somacad.app/
[somagh]: https://github.com/Kai-Jungsthoefel/SOMA
[somaagents]: https://raw.githubusercontent.com/Kai-Jungsthoefel/SOMA/cf8e629ef0dc1c2c54ee3fb62d50a208aa938c27/app/resources/template/AGENTS.md
[somaanalysis]: https://raw.githubusercontent.com/Kai-Jungsthoefel/SOMA/cf8e629ef0dc1c2c54ee3fb62d50a208aa938c27/app/resources/skills/analysis.md
[agenticmfg]: https://arxiv.org/abs/2604.09633

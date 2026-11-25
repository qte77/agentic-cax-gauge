---
title: Landscape — evidence, competitors, backend choice, contribution stance
purpose: The research behind the design decisions, split out of plan 001 so the plan stays a plan
created: 2026-07-20
updated: 2026-11-25
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

### Entry index

This index lists the named entries in §3.1–§3.8, one row per table row or "Added" block. Dates and ranks are copied from each entry's own wording; "not stated" means the entry gives none. §3.8 is ranked adjacent (low) as a whole, in its intro, and that rank is not copied onto its rows. The entry text is the source, and this table points to it.

| Entry | § | Added or read at source | Rank |
|---|---|---|---|
| build123d | [§3.1](#31-backend-decision) | not stated | not stated |
| OpenSCAD | [§3.1](#31-backend-decision) | not stated | not stated |
| CadQuery | [§3.1](#31-backend-decision) | not stated | not stated |
| FreeCAD Python API | [§3.1](#31-backend-decision) | not stated | not stated |
| pythonocc-core | [§3.1](#31-backend-decision) | not stated | not stated |
| Onshape API | [§3.1](#31-backend-decision) | not stated | not stated |
| Blender bpy | [§3.1](#31-backend-decision) | 2026-11-11 (checked) | not stated |
| Rhino (rhino3dm / Compute) | [§3.1](#31-backend-decision) | 2026-11-11 (checked) | not stated |
| SolidPython | [§3.1](#31-backend-decision) | not stated | not stated |
| Fusion 360 API | [§3.1](#31-backend-decision) | not stated | not stated |
| Zoo / KittyCAD | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| AdamCAD | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| Backflip AI | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| CAD-Assistant | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| cad-agent | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| openscad-agent | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| BlenderLLM | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| ScadLM | [§3.2](landscape-adjacent.md#32-adjacent-projects) | not stated | not stated |
| MecAgent | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-14 (re-read) | adjacent (low) |
| Leo AI | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-24 (read at source) | adjacent (low) |
| jdilla1277/agentcad | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| flowful-ai/cad-skill | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| drawing-agent.com | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| CADSmith | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| rawwerks/VibeCAD, mfranzon/render, mitsuhiko/agent-stuff | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| EdwinjJ1/3d-print-skill | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-07-25 (sweep) | not stated |
| microsoft/CADFusion | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| CAD-Judge | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| AutoBrep | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| CAD-Llama | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| CADmium | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| OpenECAD | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| GeoCAD | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-10 (sweep) | not stated |
| LEAP71 (PicoGK) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-09-19 (corrected 2026-11-11) | not stated (its "Our reading" note says adjacent (low)) |
| Steenken case study, ABS housing (with his LinkedIn post) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-09 | not stated |
| Steenken's earlier run, Pi 4 housing in Fusion | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-11 | not stated |
| SolidCraft | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-19 | not stated |
| Molitor, the incumbents' AI race (LinkedIn) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-23 | not stated |
| Molitor follow-up, partnership map | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| PhysicsX Ai.rplane | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| The map's in-scope names, audited | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| AVEVA | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 (block date) | not stated |
| Hexagon | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 (block date) | not stated |
| Molitor's whitepaper | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| OpenAI on AI for hardware engineering | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| tanishqbhattad/rhino-mcp | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-26 | not stated |
| Rhino beyond rhino-mcp | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-11 | not stated |
| Blender: headless is easy, the domain is still wrong | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-11 | not stated |
| Trace (buildwithtrace.com) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-10-09 | not stated |
| KiCad and Fusion electronics (PCB beyond Trace) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-11 | not stated |
| BenchCAD 2.0 | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| NVIDIA-Omniverse/simready-central | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| MeltFlex | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| Kyrall | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-12 | not stated |
| SOMA | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-23 | adjacent (low) |
| Agentic AI in Engineering and Manufacturing (MIT-funded interview study) | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-23 | adjacent (low) |
| matchline | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-23 | adjacent (low) as a tool, but it changes a positioning claim |
| Solvaix | [§3.2](landscape-adjacent.md#32-adjacent-projects) | 2026-11-23 | adjacent (low) |
| earthtojake/text-to-cad | [§3.3](#33-earthtojaketext-to-cad--the-largest-adjacent-project) | 2026-07-20 (analysed; figures re-verified 2026-07-25) | not stated |
| jdilla1277/agentcad (closest on thesis) | [§3.4](#34-jdilla1277agentcad--the-closest-on-thesis) | 2026-07-25 (found by sweep) | not stated |
| ahujasid/blender-mcp | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| neka-nat/freecad-mcp | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| quellant/openscad-mcp | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| hedless/onshape-mcp | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| pzfreo/build123d-mcp | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| daobataotie/CAD-MCP | [§3.5](#35-cad-mcp-servers) | not stated | not stated |
| Claude for Fusion (Autodesk official MCP connector) | [§3.5](#35-cad-mcp-servers) | 2026-09-10 (found) | not stated |
| Community Fusion-MCP servers (8+) | [§3.5](#35-cad-mcp-servers) | 2026-09-10 (same sweep) | not stated |
| Claude for Manufacturing | [§3.5](#35-cad-mcp-servers) | 2026-11-14 | adjacent (low) |
| Revit 2027 MCP server and community Revit tools | [§3.5](#35-cad-mcp-servers) | 2026-09-19 | not stated |
| revit-mcp / revit-mcp-server | [§3.5](#35-cad-mcp-servers) | 2026-09-19 (block date) | not stated |
| Mira (pirros.com) | [§3.5](#35-cad-mcp-servers) | 2026-09-19 (block date) | not stated |
| BIBIM (SquareZero-Inc/bibim-revit) | [§3.5](#35-cad-mcp-servers) | 2026-09-19 (block date) | not stated |
| ArchiLabs | [§3.5](#35-cad-mcp-servers) | 2026-09-19 (block date) | not stated |
| Claude computer use | [§3.6](#36-gui-automation-state-of-the-art-context-for-the-deferred-gui-leg) | not stated | not stated |
| OpenAI CUA / Operator | [§3.6](#36-gui-automation-state-of-the-art-context-for-the-deferred-gui-leg) | not stated | not stated |
| UI-TARS-2 | [§3.6](#36-gui-automation-state-of-the-art-context-for-the-deferred-gui-leg) | not stated | not stated |
| Agent S3 | [§3.6](#36-gui-automation-state-of-the-art-context-for-the-deferred-gui-leg) | not stated | not stated |
| OmniParser v2 | [§3.6](#36-gui-automation-state-of-the-art-context-for-the-deferred-gui-leg) | not stated | not stated |
| Free alternatives to Revit for an agent BIM track (IfcOpenShell, ifc-lite, others) | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-26 | not stated |
| Constor | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-11-14 | adjacent (low) |
| ArchLang | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-11-15 | adjacent (low) |
| IfcOpenShell 0.9.0 + trimesh | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| ifcopenshell.validate, IfcClash, IfcTester | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| ifcopenshell.util.shape (quantity takeoff) | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| Licences: ifcopenshell, ifcclash, ifctester, bcf-client | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| trimesh | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| IDS 1.0 (buildingSMART) | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| buildingSMART Validation Service | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| Autodesk/revit-ifc | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| APS Model Derivative (.rvt to IFC) | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| web-ifc-three | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| APS pricing | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| CODE-ACCORD | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-10-06 (section heading) | not stated |
| AutoCAD and Revit logs as evidence (§3.7.2) | [§3.7](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate) | 2026-11-15 (researched) | adjacent (low) |
| Agent-CAD videos on YouTube | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| YouTube Data API (captions) | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| youtube-transcript-api | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| Supadata and SearchAPI.io | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| media.ccc.de | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| Thingi10K | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| Thingiverse | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| Printables | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| Fusion 360 Gallery | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (section heading) | not stated |
| QuickTube | [§3.8](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22) | 2026-11-22 (tried) | not stated |

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

Moved 2026-11-24 to [`landscape-adjacent.md`](landscape-adjacent.md#32-adjacent-projects).

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

Moved 2026-11-24 to [`landscape-bim.md`](landscape-bim.md#37-bim--three-regimes-ifc-adopted-behind-a-data-gate).

### 3.8 Videos, transcripts and model repositories — researched 2026-11-22

Moved 2026-11-24 to [`landscape-videos.md`](landscape-videos.md#38-videos-transcripts-and-model-repositories--researched-2026-11-22).

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
[cadagent]: https://github.com/Svetlana-DAO-LLC/cad-agent
[openscadagent]: https://github.com/iancanderson/openscad-agent
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
[sketch2bim]: https://arxiv.org/abs/2510.20838
[text2bim]: https://arxiv.org/html/2408.08054v1
[qwenbim]: https://arxiv.org/abs/2602.20812
[mcp4ifc]: https://arxiv.org/abs/2511.05533
[bimscript]: https://arxiv.org/html/2608.21447
[bimedit]: https://arxiv.org/abs/2606.20146
[autoaero]: https://arxiv.org/pdf/2605.27968
[steenkencase]: https://engineer-your-idea.com/en/blog/agentic-cad-room-booking-sign/
[steenkenrun1]: https://engineer-your-idea.com/en/blog/agentic-cad-pi4-housing/
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
[agenticmfg]: https://arxiv.org/abs/2604.09633

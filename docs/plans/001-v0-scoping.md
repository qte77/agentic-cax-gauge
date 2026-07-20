---
title: agentic-cax-gauge v0 scoping plan
purpose: Full scoping decision, architecture, and context map for v0 — written so a fresh session can execute without re-researching
created: 2026-07-20
updated: 2026-07-20
validated_links: 2026-07-20
status: approved
---

**Status**: Approved, not yet implemented. Only this plan and its handoff exist.

## 1. Context

**Problem.** Coding agents write code well and reason about 3D space badly. This is
structural, not a prompting deficiency — see the evidence in the Source Map (§6.1).
An agent asked to design a part cannot be trusted to look at a render and judge whether
it is right.

**Insight.** Stop asking the model to *see*; make the geometry *assert itself*. Generate
parametric code, verify deterministically, and use rendered-image critique only as a
bounded secondary pass. This ordering is what the literature supports (§6.2).

**Estate position.** Two sibling repos independently built half this machinery and both
explicitly defer the loop itself. `so101-biolab-automation/docs/roadmap.md:47-58`
documents this exact loop as unbuilt future work and `:158-169` states no known project
closes the full loop.

**Outcome.** A standalone, domain-agnostic harness that makes CAx generation test-first.
`so101-biolab-automation` and `i3mega-pipettebot` become its first two consumers.

## 2. Locked decisions

| Decision | Value | Rationale |
|---|---|---|
| Repo | `agentic-cax-gauge`, package `caxgauge` | *gauge* = conformance-verification instrument; *CAx* = CAD/CAE/CAM umbrella so CAE needs no rename; *agentic* covers LLM+VLM |
| Relationship to estate | New standalone repo; so101 + i3mega are consumers | A general verification harness is a different concern from a bio-lab robot |
| v0 scope | CAD + deterministic verification + bounded VLM critique | User-selected |
| CAE | Documented only, not built | User-selected; research still owed (§7.1) |
| GUI leg | Minimal experimental fallback, included | User-selected; weakest leg (§7.3) |
| Testing | Strict TDD, behavior-level, no Gherkin/BDD | Estate standard; legacy `RAPID-spec-forge` BDD guidance explicitly rejected |
| Python | 3.12 exactly | Hard constraint: `build123d -> cadquery-ocp -> VTK` has no cp313 wheels |

## 3. The wedge

Comparable projects do `prompt -> CAD -> eyeball the render`. The missing primitive is a
**declarative, machine-checkable acceptance spec that exists before generation**, making
red-green-refactor possible on geometry.

`DesignSpec` declares checkable intent: envelope, named feature dimensions + tolerances,
required clearances between mating parts, mass/volume bounds, material, manufacturability
constraints. The verifier turns each into a pass/fail assertion. The agent iterates until
green, not until it looks right.

**Unvalidated.** This wedge has not been red-teamed against the incumbents in §6.4. Do
this before P1 (§7.2).

## 4. Architecture

```text
DesignSpec (YAML)  ->  Generate (agent writes parametric code)
                            |
                            v
                    Backend dispatch (build123d | OpenSCAD | stub)
                            |
                            v
              Deterministic verify  <-- load-bearing, gates everything
              (build ok, manifold, bbox/volume, clearance, printability)
                            |
                      green |  red -> feed failures back, regenerate
                            v
              Bounded VLM critique (multi-view renders, max 3, revert-on-break)
                            |
                            v
                   Escalate to human past the cap
```

Layer order is deliberate. Deterministic checks run first and are **authoritative**. The
VLM never overrides a deterministic failure; it only catches wrongness the assertions did
not encode (proportion, orientation, obvious nonsense).

## 5. Code map — what to build

Nothing below exists yet. All paths relative to repo root.

| Path | Responsibility | Phase |
|---|---|---|
| `src/caxgauge/spec.py` | `DesignSpec` pydantic-settings model, `from_yaml`. The acceptance contract. | P1 |
| `src/caxgauge/verify/geometry.py` | Manifold/watertight, bbox, volume, clearance/interference asserts. **Load-bearing.** | P1 |
| `src/caxgauge/backends/__init__.py` | `Backend` Protocol, auto-detection, stub fallback | P2 |
| `src/caxgauge/backends/build123d.py` | Primary backend | P2 |
| `src/caxgauge/backends/openscad.py` | Fallback backend | P2 |
| `src/caxgauge/loop.py` | Orchestrator: generate -> verify -> critique -> escalate | P3 |
| `src/caxgauge/generate.py` | Spec -> prompt; sandboxed execution of returned code | P3 |
| `src/caxgauge/verify/slicer.py` | Printability gate, CLI wrap, PASS/WARN/FAIL/SKIP | P4 |
| `src/caxgauge/verify/render.py` | Multi-view turntable PNGs for critique | P5 |
| `src/caxgauge/critique/vlm.py` | Thin adapter over `vlm-toolkit`; cap 3, revert-on-break | P5 |
| `src/caxgauge/verify/sim.py` | CAE acceptance asserts — **seam only, empty in v0** | deferred |
| `src/caxgauge/gui/` | Experimental sandboxed computer-use fallback; must not gate CI | P6 |
| `tests/` | Mirrors `src/` 1:1 | all |
| `configs/` | Example `DesignSpec` files | P1 |

**Why `verify/sim.py` is reserved now:** a CAE acceptance check ("peak stress under
yield") is structurally identical to a geometry check ("bbox under 80mm") — a bound on a
measured scalar. Reserving the seam costs nothing and stops CAE being bolted on sideways.

## 6. Source map

### 6.1 Why VLM spatial judgment cannot be trusted

| Finding | Evidence | ID |
|---|---|---|
| VLMs fail elementary geometry | 58% on overlapping shapes; failure is in the language decoder, not vision encoder | [arXiv:2407.06581][blind] |
| Near-chance on visual perception | Humans 95.7% vs best VLM (GPT-4V) 51.3% across 14 CV tasks | [arXiv:2404.12390][blink] |
| Generic CoT does not help | Standard CoT/self-consistency/ToT fail on spatial; explicit cognitive maps do help | [arXiv:2412.14171][vsi] |
| Root cause is data, not architecture | 2B synthetic 3D-VQA examples beat GPT-4V on distance/size | [arXiv:2401.12168][spatialvlm] |
| Tokenization mismatch | Continuous 3D geometry tokenized sequentially — prohibitive token counts or lossy encodings | [arXiv:2504.05786][tokensurvey] |
| No mental rotation ability | VLMs lack analog imagery-based rotation entirely, unlike humans | [Hyperphantasia][hyper] |

### 6.2 Mitigations that work — and what we adopt

| Technique | Result | Adopted? |
|---|---|---|
| Render + VLM verify loop | CADCodeVerify +7.3% geometric accuracy; CADPrompt benchmark | Yes, as **bounded secondary** — [arXiv:2410.05340][cadcodeverify] |
| Visual self-refinement | Query2CAD 53.6% -> 76.7% success, training-free | Yes — [arXiv:2406.00144][query2cad] |
| Revert-on-break guard | 3DCodeBench restores last-good state if a fix breaks executability | Yes, directly — [arXiv:2606.01057][3dcodebench] |
| Iteration cap | Quality plateaus/degrades after ~3 iterations without human-in-loop | Yes, cap = 3 — [Planner-Actor-Critic][pac] |
| Solver-grounded validation | LLM proposes, parametric constraint solver verifies geometric validity | Yes — this is the core thesis — [arXiv:2606.31252][embodiedcad] |
| Constraint-status post-training | Autodesk scores sketch constraint status to fix under-constrained output | Assess later — [Autodesk][autodesk] |
| Retrieval of parametric templates | Seek-CAD retrieves from 10K-model corpus as in-context examples | Assess later — [arXiv:2505.17702][seekcad] |
| Correction accuracy | CADReview/ReCAD 73% vs 41.5% raw GPT-4o | Reference — [arXiv:2505.22304][cadreview] |
| Simulation in the loop | Physics-in-the-Loop embeds FEA in Generate-Simulate-Refine | Defer to CAE leg — [arXiv:2605.19717][physicsloop] |

### 6.3 Backend decision

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

### 6.4 Competitive landscape — the wedge must survive these

| Project | What it does | Threat level |
|---|---|---|
| [Zoo / KittyCAD][zoo] | Text-to-CAD to parametric B-rep, own KCL geometry engine, Design Studio OSS. Most mature commercial. Publicly discloses **no** formal render/solver/simulation verification loop — thumbs-up/down only | High on capability, low on our specific wedge |
| [AdamCAD][adam] | YC W25, OSS CADAM (WASM/OpenSCAD backend), $4.1M seed | Medium |
| [Backflip AI][backflip] | Scan-to-parametric-CAD, $30M raised, ex-Markforged | Medium, adjacent problem |
| [CAD-Assistant][cadassistant] | Tool-augmented VLLM driving FreeCAD Python API | High conceptual overlap |
| [cad-agent][cadagent] | build123d + MCP, VTK-rendered PNG self-correction | **Highest overlap** — closest existing thing |
| [openscad-agent][openscadagent] | Claude-Code-powered generate/render/self-correct + STL manifold validation | **Highest overlap** |
| [BlenderLLM][blenderllm] | Fine-tuned Qwen2.5-Coder-7B + CADBench | Low |
| [ScadLM][scadlm] | Hackathon agentic text-to-OpenSCAD; authors report feedback approaches underperformed | Low, but a cautionary data point |
| [MecAgent][mecagent] | NL to CAD macros for SolidWorks/CATIA/Fusion — API/macro, not vision | Medium |

**Honest read:** `cad-agent` and `openscad-agent` already do generate-render-self-correct.
The claimed differentiator is the *pre-declared machine-checkable spec* and deterministic
gate ordering, not the loop itself. Verify this holds (§7.2).

#### 6.4.1 `earthtojake/text-to-cad` — the real incumbent

Analysed 2026-07-20. **This is the closest existing project and the initial research sweep
missed it.** Treat it as the primary competitive reference.

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

**What it does not have — the surviving gap:**

| Our claim | Status in text-to-cad |
|---|---|
| Pre-declared machine-checkable `DesignSpec` | **Absent.** The "CAD brief" is unstructured prose written by the *same agent* immediately before coding. No schema, no clearance/mass/volume/manufacturability fields, no independence between spec-author and generator |
| Deterministic gate authoritative over VLM | **Absent as a formal gate.** Snapshot review is "review the output" by the calling agent. No cap, no revert-on-break, no veto ordering |
| Manifold/watertight check | **Absent in code.** "Watertight" appears only as ungraded checklist prose in `benchmarks/*.md` — there is no grading script in `benchmarks/` |
| Volume/mass bounds | Absent |
| Interference/collision between bodies | Absent |
| Slicer printability as blocking gate | Only an isolated manual `--dry-run` in a separate `gcode` skill, explicitly "diagnostic only", not wired to CAD generation |

**External corroboration of the gap:** an HN commenter reported generated parts where
"gussets overlap the holes and make a part that cannot be used" and questioned whether
through-holes actually pass through — precisely the interference class no current check
catches. Author's reply: *"Working on benchmarks at the moment!"* ([HN][hn]).

**Strategic read.** The wedge survives, but narrowly and on a shot clock. Verification is
this project's weakest area, it is self-acknowledged as unfinished, and it is the most
plausible next thing they ship. Two implications:

1. Do not assume the gap stays open. If P1 is not built soon, it may be closed by the
   incumbent.
2. **Complement-vs-compete is now an open strategic question** (§11.6). Their form factor
   is an agent skill on build123d; ours is a verification harness on build123d. A gate that
   plugs into their pipeline may be higher leverage than a rival end-to-end harness.

**Adopt from it:**

- `selector_manifest_diff` — cheap deterministic regression check for unintended topology
  change between edit iterations. Directly reusable.
- `assert_close` / `assert_bbox_coordinate` / `assert_bbox_span` — clean tolerance-assertion
  shape to mirror in `verify/geometry.py`.
- "Edit source, never exported artifacts" — single-source-of-truth discipline.
- Catalog-check-before-generate (`step.parts`) — maps to a manufacturability field in
  `DesignSpec`; do not model what you can buy.
- Their `benchmarks/*.md` format (prose prompt + explicit test-case checklist with dims,
  counts, "exactly one watertight solid", "imports successfully") is a good template for
  authoring `DesignSpec` files — and the fact that it is **ungraded by code** is exactly
  the gap to fill.
- The HN failure modes (hole/gusset overlap, unverified through-holes) are concrete target
  cases for the interference and clearance checks.

### 6.5 CAD MCP servers

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

### 6.6 GUI automation state of the art (for P6)

| System | Benchmark | ID |
|---|---|---|
| Claude computer use | OSWorld ~82.3% reported for Opus 4.7; vendor recommends sandboxed VM | [docs][ccu] |
| OpenAI CUA / Operator | 38.1% OSWorld at launch; folded into ChatGPT agent Aug 2025 | [openai][cua] |
| UI-TARS-2 | 47.5% OSWorld, 88.2% Online-Mind2Web; screenshot-only | [arXiv:2509.02544][uitars2] |
| Agent S3 | 66% OSWorld, 72.6% with Behavior Best-of-N | [github][agents] |
| OmniParser v2 | 39.5% ScreenSpot Pro grounding; pure-vision, no DOM | [github][omniparser] |

**Gap confirmed:** no mature publicly documented screenshot-vision agent drives FreeCAD,
Fusion or SolidWorks GUIs. Commercial CAD AI uses native API/macro hooks. This is the open
niche P6 targets — and the reason it is high-risk.

## 7. File map — estate reuse

Exact paths verified this session. Do not re-search for these.

| Need | Source | Detail |
|---|---|---|
| Manifest-driven dual-backend build dispatch | `../so101-biolab-automation/src/hardware/render.py:1-237` + `src/hardware/parts.json` (20 parts); second instance `../i3mega-pipettebot/tools/cad/render.py:99-133` + `tools/cad/parts.json` | Declarative `{script, build_func, outputs, status}` registry, dynamic import, cache by `(script, func)`, exports STL+STEP+SVG. Two independent implementations to generalize from. |
| Slicer-as-gate validator | `../so101-biolab-automation/src/hardware/slicer/validate.py:1-275`; `../i3mega-pipettebot/tools/slicer/validate.py:77-132` | CLI wrap of CuraEngine/PrusaSlicer/OrcaSlicer, stdout keyword scrape (`overhang`/`bridge`/`support`/`empty layer`), dependency-free binary-STL integrity check via `struct`. `SKIP` when tool absent is first-class — keeps CI green. |
| Stub-mode-by-default driver | `../so101-biolab-automation/src/so101/arms.py:70-73,152-158,173-178` | Try real import, fall back to in-memory stub, log every command that would have been sent. **Directly load-bearing** — lets CI exercise full control flow with no CAD tooling installed. |
| `send` vs `query` split | `../i3mega-pipettebot/src/pipettebot/gantry.py:160-179` | For line-oriented tool REPLs where some commands need an ack and others structured output. Applies to driving a CAD tool console. |
| Probe/classify/never-mutate recon | `../i3mega-pipettebot/tools/gantry_probe.py:46-58,145-172` | Safely enumerate an unfamiliar CLI's supported commands (SUPPORTED/UNSUPPORTED/PARTIAL/SILENT) with a hard refuse-list before scripting real actions. |
| Coordinate-frame discipline | `../i3mega-pipettebot/.claude/rules/cad-script-conventions.md`, `AGENT_LEARNINGS.md:7-18`, worked example `tools/cad/labware/deck_plate.py:206-224` | CAD-frame vs machine-frame `+Y` mismatch bit them once and was promoted to an enforced rule. Adopt from day one. |
| Policy-dispatch over class hierarchy | `../i3mega-pipettebot/docs/adr/0004-*.md:88-96` | ADR with rejected-alternatives table: `discover() -> classify() -> Policy (data) -> single dispatcher function`. Template for driving heterogeneous CAD/CAE tools without polymorphism sprawl. |
| STEP round-trip escape hatch | `../so101-biolab-automation/docs/hardware/cad-tooling.md:125-145` | `build123d -> STEP -> FreeCAD GUI edit -> STEP -> slicer`; hand-edited STEP becomes new leaf source of truth. |
| Config-over-code | Pydantic `BaseSettings.from_yaml()` throughout both repos | Keeps agent-generated parameters auditable/version-controlled, not baked into generated code. |
| Governance scaffold | `AGENTS.md` + `.claude/rules/` + `AGENT_LEARNINGS.md` + `AGENT_REQUESTS.md` + compound-learning promotion path | Estate standard. Copy structure, not content. |
| **VLM critique backend** | **`../vlm-toolkit`** | Local GGUF VLM + YOLO26 detector, in-process (`llama-cpp-python`) or HTTP (`llama-server`), Python `>=3.11,<3.13`, Apache-2.0. Already names so101 + i3mega as planned consumers. **P5 consumes this — do not build a second VLM integration.** Pre-`v0.1.0`, API unstable: pin it, keep the adapter thin. See its `docs/architecture.md`, `docs/consumers.md`. |

### Research-hub relationship — `../ai-agents-research`

Verified by direct read, not by subagent sweep. That repo is a catalog for making
**adopt / defer / skip** decisions about *AI coding agents and their ecosystems* —
Claude Code internals, sandboxing, orchestration, plugins, MCP connectors, SDLC patterns.
It is **not** a domain-knowledge hub.

Consequence for this repo:

- **CAD/CAE domain research does not belong there.** The landscape in §6 lives here.
- **Harness-level findings do belong there** — e.g. what we learn about bounded
  self-critique loops, sandboxed code execution, or subagent reliability. Contribute via
  its `adding-research-source` skill; the estate also has a `research-cross-check` skill
  for bidirectional sync.
- Its doc conventions are the estate standard and are what §1 frontmatter here follows:
  frontmatter with `validated_links`, a Technology-Radar status badge
  (Adopt/Trial/Assess/Hold), reference-style links (no bare URLs in prose), and a
  mandatory `## Sources` table. See `../ai-agents-research/CONTRIBUTING.md`.
- Its `docs/research/rxiv-agentic-papers.md` is an auto-generated cumulative arXiv index —
  a possible feed for keeping §6.1/§6.2 current, but note `triage/` is machine-generated
  and explicitly **not** a content source.
- Relevant standing rule there: *"Verify subagent findings before acting"* — its
  `AGENT_LEARNINGS.md` records repeated false negatives from subagent sweeps. This session
  reproduced that failure mode (one agent returned off-task meta-text that superficially
  looked like a result). Apply the same skepticism here.

### Ruled out — do not re-investigate

| Repo | Why not |
|---|---|
| `RAPID-spec-forge` | Archived 2026-04-26, superseded by `qte77/qte77`. Its spec methodology is *business requirements* (BRD -> PRD -> FRP), a different artifact from a geometric `DesignSpec`. Its BDD guidance is legacy and rejected. |
| `VisAgent-Proto` | v0.0.0 DRAFT/WIP wrapper around landing.ai Vision Agents. Not a critique-leg candidate. |
| `CellPlateVision-Prototype` | Petri-dish cell-confluence detection with ELN export. Vision, but wrong domain. |

## 8. Tech stack

- Python 3.12 exactly (see §2 constraint; verified `so101 pyproject.toml:8`,
  `i3mega pyproject.toml:12`).
- `uv`; Pydantic v2 + pydantic-settings; pytest + Hypothesis; ruff (incl. `S`, `ANN`, `D`);
  mypy or pyright strict; complexipy; scriv fragments; lychee + markdownlint.
- Tests mirror `src/` 1:1. Tool-dependent tests marker-gated, excluded by default.
- Skip trivial tests on declarative models — test modules with real logic.

## 9. Phased delivery

Each phase independently shippable.

- **P0a — DONE (this session).** Wire `origin`, write this plan + handoff.
- **P0b — Scaffold.** Governance files, `.claude/rules/`, `Makefile`, CI, quality gates,
  `pyproject.toml`. No product code.
- **P1 — Spec + deterministic verifier.** `spec.py`, `verify/geometry.py`, test-first.
  Fed by fixture STLs, no agent involved. **Build this before anything agentic.**
- **P2 — Backend dispatch.** Generalize the two existing dispatchers; do not write a third.
- **P3 — Loop orchestrator + generation.** Sandboxed execution; failures feed back as
  structured text.
- **P4 — Manufacturability gate.** Port `verify/slicer.py` from the two validators.
- **P5 — Bounded VLM critique.** `verify/render.py` + `critique/vlm.py` over `vlm-toolkit`.
- **P6 — GUI fallback (experimental).** One tool, sandboxed, non-gating, cuttable.
- **P7 — Adoption.** Consumer PRs in so101 + i3mega; rewrite so101 roadmap to point here.

## 10. Verification strategy

- **P1/P2 property tests.** Hypothesis over spec dimensions: a spec generating a box of
  size X must pass its own bbox assertion and fail a deliberately perturbed one. Fixture
  STLs with known-bad topology must fail the manifold check.
- **Stub-mode CI (primary gate).** Full loop runs end-to-end with no build123d, no
  OpenSCAD, no slicer installed; asserts the command log matches expected sequence.
- **Golden-path integration (marker-gated).** One real part, real build123d, real slicer.
- **Loop honesty test.** Feed a spec the agent cannot satisfy; assert the loop terminates
  at the cap and escalates rather than declaring success. **Guards the failure mode that
  matters most.**
- **Real acceptance test.** Harness reproduces an existing part from
  `so101/src/hardware/parts.json` or `i3mega/tools/cad/parts.json` and passes its spec.

## 11. Open questions and risks

1. **CAE leg unresearched — BLOCKING for `outlook-cae.md` only.** The CAE/simulation
   research sweep failed twice (once off-task, once on a weekly rate limit resetting
   2026-07-22 21:00 UTC). Must not be written from memory. Re-run before P7. P1-P6
   unaffected. Topics owed: OpenFOAM/CalculiX/code_aster/FEniCS/Elmer/SU2/Gmsh/PyMAPDL
   scriptability; MetaOpenFOAM / OpenFOAMGPT / FoamGPT and LLM-FEA papers; simulation
   MCP servers; topology optimization + DoE loops; guardrails for units/BCs/convergence.
2. **Wedge not validated.** Run `adversarial-distillation` on "TDD for CAD" before P1.
   `cad-agent` and `openscad-agent` (§6.4) already do generate-render-self-correct. Cheap
   to falsify now, expensive after P3.
3. **P6 is the weakest leg.** No vendor claims unattended reliability; 47-82% OSWorld.
   Sandboxed, non-gating, cuttable.
4. **AHA check.** The CAD-build/slicer pattern appears twice. Generalizing it *inside*
   this repo is fine; extracting a separate shared package consumed by all three is
   deliberately **not** in scope until the pattern proves stable here.
5. **"agentic" is a crowded prefix.** Accepted knowingly.
6. **Complement vs compete — OPEN, decide before P0b.** `earthtojake/text-to-cad` (§6.4.1)
   is at 8.6k stars on the same build123d backend, with verification as its weakest and
   self-acknowledged-unfinished area. Options: (a) standalone rival harness as this plan
   currently assumes; (b) position as the verification layer that plugs into their skill
   pipeline; (c) contribute the gate upstream to them. Option (b)/(c) may be far higher
   leverage than (a) and would change P3/P6 scope substantially. Human decision required.
7. **Research sweep was incomplete.** The initial landscape pass missed an 8.6k-star
   direct competitor. Treat §6.4 as provisional and re-sweep before committing to
   positioning — in particular search agent-skill/plugin marketplaces, not just arXiv and
   MCP registries.

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
| [arXiv:2606.01057][3dcodebench] | 3DCodeBench — revert-on-break guard |
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
| [earthtojake/text-to-cad][texttocad] | **Primary incumbent** — 8.6k-star build123d agent-skill package; verification is its weakest area |
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

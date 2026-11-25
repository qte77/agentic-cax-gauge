---
title: Landscape — adjacent projects (§3.2)
purpose: Section 3.2 of landscape.md, split out of it on 2026-11-24 so the hub stays navigable
created: 2026-11-24
updated: 2026-11-25
validated_links: 2026-11-15
status: reference — dated, not needed to build
---

Back to the hub: [`landscape.md`](landscape.md).

<!-- markdownlint-disable-next-line MD001 -->
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
own checks this way was not checked. *Later the same day:* matchline (§3.2) blocks a publish
on a check it could not run, the same idea as `SKIP`, never `PASS`, built independently. What is
left unmatched is labelling passing checks necessary, not sufficient.

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

**Added 2026-11-25 (owner lead) — a LinkedIn post arguing that the file format decides whether
an LLM can work in an ECAD tool.** [The post][aklivanh] (Eyal Aklivanh, 2026-11-24) was read at
source on 2026-11-25, and each of its claims was then checked against the vendors' own pages.
Its argument: what decides an ECAD tool's future is whether an LLM can work on its design
files. KiCad's files are plain text, so an LLM can read, edit and review them like code.
Altium's are closed binaries, with no LLM integration in schematic or layout. The author
reports getting layout-ready schematics fast with almost no KiCad experience, for simple
designs, and predicts that Altium will become irrelevant. **What the vendors' own pages say:**

- KiCad's developer docs say that schematics, boards and libraries use an s-expression text
  format ([KiCad file-format docs][kicadsexpr]). The plain-text part of the claim holds; how
  well an LLM edits or reviews these files is not checked.
- Altium's docs recommend saving in "SCH Binary Version 5.0" and "PCB Binary Version 6.0"
  ([Altium saving docs][altiumsave]), so the recommended save formats are binary. We did not
  read what the other options are, and whether the formats are "closed" is not checked.
- Altium does ship AI agents, in its Altium 365 Requirements Portal ([Altium docs, updated
  2026-11-20][altiumagentic]). We found no such feature for schematic or layout on the Altium
  Designer product page or the Altium 365 what's-new page, but two pages do not prove there
  is none. That claim is only partly
  checked.
- The speed report can't be checked, and the prediction is the author's opinion. Both are
  recorded as the post's claims, not ours.

**Our reading:** this supports KiCad as the ECAD an agent can work with, which we had already
concluded from its CLI: [`kicad-cli`][kicadcli] runs `sch erc` and `pcb drc` and reports
through exit codes. The post names no check. Reviewing files "like code" is not ERC or DRC, and
a file an LLM can edit tells us nothing about whether the design is correct. It changes nothing
for this project: the PCB track is "Not started: no trigger yet", and a post is not a trigger,
because the owner decides. Rank: adjacent (low).

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

**Added 2026-11-23, later the same day (owner leads) — matchline and Solvaix.**

**[matchline][matchline]** (Rank: adjacent (low) as a tool, but it changes a positioning claim,
see below; BSD-3-Clause, Python, 2★ on 2026-11-23, read at `develop` commit `6a76993`). It
extracts building-energy-model geometry and quantity takeoffs from architectural drawings and
BIM, and exports gbXML and IFC4. What its [export gate][mlgate] does:

- six geometric checks on the staged export (shell closure, winding, signed volume,
  planarity, degenerate faces, duplicate surfaces), plus gbXML schema and IFC4 structural
  validation;
- a shell the exporter can't represent is reported `not_checked` with its reason, never as a
  pass, and at publish a `not_checked` result blocks the export just as a failure does;
- the gate only measures; it never repairs.

Issue [#1406][ml1406] took a loop shape from a Solvaix post (below) and narrowed it before
building anything: repair only defects with one correct fix (a shell wound inside out, a
duplicate surface, an overlapping opening whose position the drawings don't state), no model
in the repair path, and positions stated in the drawings never move. It measured first: on its
own output those defects were nearly absent (one natural case in 89 exports). The first scope
failed its own cost bar and a narrower one passed. [`bem/repair_loop.py`][mlrepair] now ships
it: at most two iterations, a repair that doesn't make its check pass is reverted, every repair
is logged in the export manifest, and the full gate still decides what is published. It is off
by default in the library and, per its docstring, on at the export commands since an owner
decision on 2026-11-17. Degenerate faces were excluded because dropping one broke shell
closure or deleted real area.

Our reading:

- `not_checked` is the same idea as this gauge's `SKIP`, never `PASS`, built independently
  and in code, and stricter: it blocks the publish, where our `SKIP` is reported and kept out
  of green. So `SKIP` is no longer something only this gauge does (plan §12 item 7).
- The excluded degenerate-face repair is plan §3.1's "deletion beats repair" path, found by
  measurement. This gauge stays measure-only: plan §3 rejects a revert-on-break loop, and
  CONTRIBUTING keeps repair out of every check path.
- IFC4 structural validation inside an export gate is prior art for row MB (plan §13), if a
  real IFC model ever lands.

**Effect on the plan:** the positioning note in §12 item 7 is updated; no decision changes.

**Solvaix** (Rank: adjacent (low)). An X account whose bio reads "Testing how far AI can go in
CAD, BIM and 3D", with about 4.5k followers on 2026-11-23. No website, company or repository
was found. The profile itself was not read at source; one post was, through a public mirror.
That post (status `2122759994672120184`, 2026-11-17) says Claude Opus 5.5 routed the
mechanical, electrical and plumbing systems of a 1,792 sq ft house drawn for the test, and
describes it as a simulation without load calculations or duct sizing. It claims:

- a first pass with 26 clashes, all rerouted;
- 8 of the model's own code mistakes caught in a review pass;
- a check against the 2021 IRC, IPC and IFGC and the 2023 NEC, with every item passing.

The post's evidence is a 28-second video. It links no model file, clash export or checking
method, so every count is the account's own. A post it quotes (2026-08-01) says Revit
2027's MCP server is read-only. That was not checked against Autodesk's documentation, and it
would conflict with the "element ops" tool group reported in §3.5.

Our reading: as the post describes it, the review pass is the same model checking its own
work, which plan §3.1 calls
correlated failure, not independent verification. "Every item passing" is a green result read
as sufficient. **Effect on the plan:** none.

[cadassistant]: https://arxiv.org/abs/2412.13810
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
[cadfusion]: https://github.com/microsoft/CADFusion
[cadjudge]: https://arxiv.org/abs/2508.04002
[autobrep]: https://arxiv.org/abs/2512.03018
[cadllama]: https://arxiv.org/abs/2505.04481
[openecad]: https://arxiv.org/pdf/2406.09913
[geocad]: https://arxiv.org/pdf/2506.10337
[cadmium]: https://arxiv.org/abs/2507.09792
[leap71]: https://github.com/leap71
[picogklegacy]: https://github.com/leap71/PicoGK.Legacy
[picogkcore]: https://github.com/leap71/PicoGK.Core
[picogk118]: https://github.com/leap71/PicoGK/discussions/118
[noyron]: https://leap71.com/noyron/
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
[soma]: https://somacad.app/
[somagh]: https://github.com/Kai-Jungsthoefel/SOMA
[somaagents]: https://raw.githubusercontent.com/Kai-Jungsthoefel/SOMA/cf8e629ef0dc1c2c54ee3fb62d50a208aa938c27/app/resources/template/AGENTS.md
[somaanalysis]: https://raw.githubusercontent.com/Kai-Jungsthoefel/SOMA/cf8e629ef0dc1c2c54ee3fb62d50a208aa938c27/app/resources/skills/analysis.md
[agenticmfg]: https://arxiv.org/abs/2604.09633
[matchline]: https://github.com/anchapin/matchline
[ml1406]: https://github.com/anchapin/matchline/issues/1406
[mlgate]: https://raw.githubusercontent.com/anchapin/matchline/6a76993f39c533c8c92fc7fcbeba4e5d1f138f21/bem/export_gate.py
[mlrepair]: https://raw.githubusercontent.com/anchapin/matchline/6a76993f39c533c8c92fc7fcbeba4e5d1f138f21/bem/repair_loop.py
[aklivanh]: https://www.linkedin.com/posts/aklivanh_im-sorry-to-say-it-but-i-think-altium-is-activity-7531101254761103360-bhWM
[kicadsexpr]: https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html
[altiumsave]: https://www.altium.com/documentation/altium-designer/saving-projects-documents
[altiumagentic]: https://www.altium.com/documentation/altium-365/requirements-portal/agentic-requirements-engineering

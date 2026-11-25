---
title: Landscape — BIM (§3.7)
purpose: Section 3.7 of landscape.md, split out of it on 2026-11-24 so the hub stays navigable
created: 2026-11-24
updated: 2026-11-25
validated_links: 2026-11-15
status: reference — dated, not needed to build
---

Back to the hub: [`landscape.md`](landscape.md).

<!-- markdownlint-disable-next-line MD001 -->
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
[openecad]: https://arxiv.org/pdf/2406.09913
[geocad]: https://arxiv.org/pdf/2506.10337
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
[ifcmcp]: https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.9.0/src/ifcmcp
[ifcedit]: https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.9.0/src/ifcedit
[ifclite]: https://github.com/LTplus-AG/ifc-lite
[bricsshape]: https://www.bricsys.com/news/bricscad-shape-discontinued

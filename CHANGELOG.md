# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/), [Semantic Versioning](https://semver.org/).

<!-- scriv-insert-here -->

## [Unreleased]

### Added

- **`make release_smoke`**, run before a minor or major tag: loads `site/index.html` and a
  `--source` report on seven presets (desktop 1280×800; iPhone 13, Pixel 7 and iPad Mini, each
  portrait and landscape) through polyfetch's Chromium (`scripts/release_smoke.py`). It
  reports a page that didn't load, browser console errors and failed requests, horizontal
  overflow, an image that didn't load or a report without its four views, a standalone touch
  target under 44×44 CSS px on a touch preset (WCAG 2.2 SC 2.5.5; links inside text are
  exempt, as that criterion's Inline exception says) and a missing screenshot. Screenshots
  go to `reports/release-smoke/` for a human; no model judges. Exit 2 when polyfetch is
  absent, so an unrun check never reads as green. Blind spot: Patchright disables the
  Console API, so a page script's own `console.error` is not seen. The device-list matrix
  and the touch-target check are ideas from
  [mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers), written here
  in our own words; its LLM verdicts are not adopted.
- **Sample-site tap targets:** the index's part and run links were 20 px tall (run links
  9×20 px) on phones; they are now at least 44×44 CSS px.
- **Known-bad benchmark controls** (owner 2026-11-22), modelled on failures in agent-CAD
  videos (landscape §3.8). Each expected result comes from the brief's closed form:
  - brief 10 with half its holes fails the volume band
  - brief 16's 80 mm bracket handed in for brief 17's 100 mm one fails the volume band
  - bim-02's wall with its door opening dropped fails the volume band
  - brief 03 with no holes passes preflight (the holes are inside the ±2 % band), so it is
    asserted as a blind spot the render covers
  Two build123d-made STL fixtures (`wall_bracket_80.stl`, `hole_grid_half_density.stl`);
  the bracket is also a fourth known-good part, for brief 16.
- **Benchmark briefs 16–18** from The Stack Underflow's Apache-2.0 labs, rewritten in our own
  words and credited in each brief with a commit-pinned link:
  - 16 and 17: an L-shaped wall bracket at 80 mm and 100 mm wide, with the holes centred.
    This is a "change one number" pair.
  - 18: a cable clip for a 6 mm cable, whose closed form needs a circular segment.
  The band test's evaluator now also allows `asin(x)`, and nothing else. The clip's formula
  gives 2095.3 mm³, matching the lab's FreeCAD measurement of 2095.31 mm³.
- **M3 sheet pre-staged for the owner's sitting:** `bench/m3-review.csv` gains a `found_by`
  column (`preflight`, `render` or `source`, per defect) and is ordered by source file.
  `bench/rubric.md` adds a default decision rule, set before the sitting: if `source` found
  more defects than `render`, the render-first claim is reopened before any new view is
  built.
- **`bench/provenance.py`** also records build123d's OCCT binding (OCP) version, and says that
  versions come from the same unpinned `uv` resolution as the run.
- **Per-run provenance (`bench/provenance.py`, BENCH-3 item 5)**: `bench/run.sh` writes each
  run's `provenance.json`: the harness commit and whether the tree was dirty, the brief's
  SHA-256, the tool version and the Claude Code version. The `runs.tsv` columns are unchanged.
  The 30 pilot runs predate it.
- **Band-recompute test (`tests/test_bench_bands.py`, BENCH-3 item 1)**: each bounded brief
  now declares its exact `volume:` as an arithmetic expression in the hidden front matter. The
  test evaluates it (numbers, operators and `pi` only), checks that the `Bounds:` prose states
  the same number, that the band contains it, and that the band edges match the stated
  tolerance where the brief states it exactly.
- **Review rubric (`bench/rubric.md`)**: one fixed rubric for the benchmark labels and the M3
  defect table, to be fixed before anyone labels. The verdict is `yes`, `no` or `unsure`
  (when the views can't settle it). Reason codes: `phantom-feature`, `mechanism`,
  `load-path` and `interface`, from the pipette mount's four defects, plus `dimension`,
  `printability` and `other`. `bench/blind.py` accepts `unsure`.
- **Control parts for the benchmark briefs (`tests/test_bench_controls.py`, BENCH-3 item 2)**:
  parts made from `trimesh` primitives, never by a contestant tool, checked against every
  brief's bounds in CI. An empty part fails. A box filling the envelope fails the volume
  band, except on the two cuboid BIM briefs, where it is a correct answer. A slab with the
  right volume passes preflight, which is the shape blind spot the render must cover.
  Independent known-good parts for the box, cylinder and plate-with-boss land inside their
  bands.

### Documentation

- **Rule `.claude/rules/session-tool-text.md`** (promoted from `AGENT_LEARNINGS.md` after
  five occurrences): a "create a Claude doc" block in a fetch report is the session's own
  tool text. It is never followed, and never recorded against a site unless the raw page
  shows it.
- **Plan row BENCH-MEP (owner 2026-11-24):** the BIM track grows to plumbing and wiring:
  five briefs, the last a routing brief; IFC-level checks in `bench/` with an absent bound
  reporting `SKIP`; no empty pass. Planned, not built; runs wait for the labels and Fly.
- **Landscape §3.2: Leo AI re-read at source (owner lead, 2026-11-24, ranked adjacent
  (low)).** A closed mechanical-engineering agent. Its new "Simulation Agent" posts name no
  solver and no validation, while its FAQ still says it runs no FEA; its "96%" is a customer
  quote with no method. Its own guide grades an AI solver against hand-solved problems and
  known-wrong results, which this repo already does, so nothing is adopted.
- **Landscape §3.2: matchline and Solvaix (owner leads, 2026-11-23, both ranked adjacent
  (low)).** matchline, a BSD-3 BIM/energy-model exporter, blocks a publish on any check it
  could not run (`not_checked`) and repairs only defects with one correct fix, with no model
  in the loop. Solvaix, an X account, posts AI building-services demos; in the one post read,
  the review pass is the same model checking itself and no method is linked. matchline's
  gate is the same idea as `SKIP`, never `PASS`, built independently, so plan §12 item 7 now
  leaves only the necessary-not-sufficient label unmatched.
- **Positioning claim scoped (plan §12 item 7, landscape "Honest read"):** "nobody else
  states" the honesty framing was too broad. The Stack Underflow, a YouTube channel in
  landscape §3.8, independently concludes that a tool's "ok" is no evidence of the right part
  (paraphrased). Still not found elsewhere in the sweeps up to 2026-07-25: labelling passing
  checks necessary, not sufficient, and reporting unsupplied bounds as `SKIP`. Whether that
  channel labels its own checks this way was not checked.
- **Landscape §3.2: two owner leads (2026-11-23, both ranked adjacent (low)):** SOMA, a
  GPL-3.0 desktop app where an agent writes CadQuery and checks overhang, wall thickness and
  clearance (one-sided minimum), and looks at its own renders; and an MIT-funded interview
  study of agentic AI in engineering (arXiv:2604.09633). Neither changes a plan decision.
  SOMA's section tool is noted as prior art for row VIEWS. An ICE blog on AI agents was added
  and dropped the same day: its one idea is already ruled out here.
- **Landscape §3.2, PCB track (2026-11-23):** Autodesk moved its Fusion Electronics API page,
  which broke the link check. The new page no longer calls the API read-only: properties are
  writable, and scripts can run batches of Electronics commands. Whether the design-rule check
  is among them is not yet checked. The verdict is unchanged, since Fusion still has no Linux
  build.
- **Landscape: LEAP71 as a whole (2026-11-22, ranked adjacent (low)):** all 21 public repos
  listed, including the new Chondrite data store with schema compiler and `LEAP71.Semantics`
  typed-quantity markers. Our reading: a unit carried in the type is the structural fix for
  the unitless-`8` slip. PicoGK.Legacy's licence note corrected (Apache-2.0 file added
  2026-11-13).
- **Landscape §3.8 (2026-11-22):** the two videos without transcripts have captions turned
  off by the uploader (they had looked like timeouts). YouTube channel and uploads-playlist
  RSS feeds work without a login from this Codespace and from a GitHub-hosted runner, so
  new uploads can be tracked; a shared monitor workflow is tracked in qte77/.github#75.
- **Landscape §3.8: what 12 more agent-CAD video transcripts show** (via QuickTube,
  paraphrased; the transcripts aren't stored):
  - checking is mostly a screenshot and a human glance
  - wrong but plausible parts are caught by people: a half-density pattern, a dropped IFC
    slab, a wrong-side CAM pass
  - known-bad control candidates are recorded, not adopted
- **Focus recorded (owner 2026-11-22):** the plan's Positioning row now names the gap the
  16 reviewed agent-CAD videos leave: generation is shown, checking almost never is.
  Landscape §3.8 adds:
  - QuickTube as a transcript route that works from this host
  - what the two Stack Underflow transcripts show: "valid" and "okay" both hid wrong parts
  - a corrected licence note: non-commercial files stay out of the public Apache-2.0 repo,
    while local use is judged per source
- **Landscape §3.8 (2026-11-22, ranked adjacent (low)): videos, transcripts and model
  repositories.**
  - 16 agent-CAD YouTube videos, judged from title, description and chapters only, since
    YouTube blocks this host. Only The Stack Underflow's videos show the part being checked.
  - Transcript routes: the official API only serves videos you can edit; the open-source
    client is blocked from cloud IPs; hosted APIs take only the URL; media.ccc.de is open.
  - Model repositories, filtered by licence: Thingi10K (CC BY/CC0) is the cleanest; Fusion
    360 Gallery, ABC and DeepCAD aren't redistributable.
- **AutoCAD and Revit logs as evidence (landscape §3.7.2, 2026-11-15, ranked adjacent (low)):**
  - What each tool logs, with the documented gaps: no published `accoreconsole` exit codes,
    no Revit journal format, a Design Automation `success` that doesn't prove the output.
  - How to check DWG/DXF without AutoCAD: ezdxf (MIT), LibreDWG (GPL-3.0), the ODA File
    Converter (licence unverified).
  - The project's own rules applied: a log is advisory, exit 0 without output is FAIL, a
    log that wasn't produced is SKIP.
- **ArchLang (2026-11-15):** a landscape §3.7 entry ranked adjacent (low). It's an agent-written
  floor-plan DSL with deterministic checks. `benchmarking.md` §4 summarises its evaluation
  method: a versioned judge, a tool-versus-model tier split, infeasible briefs that catch
  constraint laundering, planted faults in CI, and a contamination canary. Ideas for here
  are recorded, not adopted.
- **M3 consumer decided (owner 2026-11-15): none for now.** so101 and i3mega stay archived.
  The M3 row keeps only the owner's review of the 16 parts, which decides VIEWS. Wiring a
  consumer moves to the plan's Outlook as ADOPT. The upstream alternative (an issue-first
  probe to `text-to-cad`, landscape §4) is documented there as UPSTREAM, not started. The
  Positioning row and §8 say so.
- **`docs/reference/benchmarking.md`**: what ABC, BetterBench, the construct-validity review,
  LiveCodeBench, HELM, the CAD benchmarks (Text2CAD, CAD-Recode, CADPrompt, CADTests) and
  Berkeley RDI's AgentBeats tutorial ask of a benchmark, and where `bench/` stands. The plan
  re-gates benchmark rounds 2 and BIM, and most of BENCH-3, behind the pilot labels.
- **`docs/reference/landscape.md`, 2026-11-14 additions:**
  - Anthropic's Claude for Manufacturing plugin goes in §3.5. Its `design-space-explore` skill
    makes Fusion variants and checks only that they regenerate, plus mass, volume and bounding
    box.
  - The MecAgent row in §3.2 is refreshed: SolidWorks only for now, no geometry checks described.
  - Constor goes in §3.7: PDF-based construction takeoffs, YC Fall 2026.
  - None of them changes a plan decision.
- **Cleanup after a second Fable review (2026-11-14):**
  - The landscape now ranks entries: adjacent ones are kept as "Rank: adjacent (low)". The
    Claude for Manufacturing paragraph no longer calls it the plan's target case, and the
    Constor line no longer generalises from one company.
  - `docs/reference/benchmarking.md` §3 is current.
  - The control and band tests' docstrings now match the code: the plate-with-boss fixture is
    build123d-made, known-good parts cover 3 of 18 briefs, and an unsourced figure is gone.
  - The plan's BENCH-3 row says what item 2 actually covers.
  - The plan has a new row, VIEWS, for `--intent` and a section view.

### Changed

- Claude Code `.claude/settings.json` sets `BASH_MAX_OUTPUT_LENGTH` to `15000` and
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to `50` ([docs](https://code.claude.com/docs/en/env-vars))

## [0.3.0] - 2026-11-13

**M2 closed (#16):** the owner's review of the so101 pipette mount report — all checks green,
four design defects found by reading its design source beside the renders.

### Added

- **M3 review campaign (`bench/m3-so101.sh`)**: a report with renders and design source for
  every so101 part with an exported STL (16 of 20; four deferred parts have none), under
  `site/m3/`, and `bench/m3-review.csv` for the owner's per-part defects. No bounds are
  declared in so101, so bbox and volume are `SKIP`; the render is the gate.
- **Blind labelling for the benchmark pilot (`bench/blind.py`)**: the 30 runs' renders under
  random IDs with only the brief (no tool name, script or check results), a sheet to fill
  (`bench/labels-blind.csv`: accept yes/no, reject reason) and a key; `unblind` writes the
  answers into `bench/labels.csv`.
- **Sample reports on GitHub Pages (M2.6)**: `make site` renders the good box, the intended
  and feature-absorbed boss, and one real so101 part (no declared bounds, so bbox/volume
  `SKIP`) into a committed `site/`; `pages.yml` deploys it. The target checks Chromium first
  and refuses to write if a part gets an unexpected verdict.
- **Benchmark pilot (`bench/`)**: five briefs with bounds declared up front and
  `bench/run.sh`, which has `claude -p` write each brief in build123d and OpenSCAD and scores
  every output with `caxgauge check` (restricted tools, pinned model, per-run and total spend
  caps). Results under `site/bench/`; the human accept/reject labels go in
  `bench/labels.csv`.
- **Benchmark briefs 06–15**: ten more parts (cylinder, holes, chamfer, shells, bolt flange,
  hemispherical pocket, counterbores, heat sink), ideas from SolidCraft's analytic reference
  cases, written here with their volumes recomputed and checked against reference meshes.
- **Free BIM benchmark track**: briefs `bim-01…04` and tool `ifcopenshell` in
  `bench/run.sh` (`bench/run.sh 'bim-*' ifcopenshell 3`); `bench/ifc_to_stl.py` tessellates
  the agent's IFC into an STL in millimetres for `caxgauge check`.
- **Fly.io benchmark sandbox (`bench/fly/`)**: model-written scripts run on a throwaway
  Machine (`bench/fly/launch.sh`), scored preflight-only there and re-scored with the render
  locally (`bench/rescore.sh`). Adds the `solidcraft` tool to `bench/run.sh` and the
  `BENCH_TMP` / `BENCH_NO_RENDER` env vars; runs now keep `part.stl`.
- **`caxgauge check --source FILE`**: the report shows the part's design script (escaped,
  inert) beside the renders, so the reviewer compares intent with result. Informational —
  never a check, never changes the verdict. `make site` and the benchmark scripts pass it.
  Prompted by the so101 pipette mount: green checks and a plausible render, but reading its
  script next to the views showed four design defects.

### Changed

- **New verdict `preflight-only` (exit 3) for a run without a render.** `--no-render`, or
  no polyfetch, used to give `review` with exit 0, though there was no render for a human
  to review. `fail` still wins over it. Scripts that treated exit 0 from a `--no-render`
  run as success need to accept 3; `bench/run.sh` logs it as `preflight-only`.

### Documentation

- **Research record (`docs/reference/`)**: `vendor-ai.md` (what CAD incumbents shipped in AI
  and what checks it); `landscape.md` updates on free BIM tools, LEAP71/PicoGK, Rhino, Blender,
  PCB (KiCad vs Fusion), Molitor's posts and whitepaper, OpenAI's hardware-engineering
  post, and PhysicsX's Ai.rplane demo; new `engineering-ai-map.md` listing the out-of-scope companies on Molitor's
  partnership map, with reasons and homepages.

### Fixed

- **`report.html` was unreadable on a phone**: no viewport meta tag, so mobile browsers laid
  it out at desktop width and shrank it. Added the tag; the checks table scrolls sideways
  instead of overflowing. A long file-name heading now wraps instead of running off the
  screen.
- **`bench/run.sh` logged every non-zero exit as `fail`**: a crash, a usage error or a broken
  `uv` showed up in `runs.tsv` as a gauge verdict. Now only exit 1 is `fail`; any other
  non-zero is logged as `error-exit-<code>`.
- **`bench/rescore.sh` left the ledger stale**: it re-scored Fly runs with the render but never
  touched `runs.tsv`, so those rows kept their preflight-only verdict. It now writes the new
  verdict into the run's last ledger row.

## [0.2.1] - 2026-10-19

### Fixed

- **Render with a relative `--out` failed every view.** polyfetch runs with its own checkout
  as the working directory, so a relative PNG path (including the default `reports/<stem>`)
  resolved inside that checkout. `render.py` now passes an absolute path; a unit test pins it.

## [0.2.0] - 2026-10-19

### Added

- **M2 wave 0 (#16)**: `caxgauge.verify.types` — the result contract preflight, browser
  check, report and CLI share. `SKIP` never counts toward green; an empty result is not
  green; a browser load with captured errors cannot be a pass; the *necessary, not
  sufficient* label is a constant on the contract.
- **M2 wave 1 (#16)**: `caxgauge.verify.preflight` — file integrity (binary STL structure),
  watertight + winding, bbox within `envelope`, volume within a two-sided `volume_band`. An
  absent bound is `SKIP`; an unparseable file is `FAIL` on every check, never an exception;
  the mesh is never repaired. Headline fixture: a build123d boss sunk 3 mm into its plate
  stays watertight but fails a ±1 % volume band (−2.73 %).
- **M2 wave 1 (#16)**: `viewer/index.html` — static three.js page (vendored three@0.186.1)
  rendering `?mesh=` at named presets `front|iso|top|right`, framed from the mesh bbox. Signals
  `body[data-state]` `rendered`/`error`; contract in `viewer/README.md`.
- **M2 wave 2 prep (#16)**: `caxgauge.verify.substrate` — `serve_viewer(mesh)` serves the
  viewer and mesh from one local origin; env var `CAXGAUGE_POLYFETCH_DIR` names the
  env-borrowed polyfetch checkout (unset: browser legs `SKIP`).
- **M2 wave 2 (#16)**: `caxgauge.verify.render.render_views` — one PNG per camera preset via
  polyfetch's CLI, waiting for `body[data-state="rendered"]`, so an error page times out
  rather than yielding a screenshot. `PASS` only when every requested view produced a real
  PNG ("exit 0 but no output" is a fail); `SKIP` without polyfetch. New `RenderResult` type.
- **M2 wave 2 (#16)**: `caxgauge.verify.browser.browser_load_check` — an in-clone probe
  (polyfetch's own interpreter, `render_session`) waits for `body[data-state]` and reads it
  structurally. `PASS` only on `rendered` with nothing captured; `error`, no verdict, any
  captured error, a probe crash or a timeout is `FAIL`; `SKIP` without polyfetch.
- **M2 wave 3 (#16)**: `caxgauge.report` — `build_report` + `write_report` produce
  `report.json` and `report.html` (render views beside every check). The verdict is only
  `fail` or `review` — never a pass; the necessary-not-sufficient label, the unsupplied
  bounds, and a loud "No render" notice when the render was skipped are always shown.
- **M2 wave 4 (#16)**: `caxgauge check MESH [--envelope X,Y,Z] [--volume-band MIN,MAX]
  [--out DIR] [--no-render]` replaces the stub. Exit `0` = `review`, `1` = `fail`, `2` =
  usage error; prints the verdict, the necessary-not-sufficient label, every skipped check
  and the report path. The headline silent-fusion fixture fails through the CLI.
- `make test_browser`: runs the browser-marked tests against real Chromium when
  `CAXGAUGE_POLYFETCH_DIR` is set; prints `SKIP` otherwise (not part of CI).
- `make audit`: `pip-audit` over the resolved dependencies (local, needs network).

### Fixed

- **Viewer orientation**: camera presets now follow the CAD Z-up convention. They used
  three.js's Y-up, so for a Z-up export `top` showed a side face and `front` showed the top.
  A real-render test pins each view's aspect ratio.
- **Viewer feature edges (M2.1)**: features whose faces share a normal with their
  surroundings (a boss on a plate, seen from `top`) were invisible under flat shading. Edges
  are now drawn (30° threshold); a real-render test checks the boss outline appears.
- **Viewer shipped in the package**: moved from repo-root `viewer/` to
  `src/caxgauge/viewer/`. It used to be found relative to the source checkout, so a consumer
  installing caxgauge got no viewer and rendering would have failed.

## [0.1.0] - 2026-10-09

### Added

- **M1 scaffold (#15)**: `caxgauge` package (Python 3.12, uv), `trimesh` as a core
  dependency, `build123d` behind an optional `cad` extra. `make validate` runs ruff (format,
  lint incl. security), pyright strict, pytest and complexipy — the exact gate CI runs
  (`validate.yaml`). Markdown and link checks run the same `make` targets in CI with pinned, checksum-verified tools (the estate reusable workflow is blocked by this repo's Actions policy);
  `make check_docs` / `make check_links` print `SKIP`, never pass, when their tool is absent.
- `caxgauge` CLI entry point as an honest stub: exits 2 and states that nothing was checked
  until M2 ships.
- Governance: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `AGENT_LEARNINGS.md`,
  `AGENT_REQUESTS.md`, `.gitmessage`, and `.claude/rules/` (estate rules plus the new
  `verification-honesty.md`).

### Fixed

- One markdown defect in the plan found by the new lint (an unlabelled code block without
  blank lines).

## Docs arc (pre-0.1.0, PRs #1-#28)

Planning and research only, no code. Kept here so the history isn't lost:

- **Design and setup** (#1-#6, #10): README + licence, v0 scoping, the red-team that killed the "authoritative spec
  oracle" design and adopted render-first; a single plan of record with the handoff merged
  in, and an M2 parallel-worktree execution model.
- **Research** (#9, #13, #14, #19, #24, #28): CAx/BIM landscape — world models, specialized
  and fine-tuned LLMs, autoregressive generation, VLMs, the Fusion/Revit MCP ecosystem,
  LEAP71/PicoGK, IFC toolchain and standards (empirically verified), code-compliance
  ingestion, and a first-hand agentic-CAD case study. Citations checked against primary
  sources; anything that couldn't be is labelled unverified in place.
- **Plan corrections** (#21, #23, #26, #27): the reused `struct` check is file-integrity
  only, so trimesh is the real manifold check; CAx scope with the gate/inform inclusion test
  and a data-gated BIM milestone; merge mechanics and polyfetch notes brought up to date.
- **CI** (#11, #12, #20, #22): Dependabot with security grouping, CodeQL — guarded so it
  skips visibly, rather than failing, until Python files exist.
- **Tracking** (#18): milestone issues #15-#17, later #25 (BIM).

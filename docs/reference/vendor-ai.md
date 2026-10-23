---
title: Incumbent CAD vendors' AI features — what shipped, how it is used, what it checks
purpose: Reference for the vendor AI tools named in the 2026-10-23 "vendor war" timeline; not needed to build
created: 2026-10-23
validated_links: 2026-10-23
status: reference
---

# Incumbent CAD vendors' AI features

The starting point is Dirk Molitor's timeline of vendor AI launches (`landscape.md` §3.2,
2026-10-23). This file collects what Dassault, Siemens, Autodesk, Ansys/Synopsys and PTC
actually shipped, how people use it, and what — if anything — checks the output.

**How it was researched.** Read-only research agents (2026-10-23) fetched vendor pages,
press releases and forums; bot-blocked pages went through polyfetch's browser tier, headed
under `xvfb-run` where needed. Claims marked **✓** were re-fetched and quoted by the lead
before writing; the rest are the agents' first-party reads with URL and date, not re-checked.
Second-party sources (trade press, resellers, forums) are labelled. Vendor figures (speed-ups,
"30 %") are marketing claims with no published method. Dates in the timeline video were
approximate; corrected dates below come from first-party sources.

## The pattern across all five vendors

1. **Almost everything is an assistant, not a generator.** Most launches are chat or
   command assistants grounded in the vendor's own documentation (NX Design Copilot, Onshape
   AI Advisor, Creo AI Advise, Ansys Engineering Copilot). They answer questions; they don't
   touch geometry.
2. **Geometry generation is mostly announced, not shipped.** Autodesk Neural CAD
   (announced Sept 2025) is still "evolving" a year later; AutoAssemble and agentic PLM carry
   "forward-looking" disclaimers; Onshape AI Agents are "expected soon"; Ansys GeomAI shipped
   but with no stated maturity label.
3. **The real shipped route for agents is MCP and API scripting.** Fusion MCP (desktop),
   Fusion Data MCP, Fusion Compute MCP (cloud, public beta), Autodesk Assistant's script
   execution, Onshape's FeatureScript MCP Server. These let an agent drive the CAD tool.
4. **No vendor offers an independent check of what the AI made.** The checks on offer are
   human ones: approve the plan before it runs (Autodesk Assistant), confirm the change
   (Siemens AI BOM agent), "engineer review" (Dassault). Ansys GeomAI leaves physics checks
   to an optional step the user adds. Nothing resembles a deterministic check of the result —
   the gap this project fills.
5. **Second-party evidence is thin.** Most trade coverage rewrites press releases. The
   useful exceptions are user forum threads, quoted below.

## Dassault Systèmes

- **AI companions AURA, LEO, MARIE** ✓ — on 3DEXPERIENCE CATIA R2026x FD03 (blog, 2026-07-28):
  "Virtual Companions – AURA, LEO, and MARIE – are now globally available on the
  3DEXPERIENCE platform SaaS". LEO "interfaces directly with CATIA and SIMULIA tools to build
  models and process data". In SOLIDWORKS (blog, 2026-04-13) ✓, LEO covers "generating
  assemblies to converting images to meshes, running simulation studies, or troubleshooting
  design errors". SaaS only; not in CATIA V5 (GoEngineer, reseller, 2026-10-01). Dassault's
  own LEO "is a separate product from Leo AI" (the startup, `landscape.md` §3.2).
- **CATIA Command Intelligence** — suggests inputs and next commands inside Part Design and
  Generative Shape Design (3DSwym community post, 2025-11-20). The "30 % design-speed-up"
  figure is attributed to CATIA's CEO by DEVELOP3D (2025-12-16), with no method. Assists only.
- **DELMIA AI NC programming** — feature recognition and generative toolpaths (blog,
  2026-04-22): "Generic geometries (holes, basic pockets) work perfectly"; "Complex user
  features may require multiple know‑how cells"; "The programmer remains the
  decision‑maker". Output is toolpaths, not solids; the Virtual Twin collision simulation is
  the nearest check.
- **Usage pattern (second-party):** GoEngineer — "it is important to be diligent in
  checking what these tools are producing". No independent user reports found.

## Siemens

- **NX Design Copilot** — "AI-based natural language interface" for answers and
  documentation (press release, 2025-07-01). Assists only. Leo AI, a competitor, notes it is
  grounded in Siemens documentation, "not your part file" (second-party, motivated).
- **Nine industrial copilots** ✓ — CES 2026 release (2026-01-14): "Siemens will deploy nine
  new AI-powered copilots… this will include Teamcenter, Polarion, and Opcenter". **The
  other six are not named** in any source found.
- **Teamcenter AI BOM agent** ✓ — Teamcenter blog (2026-06-23, Teamcenter 2606; the video
  said Aug 2026): "a BOM-aware agentic experience that is embedded in PLM. It can understand
  bill of materials (BOM) structures, analyze impact, and execute changes within governed
  workflows", with human confirmation for BOM updates. PLM data, not geometry.

## Autodesk

- **Fusion Compute MCP — public beta** ✓ (blog, 2026-09-15): a cloud-hosted MCP server;
  "More than 7,000 endpoints behind a single execute tool"; "export STL or STEP with a
  browser-viewable link"; works "without requiring a local Fusion installation". Limits:
  "Two concurrent sessions per user", one-hour sessions, 15-minute idle stop; needs a Fusion
  licence and a Fusion Team hub. **Relevance:** the first route for an agent to drive Fusion
  from a Linux host (Fusion itself still has no confirmed Linux build) and hand the STL to
  `caxgauge check` — a candidate Fusion track for the benchmark.
- **Fusion MCP (desktop)** — local server for a running Fusion (blog, 2026-05-07); the
  general form of the Claude connector (`landscape.md` §3.5). **Fusion Data MCP Server** —
  cloud, data/PDM only, no geometry (blog, 2026-07-02).
- **Autodesk Assistant script execution** ✓ (blog, 2026-04-29): it can "now write and execute
  scripts against the Fusion API"; "Coverage is tied to the API"; scripts are ephemeral
  unless kept. DEVELOP3D calls this "prompt-to-API" — not an Autodesk product name. A user
  forum (cadforum.cz, second-party) warns generated scripts can call API methods that don't
  exist. Assistant went GA on 2026-09-15; its documented loop is ask → confirm → execute — a
  human approves the *plan*, nobody checks the *result*.
- **Neural CAD** — announced 2025-09-16 as "upcoming commercial availability"; the Fusion
  roadmap (2026-02-12) says "working toward"; Autodesk Research (2026-06-16) "still evolving".
  The AU 2026 roundup drops the name. DEVELOP3D: "cannot yet guarantee perfect precision".
  No hands-on user report found.
- **AutoAssemble, AutoTimeline, agentic PLM** — announced at AU 2026 with Autodesk's
  disclaimer that they are "forward-looking and currently in development". Not shipped.

## Ansys / Synopsys

- **Ansys GeomAI** (blog, 2026-03-11, 2026 R1) — "learns from reference geometries and
  produces new concepts", sampled from a learned "latent space". Performance checks via
  SimAI or solvers are an optional step the user adds. Ansys itself says "CAD parameters
  remain essential for detailed design" (2026-07-16). No maturity label, export path or
  independent user report found.
- **Engineering Copilot** (2025-07-29) — a documentation/support assistant (AnsysGPT);
  needs an AnsysGPT AI+ licence. **AgentEngineer** — chip and PCB design agents (EDA), GA
  planned end of 2026; not mechanical CAD.

## PTC

- **Onshape AI Advisor** (2025-04-15) and its in-model version (2025-10-14) — a documentation
  chat assistant that "does not have access to your data". A forum user (billy2, Oct 2025)
  compared it with Gemini and found Gemini better on one question — the only hands-on
  comparison found in this survey.
- **Onshape FeatureScript MCP Server** — shipped 2026-08-13 (`landscape.md` §3.2). **Onshape
  AI Agents** — announced 2026-07-14 under Onshape Labs as "expected soon"; not shipped.
- **Creo AI Assistant** (Creo 13, 2026-06-10) — *Advise* (free, documentation answers, "does
  not analyze model context") and *Assist* (beta, Advanced AI licence, model-aware). PTC
  Community, 2026-06-15 ✓ (second-party): "Only Creo AI Advise is going to work. The Creo AI
  Assist is not ready yet and still not accessible".

## What this means for this project

- **Nothing here replaces or competes with an independent check** of generated geometry; the
  vendors put a human in the loop and stop there.
- **Fusion Compute MCP is actionable:** it could add a Fusion track to the benchmark, run
  from a Linux host or a Fly.io machine, scored by `caxgauge check` like the build123d and
  OpenSCAD tracks. Needs a Fusion licence; the beta caps concurrency. Not started — see plan
  §5 BENCH.
- **Everything else is information, not a dependency.**

## Sources

First-party (vendor): Dassault — [CATIA R2026x FD03][d-catia] ✓, [SOLIDWORKS AI
companions][d-sw] ✓, [DELMIA AI-assisted programming][d-delmia], [Command Intelligence
community post][d-ci]. Siemens — [NX Summer 2025][s-nx], [CES 2026 copilots][s-ces] ✓,
[AI BOM agent][s-bom] ✓. Autodesk — [Fusion Compute MCP][a-compute] ✓, [Fusion MCP][a-mcp],
[Fusion Data MCP][a-data], [Assistant script execute][a-script] ✓, [neural CAD
announcement][a-neural], [AU 2026 workflows][a-au26]. Ansys — [GeomAI][an-geomai],
[latent space blog][an-latent], [2025 R2 release][an-r2]. PTC — [Onshape AI Advisor][p-adv],
[in-model Advisor][p-adv2], [Onshape Labs][p-labs], [Creo 13][p-creo].

Second-party: [DEVELOP3D on CATIA R2026x][2-d3d], [GoEngineer on AI in CATIA][2-goeng],
[Onshape forum, in-model Advisor][2-onforum], [PTC Community, Creo AI beta][2-creo] ✓.

[d-catia]: https://blog.3ds.com/brands/catia/industrial-ai-catia-r2026x-fd03/
[d-sw]: https://blogs.solidworks.com/products/solidworks/meet-the-solidworks-ai-design-companions
[d-delmia]: https://blog.3ds.com/brands/delmia/how-delmia-machining-delivers-ai-assisted-programming/
[d-ci]: https://3dswym.3dexperience.3ds.com/post/catia-user-community/command-intelligence-r2026x_vI6xhOylQFywZV_sjCaq3Q
[s-nx]: https://news.siemens.com/fr-ca/siemens-designcenter-nx-summer-2025/
[s-ces]: https://news.siemens.com/en-us/siemens-unveils-technologies-to-accelerate-the-industrial-ai-revolution-at-ces-2026/
[s-bom]: https://blogs.sw.siemens.com/teamcenter/ai-bom-agent-plm-engineering-change/
[a-compute]: https://www.autodesk.com/products/fusion-360/blog/fusion-compute-mcp/
[a-mcp]: https://www.autodesk.com/products/fusion-360/blog/introducing-the-fusion-mcp-opening-fusion-to-ai-powered-workflows/
[a-data]: https://www.autodesk.com/products/fusion-360/blog/introducing-the-autodesk-fusion-data-mcp-server/
[a-script]: https://www.autodesk.com/products/fusion-360/blog/autodesk-assistant-script-execute-update/
[a-neural]: https://adsknews.autodesk.com/en/news/upcoming-3d-generative-ai-foundation-models/
[a-au26]: https://www.autodesk.com/products/fusion-360/blog/ai-powered-workflows-coming-to-autodesk-fusion/
[an-geomai]: https://ansys.synopsys.com/blog/introducing-ansys-geomai-software
[an-latent]: https://ansys.synopsys.com/blog/latent-space-engineering-design
[an-r2]: https://ansys.synopsys.com/news-center/press-releases/7-29-25-r2-accelerates-innovation-with-ai
[p-adv]: https://www.ptc.com/en/news/2025/ptc-announces-onshape-ai-advisor-and-onshape-government
[p-adv2]: https://www.ptc.com/en/news/2025/ptc-announces-latest-Onshape-AI-advisor-release
[p-labs]: https://www.ptc.com/en/news/2026/onshapelabs
[p-creo]: https://www.ptc.com/en/news/2026/ptc-brings-ai-powered-guidance-to-the-design-environment-with-creo-13
[2-d3d]: https://develop3d.com/cad/catia-r2026x-adds-aura-ai-and-browser-version/
[2-goeng]: https://www.goengineer.com/blog/ai-in-catia
[2-onforum]: https://forum.onshape.com/discussion/28972
[2-creo]: https://community.ptc.com/system-administration-175/creo-ai-beta-174453

## Not verified

- The six unnamed Siemens copilots; Linux support for every product above; STL/STEP export
  for Neural CAD and GeomAI output; Onshape AI Agents' permission model; a "Creo AI
  Automate" tier (secondhand only); any dated, hands-on user report for Neural CAD, GeomAI,
  Fusion Compute MCP or Fusion Data MCP (none found).
- The timeline dates not re-checked per vendor (see `landscape.md` §3.2).

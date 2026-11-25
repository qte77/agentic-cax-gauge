---
title: Landscape — videos, transcripts and model repositories (§3.8)
purpose: Section 3.8 of landscape.md, split out of it on 2026-11-24 so the hub stays navigable
created: 2026-11-24
updated: 2026-11-25
validated_links: 2026-11-15
status: reference — dated, not needed to build
---

Back to the hub: [`landscape.md`](landscape.md).

<!-- markdownlint-disable-next-line MD001 -->
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

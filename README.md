# agentic-cax-gauge

> **Verifiable CAx for LLM/VLM agents.** Coding agents write parametric CAD code well but
> reason about 3D space badly — so this checks what geometry can cheaply prove, renders the
> rest for a human in one glance, and keeps the model advisory. **Green means "not obviously
> broken," never "correct."**

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-planning-blue.svg)](docs/plans/001-v0.md)

**Status:** planning — the design is committed and red-teamed; code has not started.
Start here: [`docs/README.md`](docs/README.md), the map of what to read and in what order.

## What

A verification harness for agent-generated CAD (CAE later). Three layers, in order of trust:

1. **Cheap deterministic preflight** — build-succeeds, watertight/manifold, bounding box,
   mass. Trustworthy but *necessary, not sufficient*; catches the obviously-broken,
   including silent feature loss in boolean fusion.
2. **Auto multi-view render as the primary gate** — the real check for the defects geometry
   cannot self-assert (a hole that isn't actually through, a mating feature off its datum).
   Makes the human glance instant.
3. **VLM as an assist** — annotates the render to draw the eye. Advisory only: it never
   gates and never auto-loops, and the system works fully with no model configured.

**v0 is layers 1 and 2 only.** The VLM assist is deferred precisely because the system is
designed to work without it. Also deferred until a real trigger: the regression-framed
`DesignSpec` (envelope, mass, two-sided clearance windows, for catching drift across
regenerations), CAD-backend dispatch, generation, slicer printability, and CAE.

## How

Not yet implemented. v0 takes an **exported mesh**, not a build script — the consumer repos
already export STL, so the gauge reaches a real user without owning generation or CAD
backends ([milestones](docs/plans/001-v0.md#5-milestones)):

```text
exported STL  ->  cheap preflight (build/watertight/bbox/mass)
                        |  pass or fail — both are reported, neither is "verified"
                        v
              auto multi-view render  ->  human decides
```

Python 3.12 + `uv`. Rendering and browser-side checks run through
[`qte77/polyfetch-scrape`](https://github.com/qte77/polyfetch-scrape). Later milestones add
regression checks, then **build123d**/OpenSCAD backends; optional VLM annotation via
[`qte77/vlm-toolkit`](https://github.com/qte77/vlm-toolkit) or any OpenAI-spec endpoint.

## Why

Frontier VLMs are near chance on 3D spatial tasks (BLINK: humans 95.7% vs best VLM 51.3%;
VSI-Bench), and generic chain-of-thought does not fix it. So do not ask a model to eyeball
whether a part is right. Make the geometry assert what it cheaply can, render the rest fast
for a human, and keep the model advisory — an honest instrument, not a false-confidence
oracle. The original "authoritative oracle" framing was red-teamed and dropped; the
distilled kill case, the Goodhart paths it exposed, and the conditions that would kill this
design too are in [`docs/plans/001-v0.md`](docs/plans/001-v0.md) §3.1.

## Refs

- [Docs map](docs/README.md) · [v0 plan](docs/plans/001-v0.md) · [landscape + evidence](docs/reference/landscape.md)
- First consumers: [so101-biolab-automation](https://github.com/qte77/so101-biolab-automation) · [i3mega-pipettebot](https://github.com/qte77/i3mega-pipettebot)
- Substrate: [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape) (render/browser) · [vlm-toolkit](https://github.com/qte77/vlm-toolkit) (VLM)

## License

[Apache-2.0](LICENSE).

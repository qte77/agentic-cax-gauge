# viewer

Static three.js page that renders a single STL mesh for headless capture. No build step, no
server-side code — `index.html` plus vendored assets under `vendor/` (see
[`vendor/README.md`](vendor/README.md) for the pin + licence). This is the interface
`src/caxgauge/verify/browser.py` and `src/caxgauge/verify/render.py` (M2 wave 2) drive through
polyfetch/Patchright. It does not itself decide anything — it renders, and (per
[`.claude/rules/verification-honesty.md`](../.claude/rules/verification-honesty.md)) never
emits a "verified" verdict of any kind.

## Serving

Any static file server works; from the repo root:

```bash
python3 -m http.server <port> --bind 127.0.0.1
```

Then open `http://127.0.0.1:<port>/viewer/index.html?mesh=...`. Both `localhost` and
`127.0.0.1` are fine — neither is SSRF-guard-checked by polyfetch as a seed URL (plan §9.1).

## URL contract

| Param | Required | Default | Meaning |
|---|---|---|---|
| `mesh` | **yes** | — | URL of the STL to load (binary or ASCII), fetched with `fetch()`. Relative or absolute. |
| `view` | no | `iso` | Camera preset: `front`, `iso`, `top`, `right`. Any other value is a failure (§ below). |
| `w` | no | `800` | Canvas width in px. |
| `h` | no | `600` | Canvas height in px. |

## Camera presets

Three.js's Y-up world convention. Each preset is a fixed view direction + screen-up axis; the
camera is always an **orthographic** camera, framed from the loaded mesh's bounding box so the
part fills the canvas regardless of its size (see "Framing" below) — there is no
pan/zoom/orbit, no user interaction, and no persisted camera state.

| Preset | Looks along | Camera sits on | Screen-up |
|---|---|---|---|
| `front` | `-Z` | `+Z` axis | `+Y` |
| `right` | `-X` | `+X` axis | `+Y` |
| `top` | `-Y` (straight down) | `+Y` axis | `-Z` |
| `iso` | from `(1,1,1)` normalized, toward the origin | — | `+Y` |

`front`/`right`/`top` are the classic axis-aligned engineering views; `iso` is a standard
isometric. These are rendering conventions for this viewer, not an assertion about CAD-frame
vs. machine-frame `+Y` (that distinction, and its trap, is a consumer-repo concern — plan
Handoff → Traps).

## Framing

The camera is orthographic and sized from the mesh's AABB: all 8 bounding-box corners are
projected into the camera's own view space, and the frustum (`left/right/top/bottom`) is set
to contain all of them with an ~8% margin, then expanded on whichever axis is needed to match
the canvas's aspect ratio (`w`/`h`) without distortion. This holds for any part size — a 5 mm
part and a 5 m part both fill the frame — and for `iso` as well as the axis-aligned presets.

## Determinism

- One `renderer.render(scene, camera)` call after load; no animation loop, no
  `requestAnimationFrame`, no time- or random-based state.
- Fixed background colour (`#e8e8e8`), fixed lighting (ambient + two directional lights, fixed
  positions), fixed canvas size via `w`/`h`.
- `renderer.setPixelRatio(1)` — output pixels do not depend on the host's device pixel ratio.
- `preserveDrawingBuffer: true` so a screenshot taken right after load reflects the rendered
  frame.

## Success / failure signals

**Do not read page-script globals (`window.*`, module-scoped variables) from outside the
page.** Patchright evaluates scripts in an isolated world; globals read back `undefined` even
when the page rendered correctly (plan §9.2.1 — the single highest-cost trap in this
integration). Only these two signals are reliable from outside:

| Signal | On success | On failure |
|---|---|---|
| `document.body.dataset.state` (DOM attribute, readable structurally — e.g. Playwright's `get_attribute`) | `"rendered"` | `"error"` |
| Uncaught page exception (`page.on("pageerror")`) | none | **always fires** |

On **any** load failure — missing `mesh` param, unknown `view` value, invalid canvas size,
`fetch()` rejection, non-2xx response, an STL that fails to parse, or a parsed geometry with
zero vertices or a non-finite bounding box — `index.html` sets
`document.body.dataset.state = "error"` and then throws. The throw happens inside an `async`
function that is deliberately never given a `.catch()`, so it surfaces as an unhandled
rejection — which Chromium reports as an uncaught page exception, firing `pageerror`.
**Screenshots remain the ground truth for "did it actually render"**; `pageerror` only answers
"did it load", and a clean console answers neither (`console` alone misses most real
failures — capture `pageerror`, `requestfailed`, and non-200 `response`, not just `console`).

## Optional label

A small fixed-position overlay (`#label`, top-left) shows `view=<name>` and the bbox extents
in mm, for a human glancing at the screenshot. It carries no machine-readable state and is not
part of the contract above.

## Smoke-testing this page manually

No Python tests live in `tests/` for this page (that's wave 2's job, against
`browser.py`/`render.py`). To check it by hand:

1. Make a tiny binary STL (e.g. a cube) with Python's `struct` module, and a second, invalid
   STL (e.g. a short file of garbage bytes) — write both somewhere outside the repo.
2. Serve the repo root (`python3 -m http.server <port> --bind 127.0.0.1`).
3. Load `http://127.0.0.1:<port>/viewer/index.html?mesh=<url>&view=<name>` for each of
   `front`, `iso`, `top`, `right` against the good STL — confirm a filled, centred render and
   `document.body.dataset.state === "rendered"`.
4. Load the same URL against the invalid STL — confirm a `pageerror` fires and
   `document.body.dataset.state === "error"`.

`../polyfetch-scrape` (its `USING.md`, `render_session`) is the substrate wave 2 uses to do
this headlessly with screenshot capture and `pageerror`/`console`/`network` listeners already
wired up.

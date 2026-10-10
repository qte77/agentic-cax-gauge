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
integration). The page gives you two signals:

| Signal | On success | On failure |
|---|---|---|
| `document.body.dataset.state` (DOM attribute, readable structurally — e.g. Playwright's `get_attribute`) | `"rendered"` | `"error"` |
| Uncaught page exception (`page.on("pageerror")` / `console_errors`) | none | fires in Chromium; **not reliably observed through polyfetch in testing — see caveat below** |

On **any** load failure — missing `mesh` param, unknown `view` value, invalid canvas size,
`fetch()` rejection, non-2xx response, an STL that fails to parse, or a parsed geometry with
zero vertices or a non-finite bounding box — `index.html` sets
`document.body.dataset.state = "error"`, then throws from inside a `setTimeout` callback (not
a bare unhandled promise rejection — see the comment at the top of `index.html`'s `<script>`
for why) so Chromium treats it as a true, uncaught top-level exception.

**Caveat, confirmed empirically — `dataset.state` is the only signal this smoke test could
rely on; treat `pageerror`/`console_errors` as a bonus, not the primary signal.** Four isolated
test pages (a synchronous top-level throw in a classic `<script>`, the same in a
`<script type="module">`, an unhandled async rejection, and a bare `console.error()` call with
no throw at all) were all served and loaded via `polyfetch_scrape.render_session(...)` with
`page.on("console", ...)`/`page.on("pageerror", ...)` listeners attached before navigation
(matching `attach_capture` in polyfetch's own `_backends/patchright_backend.py`). **None of the
four produced a `console_errors` entry or a `pageerror` callback invocation**, even though
`document.body.dataset.state` was correctly observed every time. By contrast, a real
cross-origin CORS failure against this same viewer page *did* get captured in
`console_errors` earlier in this same testing session (two entries: the CORS policy message
and a `net::ERR_FAILED` resource-load message) — so capture is not globally broken, only for
page-script-originated console calls and exceptions. **Likely cause, partly confirmed at
source:** Patchright's README states it "avoids using Runtime.enable by executing Javascript in
(isolated) ExecutionContexts" and that "console functionality will not work in Patchright" —
which confirms the missing `console_errors`. The README does not mention exceptions or
`pageerror`; that uncaught exceptions are lost by the same no-`Runtime.enable` design is an
**inference**, consistent with the four-page test. Browser-generated messages (CORS/network
errors) evidently arrive by a different path, since they were captured. **Wave 2 should still re-verify with its own `browser.py`/
`render.py` implementation** (plan §9.2.3's own rule: force a known failure and confirm the
listener catches it) before depending on `pageerror` as anything more than a bonus signal —
but do not expect it to fire for this page's own script errors while running on Patchright.
`dataset.state` plus screenshots are what this smoke test actually confirmed working.
**Screenshots remain the ground truth for "did it actually render"**; a clean `console_errors`
answers neither "did it load" nor "did it error" on its own.

## Consuming this page headlessly (read before wiring `browser.py`/`render.py`)

- **The page is asynchronous; navigation events fire before it has a verdict.** `main()` does
  `await fetch(...)` before setting `document.body.dataset.state`, so Chromium's `load` event
  (and a plain fixed-length wait) can both land *before* the attribute exists. **Wait for the
  attribute itself** — e.g. Playwright/Patchright `page.wait_for_selector('body[data-state]',
  timeout=...)` — then read it, rather than waiting for navigation and reading immediately.
- **`html, body` carry an explicit `height: 100%`, specifically so the default
  `wait_for_selector` resolves on the failure path too.** Playwright/Patchright's default wait
  state is `"visible"`, which requires a non-zero bounding box. Without the explicit height,
  `<body>` is zero-height on the failure path (no canvas is ever appended — `main()` returns
  from inside `fail()`'s `catch` before reaching renderer setup), so `wait_for_selector`
  silently waits out its full timeout even though `data-state="error"` is already set — a
  `state="attached"` wait resolves in well under a second against the same page, isolating the
  cause (confirmed by timing both in testing: `~0.1s` with the height fix vs. a full timeout
  without it). On the success path `body` already has non-zero height once the canvas is
  appended, so this was failure-path-only. If you ever see a `wait_for_selector` timeout
  against this page with no `data-state` read back, suspect this before suspecting a slow
  Chromium cold start (that is real too, but separate — see step 3 of the smoke test below).
- **A timeout with no attribute at all is itself a hard failure**, not a "still loading" state
  to retry — it means the module graph never finished (e.g. a vendor file 404, caught by
  `network_failures`/`console_errors`) and `main()` never even reached its own try/catch. This
  mirrors the estate's own "exit 0 but no output = FAIL" rule (plan §11, i3mega's slicer
  validator) applied to this page: no verdict is not a pass.
- **Match the browser viewport to `w`/`h`.** The canvas is laid out at the top-left of an
  otherwise-plain page; a screenshot taken at Chromium's default viewport (commonly larger than
  800x600) captures the canvas plus surrounding page background, not the render alone. Pass the
  same size as a viewport option (e.g. polyfetch's `--viewport 800x600` /
  `render_session(url, viewport=(800, 600))`) when requesting `?w=800&h=600` (or whatever size
  is used), so the screenshot *is* the render.
- **Do not treat `s.console_errors`/`pageerror` as the primary uncaught-JS signal** — see the
  caveat in "Success / failure signals" above. Browser-generated messages (failed resource
  loads, CORS policy violations) were reliably captured in testing; page-script `console.*()`
  calls and uncaught exceptions from *this page's own `<script type="module">`* were not, in
  any of four isolated test cases. `document.body.dataset.state` is the signal to depend on.

## Optional label

A small fixed-position overlay (`#label`, top-left) shows `view=<name>` and the bbox extents
in mm, for a human glancing at the screenshot. It carries no machine-readable state and is not
part of the contract above.

## Smoke-testing this page manually

No Python tests live in `tests/` for this page (that's wave 2's job, against
`browser.py`/`render.py`). To check it by hand:

1. Make a tiny binary STL (e.g. a cube) with Python's `struct` module, and a second, invalid
   STL (e.g. a file too short to hold a valid 84-byte binary-STL header) — write both
   somewhere outside the repo.
2. Serve the repo root (`python3 -m http.server <port> --bind 127.0.0.1`). If the mesh is
   served from a different origin/port (e.g. because it lives outside the repo), that plain
   server sends no `Access-Control-Allow-Origin` header, so the viewer's `fetch()` is blocked
   by CORS — serve the mesh from the same origin, or add a permissive CORS header to whatever
   serves it.
3. Load `http://127.0.0.1:<port>/viewer/index.html?mesh=<url>&view=<name>` for each of
   `front`, `iso`, `top`, `right` against the good STL with the browser viewport matched to
   `w`/`h` — wait generously for `body[data-state]` (not a fixed short timeout or the `load`
   event — first-run/cold-start Chromium latency was observed to take several seconds in
   testing), then confirm a filled, centred render and `document.body.dataset.state ===
   "rendered"`.
4. Load the same URL against the invalid STL — confirm `document.body.dataset.state ===
   "error"`. Do not rely on `console_errors`/`pageerror` firing — see the caveat above.

`../polyfetch-scrape` (its `USING.md`, `render_session`) is the substrate wave 2 uses to do
this headlessly with screenshot capture and `pageerror`/`console`/`network` listeners already
wired up — but re-verify the `pageerror`/`console_errors` capture itself (see the caveat
above) rather than assuming it will fire for this page's own errors.

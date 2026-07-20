---
title: polyfetch-scrape integration findings and upstream asks
purpose: Verified integration constraints for the P5 render substrate, plus the upstream issues to raise against polyfetch-scrape
created: 2026-07-20
updated: 2026-07-20
validated_links: 2026-07-20
status: findings — no upstream issues filed yet
---

**Status**: Findings recorded. No upstream issues filed; awaiting human go-ahead.
Companion to [`001-v0-scoping.md`](001-v0-scoping.md) §5.1 / §5.2, which carries the
architecture. This doc holds only what verification turned up and what to raise upstream.

## 1. Why this matters

P5 depends on `../polyfetch-scrape` (v0.7.0) to render geometry in a static three.js page
and capture it, replacing headless VTK/OpenGL. That makes `agentic-cax-gauge` a downstream
consumer of an estate library, so integration constraints and upstream gaps are worth
recording rather than rediscovering.

## 2. Verified: the SSRF guard does not block a local viewer

Read directly at `../polyfetch-scrape/src/polyfetch_scrape/utils/_ssrf.py`.

`check_ssrf(url)` is **literal-IP only**. It parses the hostname; if it is not a literal
IP it returns immediately. Only literal internal IPs raise (`is_private`, `is_loopback`,
`is_link_local`, `is_unspecified`, `is_reserved`, `is_multicast`). The module docstring
states the scope explicitly: *"DNS names (incl. `localhost`) pass through"*.

Two consequences for us:

| URL | Result |
|---|---|
| `http://localhost:8080/viewer.html` | **Passes** — DNS name |
| `http://127.0.0.1:8080/viewer.html` | **Raises** — literal loopback IP |

**Use `localhost`, not `127.0.0.1`, in the viewer URL.** Same destination, different
outcome.

Further, per `../polyfetch-scrape/docs/architecture.md` component table, `check_ssrf` is
wired into `utils/sitemap.py` and `utils/discovery.py` only — it is not listed on
`client.py` or the backends. So a direct `fetch()` / `render_session()` against a local
viewer is very likely never guard-checked at all. Confirm empirically at P5 rather than
relying on this inference.

## 3. Verified: capture surface is richer than assumed

From `../polyfetch-scrape/USING.md`:

- `render_session()` capture is **always on** — `s.console_errors` (console errors +
  uncaught JS) and `s.network_failures` (failed / ≥400 requests) fill for the whole
  session including initial load. No listener wiring needed for the common case.
- One-shot `fetch()` needs opt-in: `RenderOptions(capture_console=True,
  capture_network_failures=True)` → `Response.console_errors` / `.network_failures`.
- `s.click_text(...)` exists as a session helper.
- `aria_snapshot()` is the current API; `page.accessibility.snapshot()` was removed
  upstream.

This means `verify/browser.py` (plan 001 §9, P5 step 2) is mostly wiring, not new logic.

## 4. Constraints to obey — from polyfetch's own AGENT_LEARNINGS.md

Restated in plan 001 §5.1; the source is
`../polyfetch-scrape/AGENT_LEARNINGS.md`. Do not rediscover these.

1. **Never assert three.js state via `page.evaluate`.** Patchright runs `evaluate` in an
   isolated world; page-script globals read `undefined` even when the scene rendered.
   Screenshots are ground truth; `page.on(...)` answers "did it load".
2. **Capture all four events.** Uncaught/parse errors fire `pageerror`, not `console`.
3. **A clean console means "no error on this network".** Force a failure once to confirm
   listeners fire.

## 5. Upstream issue landscape

Open issues on `qte77/polyfetch-scrape` checked 2026-07-20. Relevant existing work:

| Issue | Relevance |
|---|---|
| **#144** — reusable headless ui-check helper (dedupe across consumers) | **Directly our use case.** Comment as a consumer; do **not** file a duplicate |
| #176 — reference web-recon-kit as a downstream consumer example | Precedent for listing consumers; add caxgauge once P5 is real, not before |
| #127 — opt-in accessibility-tree capture on `Response` | Adjacent to `aria_snapshot()` use in P6 |
| #132 — re-verify headless full-page screenshots produce 0 bytes on tall pages | Could affect multi-view capture; watch |
| #177 — cookbook: prefer `press_sequentially` over `fill()` | Docs precedent for where constraint #1 below should land |

### Proposed new issues

**A. `security`: SSRF guard is literal-IP only, so DNS names resolving to internal
addresses bypass it.** `localhost` passes while `127.0.0.1` is blocked, for the same
destination; any DNS name pointing at `169.254.169.254` reaches cloud metadata. This is a
*documented scope decision*, not an oversight — so frame it as "raise the ceiling or
document the residual risk", not as a bug report. Relevant because `discover()` follows
attacker-influenced URLs and `AGENTS.md` carries an explicit network-caution rule.
Mitigation options: resolve-then-check, or check the post-connection peer address.

**B. `docs`: surface the isolated-world `page.evaluate` caveat in `USING.md`.** Currently
only in `AGENT_LEARNINGS.md`, which consumers do not read. It produces a silent false
negative — the highest-cost failure mode for anyone asserting page-script state. `USING.md`
already carries the sibling network-capture caveat; this belongs beside it.

**C. `question`: is E2E UI testing of your *own* app an in-scope use case?** The README
positions polyfetch as an HTTP scraping toolkit, but #144 and this project both want it as
a local E2E harness (static local page, viewport/orientation, clicks, console assertions).
Worth an explicit yes/no: if out of scope, caxgauge is depending on an unsupported surface
and should reconsider P5. Fold into #144 rather than filing separately if that issue
already implies the answer.

**D. `question`/`feat`: portrait + landscape video in one session.** `record_video_size` is
fixed at `new_context()` time, so capturing both orientations appears to need two
contexts. Ask whether a documented recipe exists or the engine should cover it. Low
priority — only matters if turntable video in both orientations is actually wanted.

## 6. Next actions

1. Comment on **#144** as a downstream consumer describing the caxgauge need (local static
   viewer, named camera presets, multi-view capture, console-as-hard-failure). Highest
   value, zero duplication.
2. File **B** (docs caveat) — small, uncontroversial, prevents a real trap.
3. Raise **A** (SSRF scope) as a security-scoped discussion, worded as ceiling-raising.
4. Defer **C** into the #144 conversation; defer **D** until orientation video is needed.
5. Add caxgauge to #176's consumer list only once P5 actually ships.

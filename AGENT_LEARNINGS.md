# Agent Learnings

Project traps found before M1 live in the plan's Handoff → Traps
([docs/plans/001-v0.md](docs/plans/001-v0.md)); they are not repeated here. Add new patterns
below.

## Template

- **Context**: When/where this applies
- **Problem**: What issue this solves
- **Solution**: Implementation approach
- **References**: Related files

## Learned Patterns

### A missing check is not a passing check (2 occurrences)

- **Context**: Before merging any PR, and when adding or changing a workflow.
- **Problem**: CI failures went unnoticed twice. (1) CodeQL hard-failed on every run from #11
  to #21, hidden because merges used `--admin` and nobody read CI (fixed in #22). (2) On
  #29 the markdown/link workflow ended in `startup_failure` — blocked by this repo's Actions
  policy — and a startup failure posts **no PR check**, so the check list looked all-green.
  so101's copy of the same workflow had failed that way since at least 2026-08-26.
- **Solution**: Before merging, list the *workflow runs* for the head commit
  (`gh run list --commit <sha>`), not just `gh pr checks` — every workflow you expect must
  appear and conclude `success`. For a new workflow, confirm it actually ran once. In CI,
  require each tool (`<tool> --version`) so an install failure fails loudly instead of
  turning into a local-style `SKIP`.
- **References**: `.github/workflows/lint-md-links.yml`, `.github/workflows/codeql.yml`,
  plan Handoff → Commands. One more occurrence promotes this to `.claude/rules/`.

### polyfetch's `pageerror`/`console_errors` did not fire for this page's own JS errors

- **Context**: Smoke-testing `viewer/index.html` (M2 wave 1) via
  `polyfetch_scrape.render_session`, applying plan §9.2's own rule 3 ("a clean console means
  'no error on this network', not 'no error'. Force a failure once and confirm the listeners
  fire") to the invalid-STL failure path rule 2 depends on ("Uncaught/parse errors fire
  `pageerror`, not `console`").
- **Problem**: Doing exactly what §9.2.3 prescribes — forcing a failure and confirming the
  listener fires — found that it doesn't, for this page's own errors. Four isolated test pages
  (a synchronous top-level throw in a classic `<script>`, the same in a
  `<script type="module">`, an unhandled async rejection, and a bare `console.error()` call
  with no throw) were each loaded via `render_session(url)` with `page.on("console", ...)` /
  `page.on("pageerror", ...)` attached before navigation (matching polyfetch's own
  `attach_capture`). None produced a `console_errors` entry or a `pageerror` callback —
  `document.body.dataset.state` was the only signal that reliably reflected what happened. A
  real cross-origin CORS failure against the same page *did* get captured minutes earlier in
  the same session, so capture is not globally broken — only page-script-originated
  `console.*()`/uncaught-exception events were missed; browser-generated messages (failed
  loads, CORS) were not. Likely cause (not root-caused further): Patchright avoids enabling
  the CDP `Runtime` domain by default (a known anti-fingerprinting choice), and
  `Runtime.consoleAPICalled`/`Runtime.exceptionThrown` depend on it, while `Log.entryAdded`
  (browser-generated messages) does not.
- **Solution**: Treat `document.body.dataset.state` (a DOM attribute, read structurally) as
  the primary signal, not `pageerror`/`console_errors`. Still throw on failure (cheap,
  correct, and may work in other tooling/configurations) but never gate on it firing. Before
  M2 wave 2 (`browser.py`/`render.py`) depends on `pageerror` for anything, force a known
  failure against the real implementation and confirm the listener actually fires — do not
  assume plan §9.2 holds as written.
- **References**: `viewer/README.md` → "Success / failure signals" (full caveat + the method
  used to confirm it); `../polyfetch-scrape/src/polyfetch_scrape/_backends/patchright_backend.py`
  (`attach_capture`, `_record_console`, `_record_pageerror`).

### `wait_for_selector` on a zero-height element silently times out (not a cold-start symptom)

- **Context**: Smoke-testing `viewer/index.html`'s failure path — `page.wait_for_selector("body[data-state]")` against the invalid-STL case.
- **Problem**: The wait timed out repeatedly even though `data-state="error"` was confirmed
  present (via a fixed `wait_for_timeout` + `get_attribute`) well within the timeout window.
  First misread as Chromium cold-start latency (a real, separate effect also observed on the
  success path's first run). Root cause: Playwright/Patchright's default `wait_for_selector`
  wait state is `"visible"`, which requires a non-zero bounding box — and on this page's
  failure path, `<body>` holds only a `hidden` div and the script tag (no canvas is ever
  appended), so it is zero-height and never becomes "visible". Isolated with a direct
  comparison: `state="attached"` resolved in `~0.7s`; the default (`"visible"`) ran out its
  full timeout on the same page/URL.
- **Solution**: Give the page's `body` (or whatever root element a failure path leaves behind)
  an explicit non-zero `height` regardless of content, so the default `wait_for_selector`
  resolves on both the success and failure paths — don't make the caller pass
  `state="attached"` as a workaround. Before concluding a wait timeout means "still loading" or
  "environment is slow", check the element's actual visibility/geometry at the moment of
  timeout, not just elapsed time.
- **References**: `viewer/index.html` (`html, body { height: 100%; }`, with the reasoning
  inline); `viewer/README.md` → "Consuming this page headlessly".

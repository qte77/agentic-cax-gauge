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
  `polyfetch_scrape.render_session`, verifying the invalid-STL failure path the plan's §9.2
  design depends on.
- **Problem**: Plan §9.2 says an uncaught page exception "always fires" `pageerror`. Four
  isolated test pages (a synchronous top-level throw in a classic `<script>`, the same in a
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

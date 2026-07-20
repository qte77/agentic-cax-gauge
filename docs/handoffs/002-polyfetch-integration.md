---
title: Handoff — polyfetch-scrape integration and upstream asks
purpose: Onboard the next session to plan 002
created: 2026-07-20
updated: 2026-07-20
plan: ../plans/002-polyfetch-integration.md
---

# Handoff 002

Companion to [handoff 001](001-v0-scoping.md), which remains the primary onboarding
document. Read that first. This one covers only the `polyfetch-scrape` dependency.

## State

Findings verified and recorded in [`plan 002`](../plans/002-polyfetch-integration.md).
Upstream contact made 2026-07-20 (plan 002 §6): consumer comment on
[#144](https://github.com/qte77/polyfetch-scrape/issues/144), docs issue
[#180](https://github.com/qte77/polyfetch-scrape/issues/180), SSRF scope issue
[#181](https://github.com/qte77/polyfetch-scrape/issues/181). **No code written.**

**Check #144 for a reply before implementing P5** — it asks whether E2E UI testing of
one's own app is in scope for polyfetch. A "no" means plan 001 §5.1's render substrate
needs rethinking. P1-P4 are unaffected either way, so this does not block starting.

## The three things that matter

1. **Use `localhost`, not `127.0.0.1`, for the viewer URL.** polyfetch's SSRF guard is
   literal-IP only: `localhost` passes, `127.0.0.1` raises, same destination. Verified by
   reading `_ssrf.py` directly. This will waste an hour if rediscovered.
2. **Never assert three.js state via `page.evaluate`.** Patchright's isolated world makes
   page-script globals read `undefined` even when rendering succeeded. Screenshots are
   ground truth. This is the single highest-cost trap in the integration.
3. **#144 upstream already tracks a reusable headless ui-check helper.** Comment there as
   a consumer; do not file a duplicate issue.

## How to proceed

Plan 002 §6 has the ordered action list. Shape of it: comment on #144 first (highest
value, zero duplication), then the small docs issue, then the SSRF scope discussion
worded as ceiling-raising rather than bug-reporting — it is a documented design decision,
not an oversight, and framing it wrong is needlessly adversarial toward an estate repo.

## Open question worth resolving early

Plan 002 §5, item C: **is E2E UI testing of your own app in scope for polyfetch at all?**
Its README positions it as a scraping toolkit. If the answer is no, P5's render substrate
is built on an unsupported surface and should be reconsidered before implementation, not
after. Cheap to ask, expensive to assume.

## Unverified inference — confirm at P5

Plan 002 §2 infers from `docs/architecture.md`'s component table that `check_ssrf` is not
wired into `client.py` or the backends, so a direct `fetch()` against a local viewer is
probably never guard-checked. That is inference from a doc table, not from reading
`client.py`. Confirm empirically before relying on it.

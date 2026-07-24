# Docs map

No code exists yet. These docs are the project. There are four of them.

| Document | Status | Use it for |
|---|---|---|
| [`../README.md`](../README.md) | Live | What this is and why, in one screen |
| [`plans/001-v0.md`](plans/001-v0.md) | **Live** | The plan of record, split by lifetime. **Part I (§1-§5)** = goal, locked decisions, approach, architecture, roadmap. **Part II (§6-§12)** = executable detail, substrate traps, tests, reuse, risks |
| [`handoffs/001-v0.md`](handoffs/001-v0.md) | **Live** | Where things stand, build order, non-negotiables, traps, owner gates. Read this to start working |
| [`reference/landscape.md`](reference/landscape.md) | Reference | Research evidence, competitors, backend choice, contribution stance. Dated 2026-07-20; not needed to build |

## Start here

To **understand the project** — about 6 minutes, and you are done:

1. [`../README.md`](../README.md) — the pitch, one screen.
2. [`plans/001-v0.md`](plans/001-v0.md) **Part I** — stop at the divider. Within it, §3.1 is
   the distilled red-team: it killed the original "spec as authoritative oracle" design and
   everything else is downstream of it. If you read one section, read that one.

To **build**, continue: [`handoffs/001-v0.md`](handoffs/001-v0.md) for current state, then
plan Part II for the milestone you are on. Start on M1.

## Conventions

- **One arc, one pair.** A plan (`plans/NNNN-slug.md`) and its handoff
  (`handoffs/NNNN-slug.md`) share a number. The plan is the *what*; the handoff is the
  *where we are*. A handoff without its plan, or a plan without its handoff, is a bug.
- **A new number means work shipped**, not "time passed" or "a new document got written".
  Closing an arc migrates the remainder forward — work is never stranded.
- **Superseded documents are deleted, not archived in place.** A stale doc that still reads
  as authoritative is worse than a missing one. Git history is the archive.
- Frontmatter carries `status` and `validated_links`. Reference-style links only, no bare
  URLs in prose.

## Removed, and where to find it

Consolidated 2026-07-23. Plans 002 and 003 and handoffs 001-003 were folded into the single
`001-v0` pair — they described the same unstarted v0, split by when they were written rather
than by what shipped. All recoverable from git history:

| Was | Now | Recover with |
|---|---|---|
| `reviews/001-wedge-red-team.md` | `plans/001-v0.md` §3.1 — bedrock, Goodhart paths, WINS/LOSES-IFF | `git show 2731ae3:docs/reviews/001-wedge-red-team.md` |
| `plans/002-polyfetch-integration.md` | `plans/001-v0.md` §9 — substrate, SSRF finding, upstream issue status | `git show f3a84b0:docs/plans/002-polyfetch-integration.md` |
| `plans/003-scaffold-and-preflight.md` | `plans/001-v0.md` §6-§7 — scaffold table, gate modules, fixtures | `git show f3a84b0:docs/plans/003-scaffold-and-preflight.md` |
| `handoffs/001`, `002`, `003` | `handoffs/001-v0.md` | `git show f3a84b0:docs/handoffs/<name>.md` |
| `plans/001` §6 landscape, §12 contribution stance | `reference/landscape.md`, with post-red-team verdicts corrected | — |

Compressed 2026-07-24 to cut onboarding cost: the plan was one 502-line file mixing durable
*why* with volatile *how to build it*, so a newcomer could not tell what they had to read.
It is now split at a divider into Part I (understand) and Part II (build), and content git
already archives was dropped rather than restated:

| Was | Now | Recover with |
|---|---|---|
| §10 code map (standalone) | Merged into §4 as the projected file layout — architecture in one place | — |
| §12 verification strategy, §13 risks | Renumbered §10, §11 — no content change | — |
| §9.3 upstream issue log (5-row status table) | §9, three sentences: the open question, why it does not block M2, two issue links | `git show c9c5d1a:docs/plans/001-v0.md` |
| §14.1 annotation backends, §14.2 tech stack, §14.3 contribution stance | §5 outlook row (VLM), §6 scaffold table (stack), `reference/landscape.md` §4 (stance) | `git show c9c5d1a:docs/plans/001-v0.md` |
| §11 estate-reuse 3-column table | §11, 2 columns — need + source, prose folded in | `git show c9c5d1a:docs/plans/001-v0.md` |

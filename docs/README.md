# Docs map

No code exists yet. These docs are the project. There are five of them — two are reference
material you do not need to build.

| Document | Status | Use it for |
|---|---|---|
| [`../README.md`](../README.md) | Live | What this is and why, in one screen |
| [`plans/001-v0.md`](plans/001-v0.md) | **Live** | The plan of record, split by lifetime. **Part I (§1-§5)** = goal, locked decisions, approach, architecture, roadmap. **Part II (§6-§12)** = executable detail, substrate traps, tests, reuse, risks |
| [`handoffs/001-v0.md`](handoffs/001-v0.md) | **Live** | Where things stand, build order, non-negotiables, traps, owner gates. Read this to start working |
| [`reference/landscape.md`](reference/landscape.md) | Reference | Research evidence, competitors, backend choice, contribution stance. Re-swept 2026-07-25; not needed to build |
| [`reference/cae.md`](reference/cae.md) | Reference | The owed CAE research. Read §1 before touching `verify/sim.py` — it disproved the plan's own reason for reserving that seam. Not needed to build v0 |

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

Superseded docs are deleted, not archived — this table is just the index back into git. It
lists **deleted files and relocated content only.** Renumbering and compression *within* a
live doc are not tracked: the current section is the answer, and git has the rest.

| Was | Now | Recover with |
|---|---|---|
| `reviews/001-wedge-red-team.md` | `plans/001-v0.md` §3.1 | `git show 2731ae3:docs/reviews/001-wedge-red-team.md` |
| `plans/002-polyfetch-integration.md` | `plans/001-v0.md` §9 | `git show f3a84b0:docs/plans/002-polyfetch-integration.md` |
| `plans/003-scaffold-and-preflight.md` | `plans/001-v0.md` §6-§7 | `git show f3a84b0:docs/plans/003-scaffold-and-preflight.md` |
| `handoffs/001`, `002`, `003` | `handoffs/001-v0.md` | `git show f3a84b0:docs/handoffs/<name>.md` |
| `plans/001` landscape + contribution stance | `reference/landscape.md` | — |
| `plans/001` upstream issue log, deferred-design essays | `plans/001-v0.md` §9 · §5 and §6 · `reference/landscape.md` §4 | `git show c9c5d1a:docs/plans/001-v0.md` |

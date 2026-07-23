# Docs map

No code exists yet. These docs are the project. There are four of them.

| Document | Status | Use it for |
|---|---|---|
| [`plans/001-v0.md`](plans/001-v0.md) | **Live** | The plan of record. Design, why it looks like this (§3.1), the three v0 milestones, executable detail, substrate constraints, risks |
| [`handoffs/001-v0.md`](handoffs/001-v0.md) | **Live** | Where things stand, build order, non-negotiables, traps, owner gates. Read this to start working |
| [`reference/landscape.md`](reference/landscape.md) | Reference | Research evidence, competitors, backend choice, contribution stance. Dated 2026-07-20; not needed to build |
| [`../README.md`](../README.md) | Live | What this is and why, in one screen |

## Start here

1. [`../README.md`](../README.md) — the pitch, one screen.
2. [`plans/001-v0.md`](plans/001-v0.md) **§3.1** — the distilled red-team. It killed the
   original "spec as authoritative oracle" design; everything else is downstream of it. If
   you read one section, read this one.
3. [`handoffs/001-v0.md`](handoffs/001-v0.md) — then start on M1.

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

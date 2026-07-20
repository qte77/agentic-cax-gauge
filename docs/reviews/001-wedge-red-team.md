---
title: Wedge red-team — adversarial distillation of the DesignSpec + gate-ordering claim
purpose: Record the kill review of the core differentiator, the surviving bedrock, and the kill conditions — a diagnosis for a human pivot decision, not an executed pivot
created: 2026-07-20
updated: 2026-07-20
validated_links: 2026-07-20
status: KILL-as-scoped — reframe recommended, human decision pending
---

**Status**: The wedge as scoped in [`../plans/001-v0-scoping.md`](../plans/001-v0-scoping.md)
**does not survive** independent red-team. This is a diagnosis. No approach has been
rewritten off the back of it — that is the human's call (§ Decision).

Method: adversarial first-principles distillation, lightweight path. Distill done inline;
kill case run by an **independent** agent (separate context — did not see the distillation).
Calibrated for an estate/internal tool: moat/TAM cuts voided; only frame-independent cuts
(correctness, Goodhart, ROI, rot, cold-start, real-defect coverage) applied.

## The claim tested

1. A pre-declared, machine-checkable `DesignSpec` authored **before** generation and
   **independent** of the generating agent.
2. Deterministic geometry checks **authoritative**; bounded VLM render-critique strictly
   **secondary**, never overriding a deterministic failure.

## Bedrock — what survives total concession

Tagged by why it survives (frame-independent value, not moat):

- **[CORRECTNESS, narrow]** Deterministic checks are real and trustworthy for **global,
  static, foreseen** properties: build-succeeds, manifold/watertight, overall envelope,
  gross mass/volume, and *foreseen* pairwise clearances + FDM overhang. Notably this
  catches **silent feature loss in boolean fusion** (feature absorbed during fusion, still
  reports manifold=true, volume within a loose band) — a genuinely valuable, otherwise-
  invisible failure.
- **[CORRECTNESS, conditional]** A pre-declared spec has real value in exactly two modes:
  **regression across many regenerations** (re-run after a kernel/model upgrade; a
  component reused across many parts), and **offloading arithmetic humans eyeball badly**
  (tight clearance stacks, mass).

### What did NOT survive, and why

- **Full-taxonomy defect coverage — FALSE.** Realistic catch rate against the project's own
  example defects is roughly one third, and only for defects the author **named in
  advance**. The dominant defect category in agent-generated CAD is *local, unforeseen,
  sequential, or fidelity* — gusset overlapping a hole, a through-hole that isn't through,
  datum-offset mating feature, assembly-sequence blockage. Bbox/volume/manifold are
  structurally **blind** to all of these (mass and envelope unchanged). Catching them needs
  a *named per-feature* assertion, which requires already knowing where the bug will be —
  circular.
- **Independence — FICTION as normally deployed.** Same LLM authoring spec + generating code
  shares blind spots (correlated failure, not independent). Same human in one sitting: a
  rushed spec has the same holes a rushed review would. Pre-declaration buys real
  independence only in the regression/arithmetic modes above.
- **Deterministic-authoritative / VLM-subordinate ordering — BACKWARDS for the dominant
  defect class.** Because the deterministic gate is blind to most real defects,
  subordinating the one signal that might surface them (the visual render) to a blind gate
  is inverted. Worse, **revert-on-break selects for gaming**: a numerically-safe hack that
  dodges a check survives; an honest fix that risks a deterministic regression gets
  discarded. Optimizing against an imperfect reward with a hard reset on the honest-fix path
  predictably converges on green-but-broken.
- **"Green gauge" is worse than "no gauge" when framed as sufficient.** It licenses skipping
  the ten-second render glance for exactly the defects it cannot see — converting a
  would-have-been-caught defect into a false-confidence pass.

### Goodhart paths (concrete)

- **One-sided clearance.** "clearance ≥ min" with no upper bound: shrink a part 0.5 mm
  everywhere → passes clearance, stays in bbox, ruins a press/snap fit.
- **Deletion beats repair.** Negative constraints are cheapest satisfied by removing the
  offending feature (delete the gusset) → manifold/bbox pass, weaker part scores greener.
- **Mass band rewards hollowing/filling** to land in-band regardless of intent.

## Load-bearing bet (the #1 failing point)

That a machine-checkable spec expresses enough of "this part is correct" to be **trusted**.
It does not, as scoped: the checkable assertions are a weak proxy for usable-part, the proxy
is gameable, and pre-declaration by the same intelligence doesn't manufacture independence.
Time window is irrelevant here — this is a logic failure, not a market-timing one.

## ICP — where the surviving truth is real

Not "any agent-generated part." The one profile the value holds for: **a part regenerated
many times against a stable, small acceptance contract** — e.g. an estate labware/carriage
component re-run after a build123d/OCCT bump, or a fixture reused across many assemblies.
There, a cheap pre-declared assert (envelope, mass, a couple of genuinely-mated clearances)
amortizes and catches real regressions. For a one-shot generate-a-bracket, the render glance
dominates.

## Recommended reframe (a recommendation, not an executed pivot)

The honest alternative that dominates while consumer count is small and parts are
prototype-scale:

1. **Cheap non-negotiable preflight** — build-succeeds + manifold/watertight + bbox + mass.
   Keep. Catches silent-fusion loss. This is the incumbent baseline plus watertight-as-gate.
2. **Auto-generated fast multi-view render as the PRIMARY human gate** — invert the
   ordering. This is the real gate for the blind-spot defects, and it reuses the
   `polyfetch` substrate already speced in plan 001 §5.1. Make it automatic and fast.
3. **VLM critique as an assist that draws the human's eye**, not an authority and not a
   bounded loop that selects for gaming. Consistent with the BLINK/VSI-Bench finding that
   the VLM can't be trusted as a judge — so it advises, the human decides.
4. **Add deterministic checks reactively**, per the estate compound-learning rule (2nd/3rd
   recurrence), not a speculative tolerance/manufacturability DSL up front.
5. **`DesignSpec` survives only in regression framing** — small, reused across many
   regenerations, green explicitly documented as *necessary, not sufficient*.
6. **Fix the one-sided-clearance hole** — clearances are fit *windows* (min AND max), never
   min-only.

This also dissolves most of the differentiation claim — which is fine under the already-
locked estate-first positioning (we are not competing with text-to-cad; plan 001 §2).

## Wins-iff / Loses-iff — kill conditions to watch

**WINS IFF**: the spec stays small/cheap and is **reused across many regenerations**
(regression framing, not one-shot oracle); green is documented as necessary-not-sufficient
and never substitutes for viewing the render; new checks are added reactively after a real
recurring defect; clearances are two-sided windows; tolerance bands stay loose enough (with
an owner) to survive OCCT/build123d/slicer drift.

**LOSES IFF**: the spec is written once by the same intelligence that generates, and framed
as a substitute for looking at the part; coverage is claimed as broad correctness rather
than a narrow static-property check; effort goes into a general tolerance/manufacturability
DSL for two hobby-scale consumers, and the spec rots to a bbox+volume stub no better than
the incumbent; clearance stays min-only; or tight bands throw false failures across kernel
bumps nobody maintains, so the gate is quietly disabled while still implying verification.

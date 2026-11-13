# Review rubric: accept, reject or unsure

One rubric for every human judgement in this repo: the benchmark labels
(`bench/labels-blind.csv`, `bench/labels.csv`) and the M3 defect table
(`bench/m3-review.csv`). Fix it **before** labelling. Labels made without a fixed rubric can't
be compared later, and neither can an agreement statistic between two raters.

The gauge's checks are necessary, not sufficient. This rubric covers what they can't see.
Draft 2026-11-13. The first four reason codes come from the four defects the owner found in
the so101 pipette mount (plan §5, M2 row); the rest are the obvious companions. Change it only
between labelling rounds, never during one.

## The verdict

| Value | Means |
|---|---|
| `yes` | Accept: you'd use this part for what the brief (or the design source) says it is for. Nothing below applies. |
| `no` | Reject: at least one reason code below applies. Record every code that does. |
| `unsure` | The evidence in front of you can't settle it, e.g. an internal feature hidden in all four views. Say what you'd need (`needs: source`, `needs: section view`). |

`unsure` is a real answer, not a skip. The blind sheet hides the design source so the tool
stays hidden, but three of the four pipette-mount defects were only visible by reading the
source beside the views. Counting those cases as `yes` would turn "looked fine from outside"
into "accepted".

## Reason codes

| Code | The part… | Pipette-mount example |
|---|---|---|
| `phantom-feature` | claims a feature the geometry doesn't have: a cut that removes nothing, a hole that doesn't go through, a fillet that isn't there | The ejector cutout lies inside the empty bore, so it removes no material |
| `mechanism` | has a mechanism that can't work as intended: a fastener that can't close its joint, a hook that can't catch, a hinge that can't turn | The clamp screws run parallel to the split, so they can't tighten it |
| `load-path` | has pieces meant to act as one that are joined weakly or only through an unintended path | The clamp halves are held only by the base plate |
| `interface` | lacks what's needed to attach to its mating part: mounting holes, a bolt pattern, a locating feature | The mounting plate has no bolt holes |
| `dimension` | is grossly off from the stated size or proportion, beyond what the bounds already check | — |
| `printability` | can't be made by the stated process: an unsupported overhang, a wall below the nozzle width, a trapped volume | — |
| `other` | is wrong for a reason not listed. Describe it in a few words, and add a code next round if it recurs | — |

## Writing it down

- Blind sheet: `accept` is `yes`, `no` or `unsure`. `reject_reason` holds the codes, separated
  by `;`, then optional words, e.g. `mechanism; screws parallel to split`. For `unsure`, give
  what you'd need, e.g. `needs: source`.
- M3 table: put the codes and a short description in `defects`. Fill
  `intent_view_would_help` and `section_view_would_help` with `yes` or `no` for each part.
  Those two columns decide whether `--intent` and a section view get built.

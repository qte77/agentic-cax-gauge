# Verification Honesty

**Day-one guardrail for this project.** Encodes the kill conditions of the distilled
red-team (`docs/plans/001-v0.md` §3.1). Weakening any rule below turns the gauge into a
false-confidence instrument — worse than no gauge (plan §3.1, §12.7).

- **Green is necessary, not sufficient.** Label every passing check that way.
- **Never emit a "verified/correct" verdict from deterministic checks alone.** The word
  "verified" does not appear in a report.
- **The VLM annotates and never gates.** "No model configured" is a first-class mode.
- **No bounded auto-critique loop with revert-on-break.** It selects for gaming.
- **Clearances are two-sided windows, never min-only.**
- **An unsupplied bound reports `SKIP`, never `PASS`.** A check with no bound has checked
  nothing, and must not count toward green.

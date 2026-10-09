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

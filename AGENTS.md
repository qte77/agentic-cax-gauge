# Agent Instructions for agentic-cax-gauge

Behavioral rules for AI agents working on this verification harness for agent-generated CAx.
For technical workflows and coding standards, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Core Rules

- Follow SDLC principles: maintainability, modularity, reusability
- **Strict TDD, behavior-level, no Gherkin/BDD** (plan §2) — write the failing test first
- **Never assume missing context** — ask if uncertain about requirements
- **Never hallucinate libraries** — only use packages verified in `pyproject.toml`
- **Always confirm file paths exist** before referencing in code or tests
- **Never delete existing code** unless explicitly instructed
- **Document new patterns** in AGENT_LEARNINGS.md (concise, laser-focused)
- **Request human feedback** in AGENT_REQUESTS.md when blocked
- **Verification honesty is non-negotiable** — see `.claude/rules/verification-honesty.md`

## Architecture Overview

The plan of record is [docs/plans/001-v0.md](docs/plans/001-v0.md) (AUTHORITY). It opens
with a Handoff section — read that first. Architecture is plan §4; the file/source map is
§6-§8 and §11.

- **Cheap deterministic preflight** — necessary, not sufficient
- **Auto multi-view render** — the primary gate; a human decides
- **VLM** — advisory only, never gates, deferred out of v0

## Decision Framework

**Priority order:** User instructions → AGENTS.md → CONTRIBUTING.md → project patterns

**Information sources:**

- Requirements/scope: task description or user instruction (primary)
- Design, milestones, decisions: [docs/plans/001-v0.md](docs/plans/001-v0.md) (AUTHORITY)
- Research evidence: [docs/reference/](docs/reference/) (informational, not needed to build)
- Implementation detail: `src/` code (reference, not authority)

**Anti-scope-creep:** Only implement what is explicitly requested. Nothing in the plan's
Outlook starts without its stated trigger.

## Quality Thresholds

Before starting any task:

- **Context**: 8/10 — understand requirements, plan section, codebase patterns
- **Clarity**: 7/10 — clear implementation path and expected outcomes
- **Alignment**: 8/10 — follows the plan and the verification-honesty rule
- **Success**: 7/10 — confident in completing task correctly

If below threshold: gather more context or escalate to AGENT_REQUESTS.md.

## Agent Quick Reference

**Pre-task:**

- Read AGENTS.md → plan Handoff → CONTRIBUTING.md
- Confirm quality thresholds met
- Check AGENT_LEARNINGS.md for prior art

**During task:**

- Use `make` commands (document deviations)
- TDD: write the failing test first, then the minimal implementation
- Tag tool-dependent tests `@pytest.mark.cad` / `@pytest.mark.browser`

**Post-task:**

- Run `make validate` — must pass all checks
- Update CHANGELOG.md for non-trivial changes
- Strike the shipped row in the plan's remaining-work table in the same PR
- Document new patterns in AGENT_LEARNINGS.md
- Escalate to AGENT_REQUESTS.md if blocked

# How Agents Use Our Specs

**Last Updated:** 2025-10-20
**Audience:** Developers using Claude Code

## Quick Start

1. Specs live in code (`docs/specs/`, `docs/adr/`).
2. Agents discover specs automatically (via Claude Skills or by search).
3. Tests derive from specs (Given/When/Then → unit/integration).
4. CI enforces compliance (spec‑lint, adr‑check).

## The Spec Stack

USER PROBLEM → PRD → DESIGN DOC → ADR → TEST PLAN → CODE + TESTS → RUNBOOK

Agents read this stack to understand context, constraints, and contracts. Always reference IDs (e.g., `PRD-101`, `DESIGN-101`, `ADR-009`, `TEST-101`).

## Working Pattern

- For a new feature: write `PRD-XXX` + `TEST-XXX`, then “Implement per TEST-XXX”.
- For architectural change: open `ADR-XXX` first.
- For bugfix: add failing test with `TC-XXX` comment, then fix.

## Agent Prompts

- “Read CLAUDE.md and DESIGN-201. Implement API per TEST-201.”
- “Run spec-lint and list blockers.”
- “Propose ADR for switching cache to Redis with tradeoffs.”

## Using Superpowers (optional but recommended)

If installed via marketplace, Superpowers provides planning-first workflows, TDD loops, and subagent dispatch.
Ask: “Use Superpowers to plan and implement feature X; open ADR if architecture changes.”

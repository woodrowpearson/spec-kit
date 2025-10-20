# Agentic Spec System for iOS + Full‑Stack

**Version:** 1.0.0
**Last Updated:** 2025-10-20
**License:** MIT

An opinionated, evidence‑backed specification system optimized for agentic coding with Claude Code.

## What's Inside

- Templates (PRD, DESIGN, SDD, ADR, TEST PLAN, RUNBOOK)
- Checklists (spec review, ADR review, iOS accessibility, CI gates)
- Spec Linter skill for Claude Code
- Python scripts and GitHub Actions
- CLAUDE.md guide

## Quick Start

```bash
cp -r spec-kit/TEMPLATES docs/templates
cp -r spec-kit/.github/workflows .github/
cp -r spec-kit/scripts scripts/
cp spec-kit/CLAUDE.md .
```

Then: add your first PRD + Test Plan and run `python3 scripts/lint-specs.py`.

## Evidence & Inspirations

- Google design docs & SWE Book
- Nygard ADRs
- Gojko Adžić – Specification by Example
- Simon Willison – Vibe engineering
- Peter Steinberger – Agentic workflows
- Anthropic – Claude Code, Skills & MCP

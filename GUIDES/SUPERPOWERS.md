---
title: Installing & Governing Superpowers for Claude Code
version: 1.0
last_updated: 2025-10-20
owners: [eng-enablement@your-org.example]
---

# Superpowers for Claude Code – Integration Guide

This guide shows how to install, pin, and govern **Superpowers** (obra/superpowers) with our Spec Kit.

> Summary: Superpowers provides a bootstrap + a curated set of Skills and slash commands that teach Claude Code to plan-first, run TDD, dispatch subagents, and manage parallel worktrees.

## 1) Prerequisites
- Claude Code ≥ 2.0.13
- Code execution enabled
- Our **PLUGINS governance** in place (see `GUIDES/PLUGINS.md`)
- GitHub CLI (`gh`) optional but recommended

## 2) Install from the Marketplace
Run in Claude Code:
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```
Quit and restart `claude`.

## 3) Verify load
Use:
```
/plugins list
/skills list
```
You should see Superpowers commands and Skills registered.

## 4) Pin the version
Add an inventory entry to `PLUGINS.yaml` (see sample below) with the source `marketplace`, version tag, owners, scopes, and review date.

## 5) Configure policy
- Keep Superpowers **scoped** to non‑prod repos until approved.
- Require **spec‑lint** & **feature‑AC** checks to stay enabled.
- If Superpowers attempts architectural changes, an **ADR** is mandatory.

## 6) Updates & rollback
- To update:
```
/plugin update superpowers
```
- To rollback: uninstall, then re‑install a prior pinned version (document in `PLUGINS.yaml` history).

## 7) Troubleshooting
- If commands appear but autonomous skill use fails, restart and check Skills format compatibility.
- Inspect `claude --debug` logs for “Loaded commands” and “Loaded skills” lines.
- File issues upstream and cross‑link them in our inventory entry.

## 8) Minimal acceptance tests (run after install)
- **TDD loop:** Ask Claude to create a failing test, then implement just enough code to pass.
- **Parallel worktree:** Begin a feature while main remains open; ensure no clobbering.
- **Subagent dispatch:** Confirm task fan‑out and synthesized review.

---

# Inventory entry example (copy into PLUGINS.yaml)
```yaml
- name: superpowers
  source: marketplace
  repo: obra/superpowers-marketplace
  version: 2025-10-12          # example tag or semantic version if available
  owners: ["eng-enablement@your-org.example"]
  scopes:
    - "read:repo"
    - "execute:skills"
  environments: ["dev", "stage"]   # not prod until security sign-off
  status: "approved-with-guardrails"
  review_cycle: "quarterly"
  notes: >
    Bootstrap for Claude Code + curated Skills. Enforce ADRs for arch changes.
    Keep spec-lint and feature-AC checks required in CI.
```

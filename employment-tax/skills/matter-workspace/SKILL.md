---
name: matter-workspace
description: >
  Manage per-employer matter workspaces for payroll bureaus / multi-employer practices —
  create, list, switch, close, or turn off matters. Only relevant when you run payroll for more
  than one employer; a single-employer in-house function doesn't need it. Use for "new payroll tax matter",
  "switch payroll tax matter", "list payroll tax matters", "close payroll tax matter".
argument-hint: "new <slug> | list | switch <slug> | close <slug> | none"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# /matter-workspace

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/employment-tax/matters/<slug>/`.

## When this applies

Only when `## Matter workspaces` in the practice profile has `Enabled: ✓` (set at cold-start for a bureau / multi-employer practice). For a single-employer in-house function, matter workspaces are off and skills use practice-level context automatically — this skill isn't needed.

## Commands

- **`new <slug>`** — create a matter folder with a starter `matter.md` (employer name, PCB method, employee categories in use, contribution setup and any voluntary-rate elections, pay calendar, remittance/filing dates, any overrides to the practice-level conventions). Ask for the essentials; flag any rate/ceiling for verification.
- **`list`** — show employers with their pay frequency and last activity.
- **`switch <slug>`** — set the active employer. Subsequent skills read this matter's `matter.md` for employer-specific facts and the practice-level CLAUDE.md for conventions.
- **`close <slug>`** — archive the matter (retain the record); clear it as active if it was.
- **`none`** — work at practice level (no active employer).

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill working on employer A never reads employer B's files. Learnings meant to carry across employers go in the practice-level CLAUDE.md, not a matter folder.
- **The setup discipline.** A matter's `matter.md` records the employer's PCB method, contribution categories, and pay calendar **with the source of each** (the payroll setup, the contribution election). These are the figures the computations trust; they must be sourced, not assumed — a wrong contribution category on file produces wrong contributions every month.

## What this skill does NOT do
- Apply to a single-employer in-house function.
- Carry context across employers unless explicitly turned on.

## Close with a short confirmation of the new state.

---
name: matter-workspace
description: >
  Manage per-client matter workspaces for multi-client international-tax / TP practices —
  create, list, switch, close, or turn off matters. Only relevant for private practice;
  in-house single-group users don't need it. Use for "new matter", "switch matter",
  "list matters", "close matter".
argument-hint: "new <slug> | list | switch <slug> | close <slug> | none"
---

# /matter-workspace

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/international-tax/matters/<slug>/`.

## When this applies

Only when `## Matter workspaces` in the practice profile has `Enabled: ✓` (set at cold-start for private practice). For in-house teams working one group, matter workspaces are off and skills use practice-level context.

## Commands

- **`new <slug>`** — create a matter folder with a starter `matter.md`: the client group's structure, jurisdictions, controlled-transaction inventory (sourced), treaties in play, and CbCR/Pillar Two status (each flagged for verification). Overrides to practice-level conventions go here.
- **`list`** — matters with the client group and last activity.
- **`switch <slug>`** — set active; subsequent skills read its `matter.md` for the group facts and the practice-level CLAUDE.md for conventions.
- **`close <slug>`** — archive (retain the record — TP positions recur year to year); clear active if it was.
- **`none`** — practice level.

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill in matter A never reads matter B.
- **No comparables in the matter file.** A matter records the group, the transactions, and the methods — not benchmarking results, which live in the study and are re-run for currency.

## What this skill does NOT do
- Apply to in-house single-group setups.
- Carry context across matters unless turned on.

## Close with a short confirmation of the new state.

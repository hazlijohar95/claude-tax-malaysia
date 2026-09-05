---
name: matter-workspace
description: >
  Manage per-client / per-entity matter workspaces for multi-client tax practices —
  create, list, switch, close, or turn off matters. Only relevant for private practice;
  in-house single-entity users don't need it. Use for "new matter", "switch matter",
  "list matters", "close matter".
argument-hint: "new <slug> | list | switch <slug> | close <slug> | none"
---

# /matter-workspace

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/corporate-tax/matters/<slug>/`.

## When this applies

Only when `## Matter workspaces` in the practice profile has `Enabled: ✓` (set at cold-start for private practice). For in-house users with one entity or one group, matter workspaces are off and skills use practice-level context automatically — this skill isn't needed.

## Commands

- **`new <slug>`** — create a matter folder with a starter `matter.md` (entity name, period end, YA, tax profile, opening carried-forward balances and their source, any overrides to the practice-level conventions). Ask for the essentials; flag any rate/balance for verification.
- **`list`** — show matters with their active YA and last activity.
- **`switch <slug>`** — set the active matter. Subsequent skills read this matter's `matter.md` for entity-specific facts and the practice-level CLAUDE.md for conventions.
- **`close <slug>`** — archive the matter (retain the record); clear it as active if it was.
- **`none`** — work at practice level (no active matter).

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill working in matter A never reads matter B's files. Learnings meant to carry across matters go in the practice-level CLAUDE.md, not a matter folder.
- **The opening-balance discipline.** A matter's `matter.md` records brought-forward losses, unabsorbed CA, and residual expenditure **with the source of each** (the agreed assessment or prior filed return). These are the figures the computation trusts; they must be sourced, not asserted.

## What this skill does NOT do
- Apply to in-house single-entity setups.
- Carry context across matters unless explicitly turned on.

## Close with a short confirmation of the new state.

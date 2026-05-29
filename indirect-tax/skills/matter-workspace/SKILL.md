---
name: matter-workspace
description: >
  Manage per-client / per-entity matter workspaces for multi-client SST practices —
  create, list, switch, close, or turn off matters. Only relevant for private practice;
  in-house single-entity users don't need it. Use for "new matter", "switch matter",
  "list matters", "close matter".
argument-hint: "new <slug> | list | switch <slug> | close <slug> | none"
---

# /matter-workspace

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/indirect-tax/matters/<slug>/`.

## When this applies

Only when `## Matter workspaces` in the practice profile has `Enabled: ✓` (set at cold-start for private practice). For in-house single-entity users, matter workspaces are off and skills use practice-level context automatically.

## Commands

- **`new <slug>`** — create a matter folder with a starter `matter.md`: client/entity name, SST registration status and groups, taxable period, recorded taxability positions and exemptions specific to this client (with their basis and source), and any overrides to the practice-level positions. Flag any rate/group/threshold for verification.
- **`list`** — show matters with registration status and last activity.
- **`switch <slug>`** — set the active matter; subsequent skills read its `matter.md` for client-specific facts and the practice-level CLAUDE.md for conventions.
- **`close <slug>`** — archive (retain the record); clear active if it was.
- **`none`** — work at practice level.

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill in matter A never reads matter B. Cross-matter learnings go in the practice-level CLAUDE.md.
- **Position provenance.** A matter's recorded taxability positions and exemptions carry their basis and source — they are confirmed views, not assumptions to be reused blindly across clients with different facts.

## What this skill does NOT do
- Apply to in-house single-entity setups. - Carry context across matters unless turned on.

## Close with a short confirmation of the new state.

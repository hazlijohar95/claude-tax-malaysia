---
name: matter-workspace
description: >
  Manage per-taxpayer matter workspaces for multi-client individual tax practices —
  create, list, switch, close, or turn off matters. Only relevant for private practice;
  an individual doing their own one return doesn't need it. Use for "new matter",
  "switch matter", "list matters", "close matter".
argument-hint: "new <slug> | list | switch <slug> | close <slug> | none"
---

# /matter-workspace

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/personal-tax/matters/<slug>/`.

## When this applies

Only when `## Matter workspaces` in the practice profile has `Enabled: ✓` (set at cold-start for private practice). For an individual preparing their own return, matter workspaces are off and skills use practice-level context automatically — this skill isn't needed.

## Commands

- **`new <slug>`** — create a matter folder with a starter `matter.md` (taxpayer name, YA, residence basis and how it's established, which form applies, income sources, opening brought-forward balances for a Form B and their source, any overrides to the practice-level conventions). Ask for the essentials; flag any rate/cap/balance for verification.
- **`list`** — show matters with their active YA and last activity.
- **`switch <slug>`** — set the active matter. Subsequent skills read this matter's `matter.md` for taxpayer-specific facts and the practice-level CLAUDE.md for conventions.
- **`close <slug>`** — archive the matter (retain the record); clear it as active if it was.
- **`none`** — work at practice level (no active matter).

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill working in matter A never reads matter B's files. Learnings meant to carry across matters go in the practice-level CLAUDE.md, not a matter folder.
- **The opening-balance discipline.** A matter's `matter.md` records brought-forward business losses and unabsorbed CA (Form B) **with the source of each** (the agreed assessment or prior filed return), and the residence conclusion for the YA. These are the figures the computation trusts; they must be sourced, not asserted.

## What this skill does NOT do
- Apply to an individual doing their own single return. - Carry context across matters unless explicitly turned on.

## Close with a short confirmation of the new state.

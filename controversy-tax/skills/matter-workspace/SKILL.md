---
name: matter-workspace
description: >
  Manage controversy matter workspaces — create, list, switch, close, or turn off matters.
  Controversy work is matter-centric, so this is on by default. Use for "switch tax dispute matter",
  "list tax dispute matters", "close tax dispute matter", "work at practice level".
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

Manages matter workspaces under `~/.claude/plugins/config/claude-for-tax/controversy-tax/matters/<slug>/`.

## When this applies

Matter workspaces are ON by default for this plugin — each audit or dispute is a matter. An in-house team with a single ongoing dispute simply has one matter.

## Commands

- **`new <slug>`** — create a matter folder. For a full opening (deadline first, facts sourced, assessor's basis), prefer `/controversy-tax:matter-intake`, which this command points to. `new` alone creates the folder and an empty `matter.md` / `history.md` skeleton.
- **`list`** — show matters with taxpayer, body, stage, controlling deadline, and last activity.
- **`switch <slug>`** — set the active matter; subsequent skills read its `matter.md` and `history.md`.
- **`close <slug>`** — archive (retain the full record — disputes can reopen); clear active if it was.
- **`none`** — work at practice level (rare here; most work is in a matter).

## Rules

- **Isolation.** With `Cross-matter context: off` (default), a skill in matter A never reads matter B — except `portfolio-status`, which reads across read-only to build the rollup.
- **Deadlines live in the matter.** A matter's `matter.md` carries its controlling deadline (flagged for verification); `history.md` is append-only. Closing a matter retains both.

## What this skill does NOT do
- Open a matter properly (use `/controversy-tax:matter-intake` — it captures the deadline first).
- Delete a matter's history.

## Close with a short confirmation of the new state.

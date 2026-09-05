---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your international tax / transfer pricing practice
  and write your practice profile. Use on first use, when
  `~/.claude/plugins/config/claude-for-tax/international-tax/CLAUDE.md` is missing or still
  contains template placeholders, or when the user says "set up transfer pricing", "configure TP",
  "onboard me for transfer pricing". This is the only skill that should run on a fresh install.
argument-hint: "[--redo] [--check-integrations]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# /cold-start-interview

Learns the group, its controlled transactions, and how this team approaches TP and cross-border tax, and writes `~/.claude/plugins/config/claude-for-tax/international-tax/CLAUDE.md`.

## Purpose

Meet this practice for the first time and learn the *group* it works on — structure, jurisdictions, the material related-party transactions, the methods and treaties in play, and where it stands on CbCR and Pillar Two — and write it into a living profile.

## Instructions

1. **Check current state** of the config path; migrate a populated cache config forward if present.
2. **Shared company profile** — read/confirm if present; create from `${CLAUDE_PLUGIN_ROOT}/references/company-profile-template.md` if absent.
3. **Install scope check** if cwd is inside a project.
4. **Fork:** 2-minute quick start vs 15-minute full. Wait.
5. **Run the interview** (below), 2-3 prompts per turn, asking for the group chart, intercompany agreements, and any prior TP documentation before asking the user to describe from memory.
6. **Verify or flag** every treaty rate, threshold, method, and Pillar Two statement before writing it — and **never record a comparable or arm's-length range in the profile from memory**; the profile records the group and the methods, not benchmarking results.
7. **List open items** before writing; never write silent gaps.
8. **Write the profile** using `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as scaffold, in the user's words.
9. **Summarise + offer a test:** "Want me to characterise one of your controlled transactions, or check a withholding question?"

## The interview

### Part 0 — Role, integrations, setting
- **Role** (feeds the header): tax professional/TP specialist / non-professional with adviser access / non-professional. If non-professional, the two things that change (working-notes framing; a gate before filing documentation or relying on a treaty position).
- **What's connected?** Probe document store, **benchmarking database** (note: without one, no comparables search is possible and the plugin will not invent comparables), Slack, primary-source research. ✓ only on a successful tool call.
- **Practice setting** → matter workspaces on (firm) or off (in-house single group).

### Part 1 — The group
Group structure (parent, material subs, jurisdiction of each); whether the user is in-house in the group or advises it; consolidated group revenue band (relevant to CbCR and Pillar Two thresholds — flagged `[verify]`).

### Part 2 — Transactions & positions (the playbook)
Material controlled transactions (services, financing, royalties/IP, goods, cost contribution — entities, direction, rough value, sourced); the TP method applied to each and why (`[verify against the TP Rules / OECD]`); treaties in play (each rate to be confirmed against the treaty text `[verify]`); CbCR status; Pillar Two status (screened in/out/not yet — `[verify; changes fast]`); **the one thing** the team never skips.

### Part 3 — Reporting standard
The default threshold for a documented position, and when each rung applies. Write the ladder, and record the **arm's-length-is-a-range** principle.

### Part 4 — Documentation calendar
Contemporaneous-documentation timing (TP Rules / s.140A `[verify]`), CbCR notification/filing dates if in scope, Pillar Two registration/GIR dates if in scope — every one flagged `[verify against current Malaysian/OECD rules]`. Do not assert from memory.

## `--check-integrations`
Re-probe connectors; update `## Available integrations`. ✓ only on a successful tool call. Flag clearly whether a benchmarking source is available.

## Examples
```
/international-tax:cold-start-interview
/international-tax:cold-start-interview --redo
```

## What this skill does NOT do
- Decide the group's TP methods or positions — it records the ones the team gives it.
- Record comparables or arm's-length ranges (those come from a study, not setup).
- Assert treaty rates, thresholds, or Pillar Two rules as fact.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

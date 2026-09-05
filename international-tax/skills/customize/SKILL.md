---
name: customize
description: >
  Tune your international-tax / transfer pricing practice profile after setup — update the
  group structure, the controlled-transaction inventory, the TP methods applied, treaties in
  play, CbCR/Pillar Two status, or the reporting standard — without re-running the full
  cold-start interview. Use for "change my transfer pricing settings", "update the group", "customize transfer pricing".
argument-hint: "[what to change, in plain English]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# /customize

Targeted edits to `~/.claude/plugins/config/claude-for-tax/international-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If missing/all-placeholder, redirect to `/international-tax:cold-start-interview`.
2. **Locate the section:** `## Group & transactions profile`, `## Reporting standard`, `## Documentation calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a treaty rate, threshold, method position, or a Pillar Two/CbCR status, confirm it against a primary source or flag it `[verify]`. **Never write a comparable or an arm's-length range into the profile** — those come from a study, not configuration. A wrong treaty rate or Pillar Two date in the profile propagates everywhere.
4. **Show the diff** and confirm before writing.
5. **Write** the change, preserving the rest. Note which skills it affects.

## Examples
```
/international-tax:customize add an intercompany financing transaction (loan from parent in Singapore)
/international-tax:customize record that we screened in scope for Pillar Two for the group
/international-tax:customize set our default standard to "strong"
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start).
- Record comparables/ranges (those come from a study).
- Write unverified treaty rates or Pillar Two dates as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

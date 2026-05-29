---
name: customize
description: >
  Tune your employment-tax practice profile after setup — change a PCB convention, update a
  contribution category, add a benefit to the PCB-base list, fix a remittance deadline, or adjust
  house style — without re-running the full cold-start interview. Use for "change my settings",
  "update my conventions", "customize the plugin".
argument-hint: "[what to change, in plain English]"
---

# /customize

Targeted edits to `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If it's missing or all placeholders, redirect to `/employment-tax:cold-start-interview` — there's nothing to customize yet.
2. **Locate the section** the user's request maps to: `## PCB & contributions conventions`, `## Reporting standard`, `## Deadline calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a rate, ceiling, formula constant, category threshold, or deadline, apply the guardrail: confirm it against a primary source or flag it `[verify]` in the profile. Never write an unverified figure into the profile as if it were settled — the profile is read by every skill, so a wrong rate here propagates into every payroll run. **PCB constants and contribution rates change — record the band/category, flag the number.**
4. **Show the diff** — the before and after of the lines you'll change — and confirm before writing.
5. **Write** the change, preserving the rest of the file. Note in your reply which skills the change affects.

## Examples
```
/employment-tax:customize add "fixed phone allowance" to the benefits we include in the PCB base
/employment-tax:customize set our default reporting standard to "more likely than not"
/employment-tax:customize the PCB/CP39 remittance rule is the 15th of the following month
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start for that). - Write unverified rates/ceilings/dates as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

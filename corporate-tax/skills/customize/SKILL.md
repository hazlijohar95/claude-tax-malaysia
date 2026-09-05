---
name: customize
description: >
  Tune your corporate-tax practice profile after setup — change a convention, add an
  add-back to the standard checklist, update the reporting-standard threshold, fix a
  deadline rule, or adjust house style — without re-running the full cold-start
  interview. Use for "change my corporate tax settings", "update my corporate tax conventions", "customize corporate tax".
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

Targeted edits to `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If it's missing or all placeholders, redirect to `/corporate-tax:cold-start-interview` — there's nothing to customize yet.
2. **Locate the section** the user's request maps to: `## Computation conventions`, `## Reporting standard`, `## Deadline calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a rate, threshold, section number, or deadline, apply the guardrail: confirm it against a primary source or flag it `[verify]` in the profile. Never write an unverified figure into the profile as if it were settled — the profile is read by every skill, so a wrong fact here propagates everywhere.
4. **Show the diff** — the before and after of the lines you'll change — and confirm before writing.
5. **Write** the change, preserving the rest of the file. Note in your reply which skills the change affects.

## Examples
```
/corporate-tax:customize add "freight to bring asset to location" to the CA qualifying-expenditure note
/corporate-tax:customize set our default reporting standard to "strong"
/corporate-tax:customize the Form C deadline rule is 7 months after period end
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start for that).
- Write unverified rates/dates as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

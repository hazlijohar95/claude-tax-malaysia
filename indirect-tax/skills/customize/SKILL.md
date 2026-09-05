---
name: customize
description: >
  Tune your indirect-tax (SST) practice profile after setup — change a recorded
  taxability position, add an exemption you rely on, update registration status, fix the
  SST-02 calendar, or adjust the reporting standard — without re-running the full
  cold-start interview. Use for "change my settings", "update my SST positions", "customize the plugin".
argument-hint: "[what to change, in plain English]"
---

# /customize

Targeted edits to `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If missing/all-placeholder, redirect to `/indirect-tax:cold-start-interview`.
2. **Locate the section:** `## Registration profile`, `## Taxability positions`, `## Reporting standard`, `## SST return calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a rate, threshold, taxable-group classification, exemption, or deadline, confirm it against a primary source or flag it `[verify]` in the profile. Never write an unverified figure as settled — every skill reads this file, so a wrong fact propagates everywhere.
4. **Show the diff** and confirm before writing.
5. **Write** the change, preserving the rest. Note which skills it affects.

## Examples
```
/indirect-tax:customize record that we rely on the intra-group B2B service-tax exemption
/indirect-tax:customize set our taxable period to bi-monthly
/indirect-tax:customize set our default reporting standard to "strong"
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start).
- Write unverified rates/groups/dates as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

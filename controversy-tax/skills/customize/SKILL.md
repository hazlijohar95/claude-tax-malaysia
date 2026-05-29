---
name: customize
description: >
  Tune your tax controversy practice profile after setup — change the dispute posture,
  update the deadline calendar, adjust the reporting-standard threshold, or fix house
  submission style — without re-running the full cold-start interview. Use for "change my
  settings", "update my posture", "customize the plugin".
argument-hint: "[what to change, in plain English]"
---

# /customize

Targeted edits to `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If missing/all-placeholder, redirect to `/controversy-tax:cold-start-interview`.
2. **Locate the section:** `## Dispute posture`, `## Reporting standard`, `## Deadline calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a deadline, section, time-bar period, or penalty rate, confirm it against a primary source or flag it `[verify]` in the profile. A wrong deadline written into the profile is the most dangerous error this plugin can make — never write one as settled.
4. **Show the diff** and confirm before writing.
5. **Write** the change, preserving the rest. Note which skills it affects.

## Examples
```
/controversy-tax:customize set our posture to "litigate selectively above RM250k exposure"
/controversy-tax:customize record the objection window as 30 days from the notice date
/controversy-tax:customize set our default standard to hold a position at "more likely than not"
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start). - Edit a specific matter (use `/controversy-tax:matter-update`). - Write unverified deadlines as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

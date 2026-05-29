---
name: customize
description: >
  Tune your personal-tax practice profile after setup — change a convention, add a relief
  to the standard checklist, update the reporting-standard threshold, fix a deadline rule,
  or adjust house style — without re-running the full cold-start interview. Use for "change
  my settings", "update my conventions", "customize the plugin".
argument-hint: "[what to change, in plain English]"
---

# /customize

Targeted edits to `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md` without a full re-interview.

## Instructions

1. **Read** the current profile. If it's missing or all placeholders, redirect to `/personal-tax:cold-start-interview` — there's nothing to customize yet.
2. **Locate the section** the user's request maps to: `## Computation conventions`, `## Reporting standard`, `## Deadline calendar`, `## House style`, `## Available integrations`, or `## Who's using this`.
3. **Verify before writing.** If the change is a rate, relief cap, threshold, section number, or deadline, apply the guardrail: confirm it against a primary source or flag it `[verify]` in the profile. Never write an unverified figure into the profile as if it were settled — the profile is read by every skill, so a wrong fact here propagates everywhere. **Relief caps and rates change every Budget — record the category, flag the amount.**
4. **Show the diff** — the before and after of the lines you'll change — and confirm before writing.
5. **Write** the change, preserving the rest of the file. Note in your reply which skills the change affects.

## Examples
```
/personal-tax:customize add "PRS / deferred annuity" to the standard relief checklist
/personal-tax:customize set our default reporting standard to "more likely than not"
/personal-tax:customize the Form B deadline rule is 30 June following the YA
```

## What this skill does NOT do
- Re-run the interview (use `--redo` on cold-start for that). - Write unverified rates/caps/dates as settled fact.

## Close with a short confirmation and, if relevant, the next-steps decision tree.

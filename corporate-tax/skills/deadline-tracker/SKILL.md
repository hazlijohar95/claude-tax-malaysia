---
name: deadline-tracker
description: >
  Track company tax filing and payment deadlines — Form C, CP204 estimate, CP204A
  revisions, monthly instalments, balance of tax — from the deadline calendar in the
  practice profile, with penalty-aware warnings and an annual re-verification prompt.
  Use for "what's due", "tax deadlines", "CP204 dates", "filing calendar".
argument-hint: "[entity / YA, or 'all'] [--add to record a new obligation]"
---

# Deadline Tracker

## Purpose

The deadlines that carry penalties only help if someone reads them in time. This skill computes upcoming obligations from the deadline calendar in the profile and the entity's period end, and warns before the windows close — with the caution that **filing programmes and grace periods change every year**.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md` → `## Deadline calendar` and the entity's period end. The calendar dates are the team's recorded understanding, tagged for annual verification — this skill does not assert statutory dates from memory.

## Workflow

1. **Establish the basis period / YA and period end** for each entity (from the profile or ask).
2. **Compute each obligation's due date** from the calendar's rule (e.g., "7 months after period end") applied to this entity's period end. State the rule used and tag the result `[verify against the current LHDN filing programme for YA <year>]`.
3. **Currency check.** Before presenting dates as actionable, flag: "These are computed from your recorded calendar rules. The LHDN filing programme and any grace periods for YA [year] should be confirmed — I have not verified them against current guidance unless a source is connected." If a source is available, verify and upgrade the tag.
4. **Rank by urgency** with a penalty note on each (e.g., CP204 underestimation → s.107C(10); late Form C → s.112/s.113 — all `[verify]`).
5. **Report** sorted by due date, with 🔴 for anything inside the next 14 days, 🟠 for 15–44, 🟡 for 45–90.

## `--add`
Append a new obligation to the entity's tracking (date, basis, owner) in the matter folder or a local register. Record the source of the date.

## Output format
```
📅 Tax deadlines — [entity] — as of [date]
🔴 Due ≤14 days: [obligation] — due [date] `[verify against LHDN programme]` — penalty: [basis]
🟠 / 🟡 ...
⚠️ Dates computed from recorded calendar rules; confirm against current LHDN filing programme for YA [year].
```
If nothing is due in 90 days, say so explicitly so the user knows the tracker ran.

## What this skill does NOT do
- Assert statutory deadlines as fact — it computes from recorded rules and flags for verification. - File or pay anything. - Replace the firm's own deadline-control system; it complements it.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer the dashboard for a multi-entity calendar.

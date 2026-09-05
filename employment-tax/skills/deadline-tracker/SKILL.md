---
name: deadline-tracker
description: >
  Track employer payroll-tax deadlines — PCB/CP39 remittance, EPF/SOCSO/EIS remittance, the EA
  statement to employees, Form E + CP8D, and the CP22 / CP22A / CP21 notification windows — from
  the calendar in the practice profile, with penalty-aware warnings and an annual re-verification
  prompt. Use for "what payroll tax is due", "payroll tax deadlines", "PCB remittance date", "Form E deadline",
  "when's the EA due".
argument-hint: "[employer, or 'all'] [--add to record a new obligation]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Deadline Tracker

## Purpose

The remittance and filing dates that carry penalties only help if someone reads them in time. This skill computes upcoming obligations from the calendar in the profile and the employer's circumstances, and warns before the windows close — with the caution that **programmes and grace periods change**.

The recurring monthly remittances (PCB, EPF/SOCSO/EIS) are the ones most easily missed because they come round every month — this tracker treats them as first-class, not just the annual Form E.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md` → `## Deadline calendar`. The dates are the team's recorded understanding, tagged for verification — this skill does not assert statutory dates from memory.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

1. **Establish the employer and the in-scope obligations** (monthly remittances always; annual Form E/EA; any open leaver requiring CP21/CP22A).
2. **Compute each obligation's due date** from the calendar's rule (e.g., "PCB by the 15th of the following month") for the current period. State the rule used and tag the result `[verify against current LHDN / EPF / PERKESO guidance]`.
3. **Currency check.** Flag: "These are computed from your recorded calendar rules. The current programmes and any grace periods should be confirmed — I have not verified them against current guidance unless a source is connected." If a source is available, verify and upgrade the tag.
4. **Rank by urgency** with a penalty note on each (late PCB → employer liable for the amount + penalty; late EPF/SOCSO → late-payment interest; late Form E → s.120; missed CP21 → notification penalty + the withholding exposure — all `[verify]`).
5. **Report** sorted by due date, with 🔴 for anything inside the next 14 days, 🟠 for 15–44, 🟡 for 45–90. Always surface the next monthly remittance even if routine.

## `--add`
Append a new obligation (e.g., a leaver's CP21 window) to the employer's tracking (date, basis, owner) in the matter folder or a local register. Record the source of the date.

## Output format
```
📅 Payroll-tax deadlines — [employer] — as of [date]
🔴 Due ≤14 days: [obligation] — due [date] `[verify]` — penalty: [basis]
🟠 / 🟡 ...
🔁 Next monthly: PCB/CP39 [date]; EPF/SOCSO/EIS [date]
⚠️ Dates computed from recorded calendar rules; confirm against current LHDN / EPF / PERKESO guidance.
```
If nothing non-routine is due in 90 days, say so explicitly (and still show the next monthly remittance) so the user knows the tracker ran.

## What this skill does NOT do
- Assert statutory deadlines as fact — it computes from recorded rules and flags for verification.
- Remit or file anything.
- Replace the firm's own payroll calendar; it complements it.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer the dashboard for a multi-employer calendar.

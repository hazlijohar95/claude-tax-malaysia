---
name: deadline-tracker
description: >
  Track individual tax filing and payment deadlines — Form BE, Form B, Form M, CP500
  instalments, balance of tax — from the deadline calendar in the practice profile, with
  penalty-aware warnings and an annual re-verification prompt. Use for "what's due",
  "personal tax deadlines", "Form BE date", "filing calendar".
argument-hint: "[name / YA, or 'all'] [--add to record a new obligation]"
---

# Deadline Tracker

## Purpose

The deadlines that carry penalties only help if someone reads them in time. This skill computes upcoming obligations from the deadline calendar in the profile and the individual's circumstances (which form, business income or not), and warns before the windows close — with the caution that **filing programmes and grace periods change every year**.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md` → `## Deadline calendar` and the individual's profile (which form applies). The calendar dates are the team's recorded understanding, tagged for annual verification — this skill does not assert statutory dates from memory.

## Workflow

1. **Establish the form and YA** for each individual (Form BE if employment-only resident, Form B if business income, Form M if non-resident — from the profile or ask).
2. **Compute each obligation's due date** from the calendar's rule (e.g., "Form BE due 30 April following the YA") applied to this individual. State the rule used and tag the result `[verify against the current LHDN filing programme for YA <year>]`.
3. **Currency check.** Before presenting dates as actionable, flag: "These are computed from your recorded calendar rules. The LHDN filing programme and any e-filing grace period for YA [year] should be confirmed — I have not verified them against current guidance unless a source is connected." If a source is available, verify and upgrade the tag.
4. **Rank by urgency** with a penalty note on each (e.g., late Form BE/B → s.112/s.113; late balance of tax → s.103 increase; CP500 underpayment → s.107B — all `[verify]`).
5. **Report** sorted by due date, with 🔴 for anything inside the next 14 days, 🟠 for 15–44, 🟡 for 45–90.

## `--add`
Append a new obligation to the individual's tracking (date, basis, owner) in the matter folder or a local register. Record the source of the date.

## Output format
```
📅 Tax deadlines — [name] — as of [date]
🔴 Due ≤14 days: [obligation] — due [date] `[verify against LHDN programme]` — penalty: [basis]
🟠 / 🟡 ...
⚠️ Dates computed from recorded calendar rules; confirm against current LHDN filing programme for YA [year].
```
If nothing is due in 90 days, say so explicitly so the user knows the tracker ran.

## What this skill does NOT do
- Assert statutory deadlines as fact — it computes from recorded rules and flags for verification. - File or pay anything. - Replace the firm's own deadline-control system; it complements it.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer the dashboard for a multi-client calendar.

---
name: deadline-watcher
description: >
  Scheduled agent that checks the payroll-tax deadline calendar and posts what's coming up —
  the monthly PCB and EPF/SOCSO/EIS remittances, the annual Form E / EA dates, and any open
  CP21 / CP22A windows. Runs weekly by default. Posts to the channel named in
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md` → House style →
  Remittance / deadline alerts. Trigger phrases: "what payroll deadlines are coming",
  "check payroll tax deadlines", "deadline report", or on schedule.
model: sonnet
tools: ["Read", "Write", "mcp__*__slack_send_message"]
---

# Deadline Watcher Agent

## Purpose

The remittance and filing dates only help if someone reads them. This agent reads the calendar weekly and tells the channel which PCB/CP39 and EPF/SOCSO/EIS remittances, Form E / EA dates, and leaver notification windows are coming up before they're missed. The monthly remittances are the ones most easily missed — the agent always surfaces the next one.

## Schedule

Weekly, Monday morning. Configurable.

## What it does

1. Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md` for the alert destination and the deadline calendar rules.
2. Run the deadline-tracker logic across the employers in scope (or the active matter portfolio).
3. **Apply the currency caution.** The dates are computed from recorded calendar rules; the post explicitly says they must be confirmed against current LHDN / EPF / PERKESO guidance. The agent does not assert statutory dates as fact.
4. If there are 🔴 items (due ≤14 days) — including the next monthly remittance if it falls in the window — post them regardless of schedule.
5. Post the report to the destination.

## Output format

```
📅 **Payroll-tax deadlines — week of [date]**

🔴 **Due ≤14 days**
• [Employer] — [obligation] due **[date]** `[verify]` — penalty: [basis]

🔁 **Next monthly remittances**
• PCB / CP39 — [date]   • EPF / SOCSO / EIS — [date]

🟠 **15–44 days** / 🟡 **45–90 days**
• ...

⚠️ Dates computed from recorded calendar rules — confirm against current LHDN / EPF / PERKESO guidance.
```

If nothing non-routine is due in 90 days, post a short all-clear (still showing the next monthly remittance) so people know the agent ran.

## What this agent does NOT do

- Remit or file anything.
- Assert statutory deadlines as fact — it computes from recorded rules and flags for verification.
- Decide whether to release a leaver's final pay — it surfaces the clearance window; a person decides.

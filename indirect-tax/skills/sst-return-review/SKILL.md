---
name: sst-return-review
description: >
  Review the SST-02 return before submission — output tax tied to the taxable-supplies
  listing, exemptions and deductions checked, input/recovery figures sourced, totals
  reconciled, and a submission gate. Use for "review the SST-02", "check the SST return",
  "is the SST return ready".
argument-hint: "[taxable period] [SST-02 draft + sales/purchase listing]"
---

# SST-02 Return Review

## Purpose

Catch SST-02 errors before submission, not after a Customs audit. The return is only as good as the listing behind it and the totals carried onto the form. This skill ties the two together.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md`. You need the **SST-02 draft** and the **sales/purchase listing** for the period. With only the form, you can sanity-check it against itself but cannot confirm it ties to the underlying records — which is the point.

## Workflow

### Step 1 — Tie output tax to the listing
Recompute total taxable supplies and output tax from the listing and compare to the form. Produce a tie-out: Field | SST-02 value | Recomputed from listing | ✓/✗ | Source. Any mismatch is 🔴.

### Step 2 — Check exemptions and out-of-scope treatment
For supplies treated as exempt or out of scope on the listing, confirm the basis holds (an exemption with unmet conditions belongs in output tax). Flag any treatment that rests on a stale or unconfirmed basis `[review]` and tag the authority `[verify against the current order]`.

### Step 3 — Input / deduction / bad-debt fields
For any deduction, credit, or bad-debt relief claimed, confirm it is within the rules for the period and sourced to a record. Tag the basis `[verify against current RMCD guidance]` — relief mechanics and conditions change.

### Step 4 — Reasonableness and deadline
Analytical pass: period-on-period movement in output tax, anomalies that would draw a query. Confirm the SST-02 due date for the period (from the calendar, `[verify against current RMCD guidance]`) and whether it's at risk.

### Step 5 — Submission gate
State readiness with blocking items. **If Role is Non-professional**, gate before submission: "Submitting the SST-02 is a declaration and carries penalties for under-declaration. Has a qualified adviser reviewed it? If yes, proceed. If no, here's the brief." Do not proceed past the gate without an explicit yes. This skill does not submit to RMCD.

## Output format
```
[WORK-PRODUCT HEADER]
# SST-02 Review: [taxable period] — [READY / NOT READY]
## Bottom line — [N]🔴 [N]🟠 [N]🟡; output tax ties to listing: [yes/NO]
## Tie-out   [Step 1]
## Exemptions / out-of-scope   [Step 2]
## Inputs / deductions / bad-debt   [Step 3]
## Reasonableness & deadline   [Step 4]
## Before submitting   [blocking items + gate]
```

## Quality checks
- [ ] Output tax recomputed from the listing and tied to the form
- [ ] Exemption/out-of-scope treatments confirmed, not assumed
- [ ] Deductions/relief sourced and within current rules (flagged for verification)
- [ ] Submission gate applied for non-professional role

## What this skill does NOT do
- Submit the return.
- Recompute taxability from scratch (use `/indirect-tax:taxability-determination`).
- Assert SST-02 field rules or rates from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer the dashboard/workbook for the tie-out.

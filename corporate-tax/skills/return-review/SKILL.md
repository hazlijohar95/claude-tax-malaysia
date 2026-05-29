---
name: return-review
description: >
  Review a company tax return (Form C) against the computation it's built from,
  before filing — every figure on the form traced to the computation, the carried-
  forward balances and instalment credits checked, disclosure boxes reviewed, and a
  filing gate before submission. Use for "review the Form C", "check the return
  before we file", "is the return ready".
argument-hint: "[entity / YA] [the Form C draft + the supporting computation]"
---

# Return Review (Form C)

## Purpose

Catch errors before the return is filed, not after the assessment. The return is only as good as the computation behind it and the transcription onto the form. This skill checks both: that the computation is sound, and that the form faithfully reflects it.

A filed return is hard to unwind. This is a pre-filing review — it does not file.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`. You need **both** the Form C draft **and** the supporting tax computation. If you have only the form, say so — you can sanity-check the form against itself but cannot confirm it ties to the computation, which is the point of the review.

## Workflow

### Step 1 — Tie the form to the computation
For each key box on the Form C, find the corresponding figure in the computation and confirm they agree: chargeable income, tax payable, business statutory income, aggregate/total income, capital allowances, losses/CA carried forward, approved donations, instalments paid. Produce a tie-out table: Box | Form C value | Computation value | ✓/✗ | Source. Any mismatch is 🔴 — a return that doesn't match its computation is filed wrong.

### Step 2 — Check the carried-forward and credit figures against primary records
Brought-forward losses and unabsorbed CA on the form should agree to the latest **agreed assessment / prior filed return**, not just last year's working. CP204 instalment credits should agree to the actual payment records. Flag any that rest on a management figure `[review]`.

### Step 3 — Disclosure and election boxes
Walk the disclosure/election boxes (related-party transactions, incentives claimed, CbCR/TP declarations, any specific schedules). Each carries a representation — flag any that are ticked without support, or unticked where the facts suggest they apply, `[review]`. Tag the statutory basis of each box `[verify against the current Form C and filing programme for YA <year>]` — the form and its boxes change between years.

### Step 4 — Reasonableness and deadline
A quick analytical pass: effective rate vs expected, year-on-year movement, anything that would draw a query. Confirm the filing deadline for the YA (from the deadline calendar, `[verify against current LHDN filing programme]`) and whether it's at risk.

### Step 5 — Filing gate
State readiness: ready / not ready, with the blocking items. **If Role is Non-professional**, gate before any filing: "Filing is irreversible and carries penalties for errors (s.113 ITA `[verify]`). Has a qualified tax adviser reviewed this return? If yes, proceed. If no, here's the brief to bring them." Do not proceed past the gate without an explicit yes. This skill does not submit to LHDN — submission is the user's action.

## Output format

```
[WORK-PRODUCT HEADER]
# Form C Review: [Entity] — YA [year]
## Bottom line — [READY / NOT READY]; [N]🔴 [N]🟠 [N]🟡; ties to computation: [yes/NO]
## Tie-out table   [Step 1]
## Carried-forward & credits   [Step 2]
## Disclosure / election boxes   [Step 3]
## Reasonableness & deadline   [Step 4]
## Before filing   [the blocking items + the gate]
```

## Quality checks
- [ ] Every key box tied to the computation; mismatches flagged 🔴
- [ ] B/f balances and instalment credits checked against primary records
- [ ] Disclosure boxes reviewed, not assumed
- [ ] Form/box references tagged for verification against the current year's form
- [ ] Filing gate applied for non-professional role

## What this skill does NOT do
- File the return. - Re-derive the computation (run `/corporate-tax:tax-computation` for that). - Assert the current form's box numbers from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

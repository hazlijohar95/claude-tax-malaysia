---
name: return-review
description: >
  Review an individual tax return (Form BE / Form B / Form M) against the computation
  it's built from, before filing — every figure on the form traced to the computation,
  the reliefs and rebates and PCB credit checked, the residence and assessment-basis
  declarations reviewed, and a filing gate before submission. Use for "review the Form BE",
  "check the return before we file", "is the individual return ready".
argument-hint: "[name / YA] [the Form BE/B draft + the supporting computation]"
---

# Return Review (Form BE / Form B)

## Purpose

Catch errors before the return is filed, not after the assessment. The return is only as good as the computation behind it and the transcription onto the form. This skill checks both: that the computation is sound, and that the form faithfully reflects it.

A filed return is hard to unwind, and on self-assessment the figures are the taxpayer's own representation. This is a pre-filing review — it does not file.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`. You need **both** the Form BE/B draft **and** the supporting computation (and the relief schedule). If you have only the form, say so — you can sanity-check the form against itself but cannot confirm it ties to the computation, which is the point of the review.

Confirm the **right form**: Form BE (resident, no business income), Form B (resident, business/professional income), Form M (non-resident) `[verify against current LHDN forms]`. Filing the wrong form is a 🔴 finding.

## Workflow

### Step 1 — Tie the form to the computation
For each key entry on the form, find the corresponding figure in the computation and confirm they agree: each income source's statutory income, aggregate/total income, total reliefs, chargeable income, tax charged, rebates, PCB deducted, instalments, balance payable/repayable. Produce a tie-out table: Field | Form value | Computation value | ✓/✗ | Source. Any mismatch is 🔴 — a return that doesn't match its computation is filed wrong.

### Step 2 — Check the reliefs, rebates, and credit figures against evidence
Reliefs on the form should agree to the relief schedule **and** be within their YA caps with retained evidence — flag any unevidenced claim `[review]`. The PCB credit should agree to the **EA form**, not a payslip estimate. CP500 instalments (Form B) should agree to the payment record. The s.6A rebate should appear only if chargeable income is within the threshold.

### Step 3 — Residence, assessment basis, and declaration boxes
Confirm the residence declaration matches the computation's residence conclusion (resident scale vs non-resident). For a married taxpayer, confirm the joint-vs-separate-assessment election on the form matches the basis the computation used. Walk the other declaration boxes (disposal of assets, foreign income, any specific schedules) — each carries a representation; flag any ticked without support or unticked where the facts suggest they apply `[review]`. Tag box/section references `[verify against the current form for YA <year>]` — forms change between years.

### Step 4 — Reasonableness and deadline
A quick analytical pass: effective rate vs expected, year-on-year movement, reliefs that look high relative to income, anything that would draw a query. Confirm the filing deadline for the YA and form (from the deadline calendar, `[verify against current LHDN filing programme]`) and whether it's at risk.

### Step 5 — Filing gate
State readiness: ready / not ready, with the blocking items. **If Role is Non-professional**, gate before any filing: "Filing is your own representation and the balance is payable on filing; errors carry penalties (s.113 ITA `[verify]`). Has a qualified tax adviser reviewed this return? If yes, proceed. If no, here's the brief to bring them." Do not proceed past the gate without an explicit yes. This skill does not submit to LHDN — submission is the user's action.

## Output format

```
[WORK-PRODUCT HEADER]
# Return Review: [Name] — YA [year] — [Form BE / B / M]
## Bottom line — [READY / NOT READY]; [N]🔴 [N]🟠 [N]🟡; ties to computation: [yes/NO]
## Tie-out table   [Step 1]
## Reliefs, rebates & credits   [Step 2]
## Residence, assessment basis & declarations   [Step 3]
## Reasonableness & deadline   [Step 4]
## Before filing   [the blocking items + the gate]
```

## Quality checks
- [ ] Correct form confirmed (BE / B / M) for the residence and income profile
- [ ] Every key field tied to the computation; mismatches flagged 🔴
- [ ] Reliefs within caps and evidenced; PCB tied to the EA form
- [ ] Residence and assessment-basis declarations match the computation
- [ ] Box/section references tagged for verification against the current year's form
- [ ] Filing gate applied for non-professional role

## What this skill does NOT do
- File the return. - Re-derive the computation (run `/personal-tax:tax-computation` for that). - Assert the current form's box numbers from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

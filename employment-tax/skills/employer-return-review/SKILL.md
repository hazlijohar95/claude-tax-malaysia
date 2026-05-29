---
name: employer-return-review
description: >
  Review the employer's annual return (Form E and its CP8D employee listing) and the EA
  statements before submission — every total tied to the payroll register and the year's CP39
  remittances, each employee's CP8D line checked, EA statements reconciled to what was reported,
  and a filing gate. Use for "review Form E", "check the CP8D", "are the EA forms right",
  "employer return before we file".
argument-hint: "[employer / year] [the Form E + CP8D draft, EA statements, and payroll summary]"
---

# Employer Return Review (Form E / CP8D / EA)

## Purpose

Catch errors before the employer return is filed and the EA statements go out, not after LHDN cross-matches them. Form E (with the CP8D employee listing) is the employer's annual declaration of remuneration and PCB; the EA statements are what each employee relies on for their own return. The two must reconcile to the payroll register and to the year's PCB remittances — and to each other.

A filed Form E and issued EA statements are hard to unwind. This is a pre-filing review — it does not file.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. You need the **Form E + CP8D draft**, the **EA statements** (or a sample), and the **payroll summary / register + the year's CP39 totals**. If you have only the form, say so — you can sanity-check it against itself but cannot confirm it ties to the payroll, which is the point.

Confirm the correct year's form and CP8D layout `[verify against the current LHDN forms]` — the form changes between years.

## Workflow

### Step 1 — Tie Form E totals to the payroll and remittances
Reconcile the Form E headline figures — number of employees, total remuneration, total PCB — to the payroll register and the sum of the year's CP39 remittances. Tie-out table: Field | Form E | Payroll/CP39 | ✓/✗ | Source. Any mismatch is 🔴. A common 🔴: total PCB on Form E ≠ sum of CP39s remitted (a remittance was missed or misposted).

### Step 2 — Check the CP8D employee listing
For a sample (or all, if scoped), confirm each employee's CP8D line — name/ID, remuneration, BIK/VOLA, EPF, PCB — agrees to that employee's payroll record and EA statement. Flag employees missing from the listing, or listed with figures that don't match their EA `[review]`. New joiners and leavers in the year are the usual source of gaps — check CP22/CP22A were filed (hand to `/employment-tax:tax-clearance` for leavers).

### Step 3 — Reconcile the EA statements
The EA given to each employee must equal what's reported for them on CP8D. Check that taxable BIK/perquisites (from `/employment-tax:bik-perquisites`) actually made it onto the EA — a benefit valued but omitted from the EA is both an employee-return error and a sign it was also left out of the PCB base (an employer under-deduction). Flag any such omission 🔴 with the under-deduction exposure.

### Step 4 — Reasonableness and deadline
A quick analytical pass: total PCB vs total remuneration at a plausible effective rate; any employee with remuneration but zero PCB; year-on-year movement. Confirm the Form E and EA deadlines for the year (from the deadline calendar, `[verify against current LHDN guidance]`) and whether they're at risk.

### Step 5 — Filing gate
State readiness: ready / not ready, with the blocking items. **If Role is Non-professional**, gate before any filing: "Form E is the employer's declaration; errors and omissions carry penalties (s.120 ITA `[verify]`), and the EA statements drive your employees' own returns. Has a qualified tax adviser reviewed this? If yes, proceed. If no, here's the brief." Do not proceed past the gate without an explicit yes. This skill does not submit — submission is the user's action.

## Output format

```
[WORK-PRODUCT HEADER]
# Employer Return Review: [Employer] — [year]
## Bottom line — [READY / NOT READY]; [N]🔴 [N]🟠 [N]🟡; Form E ties to payroll & CP39: [yes/NO]
## Form E tie-out   [Step 1]
## CP8D employee listing   [Step 2]
## EA reconciliation   [Step 3 — include any benefit omitted from EA + the under-deduction exposure]
## Reasonableness & deadline   [Step 4]
## Before filing   [the blocking items + the gate]
```

## Quality checks
- [ ] Correct year's Form E / CP8D layout confirmed
- [ ] Form E totals tied to the payroll register AND the sum of CP39 remittances; mismatches 🔴
- [ ] CP8D lines checked (sample or all); missing employees / mismatches flagged
- [ ] EA statements reconciled to CP8D; benefits omitted from EA flagged 🔴 with under-deduction exposure
- [ ] Deadlines confirmed for the year; filing gate applied for non-professional role

## What this skill does NOT do
- File Form E or issue the EA statements. - Re-derive the PCB (run `/employment-tax:pcb-computation`). - Assert the current form's layout or box numbers from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

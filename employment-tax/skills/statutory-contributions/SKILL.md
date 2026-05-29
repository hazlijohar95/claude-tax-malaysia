---
name: statutory-contributions
description: >
  Compute EPF (KWSP), SOCSO (PERKESO), and EIS (SIP) contributions for an employee or a
  payroll run — employer and employee portions, by wage band, age, and citizenship category —
  from the payroll register, against the team's setup in
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. Every contribution traces
  to a register line and ties to the remittance total; every rate, ceiling, and category rule is
  flagged for verification against the current EPF / PERKESO schedules because the employer is
  liable for under-contribution. Use for "compute EPF", "SOCSO and EIS", "statutory deductions",
  "contribution schedule for the payroll".
argument-hint: "[employee / month, or 'payroll run'] [path to payroll register, or paste it]"
---

# Statutory Contributions (EPF / SOCSO / EIS)

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip — skills use practice-level context. If enabled, load the active employer's `matter.md` (contribution categories, any voluntary-rate elections) and write outputs there.

## Purpose

Produce the EPF, SOCSO, and EIS figures a reviewer can sign off and remit: each contribution split into employer and employee portions, computed against the correct wage band and category, traced to the register, and tied to the remittance total — with every rate and ceiling flagged for verification, because under-contribution is the employer's exposure.

This skill does not assert contribution rates, wage ceilings, or category thresholds from memory. **They change — sometimes mid-year, sometimes by temporary rate — so every one is `[verify for <period>]`.**

## Precondition: load the profile

**Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`** for the contribution setup — the rate bands, ceilings, and age/citizenship categories the team applies. If missing or placeholder, redirect to `/employment-tax:cold-start-interview`, or proceed `[PROVISIONAL]` against the generic structure with every rate/ceiling flagged.

## Inputs required

1. **The payroll register / payslip detail** — wages and the components that count as "wages" for each scheme (the contribution base can differ from the PCB base).
2. **Per-employee category facts** — age, citizenship/residency status (Malaysian / permanent resident / foreign worker), and any voluntary-rate election — these change which table applies.
3. **The period** — drives the rate/ceiling version.

## Workflow

### Step 1 — Establish the contribution base per scheme

The definition of "wages" differs by scheme — confirm which components are contributory for **EPF**, for **SOCSO**, and for **EIS** `[model knowledge — verify]`. Build each base from the register with a source reference per line. A component contributory for one scheme may be excluded from another — don't assume a single base.

### Step 2 — Categorise each employee

For each employee, establish the category that selects the rate table:
- **EPF:** age band (the employee/employer rate can differ above a certain age) and citizenship (foreign employees follow a different rule) `[verify]`.
- **SOCSO:** which scheme applies (Employment Injury only vs Employment Injury + Invalidity, driven by age) and citizenship `[verify]`.
- **EIS:** eligibility by age and citizenship `[verify]`.

State the category and its source for each employee. A wrong category is a wrong contribution — flag any employee whose category isn't clear `[review]`.

### Step 3 — Compute each contribution (employer + employee)

For each scheme, apply the rate/table to the base, respecting the wage ceiling:

```
**EPF** — base RM [x]
  Employee portion: [rate]% (or table) = RM [e]                    `[verify rate for period]`
  Employer portion: [rate]% (or table) = RM [r]                    `[verify rate for period]`
**SOCSO** — base RM [x] (capped at ceiling RM [c] `[verify]`)
  Employee + Employer per the contribution table = RM [...]        `[verify table]`
**EIS** — base RM [x] (capped at ceiling RM [c] `[verify]`)
  Employee + Employer per the table = RM [...]                     `[verify table]`
```

**Critical distinction:** the **employer portion is the employer's own cost on top of wages** — it is NOT deducted from the employee's pay. Only the **employee portion** is deducted. State this split clearly so it isn't conflated. Note that only the **employee EPF** feeds the PCB relief / the employee's personal relief — hand the employee-EPF figure to `/employment-tax:pcb-computation`.

### Step 4 — Totals and remittance reconciliation

Sum employer and employee portions per scheme. State the total to remit to each body (EPF, SOCSO/EIS via PERKESO) and the due date (from the deadline calendar, `[verify]`). CHECK that the per-employee figures sum to the schedule total.

### Step 5 — Tie-out (CHECK cells)

- **CHECK 1:** Each scheme's base built from the register, source per line; scheme-specific inclusions respected. ✓/✗
- **CHECK 2:** Each employee categorised; uncertain categories flagged `[review]`. ✓/✗
- **CHECK 3:** Employer vs employee portions separated; only the employee portion shown as a pay deduction. ✓/✗
- **CHECK 4:** Wage ceilings applied where they exist. ✓/✗
- **CHECK 5:** Per-employee figures sum to the remittance total. ✓/✗
- **CHECK 6:** Employee-EPF figure reconciled to the figure used as relief in the PCB computation. ✓/✗

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Statutory Contributions: [Employee or 'Payroll run'] — [month/year]

## Bottom line
EPF RM [..] (er RM [..] / ee RM [..]); SOCSO RM [..]; EIS RM [..]. Total employer cost RM [..]; total employee deduction RM [..].
[N]🟠 [N]🟡 flagged (category/base). Ties to remittance total: [yes / NO].

## Contributions
[the Step 3 blocks per scheme, employer/employee split, rates tagged `[verify for period]`]

## For the PCB computation
[employee-EPF figure + source, to feed the PCB relief]

## Open items
[uncertain categories or contributory-base calls flagged `[review]`]

## CHECK
[the Step 5 reconciliations, pass/fail]
```

For a **payroll run**, scope per `## Large output` — sample in detail + tabular pass, or batches.

## Quality checks before delivering

- [ ] Each scheme's contributory base built from the register (not assumed identical to the PCB base)
- [ ] Every employee categorised by age/citizenship; uncertain ones flagged
- [ ] Employer portion shown as employer cost, NOT as a pay deduction
- [ ] Every rate, table, and ceiling tagged `[verify for period]`
- [ ] Employee-EPF reconciled to the PCB relief figure
- [ ] Per-employee figures tie to the remittance total

## What this skill does NOT do

- Remit to EPF / PERKESO (that's the user's gated action).
- Assert contribution rates, ceilings, or category thresholds as settled fact — it flags every one for verification.
- Compute PCB (run `/employment-tax:pcb-computation`).

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer the workbook export, the PCB computation, or the deadline view as natural next steps.

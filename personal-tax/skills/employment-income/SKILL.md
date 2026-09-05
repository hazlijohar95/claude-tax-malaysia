---
name: employment-income
description: >
  Build the employment income figure under s.13 ITA from the EA/EC form and payroll —
  salary, bonuses, benefits-in-kind and perquisites, ESOS, gratuity and compensation
  for loss of employment — separating taxable amounts from exempt reimbursements, and
  identifying the exemptions that apply, against the team's conventions in
  `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`. Every figure traced
  to the EA form / payslip; every exemption and valuation basis tagged for verification.
  Use for "work out the employment income", "is this benefit taxable", "BIK / perquisite
  treatment", "gratuity exemption".
argument-hint: "[name / YA] [the EA/EC form + payroll detail, or paste them]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Employment Income (s.13)

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip — skills use practice-level context. If enabled, load the active matter's `matter.md` and write outputs there.

## Purpose

Produce the s.13 employment income figure that feeds the computation — with the taxable/exempt line drawn explicitly for every benefit, each amount traced to the EA form or payroll, and each exemption named with its condition and tagged for verification. The characterisation calls (taxable perquisite vs exempt reimbursement) are surfaced, not silently resolved.

This skill does not invent valuations or exemption amounts. If the basis isn't in a source document, it is asked for, not guessed.

## Precondition: load the profile

**Read `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`** for the team's BIK/perquisite treatment, EPF treatment, and exemption conventions. If missing or placeholder, redirect to `/personal-tax:cold-start-interview`, or proceed `[PROVISIONAL]` against generic Malaysian defaults with every exemption flagged.

## Inputs required

1. **The EA / EC form** — the primary source for gross remuneration, BIK, EPF, and PCB.
2. **Payroll detail / payslips** — to see the components behind the EA-form totals and to test characterisation.
3. **Benefit documentation** — for company car/accommodation, ESOS grant/exercise, gratuity or compensation packages — to establish the valuation basis and exemption conditions.

## Workflow

### Step 1 — Map the EA form

List each EA-form box and what it represents, with the box as the **source reference**. The EA-form totals are the figures the computation ties to (CHECK in the main computation). Note anything in payroll that should be on the EA form but isn't, or vice versa, `[review]`.

### Step 2 — s.13(1)(a)–(e): classify each component

Work through the heads of employment income:

- **s.13(1)(a)** — salary, wages, bonus, commission, gratuity, allowances (cash).
- **s.13(1)(b)** — benefits-in-kind (car, fuel, driver, household, etc.) — by the prescribed valuation method `[model knowledge — verify]`.
- **s.13(1)(c)** — value of living accommodation provided.
- **s.13(1)(d)** — unapproved-fund withdrawals.
- **s.13(1)(e)** — compensation for loss of employment.

For each, state the amount, its **source**, the valuation basis, and the authority `[verify]`. BIK valuation methods (prescribed-value vs formula) and accommodation valuation are tagged `[model knowledge — verify]` — do not assert the prescribed rates from memory.

### Step 3 — Taxable vs exempt: the line

For every allowance, reimbursement, and benefit, draw the line explicitly:

```
**[Item]** — RM [amount]
Source: [EA box / payslip line]
Treatment: [taxable perquisite under s.13(1)(_) | exempt — [basis] | partly exempt — RM [x] exempt, RM [y] taxable]
Authority: [PR / gazette exemption order] `[model knowledge — verify]`
[review] — where the characterisation is a judgment call, carry BOTH treatments
```

Common judgment calls (flag, don't resolve silently): a travel/petrol allowance vs an exempt official-duties reimbursement; a phone/internet benefit; medical vs non-medical; the perquisite-vs-tool-of-trade line. **Exemption amounts and conditions are `[verify for YA <year>]`** — these change by Budget and gazette order.

### Step 4 — Gratuity, compensation, ESOS

- **Gratuity / compensation for loss of employment (s.13(1)(e)):** the exemption depends on the reason for cessation and years of service `[model knowledge — verify]`. State the basis, compute the exempt portion, flag the conditions `[review]`.
- **ESOS:** the perquisite arises and is valued at a prescribed point (typically the earlier of exercisable/exercise) `[verify]`. Establish the date and the valuation; flag if the basis isn't documented.

### Step 5 — EPF and deductions

EPF/approved-fund contributions are **not deducted from employment income** — the employee contribution feeds the EPF + life insurance relief in the computation (capped, `[verify]`), not this figure. State this so it isn't double-counted. Note the employee EPF figure and its source for the relief step.

### Step 6 — Assemble the s.13 figure and tie

State the total s.13 employment income, with the taxable/exempt split shown, and the CHECK that it reconciles to the EA-form total (taxable portion) used in the computation. If it doesn't tie, say so.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Employment Income (s.13): [Name] — YA [year]

## Bottom line
Taxable employment income RM [x]. RM [e] treated as exempt across [N] items.
[N]🔴 [N]🟠 [N]🟡 items flagged for characterisation. Ties to EA form: [yes / NO].

## Components (s.13(1)(a)–(e))
[the Step 2–3 blocks, taxable/exempt line drawn on each]

## Exemptions applied
[gratuity/compensation, ESOS, allowance exemptions — each with basis and condition `[verify]`]

## For the relief step
[employee EPF figure + source, flagged for the EPF + life relief — not deducted here]

## Open items for your judgment
[each `[review]` characterisation: the item, both treatments, the standard each meets]

## CHECK
Taxable employment income reconciles to EA-form total used in the computation: ✓/✗
```

## Quality checks before delivering

- [ ] Every component traced to an EA box or payslip line
- [ ] Taxable/exempt line drawn explicitly on every benefit and allowance
- [ ] BIK valuation method and exemption amounts tagged `[verify for YA]`
- [ ] Characterisation judgment calls flagged `[review]` with both treatments
- [ ] EPF noted for the relief step, not deducted from income here
- [ ] Total ties to the EA-form figure used in the computation

## What this skill does NOT do

- Assert prescribed BIK valuations or exemption amounts as settled fact — it flags them for verification.
- Decide a borderline taxable/exempt characterisation for you — it surfaces both for adviser judgment.
- Build the full computation (run `/personal-tax:tax-computation`).

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer to feed this into `/personal-tax:tax-computation` or to build the relief schedule with `/personal-tax:reliefs-rebates`.

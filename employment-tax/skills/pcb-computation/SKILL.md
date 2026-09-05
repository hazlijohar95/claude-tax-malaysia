---
name: pcb-computation
description: >
  Compute monthly tax deduction (PCB / MTD) for an employee or a payroll run under the
  Income Tax (Deduction from Remuneration) Rules — normal monthly PCB and the separate
  additional-remuneration PCB for bonus / commission / arrears — from the payroll register,
  TP1 / TP3 declarations, and benefit records, against the team's conventions in
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. The PCB base is built
  explicitly (with an under-deduction watch on every doubtful benefit), every figure traces to
  payroll source and ties back, and every formula constant, relief, and rate is tagged for
  verification. Use for "compute PCB", "MTD for [employee]", "PCB on the bonus", "run PCB for
  the payroll".
argument-hint: "[employee / month, or 'payroll run'] [path to payroll register, TP1/TP3, benefit records, or paste them]"
---

# PCB / MTD Computation

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the single-employer default), skip this — skills use practice-level context. If enabled with no active matter, ask which employer, load its `matter.md` (PCB method, categories, pay calendar), and write outputs to the matter folder.

## Purpose

Produce a PCB computation a reviewer can sign off and remit: the PCB base built line by line from the payroll register, the employee category and reliefs stated, the normal and additional-remuneration PCB shown separately, every formula input traced to a source, and every doubtful inclusion flagged with the employer's under-deduction exposure quantified.

This skill does not invent the PCB formula constants, relief amounts, or rates. If a constant isn't confirmed from a primary source, it is tagged `[verify]`, the period stated, and the computation flagged accordingly.

## Precondition: load the profile

**Before touching the numbers, read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`.** If missing or placeholder:

> You haven't configured your practice profile yet — that's how I tailor your PCB method, employee categories, which benefits go into the base, and your contribution setup.
>
> - Run `/employment-tax:cold-start-interview` (2 min, quick start) to configure, then I'll compute against YOUR conventions.
> - Or say **"provisional"** and I'll compute against the generic Malaysian PCB structure, tag everything `[PROVISIONAL — configure your profile]`, and flag every formula constant, relief, and rate for verification.

## Inputs required

State what you need up front; don't start on half the inputs:

1. **The payroll register / payslip detail** for the month (gross pay, allowances, benefits, EPF deducted — the source of every figure).
2. **The employee's category and qualifying children (KA)** — from the TP1 / employee declaration.
3. **TP1** (employee's claim for current-year deductions/rebates — zakat, additional reliefs) and **TP3** (remuneration and PCB from prior employment in the same year) if applicable.
4. **Accumulated figures year-to-date** — accumulated gross remuneration, accumulated EPF (capped at the statutory annual relief limit), and PCB already paid — for the formula.
5. **Benefit / BIK records** — to build the PCB base correctly (see Step 1).
6. **The pay period and year** — drives the formula constants and reliefs.

If any are missing, say which and what it blocks. PCB computed without the accumulated YTD figures or the TP3 prior-employment data will be wrong — flag it, don't assume zero.

## Workflow

### Step 1 — Build the PCB base (the under-deduction watch lives here)

List every payroll-register line and classify it: **in the PCB base** (taxable remuneration: salary, wages, allowances that are perquisites, taxable BIK, director's fees) or **out** (genuinely exempt reimbursements, employer EPF, employee EPF deducted as relief). Give every line a **source reference**.

- For each benefit/allowance whose treatment isn't clear-cut, **do not silently leave it out.** Flag it `[review]`, state both treatments, and quantify: "if this RM [x] allowance is a taxable perquisite, including it raises this month's PCB by ~RM [y]; leaving it out is an employer under-deduction exposure of that amount." Hand off characterisation detail to `/employment-tax:bik-perquisites` where needed.
- Distinguish **normal remuneration** (recurring monthly) from **additional remuneration** (bonus, commission, arrears, director's fees, gratuity) — they run through different formulas (Steps 3 and 4).

This step is CHECK #1: every register line is classified exactly once (nothing dropped, nothing double-counted).

### Step 2 — Establish category, reliefs, and accumulated figures

- **Category** (1 / 2 / 3) and **KA** (qualifying children) from the TP1/declaration — these set the reliefs in the formula. State them with their source.
- **Reliefs in the formula:** the mandatory individual relief and the EPF/life element (capped at the statutory limit) are built in; **optional TP1 reliefs/rebates** (zakat, approved additional reliefs) are applied per the employee's TP1. Tag every relief amount `[model knowledge — verify for <year>]`.
- **Accumulated remuneration, accumulated EPF (capped), and PCB paid YTD** — from the register / prior CP39. If a TP3 shows prior-employment remuneration and PCB, fold it into the accumulated figures.

### Step 3 — Normal monthly PCB (the formula)

Apply the Computerised Calculation Method (or the schedule, per the profile). Conceptually:

```
Determine net annual taxable remuneration:
  (accumulated normal remuneration to date + current month normal × remaining months)  [from register]
  − allowable EPF/contribution relief (capped)                                         [verify cap]
  − individual & category reliefs (incl. KA child relief, TP1 optional reliefs)         [verify amounts]
= estimated annual chargeable income
Apply the resident scale rates to get estimated annual tax                              [verify scale for year]
  − rebates (s.6A if applicable; zakat per TP1)                                         [verify]
  − PCB already paid year-to-date                                                       [from CP39 / register]
= balance ÷ remaining months in the year
= normal monthly PCB for this month
```

**Every constant, relief amount, scale band, and the formula itself is `[model knowledge — verify for <year>]`** — the MTD rules are gazetted and change. State the formula you used and the period it's for. Do not assert a constant as settled.

### Step 4 — Additional-remuneration PCB (run separately)

If the month includes a bonus, commission, arrears, director's fee, or other additional remuneration, compute its PCB by the **additional-remuneration method** (not by adding it to normal pay and re-running Step 3 naively):

```
Recompute estimated annual tax INCLUDING the additional remuneration
  − estimated annual tax EXCLUDING it (the Step 3 annualised position)
= PCB attributable to the additional remuneration
```

State it as a separate line from the normal monthly PCB. A bonus that pushes the employee across a scale band makes this materially larger than a flat percentage — that's the point of the separate method. Tag `[verify]`.

### Step 5 — Total PCB for the month and the contribution cross-check

- **Total PCB** = normal monthly PCB (Step 3) + additional-remuneration PCB (Step 4).
- Note that PCB is distinct from EPF/SOCSO/EIS — those are separate obligations; hand off to `/employment-tax:statutory-contributions` for them, but cross-check that the EPF used as relief in Step 2 reconciles to the EPF actually deducted.

### Step 6 — Tie-out (CHECK cells — non-negotiable)

Before assembling, run and state the reconciliations:

- **CHECK 1:** Every payroll-register line classified in/out of the PCB base exactly once. ✓/✗
- **CHECK 2:** PCB base = register gross − exclusions; the exclusions list is explicit and each is justified. ✓/✗
- **CHECK 3:** Accumulated remuneration + EPF + PCB-paid agree to the register / prior CP39 (and TP3 if any). ✓/✗
- **CHECK 4:** Category, KA, and TP1 reliefs match the employee declaration. ✓/✗
- **CHECK 5:** Additional remuneration run through the additional-remuneration method, not lumped into normal pay. ✓/✗
- **CHECK 6 (under-deduction watch):** Every doubtful benefit is flagged with its exposure; nothing left out of the base silently. ✓/✗

If any CHECK fails, the reviewer note's **Tie-out** line says so and the output is NOT presented as final.

### Step 7 — Assemble

Prepend the work-product header (per profile `## Outputs`, conditional on role). Lead with the reviewer note (Sources / Read / Tie-out / Flagged / Currency / **Under-deduction watch** / Before relying). Then the bottom line, then the computation, then the open items.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# PCB / MTD: [Employee or 'Payroll run'] — [month/year]

## Bottom line
Total PCB RM [t] = normal RM [n] + additional-remuneration RM [a].
Category [1/2/3], KA [n]. PCB base RM [b] (RM [x] excluded across [N] items).
[N]🔴 [N]🟠 [N]🟡 [N]🟢 flagged. Under-deduction exposure if doubtful items are in the base: RM [e]. Ties out: [yes / NO — see CHECK n].

## PCB base
[the Step 1 classification — every register line, in/out, with source]

## Computation
[normal monthly PCB (Step 3) and additional-remuneration PCB (Step 4), formula stated, constants tagged `[verify for year]`]

## Open items for your judgment
[each `[review]` item: the benefit, both treatments, the standard each meets, the under-deduction exposure]

## CHECK
[the Step 6 reconciliations, pass/fail]
```

For a **payroll run** (many employees), scope per `## Large output`: offer a sample in detail + a tabular pass on all, or batches. Never silently truncate a register.

## Integration

If a document store is connected, offer to pull the register / TP1 / TP3 / prior CP39 by name, and to write the finished PCB schedule (with a `Sources` sheet and CHECK cells) to the house folder. **Before any step that remits:** if Role is Non-professional, gate it — "Remitting PCB to LHDN is the employer's obligation and a shortfall is assessed on the employer with penalties. Has a qualified tax adviser reviewed this run? If yes, proceed. If no, here's a brief: [total PCB, the flagged base items and the standard each meets, the under-deduction exposure]." Do not proceed past the gate without an explicit yes. This skill does not file CP39 or remit — that's the user's gated action.

## Quality checks before delivering

- [ ] Profile loaded and conventions applied — not generic positions
- [ ] PCB base built line by line; every doubtful benefit flagged with its exposure (under-deduction watch)
- [ ] Every figure has a payroll-register source reference; none typed from memory
- [ ] All six CHECKs run and stated; output not presented as final if any fails
- [ ] Every formula constant / relief / scale band tagged `[verify]` with the year stated
- [ ] Additional remuneration run through the separate method
- [ ] Category, KA, and TP1 reliefs traced to the employee declaration

## What this skill does NOT do

- File CP39 or remit PCB (that's a gated action).
- Compute EPF/SOCSO/EIS (run `/employment-tax:statutory-contributions`).
- Assert PCB formula constants, reliefs, or scale rates as settled fact — it flags them for verification.
- Silently exclude a doubtful benefit from the base — it flags and quantifies the employer exposure.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer the workbook export, the statutory contributions (`/employment-tax:statutory-contributions`), benefit valuation (`/employment-tax:bik-perquisites`), or the deadline view as natural next steps.

---
name: tax-provision
description: >
  Prepare the current and deferred tax provision under MFRS 112 / IAS 12 for the
  financial statements — current tax from the computation, deferred tax from
  temporary differences with a deferred-tax proof, the tax reconciliation (effective
  rate), and the disclosure note. Ties the provision to the computation and the
  trial balance. Use for "tax provision", "deferred tax", "ASC 740 / IAS 12 / MFRS 112",
  "tax note", "effective tax rate reconciliation".
argument-hint: "[entity / period] [computation + accounts + prior-year deferred tax working]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Tax Provision (MFRS 112 / IAS 12)

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md; if enabled and no active matter, ask which matter before doing substantive work.

## Purpose

Produce the tax figures the financial statements need, reconciled and tied: the **current tax** charge (from the income tax computation), the **deferred tax** movement (from temporary differences, proven against opening and closing balances), the **tax reconciliation** that explains the effective rate, and the **disclosure note** in MFRS 112 / IAS 12 form. Every number ties to the computation, the trial balance, or the prior-year deferred-tax working.

This is the bridge between the tax computation and the accounts. It does not invent figures — current tax comes from the computation; deferred tax comes from the carrying-amount-vs-tax-base differences in the accounts.

## Precondition: load the profile + the inputs

Read `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md` first (bounce to cold-start or "provisional" if placeholder, per the standard precondition). Then confirm you have:

1. **The current-year tax computation** (gives the current tax charge). If not done, offer to run `/corporate-tax:tax-computation` first — the provision depends on it.
2. **The financial statements / trial balance** (carrying amounts of assets and liabilities).
3. **The prior-year deferred tax working** (opening deferred tax balances — the proof reconciles to these).
4. **The capital allowance / tax-base detail** (tax bases of fixed assets — the largest temporary difference for most companies).
5. **The deferred tax rate** — the rate expected to apply when the difference reverses, for the **stated period**, tagged `[rate — verify for the reversal period]`.

## Workflow

### Step 1 — Current tax

Take the current tax charge from the computation (tax payable on chargeable income for the YA). State it with the source (the computation's bottom line) and the YA. CHECK: current tax here = tax payable in the computation. Add any prior-year (over)/under-provision separately, sourced to the difference between last year's provision and the agreed/filed assessment.

### Step 2 — Identify temporary differences

For each asset/liability, compute **carrying amount (accounts) − tax base = temporary difference**. Source the carrying amount to the TB/accounts and the tax base to the tax computation / CA schedule. The usual drivers:

- **Fixed assets:** carrying amount (cost − accounting depreciation) vs tax written-down value (residual expenditure after CA). Usually a **taxable** temporary difference → deferred tax liability.
- **Provisions** not yet deductible (deductible when incurred/paid): **deductible** temporary difference → deferred tax asset.
- **Unabsorbed losses / unabsorbed CA carried forward:** deferred tax asset — **only to the extent recovery is probable** (MFRS 112 recognition test). This is a `[review]` judgment, not an automatic recognition. State the basis for probability and flag it.
- **Unrealised items, fair-value adjustments, leases (MFRS 16), revaluations** as applicable.

List each with: item, carrying amount (source), tax base (source), temporary difference, type (taxable/deductible).

### Step 3 — Deferred tax balances and the proof

Apply the deferred tax rate to closing temporary differences → **closing deferred tax** balance. Then build the **deferred-tax proof** (the reconciliation that makes this skill trustworthy):

```
Opening deferred tax (per prior-year working)        [source: PY working]   CHECK A
+/- movement recognised in P&L                       [the deferred tax charge/credit]
+/- movement recognised in OCI / equity              [revaluations, etc.]
+/- rate-change adjustment                            [if the rate changed — verify]
= Closing deferred tax (per Step 3 calc)             [source: this working]  CHECK B
```

CHECK A: opening balance ties to the prior-year working. CHECK B: the proof's closing balance equals the balance computed from closing temporary differences × rate. If the proof doesn't close, the deferred tax charge is wrong — say so; don't plug it.

### Step 4 — Tax reconciliation (effective rate)

Explain why the total tax charge differs from accounting profit × statutory rate:

```
Profit before tax × statutory rate [verify for YA]                 = [a]
+ tax effect of non-deductible expenses (add-backs)                = [b]
- tax effect of non-taxable income                                 = [c]
+/- deferred tax not recognised / rate differences / PY adjustments= [d]
= Total tax charge (current + deferred)                            = [e]   CHECK C
```

CHECK C: the reconciliation's total = current tax (Step 1) + deferred tax movement to P&L (Step 3). The reconciling items should trace to the add-backs/deductions in the computation — they are the same differences, viewed from the accounts side.

### Step 5 — Disclosure note

Draft the MFRS 112 / IAS 12 note: tax expense components (current, deferred, PY adjustment), the reconciliation, deferred tax balances by component, and the unrecognised deferred tax asset (if any) with the reason. State each MFRS 112 reference `[verify against the current standard]` — disclosure requirements are revised.

## Output format

```
[WORK-PRODUCT HEADER]

# Tax Provision: [Entity] — [period]

## Bottom line
Total tax charge RM [e] (current RM [x], deferred RM [d]). Effective rate [%].
Deferred tax [liability/asset] RM [b]. Proof closes: [yes / NO]. Recognition judgments: [N] flagged `[review]`.

## Current tax            [Step 1, tied to computation]
## Temporary differences  [Step 2 table, each side sourced]
## Deferred tax proof     [Step 3, with CHECK A and CHECK B]
## Tax reconciliation     [Step 4, with CHECK C]
## Disclosure note        [Step 5, MFRS 112 references flagged]

## CHECK
A opening ties · B proof closes · C reconciliation ties — pass/fail each
```

## Quality checks before delivering

- [ ] Current tax = computation tax payable (CHECK)
- [ ] Each temporary difference has carrying amount AND tax base, both sourced
- [ ] Deferred-tax proof closes (opening + movement = closing)
- [ ] Reconciliation total = current + deferred to P&L
- [ ] Deferred tax asset recognition treated as a `[review]` judgment, not automatic
- [ ] Rate tagged for verification, with the reversal period stated

## What this skill does NOT do

- Decide whether a deferred tax asset is recoverable — it surfaces the judgment and the evidence; the reviewer decides.
- Assert the statutory or deferred rate as fact — both are flagged for the relevant period.
- Substitute for the auditor's or adviser's review of the provision.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`.

# Employment Tax (Payroll)

The employer's payroll-tax obligations — monthly tax deduction (PCB/MTD), EPF / SOCSO / EIS contributions, benefit-in-kind and perquisite valuation, the employer return (Form E / CP8D) and EA statements, and tax clearance for departing employees — Malaysia-first, built on the `claude-for-tax` robustness spine. It is the **employer side**; the employee's own return is `personal-tax`.

> **Every output is a draft for review by a qualified tax adviser.** It is not a filing or remittance position you can rely on without checking. The employer carries the liability for under-deducted PCB and under-remitted contributions, so getting this wrong on the low side is the dangerous direction. Tax law changes — PCB constants, reliefs, and the EPF/SOCSO/EIS rates and ceilings move, sometimes mid-year — so anything recalled from training is `[model knowledge — verify]` until confirmed against the MTD rules, the EPF/PERKESO schedules, or current LHDN guidance.

## Setup first

```
/plugin install employment-tax@claude-for-tax
# restart Claude Code
/employment-tax:cold-start-interview
```

The interview learns your conventions (PCB method, employee categories, which benefits go into the PCB base, contribution setup, remittance/filing calendar) and writes them to `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. Every skill reads it. Skipping setup is the main reason a skill produces generic output.

## Commands

| Command | What it does |
|---|---|
| `/employment-tax:cold-start-interview` | Learn your payroll function and write the profile (run first) |
| `/employment-tax:pcb-computation` | Compute monthly PCB/MTD — base built line by line, normal + additional-remuneration formulas, six CHECK tie-outs, under-deduction watch |
| `/employment-tax:statutory-contributions` | EPF / SOCSO / EIS — employer and employee portions by band, age, and citizenship, tied to the remittance total |
| `/employment-tax:bik-perquisites` | Value BIK, perquisites, VOLA, and ESOS — taxable/exempt line on every item, what enters the PCB base and the EA |
| `/employment-tax:employer-return-review` | Tie Form E / CP8D to the payroll and the year's CP39s, reconcile the EA statements, filing gate |
| `/employment-tax:tax-clearance` | SPC for leavers — CP21 / CP22A windows and the withholding obligation on final pay |
| `/employment-tax:deadline-tracker` | PCB / EPF / SOCSO / EIS remittances, Form E / EA, and leaver-notification windows with penalty-aware warnings |
| `/employment-tax:customize` | Tune the profile without a full re-interview |
| `/employment-tax:matter-workspace` | Manage per-employer matters (payroll bureaus only) |
| scheduled | `deadline-watcher` — weekly remittance + deadline digest to your channel |

## The disciplines this plugin enforces

1. **Figures trace and tie.** No number is typed from memory. Each amount carries a payroll-register reference; each computation carries CHECK cells reconciling PCB and contributions to the register and the remittance total.
2. **The employer carries the liability — under-deduction is the dangerous error.** A benefit silently left out of the PCB base, a contribution category set too low, or final pay released before clearance are employer exposures. Every skill that builds the PCB base or a contribution surfaces and quantifies the under-deduction risk rather than resolving it away — and never pads the deduction "to be safe" either; the answer to doubt is flag-and-verify.
3. **Authorities are verified, not assumed.** Every PCB constant, relief, rate, ceiling, and deadline is tagged `[verify]` with the period stated, because they change and a confident wrong rate is worse than a gap.

## What this plugin does NOT do

- Remit PCB or contributions, file Form E, issue EA statements, or obtain the SPC — preparation and review only; these are the user's gated actions.
- Assert PCB constants, contribution rates, ceilings, or deadlines as settled fact — it flags them for verification.
- Decide a borderline taxable/exempt characterisation for you — it surfaces both with the employer exposure quantified.
- Replace a qualified tax adviser's review.
- Handle cross-border / shadow-payroll cases without the jurisdiction-recognition flag firing.

## Connectors

Configured in `.mcp.json`: Google Drive (pull payroll registers / TP1/TP3 / EA forms / prior filings), Slack (remittance and deadline alerts). All optional — skills fall back to paste/upload and say so rather than failing silently.

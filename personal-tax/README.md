# Personal Tax

Individual income tax computation and the self-assessment return (Form BE / Form B) — Malaysia-first, built on the `claude-for-tax` robustness spine. Residence is established first because it drives the whole computation; every figure traces to a source document (EA form, statements, relief receipts) and ties back; every rate, relief cap, and statutory reference is flagged for verification against a primary source.

> **Every output is a draft for review by a qualified tax adviser.** It is not a filing position you can rely on without checking. On self-assessment the figures are the taxpayer's own representation, and the signing taxpayer is responsible. Tax law changes every Budget — reliefs, caps, and rates move every year — so anything recalled from training is `[model knowledge — verify]` until confirmed against the ITA 1967, a Public Ruling, a gazette order, or current LHDN guidance.

## Setup first

```
/plugin install personal-tax@claude-for-tax
# restart Claude Code
/personal-tax:cold-start-interview
```

The interview learns your conventions (relief checklist and evidence standard, BIK/perquisite treatment, how you establish residence, reporting-standard threshold, deadline calendar) and writes them to `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`. Every skill reads it. Skipping setup is the main reason a skill produces generic output.

## Commands

| Command | What it does |
|---|---|
| `/personal-tax:cold-start-interview` | Learn your practice and write the profile (run first) |
| `/personal-tax:tax-computation` | Build the computation: residence → income sources → total income → (less reliefs) chargeable income → tax on the scale → (less rebates, PCB, instalments) → balance, every line sourced, six CHECK tie-outs |
| `/personal-tax:employment-income` | s.13 employment income from the EA form — salary, BIK and perquisites, ESOS, gratuity — with the taxable/exempt line drawn on every benefit |
| `/personal-tax:reliefs-rebates` | The relief checklist (capped and evidenced) and rebates (s.6A, zakat/fitrah), with joint-vs-separate assessment surfaced |
| `/personal-tax:return-review` | Tie the Form BE/B to the computation, check reliefs and the PCB credit, review residence and declaration boxes, filing gate |
| `/personal-tax:deadline-tracker` | Compute Form BE / Form B / CP500 / balance-of-tax deadlines with penalty-aware, verify-against-LHDN warnings |
| `/personal-tax:customize` | Tune the profile without a full re-interview |
| `/personal-tax:matter-workspace` | Manage per-taxpayer matters (private practice only) |
| scheduled | `deadline-watcher` — weekly deadline digest to your channel |

## The two disciplines this plugin enforces

1. **Figures trace and tie.** No number is typed from memory. Each amount carries a source reference (EA-form box, statement line, relief receipt); each computation carries CHECK cells reconciling to the source documents or the return total. The PCB credit ties to the EA form, not a payslip estimate. A working paper that doesn't tie is not presented as final.
2. **Authorities are verified, not assumed.** Every rate, relief cap, threshold, and deadline is tagged `[verify]` with the year of assessment stated, because Malaysian individual tax reliefs and rates change every Budget and a confident wrong cap is worse than a gap.

## What this plugin does NOT do

- File returns or pay tax — preparation and review only; filing is the user's gated action.
- Assert Malaysian rates, relief caps, or deadlines as settled fact — it flags them for verification.
- Decide a borderline residence or taxable/exempt characterisation for you — it surfaces both for adviser judgment.
- Replace a qualified tax adviser's review.
- Handle non-Malaysian or dual-resident individuals without the jurisdiction-recognition flag firing.

## Connectors

Configured in `.mcp.json`: Google Drive (pull EA forms / statements / relief receipts / prior returns), Slack (deadline alerts). All optional — skills fall back to paste/upload and say so rather than failing silently.

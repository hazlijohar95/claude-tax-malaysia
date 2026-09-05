# Corporate Tax

Company income tax computation and the MFRS 112 / IAS 12 tax provision — Malaysia-first, built on the `claude-for-tax` robustness spine. Every figure traces to a source document and ties back to the computation; every rate and statutory reference is flagged for verification against a primary source.

> **Every output is a draft for review by a qualified tax adviser.** It is not a filing position you can rely on without checking. The signing preparer or taxpayer is responsible. Tax law changes every Budget — anything recalled from training is `[model knowledge — verify]` until confirmed against the ITA 1967, a Public Ruling, a gazette order, or current LHDN guidance.

## Setup first

```
/plugin install corporate-tax@claude-for-tax
# restart Claude Code
/corporate-tax:cold-start-interview
```

The interview learns your conventions (add-back checklist, CA treatment, carried-forward tracking, reporting-standard threshold, deadline calendar) and writes them to `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`. Every skill reads it. Skipping setup is the main reason a skill produces generic output.

## Commands

| Command | What it does |
|---|---|
| `/corporate-tax:cold-start-interview` | Learn your practice and write the profile (run first) |
| `/corporate-tax:tax-computation` | Build the computation: PBT → adjusted → statutory → chargeable income → tax payable, every line sourced, five CHECK tie-outs |
| `/corporate-tax:tax-provision` | MFRS 112 / IAS 12 current + deferred tax, deferred-tax proof, effective-rate reconciliation, disclosure note |
| `/corporate-tax:capital-allowances` | Schedule 3 CA schedule — QE, IA/AA, balancing adjustments, residual expenditure carried forward |
| `/corporate-tax:return-review` | Tie the Form C to the computation, check carried-forward balances and credits, review disclosure boxes, filing gate |
| `/corporate-tax:deadline-tracker` | Compute Form C / CP204 / CP204A / instalment deadlines with penalty-aware, verify-against-LHDN warnings |
| `/corporate-tax:customize` | Tune the profile without a full re-interview |
| `/corporate-tax:matter-workspace` | Manage per-entity matters (private practice only) |
| scheduled | `deadline-watcher` — weekly deadline digest to your channel |

## The two disciplines this plugin enforces

1. **Figures trace and tie.** No number is typed from memory. Each amount carries a source reference; each computation carries CHECK cells reconciling to the trial balance, the accounts, or the return total. A working paper that doesn't tie is not presented as final.
2. **Authorities are verified, not assumed.** Every rate, threshold, section, and deadline is tagged `[verify]` with the year of assessment stated, because Malaysian tax law changes annually and a confident wrong cite is worse than a gap.

## What this plugin does NOT do

- File returns or pay tax — preparation and review only; filing is the user's gated action.
- Assert Malaysian rates, thresholds, or deadlines as settled fact — it flags them for verification.
- Replace a qualified tax adviser's review, or an auditor's review of the provision.
- Handle non-Malaysian entities without the jurisdiction-recognition flag firing.

## Connectors

Configured in `.mcp.json`: Google Drive (pull TB / accounts / prior returns), Slack (deadline alerts). All optional — skills fall back to paste/upload and say so rather than failing silently.

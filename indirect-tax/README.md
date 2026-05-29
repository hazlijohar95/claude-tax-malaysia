# Indirect Tax (SST)

Sales tax and service tax (SST) determination, registration, return review, and e-invoicing readiness — Malaysia-first, on the `claude-for-tax` robustness spine. Every taxability conclusion names the standard it meets and flags its authority for verification, because the taxable groups, rates, and exemptions change by gazette order.

> **Every output is a draft for review by a qualified tax adviser.** It is not a position you can submit on without checking. Anything recalled from training is `[model knowledge — verify]` until confirmed against the Sales Tax Act 2018, the Service Tax Act 2018, the relevant gazette order, or current RMCD guidance.

## Setup first

```
/plugin install indirect-tax@claude-for-tax
# restart Claude Code
/indirect-tax:cold-start-interview
```

The interview learns your registration profile, your recorded taxability positions, the exemptions you rely on, your reporting standard, and your SST-02 calendar, and writes them to `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md`. Every skill reads it.

## Commands

| Command | What it does |
|---|---|
| `/indirect-tax:cold-start-interview` | Learn your practice and write the profile (run first) |
| `/indirect-tax:taxability-determination` | Is this supply taxable / exempt / out of scope, at what rate, with the standard it meets |
| `/indirect-tax:registration-check` | Test taxable turnover against the threshold for each group; liability date and deadline |
| `/indirect-tax:sst-return-review` | Tie the SST-02 to the listing, check exemptions and reliefs, submission gate |
| `/indirect-tax:einvoice-check` | MyInvois structural readiness check on an invoice or template |
| `/indirect-tax:customize` | Tune the profile without a full re-interview |
| `/indirect-tax:matter-workspace` | Manage per-client matters (private practice only) |

## The two disciplines this plugin enforces

1. **Scope before rate, conditions before exemption.** A service that isn't in a prescribed taxable group is out of scope and has no rate; an exemption with unmet conditions is not an exemption. The plugin checks these in order and won't skip to a rate.
2. **Figures trace and tie.** Output tax is recomputed from the listing and tied to the SST-02; every figure carries a source reference. A working that doesn't tie is not presented as final.

## What this plugin does NOT do

- Submit returns or register the business with RMCD — preparation and review only; submission is the user's gated action.
- Assert taxable groups, rates, thresholds, or exemptions as settled fact — it flags them for verification.
- Confirm an invoice's tax treatment via the readiness check (that's `taxability-determination`).
- Handle non-Malaysian VAT/GST without the jurisdiction-recognition flag firing.

## Connectors

Configured in `.mcp.json`: Google Drive (pull listings / invoices / prior returns), Slack (reminders). All optional — skills fall back to paste/upload and say so.

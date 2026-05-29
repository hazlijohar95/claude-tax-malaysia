# International Tax & Transfer Pricing

Transfer pricing documentation, arm's-length review, related-party characterisation, cross-border withholding and treaty analysis, and BEPS Pillar Two screening — Malaysia-first (ITA s.140A, the TP Rules, LHDN guidance) with the OECD Guidelines as the international reference, on the `claude-for-tax` robustness spine.

> **Every output is a draft for review by a qualified tax / transfer-pricing adviser.** This is the fastest-moving area in tax — treaty rates differ treaty by treaty, and Pillar Two rules and effective dates have moved repeatedly. Anything recalled from training is `[model knowledge — verify]`, and **the plugin will never invent comparables or an arm's-length range** — those require a real benchmarking study.

## Setup first

```
/plugin install international-tax@claude-for-tax
# restart Claude Code
/international-tax:cold-start-interview
```

The interview learns your group structure, controlled transactions, methods, treaties, and CbCR/Pillar Two status, and writes them to `~/.claude/plugins/config/claude-for-tax/international-tax/CLAUDE.md`.

## Commands

| Command | What it does |
|---|---|
| `/international-tax:cold-start-interview` | Learn the group and your practice; write the profile (run first) |
| `/international-tax:related-party-review` | Inventory and characterise controlled transactions; triage docs + WHT |
| `/international-tax:tp-documentation` | Local File / Master File — overview, FAR, method selection, economic analysis around a study |
| `/international-tax:arms-length-review` | Pressure-test a benchmarking study — method fit, comparability, range, audit exposure |
| `/international-tax:withholding-tax` | WHT on a cross-border payment, with treaty relief (treaty in hand) |
| `/international-tax:treaty-analysis` | Apply a specific DTA — residence, PE, governing article, anti-abuse |
| `/international-tax:pillar-two-check` | Screen GloBE / top-up tax applicability (not the computation) |
| `/international-tax:customize` | Tune the profile without a full re-interview |
| `/international-tax:matter-workspace` | Manage per-client matters (private practice only) |

## The disciplines this plugin enforces

1. **Never fabricate comparables or a range.** Arm's-length pricing is the output of a real benchmarking study against a real database. With no study, the plugin structures the search and the functional analysis but refuses to manufacture comparables — because fabricated comparables are indefensible on audit.
2. **Arm's length is a range, not a point.** Conclusions are stated as a range with a justified point and the standard the *method and characterisation* meet.
3. **Currency is paramount.** No treaty rate, threshold, or Pillar Two rule is asserted from memory — every one is flagged for verification with the year stated, because this area changes fastest.
4. **The specific treaty, not the model.** Treaty answers are anchored to the actual treaty text; a Model-only structure is labelled as such and every conclusion flagged.

## What this plugin does NOT do

- Invent comparables, benchmark ranges, or treaty rates — it flags what needs a study or the treaty text.
- Compute the GloBE top-up tax (the Pillar Two skill is a screen; the computation is a separate specialist exercise).
- File documentation or remit withholding tax.
- Decide method, characterisation, or treaty entitlement silently — it flags the calls.

## Connectors

`.mcp.json`: Google Drive (agreements, financials, group charts), Slack (reminders). A benchmarking database (Orbis / RoyaltyRange / etc.) is recommended — without one, no comparables search is possible and the plugin will say so rather than guess.

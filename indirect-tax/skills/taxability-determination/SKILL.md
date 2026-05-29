---
name: taxability-determination
description: >
  Determine whether a supply is taxable under the Sales Tax Act 2018 or Service Tax
  Act 2018 — is it within scope, is it a prescribed taxable service group, what rate,
  does an exemption apply — against the business's recorded positions in
  `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md`. States the standard
  the conclusion meets and flags every authority for verification. Use for "is this
  taxable", "do we charge SST on this", "is this service in scope", "does the exemption apply".
argument-hint: "[describe the supply: what, to whom, where] [any contract/invoice]"
---

# Taxability Determination (SST)

## Matter context

Check `## Matter workspaces`; if enabled with no active matter, ask which before proceeding.

## Purpose

Give a fast, defensible answer to "is this taxable, and at what rate" — sized to the question (a clear case gets three sentences; an uncertain one gets the competing treatments and the standard each meets). The answer always states the year/period and flags the authority for verification, because the taxable groups, rates, and exemptions change by gazette order.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md` (bounce to cold-start or "provisional" if placeholder). The recorded positions and exemptions there are the starting point — but a recorded position is a view to confirm, not a settled fact.

## Workflow

### Step 1 — Characterise the supply
Pin down: **what** is supplied (good or service), **by whom** (registered? for which group?), **to whom** (B2B/B2C, related party, recipient's location), **where** performed/consumed, and **when** (which taxable period — drives the applicable order). If any of these is unclear, ask — the answer often turns on one of them. Don't guess the recipient or the place of supply.

### Step 2 — Scope and classification
- **Sales tax:** is it a taxable good (manufactured/imported, not exempt under the relevant order)? `[verify against the Sales Tax (Goods Exempted) order and the rate order for the period]`
- **Service tax:** is it a **prescribed taxable service** within a gazetted group, provided by a registered person above the threshold? A service that isn't in a prescribed group is **out of scope** — say so plainly. `[verify against the Service Tax Regulations / the prescribed-services order for the period]`

State the classification and the basis, tagged. Where the business has a recorded position for this supply, cite it and confirm it still holds.

### Step 3 — Rate and exemptions
State the rate for the period `[rate — verify per the current rate order]`. Check any exemption the business relies on (raw-material exemption, intra-group / B2B service-tax exemption, professional-services exemption) and its **conditions** — an exemption with unmet conditions is not an exemption. Flag condition-dependence `[review]`.

### Step 4 — Conclusion with the standard
State: taxable / exempt / out of scope, the rate if taxable, and **the reporting standard the conclusion meets** (will / should / MLTN / review). Where it's below the firm's threshold, flag `[review]` and say what would lift it (a Customs ruling, a clearer gazette basis). Where the place of supply, the recipient, or the classification is genuinely uncertain, surface both treatments — don't pick one silently.

## Output format

```
[WORK-PRODUCT HEADER]
# Taxability: [the supply] — [period]
## Bottom line — [Taxable at X% / Exempt (condition: …) / Out of scope]. Standard: [will/should/MLTN/review].
## How I got there — scope → classification → rate → exemption, each with basis `[verify]`
## What would change the answer — [the fact(s) the conclusion turns on]
## Open items — [`[review]` judgment calls, if any]
```

Size it down for a clear case: a short paragraph with the one caveat that matters, still tagged and still naming the standard.

## Quality checks
- [ ] Supply characterised on all five axes (what/who-supplies/who-receives/where/when) before concluding
- [ ] Scope checked before rate (an out-of-scope service has no rate)
- [ ] Exemption conditions stated, not assumed met
- [ ] Conclusion names the reporting standard and the period
- [ ] Every authority/rate/group tagged for verification

## What this skill does NOT do
- Assert taxable groups, rates, or exemptions as settled fact — it flags them. - Issue or substitute for a Customs ruling. - Replace a qualified adviser's review on an uncertain position.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs` — offer to draft a determination memo, a ruling-request, or feed the result into `/indirect-tax:sst-return-review`.

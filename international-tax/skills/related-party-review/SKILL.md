---
name: related-party-review
description: >
  Identify and characterise a group's controlled (related-party) transactions — who's
  related, what flows between them, the direction and value, whether a written intercompany
  agreement exists, and which need TP documentation. Builds the transaction inventory that
  drives everything else. Use for "map our related-party transactions", "which transactions
  need TP docs", "characterise this intercompany transaction".
argument-hint: "[group chart + financials / intercompany ledgers]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Related-Party Transaction Review

## Purpose

Build the inventory of controlled transactions — the foundation for documentation, withholding, and Pillar Two analysis. Missing or mischaracterising a transaction is how a group ends up under-documented and exposed.

## Precondition

Read the profile for the group structure. You need the group chart and the financials / intercompany ledgers. Source every related party and every flow.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

### Step 1 — Who is related
Identify the related parties (control/ownership per the TP Rules definition `[verify]`). Flag any borderline relationship `[review]` — the relatedness test determines whether the TP rules even apply.

### Step 2 — What flows
For each pair, list the transactions: tangible goods, services (management, technical, IT, shared), financing (loans, guarantees, cash pooling), IP/royalties, cost contribution. Direction and value, each sourced to the ledger/financials. Flag any flow with no clear business substance `[review]`.

### Step 3 — Agreement and characterisation
For each material transaction: is there a written intercompany agreement? (No agreement is a 🟠 finding.) How is it characterised, and is the characterisation consistent with conduct (post-BEPS, substance over the contract)? Flag characterisation calls `[review]`.

### Step 4 — Documentation & withholding triage
For each: does it require TP documentation (materiality threshold `[verify]`)? Does it carry a withholding exposure (royalties, interest, technical fees cross-border)? Route the WHT ones to `/international-tax:withholding-tax`. Produce the inventory with these flags.

## Output format
```
[WORK-PRODUCT HEADER]
# Related-Party Transactions: [group] — [year]
## Transaction inventory   [parties · type · direction · value (sourced) · agreement? · TP docs? · WHT?]
## Flagged   [`[review]`: borderline relatedness, no agreement, weak substance, characterisation]
## Next   [which need documentation / a WHT check]
```

## Quality checks
- [ ] Relatedness tested against the rules definition (flagged for verification)
- [ ] Every flow sourced to the ledger/financials
- [ ] Missing intercompany agreements flagged
- [ ] Documentation and WHT triage applied per transaction

## What this skill does NOT do
- Price the transactions (that's documentation + a study).
- Assert the relatedness/materiality thresholds from memory.
- Decide characterisation silently — it flags the calls.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

---
name: withholding-tax
description: >
  Determine Malaysian withholding tax on a cross-border payment — characterise the payment
  (royalty, interest, technical/service fee, etc.), find the domestic WHT rate, then check
  whether a double tax agreement reduces it and on what conditions. Requires the specific
  treaty in hand. Use for "do we withhold on this payment", "WHT on royalty to [country]",
  "withholding tax rate", "treaty relief".
argument-hint: "[describe the payment: type, payer, payee, country] [the relevant treaty if available]"
---

# Withholding Tax Determination

## Purpose

Answer "do we withhold, and how much" on a cross-border payment — correctly characterised, at the right domestic rate, reduced by the right treaty rate only where the treaty actually applies. Wrong WHT is both an under-deduction exposure and a deductibility risk for the payer.

## Precondition

Read the profile. You need the payment details (type, payer, payee, payee's country and residence) and, for treaty relief, **the specific treaty** — WHT treaty rates vary treaty by treaty and cannot be asserted generically.

## Workflow

### Step 1 — Characterise the payment
What is it for tax purposes — royalty, interest, fees for technical services, rental of movable property, contract payment, dividend? Characterisation drives both the domestic rate and the treaty article. Flag a borderline characterisation `[review]` (e.g., software payment as royalty vs business income — a frequent dispute).

### Step 2 — Domestic WHT rate
State the domestic WHT rate for that payment type under the ITA (e.g., s.109 / s.109B `[verify the section and the current rate]`). **Do not assert the rate from memory** — confirm against the current Act/guidance or flag it. Note any domestic exemption.

### Step 3 — Treaty relief
Is the payee a resident of a treaty country (residence, not just location — may need a certificate of residence)? Does a DTA apply and reduce the rate? **State the treaty rate only from the actual treaty text** — if you don't have it, say "the [country] treaty may reduce this; I need the treaty text to state the rate — `[treaty unretrieved — verify]`." Check beneficial ownership and any limitation-on-benefits/anti-treaty-shopping condition `[review]`.

### Step 4 — Conclusion & mechanics
The rate to withhold (domestic vs treaty, with the basis), the conditions for treaty relief (CoR, beneficial ownership), the remittance deadline `[verify]`, and the consequence of getting it wrong (penalty + the payer's deduction at risk). Name the standard the conclusion meets.

## Output format
```
[WORK-PRODUCT HEADER]
# WHT: [payment] from [payer] to [payee, country]
## Bottom line — withhold [X]% [domestic / treaty rate] — standard: [settled / strong / arguable / doubtful]
## Characterisation / Domestic rate `[verify]` / Treaty relief (treaty in hand? rate · conditions) / Mechanics & deadline
```

## Quality checks
- [ ] Payment characterised before any rate; borderline characterisation flagged
- [ ] Domestic rate and section tagged for verification (not asserted from memory)
- [ ] Treaty rate stated ONLY from the actual treaty; otherwise flagged as needing the text
- [ ] Beneficial ownership / residence conditions surfaced
- [ ] Remittance deadline and consequence stated

## What this skill does NOT do
- Remit the WHT.
- Assert a treaty rate without the treaty in hand.
- Decide a borderline characterisation silently.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

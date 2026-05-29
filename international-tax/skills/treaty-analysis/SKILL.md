---
name: treaty-analysis
description: >
  Apply a double tax agreement to a cross-border situation — test treaty residence and
  tie-breakers, whether a permanent establishment exists, which article governs the income,
  the treaty rate or relief, and any limitation-on-benefits / principal-purpose condition.
  Requires the specific treaty text. Use for "apply the [country] treaty", "is there a PE",
  "does the treaty cover this", "treaty residence".
argument-hint: "[the situation: parties, countries, income, activities] [the treaty text]"
---

# Treaty Analysis

## Purpose

Work a double tax agreement properly — residence, PE, the governing article, the rate/relief, and the anti-abuse conditions — for the *specific* treaty, not a generic OECD model. Treaties differ article by article; an answer from "the model treaty" is a wrong answer waiting to happen.

## Precondition

Read the profile. You need the situation and **the actual treaty text**. If you don't have it, say so first: "Treaty answers depend on the specific treaty's wording, which varies. I need the [country] DTA text to do this properly — paste it or connect a source. I can frame the questions against the OECD Model as a structure, but every conclusion will be tagged `[Model — verify against the actual treaty]`." Do not state treaty conclusions from a generic model as if they were the treaty.

## Workflow

### Step 1 — Treaty residence
Is each party a resident of a contracting state for treaty purposes? Apply the tie-breaker if dual-resident. A certificate of residence is usually needed to claim benefits `[verify]`.

### Step 2 — Permanent establishment (if relevant)
Does the activity create a PE under the treaty's PE article (fixed place, dependent agent, the specific time thresholds for construction/services PE in *this* treaty)? PE existence changes everything downstream. Flag the judgment `[review]`.

### Step 3 — Governing article & relief
Which distributive article applies (business profits, dividends, interest, royalties, technical fees, capital gains, employment)? What rate cap or exemption does it give, and on what conditions? Quote the article. Where the treaty has a technical-fees article (many Malaysian treaties do), apply it rather than defaulting to the model's silence.

### Step 4 — Anti-abuse
Check the limitation-on-benefits and/or principal-purpose test (post-MLI, many treaties carry a PPT) `[verify whether the MLI modified this treaty]`. Beneficial ownership for dividends/interest/royalties. Flag any treaty-shopping risk `[review]`.

### Step 5 — Conclusion
The treaty outcome, the conditions to claim it, the documentation needed (CoR, forms), and the standard the conclusion meets — all anchored to the quoted treaty text.

## Output format
```
[WORK-PRODUCT HEADER]
# Treaty Analysis: [country] DTA — [situation]
## Treaty in hand?   [yes — analysed against text | NO — Model structure only, every conclusion `[verify]`]
## Residence / PE / Governing article & relief / Anti-abuse / Conclusion (standard + conditions)
```

## Quality checks
- [ ] Worked against the actual treaty text, or clearly flagged as Model-only
- [ ] Residence and (where relevant) PE tested before the rate
- [ ] Governing article quoted; technical-fees article applied where the treaty has one
- [ ] MLI / PPT / beneficial-ownership conditions checked
- [ ] Conclusion anchored to quoted text, with the standard named

## What this skill does NOT do
- State a treaty outcome from a generic model as if it were the treaty. - Assert MLI modifications from memory. - Issue a residence certificate.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

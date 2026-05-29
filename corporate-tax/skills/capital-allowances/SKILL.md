---
name: capital-allowances
description: >
  Build the capital allowance schedule under Schedule 3 of the Income Tax Act 1967 —
  qualifying expenditure, initial and annual allowances, balancing charges/allowances
  on disposal, and residual expenditure carried forward — from the fixed-asset register
  and prior-year CA schedule. Every asset traced; every rate and class flagged for
  verification. Use for "capital allowances", "CA schedule", "balancing charge".
argument-hint: "[entity / YA] [fixed-asset register + prior-year CA schedule]"
---

# Capital Allowances (Schedule 3 ITA 1967)

## Purpose

Produce the CA schedule the computation needs: current-year qualifying expenditure, allowances claimed, disposals with balancing adjustments, and residual expenditure carried forward — each asset traced to the register and tied to the prior-year schedule.

## Precondition

Read the profile. You need the **fixed-asset register** (additions, disposals, descriptions, cost) and the **prior-year CA schedule** (opening residual expenditure and the rates previously applied). Without the prior-year schedule, opening residual expenditure cannot be carried — flag it, don't assume.

## Workflow

### Step 1 — Classify qualifying expenditure
For each addition, determine whether it is qualifying plant & machinery expenditure and which class/rate applies. **Classification and rates are not asserted from memory** — tag each `[class & rate — verify against Schedule 3 / the relevant Rules for YA <year>]`. Non-qualifying items (e.g., items where the qualifying-expenditure rules exclude them) are listed separately with the reason. Small-value-asset and special-rate treatments per the team's convention from the profile, flagged for verification.

### Step 2 — Compute allowances per asset
Initial allowance (on additions) + annual allowance (on residual expenditure), per the applicable rates `[verify]`. Show the rate used for each. Carry the team's pooling/asset-by-asset convention from the profile.

### Step 3 — Disposals and balancing adjustments
For each disposal: disposal value vs residual expenditure → balancing allowance (disposal value < RE) or balancing charge (disposal value > RE, capped at allowances given). Source disposal values to the register/agreement. Flag any disposal where the value or date is uncertain `[review]`.

### Step 4 — Residual expenditure carried forward
Closing residual expenditure per asset and in total. CHECK: opening RE (prior schedule) + additions − allowances − disposals = closing RE. The schedule must tie to the prior year.

### Step 5 — Feed the computation
Total CA for the year (current + brought-forward unabsorbed CA, capped at adjusted income) for the statutory-income step, and unabsorbed CA carried forward separately with its continuity conditions flagged `[review]`.

## Output format
A per-asset table (Asset | Source ref | QE | Class/rate `[verify]` | IA | AA | Balancing adj | Closing RE) plus totals, the opening→closing CHECK, and the figure to carry into the computation. Lead with the reviewer note.

## Quality checks
- [ ] Every asset traced to the register; opening RE tied to prior schedule
- [ ] Every class and rate tagged for verification with the YA
- [ ] Balancing charges capped at allowances given; disposals sourced
- [ ] Opening + additions − allowances − disposals = closing RE (CHECK)

## What this skill does NOT do
- Decide whether expenditure qualifies as a settled fact — it flags classification for verification. - Assert Schedule 3 rates from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

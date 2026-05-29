---
name: reliefs-rebates
description: >
  Build the personal reliefs and rebates schedule for an individual — work through the
  relief checklist (self, spouse, child, EPF + life, medical, education, lifestyle, SSPN,
  parental care, disability, etc.), apply the cap and condition for each, then the rebates
  (s.6A, zakat/fitrah, departure levy) — against the team's evidence standard in
  `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`. Every claim traced to a
  retained receipt; every cap and threshold tagged for verification because they change every
  Budget. Use for "what reliefs can be claimed", "build the relief schedule", "is this
  deductible as a relief", "s.6A rebate".
argument-hint: "[name / YA] [the relief receipts / statements, or describe the claims]"
---

# Reliefs & Rebates

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip. If enabled, load the active matter's `matter.md` and write outputs there.

## Purpose

Produce the reliefs-and-rebates schedule that takes total income down to chargeable income and then tax charged down to the balance — each relief carrying its cap, condition, and the retained evidence; each rebate carrying its threshold. The output is honest about which claims are evidenced and which are not, because an unevidenced relief is the thing that fails on audit.

This skill does not assert relief caps from memory. **Caps and thresholds change every Budget — every amount is `[verify for YA <year>]`.**

## Precondition: load the profile

**Read `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`** for the team's relief checklist and **evidence standard** (a relief without a retained receipt is flagged, not claimed). If missing or placeholder, redirect to `/personal-tax:cold-start-interview`, or proceed `[PROVISIONAL]` against generic Malaysian relief categories with every cap flagged.

## Precondition: residence

Reliefs and rebates are (generally) available only to **resident** individuals. Confirm residence (from the computation or `/personal-tax:tax-computation` Step 0) before building the schedule. For a non-resident, state that reliefs do not apply rather than listing them.

## Inputs required

1. **The relief receipts / evidence** — the source for each claim (a claim without evidence is flagged).
2. **The relief categories the individual is claiming** — or the life facts to work out eligibility (spouse income, children and their status, dependents, disability status).
3. **The year of assessment** — drives every cap.
4. **Zakat / fitrah receipts and any departure levy** — for the rebate step.

## Workflow

### Step 1 — Work the relief checklist

For each relief category in the profile's checklist, capture:

```
**[Relief]** — RM [amount claimed]  (cap RM [cap] for YA [year] `[model knowledge — verify]`)
Evidence: [receipt index / statement] — or `[review — no evidence retained]`
Condition: [eligibility — e.g., child in full-time tertiary education; medical for serious illness; self vs spouse] `[verify]`
Status: [claimed / restricted to cap / not claimed — reason]
```

Standard categories to walk (a FLOOR, not a ceiling — add any the facts raise):
- Self and dependent relatives; **spouse** (and the joint-vs-separate-assessment question `[review]`).
- **Child** relief (by age/education status, disabled child).
- **EPF + life insurance / takaful** (note the split caps and that employee EPF comes from the employment-income step) `[verify]`.
- **Medical** (serious illness, parents' medical, full medical check-up, fertility) `[verify]`.
- **Education** (self, and the SSPN net deposit) `[verify]`.
- **Lifestyle** (books, devices, internet, sports — watch for a single item exhausting the cap) `[verify]`.
- **Parental care**, **disability** (self/spouse/child), **PRS / deferred annuity**, and any YA-specific reliefs `[verify]`.

**Each cap and condition is `[verify for YA <year>]`.** Do not state a cap from memory as fact. Where a claim has no retained evidence, flag `[review — no evidence]` — surface it, don't silently include or exclude it.

### Step 2 — Joint vs separate assessment (if a spouse)

Where there's a spouse, the joint-vs-separate-assessment choice changes the reliefs available and the tax. Flag it `[review]`, state the factors (each spouse's income, who claims the children, the spouse relief), and offer to compute both ways rather than assuming one. Do not silently pick.

### Step 3 — Total reliefs → chargeable income

Sum the reliefs (each at the lower of claimed and cap) and show:

```
Total income                                          [from the computation]
  - total reliefs (Step 1, each capped)               [verify caps for YA]
= Chargeable income
```

### Step 4 — Rebates (after the tax-on-the-scale step)

Apply rebates against the tax charged, not against income:

```
Tax on chargeable income                              [from the computation]
  - s.6A rebate                  [ONLY if chargeable income within the YA threshold] `[verify threshold]`
  - zakat / fitrah rebate        [to the extent of tax charged, with receipt]
  - departure levy rebate        [if applicable, with evidence]
= Tax charged after rebates
```

The s.6A rebate is conditional on chargeable income being within the threshold for the YA `[verify]` — state the threshold and whether it's met. Zakat is a rebate (against tax), distinct from the donation deduction — don't confuse the two.

### Step 5 — Tie and assemble

CHECK that each relief is at the lower of claimed and cap, that unevidenced claims are flagged, and that rebates are applied against tax (not income). State the total reliefs and total rebates with the chargeable-income and tax impact.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Reliefs & Rebates: [Name] — YA [year]

## Bottom line
Total reliefs RM [r] (→ chargeable income RM [ci]). Rebates RM [rb].
[N] claims unevidenced and flagged. [Joint/separate assessment: flagged for decision].

## Reliefs schedule
[the Step 1 blocks — each with cap, evidence, condition, status]

## Assessment basis (if spouse)
[joint vs separate — factors and the `[review]` flag]

## Rebates
[the Step 4 block — s.6A threshold test, zakat/fitrah, departure levy]

## Open items for your judgment
[unevidenced claims; the assessment-basis choice; any borderline eligibility]

## CHECK
- Each relief at lower of claimed and cap: ✓/✗
- Unevidenced claims flagged: ✓/✗
- Rebates applied against tax, not income: ✓/✗
- s.6A applied only if chargeable income within threshold: ✓/✗
```

## Quality checks before delivering

- [ ] Residence confirmed before reliefs applied (non-resident → not applicable)
- [ ] Every relief carries its cap `[verify for YA]` and its evidence (or a flag)
- [ ] Unevidenced claims flagged `[review]`, not silently included
- [ ] Joint-vs-separate assessment surfaced where a spouse exists
- [ ] s.6A rebate gated on the chargeable-income threshold
- [ ] Zakat treated as a rebate, not confused with the donation deduction

## What this skill does NOT do

- Assert relief caps or rebate thresholds as settled fact — it flags every one for verification for the YA.
- Decide the joint-vs-separate assessment for you — it surfaces it for decision.
- Build the full computation (run `/personal-tax:tax-computation`).

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer to feed the schedule into `/personal-tax:tax-computation` or to compute joint vs separate both ways.

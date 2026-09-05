---
name: bik-perquisites
description: >
  Value benefits-in-kind, perquisites, and living accommodation (VOLA) for an employee — and
  handle ESOS / share-scheme perquisites — to determine what enters the PCB base and the EA
  statement, against the team's conventions in
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. The taxable/exempt line is
  drawn on every item, prescribed-method vs formula valuation is stated, and each doubtful
  inclusion carries the employer's under-deduction exposure. Every valuation basis and exemption
  is flagged for verification. Use for "value the company car BIK", "is this allowance taxable",
  "VOLA on the accommodation", "ESOS perquisite", "what goes on the EA form".
argument-hint: "[employee / year] [the benefit details, ESOS records, or paste them]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# BIK & Perquisites Valuation

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip — skills use practice-level context. If enabled, load the active employer's `matter.md` and write outputs there.

## Purpose

Produce the valuation of each benefit, perquisite, and accommodation that an employer must put into the PCB base and report on the EA statement — with the taxable/exempt line drawn explicitly, the valuation method named, and each uncertain inclusion flagged with the employer's under-deduction exposure. This is the employer-reporting counterpart to `personal-tax:employment-income` (which is the employee's own-return view).

This skill does not invent prescribed BIK values or exemption amounts. **They are gazetted / set by Public Ruling and change — every valuation basis is `[verify for <year>]`.**

## Precondition: load the profile

**Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`** for the team's BIK/perquisite treatment, which benefits go into the PCB base, and the VOLA convention. If missing or placeholder, redirect to `/employment-tax:cold-start-interview`, or proceed `[PROVISIONAL]` against generic Malaysian defaults with every valuation flagged.

## Inputs required

1. **The benefit details** — for each benefit: what it is, the cost to the employer, the period provided, shared/sole use, and any employee contribution toward it.
2. **Accommodation details** — for VOLA: the type, the defined value / rent, and the period.
3. **ESOS / share-scheme records** — grant date, vesting/exercisable date, exercise date, offer price, and market value at the relevant date.
4. **The year** — drives the prescribed values and exemption amounts.

## Workflow

### Step 1 — Classify each item: perquisite vs BIK vs accommodation

- **Perquisite (s.13(1)(a))** — cash or convertible-to-cash benefits (allowances, bill reimbursements, club memberships paid, etc.).
- **Benefit-in-kind (s.13(1)(b))** — non-convertible benefits provided (car, fuel, driver, household appliances, etc.), valued by the prescribed method or the formula method.
- **Living accommodation / VOLA (s.13(1)(c))** — valued by its own rule.

State the head for each item and the authority `[model knowledge — verify]`.

### Step 2 — Value each item

```
**[Item]** — value RM [x] for the period
Head: [s.13(1)(a) perquisite | s.13(1)(b) BIK | s.13(1)(c) VOLA]
Valuation method: [prescribed value | formula (cost ÷ prescribed lifespan) | defined value for VOLA] `[verify for year]`
Less employee contribution: RM [c]   [if any]
= taxable amount RM [t]
Source: [benefit record / cost invoice]
```

For BIK, state which valuation method was used and why (the prescribed-value table vs the cost-based formula) — the choice changes the amount, and the rates/lifespans are `[verify]`. For VOLA, state the basis (defined value vs a percentage of remuneration, whichever rule applies) `[verify]`.

### Step 3 — Draw the taxable/exempt line

For every allowance and reimbursement, decide explicitly:

```
**[Item]** — RM [amount]
Treatment: [taxable perquisite | exempt — [basis] | partly exempt — RM [x] exempt, RM [y] taxable]
Authority: [PR / gazette exemption order] `[model knowledge — verify]`
[review] — where the call is uncertain, carry BOTH treatments AND the under-deduction exposure:
  "if taxable, this RM [x] belongs in the PCB base; leaving it out under-deducts ~RM [y] PCB — employer exposure"
```

Common judgment calls (flag, don't resolve silently): petrol/travel allowance vs exempt official-duties reimbursement; phone/internet; medical vs non-medical; subsidised vs free; the perquisite-vs-tool-of-trade line. **Exemption amounts and conditions are `[verify for <year>]`.**

### Step 4 — ESOS / share-scheme perquisite

The share-scheme perquisite (s.13(1)(a)) arises and is valued at the prescribed point — typically the **earlier of the date the option is exercisable and the date exercised** `[model knowledge — verify]`. Establish:
- The relevant date and why.
- The perquisite value = (market value at that date − offer/exercise price) × shares `[verify the valuation rule]`.
- Whether and when it enters the PCB base and the EA statement.

If the dates or values aren't documented, flag it `[review]` — do not assume a date.

### Step 5 — What enters the PCB base and the EA statement

Summarise: the total taxable BIK/perquisite/VOLA that must be (a) included in the PCB base for the relevant month(s) — hand to `/employment-tax:pcb-computation` — and (b) reported on the EA statement at year end. State anything excluded and why, with the under-deduction exposure if the exclusion is doubtful.

### Step 6 — Tie-out (CHECK cells)

- **CHECK 1:** Every item classified by head (a)/(b)/(c) with its authority. ✓/✗
- **CHECK 2:** Valuation method stated for each; rates/lifespans/defined values tagged `[verify]`. ✓/✗
- **CHECK 3:** Taxable/exempt line drawn on every allowance; doubtful calls flagged with exposure. ✓/✗
- **CHECK 4:** ESOS valued at the correct prescribed date, or flagged if undocumented. ✓/✗
- **CHECK 5:** Taxable totals carried to both the PCB base and the EA statement consistently. ✓/✗

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# BIK & Perquisites: [Employee] — [year]

## Bottom line
Total taxable benefits RM [t] (RM [e] treated as exempt across [N] items). To PCB base: RM [p]. To EA statement: RM [t].
[N]🔴 [N]🟠 [N]🟡 flagged. Under-deduction exposure on doubtful inclusions: RM [x].

## Valuation
[the Step 2–3 blocks — head, method, taxable amount, source]

## ESOS / share scheme
[the Step 4 determination — date, value, PCB/EA treatment]

## To PCB and EA
[the Step 5 summary — what's in the base, what's on the EA, what's excluded and why]

## Open items for your judgment
[each `[review]`: the item, both treatments, the standard each meets, the under-deduction exposure]

## CHECK
[the Step 6 reconciliations, pass/fail]
```

## Quality checks before delivering

- [ ] Every item classified by head with its authority `[verify]`
- [ ] Valuation method named for each; prescribed values/lifespans tagged `[verify for year]`
- [ ] Taxable/exempt line drawn explicitly; doubtful calls flagged with the under-deduction exposure
- [ ] ESOS valued at the correct prescribed date, or flagged if undocumented
- [ ] Taxable totals consistent between the PCB base and the EA statement

## What this skill does NOT do

- Assert prescribed BIK values, VOLA rules, or exemption amounts as settled fact — it flags them for verification.
- Decide a borderline taxable/exempt characterisation for you — it surfaces both with the employer exposure.
- Build the PCB computation or the EA/Form E (run `/employment-tax:pcb-computation` or `/employment-tax:employer-return-review`).

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer to feed the taxable totals into `/employment-tax:pcb-computation` or the employer return review.

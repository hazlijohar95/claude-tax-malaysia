---
name: tax-computation
description: >
  Build a Malaysian company income tax computation from the trial balance and
  accounts — profit before tax → adjusted income → statutory income → aggregate
  income → total income → chargeable income → tax payable — against the team's
  conventions in `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`.
  Every figure is traced to a source document and tied back to the accounts; every
  rate and section is tagged for verification. Use for "do the tax comp", "compute
  the tax", "tax computation for [entity] YA [year]".
argument-hint: "[entity / YA] [path to trial balance and accounts, or paste them]"
---

# Tax Computation

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the in-house default), skip this — skills use practice-level context. If enabled with no active matter, ask which matter, load its `matter.md`, and write outputs to the matter folder.

## Purpose

Produce a company income tax computation a reviewer can sign off in one pass: every line traced to a source, every adjustment carrying its reason and authority, every total tied back to the accounts, and the tax charge stated with the year of assessment and the rate it used (tagged for verification).

This skill does not invent numbers. If a figure isn't in a source document in front of you, it is asked for, not guessed.

## Precondition: load the profile

**Before touching the numbers, read `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`.** If missing or placeholder:

> You haven't configured your practice profile yet — that's how I tailor add-back conventions, CA treatment, reporting standard, and deadlines.
>
> - Run `/corporate-tax:cold-start-interview` (2 min) to configure, then I'll compute against YOUR conventions.
> - Or say **"provisional"** and I'll compute against generic Malaysian defaults (resident company, standard add-backs from first principles), tag everything `[PROVISIONAL — configure your profile]`, and flag every rate/threshold for verification.

## Inputs required

State what you need up front; don't start a comp on half the inputs:

1. **Trial balance** for the period (the source of every figure).
2. **The accounts / financial statements** (to tie profit before tax and read the notes).
3. **Prior-year tax computation + CA schedule** (for brought-forward losses, unabsorbed CA, residual expenditure, and continuity of treatment).
4. **The year of assessment and basis period** (drives every rate and deadline).

If any are missing, say which and what it blocks. A computation without the prior-year CA schedule cannot carry residual expenditure forward — flag it, don't assume zero.

## Workflow

### Step 0 — Build the source map (do this before any arithmetic)

Read the trial balance and list, line by line, how each account will be treated: taxable income / non-taxable / deductible / non-deductible add-back / capital (→ CA) / below-the-line. Give every line a **source reference** (TB account code or accounts caption). This map is the spine of the tie-out — every later figure points back to a row here. If a line's treatment is uncertain, mark it `[review]` and carry the competing treatments; do not silently pick one.

### Step 1 — Start from profit before tax, and tie it

Take **profit before tax per the audited/management accounts** as the starting point. State the figure with its source (accounts page / TB). This is CHECK #1: the starting PBT in the computation must equal the PBT in the accounts. If you can't tie it, stop and reconcile before going further.

### Step 2 — Adjustments (add-backs and deductions)

Work through the source map. For each adjustment produce:

```
**[Item]** — [add back / deduct] RM [amount]
Source: [TB code / accounts note]
Reason: [why — e.g., "depreciation: non-deductible; CA claimed separately"]
Authority: [s.33 / s.39(1)(l) entertainment / Schedule 3 / Public Ruling X] `[model knowledge — verify]`
Standard met: [will / should / MLTN / review] — [only where the treatment is a judgment call]
```

- **Always run the team's standard add-back checklist** from the profile (depreciation, non-deductible provisions, s.39 restrictions, donations, fines/penalties, leave passage, etc.). A clean list still states "checked, none applicable."
- **Capital vs revenue** and **wholly-and-exclusively** calls that aren't clear-cut are flagged `[review]` with both treatments — never silently resolved.
- Tag every section/Public Ruling reference. **Do not state a deduction restriction or a rate from memory as fact** — flag it for verification against the ITA / the relevant Public Ruling for this YA.

### Step 3 — Capital allowances

Pull the CA position from the prior-year CA schedule (residual expenditure, brought-forward unabsorbed CA) and the current-year additions/disposals. For anything beyond a summary, hand off: "Want me to run `/corporate-tax:capital-allowances` for the full schedule?" Rates and qualifying-expenditure classifications are tagged `[verify against Schedule 3 / the relevant rules for YA <year>]`. Carry CA into the statutory income step, not the adjusted income step.

### Step 4 — Build the statutory layers

Lay out, per the team's house format:

```
Profit before tax                                    [tie to accounts]
  +/- adjustments (Step 2)
= Adjusted income (business source)
  - capital allowances (current + b/f, capped at adjusted income)   [s.42 / Sch 3 — verify]
= Statutory income (business)
  + statutory income (other sources)
= Aggregate income
  - current-year business loss / approved donations (s.44)          [verify ordering & limits]
= Total income
  - [any further reliefs]
= Chargeable income
```

Each layer states its figure and the rule that governs the step, tagged `[verify]`. Unabsorbed losses and unabsorbed CA carried **forward** (not deducted this year) are listed separately with the carry-forward conditions flagged `[review]` (time limits and shareholding-continuity tests change and must be confirmed for the YA).

### Step 5 — Tax payable

Apply the rate for the **stated YA** to chargeable income. **The rate is not asserted from memory** — establish the YA, confirm the company's rate band (SME band conditions, or the standard rate) against current guidance or flag it, and tag the figure `[rate — verify for YA <year>]`. Show: gross tax, any rebates/set-offs, instalments paid per CP204 (from source), and the **balance of tax payable / repayable**.

### Step 6 — Tie-out (CHECK cells — non-negotiable)

Before assembling, run and state the reconciliations:

- **CHECK 1:** Starting PBT = PBT per accounts. ✓/✗
- **CHECK 2:** Sum of every adjustment = (chargeable-income build − PBT) for the business source. ✓/✗
- **CHECK 3:** Every TB line appears in the source map exactly once (nothing dropped, nothing double-counted). ✓/✗
- **CHECK 4:** Brought-forward losses / unabsorbed CA agree to the prior-year computation (and ideally the latest agreed assessment, not the management figure). ✓/✗
- **CHECK 5:** Instalments deducted = CP204 instalments per the source record. ✓/✗

If any CHECK fails, the reviewer note's **Tie-out** line says so and the output is NOT presented as final. A computation that doesn't tie is not done.

### Step 7 — Assemble

Prepend the work-product header (per profile `## Outputs`, conditional on role). Lead with the reviewer note (Sources / Read / Tie-out / Flagged / Currency / Before relying). Then the bottom line, then the computation, then the open items.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Tax Computation: [Entity] — YA [year] (basis period [dates])

## Bottom line
Chargeable income RM [x]. Tax payable RM [y] (rate [z]% `[verify for YA]`).
Balance [payable/repayable] RM [b] after CP204 instalments.
[N]🔴 [N]🟠 [N]🟡 [N]🟢 items flagged. Ties out: [yes / NO — see CHECK n].

## Computation
[the statutory build from Step 4, with a source ref on every line]

## Adjustments detail
[the Step 2 blocks]

## Carried forward
[unabsorbed losses / CA / s.44(6) excess, with conditions flagged `[review]`]

## Open items for your judgment
[each `[review]` item: the question, the competing treatments, the standard each meets]

## CHECK
[the Step 6 reconciliations, pass/fail]
```

## Integration

If a document store is connected, offer to pull the TB/accounts/PY computation by name instead of pasting, and to write the finished working paper (with a `Sources` sheet and CHECK cells) to the house folder. Do not file anything — preparing a computation is not filing a return.

**Before any step that files or submits:** if Role is Non-professional, gate it — "Filing binds the company. Have you had this reviewed by a qualified tax adviser? If yes, proceed. If no, here's a one-page brief to bring to them: [chargeable income, the flagged positions and the standard each meets, the open items]." Do not proceed past the gate without an explicit yes.

## Quality checks before delivering

- [ ] Profile loaded and conventions applied — not generic positions
- [ ] Every figure has a source reference; none typed from memory
- [ ] All six CHECKs run and stated; output not presented as final if any fails
- [ ] Every rate/section/threshold tagged for verification with the YA stated
- [ ] Judgment calls flagged `[review]` with competing treatments, not silently resolved
- [ ] Brought-forward balances traced to the prior computation, not the management figure

## What this skill does NOT do

- File the return (that's a gated action; see `/corporate-tax:return-review` for pre-filing review).
- Assert Malaysian rates, thresholds, or restrictions as settled fact — it flags them for verification.
- Replace a qualified adviser's review of the positions taken.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer the workbook export, the provision (`/corporate-tax:tax-provision`), the CA schedule, or the return review as natural next steps.

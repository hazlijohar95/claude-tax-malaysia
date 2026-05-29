---
name: tax-computation
description: >
  Build a Malaysian individual income tax computation from the EA/EC form, income
  statements, and relief receipts — aggregate income → total income → (less reliefs)
  chargeable income → tax on the scale → (less rebates, PCB, set-offs, instalments) →
  balance payable/repayable — against the team's conventions in
  `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`. Residence status is
  established first because it drives the whole computation. Every figure is traced to a
  source document and tied back; every rate, relief cap, and section is tagged for
  verification. Use for "do the personal comp", "compute the individual tax",
  "tax computation for [name] YA [year]".
argument-hint: "[name / YA] [path to EA form, statements, and relief receipts, or paste them]"
---

# Tax Computation (Individual — Form BE / Form B)

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the individual/one-return default), skip this — skills use practice-level context. If enabled with no active matter, ask which matter, load its `matter.md`, and write outputs to the matter folder.

## Purpose

Produce an individual income tax computation a reviewer can sign off in one pass: residence established and stated first, every income source traced to a source document, every relief carrying its cap and evidence, every total tied back, and the tax charge stated with the year of assessment and the rate basis it used (tagged for verification).

This skill does not invent numbers. If a figure isn't in a source document in front of you, it is asked for, not guessed. It does not assert a relief cap from memory.

## Precondition: load the profile

**Before touching the numbers, read `~/.claude/plugins/config/claude-for-tax/personal-tax/CLAUDE.md`.** If missing or placeholder:

> You haven't configured your practice profile yet — that's how I tailor relief conventions, BIK treatment, reporting standard, and deadlines.
>
> - Run `/personal-tax:cold-start-interview` (2 min) to configure, then I'll compute against YOUR conventions.
> - Or say **"provisional"** and I'll compute against generic Malaysian defaults (resident individual, standard relief categories from first principles), tag everything `[PROVISIONAL — configure your profile]`, and flag every rate/cap/threshold for verification.

## Inputs required

State what you need up front; don't start a comp on half the inputs:

1. **The EA / EC form** (employment income, BIK, EPF, PCB deducted — the source of the employment figures and the tax credit).
2. **Income statements** for other sources (dividend vouchers, rental income and expenses, interest, pension) as applicable.
3. **Relief receipts / evidence** for the reliefs being claimed (a relief without evidence is flagged, not claimed).
4. **Prior-year return / computation** (for continuity, brought-forward business losses on a Form B, and to sanity-check residence and reliefs claimed).
5. **The year of assessment** (drives every rate, relief cap, and deadline) and the **residence facts** (day-count) if not already in a document.

If any are missing, say which and what it blocks. A computation that claims reliefs without the receipts cannot be presented as final — flag the unevidenced reliefs, don't assume them.

## Workflow

### Step 0 — Establish residence (do this before any rate)

Determine residence under s.7 ITA from the day-count and linked-period tests `[model knowledge — verify]`. State the basis and the conclusion. **This is the gateway:** resident → progressive scale rates and access to reliefs/rebates; non-resident → flat rate (Form M) and generally no reliefs. If the day-count is borderline or the facts are incomplete, flag it `[review]` and do not silently assume resident. Residence is re-established every YA — state the YA.

### Step 1 — Build each income source, and tie it

For each source the individual has, compute the statutory income and give every figure a **source reference**:

- **Employment (s.13):** gross salary, bonuses, BIK and perquisites, less allowable expenses. Read these from the EA form. BIK/perquisite *characterisation* (taxable perquisite vs exempt reimbursement) that isn't clear-cut is flagged `[review]` with both treatments — hand off to `/personal-tax:employment-income` for the full build. **CHECK:** employment income used = EA form figure.
- **Business/profession (s.4(a)) — Form B:** adjusted income from the accounts, capital allowances, brought-forward losses (traced to the prior return/agreed assessment, not the management figure).
- **Rent (s.4(d)), dividends, interest, pension:** per the statements, with the source line for each.

### Step 2 — Aggregate to total income

Lay out, per the team's house format:

```
Statutory income — employment (s.13)                 [tie to EA form]
  + statutory income — business (s.4(a))              [Form B only]
  + statutory income — other sources (rent, etc.)
= Aggregate income
  - current-year business loss / approved donations (s.44)   [verify ordering & limits]
= Total income
```

Each layer states its figure and the rule that governs the step, tagged `[verify]`. Unabsorbed business losses and CA carried **forward** (Form B) are listed separately with the carry-forward conditions flagged `[review]`.

### Step 3 — Reliefs → chargeable income

Apply the reliefs the individual is entitled to, working the team's relief checklist from the profile. For each:

```
**[Relief]** — RM [amount claimed]
Source / evidence: [receipt index / EA form / statement] — [or `[review — no evidence]` if unevidenced]
Cap for YA [year]: RM [cap] `[model knowledge — verify]`
Conditions: [eligibility conditions] `[verify]`
```

- **Run the team's standard relief checklist** (self, spouse, child, EPF + life, medical, education, lifestyle, SSPN, parental care, disability…). A relief not claimed still states "not claimed — [reason]".
- **Every cap and condition is `[verify for YA <year>]`** — caps change every Budget. Do not state a relief amount from memory as fact.
- A relief without retained evidence is flagged `[review — no evidence]`, never silently claimed.
- Non-resident: reliefs generally do not apply — state this, don't apply them.

```
Total income
  - reliefs (Step 3, each capped)                     [verify caps for YA]
= Chargeable income
```

### Step 4 — Tax on the scale

Apply the rate for the **stated YA** and the **residence basis** to chargeable income. **The rate is not asserted from memory** — establish the YA, apply the resident progressive scale or the non-resident flat rate, and tag the figure `[scale/rate — verify for YA <year>]`. Show the tax before rebates.

### Step 5 — Rebates, set-offs, and credits → balance

```
Tax on chargeable income (Step 4)
  - rebates (s.6A — if chargeable income within threshold; zakat/fitrah; departure levy)  [verify caps/thresholds for YA]
  - s.110 set-off / foreign tax credit                [if applicable, with source]
= Tax charged
  - PCB / MTD deducted                                [tie to EA form]
  - CP500 instalments paid                            [Form B — tie to payment record]
= Balance of tax payable / repayable
```

The s.6A rebate is only available where chargeable income is within the threshold for the YA `[verify]` — state the threshold and whether it's met. PCB and instalments are read from source records, not estimated.

### Step 6 — Tie-out (CHECK cells — non-negotiable)

Before assembling, run and state the reconciliations:

- **CHECK 1:** Employment income used = EA/EC form figure. ✓/✗
- **CHECK 2:** Every income source has a source document; none typed from memory. ✓/✗
- **CHECK 3:** Each relief claimed is within its YA cap and has retained evidence (or is flagged). ✓/✗
- **CHECK 4:** PCB credit = EA form PCB figure; CP500 instalments = payment record. ✓/✗
- **CHECK 5:** Residence basis stated and consistent with the rate applied (resident scale vs non-resident flat). ✓/✗
- **CHECK 6:** Brought-forward business losses/CA (Form B) agree to the prior return / agreed assessment, not the management figure. ✓/✗

If any CHECK fails, the reviewer note's **Tie-out** line says so and the output is NOT presented as final. A computation that doesn't tie is not done.

### Step 7 — Assemble

Prepend the work-product header (per profile `## Outputs`, conditional on role). Lead with the reviewer note (Sources / Read / Tie-out / Flagged / Currency / Before relying). Then the bottom line, then the computation, then the open items.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Tax Computation: [Name] — YA [year] ([Form BE / Form B], [resident / non-resident])

## Bottom line
Chargeable income RM [x]. Tax charged RM [y] ([resident scale / non-resident flat] `[verify for YA]`).
Balance [payable/repayable] RM [b] after PCB RM [p] and instalments RM [i].
[N]🔴 [N]🟠 [N]🟡 [N]🟢 items flagged. Ties out: [yes / NO — see CHECK n].

## Residence
[the Step 0 determination, basis, and YA]

## Computation
[the income → total → reliefs → chargeable → tax → balance build, source ref on every line]

## Reliefs claimed
[the Step 3 blocks — each with cap, evidence, conditions]

## Carried forward
[Form B only — unabsorbed losses / CA, with conditions flagged `[review]`]

## Open items for your judgment
[each `[review]` item: the question, the competing treatments, the standard each meets]

## CHECK
[the Step 6 reconciliations, pass/fail]
```

## Integration

If a document store is connected, offer to pull the EA form / statements / PY return by name instead of pasting, and to write the finished working paper (with a `Sources` sheet and CHECK cells) to the house folder. Do not file anything — preparing a computation is not filing a return.

**Before any step that files or submits:** if Role is Non-professional, gate it — "Filing binds you and the balance is payable on filing. Have you had this reviewed by a qualified tax adviser? If yes, proceed. If no, here's a one-page brief to bring to them: [chargeable income, the flagged positions and the standard each meets, the unevidenced reliefs]." Do not proceed past the gate without an explicit yes.

## Quality checks before delivering

- [ ] Profile loaded and conventions applied — not generic positions
- [ ] Residence established and stated before any rate applied
- [ ] Every figure has a source reference; none typed from memory
- [ ] All six CHECKs run and stated; output not presented as final if any fails
- [ ] Every rate/relief cap/threshold tagged for verification with the YA stated
- [ ] Reliefs without evidence flagged `[review]`, not silently claimed
- [ ] PCB credit and instalments traced to source records, not estimated

## What this skill does NOT do

- File the return (that's a gated action; see `/personal-tax:return-review` for pre-filing review).
- Assert Malaysian rates, relief caps, or scale bands as settled fact — it flags them for verification.
- Replace a qualified adviser's review of the positions taken or the residence conclusion.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer the workbook export, the employment-income build (`/personal-tax:employment-income`), the relief schedule (`/personal-tax:reliefs-rebates`), or the return review as natural next steps.

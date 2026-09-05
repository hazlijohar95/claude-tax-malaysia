---
name: registration-check
description: >
  Check whether the business is required to register for sales tax or service tax —
  test taxable turnover against the threshold for each relevant taxable group, identify
  the liability date, and flag the registration deadline. Use for "do we need to register
  for SST", "are we over the SST threshold", "service tax registration".
argument-hint: "[taxable turnover by supply type / period] [or point at the listing]"
---

# Registration Check (SST)

## Purpose

Tell the business whether — and from when — it must register, based on its taxable turnover against the threshold for each relevant taxable group. Late registration carries exposure, so the liability date and the registration deadline matter as much as the yes/no.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md` for current registration status and the taxable groups in play. You need the taxable turnover (by supply type / taxable service group) over the relevant look-back period — from the listing or stated by the user (verify if stated).

## Workflow

### Step 1 — Identify the relevant regime and group
Sales tax (manufacturer/importer of taxable goods) or service tax (provider of a prescribed taxable service), and **which taxable group** — the threshold is per group, and what counts as taxable turnover differs. Tag the group classification `[verify against the current prescribed-services / goods order]`.

### Step 2 — Measure taxable turnover correctly
Include only turnover from taxable supplies in the relevant group, over the prescribed look-back basis. Exclude exempt and out-of-scope supplies. Source the figures to the listing. Flag any supply whose taxability is itself uncertain `[review]` — it changes the turnover test.

### Step 3 — Apply the threshold
Compare to the threshold for the group, **tagged `[verify against current RMCD threshold]`** — thresholds are set by order and change. State the result and, if over, the date liability arose and the registration deadline `[verify against current RMCD guidance]`.

### Step 4 — Conclusion
Required to register (from [date], deadline [date]) / not required (turnover below threshold, monitoring point [figure]) / voluntary registration available. Name the standard the conclusion meets and flag anything condition-dependent.

## Output format
```
[WORK-PRODUCT HEADER]
# SST Registration Check — [business / period]
## Bottom line — [Required from [date] / Not required / Voluntary] — threshold [figure] `[verify]`
## Turnover measured   [Step 2, sourced]
## Threshold test   [Step 3]
## Deadlines & next steps
```

## Quality checks
- [ ] Correct regime and group identified before measuring
- [ ] Only taxable-group turnover counted; figures sourced
- [ ] Threshold tagged for verification; liability date and deadline stated if over
- [ ] Uncertain taxability of any supply flagged (it affects the test)

## What this skill does NOT do
- Register the business with RMCD.
- Assert the threshold or group classification from memory.
- Replace a qualified adviser's confirmation on an uncertain liability date.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

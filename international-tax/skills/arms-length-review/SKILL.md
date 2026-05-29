---
name: arms-length-review
description: >
  Review an arm's-length analysis or benchmarking study — does the method fit the
  functional analysis, are the comparables genuinely comparable, is the range and the
  chosen point defensible, and where is it weak on audit. Reviews a study; does not
  manufacture one. Use for "review the benchmarking", "is this arm's length", "check the
  TP method", "review the comparables".
argument-hint: "[the study / analysis to review] [the related agreements + financials]"
---

# Arm's-Length Review

## Purpose

Pressure-test an arm's-length analysis the way an auditor would. The output tells the adviser where the analysis is strong, where it's weak, and what to fix before it's relied on. It reviews an existing study — it does not invent comparables to fill gaps.

## Precondition

Read the profile. You need the analysis/study to review and the underlying functional analysis and financials. If the "study" is just an asserted range with no comparable set behind it, say so — that is the finding: there is no study to review.

## Workflow

### Step 1 — Method fit
Does the selected method fit the functional analysis and the data? Is the tested party the right one (typically the less complex party)? Is the PLI appropriate for the method and transaction? Flag a mismatch `[review]` — the most common and most damaging weakness.

### Step 2 — Comparability of the comparables
For the comparable set: are they genuinely comparable (industry, functions, size, independence, period)? Were rejection reasons documented? Are there obvious accept/reject inconsistencies? **Do not add comparables from memory** — assess the ones present and identify *criteria* for any that are missing, for the user to run.

### Step 3 — Range and point
Is the range built correctly (interquartile vs full range, per the method/rules `[verify]`)? Is the chosen point justified (median vs a specific point), and is the tested party's result actually within it? Recompute the tested party's PLI from the segmented financials (sourced) and confirm it lands where the study says.

### Step 4 — Audit exposure
Where would LHDN push? Stale comparables, a strained method, an undocumented characterisation, a result at the edge of the range. State each as a finding with severity and the fix.

## Output format
```
[WORK-PRODUCT HEADER]
# Arm's-Length Review: [entity] — [transaction]
## Bottom line — [defensible / weak on [points]]; tested-party result [within / outside] range
## Method fit / Comparability / Range & point (recomputed) / Audit exposure
## Findings   [severity · issue · fix — `[review]`]
```

## Quality checks
- [ ] Method fit tested against the FAR and the tested-party choice
- [ ] Comparables assessed, not supplemented from memory
- [ ] Tested-party PLI recomputed from sourced financials and checked against the range
- [ ] Range construction tagged for verification against the rules

## What this skill does NOT do
- Add or invent comparables. - Bless a range with no study behind it. - Assert the range-construction rules from memory.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

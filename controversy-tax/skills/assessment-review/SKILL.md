---
name: assessment-review
description: >
  Review a notice of assessment or additional assessment — pin the basis, check it against
  the return and the facts, test whether it is time-barred, recompute the disputed amounts,
  and assess each adjustment's defensibility at the standard it meets. Produces the
  decision input for whether to object. Use for "review the assessment", "is this
  assessment right", "they raised an additional assessment".
argument-hint: "<matter-slug> [the notice of assessment + the underlying return/computation]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Assessment Review

## Purpose

Work out whether an assessment is right, wrong, or arguable — and whether it should even have been raised. The output feeds the object/concede decision: every disputed adjustment recomputed from source, each tested for defensibility, and the time-bar question answered.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` and the matter's `matter.md`. You need the notice of assessment and the underlying return/computation and source records. Flag the objection deadline 🔴 at the top `[verify against the notice]`.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

### Step 1 — Pin the basis
Quote what the assessment changed and the reason LHDN gave (adjustment by adjustment). If the basis isn't stated, that itself is a point — note it.

### Step 2 — Time-bar check (do this early)
Test whether the assessment was raised within the statutory window for the year(s) — standard period vs the extended window for fraud/wilful default/negligence (s.91 / s.91A `[verify — confirm the current periods and which applies]`). If it looks time-barred, that may dispose of the matter — flag it 🔴 `[review]` and say it should be confirmed before anything else.

### Step 3 — Recompute each adjustment from source
For each disputed adjustment, recompute the correct figure from the return and source records, traced. Compare to LHDN's figure. State the difference. A figure is never accepted or rejected from memory — it is recomputed from the document.

### Step 4 — Defensibility per adjustment
For each adjustment, assess the taxpayer's position and the standard it meets (settled / strong / arguable / doubtful), with the authority `[verify]`. Separate the adjustments that are plainly wrong (recompute and they fall away), arguable (a real position, named standard), and likely correct (LHDN has it right — concede candidate).

### Step 5 — Bottom line and decision input
Total defensible vs likely-correct exposure. The object/concede recommendation flagged `[review]` for the person with settlement authority, with the deadline restated.

## Output format
```
[WORK-PRODUCT HEADER]
# Assessment Review: [taxpayer] — [matter], YA [years]
## Objection deadline   [🔴 date `[verify]`]
## Time bar   [within window / POSSIBLY TIME-BARRED — `[review]`]
## Adjustment-by-adjustment   [basis quoted · recomputed from source · standard · defensible/arguable/concede]
## Exposure   [defensible vs likely-correct, traced]
## Recommendation   [object on [items] / concede [items] — `[review]`]
```

## Quality checks
- [ ] Objection deadline flagged first
- [ ] Time-bar tested early and flagged if arguable
- [ ] Every adjustment recomputed from source, not accepted/rejected from memory
- [ ] Each position tagged with the standard it meets
- [ ] Object/concede flagged `[review]`, not decided

## What this skill does NOT do
- File the objection (that's `objection-appeal`).
- Decide whether to object.
- Assert the time-bar period or a rate from memory — flags them for verification.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

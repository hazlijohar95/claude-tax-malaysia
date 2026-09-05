---
name: penalty-analysis
description: >
  Analyse penalty exposure on an assessment and the arguments for reduction or remission —
  identify the penalty provision and rate applied, test whether it's correctly imposed,
  and build the reasonable-cause / voluntary-disclosure / remission arguments at the
  standard each meets. Use for "penalty analysis", "can we get the penalty reduced",
  "argue for remission", "s.113 penalty".
argument-hint: "<matter-slug> [the notice / penalty computation]"
---

# Penalty Analysis

## Purpose

Penalties are often the larger number and the more arguable one. This skill pins which penalty provision was applied and at what rate, tests whether it was correctly imposed, and builds the remission/reduction arguments — each at the standard it meets, none asserted from memory.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` and the matter's `matter.md`. You need the notice / penalty computation showing the penalty and its stated basis.

## Workflow

### Step 1 — Pin the penalty
Identify the provision and rate applied (e.g., s.113(2) incorrect return, s.112(3) failure to furnish, s.124 / understatement penalties — `[verify the provision, the current rate, and the framework]`). Quote LHDN's stated basis. **Do not assert the penalty rate or framework from memory** — penalty rates and the concessionary framework change; confirm against current LHDN penalty guidance or flag it.

### Step 2 — Test the imposition
Is the penalty correctly imposed on its own terms? Check: does the conduct actually fall within the provision; is the rate the correct one for the circumstances (first vs repeat, disclosed vs discovered); is it computed on the right base; was the underlying adjustment even correct (if the assessment falls, the penalty may fall with it). Flag each as a potential ground.

### Step 3 — Build the reduction / remission arguments
Per the facts, assess which apply and the standard each meets:
- **Reasonable cause / no negligence** — the facts that support it, sourced.
- **Voluntary disclosure** — if the taxpayer disclosed before discovery, the concessionary rate `[verify the current programme and rate]`.
- **Cooperation / first-time / proportionality** — mitigating factors the framework recognises `[verify]`.
- **The adjustment was arguable** — a position with real authority behind it undercuts a "negligence" characterisation.

Each argument: the facts (sourced), the basis `[verify]`, and the standard it meets. Flag the realistic expected reduction as a `[review]` range, not a promise.

### Step 4 — Recommendation
Whether to argue the penalty separately, the grounds to lead with, and the realistic outcome — flagged `[review]` for the reviewer.

## Output format
```
[WORK-PRODUCT HEADER]
# Penalty Analysis: [taxpayer] — [matter]
## Penalty pinned   [provision · rate · basis quoted — `[verify]`]
## Imposition test   [correctly imposed? grounds to challenge]
## Reduction / remission arguments   [each: facts sourced · basis · standard]
## Recommendation   [argue / accept — `[review]`, with a realistic range]
```

## Quality checks
- [ ] Provision and rate pinned and flagged for verification (not asserted from memory)
- [ ] Imposition tested on its own terms, including whether the underlying adjustment holds
- [ ] Each remission argument's facts sourced and tagged with the standard it meets
- [ ] Expected reduction given as a flagged range, not a promise

## What this skill does NOT do
- Negotiate or file the remission request (it drafts the analysis; the letter is a `--draft` next step).
- Assert penalty rates or the remission framework from memory.
- Promise an outcome.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

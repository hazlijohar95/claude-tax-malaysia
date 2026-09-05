---
name: pillar-two-check
description: >
  Screen whether a group is in scope for BEPS Pillar Two (GloBE) and the Malaysian top-up
  tax rules, and what it must do — revenue-threshold test, in-scope entities, a high-level
  effective-tax-rate read, safe-harbour eligibility, and the registration/filing obligations.
  An applicability SCREEN, not a top-up computation. Use for "are we in Pillar Two",
  "GloBE", "top-up tax", "Pillar Two registration".
argument-hint: "[group revenue + jurisdictions + entity list]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Pillar Two (GloBE) Applicability Screen

## Purpose

Tell a group whether Pillar Two reaches it, which entities/jurisdictions are in scope, roughly where the ETR risk sits, whether a safe harbour applies, and what it must file — so the group doesn't discover it was in scope after a deadline passed. This is a **screen**, not the GloBE computation (which is its own substantial exercise).

## The currency warning (read this first, every time)

**Pillar Two is the fastest-moving area in tax.** The rules, the safe harbours (transitional CbCR safe harbour, QDMTT safe harbour), the Malaysian top-up tax (MTT/DMTT) implementation, and the effective dates have changed repeatedly and continue to. **Nothing in this screen may rely on training knowledge for a threshold, a rate, a safe-harbour condition, or an effective date.** Confirm each against current Malaysian rules and current OECD guidance, or flag it `[verify — Pillar Two changes frequently]`. State the year and say explicitly that the user must confirm currency before relying.

## Precondition

Read the profile for group revenue and structure. You need consolidated group revenue (for the threshold), the jurisdictions with group entities, and ideally CbCR data for the ETR read.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

### Step 1 — Threshold test
Is consolidated group revenue at or above the GloBE threshold (commonly stated as €750m, in the relevant years `[verify the threshold, the look-back, and the MYR equivalent]`)? Below it, the group is generally out of scope — say so and stop (with the verify caveat). At/above, continue.

### Step 2 — In-scope entities and jurisdictions
Identify the constituent entities and the jurisdictions to test. Note excluded entities (governmental, non-profit, pension, investment entities — per the rules `[verify the current exclusions]`), flagged `[review]`.

### Step 3 — High-level ETR read
Using CbCR / financial data (sourced), a rough jurisdictional ETR read to spot where blended ETR may fall below the minimum (commonly 15% `[verify]`) — i.e., where top-up risk concentrates. This is indicative only; the GloBE ETR uses specific adjustments, so flag this as a screen, not the computation.

### Step 4 — Safe harbours
Check eligibility for the transitional CbCR safe harbour and any QDMTT safe harbour for the in-scope jurisdictions `[verify the current conditions and which years they cover]`. A safe harbour may take a jurisdiction out of top-up for a period — material to the conclusion.

### Step 5 — Obligations & conclusion
If in scope: the registration, notification, and GloBE Information Return obligations and their deadlines `[verify]`, plus the Malaysian top-up tax interaction. Conclusion: in/out of scope, where the risk sits, what to file, and the explicit instruction to confirm currency and run the full computation with a specialist.

## Output format
```
[WORK-PRODUCT HEADER]
# Pillar Two Screen: [group] — [year]
## ⚠️ Currency — Pillar Two rules/dates change frequently; every figure below `[verify]` before relying
## Threshold / In-scope entities / ETR read (indicative) / Safe harbours / Obligations
## Bottom line — [in scope / out of scope / below threshold] — confirm currency + run full computation with a specialist
```

## Quality checks
- [ ] Currency warning stated up front; every threshold/rate/date flagged for verification
- [ ] Revenue and ETR data sourced, not assumed
- [ ] Framed as a screen, not the GloBE computation
- [ ] Safe-harbour eligibility checked (and flagged for verification)
- [ ] Obligations and the specialist hand-off stated

## What this skill does NOT do
- Compute the GloBE top-up tax (this is a screen; the computation is a separate specialist exercise).
- Assert Pillar Two thresholds, rates, safe-harbour conditions, or effective dates from memory.
- Conclude in/out of scope without flagging that currency must be confirmed.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

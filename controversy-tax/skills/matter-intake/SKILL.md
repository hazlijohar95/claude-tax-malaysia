---
name: matter-intake
description: >
  Open a new tax controversy matter — capture the taxpayer, the disputing body, the
  assessment or audit, the facts and their sources, and (first) the controlling deadline —
  then write matter.md and history.md and append to the open-matters index. Use for "open
  a matter", "new audit", "new dispute", "we got an assessment / audit letter".
argument-hint: "<matter-slug> [the audit letter / notice of assessment, pasted or a file]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Matter Intake

## Purpose

Open a dispute matter uniformly so nothing is lost and — above all — **the controlling deadline is captured and diarised before anything else.** Intake writes the matter's `matter.md` (facts, assessment, deadlines, exposure) and `history.md` (a dated event log), and adds a row to `## Open matters` in the practice profile.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md`. Matter workspaces are ON for this plugin. Take the matter slug from the argument or ask for one.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

### Step 1 — Deadline first (do this before full intake)
From the audit letter or notice of assessment, identify the controlling deadline (objection window from a notice of assessment under s.99 `[verify — typically 30 days from the date of the notice]`; or the audit-query response date). State it, tag it `[verify against the notice and current procedure]`, and record it at the top of `matter.md` as 🔴. If a notice of assessment is involved, say plainly: "The objection window is a one-way door — if it lapses, the assessment becomes final. Confirm this date against the notice now." Do not bury the deadline below the fact-gathering.

### Step 2 — Capture the matter
Pull from the document(s) and ask only for what's missing:
- **Taxpayer** (name, tax reference, entity type), **disputing body** (LHDN/RMCD), **matter type** (desk/field audit, additional assessment, penalty, refund dispute), **years/periods in dispute**.
- **The assessor's basis** — what is LHDN actually relying on? Quote it from the letter; if it's not stated, flag that pinning the basis is the first substantive task.
- **Exposure** — additional tax and penalties claimed, traced to the notice.
- **Key facts** — each with its **source document**. Do not record a fact you can't source; flag the gap.

### Step 3 — Write the matter files
Write `matters/<slug>/matter.md` (deadline block at top; taxpayer; body; type; years; assessor's basis quoted; exposure; facts-with-sources; open questions; posture overrides if any) and `matters/<slug>/history.md` (one dated line: "matter opened; [deadline] diarised"). Append the index row to `## Open matters` in the practice profile. Set this matter active.

### Step 4 — Orient the user
Confirm what's captured, restate the deadline, and offer the natural next step (brief it, pin the assessor's basis, draft the audit response, or assess the position).

## Output format
A short confirmation: matter opened, the controlling deadline (flagged for verification), exposure, and the open questions — then the decision tree. The detail is in the files; don't dump them back.

## Quality checks
- [ ] Controlling deadline captured FIRST and flagged for verification against the notice
- [ ] Assessor's basis quoted from the document, or the gap flagged
- [ ] Every recorded fact carries a source; unsourced facts flagged not asserted
- [ ] Exposure traced to the notice
- [ ] matter.md + history.md written; index updated; matter set active

## What this skill does NOT do
- Object, appeal, or respond — it opens the matter (use the work skills next).
- Assert the deadline as settled — it flags it for verification against the notice and current procedure.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

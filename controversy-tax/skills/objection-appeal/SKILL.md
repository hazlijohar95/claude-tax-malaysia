---
name: objection-appeal
description: >
  Draft a formal objection to an assessment under s.99 ITA, or an appeal to the Special
  Commissioners of Income Tax (Form Q), against the case theory from the assessment review —
  with a hard deadline gate that will not let the skill proceed without the deadline
  confirmed. Use for "draft the objection", "object to the assessment", "appeal to the SCIT",
  "Form Q".
argument-hint: "<matter-slug> [--appeal for an SCIT appeal instead of an s.99 objection]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Objection / Appeal

## Purpose

Turn the assessment review's case theory into a formal objection or appeal — grounds organised, each ground supported by sourced facts and verified authority, written in the house submission style. The deadline gate is the spine: this skill will not finalise a submission without the controlling deadline confirmed, because the window is a one-way door.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` and the matter's `matter.md`. Ideally `/controversy-tax:assessment-review` has run — if not, say the grounds rest on an un-reviewed assessment and offer to run it first.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## The deadline gate (runs before drafting)

State the controlling deadline and its source:
- **s.99 objection:** within the window from the date of the notice of assessment `[verify — typically 30 days; confirm against the notice and the current section]`.
- **SCIT appeal (Form Q):** within the Schedule 5 window after LHDN's decision/forwarding `[verify]`.

Then: "Confirm the deadline date and that we are within it before I draft. If the window has lapsed, the route is an application for extension of time (s.100/s.131 `[verify]`), not an objection — tell me and I'll draft that instead." **Do not draft the substantive submission until the user confirms the date.** If the deadline is inside [7] days, lead with that and recommend filing a holding objection if the full grounds aren't ready.

## Workflow

### Step 1 — Grounds from the case theory
Take the arguable adjustments from the assessment review. For each, state the **ground** (what's wrong with the assessment), the **facts** that support it (each sourced), and the **authority** `[verify]`. Order grounds strongest-first; lead with a dispositive one (e.g., time bar) if there is one.

### Step 2 — Draft each ground
For each: the assessor's position, the taxpayer's position, the facts (sourced), the authority (quoted/cited, tagged by provenance — never a fabricated or unretrieved cite), and the relief sought. Where a ground is below the firm's reporting standard, flag it `[review]` — including a weak ground can cost credibility on the strong ones.

### Step 3 — Assemble in house style
Per `## House style`: the form/structure for an objection or Form Q, the statement of grounds, the relief sought, and the supporting documents list. Clean external version — no work-product header on what goes to LHDN/SCIT.

### Step 4 — Gate and log
**If Role is Non-professional**, gate before filing: "Filing an objection/appeal is a formal step on a hard deadline with consequences for the matter. Has a qualified tax agent / tax litigator reviewed this? If yes, proceed. If no, here's the brief." Do not finalise for filing past the gate without an explicit yes. Append the filing event and the (new) deadline to the matter.

## Output format
```
[WORK-PRODUCT HEADER — internal working version]
# [Objection under s.99 / Form Q Appeal]: [taxpayer] — [matter]
## Deadline gate   [date confirmed: yes/no — `[verify]`]
## Grounds (strongest first)   [ground · facts sourced · authority · standard]
## Flagged   [weak grounds `[review]`, missing authority]
---
## Draft submission   [clean, external, in house style]
## Supporting documents list
```

## Quality checks
- [ ] Deadline gate passed — date confirmed before substantive drafting
- [ ] Every ground's facts sourced; no unsourced assertion
- [ ] Every authority tagged by provenance; no fabricated or unretrieved cite
- [ ] Weak grounds flagged `[review]`, not silently included
- [ ] Non-professional filing gate applied; event + new deadline logged

## What this skill does NOT do
- File with LHDN/SCIT.
- Proceed without the deadline confirmed.
- Cite an authority it didn't retrieve or that the user didn't provide.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

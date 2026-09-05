---
name: matter-briefing
description: >
  Produce a deep briefing on one controversy matter — ready for a call with the client,
  the partner, or a tax litigator. Pulls the matter file into a structured brief: facts,
  the assessor's basis, the position and the standard it meets, exposure, deadlines, and
  the recommended path. Use for "brief me on [matter]", "prep for the call on [matter]".
argument-hint: "<matter-slug>"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Matter Briefing

## Purpose

Turn a matter file into a brief someone can walk into a call with — no re-reading the whole file. Every fact is sourced; the position is stated at the standard it meets; the deadline is front and centre.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` and the active (or named) matter's `matter.md` and `history.md`. If no matter is active and none is named, ask which. Never brief from memory of a prior session — re-read the matter file.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

## Workflow

1. **Lead with the deadline and the ask.** The controlling deadline (flagged for verification) and the decision this call needs to produce.
2. **The facts** — a tight chronology, each fact cited to its source document. Flag any fact still unsourced.
3. **The assessor's basis** — quoted, with the position LHDN is taking and the authority they're relying on (or "not yet pinned").
4. **Our position** — the argument(s), each tagged with the standard it meets (settled / strong / arguable / doubtful) and the authority `[verify]`. Note the weakest link.
5. **Exposure** — tax + penalties, traced; best/worst/likely if the team works that way.
6. **The path** — the realistic options (respond/negotiate/concede/object/appeal), the recommended one flagged `[review]` for the person with settlement authority, and what each costs in time and risk.
7. **Open questions** — what's missing before the next step.

## Output format
```
[WORK-PRODUCT HEADER]
# Matter Briefing: [taxpayer] — [matter] ([body], YA [years])
## Deadline & decision needed   [🔴 date `[verify]`]
## Facts (sourced) / Assessor's basis / Our position (by standard) / Exposure / Path / Open questions
```
Lead with the reviewer note.

## Quality checks
- [ ] Deadline stated first, flagged for verification
- [ ] Every fact sourced; unsourced facts flagged
- [ ] Positions tagged with the standard each meets
- [ ] Recommended path flagged `[review]`, not decided
- [ ] Re-read the matter file; not briefed from memory

## What this skill does NOT do
- Decide the path.
- Draft the submission (that's `objection-appeal` / `audit-response`).

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

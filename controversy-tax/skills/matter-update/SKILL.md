---
name: matter-update
description: >
  Append a dated event to a controversy matter's history and update matter.md — a new
  letter received, a response sent, a deadline met or moved, a decision taken. Keeps the
  matter file current so briefings and the portfolio are accurate. Use for "log an update
  on [matter]", "we got LHDN's reply", "objection filed".
argument-hint: "<matter-slug> [what happened]"
---

# Matter Update

## Purpose

Keep the matter file current. An append-only `history.md` plus targeted edits to `matter.md` (deadline changes, new exposure, status). The portfolio and every briefing are only as accurate as this.

## Precondition

Read the named (or active) matter's `matter.md` and `history.md`. If none active and none named, ask.

## Workflow

1. **Capture the event** — date, what happened, source document (if any). Append one dated line to `history.md`. Never rewrite history; only append.
2. **Update matter.md where the event changes a fact:** a new or revised deadline (re-confirm and flag it; if a decision letter resets the appeal clock, capture the new date 🔴), revised exposure (traced), stage change, a new fact (sourced).
3. **Surface any deadline consequence** — if the event starts or moves a clock (an LHDN decision forwarding the appeal, a granted extension), say so explicitly and update the controlling deadline.
4. **Update the practice-profile index row** if stage, deadline, or exposure changed.

## Output format
A one-line confirmation of what was logged and any deadline change — then, only if a deadline moved or a decision is now needed, the decision tree.

## Quality checks
- [ ] Event appended to history.md, not overwritten
- [ ] Any deadline change re-confirmed and flagged
- [ ] New facts/exposure sourced
- [ ] Index row updated if stage/deadline/exposure changed

## What this skill does NOT do
- Rewrite the matter's history.
- Assert a new deadline without flagging it for verification.

## Close with a short confirmation; offer the decision tree only if an action now follows.

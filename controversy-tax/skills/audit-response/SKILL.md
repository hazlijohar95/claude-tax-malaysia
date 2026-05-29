---
name: audit-response
description: >
  Draft a response to an LHDN audit query or information request — pin what the assessor
  is actually asking and why, map each item to the source documents that answer it, draft
  a response that answers what's asked without conceding more than necessary, and flag
  what to withhold or clarify. Use for "respond to the audit query", "LHDN asked for...",
  "draft the audit reply".
argument-hint: "<matter-slug> [the audit/query letter, pasted or a file]"
---

# Audit Response

## Purpose

Answer an audit query accurately and no more broadly than it asks. The two failure modes are missing the response deadline and volunteering a concession the query didn't require. This skill pins the assessor's actual ask, answers it from sourced documents, and flags anything that would give ground.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` and the matter's `matter.md`. You need the query letter and access to the source documents it concerns. If the matter isn't open, run `/controversy-tax:matter-intake` first.

## Workflow

### Step 1 — Pin the ask and the basis
Quote each item the query asks for. For each, infer what position the assessor is testing (often unstated) and note it — answering well means understanding why they're asking. Flag the response deadline 🔴 `[verify against the letter]`.

### Step 2 — Map each item to source
For every item asked, identify the source document(s) that answer it (the working paper, the ledger, the agreement, the prior computation). Each answer is built from a sourced document, never from memory or assertion. Where a document doesn't exist or can't be located, say so — do not fabricate a figure or a fact to fill the gap.

### Step 3 — Draft the response, item by item
For each item: a direct answer, the supporting document referenced (and attached/listed), and the authority for the position where relevant `[verify]`. Answer **what is asked** — do not volunteer adjacent positions, additional years, or concessions the query didn't seek. Where an item invites a concession or a characterisation that could hurt at a later objection/appeal, flag it `[review]` and offer a neutral framing.

### Step 4 — Withhold / clarify check
Flag anything that should be clarified rather than answered as asked (an ambiguous request, a request outside the audit's stated scope, a request for privileged solicitor material — `[review]`). Note that what's provided shapes the record for any later objection.

### Step 5 — Assemble and gate
Draft the response letter (clean external version — no work-product header). **If Role is Non-professional**, gate before sending: "An audit response goes on the record and shapes any later dispute. Has a qualified adviser / tax agent reviewed this? If yes, proceed. If no, here's the brief." Do not finalise for sending past the gate without an explicit yes. Append the event to the matter (`/controversy-tax:matter-update`).

## Output format
```
[WORK-PRODUCT HEADER — internal working version]
# Audit Response Working: [taxpayer] — [matter]
## Deadline   [🔴 date `[verify]`]
## The ask, pinned   [each item + the position being tested]
## Item-by-item response   [answer + source doc + authority]
## Flagged   [`[review]`: concessions to avoid, items to clarify/withhold]
---
## Draft response letter   [clean, external, no header]
```

## Quality checks
- [ ] Response deadline flagged first
- [ ] Each item answered from a sourced document; gaps flagged not filled
- [ ] No volunteered concessions or out-of-scope answers
- [ ] Concession/characterisation risks flagged `[review]`
- [ ] Non-professional gate applied before sending; event logged

## What this skill does NOT do
- Send to LHDN. - Concede a position (it flags concession risk for the reviewer). - Invent a document or figure to answer a query — it flags the gap.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

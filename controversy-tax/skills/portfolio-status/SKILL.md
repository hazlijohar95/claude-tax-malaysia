---
name: portfolio-status
description: >
  Roll up the controversy portfolio — open matters by stage, total and per-matter
  exposure, upcoming deadlines ranked by urgency, and stale matters with no recent
  activity. Use for "portfolio status", "what's open", "what deadlines are coming",
  "show me all the matters".
argument-hint: "[--deadlines to show only the deadline calendar] [--stale to show only stale matters]"
---

# Portfolio Status

## Purpose

The one view of every open dispute: where each stands, what it's worth, what's due, and what's gone quiet. The deadline ranking is the point — a missed objection window is the failure this plugin exists to prevent.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` `## Open matters` and each matter's `matter.md` for current deadline, stage, and exposure. With cross-matter context off, this is the one skill permitted to read across matters (read-only) to build the rollup.

## Workflow

1. **Collect** each open matter's taxpayer, body, type, stage, controlling deadline, last activity (from history.md), and exposure.
2. **Rank deadlines** across the portfolio: 🔴 ≤14 days (or any objection/appeal window open now), 🟠 15–44, 🟡 45–90. Every date tagged `[verify against the notice / current procedure]` — the rollup does not assert deadlines as settled.
3. **Flag stale matters** — open, with no history.md entry in [the team's staleness window, default 30 days]. A stale matter with a live deadline is 🔴.
4. **Total exposure** — sum, traced to the matters; note any single matter that dominates.
5. **Report** sorted by deadline urgency, with a summary stat line first.

## Output format
```
Tax controversy portfolio — as of [date]
[N] open · RM [x] total exposure · [N] deadlines ≤14 days · [N] stale

🔴 Deadlines ≤14 days (or open window now)
• [taxpayer] — [event] due [date] `[verify]` — [matter]

🟠 / 🟡 ... | ⚠️ Stale: [matters] | Dominant exposure: [matter] RM[x]
```

## `--deadlines` / `--stale`
Filter to just the deadline calendar, or just stale matters.

## Quality checks
- [ ] Every open matter included; exposure traced
- [ ] Deadlines ranked and flagged for verification
- [ ] Stale matters surfaced; stale + live deadline = 🔴
- [ ] Read-only across matters (no matter file modified)

## What this skill does NOT do
- Modify any matter.
- Assert deadlines as settled — flags them for verification.
- Decide priorities (it surfaces; the reviewer triages).

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer the dashboard for a portfolio of more than ~10 matters.

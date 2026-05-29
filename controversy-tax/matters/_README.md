# matters/ — controversy portfolio data

This folder is the in-repo **template** for the matter portfolio. At runtime the
matter-workspace and matter-intake skills write to
`~/.claude/plugins/config/claude-for-tax/controversy-tax/matters/` — this copy
documents the layout and the ledger schema so they stay consistent.

Two layers:

- **`_log.yaml`** — the ledger. One row per matter. Parseable by skills. Source
  of truth for `/controversy-tax:portfolio-status` rollups.
- **`[slug]/`** — per-matter detail. Narrative and history. Where humans read and
  edit.

## Layout

```
matters/
├── _log.yaml                  # ledger (all matters, including closed)
├── _README.md                 # this file
└── [matter-slug]/
    ├── matter.md              # deadline block + taxpayer + basis + facts-with-sources
    └── history.md             # append-only dated event log
```

## Slug conventions

Lowercase, hyphens, year at the end. Examples:

- `acme-sdn-field-audit-2026`
- `noa-ya2022-objection-2026`
- `tp-adjustment-appeal-2026`

Year makes the slug stable even if a similar matter arises later. The folder name
matches the slug exactly.

## Who writes what

| File | Written by | Edit directly? |
|---|---|---|
| `_log.yaml` | `/matter-intake`, `/matter-update` | Yes, but reflect the change in the matter's `history.md` |
| `matter.md` | `/matter-intake` at intake | Yes, for evolving posture / position notes |
| `history.md` | `/matter-intake` seeds; `/matter-update` appends | Append-only in practice — treat past entries as record |

## The controlling deadline is the point

Every controversy matter is governed by a deadline that is a one-way door — the
objection window on a notice of assessment (s.99 ITA `[verify — typically 30
days from the date of the notice]`), the audit-query response date, the appeal
period to the SCIT. `next_deadline` in the ledger is not optional. A matter row
without a confirmed controlling deadline is flagged, not filed.

## Closed matters

Stay here. Don't delete. `/portfolio-status` filters them from active rollups by
default. Closed matters are the record of how positions resolved — the training
set for portfolio judgment.

## Corrections

If a past history entry was wrong, don't edit it. Append a new entry that
references and corrects it. In a dispute, the record of when you knew something
can matter as much as the fact itself.

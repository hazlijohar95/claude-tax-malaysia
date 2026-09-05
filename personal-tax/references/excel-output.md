# Excel / Workbook Output — tax working-paper recipe

*Referenced by the **Dashboard / workbook offer** guardrail and by every
data-heavy skill (`tax-computation`, `tax-provision`, `capital-allowances`,
`sst-return-review`, `pcb-computation`, `reliefs-rebates`, the deadline
calendars). This is the **structural** recipe — sheet layout, the CHECK
formulas, the source column. It does **not** assert any rate, threshold, or
section; those come from the computation and stay verify-tagged.*

The two rules are non-negotiable and they are the reason a tax workbook exists
rather than a printout:

1. **Every figure traces to a source and ties to the computation.** Each amount
   carries a source reference, and CHECK cells reconcile the build back to the
   trial balance / accounts / return total.
2. **Formula-injection defence.** Any value that originated outside this session
   (a ledger description, a counterparty name, an uploaded line item) is
   sanitised before it lands in a cell.

A workbook that doesn't tie, or that drops a source reference, is not ready —
say so in the reviewer note's **Tie-out** line and do not present it as final.

## Sheet structure (every tax workbook)

Order matters — a reviewer reads top sheet to bottom, left column to right.

| Sheet | Purpose |
|---|---|
| **`Cover`** | Work-product header (per the profile `## Outputs`), entity, YA / basis period, preparer, date, and the reviewer note (Sources / Read / Tie-out / Flagged / Currency / Before relying). The one-line summary stat sits here. |
| **`Computation`** | The statutory build. One row per line, a **Source** column on every row, a **Note/`[verify]`** column on the right. Totals are **formulas**, never typed. |
| **`Adjustments`** | One row per add-back / deduction: item, amount, source, reason, authority (verify-tagged), and the standard met where it's a judgment call. Sums feed the `Computation` sheet by cell reference. |
| **`CA`** *(where relevant)* | The capital-allowance schedule: per-asset QE, class/rate `[verify]`, IA, AA, balancing adjustment, closing residual expenditure. Opening RE links to the prior-year cell. |
| **`Sources`** | The source map: every source reference used anywhere in the workbook, what it is (TB code, accounts caption, prior-year return line, working-paper index), and where it came from. Every `Source` cell elsewhere should resolve to a row here. |
| **`CHECK`** | The reconciliations, each a live formula returning `OK` / `FAIL`. See below. |

For non-computation outputs (a deadline calendar, an SST-02 review, a findings
list) collapse to `Cover` + one data sheet + `Sources` + `CHECK`, but keep the
four-sheet spine.

## The Source column — make tracing structural, not manual

- Every numeric row on every sheet has a `Source` cell. No exceptions. A blank
  `Source` is the workbook equivalent of a number typed from memory.
- A figure pulled from another sheet is a **cell reference**
  (`=Adjustments!E14`), not a re-typed number — so the trace is the formula.
- A figure from a source document carries the reference as text
  (`TB 5200`, `Accounts note 7`, `PY comp line 4`, `CP204 instalment 3`) and
  that reference exists as a row on the `Sources` sheet.
- A figure that has **no** source yet is left blank with the `Note` cell set to
  `[need source — not computed]`. Never fill it to make the sheet look complete.

## CHECK cells — live formulas, not a tick-box

The `CHECK` sheet holds one row per reconciliation; the verdict is a formula so
it re-evaluates if any input changes. Pattern:

```
Check                                          Expected      Actual          Verdict
PBT ties to accounts                           =Sources!..   =Computation!.. =IF(ABS(C2-B2)<=Tol,"OK","FAIL")
Σ adjustments = (CI build − PBT)               =Computation  =Adjustments    =IF(ABS(C3-B3)<=Tol,"OK","FAIL")
Every TB line mapped once                      =count(TB)    =count(map)     =IF(C4=B4,"OK","FAIL")
B/f losses & CA agree to PY computation        =PY!..        =Computation!.. =IF(ABS(C5-B5)<=Tol,"OK","FAIL")
Instalments deducted = CP204 per record        =Sources!..   =Computation!.. =IF(ABS(C6-B6)<=Tol,"OK","FAIL")
```

- Put a rounding tolerance in one named cell (`Tol`, e.g. `0.5` for nearest RM)
  and reference it — don't hard-code it into each formula.
- A red conditional-format on any `FAIL` so a failed tie is visible at a glance.
- The `Cover` summary stat reads the CHECK sheet:
  `Ties out: =IF(COUNTIF(CHECK!D:D,"FAIL")=0,"yes","NO — see CHECK")`.

## Formula-injection defence (apply to every externally-sourced cell)

Any string that came from outside this session — a ledger narration, a
supplier/counterparty name, a line item from an uploaded file — can be a formula
payload. Before it lands in a cell, if it starts with `=`, `+`, `-`, or `@`,
prefix it with an apostrophe so Excel/Sheets treats it as text:

```python
def safe_cell(v):
    s = "" if v is None else str(v)
    return "'" + s if s[:1] in ("=", "+", "-", "@") else s
```

Apply `safe_cell` to every value that did not originate as a number you computed
this session. Numbers you computed are written as numbers (so the CHECK formulas
work); untrusted **text** is always written through `safe_cell`.

## Rendering by surface

- **Claude Code:** write the file with `openpyxl` to the plugin's outputs folder
  (`~/.claude/plugins/config/claude-for-tax/<plugin>/outputs/<topic>-<entity>-YA<year>.xlsx`)
  and tell the user the path (`open <path>` on macOS). Use formulas for every
  total and every CHECK — never write a pre-computed total as a literal, or the
  workbook can't be re-checked after an edit.
- **Cowork / Claude Desktop:** if a true `.xlsx` isn't available, produce the
  same structure as an HTML workbook (one `<table>` per sheet, the CHECK table
  with red `FAIL` styling) following `references/dashboard-template.md`, and
  apply the HTML-escape rule there to every untrusted string.
- **Always also give the markdown view** of the bottom line and the CHECK
  results, so a reviewer in a terminal sees whether it ties without opening the
  file.

## Before you hand it over

- [ ] Every numeric row has a `Source` cell; every `Source` resolves to a
      `Sources` row or a cell reference
- [ ] Every total and every CHECK is a **formula**, not a typed number
- [ ] All CHECK rows return `OK` — or the reviewer note says which failed and the
      workbook is not presented as final
- [ ] Every externally-sourced string written through `safe_cell` (or HTML-escaped)
- [ ] Rates / thresholds / sections still carry their `[verify]` tags in the
      `Note` column — the workbook format does not launder a flag into a fact

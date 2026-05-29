# Dashboard Template

*Referenced by the Dashboard offer guardrail. Keep dashboards simple and consistent — the value is speed of comprehension, not visual polish.*

## Structure (top to bottom)

1. **Title and metadata.** What this is, when it was generated, what it covers, the year of assessment / taxable period. One line.
2. **Summary stats.** The counts that matter, colour-coded. "18 findings: 🔴 2 blocking · 🟠 5 high · 🟡 7 medium · 🟢 4 low — RM 312k exposure, 3 deadlines this month." This is the most valuable line. Make it scannable.
3. **The reviewer note.** Same one-block format as any output. Sources, scope, flags, tie-out status, before-relying. Dashboards don't skip the safety metadata.
4. **Chart(s).** One or two max. Pick the one that shows the shape:
   - **Risk / exposure distribution** (bar): counts or RM by severity. Use for findings, adjustments, flags.
   - **Category breakdown** (pie or stacked bar): counts by type. Use for adjustment categories, taxability buckets, deferred-tax components.
   - **Timeline** (Gantt-lite or sorted table): dates in order. Use for deadline calendars, instalment (CP204) schedules, audit milestones.
   - Never more than two. A dashboard with five charts is a report, and reports are harder to read than the table.
5. **The table.** Sortable, filterable, colour-coded by severity/status. Columns: the ones in the original output, trimmed to what fits on a screen. Put a "notes / source ref" column last — it's the one that gets truncated.
6. **The decision tree.** Same options as the text output. "What next?"

## Rendering by surface

- **Cowork / Claude Desktop:** HTML artifact. Self-contained, single file, inline CSS. No external dependencies, no CDN, no npm. Tables: HTML `<table>` with `data-sort` attributes and a small inline JS sorter. Charts: inline SVG or Unicode block chars for bar charts. Keep the JS minimal — sorting and filtering, nothing else.
- **Claude Code:** Write the same HTML file to the plugin's outputs folder (`~/.claude/plugins/config/claude-for-tax/<plugin>/outputs/dashboard-<topic>-<date>.html`) and tell the user to open it: `open <path>` on macOS, or "open in your browser." Also produce a markdown version with Unicode block charts for the summary stats so the user can see the shape without leaving the terminal.
- **Excel (the default for tax — most outputs land here).** Tax computations, SST returns, deferred-tax proofs, capital-allowance schedules, deadline calendars, and anything taken into a client or board meeting belong in a workbook. The full structural recipe — sheet layout, the `Source` column, the live CHECK formulas, the `safe_cell` injection defence — is in **`references/excel-output.md`**; follow it for any workbook export. The two non-negotiable rules, in short:
  1. **Every figure traces and ties.** Each amount carries a source reference (trial-balance account code, ledger, prior-year return line, working-paper ref). Include a `Sources` sheet and CHECK cells that reconcile the computation back to the trial balance / financial statements / return total. A workbook that doesn't tie is not ready.
  2. **Formula-injection defence.** Any cell value that originated outside this session (a ledger description, a counterparty name, a line item pulled from an uploaded file) is sanitised before it lands in a cell: prefix a leading `=`, `+`, `-`, or `@` with a `'` so it is treated as text, not a formula. Same threat as the HTML-escape rule below, different execution surface.
- **Escape untrusted input (apply every dashboard, every time).** Every value that came from outside this session — ledger descriptions, counterparty/supplier names, document-supplied strings, anything the user or a connector handed you — must be HTML-escaped before it lands in the document. Escape `&`, `<`, `>`, `"`, `'` into entities when writing into table cells, summary lines, chart labels, and tooltip text. In the inline JS sorter/filter, set cell text via `textContent`, never `innerHTML`. Do not emit `<script>` blocks whose contents interpolate untrusted strings. Do not render untrusted URLs into `href` or `src` without scheme-checking (`http:` / `https:` / `mailto:` only). A dashboard the reviewer opens in a browser is a trust boundary; treat it like one.

## Keep it boring

- **Colour palette:** Red / orange / yellow / green for severity. Gray for neutral. Blue for status. Nothing else.
- **No animations, no frameworks, no external fonts.** A dashboard that breaks offline is a dashboard that breaks.
- **No clever layouts.** Summary, reviewer note, chart, table, decision tree. Top to bottom. Every dashboard looks the same so the reader knows where to look.
- **The markdown version matters.** Some users are in a terminal and won't open a browser. The summary stat line with Unicode bars (e.g., `🔴 ███ 2  🟠 ████████ 5  🟡 ███████████ 7  🟢 ██████ 4`) gives them the shape.

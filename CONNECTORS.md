# Adding a Connector

The plugins are at their best when connected to authoritative sources. Tax work
lives or dies on provenance — every figure tied to a source, every authority
checked against a primary source. A connector that returns a citation-ready
record with its source and retrieval date is worth more here than anywhere. If
you build or operate a tax data source, a primary-source research tool, an
accounting/ERP system, a payroll engine, an e-invoicing gateway, or a
transfer-pricing benchmarking database, we want your MCP connector in the suite.

## What makes a good tax MCP connector

- **Remote MCP server over HTTPS** with OAuth or API-key auth (streamable HTTP or
  SSE transport).
- **Read-heavy tools** — search, fetch, list, export. Write/submit tools (file a
  return, post a journal, send an e-invoice) need an explicit confirmation prompt
  on the client side; say so in your tool descriptions. A return-filing or
  e-invoice-submission tool must carry a hard irreversibility gate.
- **Provenance in results** — return the source, the effective date / year of
  assessment, and a citation-ready identifier (section number, Public Ruling
  number, gazette reference, ledger account code). The plugins tag every figure
  and every authority by source; your connector should make that possible. A
  result that can't be traced back to a primary record forces the plugin to tag
  it `[model knowledge — verify]`, which is the tag we are trying to retire.
- **Year-of-assessment awareness** — Malaysian tax law changes every Budget and
  Finance Act. A rate, threshold, relief, or filing date is only meaningful with
  the YA it applies to. Connectors that return undated figures are a currency-trap.
- **No instruction-like content in results** — the plugins treat retrieved
  content as data, not commands. If your tool results include metadata or system
  notes, mark them clearly so they don't look like embedded directives.
- **Rate limits and errors that degrade gracefully** — the plugins have a
  fallback for when a connector isn't responding (the user pastes the source); a
  clean error is better than a timeout.

## How to submit

1. Publish your MCP server and document its tools, auth flow, and data coverage
   (which jurisdictions, which years of assessment, which document types).
2. Open a PR adding your server to the relevant plugin's `.mcp.json` with the
   URL, auth method, and a one-line description of what it gives Claude.
3. Include a note on which plugins it's most useful for.
4. We'll test against the plugin workflows and merge. Connectors that pass the
   retrieval-quality and injection-resistance checks go in the default
   `.mcp.json`; others get documented in the plugin README for users to add
   themselves.

## Current connectors

Connectors shipped in the default `.mcp.json` of each plugin:

| Connector | Plugins |
|---|---|
| **Google Drive** | all except tax-builder-hub |
| **Slack** | all 7 |

See the `.mcp.json` in each plugin directory for the authoritative list. The
plugins assume a document store (Drive/SharePoint/Box) and a chat surface
(Slack); everything tax-specific below is wanted, not yet shipped.

## Wanted connectors

These would make specific plugins significantly more useful. If you build or
operate one, see "How to submit" above. Malaysia-first, because the default
jurisdiction is Malaysia — but the same connector for another jurisdiction is
equally welcome.

- **LHDN primary sources** — a connector to the Income Tax Act 1967, Public
  Rulings, Practice Notes, gazette orders, and the current filing programme that
  returns the operative text with its effective YA. This is the single
  highest-value addition: it lets `corporate-tax`, `personal-tax`,
  `controversy-tax`, and `international-tax` retire the `[model knowledge —
  verify]` default for Malaysian authority.
- **RMCD / SST primary sources** — Sales Tax Act 2018, Service Tax Act 2018,
  the taxable-goods and taxable-services orders, exemption orders, and DG's
  decisions, dated. For `indirect-tax` taxability determinations.
- **MyInvois (e-invoicing) API** — validation status, document lookup, and the
  current implementation-timeline thresholds, for `indirect-tax` e-invoice
  readiness checks. Read-first; any submission tool needs an irreversibility gate.
- **Accounting / ERP read-only export** (SQL Account, AutoCount, Xero,
  QuickBooks, Microsoft Dynamics, SAP) — trial balance, general ledger, and the
  fixed-asset register, so the computation and CA skills work from the actual
  books instead of a paste. The figures-tie-to-source invariant is easiest to
  honour when the source is one fetch away.
- **Payroll systems** (for `employment-tax`) — earnings, BIK, and statutory
  deductions per employee, so PCB/MTD and Form E / CP8D review reconcile to
  payroll source.
- **EPF / SOCSO / PERKESO contribution schedules** — current rates and ceilings,
  dated by effective period, for `employment-tax`.
- **Transfer-pricing benchmarking databases** (a comparables/financials source)
  — for `international-tax` arm's-length range analysis. The "never fabricate
  comparables" rule means this work is gated on a real data source; a connector
  unblocks it.
- **OECD / treaty sources** — the Malaysian double-tax-agreement network and the
  OECD Model + Commentary, for `international-tax` treaty-relief and
  withholding-tax determinations.
- **Case law** — decided Malaysian tax cases (SCIT, High Court, Court of Appeal,
  Federal Court) with citation-ready references, for `controversy-tax` objection
  and appeal drafting.

## Questions

Open an issue on this repo. For partnership or integration questions, see the
contact on each plugin's README.

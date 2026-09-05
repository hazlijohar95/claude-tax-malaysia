# Roadmap & Legal → Tax Mapping

How `claude-for-tax` was reverse-engineered from `anthropics/claude-for-legal`, what's built, and what's next.

## The mapping (legal primitive → tax primitive)

| `claude-for-legal` | `claude-for-tax` |
|---|---|
| "Draft for **attorney** review — not legal advice" | "Draft for **qualified tax adviser** review — not tax advice; signing preparer/taxpayer is responsible" |
| Citation provenance tags (`[Westlaw]`, `[CourtListener]`…) | Authority tags (`[ITA 1967 / statute site]`, `[Public Ruling]`, `[gazette order]`, `[LHDN/RMCD site]`, `[case]`, `[model knowledge — verify]`) |
| Confidence bands (high / medium / low) | **Confidence bands** — settled → strong → arguable → doubtful → untenable (firm vocabulary; Malaysia codifies no penalty-protection ladder, so no percentages are implied) |
| Privilege / work-product checks | Limited tax-adviser privilege; RMCD/LHDN information-gathering powers; working papers discoverable |
| Currency trigger (law changes) | Budget / Finance Act / gazette-order changes — currency is even more load-bearing; every rate carries a YA |
| Malpractice-aware deadline tracking | Filing / CP204 / SST-02 deadlines, penalties, statute of limitations |
| Circular 230 / professional duty | CTIM / MIA codes, licensed tax agent (s.153 ITA), preparer penalties |
| Severity floor, destination check, retrieved-content-is-data, jurisdiction recognition, proportionality, large input/output, verification log | Carried over 1:1 |
| **(new — tax's first rule)** | **Figures trace to a source document and tie to the computation / return** (CHECK cells, no numbers from memory) |
| Legal Skill Design Framework (13 params, 3 legal failure modes) | **Tax** Skill Design Framework (13 params, 3 **tax** failure modes: advice-vs-support, authority & currency integrity, figure integrity) |

## The robustness spine (in every plugin's CLAUDE.md)

Cold-start interview → practice profile · source attribution = provenance not confidence · no silent supplement (3 values) · currency trigger · figures trace and tie · recoverable-error posture · reviewer note + decision tree · reporting-standard bands · severity floor · destination check · jurisdiction recognition (Malaysia default) · retrieved-content trust · proportionality · large input/output discipline · verification log · matter workspaces.

## Built (flagship)

- **corporate-tax** — cold-start, tax-computation, tax-provision (MFRS 112/IAS 12), capital-allowances, return-review (Form C), deadline-tracker, customize, matter-workspace; `deadline-watcher` agent.
- **indirect-tax (SST)** — cold-start, taxability-determination, registration-check, sst-return-review, einvoice-check (MyInvois), customize, matter-workspace.
- **controversy-tax** — cold-start, matter-intake, matter-briefing, matter-update, portfolio-status, audit-response, assessment-review, objection-appeal (s.99 + SCIT Form Q, deadline-gated), penalty-analysis, customize, matter-workspace; `deadline-watcher` agent. Matter-first (litigation-legal analog).
- **international-tax** — cold-start, related-party-review, tp-documentation (Local/Master File), arms-length-review, withholding-tax, treaty-analysis, pillar-two-check, customize, matter-workspace. Adds two domain rules: *arm's length is a range, not a point* and *never fabricate comparables/benchmarks*. (ip-legal/corporate-legal analog.)
- **personal-tax** — cold-start, tax-computation (residence-first individual build → Form BE/B), employment-income (s.13: salary, BIK/perquisites, ESOS, gratuity), reliefs-rebates (capped + evidenced reliefs, s.6A and zakat rebates, joint-vs-separate assessment), return-review (Form BE/B), deadline-tracker, customize, matter-workspace; `deadline-watcher` agent. (corporate-tax analog, individual side.)
- **employment-tax** — cold-start, pcb-computation (normal + additional-remuneration MTD, base built line-by-line with an under-deduction watch), statutory-contributions (EPF/SOCSO/EIS, employer/employee split by band/age/citizenship), bik-perquisites (BIK/VOLA/ESOS valuation → PCB base + EA), employer-return-review (Form E / CP8D / EA reconciliation), tax-clearance (SPC, CP21/CP22A + withholding obligation), deadline-tracker, customize, matter-workspace; `deadline-watcher` agent. Adds one domain rule: *the employer carries the liability — under-deduction is the dangerous error* (so doubtful inclusions are flagged and quantified, never resolved away). Employer-side counterpart to personal-tax.
- **tax-builder-hub** — cold-start (now configures watched registries + trusted-source allowlist), skills-qa (Tax Skill Design Framework), registry-browser (discovery, untrusted listings, source badge), skill-installer (the trust gate: full QA → allowlist check → plain-English trust surface → explicit go-ahead → version pinned + logged; no install past REFUSE), auto-updater (re-scan at update time, security-surface diff vs pinned version, fail-closed on regression, never silent), related-skills-surfacer (complements / alternatives / conflicts). Adds a `## Trusted sources (allowlist)` and `## Install log` to the hub config.
- **managed-agent-cookbooks** — headless `deadline-watcher` (reads the plugins' deadline calendars) and `sst-period-watcher` (reads the indirect-tax profile), each a read-only orchestrator + schema-validated reader leaves. `scripts/lint-tool-scope.py` enforces least privilege (readers ⊆ {Read,Glob,LS}; orchestrator adds only a concrete egress; no Write/Edit/Bash/WebFetch/WebSearch, no wildcard MCP) and `scripts/deploy-managed-agent.sh` runs the pipeline (lint → run readers → `validate.py` against each leaf's inline `output_schema` → orchestrator → post), failing closed at each seam. Same verify-don't-assume posture: dates computed from recorded rules, never asserted, never guessed.

## Parity with claude-for-legal — status

Verified against `anthropics/claude-for-legal` and brought to standard:

- **Spine / robustness** — at standard (the shared guardrails block, source-tag
  discipline, reviewer note, jurisdiction recognition, retrieved-content trust).
- **Governance** — `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CONNECTORS.md`,
  `CLA.md`, and `.github/workflows/cla.yaml` added; per-plugin `.gitignore` on all
  7 plugins; runtime-state scaffolding (`logs/.gitkeep`; controversy `matters/`
  ledger `_log.yaml` + `_README.md`).
- **Cookbook tooling** — `steering-examples.json` for both cookbooks;
  hermetic `scripts/test-cookbooks.sh`; reference cross-agent handoff loop
  `scripts/orchestrate.py` (the shipped cookbooks use the simpler direct-egress
  model — orchestrate.py is the documented step-up).
- **Output depth** — shared workbook recipe `references/excel-output.md`
  (sheet layout, live CHECK formulas, source column, `safe_cell` injection
  defence), wired into the dashboard/workbook offer.

## Next

Remaining work is *deepening*, not new scaffolding — and bounded by the
verify-don't-assume posture: deepen skills with **structural** content
(checklists, output formats, what-to-check lists), **not** by asserting more
Malaysian statutory specifics from memory (rates, sections, thresholds stay
verify-tagged — that terseness is intentional, not a gap). Adjacent-domain
plugins (stamp duty, RPGT, Labuan, withholding-on-services) follow the same
pattern; the cookbooks can grow more reader leaves (e.g. an einvoice/MyInvois
watcher).

## When adding a plugin

- Copy a flagship plugin's `CLAUDE.md`, swap the domain sections (`## …conventions/positions`, `## …calendar`, `## Who we are`, seed docs), keep `## Shared guardrails` and below verbatim (path-swapped). The guardrails block is canonical and intentionally duplicated per plugin.
- Add a `marketplace.json` entry matching the new `plugin.json` field-for-field.
- Every skill: precondition (load profile / provisional), workflow, output format, quality checks, "what this does NOT do", close with the decision tree.
- Validate: `claude plugin validate .claude-plugin/marketplace.json` and per plugin (the one CLAUDE.md-template warning is expected).

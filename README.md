# Claude for Tax

Reference agents, skills, and data connectors for the tax workflows we see most — corporate income tax and provision, indirect tax (SST/VAT/GST), tax controversy and audit defence, and transfer pricing and international tax. Built **Malaysia-first**, with a **verify-don't-assume** posture and a jurisdiction-recognition layer for everything else.

> **New here?** Start with [QUICKSTART.md](QUICKSTART.md) — install in about a minute, then a 2-minute setup. This README is the full reference.

This repo is modelled on [`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal): same architecture, same robustness spine, the legal nouns swapped for tax nouns. Install it as a [Claude Cowork](https://claude.com/product/cowork) or [Claude Code](https://claude.com/product/claude-code) plugin.

> [!IMPORTANT]
> **Every output from these plugins is a draft for review by a qualified tax adviser — not tax advice, not a filing position you can rely on without checking, not a substitute for a chartered tax practitioner.** They are built with guardrails that reflect that: every statutory reference and rate marked by source, every figure traced to a source document and tied back to the computation, jurisdiction assumptions surfaced, reporting-standard confidence stated, and explicit gates before anything is filed, submitted, or signed. The signing preparer or taxpayer — not the plugin, and not the author — is responsible for the positions taken in their work product. **The plugins make the review faster; they do not replace it.**
>
> **Tax law changes every year.** Rates, thresholds, reliefs, and procedures move with each Budget and Finance Act, and gazette orders and Public Rulings are revised continually. Anything these plugins recall from training knowledge is treated as stale by default and tagged `[model knowledge — verify]` until checked against a primary source (the Income Tax Act 1967, the Sales/Service Tax Acts 2018, a Public Ruling, a gazette order, or an LHDN/RMCD publication). **Verify before you rely.**

## The robustness spine

The thing worth copying from `claude-for-legal` is not its legal content — it's the discipline every skill inherits from one practice profile per plugin. The same spine runs here:

- **Cold-start interview → practice profile.** Nothing substantive runs until the plugin interviews you and writes `~/.claude/plugins/config/claude-for-tax/<plugin>/CLAUDE.md`. Every skill reads it first. Generic output is treated as a failure, not a default.
- **Source attribution = provenance, not confidence.** `[ITA 1967 / statute site]`, `[Public Ruling]`, `[gazette order]`, `[LHDN/RMCD site]`, `[case]`, `[user provided]`, `[model knowledge — verify]`. A tag describes where a cite came from this session, never how confident the model feels.
- **No silent supplement (three values).** Supplement-with-a-flag, stop-and-ask, or flag-but-don't-use. Plus a **currency trigger**: if a Budget/Finance Act could have changed it, search or ask before relying on memory.
- **Confidence bands.** Settled → strong → arguable → doubtful → untenable. A position is stated with the band it meets, not asserted flat. The bands describe how well authority supports a position; they are firm vocabulary, not a statutory standard, and carry no likelihood percentage.
- **Figures trace and tie.** Every amount carries a source reference; every computation carries CHECK cells reconciling to the trial balance / accounts / return total. (This is the discipline tax demands that legal only gestures at.)
- **The recoverable-error posture.** Uncertain subjective call → flag `[review]` inline for the adviser, don't silently decide. Under-flagging is a one-way door; over-flagging is a two-way door closed in 30 seconds.
- **Reviewer note + decision tree** on every deliverable; **deadline awareness** (filing dates, instalments, statute of limitations) with penalty-aware caution; **jurisdiction recognition**; **retrieved-content-is-data**; **proportionality**; a **verification log**.
- **A QA framework** (`/tax-builder-hub:skills-qa`) scoring any skill against the Tax Skill Design Framework before you trust it.

## Plugins in this repo

| Plugin | What it adds |
|---|---|
| **[corporate-tax](./corporate-tax)** | Company income tax computation against the Income Tax Act 1967 (adjusted income → statutory income → chargeable income), capital allowances, the MFRS 112 / IAS 12 current and deferred tax provision with a deferred-tax proof, Form C return review before filing, and a filing / CP204 instalment deadline tracker. Every figure traced to source and tied to the computation. |
| **[indirect-tax](./indirect-tax)** | Taxability determination under the Sales Tax Act 2018 and Service Tax Act 2018, registration-threshold checks, SST-02 return review, exemption and input-cost treatment, and MyInvois e-invoicing readiness. |
| **[controversy-tax](./controversy-tax)** | Matter-first management of audits and disputes — intake (deadline captured first), portfolio status, audit-query response, assessment review with a time-bar check, objections under s.99 ITA and SCIT Form Q appeals (deadline-gated), and penalty/remission analysis. |
| **[international-tax](./international-tax)** | Transfer pricing documentation (Local/Master File), arm's-length review, related-party characterisation, cross-border withholding and treaty analysis, and BEPS Pillar Two screening. Never fabricates comparables; treats arm's length as a range, not a point. |
| **[personal-tax](./personal-tax)** | Individual income tax computation (residence-first → Form BE/B), employment income (s.13 salary, BIK/perquisites, ESOS, gratuity), personal reliefs and rebates (capped and evidenced, s.6A and zakat, joint-vs-separate assessment), return review, and deadlines. The employee side. |
| **[employment-tax](./employment-tax)** | The employer's payroll-tax obligations — monthly tax deduction (PCB/MTD, incl. additional remuneration), EPF/SOCSO/EIS contributions, BIK/VOLA/ESOS valuation, Form E / CP8D / EA review, and tax clearance (SPC) for leavers. The employer carries the liability, so under-deduction is the watched error. The employer side. |
| **[tax-builder-hub](./tax-builder-hub)** | The QA → install → update trust layer for community tax skills: the Tax Skill Design Framework review, a prompt-injection scan, an install gate (QA + allowlist + version pinning; no install past REFUSE), and an auto-updater that re-scans every new version and fails closed on regression. Browsing works against registries you configure — **no registry ships with this repo**, so `skills-qa` on a skill file you already have is the entry point. |

### Headless agents

[`managed-agent-cookbooks/`](./managed-agent-cookbooks) ships two deployable, scheduled watchers — `deadline-watcher` (reads the plugins' deadline calendars) and `sst-period-watcher` (reads the indirect-tax profile) — each a read-only orchestrator + schema-validated reader leaves, deployed through a least-privilege linter and a fail-closed harness.

The roadmap is built out; remaining work is deepening reference content and adding adjacent-domain plugins the same way. See [ROADMAP.md](ROADMAP.md).

## Repository layout

```
corporate-tax/            # company income tax computation, provision, return review, deadlines
indirect-tax/             # SST taxability, registration, SST-02 return, e-invoicing
controversy-tax/          # audits, assessments, objections and appeals — matter-first
international-tax/         # transfer pricing, treaties, withholding, Pillar Two
personal-tax/             # individual self-assessment (Form BE/B), employment income, reliefs
employment-tax/           # employer payroll tax — PCB/MTD, EPF/SOCSO/EIS, BIK, Form E, clearance
tax-builder-hub/          # community tax skill discover/QA/install/update with a trust gate
references/               # shared templates (company-profile, dashboard, excel-output workbook recipe)
managed-agent-cookbooks/  # headless watchers — read-only orchestrator + schema-validated readers
scripts/                  # validation + deploy harness — see scripts/README.md
.github/workflows/        # CLA Assistant + validation CI
.claude-plugin/
  marketplace.json        # plugin registry
```

Governance: [`CONTRIBUTING.md`](CONTRIBUTING.md) (design principles + the verify-don't-assume
invariant), [`CONNECTORS.md`](CONNECTORS.md) (how to add an MCP connector + the wanted list),
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), and [`CLA.md`](CLA.md).

Each plugin directory has the same shape:

```
<plugin>/
  .claude-plugin/plugin.json
  .mcp.json               # MCP connectors the plugin uses
  CLAUDE.md               # template practice profile — filled in by /<plugin>:cold-start-interview
  README.md
  skills/                 # skills — each is a /<plugin>:<skill> slash command
  agents/                 # scheduled agents (if any)
  hooks/                  # hook config (empty stub by default)
```

## Getting started

### Claude Code

```bash
# Add the marketplace (absolute path to this repo)
/plugin marketplace add <path-to-this-repo>

# Install the plugins that match your work
/plugin install corporate-tax@claude-for-tax
/plugin install indirect-tax@claude-for-tax

# Restart Claude Code, then run setup for each plugin.
/corporate-tax:cold-start-interview
/indirect-tax:cold-start-interview
```

**Run the cold-start interview first.** Every other skill reads the practice profile it writes. Skipping it is the single most common reason a skill produces generic output. The interview takes 10–15 minutes per plugin and asks you to point at seed documents (a prior-year tax computation, a signed Form C, a set of accounts, your SST returns — whatever fits). More seed material is better; a **quick start** option gets you productive in 2 minutes and you refine later.

## Using a single skill outside Claude Code

Every skill here is a plain [Agent Skills](https://agentskills.io/specification)
`SKILL.md`, so a single one can be installed into any agent that reads the
standard — Cursor, Codex, Copilot, Gemini CLI and others — without the
marketplace:

```bash
# with the Skills CLI (installs into whichever agents it detects)
npx skills add hazlijohar95/claude-tax-malaysia --skill capital-allowances

# or with the GitHub CLI
gh skill install hazlijohar95/claude-tax-malaysia capital-allowances
```

**What you get and what you lose.** The computational skills carry their own
method and their guardrails travel with them, so they work standalone. What does
*not* travel is everything the plugin runtime provides: the practice profile the
cold-start interview writes, the MCP connectors, the scheduled `deadline-watcher`
agents, and the `/plugin:skill` handoffs between skills. A standalone skill will
say it has no profile and work from generic Malaysian defaults, tagging output
`[PROVISIONAL — profile not configured]`. If you want the profile-driven
behaviour, install the plugin.

Skills carry `license`, `compatibility` and `metadata` (author, version,
jurisdiction) in frontmatter, and CI validates every one against the spec with
the reference validator.

## Making it yours

These are reference templates. They get sharper when tuned to how your practice works — and the customization mechanism is the plugin itself.

- **Run the cold-start interview.** It *is* the customization mechanism. It learns your conventions, your house review framework, your reporting-standard threshold, your deadline calendar, and reads your seed documents.
- **Edit the practice profile.** It lives at `~/.claude/plugins/config/claude-for-tax/<plugin>/CLAUDE.md`. Edit it directly for small fixes — a changed rate, a new entity, a revised threshold. It survives plugin updates.
- **Swap connectors.** Point `.mcp.json` at your document store, accounting system, or e-invoicing middleware. Skills fall back gracefully when a connector isn't configured — they ask you to paste instead of failing silently.
- **Fork skills for house style.** Every skill is a markdown file under `skills/`. Edit the steps, the gates, the output format.

No build step. Everything is markdown and JSON.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).

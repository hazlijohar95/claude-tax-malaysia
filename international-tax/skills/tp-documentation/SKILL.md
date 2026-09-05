---
name: tp-documentation
description: >
  Prepare or review transfer pricing documentation (Local File / Master File) against the
  Malaysian TP Rules and OECD Guidelines — group and entity overview, functional analysis
  (functions, assets, risks), method selection and rationale, and the economic analysis
  framing around a benchmarking study. Will NOT manufacture comparables. Use for "TP
  documentation", "Local File", "Master File", "prepare the TP report".
argument-hint: "[entity / transaction / year] [intercompany agreements + financials + group chart]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Transfer Pricing Documentation

## Purpose

Produce contemporaneous TP documentation that holds up on audit: the group and entity overview, a rigorous functional analysis, a reasoned method selection, and an economic analysis built **around** a real benchmarking study — never around invented comparables. The documentation's job is to show the controlled transactions were priced at arm's length and to evidence the analysis behind it.

## Precondition

Read `~/.claude/plugins/config/claude-for-tax/international-tax/CLAUDE.md`. You need the group structure, the intercompany agreement(s) for the transaction(s), and the relevant financials. Confirm the year — documentation must be contemporaneous for the YA `[verify the requirement and deadline]`.

If the profile is missing or still has `[PLACEHOLDER]` markers, do not refuse: follow the provisional path in the plugin profile — say you're working from generic Malaysian defaults, tag the output `[PROVISIONAL — profile not configured]`, and offer the interview at the end.

**Benchmarking gate.** If the documentation needs an arm's-length range and no benchmarking study is provided or connectable, say so up front: "I can build everything except the economic analysis' comparable set — that needs a benchmarking study. I'll structure the search criteria and the comparability factors so the study is targeted, but I will not invent comparables." Proceed with the rest; mark the economic-analysis section as pending the study.

## Workflow

### Step 1 — Group & entity overview
From the group chart and financials: the group's business, the entity's role, the organisational and ownership structure, and the value chain. Each fact sourced.

### Step 2 — Controlled transactions
List the material controlled transactions in scope (entities, direction, value — sourced to agreements/ledgers). For each, summarise the contractual terms from the actual intercompany agreement; flag any transaction with no written agreement `[review]` (a common audit weakness).

### Step 3 — Functional analysis (FAR)
For each transaction, analyse **functions** performed, **assets** used, and **risks** assumed by each party — and which party controls and has the financial capacity to bear each risk (post-BEPS, this drives the result). Conclude which entity is the tested party and why. This is judgment-heavy; flag the characterisation calls `[review]`.

### Step 4 — Method selection
Select the most appropriate method (CUP / RPM / cost plus / TNMM / profit split) with the reason, tested against the FAR and data availability, tagged `[verify against the TP Rules / OECD Guidelines]`. State why rejected methods were rejected. Method selection is a `[review]` position stated at the standard it meets.

### Step 5 — Economic analysis (around the study)
Frame the comparability search: the tested party's PLI (if TNMM), the search criteria, the comparability factors, and the period. **If a study is provided/connected:** present the range, the chosen point and why, and tie the tested party's result to its segmented financials (sourced). Tag comparables with the study source. **If no study:** state the criteria for the study to be run and mark the range as not yet established — do not state a range.

### Step 6 — Assemble
Per `## House style`, in Local File / Master File structure, with the work-product header (internal) and a clean version note for the filed document.

## Output format
```
[WORK-PRODUCT HEADER]
# TP Documentation: [entity] — [transaction(s)] — YA [year]
## Documentation status   [contemporaneous? deadline `[verify]`]
## Group & entity overview / Controlled transactions / Functional analysis / Method selection / Economic analysis
## Comparables   [from study via [source] | NONE — study required, range not established]
## Flagged   [`[review]`: characterisation, method, missing agreements]
```

## Quality checks
- [ ] Every fact and figure sourced; financials tie to the accounts
- [ ] FAR done properly, including risk control/capacity; characterisation flagged `[review]`
- [ ] Method selection reasoned and tagged for verification
- [ ] Comparables ONLY from a real study; no invented range
- [ ] Contemporaneous-documentation deadline flagged

## What this skill does NOT do
- Invent comparables or an arm's-length range.
- File the documentation.
- Assert the TP Rules or OECD guidance from memory — flags them for verification.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`. Offer `/international-tax:arms-length-review` to scrutinise the method/benchmark, or `/international-tax:related-party-review` to characterise transactions.

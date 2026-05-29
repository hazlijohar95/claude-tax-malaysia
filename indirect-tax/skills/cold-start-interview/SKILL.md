---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your SST / indirect-tax practice and write
  your practice profile. Use on first use of the plugin, when
  `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md` is missing or still
  contains template placeholders, or when the user says "set up the plugin", "configure
  SST", "onboard me". This is the only skill that should run on a fresh install.
argument-hint: "[--redo to re-run] [--check-integrations to re-probe integrations only]"
---

# /cold-start-interview

Learns how this business handles SST and writes `~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md`, which every other skill reads.

## Purpose

Meet this team for the first time and learn how *they* treat their supplies — their registration status, their taxable outputs, the exemptions they rely on, the determinations they make repeatedly — and write it into a living profile. They should feel like they onboarded a sharp indirect-tax senior, not filled in a form.

## Instructions

1. **Check current state** of the config path (exists / paused / placeholder / populated), same logic as any cold-start. Migrate a populated cache config forward if present.
2. **Shared company profile** at `~/.claude/plugins/config/claude-for-tax/company-profile.md` — read and confirm if present (skip company questions); create from `references/company-profile-template.md` if absent.
3. **Install scope check** if cwd is inside a project.
4. **Fork:** offer 2-minute quick start vs 15-minute full. Wait.
5. **Run the interview** (below), 2-3 prompts per turn, asking for pastes/files before memory.
6. **Ask for seed docs:** recent invoices (to see how the team classifies its outputs), a prior SST-02 return, the sales/purchase listing, any exemption certificates or rulings.
7. **Read them** and extract recorded taxability positions and exemptions. **Verify or flag** every rate, taxable-group classification, threshold, and exemption against a primary source before writing it — never write an unverified figure as settled.
8. **List open items** before writing; never write silent gaps.
9. **Write the profile** using `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as the scaffold, in the user's words.
10. **Summarise + offer a test:** "Want to throw an invoice or a supply at me to determine?"

## The interview

### Part 0 — Role, integrations, setting
- **Role** (feeds the header): tax professional / non-professional with adviser access / non-professional. If non-professional, say the two things that change (working-notes framing; a gate before submitting the SST-02), and how to find a licensed tax agent.
- **What's connected?** Probe document store, accounting/billing export, MyInvois middleware, Slack, primary-source research. Report ✓ only on a successful tool call.
- **Practice setting** → matter workspaces on (private practice) or off (in-house).

### Part 1 — Registration profile
Sales-tax and service-tax registration status and dates; which taxable service groups the business is registered for; taxable period (monthly/bi-monthly); thresholds monitored (tagged `[verify against current RMCD threshold]`); any intra-group supply position.

### Part 2 — Taxability positions (the playbook)
For the business's common supplies, capture the **recorded treatment** (taxable / exempt / out of scope / not a prescribed service) and the **basis**, each tagged `[verify against the current Acts and gazette orders]`. Capture exemptions relied on (with the conditions). Capture **the one thing** the team never skips.

### Part 3 — Reporting standard
The firm's default threshold before taking a taxability position, and when each rung is used. Write the confidence ladder.

### Part 4 — SST return calendar
SST-02 due date and registration timing as the team understands them, tagged `[verify against current RMCD guidance]`. Do not assert dates from memory.

## `--check-integrations`
Re-probe connectors; update `## Available integrations`. ✓ only on a successful tool call.

## Examples
```
/indirect-tax:cold-start-interview
/indirect-tax:cold-start-interview --redo
```

## What this skill does NOT do
- Decide the business's positions — it records the ones they give it. - Assert SST rates, groups, thresholds, or deadlines as fact — it flags every one for verification.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

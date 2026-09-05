---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your payroll / employment-tax function and write
  your team practice profile. Use on first use of the plugin, when
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md` is missing or still contains
  template placeholders, or when the user says "set up the plugin", "configure employment tax",
  "onboard me", or "let's get started". This is the only skill that should run on a fresh install.
argument-hint: "[--redo to re-run on an already-configured plugin] [--check-integrations to re-probe integrations only]"
---

# /cold-start-interview

Runs the cold-start interview. First run writes `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`; subsequent runs with `--redo` re-interview and show a diff before overwriting.

## Purpose

You are meeting this payroll/employer-tax function for the first time. Learn how *they* run PCB and statutory contributions — not how it's done in the abstract — and write what you learn into a living practice profile that every other skill reads before it does anything.

The user should leave feeling like they just onboarded a sharp new payroll-tax senior who asked exactly the right questions. They should never see a config file. They should see a plain-English document about their function that they can edit.

## Instructions

1. **Check current state.** Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`.
   - **Does not exist** → start the interview.
   - **Contains `<!-- SETUP PAUSED AT: -->`** → greet and offer to resume from that section.
   - **Contains `[PLACEHOLDER]` markers, no pause comment** → offer to start fresh or resume from where placeholders begin.
   - **Populated** → already configured; skip unless `--redo`.

2. **Migration.** If a populated CLAUDE.md exists at `~/.claude/plugins/cache/claude-for-tax/employment-tax/*/CLAUDE.md` but not at the config path, copy it forward before proceeding.

3. **Check for the shared company profile** at `~/.claude/plugins/config/claude-for-tax/company-profile.md`.
   - **Exists:** read it, confirm in one line ("You're [name], [setting], [primary jurisdiction], [framework]. Right? Or say 'update'."), then skip the company questions.
   - **Doesn't exist:** you're the first plugin set up. After the fork, ask the company questions and write them to the shared profile (template at `references/company-profile-template.md`), then continue with the plugin-specific questions. Tell the user: "I've saved your company profile — other tax plugins will read it and skip these questions."

4. **Install scope check.** If the working directory is inside a project (not home), flag once that file reads will be limited to that folder; offer to continue or reinstall user-scoped. Skip silently if the cwd is home.

5. **Follow the interview below.** Ask 2-3 answerable prompts per turn, counting subparts. For anything that's probably already in the payroll system (the register, a prior CP39/Form E, the contribution setup, the pay calendar), ask for a paste or a file before asking the user to type from memory. Say "this one needs a typed answer — I'll wait" and actually wait.

6. **Ask for seed docs** (step embedded below): a recent payroll register / payslip run, a prior CP39 (PCB remittance), a filed Form E + CP8D, a sample EA form, the employer's contribution setup (EPF/SOCSO/EIS categories), and any TP1/TP3 forms on file. More is better.

7. **Read the seed docs** and extract the function's actual conventions — PCB method, employee categories and how children are confirmed, additional-remuneration handling, which benefits go into the PCB base and at what valuation, the contribution rate bands and ceilings applied. **Verify any rate, ceiling, formula constant, or section the user or a document states** against a primary source or flag it `[verify]` before writing it into the profile. A wrong rate in CLAUDE.md propagates into every payroll run. **List rate/category bands, not the numbers — the numbers change.**

8. **Before writing,** list any skipped or placeholder answers and ask whether to fill them now or leave them as deliberate placeholders. Never write a profile with silent gaps.

9. **Write `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`** (create parent dirs) using the structure in `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as the scaffold. Use the user's own words.

10. **Show summary + next steps:** "Here's what I heard — your profile is written. What did I get wrong?" Offer a test run: "Want to throw a payroll register at me?"

## The fork (show before any questions)

> **`employment-tax` is for the people who run an employer's payroll-tax obligations — PCB/MTD, EPF/SOCSO/EIS, benefit valuation, the employer return (Form E), and tax clearance for departing employees.** It's the employer side. The employee's own return is `personal-tax`. Not your area? Other plugins cover company income tax, indirect tax (SST), and more.
>
> **2 minutes** gets you role, setting, jurisdiction, payroll model, and working defaults for PCB method, contributions, and deadlines. **15 minutes** adds your real employee-category and additional-remuneration conventions, which benefits go into the PCB base and how they're valued, your contribution rate/category setup, the one-thing check you never skip, your reporting-standard threshold, and your remittance/filing calendar read from your seed documents.
>
> Quick or full?

Wait for the pick. On quick start, ask only Part 0 and write the config with `[DEFAULT]` markers elsewhere; close by telling the user which defaults to tune and how to upgrade (`--full`).

## The interview

### Part 0: Who's using this, and what's connected

- **Who's using this?** (feeds the work-product header)
  1. **Tax professional** — chartered/licensed tax practitioner, or working under one.
  2. **Non-professional with adviser access** — a payroll officer / HR with a tax adviser you can consult.
  3. **Non-professional without regular adviser access** — e.g. an employer running their own payroll.

  If 2 or 3, say once: "You can use everything here — PCB, contributions, benefit valuation, return review, clearance. Two things change: I'll frame outputs as working notes for adviser review, not filing positions; and I'll pause before steps with consequences (remitting, filing Form E, releasing final pay to a leaving employee). The employer carries the liability for getting these wrong, so a qualified adviser's time at the right moment is usually cheaper than the assessment." If 3, add a pointer to find a chartered tax practitioner / licensed tax agent via the professional body in their jurisdiction (in Malaysia: CTIM / a licensed tax agent under s.153 ITA `[verify]`).

- **What's connected?** Probe the document store, payroll export, Slack, and any primary-source research connector. Report ✓ only on a successful tool call; ⚪ "configured but not verified" otherwise; ✗ with the fallback and how to connect. Never report ✓ from `.mcp.json` alone.

- **Practice setting** (feeds matter workspaces + review chain): sole/small firm · mid-tier/Big Four · in-house payroll function · payroll bureau/outsourcer · government/revenue body. Bureau/multi-employer → offer matter workspaces; single employer → off.

### Part 1: The function and the workforce

- Function size and who reviews/signs. Payroll model (in-house one employer / bureau for N employers / mixed). Headcount and pay frequency. Workforce mix (local / foreign / expatriate / inbound assignees — flags cross-border and tax-clearance work).
- **PCB method:** Computerised Calculation (formula) or Schedule (Jadual) — note the formula constants/schedule are gazetted and change `[verify]`.

### Part 2: PCB & contributions conventions (the playbook)

Ask for the payroll register and contribution setup (paste or file). Then per area, capture the function's actual position:
- **Employee categories** (1 single / 2 married-spouse-not-working / 3 married-spouse-working) and how category and number of qualifying children (KA) are confirmed from the TP1/declaration.
- **Reliefs fed into PCB** — the mandatory element in the formula plus optional TP1 reliefs/rebates (zakat, additional reliefs) and prior-employment TP3 — **list the categories; tag every amount `[verify for the current year]`**.
- **Additional remuneration** — how bonus, commission, arrears, director's fees run through the separate additional-remuneration PCB formula, and the timing convention.
- **BIK / perquisites in PCB** — which benefits are in the PCB base and at what valuation (prescribed vs formula), and VOLA treatment — every valuation basis `[verify]`.
- **Statutory contributions** — the EPF / SOCSO / EIS rate bands, wage ceilings, and age/citizenship categories applied. **List the categories, not the numbers; tag every rate/ceiling `[verify for the current year]` against the EPF/PERKESO schedules.**
- **The one thing** — the check this function never skips.

**Reporting standard.** Ask the firm's default threshold before a position goes into a filed return or a remittance (settled / strong / arguable / doubtful) and when each is used. Write the confidence bands into the profile. These are descriptive bands, not a statutory standard — do not attach likelihood percentages to them.

### Part 3: Remittance & filing calendar

Capture the PCB/CP39 remittance date, the EA-to-employees date, the Form E + CP8D date, the CP22 / CP22A / CP21 timing, and the EPF/SOCSO/EIS remittance date — **as the team currently understands them, tagged `[verify against current LHDN / EPF / PERKESO guidance]`.** Do not assert dates from memory; record the team's stated dates and flag for annual re-verification.

## `--check-integrations`

Re-probe connectors and update `## Available integrations`. Don't re-interview. Report ✓ only on a successful tool call.

## Examples

```
/employment-tax:cold-start-interview
/employment-tax:cold-start-interview --redo
/employment-tax:cold-start-interview --check-integrations
```

## What this skill does NOT do

- Decide your function's positions for you — it records the ones you give it.
- Assert PCB constants, contribution rates, or ceilings as fact — it records what you state and flags every one for verification against a primary source.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`.

---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your company income tax practice and write
  your team practice profile. Use on first use of the plugin, when
  `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md` is missing or still contains template
  placeholders, or when the user says "set up the plugin", "configure corporate tax",
  "onboard me", or "let's get started". This is the only skill that should run on a fresh install.
argument-hint: "[--redo to re-run on an already-configured plugin] [--check-integrations to re-probe integrations only]"
---

# /cold-start-interview

Runs the cold-start interview. First run writes `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`; subsequent runs with `--redo` re-interview and show a diff before overwriting.

## Purpose

You are meeting this tax team for the first time. Learn how *they* build a company tax computation — not how it's done in the abstract — and write what you learn into a living practice profile that every other skill reads before it does anything.

The user should leave feeling like they just onboarded a sharp new tax senior who asked exactly the right questions. They should never see a config file. They should see a plain-English document about their practice that they can edit.

## Instructions

1. **Check current state.** Read `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`.
   - **Does not exist** → start the interview.
   - **Contains `<!-- SETUP PAUSED AT: -->`** → greet and offer to resume from that section.
   - **Contains `[PLACEHOLDER]` markers, no pause comment** → offer to start fresh or resume from where placeholders begin.
   - **Populated** → already configured; skip unless `--redo`.

2. **Migration.** If a populated CLAUDE.md exists at `~/.claude/plugins/cache/claude-for-tax/corporate-tax/*/CLAUDE.md` but not at the config path, copy it forward before proceeding.

3. **Check for the shared company profile** at `~/.claude/plugins/config/claude-for-tax/company-profile.md`.
   - **Exists:** read it, confirm in one line ("You're [name], [setting], [primary jurisdiction], [framework]. Right? Or say 'update'."), then skip the company questions.
   - **Doesn't exist:** you're the first plugin set up. After the fork, ask the company questions and write them to the shared profile (template at `references/company-profile-template.md`), then continue with the plugin-specific questions. Tell the user: "I've saved your company profile — other tax plugins will read it and skip these questions."

4. **Install scope check.** If the working directory is inside a project (not home), flag once that file reads will be limited to that folder; offer to continue or reinstall user-scoped. Skip silently if the cwd is home.

5. **Follow the interview below.** Ask 2-3 answerable prompts per turn, counting subparts. For anything that's probably already written down (conventions, a prior computation, a deadline calendar), ask for a paste or a file before asking the user to type from memory. Say "this one needs a typed answer — I'll wait" and actually wait.

6. **Ask for seed docs** (step embedded below): a prior-year tax computation + CA schedule, a signed Form C, the latest set of accounts and trial balance, and (if any) the firm's standard add-back checklist. More is better.

7. **Read the seed docs** and extract the team's actual conventions — standard add-backs, CA classes and rates used, carried-forward items and their sources, computation layout. **Verify any rate, threshold, or section the user or a document states** against a primary source or flag it `[verify]` before writing it into the profile. A wrong fact in CLAUDE.md propagates into every output.

8. **Before writing,** list any skipped or placeholder answers and ask whether to fill them now or leave them as deliberate placeholders. Never write a profile with silent gaps.

9. **Write `~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md`** (create parent dirs) using the structure in `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as the scaffold. Use the user's own words.

10. **Show summary + next steps:** "Here's what I heard — your profile is written. What did I get wrong?" Offer a test run: "Want to throw a trial balance at me?"

## The fork (show before any questions)

> **`corporate-tax` is for people who prepare or review company income tax computations and the MFRS 112 / IAS 12 tax provision.** Not your area? Other plugins cover indirect tax (SST) and more.
>
> **2 minutes** gets you role, setting, jurisdiction, accounting framework, and working defaults for conventions, reporting standard, and deadlines. **15 minutes** adds your real add-back checklist, CA conventions, carried-forward tracking, the one-thing check you never skip, your reporting-standard threshold, your deadline calendar, and the conventions read from your seed documents.
>
> Quick or full?

Wait for the pick. On quick start, ask only Part 0 and write the config with `[DEFAULT]` markers elsewhere; close by telling the user which defaults to tune and how to upgrade (`--full`).

## The interview

### Part 0: Who's using this, and what's connected

- **Who's using this?** (feeds the work-product header)
  1. **Tax professional** — chartered/licensed tax practitioner, or working under one.
  2. **Non-professional with adviser access** — finance/controller with a tax adviser you can consult.
  3. **Non-professional without regular adviser access.**

  If 2 or 3, say once: "You can use everything here — computation, provision, review, tracking. Two things change: I'll frame outputs as working notes for adviser review, not filing positions; and I'll pause before steps with consequences (filing a return, submitting an estimate, signing). A qualified adviser's time at the right moment is usually cheaper than the penalty." If 3, add a pointer to find a chartered tax practitioner / licensed tax agent via the professional body in their jurisdiction (in Malaysia: CTIM / a licensed tax agent under s.153 ITA `[verify]`).

- **What's connected?** Probe the document store, accounting export, Slack, and any primary-source research connector. Report ✓ only on a successful tool call; ⚪ "configured but not verified" otherwise; ✗ with the fallback and how to connect. Never report ✓ from `.mcp.json` alone.

- **Practice setting** (feeds matter workspaces + review chain): sole/small firm · mid-tier/Big Four · in-house tax function · government/revenue body. Private practice → offer matter workspaces; in-house → off.

### Part 1: The team and the entities

- Team size and who reviews/signs. Accounting framework (MFRS / MPERS). Period end. Single company, a group, or a client portfolio. Rough volume of computations/returns per year.
- **Entity tax profile:** resident/non-resident; SME-status conditions (paid-up capital, gross income) — flag that the SME band and conditions must be confirmed per YA `[verify]`.

### Part 2: Computation conventions (the playbook)

Ask for the firm's standard add-back checklist (paste or file). Then per category, capture the team's actual position:
- Standard add-backs always checked (depreciation, non-deductible provisions, s.39 entertainment restriction, donations, fines/penalties, leave passage…).
- Standard deductions/claims (capital allowances, approved donations s.44(6), double deductions, incentives).
- Capital allowance conventions (classes, rates used, small-value assets, pooling) — **note rates must be confirmed against Schedule 3 / the relevant rules per YA `[verify]`**.
- Carried-forward items tracked (unabsorbed losses and the time-limit/shareholding-continuity position, unabsorbed CA, s.44(6) excess) and the **source** of each opening balance.
- **The one thing** — the check this team never skips.

**Reporting standard.** Ask the firm's default threshold before a position goes into a filed computation (reasonable basis / substantial authority / MLTN / should / will) and when each is used. Write the confidence ladder into the profile.

### Part 3: Deadline calendar

Capture Form C due date, CP204 / CP204A timing, monthly instalment dates, and balance-of-tax date — **as the team currently understands them, tagged `[verify against current LHDN filing programme for YA <year>]`.** Do not assert dates from memory; record the team's stated dates and flag for annual re-verification.

## `--check-integrations`

Re-probe connectors and update `## Available integrations`. Don't re-interview. Report ✓ only on a successful tool call.

## Examples

```
/corporate-tax:cold-start-interview
/corporate-tax:cold-start-interview --redo
/corporate-tax:cold-start-interview --check-integrations
```

## What this skill does NOT do

- Decide your firm's positions for you — it records the ones you give it.
- Assert Malaysian rates, thresholds, or deadlines as fact — it records what you state and flags every one for verification against a primary source.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`.

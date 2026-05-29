---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your tax controversy practice and write your
  practice profile. Use on first use of the plugin, when
  `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md` is missing or still
  contains template placeholders, or when the user says "set up the plugin", "configure
  controversy", "onboard me". This is the only skill that should run on a fresh install.
argument-hint: "[--redo] [--check-integrations] [--new-matter to set up and immediately open a first matter]"
---

# /cold-start-interview

Learns how this practice runs disputes and writes `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md`, which every other skill reads.

## Purpose

Meet this controversy practice for the first time and learn how *they* run disputes — their disputing body, their posture (settle early vs hold the line), their brief style, their deadline discipline — and write it into a living profile. They should feel like they onboarded a sharp dispute-resolution senior.

## Instructions

1. **Check current state** of the config path (exists / paused / placeholder / populated); migrate a populated cache config forward if present.
2. **Shared company profile** at `~/.claude/plugins/config/claude-for-tax/company-profile.md` — read/confirm if present; create from `references/company-profile-template.md` if absent.
3. **Install scope check** if cwd is inside a project.
4. **Fork:** 2-minute quick start vs 15-minute full. Wait.
5. **Run the interview** (below), 2-3 prompts per turn, asking for pastes/files before memory.
6. **Verify or flag** every deadline, section, and procedure the user states before writing it — a wrong deadline written into the profile is the most dangerous error this plugin can make.
7. **List open items** before writing; never write silent gaps.
8. **Write the profile** using `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as scaffold, in the user's words. Matter workspaces default ON.
9. **Offer to open the first matter:** "Want to open your most urgent matter now? `/controversy-tax:matter-intake`" — and if `--new-matter`, go straight there after writing the profile.

## The interview

### Part 0 — Role, integrations, setting
- **Role** (feeds the header and the gates): tax professional/agent / non-professional with adviser access / non-professional. If non-professional, say the two things that change (working-notes framing; a hard gate before objecting, appealing, or settling) and how to find a tax litigator / licensed tax agent. **Stress the deadline point regardless of role.**
- **What's connected?** Probe document store, Slack, primary-source research. ✓ only on a successful tool call.
- **Practice setting** → in-house (own disputes) vs firm (clients' disputes); matters default ON either way.

### Part 1 — The practice
Disputing body (LHDN / RMCD / both); whether you run your own disputes or clients'; who has settlement and signing authority; rough number of open matters; whether a tax litigator is briefed for SCIT/court and who.

### Part 2 — Dispute posture (the playbook)
Risk appetite in dispute (settle early / hold / litigate selectively); the team's concede-vs-proceed threshold; house brief/submission style; **the one thing** the team never skips on a new matter (usually: confirm and diarise the objection deadline first).

### Part 3 — Reporting standard
The default threshold to *hold* a position in dispute rather than concede, and when each rung applies. Write the ladder.

### Part 4 — Deadline calendar
The objection window (s.99 `[verify — typically 30 days from the notice]`), extension-of-time route, appeal-to-SCIT window (Form Q, Schedule 5 `[verify]`), time bar on raising assessments (s.91/s.91A `[verify — standard vs fraud/wilful default]`), and audit-query response norms — **as the team understands them, every date tagged `[verify against the ITA and current LHDN procedure]`.** Do not assert any deadline from memory.

## `--check-integrations`
Re-probe connectors; update `## Available integrations`. ✓ only on a successful tool call.

## Examples
```
/controversy-tax:cold-start-interview
/controversy-tax:cold-start-interview --new-matter
/controversy-tax:cold-start-interview --redo
```

## What this skill does NOT do
- Open a matter by itself (use `--new-matter` or `/controversy-tax:matter-intake`). - Assert objection/appeal deadlines or procedure as fact — it flags every one for verification.

## Close with the next-steps decision tree per CLAUDE.md `## Outputs`.

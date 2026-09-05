---
name: cold-start-interview
description: >
  Set up the Tax Builder Hub — learn the user's practice and tooling comfort, record
  their role for other tax plugins to read, and configure watched registries and update
  preferences. Use on first use, when the hub config is missing or placeholder, or when
  the user says "set up the hub", "configure builder hub".
argument-hint: "[--redo] [--check-integrations]"
---

# /cold-start-interview

Writes `~/.claude/plugins/config/claude-for-tax/tax-builder-hub/CLAUDE.md`.

## Instructions

1. **Check state** of the config path (exists / paused / placeholder / populated); migrate a populated cache config forward if present.
2. **Shared company profile** at `~/.claude/plugins/config/claude-for-tax/company-profile.md` — read/confirm if present; create from `references/company-profile-template.md` if absent. The hub is often the first plugin a builder sets up.
3. **Part 0 — Role.** Tax professional / non-professional with adviser access / non-professional. Write it to `## Who's using this` so other tax plugins can read it.
4. **Integrations.** Probe Slack (✓ only on a successful tool call).
5. **Practice + tooling.** Practice type, primary jurisdiction (default Malaysia), tooling comfort.
6. **Registries + updates.** Which community registries to watch; update preference (notify is the default — every update requires approval); new-skill notification scope.
7. **Trusted sources (allowlist).** Ask which registries/publishers (if any) the firm trusts, and write them to `## Trusted sources (allowlist)`. Default is empty — explain that nothing is allowlisted until deliberately added, and that the allowlist only changes install friction, never whether QA runs. Don't pre-populate it with a registry just because it's watched; watching ≠ trusting.
8. **Write** the config using `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` as scaffold; summarise.

## What this skill does NOT do
- Install anything (that's `/tax-builder-hub:skill-installer`).
- Override an installed skill's own headers or guardrails.
- Allowlist a source the user didn't explicitly name.

## Close with a short summary and a pointer to browse (`/tax-builder-hub:registry-browser`) or evaluate a skill (`/tax-builder-hub:skills-qa`).

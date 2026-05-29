# Tax Builder Hub

The trust layer for community tax skills. Discover, evaluate, and install community-built tax skills — with a design-quality review (the **Tax Skill Design Framework**) and a prompt-injection / trust-surface gate before anything lands in your environment.

A tax professional installing a random skill from the internet is installing code that runs with access to their source documents, their practice profile, and (often) their clients' financial data and revenue-portal connectors. The hub gives that the review a careful person would do if they could read code.

## Setup first

```
/plugin install tax-builder-hub@claude-for-tax
# restart Claude Code
/tax-builder-hub:cold-start-interview
```

## Commands

| Command | What it does |
|---|---|
| `/tax-builder-hub:cold-start-interview` | Set up the hub; record your role for other tax plugins to read; configure watched registries and the trusted-source allowlist |
| `/tax-builder-hub:registry-browser` | Discover skills from watched registries — list, surface what's new since last sync, filter to your practice; never installs |
| `/tax-builder-hub:skills-qa` | Evaluate a skill against the Tax Skill Design Framework — 13 parameters, 3 tax failure modes, injection scan, verdict |
| `/tax-builder-hub:skill-installer` | Install through the trust gate — full QA, allowlist check, plain-English trust-surface summary, explicit go-ahead, version pinned and logged; never installs past a REFUSE |
| `/tax-builder-hub:auto-updater` | Check installed skills for updates — re-run the injection scan, diff the security surface against the pinned version, fail-closed on regression; never silently updates |
| `/tax-builder-hub:related-skills-surfacer` | Surface complements, alternatives, and would-be conflicts for what you're doing or already have installed |

## The trust gate

Discovery and installation are deliberately separate, and nothing runs code without passing through the gate:

1. **Browse** (`registry-browser`) reads registries as untrusted listings and badges each source 🟢/⚪/🟠 — provenance only, never a quality verdict.
2. **QA** (`skills-qa`) scores design and scans for injection — at install *and* at update time.
3. **Install** (`skill-installer`) runs the full QA, checks the allowlist, shows what the skill can do in plain English, and installs only the reviewed version on an explicit go-ahead — pinning it and logging it. A REFUSE verdict has no "install anyway" path.
4. **Update** (`auto-updater`) treats every new version as untrusted, diffs the security surface against the pinned version, and fails closed on any regression — because the trusted-publisher-poisoned-update is the attack that matters here.

## The Tax Skill Design Framework

`/tax-builder-hub:skills-qa` scores any skill on:

- **13 design parameters** — Audience, Work Shape, Delegation Threshold, Input Requirements, Versioning/Ownership, Confidence Bands (mapped to the reporting-standard ladder), Failure Modes, Scope Boundaries, Escalation Logic, Trust Surface, Freshness, Schema, Conflicts.
- **3 tax-specific failure modes** — *tax advice vs. tax support* (is the signing preparer/taxpayer the decision-maker?), *authority & currency integrity* (does it treat authority as verify-by-default and handle the annual-change problem, or hardcode rates?), and *figure integrity* (does it source every figure and tie every computation, or type numbers from memory?).
- **A prompt-injection heuristic scan** run at install *and* update time, fail-closed on regression.
- **A four-band verdict** — Ready / Some Concern / Material Concerns / Refuse.

Run it before incorporating any community skill, and against your own first-party skills before deploying them to a team.

## What this plugin does NOT do

- Produce tax work product — it discovers, QAs, installs, and updates skills.
- Override an installed skill's own headers or guardrails.
- Auto-install or silently update — every install and update needs an explicit go-ahead; a REFUSE verdict has no override.
- Guarantee a skill is safe — the QA is a heuristic AI review, not a security audit. Read the raw SKILL.md, and in firm deployments install only from allowlisted sources.

# CLAUDE.md

Guidance for working on this repo. `claude-for-tax` is a Claude Code plugin
marketplace — a set of first-party tax plugins plus (later) managed-agent
cookbooks. Most work here is editing prompt content (skills, agents, hooks),
plugin metadata, or cookbook config — not application code.

It is modelled directly on `anthropics/claude-for-legal`: same architecture,
same robustness spine, the legal nouns swapped for tax nouns and the default
jurisdiction set to **Malaysia**. If you are unsure how something should be
shaped, look at how the legal repo does the equivalent and mirror it.

## The one rule that governs everything

**Truth, always verify, never assume.** This repo's domain is tax, where a
confident wrong number or a fabricated statutory reference is worse than a gap.
Two consequences run through every plugin:

1. **Every authority is `[model knowledge — verify]` by default.** Malaysian tax
   authority (Income Tax Act 1967 sections, Public Rulings, SST orders, gazette
   orders, current rates and thresholds) recalled from training is treated as
   unverified until checked against an LHDN/RMCD primary source or pasted by the
   user. Do not promote a tag because a cite "feels right."
2. **Every figure traces to a source and ties to the computation.** No number is
   typed from memory. Each amount carries a source reference; each computation
   carries CHECK cells that reconcile back to the trial balance, financial
   statements, or return total. A working paper that doesn't tie is not done.

These are not disclaimers bolted on at the end — they are encoded in each
plugin's `## Shared guardrails` and in the skills themselves.

## Layout

```
.claude-plugin/marketplace.json   # the marketplace manifest — one entry per plugin
<plugin>/                         # first-party plugins (corporate-tax, indirect-tax, ...)
  .claude-plugin/plugin.json      # plugin manifest (name, version, description, author)
  .mcp.json                       # MCP servers the plugin connects to
  CLAUDE.md                       # practice-profile TEMPLATE (see "Plugin CLAUDE.md" below)
  README.md                       # per-plugin docs
  skills/<name>/SKILL.md          # one skill per directory
  agents/<name>.md                # subagent definitions (scheduled / event-driven)
  hooks/hooks.json                # hook config (most plugins ship an empty stub)
references/                       # shared templates (company-profile, dashboard, excel-output workbook recipe)
managed-agent-cookbooks/          # headless deployable agents (deadline-watcher, sst-period-watcher)
  <cookbook>/orchestrator.yaml    #   read-only orchestrator + one concrete egress (Slack send)
  <cookbook>/readers/*.yaml       #   read-only reader leaves with inline output_schema
  <cookbook>/steering-examples.json #  example invocations (scheduled / single-plugin / red-only / dry-run)
scripts/                          # validation (check-conventions, check-guardrails, test-cookbooks,
                                  #   lint-tool-scope), run-time harness (validate.py,
                                  #   deploy-managed-agent.sh), and orchestrate.py (reference only)
                                  #   — see scripts/README.md
.github/workflows/                # cla.yaml (CLA) + validate.yaml (the checks below)
CONTRIBUTING.md / CODE_OF_CONDUCT.md / CONNECTORS.md / CLA.md   # governance
```

The managed-agent cookbooks are YAML, not plugin markdown, and follow their own
convention (`role`, `tools`, inline `output_schema`, `readers`). They are not part
of the marketplace; `scripts/lint-tool-scope.py` is their validator (least-privilege
check), `scripts/test-cookbooks.sh` is their hermetic CI check (lint + structural
well-formedness, no model needed), and `scripts/deploy-managed-agent.sh` is their
deploy harness (lint → run readers → `validate.py` → orchestrator → post, failing
closed at each seam). The shipped cookbooks post directly via one pinned egress;
`scripts/orchestrate.py` is a **reference only** for the step up to cross-agent
handoffs (closed-schema intents, target allowlist, data-frame wrapping, audit log).

## Validation — run before committing

The Python checks need two libraries. Install them once:

```bash
pip install -r scripts/requirements.txt
```

Then:

```bash
# Per-plugin + marketplace schema validation (if claude CLI is available)
claude plugin validate .claude-plugin/marketplace.json
for d in */; do [ -f "$d/.claude-plugin/plugin.json" ] && claude plugin validate "$d"; done

# JSON sanity (always available)
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True)]"

# Managed-agent cookbooks — hermetic (no model needed)
bash scripts/test-cookbooks.sh

# Repo conventions: whitespace, 2-space JSON, frontmatter, dead /plugin:skill
# references, marketplace-vs-plugin.json parity
python3 scripts/check-conventions.py

# Guardrail coverage: every plugin carries all 12 canonical rules
python3 scripts/check-guardrails.py
```

`.github/workflows/validate.yaml` runs the last four on every push and pull
request, so a broken one fails CI rather than being discovered by a user.

### Frontmatter requirements

Every `skills/<name>/SKILL.md` needs `name` and `description`. Every
`agents/*.md` needs `name` and `description`. Keep skill `description` under
1024 characters — it is the trigger signal. Mark pure-reference skills
`user-invocable: false`.

### Naming

- Plugin `name` must match `^[a-z0-9][a-z0-9-]{1,63}$`.
- Skill names referenced in prose ("run `/corporate-tax:tax-computation`") must
  be the actual `skills/<name>/` directory name. Short forms look right in prose
  but are dead commands.
- `marketplace.json`'s `name`/`description`/`author` for a first-party plugin
  should match that plugin's own `.claude-plugin/plugin.json` field for field.

## Conventions

### Plugin CLAUDE.md is a template, not project context

Each `<plugin>/CLAUDE.md` is a practice-profile template that the
`cold-start-interview` skill copies to
`~/.claude/plugins/config/claude-for-tax/<plugin>/CLAUDE.md` on the user's
machine. It is *not* loaded as project context when the plugin is installed.
Don't "fix" the placeholders by moving content into a skill — the placeholders
are the point.

### The shared guardrails block is canonical and repeated

Every plugin's `CLAUDE.md` carries the full `## Shared guardrails` block. It is
intentionally duplicated per plugin (so each plugin is self-contained) and is
the source of truth — when a skill's text conflicts with it, the guardrails
win.

**What is shared is the rule SET, not the prose.** All twelve rules appear in
every plugin: figures-trace, no-silent-supplement, currency-trigger,
verify-user-stated, quote-or-decline, pre-flight, source-tags, tag-vocabulary,
destination-check, severity-floor, file-access, verification-log. Each plugin
states them in its own domain's nouns — SST gazette orders in `indirect-tax`,
treaty texts and comparables in `international-tax`, the matter file in
`controversy-tax` — and some plugins add a domain rule of their own (never
fabricate comparables; the employer carries the under-deduction liability).
Some blocks are consequently longer than others, and that is fine.

What is NOT fine is a plugin losing a rule during a copy, which is invisible
because the block still reads as complete. `scripts/check-guardrails.py` pins
the rule set and runs in CI. When you add a guardrail, add it to every plugin
*and* to `CANONICAL_RULES` in that script; when you reword one, keep its bold
lead-in recognisable or update the accepted spellings there.

### Jurisdiction default is Malaysia

Default frameworks, statutes, rates, and procedures are Malaysian (ITA 1967,
Sales Tax Act 2018, Service Tax Act 2018, LHDN/RMCD practice, MFRS). When facts
involve another jurisdiction, the `## Jurisdiction recognition` guardrail fires
— recognise it, don't silently apply Malaysian rules to non-Malaysian facts.

### Formatting

- 2-space indent in all JSON and `.mcp.json` files.
- Final newline at end of every text file.
- No trailing whitespace.

## Things to leave alone

- `hooks/hooks.json` ships as an empty stub (`{"hooks": {}}`) in most plugins.
  Hooks are optional; the empty stub is not a bug.
- `references/` lives only at repo root and is referenced by plugin CLAUDE.md
  templates as if it were inside the plugin — that mirrors the legal repo's
  known gap. Don't silently relocate it.

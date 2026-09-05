#!/usr/bin/env python3
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
"""Guardrail-coverage lint for every plugin CLAUDE.md.

CLAUDE.md says the `## Shared guardrails` block is canonical and duplicated per
plugin. Duplication drifts silently: a rule gets dropped from one plugin during
a copy and nothing notices, because each plugin still *looks* complete on its
own. This lint pins the rule SET without forcing identical prose, so each plugin
keeps its domain wording (SST gazette orders, treaty texts, matter files) while
no plugin can quietly lose a rule.

What it checks, per plugin:
  1. A `## Shared guardrails` section exists.
  2. Every canonical rule below appears in it, matched on the rule's bold lead-in.
  3. The plugin's own config path appears in the verification-log rule, so a
     copied block can't point at another plugin's log.
  4. The sections that sit below the guardrails (jurisdiction recognition,
     retrieved-content trust, large input/output) are present.

Usage: check-guardrails.py
Exits 0 clean, 1 on any finding.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# rule key -> list of accepted bold lead-ins (a plugin may phrase its own domain
# version, e.g. "Facts and figures trace to source" in controversy-tax).
CANONICAL_RULES: dict[str, tuple[str, ...]] = {
    "figures-trace": ("Figures trace", "Facts and figures trace"),
    "no-silent-supplement": ("No silent supplement",),
    "currency-trigger": ("Currency trigger",),
    "verify-user-stated": ("Verify user-stated",),
    "quote-or-decline": ("When disagreeing with a cited",),
    "pre-flight": ("Pre-flight check",),
    "source-tags": ("Source tags describe what you actually did",),
    "tag-vocabulary": ("Tag vocabulary",),
    "destination-check": ("Destination check",),
    "severity-floor": ("Cross-skill severity floor",),
    "file-access": ("File access failures",),
    "verification-log": ("Verification log",),
}

# Sections that must follow the guardrails block in every plugin.
REQUIRED_SECTIONS = (
    "## Scaffolding, not blinders",
    "## Jurisdiction recognition",
    "## Retrieved-content trust",
)

errors: list[str] = []


def main() -> int:
    plugins = sorted(p.parent.parent for p in ROOT.glob("*/.claude-plugin/plugin.json"))
    if not plugins:
        print("check-guardrails: no plugins found", file=sys.stderr)
        return 1

    for plugin in plugins:
        name = plugin.name
        path = plugin / "CLAUDE.md"
        if not path.exists():
            errors.append(f"{name}: no CLAUDE.md")
            continue
        text = path.read_text()

        if "## Shared guardrails" not in text:
            errors.append(f"{name}: no '## Shared guardrails' section")
            continue
        start = text.index("## Shared guardrails")
        rest = text[start + 1 :]
        nxt = re.search(r"^## ", rest, re.M)
        block = rest[: nxt.start()] if nxt else rest

        bold_leads = re.findall(r"\*\*([^*]+?)\*\*", block)
        for key, accepted in CANONICAL_RULES.items():
            if not any(lead.startswith(a) for lead in bold_leads for a in accepted):
                errors.append(f"{name}: guardrails missing rule '{key}' (expected one of {accepted})")

        log_path = f"claude-for-tax/{name}/verification-log.md"
        if "Verification log" in block and log_path not in block:
            errors.append(f"{name}: verification-log rule does not point at {log_path}")

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{name}: missing section '{section}'")

    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print(f"check-guardrails: {len(errors)} finding(s)", file=sys.stderr)
        return 1
    print(f"check-guardrails: {len(plugins)} plugins carry all {len(CANONICAL_RULES)} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())

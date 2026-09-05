#!/usr/bin/env python3
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
"""Repo convention checks that need no model and no network.

Enforces the rules CLAUDE.md states, so they stop drifting:

  1. Text files end with a newline; no trailing whitespace.
  2. JSON files parse and use 2-space indentation.
  3. Every skill validates against the Agent Skills spec (agentskills.io) via
     the spec's own `skills_ref` library, plus the house rules it doesn't cover:
     name matches the directory, and `license` and `metadata` are present.
     Every agents/*.md has `name` and `description`.
  4. Every `/<plugin>:<skill>` reference in prose resolves to a real skill
     directory (short forms look right and are dead commands).
  5. Each plugin ships the shared templates it cites, in sync with the canonical
     copies at repo root.
  6. marketplace.json entries match the plugin's own plugin.json field for field.

Usage: check-conventions.py [--fix-whitespace]
Exits 0 clean, 1 on any finding.
"""
import json
import re
import sys
from pathlib import Path

import skills_ref
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", "node_modules", "signatures"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".txt", ".gitkeep"}

errors: list[str] = []


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def walk() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def check_whitespace(files: list[Path], fix: bool) -> None:
    for p in files:
        if p.suffix not in TEXT_SUFFIXES and p.name != ".gitkeep":
            continue
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        if text == "":
            continue
        fixed = "\n".join(line.rstrip() for line in text.split("\n"))
        if not fixed.endswith("\n"):
            fixed += "\n"
        if fixed == text:
            continue
        if fix:
            p.write_text(fixed)
            continue
        if any(line != line.rstrip() for line in text.split("\n")):
            errors.append(f"{rel(p)}: trailing whitespace")
        if not text.endswith("\n"):
            errors.append(f"{rel(p)}: missing final newline")


def check_json(files: list[Path]) -> None:
    for p in files:
        if p.suffix != ".json":
            continue
        text = p.read_text()
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            errors.append(f"{rel(p)}: invalid JSON: {e}")
            continue
        # 2-space indent: no tabs, and every indent is a multiple of 2.
        for lineno, line in enumerate(text.split("\n"), 1):
            if "\t" in line:
                errors.append(f"{rel(p)}:{lineno}: tab in JSON (use 2-space indent)")
                break
            indent = len(line) - len(line.lstrip(" "))
            if line.strip() and indent % 2:
                errors.append(f"{rel(p)}:{lineno}: indent of {indent} is not a multiple of 2")
                break


def parse_frontmatter(p: Path) -> dict | None:
    m = re.match(r"---\n(.*?)\n---\n", p.read_text(), re.S)
    if not m:
        errors.append(f"{rel(p)}: missing YAML frontmatter")
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{rel(p)}: frontmatter is not valid YAML: {e}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{rel(p)}: frontmatter is not a mapping")
        return None
    return data


# The single frontmatter field we knowingly carry beyond the Agent Skills spec.
# Claude Code reads top-level `argument-hint` and uses it to prompt for input when
# a skill is invoked with no arguments; the spec has no equivalent, and moving it
# under `metadata` would lose that behaviour because Claude Code does not look
# there. Other spec clients ignore unknown fields. Every OTHER unknown field is a
# real error — this allowance is deliberately narrow, not a blanket mute.
SPEC_DEVIATIONS = ("argument-hint",)

_UNEXPECTED = re.compile(r"^Unexpected fields in frontmatter: (.+?)\. Only ")


def _is_allowed_deviation(spec_error: str) -> bool:
    m = _UNEXPECTED.match(spec_error)
    if not m:
        return False
    found = {f.strip() for f in m.group(1).split(",")}
    return found.issubset(set(SPEC_DEVIATIONS))


def check_skills_spec() -> None:
    """Validate every skill against the Agent Skills spec (agentskills.io).

    skills_ref is the spec's own reference implementation, so it — not this
    script — is the authority on name/description rules. We add the house
    conventions it does not cover.
    """
    for p in sorted(ROOT.glob("*/skills/*/SKILL.md")):
        # NOTE: skills_ref.validate RETURNS a list of error strings; it does not
        # raise. Wrapping it in try/except passes everything silently.
        try:
            spec_errors = skills_ref.validate(p.parent)
        except Exception as e:  # noqa: BLE001 — a crash is itself a failure
            errors.append(f"{rel(p)}: skills_ref crashed: {type(e).__name__}: {e}")
            continue
        for se in spec_errors:
            if _is_allowed_deviation(se):
                continue
            errors.append(f"{rel(p)}: Agent Skills spec: {se}")
        fields = parse_frontmatter(p)
        if fields is None:
            continue
        # House conventions on top of the spec.
        if fields.get("name") != p.parent.name:
            errors.append(
                f"{rel(p)}: frontmatter name {fields.get('name')!r} != directory {p.parent.name!r}"
            )
        if not fields.get("license"):
            errors.append(f"{rel(p)}: missing 'license' (every skill here is Apache-2.0)")
        meta = fields.get("metadata")
        if not isinstance(meta, dict):
            errors.append(f"{rel(p)}: missing 'metadata' mapping (author, version)")
        else:
            for key in ("author", "version"):
                if not meta.get(key):
                    errors.append(f"{rel(p)}: metadata missing '{key}'")
            for k, v in meta.items():
                if not isinstance(v, str):
                    errors.append(f"{rel(p)}: metadata.{k} must be a string (spec requires a string map)")


def check_agent_frontmatter() -> None:
    for p in sorted(ROOT.glob("*/agents/*.md")):
        fields = parse_frontmatter(p)
        if fields is None:
            continue
        for required in ("name", "description"):
            if not fields.get(required):
                errors.append(f"{rel(p)}: frontmatter missing '{required}'")


def check_skill_references(files: list[Path]) -> None:
    plugins = {p.parent.parent.name for p in ROOT.glob("*/.claude-plugin/plugin.json")}
    pattern = re.compile(r"/([a-z0-9-]+):([a-z0-9-]+)")
    for p in files:
        if p.suffix not in {".md", ".json", ".yaml", ".yml"}:
            continue
        for lineno, line in enumerate(p.read_text().split("\n"), 1):
            for plugin, skill in pattern.findall(line):
                if plugin not in plugins:
                    continue
                if not (ROOT / plugin / "skills" / skill).is_dir():
                    errors.append(
                        f"{rel(p)}:{lineno}: /{plugin}:{skill} has no skills/{skill}/ directory"
                    )


def check_references_in_sync() -> None:
    """Each plugin ships its own copy of the shared templates.

    A plugin's paths cannot escape its own directory at runtime, so the root
    `references/` cannot be read from inside an installed plugin — the copies are
    required, not redundant. Root stays canonical; this catches divergence.
    """
    root_refs = ROOT / "references"
    for plugin_refs in sorted(ROOT.glob("*/references")):
        if plugin_refs.parent == ROOT:
            continue
        for copy in sorted(plugin_refs.glob("*.md")):
            canonical = root_refs / copy.name
            if not canonical.exists():
                errors.append(f"{rel(copy)}: no canonical references/{copy.name} at repo root")
            elif copy.read_text() != canonical.read_text():
                errors.append(
                    f"{rel(copy)}: out of sync with references/{copy.name} "
                    f"(root is canonical; re-copy it)"
                )
    # And every plugin-root-relative citation must resolve to a shipped file.
    cite = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/references/([a-z0-9-]+\.md)")
    for p in sorted(ROOT.glob("*/CLAUDE.md")) + sorted(ROOT.glob("*/skills/*/SKILL.md")):
        plugin = ROOT / p.relative_to(ROOT).parts[0]
        for name in cite.findall(p.read_text()):
            if not (plugin / "references" / name).exists():
                errors.append(f"{rel(p)}: cites references/{name}, which {plugin.name} does not ship")


def check_marketplace() -> None:
    mpath = ROOT / ".claude-plugin" / "marketplace.json"
    if not mpath.exists():
        errors.append("marketplace.json missing")
        return
    market = json.loads(mpath.read_text())
    for entry in market.get("plugins", []):
        source = entry.get("source", "").lstrip("./")
        manifest = ROOT / source / ".claude-plugin" / "plugin.json"
        if not manifest.exists():
            errors.append(f"marketplace.json: {entry.get('name')} source has no plugin.json")
            continue
        plugin = json.loads(manifest.read_text())
        for field in ("name", "description", "author"):
            if entry.get(field) != plugin.get(field):
                errors.append(
                    f"marketplace.json: {entry.get('name')} '{field}' differs from {source}/.claude-plugin/plugin.json"
                )


def main() -> int:
    fix = "--fix-whitespace" in sys.argv[1:]
    files = walk()
    check_whitespace(files, fix)
    check_json(files)
    check_skills_spec()
    check_agent_frontmatter()
    check_skill_references(files)
    check_references_in_sync()
    check_marketplace()
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print(f"check-conventions: {len(errors)} finding(s)", file=sys.stderr)
        return 1
    print(f"check-conventions: {len(files)} files clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

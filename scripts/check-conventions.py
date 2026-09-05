#!/usr/bin/env python3
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
"""Repo convention checks that need no model and no network.

Enforces the rules CLAUDE.md states, so they stop drifting:

  1. Text files end with a newline; no trailing whitespace.
  2. JSON files parse and use 2-space indentation.
  3. Every skills/<name>/SKILL.md and agents/*.md has `name` and `description`
     frontmatter; skill `description` stays under 1024 characters; the skill's
     `name` matches its directory name.
  4. Every `/<plugin>:<skill>` reference in prose resolves to a real skill
     directory (short forms look right and are dead commands).
  5. marketplace.json entries match the plugin's own plugin.json field for field.

Usage: check-conventions.py [--fix-whitespace]
Exits 0 clean, 1 on any finding.
"""
import json
import re
import sys
from pathlib import Path

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
    text = p.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{rel(p)}: missing YAML frontmatter")
        return None
    block = m.group(1)
    fields: dict[str, str] = {}
    key = None
    for line in block.split("\n"):
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fields[key] = km.group(2).strip()
        elif key is not None and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def check_frontmatter() -> None:
    for p in sorted(ROOT.glob("*/skills/*/SKILL.md")):
        fields = parse_frontmatter(p)
        if fields is None:
            continue
        for required in ("name", "description"):
            if not fields.get(required):
                errors.append(f"{rel(p)}: frontmatter missing '{required}'")
        name = fields.get("name", "")
        if name and name != p.parent.name:
            errors.append(
                f"{rel(p)}: frontmatter name {name!r} != directory {p.parent.name!r}"
            )
        desc = fields.get("description", "")
        if len(desc) > 1024:
            errors.append(f"{rel(p)}: description is {len(desc)} chars (max 1024)")
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
    check_frontmatter()
    check_skill_references(files)
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

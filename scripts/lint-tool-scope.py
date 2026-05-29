#!/usr/bin/env python3
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
"""Least-privilege linter for the tax managed-agent cookbooks.

For a headless agent that runs unattended, the tool scope IS the security
boundary — there is no human to catch an over-broad grant at run time. This
linter fails the build (exit 1) if any agent YAML violates the cookbook's
least-privilege invariants. deploy-managed-agent.sh runs it before deploying.

Invariants
----------
Every agent (role: reader | orchestrator):
  * parses as YAML and declares name, role, tools (a list).
  * carries NO mutating/eval/network tool: Write, Edit, MultiEdit, NotebookEdit,
    Bash, WebFetch, WebSearch.
  * carries NO wildcard tool — any name containing '*' (e.g. mcp__*__send) is a
    finding: a wildcard is the opposite of a pinned scope.

Reader leaves (role: reader):
  * tools are a subset of the read-only allowlist {Read, Glob, LS}.
  * declare an `output_schema` (so the harness can validate their output).
  * do NOT declare `readers` (a leaf does not orchestrate).

Orchestrators (role: orchestrator):
  * tools are a subset of {Read, Glob, LS} PLUS at most the egress allowlist
    (default: mcp__slack__send_message). Egress must be a concrete, named tool.
  * declare a `readers` list (the leaves they consume).
  * do NOT declare an `output_schema` (the orchestrator is the terminal poster,
    not a validated producer).

Usage
-----
  lint-tool-scope.py [path ...] [--egress TOOL ...]

With no path, lints every *.yaml under ../managed-agent-cookbooks relative to
this script. --egress may be repeated to allow additional concrete egress tools
for orchestrators (still never wildcards).
"""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("lint-tool-scope: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

READ_ONLY = {"Read", "Glob", "LS"}
FORBIDDEN = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Bash", "WebFetch", "WebSearch"}
DEFAULT_EGRESS = {"mcp__slack__send_message"}


def _violations(path: Path, doc: dict, egress: set[str]) -> list[str]:
    out: list[str] = []
    name = doc.get("name", path.stem)
    role = doc.get("role")
    tools = doc.get("tools")

    if role not in ("reader", "orchestrator"):
        out.append(f"role must be 'reader' or 'orchestrator' (got {role!r})")
        # keep checking what we can
    if not isinstance(tools, list) or not all(isinstance(t, str) for t in tools):
        out.append("tools must be a list of strings")
        return [f"[{name}] {v}" for v in out]

    tool_set = set(tools)

    for t in sorted(tool_set & FORBIDDEN):
        out.append(f"forbidden tool for a headless agent: {t}")
    for t in sorted(t for t in tool_set if "*" in t):
        out.append(f"wildcard tool not allowed (pin the concrete tool): {t}")

    if role == "reader":
        extra = tool_set - READ_ONLY
        for t in sorted(extra):
            if "*" not in t and t not in FORBIDDEN:  # already reported above
                out.append(f"reader leaf may only use {sorted(READ_ONLY)}; remove: {t}")
        if "output_schema" not in doc:
            out.append("reader leaf must declare an output_schema (so the harness can validate its output)")
        if "readers" in doc:
            out.append("reader leaf must not declare `readers` (a leaf does not orchestrate)")

    elif role == "orchestrator":
        allowed = READ_ONLY | egress
        extra = tool_set - allowed
        for t in sorted(extra):
            if "*" not in t and t not in FORBIDDEN:
                out.append(
                    f"orchestrator may only use {sorted(READ_ONLY)} plus a concrete egress tool "
                    f"({sorted(egress)}); remove or pin: {t}"
                )
        if not isinstance(doc.get("readers"), list) or not doc["readers"]:
            out.append("orchestrator must declare a non-empty `readers` list")
        if "output_schema" in doc:
            out.append("orchestrator must not declare an output_schema (it is the terminal poster, not a validated leaf)")

    return [f"[{name}] {v}" for v in out]


def main() -> int:
    args = sys.argv[1:]
    egress = set(DEFAULT_EGRESS)
    paths: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--egress":
            if i + 1 >= len(args):
                print("lint-tool-scope: --egress needs a tool name", file=sys.stderr)
                return 2
            egress.add(args[i + 1])
            i += 2
        else:
            paths.append(args[i])
            i += 1

    if any("*" in t for t in egress):
        print("lint-tool-scope: egress tools must be concrete, not wildcards", file=sys.stderr)
        return 2

    if paths:
        targets: list[Path] = []
        for p in paths:
            pp = Path(p)
            targets.extend(sorted(pp.rglob("*.yaml")) if pp.is_dir() else [pp])
    else:
        root = Path(__file__).resolve().parent.parent / "managed-agent-cookbooks"
        targets = sorted(root.rglob("*.yaml"))

    if not targets:
        print("lint-tool-scope: no agent YAML files found", file=sys.stderr)
        return 2

    total = 0
    for path in targets:
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            print(f"FAIL {path}: not valid YAML — {e}")
            total += 1
            continue
        if not isinstance(doc, dict):
            print(f"FAIL {path}: top-level YAML is not a mapping")
            total += 1
            continue
        violations = _violations(path, doc, egress)
        if violations:
            total += len(violations)
            print(f"FAIL {path}")
            for v in violations:
                print(f"  - {v}")
        else:
            print(f"ok   {path}  ({doc.get('role')}, tools={doc.get('tools')})")

    if total:
        print(f"\nlint-tool-scope: {total} violation(s) — refusing the build.", file=sys.stderr)
        return 1
    print(f"\nlint-tool-scope: {len(targets)} agent(s) clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
#
# Hermetic structural test for every managed-agent cookbook. Asserts each cookbook
# is well-formed WITHOUT calling a model, so it runs in CI:
#
#   1. lint-tool-scope.py            — least-privilege on every agent YAML (fail closed).
#   2. orchestrator.yaml             — parses; declares name/role/tools/inputs/instructions;
#                                      role == orchestrator; lists readers that exist on disk.
#   3. readers/*.yaml                — parse; declare name/role/tools/inputs/instructions;
#                                      role == reader; carry an output_schema that is itself a
#                                      VALID JSON Schema (the load-bearing seam — the deploy
#                                      harness validates each reader's JSON against it at run time).
#
# Tax's deploy --dry-run actually runs the reader model against live configs, so it
# is NOT hermetic; this test covers everything that can be checked without a model.
# Exits non-zero if any cookbook fails.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

echo "test-cookbooks: [1/2] least-privilege lint"
if ! python3 "$ROOT/scripts/lint-tool-scope.py"; then
  echo "  ✗ tool-scope lint" >&2
  fail=1
fi

echo "test-cookbooks: [2/2] structural well-formedness"
for d in "$ROOT"/managed-agent-cookbooks/*/; do
  [ -f "$d/orchestrator.yaml" ] || continue
  slug=$(basename "$d")
  if python3 - "$d" "$slug" <<'PY'
import sys, pathlib, yaml, jsonschema

d = pathlib.Path(sys.argv[1]); slug = sys.argv[2]
errs = []

def load(p):
    try:
        return yaml.safe_load(p.read_text())
    except Exception as e:  # noqa: BLE001 — report any parse failure
        errs.append(f"{p.name}: YAML parse error: {e}")
        return None

REQ = ("name", "role", "tools", "inputs", "instructions")

orch = load(d / "orchestrator.yaml")
if orch is not None:
    for k in REQ:
        if not orch.get(k):
            errs.append(f"orchestrator.yaml: missing/empty '{k}'")
    if orch.get("role") != "orchestrator":
        errs.append(f"orchestrator.yaml: role is {orch.get('role')!r}, expected 'orchestrator'")
    if not isinstance(orch.get("tools"), list):
        errs.append("orchestrator.yaml: 'tools' must be a list")
    # readers it names must exist
    for r in (orch.get("readers") or []):
        if not (d / r).exists():
            errs.append(f"orchestrator.yaml: readers entry '{r}' not found on disk")

readers = sorted((d / "readers").glob("*.yaml")) if (d / "readers").is_dir() else []
if not readers:
    errs.append("no readers/*.yaml found")
for rp in readers:
    r = load(rp)
    if r is None:
        continue
    for k in REQ:
        if not r.get(k):
            errs.append(f"readers/{rp.name}: missing/empty '{k}'")
    if r.get("role") != "reader":
        errs.append(f"readers/{rp.name}: role is {r.get('role')!r}, expected 'reader'")
    if not isinstance(r.get("tools"), list):
        errs.append(f"readers/{rp.name}: 'tools' must be a list")
    schema = r.get("output_schema")
    if not schema:
        errs.append(f"readers/{rp.name}: missing output_schema (the validation seam)")
    else:
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as e:
            errs.append(f"readers/{rp.name}: output_schema is not a valid JSON Schema: {e.message}")

if errs:
    for e in errs:
        print(f"      {e}", file=sys.stderr)
    sys.exit(1)
print(f"  ✓ {slug:24s} orchestrator + {len(readers)} reader(s), schemas valid")
PY
  then :; else
    echo "  ✗ $slug" >&2
    fail=1
  fi
done

exit $fail

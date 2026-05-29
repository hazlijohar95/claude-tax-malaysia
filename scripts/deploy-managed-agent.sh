#!/usr/bin/env bash
# Copyright 2026 Hazli Johar
# SPDX-License-Identifier: Apache-2.0
#
# deploy-managed-agent.sh — reference deploy harness for the tax managed-agent
# cookbooks (deadline-watcher, sst-period-watcher).
#
# It enforces the seams the cookbook depends on, in order, FAILING CLOSED at each:
#   1. lint-tool-scope.py        — least-privilege check on every agent YAML.
#   2. run each reader headless  — with ONLY the tools the leaf declares.
#   3. validate.py               — the reader's JSON against its inline output_schema.
#                                  An invalid leaf output is dropped, never posted.
#   4. run the orchestrator      — fed only validated reader JSON; it posts once.
#
# The schema-validation seam (step 3) is the load-bearing, runtime-independent
# part: the CMA API does not enforce structured output, so the harness does.
# The headless invocation (steps 2 & 4) is shown with Claude Code's print mode
# (`claude -p ... --allowedTools ...`); map it to your runtime if different.
# Nothing about steps 1 and 3 changes when you do.
#
# Usage:
#   deploy-managed-agent.sh <cookbook-dir> [--dry-run] [--config PATH ...]
#
#   <cookbook-dir>   e.g. managed-agent-cookbooks/deadline-watcher
#   --dry-run        run readers + validate, print the assembled orchestrator
#                    input, but DO NOT run the orchestrator (no external post).
#   --config PATH    a plugin config file to pass to the readers (repeatable).
#                    Defaults to the standard claude-for-tax config locations.
#
# Env:
#   CLAUDE_BIN       the CLI to invoke headless (default: "claude").
#   ALERT_CHANNEL    destination passed to the orchestrator (default: from env).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$REPO_ROOT/scripts"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
AS_OF="$(date +%F)"

die() { echo "deploy: $*" >&2; exit 1; }

# --- args ---------------------------------------------------------------------
COOKBOOK="${1:-}"; shift || true
[ -n "$COOKBOOK" ] || die "usage: deploy-managed-agent.sh <cookbook-dir> [--dry-run] [--config PATH ...]"
[ -d "$COOKBOOK" ] || die "cookbook dir not found: $COOKBOOK"

DRY_RUN=0
CONFIGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --config)  shift; [ $# -gt 0 ] || die "--config needs a path"; CONFIGS+=("$1"); shift ;;
    *) die "unknown arg: $1" ;;
  esac
done

if [ "${#CONFIGS[@]}" -eq 0 ]; then
  CFG_BASE="$HOME/.claude/plugins/config/claude-for-tax"
  for p in corporate-tax/CLAUDE.md personal-tax/CLAUDE.md employment-tax/CLAUDE.md indirect-tax/CLAUDE.md; do
    [ -f "$CFG_BASE/$p" ] && CONFIGS+=("$CFG_BASE/$p")
  done
fi

ORCH="$COOKBOOK/orchestrator.yaml"
[ -f "$ORCH" ] || die "no orchestrator.yaml in $COOKBOOK"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# --- helpers ------------------------------------------------------------------
# Pull a top-level field out of an agent YAML as JSON (PyYAML; same dep as validate.py).
yaml_field_json() { # <yaml> <field>
  python3 - "$1" "$2" <<'PY'
import json, sys, yaml
doc = yaml.safe_load(open(sys.argv[1]).read())
print(json.dumps(doc.get(sys.argv[2])))
PY
}
yaml_field_scalar() { # <yaml> <field>
  python3 - "$1" "$2" <<'PY'
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1]).read())
v = doc.get(sys.argv[2])
print("" if v is None else v if isinstance(v, str) else "")
PY
}
# Build a space-separated --allowedTools argument list from a YAML tools field.
tools_args() { # <yaml>
  python3 - "$1" <<'PY'
import sys, yaml
for t in (yaml.safe_load(open(sys.argv[1]).read()).get("tools") or []):
    print(t)
PY
}

# --- step 1: least-privilege lint (fail closed) -------------------------------
echo "deploy: [1/4] lint-tool-scope on $COOKBOOK"
python3 "$SCRIPTS/lint-tool-scope.py" "$COOKBOOK" || die "lint-tool-scope failed — refusing to deploy."

# --- step 2+3: run each reader headless, then schema-validate -----------------
VALIDATED=()  # files of validated reader JSON
if [ -d "$COOKBOOK/readers" ]; then
  for reader in "$COOKBOOK"/readers/*.yaml; do
    [ -e "$reader" ] || continue
    rname="$(basename "$reader" .yaml)"
    echo "deploy: [2/4] running reader '$rname' (read-only)"

    # Extract the inline output_schema to a temp .json for validate.py.
    schema="$WORK/$rname.schema.json"
    yaml_field_json "$reader" output_schema > "$schema"
    [ "$(cat "$schema")" != "null" ] || die "reader $rname has no output_schema"

    # Build the reader prompt: its instructions + the harness inputs + JSON-only directive.
    instr="$(yaml_field_scalar "$reader" instructions)"
    prompt="$instr

HARNESS INPUTS:
  as_of: $AS_OF
  config_paths: ${CONFIGS[*]:-<none configured>}

Read the config_paths above. Output ONLY the JSON object for your output_schema."

    # Constrain the headless run to exactly the leaf's declared tools.
    mapfile -t rtools < <(tools_args "$reader")
    out="$WORK/$rname.out.json"

    # Headless invocation (Claude Code print mode). Map to your runtime if different;
    # the --allowedTools allowlist is the run-time mirror of the linted scope.
    if ! "$CLAUDE_BIN" -p "$prompt" --allowedTools "${rtools[@]}" --output-format text > "$out" 2>"$WORK/$rname.err"; then
      cat "$WORK/$rname.err" >&2
      die "reader $rname failed to run"
    fi

    # The reader is instructed to emit JSON only; strip any stray fences defensively.
    python3 - "$out" <<'PY'
import re, sys
p = sys.argv[1]
t = open(p).read().strip()
t = re.sub(r'^```(?:json)?\s*|\s*```$', '', t, flags=re.MULTILINE).strip()
open(p, "w").write(t)
PY

    echo "deploy: [3/4] validating '$rname' output against its output_schema"
    python3 "$SCRIPTS/validate.py" "$out" "$schema" \
      || die "reader $rname output failed schema validation — dropped, not posted."
    VALIDATED+=("$out")
  done
fi

[ "${#VALIDATED[@]}" -gt 0 ] || die "no validated reader output — nothing to orchestrate."

# Assemble the validated reader payloads into the orchestrator input.
ASSEMBLED="$WORK/reader_output.json"
python3 - "$ASSEMBLED" "${VALIDATED[@]}" <<'PY'
import json, sys
out = sys.argv[1]
payloads = [json.load(open(p)) for p in sys.argv[2:]]
# Single reader → pass its object; multiple → an array under "readers".
json.dump(payloads[0] if len(payloads) == 1 else {"readers": payloads},
          open(out, "w"), indent=2)
PY

# --- step 4: orchestrator (posts) ---------------------------------------------
if [ "$DRY_RUN" -eq 1 ]; then
  echo "deploy: [4/4] --dry-run — assembled orchestrator input (NO post):"
  cat "$ASSEMBLED"
  echo "deploy: dry run complete; orchestrator not invoked."
  exit 0
fi

echo "deploy: [4/4] running orchestrator (read-only + single egress) → posting"
oinstr="$(yaml_field_scalar "$ORCH" instructions)"
oprompt="$oinstr

HARNESS INPUTS:
  as_of: $AS_OF
  alert_channel: ${ALERT_CHANNEL:-<set ALERT_CHANNEL or read from the plugin House style>}
  reader_output: $(cat "$ASSEMBLED")"

mapfile -t otools < <(tools_args "$ORCH")
"$CLAUDE_BIN" -p "$oprompt" --allowedTools "${otools[@]}" --output-format text \
  || die "orchestrator failed to run."

echo "deploy: done."

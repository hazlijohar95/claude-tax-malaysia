# scripts/

Install the Python dependencies once:

```bash
pip install -r scripts/requirements.txt
```

## Checks that run in CI

`.github/workflows/validate.yaml` runs these on every push and pull request.

| Script | What it does |
|---|---|
| `check-conventions.py` | Whitespace and final newlines, 2-space JSON, skill/agent frontmatter, `/plugin:skill` references that resolve to a real directory, `marketplace.json` matching each `plugin.json`. `--fix-whitespace` applies the whitespace fixes. |
| `check-guardrails.py` | Every plugin's `## Shared guardrails` carries all 12 canonical rules, and its verification-log rule points at its own config path. Pins the rule set without forcing identical prose. |
| `test-cookbooks.sh` | Hermetic structural test of the managed-agent cookbooks: runs `lint-tool-scope.py`, then checks each orchestrator and reader parses, declares its required fields, and carries a valid JSON Schema. No model needed. |
| `lint-tool-scope.py` | Least-privilege lint on the cookbook agent YAML: readers are limited to read tools, an orchestrator may add exactly one concrete egress, and no agent may carry `Write`/`Edit`/`Bash`/`WebFetch`/`WebSearch` or a wildcard MCP tool. Also invoked by `test-cookbooks.sh` and the deploy harness. |

## Run-time harness

| Script | What it does |
|---|---|
| `validate.py` | Validates one reader's JSON output against a schema. The deploy harness runs it between a reader and the orchestrator, because the runtime does not enforce structured output. |
| `deploy-managed-agent.sh` | Reference deploy harness: lint, run readers, validate each against its inline `output_schema`, run the orchestrator, post. Fails closed at each seam. Needs a headless CLI (`CLAUDE_BIN`, default `claude`); use `--dry-run` to stop before the post. |

## Reference only — not wired into anything

| Script | What it does |
|---|---|
| `orchestrate.py` | A worked example of the cross-agent handoff loop (closed-schema intents, target allowlist, data-frame wrapping, audit log) for when you outgrow the shipped cookbooks' single pinned egress. **Nothing in this repo imports or runs it**, and the shipped cookbooks deliberately use the simpler direct-egress model. Read it as documentation; replace it with your own workflow engine if you need the pattern. |

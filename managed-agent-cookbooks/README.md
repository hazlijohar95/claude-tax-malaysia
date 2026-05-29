# Managed-agent cookbooks

Headless, scheduled tax agents — built to run **unattended**, where no human is in
the loop to catch a mistake at run time. Two are shipped:

- **`deadline-watcher/`** — posts a weekly digest of upcoming filing/payment
  deadlines read from the installed plugins' deadline calendars (Form C, CP204,
  Form BE/B, PCB/CP39, EPF/SOCSO/EIS, …).
- **`sst-period-watcher/`** — posts an SST taxable-period and SST-02 reminder read
  from the `indirect-tax` profile.

They are the deployable counterparts of the in-plugin `deadline-watcher` agents.
The in-plugin agents assume a person is present; these assume no one is, and are
scoped accordingly.

## The shape: read-only orchestrator + schema-validated reader leaves

Each cookbook is a tiny pipeline, not one big agent:

```
reader leaf (read-only)  →  schema validation  →  orchestrator (read-only + 1 egress)  →  post
```

- **Reader leaves** (`readers/*.yaml`) do exactly one thing: read recorded config
  and return structured JSON. Their tools are a subset of `{Read, Glob, LS}` —
  nothing that writes, runs code, or reaches the network. Each declares an inline
  `output_schema`.
- **Schema validation** happens *between* the leaf and the orchestrator. The CMA
  API does not enforce structured output, so the harness runs `scripts/validate.py`
  on each leaf's JSON against its `output_schema`. **A leaf output that fails the
  schema is dropped, never posted.**
- **The orchestrator** (`orchestrator.yaml`) is read-only plus exactly one concrete
  egress tool (the Slack send — not a wildcard). It never reads source documents
  itself; it consumes the validated leaf JSON, ranks and formats it, and posts once.

### Why this shape

For a headless agent, **the tool scope is the security boundary** — there is no
human to approve an action. So:

- the agent that touches the most (reads many configs) can do the least (read only);
- the agent with an external action (the post) sees only clean, schema-shaped data,
  never raw config text that could carry an injection;
- the one egress is a pinned tool, so a compromised prompt cannot exfiltrate via an
  arbitrary URL or a wildcard MCP call.

`scripts/lint-tool-scope.py` enforces these invariants and the deploy harness fails
closed if they're violated.

## The verify-don't-assume posture carries over

These watchers **never assert a statutory date as fact.** They read the team's
*recorded* calendar rules, compute dates where the config gives enough to do so
(and return `null` / `"unknown"` where it doesn't — never a guess), and flag every
date for verification against the current filing programme / RMCD guidance. A
watcher that silently skips an unconfigured plugin says so, rather than posting a
false all-clear.

## Running one

```bash
# lint + run readers + validate + assemble, but DO NOT post (safe to run anywhere):
scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher --dry-run

# live (posts to ALERT_CHANNEL via the orchestrator's Slack send tool):
ALERT_CHANNEL="#tax-deadlines" scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher
```

Schedule it with cron (weekly for deadlines; around each period end for SST):

```cron
0 8 * * 1  cd /path/to/claude-for-tax && ALERT_CHANNEL="#tax-deadlines" scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher >> ~/tax-watcher.log 2>&1
```

`CLAUDE_BIN` overrides the CLI used for the headless runs. The headless invocation
is shown with Claude Code's print mode (`claude -p … --allowedTools …`); map it to
your runtime if different — the **lint** and **schema-validation** seams don't change
when you do.

## Files

```
managed-agent-cookbooks/
  deadline-watcher/
    orchestrator.yaml            # read-only + Slack send; consumes validated reader JSON
    readers/deadline-reader.yaml # read-only; reads ## Deadline calendar sections; inline output_schema
    steering-examples.json       # example invocations (scheduled sweep, single-plugin, red-only, dry-run)
  sst-period-watcher/
    orchestrator.yaml
    readers/sst-period-reader.yaml
    steering-examples.json
scripts/
  lint-tool-scope.py             # least-privilege linter (fail closed)
  test-cookbooks.sh              # hermetic CI: lint + structural well-formedness (no model needed)
  deploy-managed-agent.sh        # lint → run readers → validate.py → orchestrator → post
  validate.py                    # schema validation between reader and orchestrator
  orchestrate.py                 # REFERENCE cross-agent handoff loop (for when you wire agents together)
```

`steering-examples.json` documents how each cookbook is invoked — a scheduled
sweep, a single-plugin run, a red-only near-term check, and a dry run.

`scripts/orchestrate.py` is a **reference only**. The shipped cookbooks post
directly via one pinned Slack egress (the smaller surface for a single digest).
`orchestrate.py` is the pattern for the step up — when one agent's output must
steer another — with closed-schema intents, a target allowlist, data-frame
wrapping, and an audit log so untrusted document text can never become a steering
prompt. Use it when you outgrow direct egress; keep direct egress while a cookbook
is a single post.

### Testing the cookbooks

```bash
# Hermetic — runs in CI, no model or config needed:
scripts/test-cookbooks.sh    # least-privilege lint + every orchestrator/reader well-formed, schemas valid
```

## What these cookbooks do NOT do

- File, pay, or submit anything — they read and they post a reminder.
- Assert a statutory deadline as fact — they compute from recorded rules and flag for verification.
- Decide anything — they surface windows; a person acts. (Whether to revise a CP204
  estimate, release a leaver's final pay, or submit the SST-02 is never automated.)
- Guarantee delivery — if a plugin is unconfigured, the post says so rather than
  going quiet.

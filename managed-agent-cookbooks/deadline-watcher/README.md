# deadline-watcher (managed agent)

A headless weekly digest of upcoming tax filing and payment deadlines, read from
the deadline calendars the installed plugins already maintain — no separate
calendar to keep in sync.

## Pipeline

```
deadline-reader (Read, Glob)            →  validate.py  →  deadline-watcher-orchestrator (Read, Slack send)  →  weekly post
  reads ## Deadline calendar sections      against the       ranks red/amber/green, applies the currency
  of corporate-tax / personal-tax /        reader's          caution, names the "not checked" configs, posts once
  employment-tax configs                   output_schema
```

- **`readers/deadline-reader.yaml`** — read-only leaf. For each plugin config it's
  given, it extracts the recorded obligations (rule, basis, penalty) *as written*,
  computes a due date only when the config supplies enough to do so (else `null` /
  `urgency: "unknown"`), and flags every one for verification. Configs that are
  missing or still `[PLACEHOLDER]` go into `unread_or_unconfigured`.
- **`orchestrator.yaml`** — read-only + a single Slack send. Consumes the validated
  obligations, ranks them (🔴 ≤14d / 🟠 15–44d / 🟡 45–90d), leads with the currency
  caution, lists anything not checked, and posts. Red items post regardless of the
  rest of the week; an empty 90-day horizon posts a short all-clear.

## Run

```bash
# dry run (no post):
scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher --dry-run

# live:
ALERT_CHANNEL="#tax-deadlines" scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher

# point it at specific configs instead of the defaults:
scripts/deploy-managed-agent.sh managed-agent-cookbooks/deadline-watcher \
  --config ~/.claude/plugins/config/claude-for-tax/corporate-tax/CLAUDE.md \
  --config ~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md
```

By default the harness passes the corporate-tax, personal-tax, employment-tax, and
indirect-tax configs that exist on the machine. Schedule weekly (e.g. Monday 08:00)
via cron — see the top-level `managed-agent-cookbooks/README.md`.

## Posture

The watcher does not assert a deadline as fact. It surfaces the team's recorded
rules for a human to confirm against the current LHDN filing programme, and it never
guesses a date the config doesn't support. It posts a reminder; it never files,
pays, or revises anything.

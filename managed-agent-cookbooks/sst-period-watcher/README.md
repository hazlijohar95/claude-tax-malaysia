# sst-period-watcher (managed agent)

A headless reminder of the SST taxable period and the upcoming SST-02 return and
payment, read from the `indirect-tax` profile.

## Pipeline

```
sst-period-reader (Read, Glob)         →  validate.py  →  sst-period-watcher-orchestrator (Read, Slack send)  →  reminder post
  reads the indirect-tax config:           against the      states the period + SST-02 due with the currency
  ## Registration profile (taxable         reader's         caution, or a "not configured" note — never a false
  period) + ## SST return calendar         output_schema    all-clear; posts once
```

- **`readers/sst-period-reader.yaml`** — read-only leaf. Reads the recorded
  registration status and taxable period (monthly / bi-monthly) and the SST-02 due
  rule *as written*. Derives the current period and due date only when the config
  supplies enough (else `computable: false` / `null` / `urgency: "unknown"`). Flags
  the SST-02 date for verification against the current Act and RMCD guidance.
- **`orchestrator.yaml`** — read-only + a single Slack send. If indirect-tax isn't
  configured or the period can't be determined, it posts a short "set it up" note
  rather than a false all-clear. Otherwise it posts the period and the SST-02
  reminder, red (≤14d) regardless of schedule.

## Run

```bash
# dry run (no post):
scripts/deploy-managed-agent.sh managed-agent-cookbooks/sst-period-watcher --dry-run

# live:
ALERT_CHANNEL="#sst" scripts/deploy-managed-agent.sh managed-agent-cookbooks/sst-period-watcher
```

The reader uses the indirect-tax config among the harness defaults; you can pin it
explicitly with `--config ~/.claude/plugins/config/claude-for-tax/indirect-tax/CLAUDE.md`.
Because SST periods are typically bi-monthly, schedule this to run in the days
around each period end rather than weekly — see the top-level README for cron.

## Posture

SST rates, taxable periods, and the return programme change by gazette order, so the
watcher treats the SST-02 date as a recorded rule to confirm, never settled statute.
It reminds; it never submits the SST-02 or pays.

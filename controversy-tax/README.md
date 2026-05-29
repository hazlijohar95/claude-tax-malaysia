# Tax Controversy

Manage tax audits, assessments, and disputes — matter by matter — on the `claude-for-tax` robustness spine. Malaysia-first (ITA 1967, LHDN audit and appeal procedure, the SCIT). Every fact traced to a source document; every deadline treated as a one-way door and flagged against the limitation period.

> **Every output is a draft for review by a qualified tax adviser or tax litigator.** It is not a filing, an objection, or a settlement you can act on without checking. The objection window is unforgiving — a lapsed deadline makes an assessment final — so confirm every date against the notice and current procedure. Anything recalled from training is `[model knowledge — verify]`.

## Setup first

```
/plugin install controversy-tax@claude-for-tax
# restart Claude Code
/controversy-tax:cold-start-interview        # add --new-matter to open your first matter straight after
```

The interview learns your disputing body, posture, reporting standard, and deadline calendar, and writes them to `~/.claude/plugins/config/claude-for-tax/controversy-tax/CLAUDE.md`. Matter workspaces are on by default — each dispute is a matter.

## Commands

| Command | What it does |
|---|---|
| `/controversy-tax:cold-start-interview` | Learn your practice and write the profile (run first) |
| `/controversy-tax:matter-intake` | Open a matter — **deadline captured first**, facts sourced, assessor's basis pinned |
| `/controversy-tax:matter-briefing` | Deep brief on one matter, ready for a call |
| `/controversy-tax:matter-update` | Append a dated event; update deadlines and exposure |
| `/controversy-tax:portfolio-status` | Rollup — stage, exposure, ranked deadlines, stale matters |
| `/controversy-tax:audit-response` | Answer an LHDN query from sourced docs without over-conceding |
| `/controversy-tax:assessment-review` | Pin the basis, test the time bar, recompute adjustments, assess defensibility |
| `/controversy-tax:objection-appeal` | Draft an s.99 objection or SCIT Form Q — with a hard deadline gate |
| `/controversy-tax:penalty-analysis` | Penalty exposure and remission / reasonable-cause arguments |
| `/controversy-tax:customize` | Tune the profile without a full re-interview |
| `/controversy-tax:matter-workspace` | Manage matters |
| scheduled | `deadline-watcher` — daily sweep for objection/appeal/response deadlines |

## The disciplines this plugin enforces

1. **Deadline first, and never asserted.** Intake captures the controlling deadline before anything else; the objection/appeal drafter won't finalise a submission until the deadline is confirmed; the watcher sweeps daily. Every date is flagged for verification against the notice and current procedure — never stated from memory.
2. **Facts trace to source.** Every fact in a response, objection, or memo cites the document it came from; exposure ties to the assessment. A submission built on an unsourced fact is how a matter is lost on a point that wasn't true.
3. **Surface the call, don't make it.** Concede/proceed and settle/litigate are flagged `[review]` for the person with settlement authority — the skill states the standard each position meets and the downside of each path.

## What this plugin does NOT do

- File objections/appeals or send responses — drafting and review only; filing is the user's gated action.
- Assert deadlines, time-bar periods, penalty rates, or procedure as settled fact — it flags every one for verification.
- Decide whether to concede, settle, or proceed.
- Create privilege it can't (tax-adviser working papers are not generally privileged in Malaysia — see the practice profile).

## Connectors

`.mcp.json`: Google Drive (matter documents), Slack (deadline alerts). Optional — skills fall back to paste/upload and say so.

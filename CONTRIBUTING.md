# Contributing to Claude for Tax

Notes for anyone writing or editing a plugin in this repo. Keep this short — the
design principles that matter most for the quality of the output, not a style
guide.

## Before your first PR

Sign the CLA. The first time you open a pull request, the CLA Assistant bot will
comment with a link to the [CLA](CLA.md) and ask you to confirm. Reply with
`I have read the CLA Document and I hereby sign the CLA` and the check will pass.
You only need to do this once.

## The one rule that governs everything

Before anything else, read `CLAUDE.md` → **"Truth, always verify, never assume."**
This repo is tax. A confident wrong number or a fabricated statutory reference is
worse than a gap. Two invariants run through every skill and must survive every
edit:

1. **Every authority is `[model knowledge — verify]` by default** until it is
   retrieved from an LHDN/RMCD primary source or pasted by the user.
2. **Every figure traces to a source and ties to the computation** — a source
   reference on each amount, CHECK cells that reconcile to the TB/accounts/return.

If an edit weakens either invariant, it does not merge.

## Design principle: SKILL.md encodes the right behavior; CLAUDE.md guardrails are the net

Every plugin in this repo ships with two layers of instruction:

1. **`<plugin>/skills/<skill>/SKILL.md`** — what this specific skill does, step by
   step. The narrow, task-specific scaffold.
2. **`<plugin>/CLAUDE.md`** — the shared guardrails and the practice profile:
   "Scaffolding, not blinders," source-tag discipline, "verify user-stated tax
   facts," premise verification, the currency trigger, destination check,
   cross-skill severity floor, the pre-flight citation banner. The wide,
   plugin-level safety net.

**If a skill's correct output depends on a CLAUDE.md guardrail catching a mistake
the SKILL.md would have made, that's a design smell.** The SKILL.md should tell
the model what to do directly; the guardrails should catch what the SKILL.md
missed. Every time a guardrail has to rescue a skill, we're relying on the
guardrail firing consistently — and on a bad run, a weaker model, a terser
prompt, or a future editor who reads only the skill text, the rescue doesn't
happen.

**Rule of thumb: if a QA test passes only because a guardrail fired, add the
behavior to the SKILL.md directly.** The guardrail stays (belt and suspenders),
but the skill now carries the knowledge it needs on its own.

Examples of this rule in practice (tax):

- An SME-rate question should not land on the right answer only because
  "Scaffolding, not blinders" let the model reconsider. The computation skill
  should branch on **both** SME conditions itself — paid-up capital ≤ the
  threshold **and** gross business income ≤ the threshold, with the
  related-company test — and flag the year-of-assessment for verification, not
  hope the model remembers the second limb.
- A filing deadline that falls on a weekend or a public holiday should not get
  rolled correctly only because the user thought to ask. The deadline skill and
  the deadline-calendar schema should carry the business-day roll-forward and the
  "confirm against the current LHDN filing programme" tag themselves.
- A deferred-tax figure should not get the rate right only because the model
  happens to remember a rate change. The provision skill should force the
  question into every proof: *does this temporary difference reverse in a year the
  rate differs?* — and tie the closing deferred-tax balance to the prior-year
  proof.

## A few concrete things that follow

- **Put the doctrine in the skill.** If a computation skill covers capital
  allowances, cover balancing charges and the cap at allowances given. If it
  covers reliefs, list the actual reliefs and their conditions — not a pointer to
  "and also consider." The actual checklist.
- **Attach provenance tags to numbers, not to paragraphs.** `[model knowledge —
  verify against Schedule 3 for YA 2024]` next to the rate; `[verify against the
  current LHDN filing programme]` on the deadline line. Tags on surrounding prose
  get lost; tags on the load-bearing digit do not.
- **Make the decline pathway a scaffold, not an escape hatch.** Where the right
  answer is "I won't assert this," bake it into the skill as a hard gate: the
  "three values, not two" rule (supplement-with-a-flag / say-nothing-and-stop /
  flag-but-don't-use) is the pattern. Stated plainly, owned by the skill.
- **Write the gate header so the gate is default-on.** If there is an exemption,
  phrase the heading as the gate and narrow the exemption in a sub-bullet, not the
  other way around. A load-bearing parenthetical is a bug waiting to be
  reintroduced by the next edit.

## Workflow notes

- **Read the plugin's `CLAUDE.md` before editing any skill in that plugin.** The
  practice profile, the integrations table, the shared guardrails, the reporting
  standard, and the decision-posture statement all shape what the skill should
  say and omit.
- **Keep the `## Shared guardrails` block byte-identical across plugins** (only
  the config path swaps). When you change a guardrail, change it in every plugin.
- **Bump the plugin version on a material change.** Patch bumps for behavior
  additions; minor bumps for new skills or new required inputs.
- **Run the validators.** `claude plugin validate` on the marketplace and each
  plugin, then `scripts/lint-tool-scope.py` and `scripts/test-cookbooks.sh` for
  the managed-agent cookbooks. They check the structural and least-privilege
  invariants the loader and the deploy harness depend on.
- **Default jurisdiction is Malaysia.** New skills assume the Malaysian framework
  (ITA 1967, Sales Tax Act 2018, Service Tax Act 2018, MFRS, LHDN/RMCD practice)
  and fire the `## Jurisdiction recognition` guardrail for everything else. Don't
  silently apply Malaysian rules to non-Malaysian facts.
- **Do not remove the shared guardrails from CLAUDE.md.** The net stays. The goal
  is a skill that doesn't need the net, not a plugin without one.

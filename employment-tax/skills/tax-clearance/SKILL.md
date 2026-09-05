---
name: tax-clearance
description: >
  Handle tax clearance (SPC) and the employer notification obligations when an employee leaves —
  CP22A on cessation, CP21 when an employee leaves Malaysia — and the employer's duty to withhold
  monies pending the clearance letter, against the team's conventions in
  `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`. The withholding obligation is
  the load-bearing point: releasing final pay before clearance makes the employer liable for the
  amount. Every date and threshold is flagged for verification. Use for "tax clearance for a
  leaver", "CP21 for an employee leaving Malaysia", "CP22A cessation", "do we withhold the final
  salary".
argument-hint: "[employee] [leaving date / departure date, final pay components, employment facts]"
license: Apache-2.0
compatibility: >-
  Designed for Claude Code (or a client that supports the Agent Skills spec). Reads a practice profile written by this plugin's cold-start interview; without one it runs from generic Malaysian tax defaults and tags output as provisional.
metadata:
  author: Hazli Johar
  version: "1.0.0"
  jurisdiction: Malaysia
---

# Tax Clearance (SPC) & Cessation Notifications

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip — skills use practice-level context. If enabled, load the active employer's `matter.md` and write outputs there.

## Purpose

When an employee ceases or leaves Malaysia, the employer has two duties that carry direct liability: **notify** (CP22A on cessation; CP21 when leaving Malaysia) within the statutory window, and **withhold** the employee's final monies until LHDN issues the clearance (SPC). Release the final pay early and the employer can be made liable for the tax that should have been covered. This skill maps the obligations, the timeline, and the amount to withhold.

This skill does not assert the statutory windows or thresholds from memory — they are `[verify against current LHDN guidance]`.

## Precondition: load the profile

**Read `~/.claude/plugins/config/claude-for-tax/employment-tax/CLAUDE.md`** for the team's clearance convention and the deadline calendar. If missing or placeholder, redirect to `/employment-tax:cold-start-interview`, or proceed `[PROVISIONAL]` against the generic obligations with every date/threshold flagged.

## Inputs required

1. **The employment facts** — cessation date or expected departure date, reason (resignation, retirement, end of contract, leaving Malaysia), citizenship/residency, and whether the employee is expected to be chargeable to tax.
2. **The final-pay components** — final salary, bonus, leave encashment, gratuity, any ESOS crystallising on departure — the monies potentially subject to withholding.
3. **The notification status** — whether CP22A / CP21 has been filed and when.

## Workflow

### Step 1 — Which notification, and the window

- **Leaving Malaysia** (expected to leave for more than the threshold period, with no intention to return) → **CP21**, filed **not less than [30] days** before expected departure `[verify]`, **and the withholding duty applies**.
- **Cessation of employment** (private sector, employee remaining in Malaysia / chargeable) → **CP22A**, filed **not less than [30] days** before cessation (or as the rules require) `[verify]`.
- **Death** → the applicable notification `[verify]`.

State which applies, the window, and whether it's already at risk given today's date. A missed notification is a penalty exposure (s.83 `[verify]`).

### Step 2 — The withholding obligation (the load-bearing step)

Where the obligation applies (notably CP21 / leaving Malaysia, and cessation pending clearance), the employer must **withhold the employee's final monies** until the clearance letter (SPC) is received `[verify the scope and trigger]`. State plainly:

> Do not release the final pay (salary, bonus, leave encashment, gratuity, crystallising ESOS) until LHDN issues clearance. If the employer releases these monies before clearance, the employer can be held liable for the employee's tax up to the amount released `[verify against current LHDN guidance]`.

Identify the specific monies in scope from the final-pay components, and quantify the amount to withhold. If the employer has already committed or released funds, flag it 🔴 as a live exposure and state what to do now.

### Step 3 — Final-pay tax treatment feeding clearance

The final-pay components have their own treatment that affects the clearance position: gratuity / compensation-for-loss-of-office exemptions, leave encashment, and any ESOS perquisite crystallising on departure (hand valuation to `/employment-tax:bik-perquisites`). Set out the taxable picture LHDN will assess against, flagging each treatment `[review]`/`[verify]`. This is what the withheld amount is covering.

### Step 4 — The clearance timeline and release

Lay out the sequence: notify (CP21/CP22A) → withhold → LHDN reviews → SPC issued (stating the amount due, if any) → employer settles from withheld monies → release the balance to the employee. State the documents to submit and the realistic timing caution (clearance is not instant; plan the departure around it).

### Step 5 — Assemble

Prepend the work-product header. Lead with the reviewer note (Sources / Read / Flagged / Currency / Before relying), and put the withholding instruction and any live exposure at the top of the bottom line — it is the thing that must not be missed.

## Output format

```
[WORK-PRODUCT HEADER — per profile ## Outputs]

# Tax Clearance: [Employee] — [cessation / departure date]

## Bottom line
Notification: [CP21 / CP22A] due [date] `[verify]` — [filed / NOT filed].
WITHHOLD RM [x] (final pay in scope) until SPC issued. [Live exposure if already released: RM [y] 🔴].

## Notification obligation
[the Step 1 determination — which form, window, status]

## Withholding obligation
[the Step 2 instruction — what to withhold, why, the liability if released early]

## Final-pay tax picture
[the Step 3 treatment of each component, flagged]

## Clearance timeline
[the Step 4 sequence and documents]
```

## Quality checks before delivering

- [ ] Correct notification identified (CP21 vs CP22A) with its window `[verify]`
- [ ] Withholding obligation stated plainly with the amount and the early-release liability
- [ ] Any already-released funds flagged 🔴 as a live exposure
- [ ] Final-pay components' tax treatment set out and flagged
- [ ] Clearance timeline and documents listed; timing caution given

## What this skill does NOT do

- File CP21 / CP22A or obtain the SPC (those are the user's actions) — it maps the obligation and the withholding.
- Assert the statutory windows or withholding scope as settled fact — it flags them for verification.
- Value the final-pay benefits in detail (run `/employment-tax:bik-perquisites`).

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — offer to draft the withholding/communication note, value the final-pay benefits, or add the notification to the deadline tracker.

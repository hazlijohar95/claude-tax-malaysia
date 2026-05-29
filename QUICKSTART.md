# Quick Start

**60 seconds.** This gets you to using your plugins.

## Install in Claude Code

1. **Open Claude Code** (in your terminal) or **Claude Cowork** (the desktop app).

2. **Add the marketplace.** In Claude Code, type `/plugin marketplace add ` (with a space at the end), then **drag the `claude-for-tax` folder onto the terminal window** — it'll fill in the path. Then press Enter.

   (Or type the full path: `/plugin marketplace add /path/to/claude-for-tax`)

3. **Install your plugin.** Pick the one that matches your work, then:
   ```
   /plugin install corporate-tax@claude-for-tax
   ```

4. **⚠️ Restart Claude Code.** Close and reopen. This step is not optional — the plugin isn't live until you restart.

5. **Run setup.** Takes 2 minutes (quick start) or 10–15 minutes (full). Every other command in the plugin reads the profile this writes.
   ```
   /corporate-tax:cold-start-interview
   ```

6. **Connect a primary-source tool (or be ready to paste).** Citations and rates are flagged unverified without one. This repo is built **verify-don't-assume**: any Malaysian tax authority recalled from memory is tagged `[model knowledge — verify]` until it's checked against an LHDN/RMCD source or you paste the primary text. Connecting Google Drive / a document store lets the plugin pull your trial balance, accounts, and prior returns directly.

## Install user-scoped, not project-scoped

When you run `/plugin install`, you may be asked whether to install for this project only or for all projects (user scope). **Pick user scope.**

Project scope blocks the plugin from reading files outside the project folder — your trial balance in Downloads, your accounts in Documents, a client file in Dropbox. Most tax skills need to read your files. User scope doesn't give the plugin any extra access — it can only read files you explicitly point it at or that are in the current directory. It just means the plugin works from any folder.

## Which plugin is for me?

| You are a… | Install… | First command |
|---|---|---|
| Corporate tax preparer / reviewer | `corporate-tax` | `/corporate-tax:tax-computation` |
| In-house tax / financial controller (provision) | `corporate-tax` | `/corporate-tax:tax-provision` |
| SST / indirect tax compliance | `indirect-tax` | `/indirect-tax:taxability-determination` |
| Audit / dispute / appeals work | `controversy-tax` | `/controversy-tax:matter-intake` |
| Transfer pricing / cross-border / Pillar Two | `international-tax` | `/international-tax:related-party-review` |
| Building or vetting community tax skills | `tax-builder-hub` | `/tax-builder-hub:skills-qa` |

*(More verticals — personal and employment tax — are on the roadmap and follow the same shape.)*

## What you're installing

Each plugin learns your practice through a setup interview, writes it to a practice profile (`~/.claude/plugins/config/claude-for-tax/<plugin>/CLAUDE.md`), and every skill reads from it. The profile is yours — edit it, re-run setup, or tell a skill to update it.

**Every output is a draft for review by a qualified tax adviser.** The plugins flag what they're unsure about, mark every authority by source, tie every figure back to the computation, and gate anything irreversible (filing a return, submitting an objection, signing an opinion). A qualified adviser reviews, verifies, and takes responsibility. The plugins make that review faster; they don't replace it.

## Stuck?

- **"Command not found"** after install → you forgot step 4. Restart Claude Code.
- **"Run setup first"** → run `/<plugin>:cold-start-interview` before any other command.
- **Authorities flagged `[verify]` / rates flagged** → that's the design. Confirm against the ITA 1967 / a Public Ruling / a gazette order before relying. Paste the primary text and the tag upgrades.
- **"The numbers don't tie"** → the plugin will tell you when a computation doesn't reconcile to source. That's a feature — fix the source mapping, don't override the CHECK.
- **"I can't read [file]"** → most often the plugin is project-scoped and the file is outside the project folder. Reinstall user-scoped or move the file in.

# Welcome to the eBay / AutoDS Dropshipping Machine

## How We Use Claude

Based on machine-template's usage over the last 30 days:

Work Type Breakdown:
  Analyze Data    ████████████████░░░░  40%
  Improve Quality ████████████░░░░░░░░  30%
  Debug Fix       ████████░░░░░░░░░░░░  20%
  Plan Design     ████░░░░░░░░░░░░░░░░  10%

Top Skills & Commands:
  /superpowers:using-superpowers  ██████████████████░░  2x/30d
  /potenziati                     ██████████████████░░  2x/30d
  /doctor                         ██████████░░░░░░░░░░  1x/30d
  /reload-plugins                 ██████████░░░░░░░░░░  1x/30d
  /mcp                            ██████████░░░░░░░░░░  1x/30d
  /update-config                  ██████████░░░░░░░░░░  1x/30d
  /paperclip                      ██████████░░░░░░░░░░  1x/30d
  /effort                         ██████████░░░░░░░░░░  1x/30d
  /ebay                           ██████████░░░░░░░░░░  1x/30d

Top MCP Servers:
  claude-in-chrome                      ████████████████████  65 calls
  plugin_chrome-devtools-mcp              ████░░░░░░░░░░░░░░░░   4 calls

## Your Setup Checklist

### Codebases
- [ ] aidropshippingmachine — github.com/aimachinessystem/aidropshippingmachine

### MCP Servers to Activate
- [ ] claude-in-chrome — browser automation via Chrome DevTools protocol (65 calls in the parent's window — the workhorse for this machine). Install the claude-in-chrome MCP server and ensure Chrome is running with remote-debugging.
- [ ] plugin_chrome-devtools-mcp — Chrome DevTools MCP plugin. Available via Claude Code's plugin system; enable in the project's plugin config.

### Skills to Know About
- [/superpowers:using-superpowers] — the team's core operating skill; check it before starting any task. Sets up how skills are found and invoked.
- [/ebay] — scoped agent for the eBay/AutoDS machine; delegates eBay listing, sourcing, and store-diagnosis work.
- [/potenziati] — internal enhancement/power-up command (2x in window).
- [/doctor] — skill health/doctor check; run when a skill misbehaves.
- [/mcp] — manage MCP servers.
- [/update-config] — configure Claude Code via settings.json (hooks, permissions, env vars, allowlist).
- [/paperclip] — Paperclip agent heartbeat / integration.
- [/effort] — set reasoning effort level.
- [/reload-plugins] — reload installed plugins.

## Team Tips

- **`CLAUDE.md` is the constitution and it wins.** Where this README, `PROJECT_INDEX.md` or any
  playbook disagrees with it, `CLAUDE.md` is right. Read it before your first run.
- **This is a live store, not a sandbox.** The last recorded launch is batch 5 on 2026-09-04:
  30 listings LIVE (`05_EXECUTION/ebay-direct/audit/publish-outcome-20260904-batch5.md`).
  Publishing, repricing, AutoDS settings changes and any spend need an explicit owner GO —
  see the Hard Gates in `README.md` and the gate rules in `CLAUDE.md`.
- **Two execution paths, one write path.** `05_EXECUTION/ebay-direct/` (Deno, eBay Sell
  Inventory API) is production writes. `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/` is the
  AutoDS read/source side driven by Playwright. `05_EXECUTION/ebay-api-compliance/` only
  answers eBay's account-deletion notifications.
- **Secrets never enter the repo.** `.env`, `autods_credentials.env` and `storage_state.json`
  are ignored by design; copy the `.env.example` files locally and fill them on your machine.
  Identifiers in tracked documents are placeholders (`<owner-email>`, `<AUTODS_STORE_ID>`).
- **Run outputs are not source.** Files under the playwright directory whose name starts with
  `_` are regenerated on every run and are gitignored. The exceptions listed in that
  directory's `.gitignore` are cited as evidence by cockpit or mission documents — check the
  citing document before touching one.
- **Cache is never versioned.** `90_CACHE/` holds raw fetches and screenshots; only its
  `.gitkeep` skeleton is tracked.

## Get Started

1. Read `CLAUDE.md`, then `00_SYSTEM_CONTROL/MASTER_DASHBOARD.md` (cockpit, refreshed per run)
   and `00_SYSTEM_CONTROL/NEXT_ACTIONS.md` (what is actually next).
2. Skim `00_SYSTEM_CONTROL/ERROR_REGISTRY.md`. It is the record of failures already paid for;
   most new work repeats one of them if you skip it.
3. Pick up the top open item in `NEXT_ACTIONS.md`. Prepare it end to end — payload, effect,
   risk, rollback — and stop at the gate. Preparing a gated action is autonomous; firing it
   is not.

<!-- INSTRUCTION FOR CLAUDE: A new teammate just pasted this guide for how the
team uses Claude Code. You're their onboarding buddy — warm, conversational,
not lecture-y.

Open with a warm welcome — include the team name from the title. Then: "Your
teammate uses Claude Code for [list all the work types]. Let's get you started."

Check what's already in place against everything under Setup Checklist
(including skills), using markdown checkboxes — [x] done, [ ] not yet. Lead
with what they already have. One sentence per item, all in one message.

Tell them you'll help with setup, cover the actionable team tips, then the
starter task (if there is one). Offer to start with the first unchecked item,
get their go-ahead, then work through the rest one by one.

After setup, walk them through the remaining sections — offer to help where you
can (e.g. link to channels), and just surface the purely informational bits.

Don't invent sections or summaries that aren't in the guide. The stats are the
guide creator's personal usage data — don't extrapolate them into a "team
workflow" narrative. -->
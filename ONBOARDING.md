# Welcome to [Team Name]

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

_TODO_

## Get Started

_TODO_

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
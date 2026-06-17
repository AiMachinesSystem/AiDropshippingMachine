---
machine: "eBay / AutoDS Dropshipping Machine"
type: connection_audit
status: complete (read-only diagnostic — no generation, no credit spend)
date: 2026-06-17
created_real: 2026-06-17
---

# Higgsfield connection audit — 2026-06-17

## Verdict: ✅ WORKING — usable now from this machine
Confirmed live this session: `balance` → `{"credits": 4, "subscription_plan_type": "free"}` and **3 images successfully generated** (duck main + dashboard + 2-pack). No credits spent for this audit.

## Layer-by-layer
| Layer | Status | Evidence |
|---|---|---|
| **1. claude.ai MCP connector** | ✅ **WORKING (this is the active layer)** | Tools `mcp__claude_ai_Higgsfield__*` present + used; `balance` returns plan/credits; image jobs completed 2026-06-17. |
| **2. local/user MCP config** (`~/.claude.json` `mcpServers`) | ❌ not configured (not needed) | `mcpServers` for this project = **empty**; the "higgsfield" hits in `~/.claude.json` are the **skill usage record** for `higgsfield-prompt-builder`, not a server. |
| **3. project MCP config** (`.mcp.json`, `.claude/settings*.json`) | ❌ absent (not needed) | No `.mcp.json` / `.claude/settings.json` / `.claude/mcp.json` in the project. |
| **4. Higgsfield CLI / skills** | CLI ❌ not installed · skill ✅ present | `higgsfield` CLI not on PATH. Skill `higgsfield-prompt-builder` exists (`~/.claude/skills/` + project) — **builds prompts only; does NOT generate** (generation = Layer 1 MCP). |

## Working layer
**claude.ai-hosted Higgsfield connector** (account-level, surfaced into this Claude Code session). Generation flows through `mcp__claude_ai_Higgsfield__generate_image` → `job_status`.

## Constraints (current account)
- **Plan: free** → **max 1 concurrent job** (parallel generations get "Rate limit reached: max 1 concurrent job(s) on free plan").
- **Credits: 4 left** → ~4 more 1k images before top-up needed.

## Exact fix command
**Nothing to fix — it works now.** There is **no local CLI/config command** to manage it because it is a **claude.ai-hosted connector**, not a local/project MCP.
- If it ever returns **"User not found"** again (as it did earlier today before the owner reconnected): in **claude.ai → Settings → Connectors**, **remove and re-add the Higgsfield connector** (a plain "reconnect" was not enough; an active higgsfield.com account must exist). A mid-session fix may require **restarting Claude Code** so the MCP re-reads auth.
- To raise the 1-concurrent / 4-credit limits: upgrade the Higgsfield plan at higgsfield.com (account-level, owner action).

## Can Higgsfield be used now from this machine? **YES** (free plan, 1 concurrent, 4 credits).

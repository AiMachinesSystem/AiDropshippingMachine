---
machine: "eBay / AutoDS Dropshipping Machine"
type: owner_go_decision_pack
phase: "Core Intelligence Architect — Phase 3"
status: complete (awaiting owner decisions)
date: 2026-06-22
created_real: 2026-06-22
---

# OWNER GO DECISION PACK

> Everything that hit a boundary across Phases 1-3. Each: what, why GO needed, exact authorizing command.

## Strategic / firewall
| # | Decision | Why | Authorize with |
|---|---|---|---|
| D1 | ~~**R4 firewall:** keep or remove `10_OUTPUTS/n8n_digital_products/` + `PLAYBOOKS/.../03_shopify_daily_snapshot.json` (other-domain residue)~~ | digital-products/Shopify ≠ this eBay machine; risk of identity drift | **PARTIALLY CLOSED 2026-09-08** — owner GO given for the n8n folder: moved to `99_ARCHIVE/MISPLACED__n8n_digital_products/`. **STILL OPEN:** `00_SYSTEM_CONTROL/PLAYBOOKS/n8n_workflows/03_shopify_daily_snapshot.json` — no GO given, untouched. |
| D2 | **Lian Li winner:** de-brand title / delist / keep-as-is | brand in title = VeRO + arbitrage = suspension risk | `GO DE-BRAND LIANLI` / `GO DELIST LIANLI` / `KEEP` |

## Live business moves (GO-class)
| # | Action | Why | Authorize with |
|---|---|---|---|
| D3 | **Read pull** sell price + landed cost for 13 winners (M1) | compute exact reprice deltas | `GO READ PRICES` (read-only, GO-light) |
| D4 | **Apply reprice** of winners to market bands | live price change (Strategic if large) | `GO REPRICE` (I bring large shifts back) |
| D5 | **Re-source winners on AliExpress** | margin + survival | provide **AliExpress URLs** → import draft (GO) |
| D6 | **Kill remaining 12 dead+errored** (4 untickable + 8 no-id) | manual in UI | owner manual (tool can't) |
| D7 | **Fix fulfillment** (buyer account + wallet) + AutoDS subscription | unlock scaling (M5/M6) | owner action |

## Repo hygiene (reversible but at a boundary)
| # | Action | Why | Authorize with |
|---|---|---|---|
| D8 | **Checkpoint commit** of this session (no push) | reversible snapshot (R7) | `GO COMMIT CHECKPOINT` |
| D9 | Archive `_IMPORT/` duplicate + root `.zip` (R5) | stale duplicate | `GO ARCHIVE IMPORT` (deletion/move boundary) |
| D10 | Untrack 1 stray `.pyc` (R8) | repo hygiene | `GO UNTRACK PYC` |
| D11 | Git **history secret scan** (M4/G1) | fully close secret risk | `GO HISTORY SCAN` (read-only) |

## Recommended first 3 (impact × reversibility)
1. `GO READ PRICES` → I compute reprice deltas (internal, low risk).
2. **D1 / D2** firewall + Lian Li calls (cut risk + identity drift).
3. `GO COMMIT CHECKPOINT` (preserve this session's work safely).

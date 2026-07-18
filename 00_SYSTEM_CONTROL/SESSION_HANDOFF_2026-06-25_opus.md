---
machine: "eBay / AutoDS Dropshipping Machine"
type: session_handoff
date: 2026-06-25
created_real: 2026-06-25
from: Opus 4.8 session (architecture + profit-engine + Terapeak capability + publishing)
---

# SESSION HANDOFF — 2026-06-25 (for the next chat)

## What this session delivered (all files ON DISK, committed; latest commit ee11d7d)
- **Cracked the AutoDS marketplace READ API** (`POST gw.autods.com/marketplace/api/products/`: filters
  search_query / categories.autods_category_id.$id / rating / rating_count / price-between; auth = captured Bearer)
  **and the WRITE API** (`PUT /products/<store>/bulk`, bulk_changes). Sourcing tools:
  `marketplace_source(_band/_pool/_summer/_kitchen).py`, `rank_us_source.py`, `marketplace_filter_probe*.py`.
- **10-engine ARCHITECTURE** → `00_SYSTEM_CONTROL/ENGINE_ARCHITECTURE.md` (+ growth ladder, eBay-demand-first / NET-margin principle).
- **Skill `ebay-amazon-autods-profit-engine`** (`.claude/skills/…`) — codifies the owner Training OS (`docs/EBAY_AMAZON_AUTODS_PRODUCT_RESEARCH_TRAINING_OS.md`).
- **Reports** (`REPORTS/EBAY_AUTODS/` + `10_OUTPUTS/ANALYSIS_REPORTS/`): price-band study, `EBAY_AMAZON_AUTODS_PROFIT_TEST_001`, `PRODUCT_RESEARCH_RUN_001`.
- **Terapeak capability A — BUILT, NOT ACTIVATED** (`05_EXECUTION/…/integrations/ebay/`): `login_ebay_save_session.py`
  + `read_terapeak.py` (probe) + `ebay_demand_gate.py` (3→2→1 funnel, self-test PASS). Spec: `docs/superpowers/specs/2026-06-25-ebay-demand-terapeak-design.md`.
- **Orchestration/live tools:** `batch_publish.py` (E-012/E-013/E-002 safeguards + desc-retry), `reprice_apply.py`, `reprice_all_dryrun.py`, `delete_drafts_guarded.py`.
- **Published 24 listings LIVE this session** (each verified in /products). E-011 logged (see below).

## Key findings (data-backed — do not re-derive)
1. **E-012 import-fail wall = the #1 VOLUME bottleneck.** AutoDS Amazon import fails ~50–85% on MULTI-VARIANT
   products (sentinel `buy=$133.13 / stock=0`). Batches this session: 8/14 · 6/55 · 2/10 · 4/9.
2. **NET margins are thin (8–11%)** with the owner net-profit formula — BELOW the OS's 12–15% bar. Gross margin misleads.
3. **Clean generic single-config Amazon supply is DRAINED** after ~24 publishes across ~9,000 products scanned.
4. **#1 UNLOCK = eBay demand data (Terapeak / eBay API).** Capability A is built; needs the owner's eBay login to activate.
5. **Real structural fix = AliExpress sourcing** (single-config → no E-012; margin 12–15%). Design "B" NOT yet done.

## Open items / next actions (priority order)
1. **Activate Terapeak (A):** owner runs `login_ebay_save_session.py` (manual eBay login) → then finalize
   `read_terapeak.py` parser by probing the real Terapeak API (like the AutoDS crack) → wire into the profit-engine
   (replaces the `[eBay-DATA REQUIRED]` account-band proxy with real sold/sell-through).
2. **Design + build B — AliExpress pivot** (the volume + margin unlock). Brainstorming was the next step.
3. **Branded live titles — LEFT by owner (2026-06-25):** 5 flagged live (SHOW / CABIN / DisplayGifts / decorUhome /
   HQiJun) from other sessions' off-niche sourcing. Fixing needs a LIVE-title-edit tool (not built; cold-test like reprice).
4. **`gen_title` brand-strip gap:** leaks mid-title + some TitleCase brands (Camp Chef, Bull, iSPECLE, Starpack leaked
   earlier). Improve the BRAND list + add mid-title stripping before the next publish batch.

## ⚠️ State flags (read before acting)
- **Catalog is now 420 active listings** — grew from ~144 (this session) via OTHER parallel sessions (~+276). Web-led
  sourcing + de-branding happened elsewhere (`.remember/now.md` note "48 live web-led").
- **Git is tangled:** `git log -1` HEAD = `990a021` (this session's START commit), but this session's commits exist on
  another branch/state (latest `ee11d7d`). Working tree CLEAN, all files present. **Reconcile branches before committing** —
  don't force anything; the files are safe on disk.
- **Prices UNTOUCHED** (reprice halted after E-011: bulk `percentage_profit` SETS margin → price crash, cold-test caught
  it, listing restored). **No deletes** performed. Publishing = OWNER_GO only.

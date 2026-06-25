---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: playbook
status: active
created_real: "<first git commit>"
description: "Canonical Amazon->eBay publishing pipeline, profit-first selection, and the wall-avoid list. Distilled from the 2026-06-24 session (~27 listings published) + ERROR_REGISTRY E-008..E-014. Apply on every 'publish N products' run to maximize hit-rate and NET profit and minimize wasted imports."
---

# PUBLISHING PIPELINE v2 — Amazon US -> eBay (AutoDS), profit-first

> North Star = **NET profit** (see memory [[profit-objective-function]]). Select for **eBay demand + real NET margin**, not scrape-ability or theoretical AutoDS markup. Publishing is GO-class; under standing owner GO it runs, but the constitutional integrity filter (§0.8, no fabricated proof) and the walls below are non-negotiable.

## The proven pipeline (per product)
1. **Session check** (once/run): `manage_draft.py status` must return a number (E-004). If `None` -> session dead, owner must redo Google SSO login. If desc-persist starts failing late in a session (E-013) -> session fatigue, refresh before continuing.
2. **Pick** a **single-config** ASIN (NO size/color variants -> see Wall #1). Prefer in-stock bestsellers, light/non-fragile, non-restricted category, generic (no protected brand).
3. **Import**: `manage_draft.py import --url https://www.amazon.com/dp/<ASIN>` -> draft count must rise (no rise = silent import fail, skip).
4. **Economics filter**: `read_draft_economics.py` -> read buy/sell/profit/stock/region.
   - `buy≈133.13 AND stock=0` = **scrape FAIL sentinel** (E-012) -> DISCARD, never publish.
   - `stock=0` = OOS -> DISCARD.
   - `region 6` (AliExpress) = location wall (E-008/E-010) -> DISCARD (won't publish).
   - Keep only **region 1 (Amazon US), stock>0**. Note the real `profit` (~$7.5 via markup policy, but validate against eBay demand for true NET).
5. **Error pre-check** (E-014): `read_draft_errors.py` (or `read_full_error.py <needle>` for full message).
   - `EbayViolation` = restricted category -> DISCARD (don't waste a publish).
   - VeRO-word in title/desc -> fix in SEO step (rewrite to remove the word), then re-check.
6. **SEO**: `manage_draft.py set-title --match "<curr>" --title "<=80 generic VeRO-safe>"` (hard-caps 80) + `set-desc --id <id> --desc-file copy_X.html` (FULL rewrite, benefits not features, US-natural, only substantiated claims). Confirm **`PERSISTED: True` on BOTH** before publishing. Desc `PERSISTED: False` x2 (E-013) -> do NOT publish, skip.
7. **Publish** (one at a time): `publish_one_draft.py <id> "<guard substring of new title>"`. The script asserts guard==title (E-002) + cap80 before clicking. `RESULT: PUBLISHED (left drafts)` = live. `UNCONFIRMED` = verify with `read_draft_errors` (gone from drafts = published; still there = check error).
8. **Verify** the batch independently: `read_draft_errors.py` -> published items must be GONE from drafts.

## WALLS — avoid up front (do not re-learn these)
1. **Variant-heavy products** (size/color options: drawer dividers, herb scissors, kickboards, drink holders) -> AutoDS scrape-fail `$133/0`. Pick single-SKU.
2. **Restricted/chemical categories**: pool chlorine/bromine/test strips/sanitizers -> `EbayViolation` (E-014). Pick accessories, not chemicals.
3. **AutoDS VeRO-word list** (flagged in title/desc): **"gun"** (weapons -> use "blaster/soaker"), **"Ponds"** (brand -> use "water gardens"), **"Loop"**, **"Panasonic"**, **"Drop Stop"**, **"Gorilla Grip"**. Strip from MY copy; rewrite the scraped desc to clear them.
4. **AliExpress (region 6)** -> US item-location mismatch, won't publish. Amazon-US only.
5. **Seasonal/sports items frequently OOS** (swim training: dumbbells, pull buoy, kickboard, mesh bag). Check stock via economics first.

## PROFIT-FIRST selection (the upgrade)
- Don't publish for theoretical AutoDS markup; validate **eBay sold-demand + NET margin** first (skill `ebay-amazon-autods-profit-engine`, memory [[ebay-demand-first-net-margin]]). **#1 data gap = eBay sold-data (Terapeak/Seller Hub/API)** — owner-controlled; until enabled, demand is estimated and selection is partly blind.
- After listings go live: **measure sell-through** (which actually sell) -> double down on winners, kill the dead (skill `dropship-profit-run`). Net-profit per listing is the only score that matters.

## Risk / pacing (account stewardship)
- **Velocity:** flooding many arbitrage listings in one day raises eBay velocity/suspension risk (and the chemical `EbayViolation` is a real "no"). Pace it; don't dump 20+/day. (2026-06-24 hit ~27/day.)
- **Strategic endgame:** pure Amazon->eBay arbitrage is thin + fragile (AutoDS scrape ~50% fail + policy risk). The real moat = supply-chain L4 (US-warehouse / branded re-source) — skill `aliexpress-resourcing`.

## Known ops debt
- **Junk drafts accumulate** from scrape-fails ($133/0, wrong-product scrapes). At ~80 drafts, draft-id resolution gets unstable (an id resolved to the wrong product; E-002 guard correctly aborted the wrong publish). **Clean up scrape-fail drafts periodically** (bulk-delete the $133/0 junk) to keep the workspace deterministic.

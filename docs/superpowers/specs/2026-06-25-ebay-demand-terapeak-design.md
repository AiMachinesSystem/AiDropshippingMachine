# eBay Demand Validation (Terapeak) — design spec

Date: 2026-06-25 · Owner-approved (brainstorming, "fai A subito"). Implements the #1 capability gap from
`ENGINE_ARCHITECTURE.md` / the Training OS: per-candidate eBay demand (sold/sell-through/avg sold price/competitors)
so product validation runs on REAL eBay demand instead of an account-band proxy.

## Goal
Give the machine a read-only capability to fetch real eBay demand metrics for any product keyword, via **Terapeak**
(free in the owner's eBay Seller Hub → Research), automated with authenticated Playwright (same pattern as AutoDS).

## Components (3 isolated units)
1. **`login_ebay_save_session.py`** — one-time, HEADED. Opens eBay sign-in; the OWNER authenticates (incl. 2FA);
   saves `storage_state_ebay.json`. No automation of credentials. GO-CLASS (owner account login). Mirrors the AutoDS
   `login_and_save_session.py` contract. Prerequisite to everything else.
2. **`read_terapeak.py`** — READ-ONLY reader. Input: a keyword (or list). Navigates Terapeak Product Research,
   **captures the Terapeak API JSON** (same technique used to crack the AutoDS marketplace filter) + DOM fallback,
   extracts: avg sold price, sold count, sell-through %, active listings/competitors, free-ship %, top title keywords,
   price range. Caches to `90_CACHE/fetches/ebay/terapeak_<date>/`. Gentle rate (cap lookups/run). Per-keyword JSON out.
   *(First version is a PROBE: it must be cold-tested once a session exists to map the real Terapeak DOM/API — like the
   AutoDS probe. Unverified until then.)*
3. **`ebay_demand_gate.py`** — pure offline logic. Takes Terapeak metrics + Amazon cost → recomputes NET profit at the
   REAL avg sold price (owner formula) → assigns the candidate to the 3-stage funnel.

## The 3-stage demand funnel (owner: "3 → 2 → 1", permissive → balanced → severe)
- **ENTRY (permissive):** sell-through ≥25% AND sold ≥3/mo AND net ≥$3 (at avg sold price) → admit (≈3 per cohort to test).
- **VALIDATE (balanced):** ≥40% AND ≥10/mo AND net ≥$4 AND real 7-day impressions/watchers → keep ≈2.
- **SCALE (severe):** ≥60% AND ≥30/mo AND net ≥$5 AND real sales + clean account health → scale ≈1.
Thresholds are tunable constants. Maps onto the test→winner ladder + kill/fix/scale.

## Data flow
Amazon candidate (marketplace_source) → generic head-keywords → `read_terapeak` → cached metrics →
`ebay_demand_gate` (net at real avg sold price + funnel stage) → profit-engine scorecard (TEST/WATCHLIST/REJECT) →
report. Replaces the `[eBay-DATA REQUIRED]` flags with real numbers.

## Auth / prerequisite (the activation gate)
Owner runs `login_ebay_save_session.py` once and signs into eBay Seller Hub. Terapeak requires an eBay seller account
(owner has one, ~503+ listings). Until the session exists, the reader cannot run — clearly flagged.

## Error handling / known walls
- Terapeak captcha / UI change → document as a known wall (like AutoDS dropdowns); no-data → `[eBay-DATA: no Terapeak]`,
  never fabricated. Session expiry → re-run login. Rate-gentle (cap ~20-30 lookups/run).

## Success criteria (exit proof)
1. `login_ebay_save_session.py` produces a valid `storage_state_ebay.json` (owner-run).
2. `read_terapeak.py` returns real metrics for a test keyword (e.g. "kitchen utensil set") — VERIFIED live once session exists.
3. The profit-engine report shows real Terapeak sold/sell-through/avg-price instead of proxy; the funnel assigns stages.

## Out of scope (anti-overbuilding)
No auto-publish from this capability; no eBay API (separate path); no scaling logic beyond the funnel definition.
Build only the 3 units; wire into the profit-engine once the reader is cold-tested.

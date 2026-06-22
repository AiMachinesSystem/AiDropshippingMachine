---
machine: "eBay / AutoDS Dropshipping Machine"
type: intelligence_extraction + pattern_anomaly_report
phase: "Core Intelligence Architect — Phase 2"
status: complete
date: 2026-06-22
created_real: 2026-06-22
covers: INTELLIGENCE_EXTRACTION_REPORT + PATTERN_AND_ANOMALY_REPORT
---

# INTELLIGENCE & PATTERNS — Phase 2

> Reusable intelligence mined from the machine's own history. Each item is actionable (what changes / what risk it cuts).

## Strong patterns (repeated, high-confidence)
1. **"Demand ≠ opportunity" — proven 3× independently.** Every market run (2026-06-20 multi-niche, 06-21 amazon-to-ebay ×2) concluded: demand is real but commodity-saturated; win only with an ANGLE or cheaper sourcing. → routing: stop testing raw-demand commodities.
2. **Extreme sales concentration.** 94% of listings = 0 sales; top-5 = 66%, top-10 = 91%. The business is ~13 SKUs. → allocate to winners, kill the tail.
3. **Real edge = pool/pond/water cluster** (~7/13 winners) + kitchen ham-press + pet. Seasonal peak NOW. → sourcing focus.
4. **Sourcing is the margin ceiling AND the survival lever.** Amazon ~19% realized + suspension risk; AliExpress 45-55% + compliant. → top priority by impact and risk.

## Anomalies & risks
- **Suspension mechanism (external-confirmed):** eBay detects Amazon TBA tracking → "Retailer Dropshipping"; OOS defects = ~45% of bans. Our catalog was 62% errored/OOS (now 21). High historic ban exposure.
- **Operational dead-ends:** auto-order ON but **non-functional** (0 buyer accounts, $0 wallet); AutoDS **trial expired 2026-06-18**; AutoDS cost monitoring degraded (placeholder/inflated costs seen). → fulfillment + tooling gaps cap all scaling.
- **Pricing leak:** live 27% markup ≈ 3× under the profit-max point (elasticity sim). → reprice winners to market.

## Redundancies / stale / premature
- **Duplicate:** `_IMPORT/ebay_autods_initialization/...` full nested machine copy + root `.zip` (stale; both gitignored).
- **Stale caches:** `audit_2026-06-17_*`, `products/run/marketplace_2026-06-16/17`, `listing_audit_actions_2026-06-17.csv` — all pre-kill (214-era), superseded by `audit_2026-06-22_044324`.
- **Premature/other-domain automation (firewall R4):** `10_OUTPUTS/n8n_digital_products/` (Stripe/digital delivery) + `PLAYBOOKS/n8n_workflows/03_shopify_daily_snapshot.json` — "digital products"/"Shopify" are NOT this eBay machine's domain; built before the store is even operational. → owner decision: template scaffolding vs contamination.

## Bottlenecks (recurring walls)
- eBay aggregate sold = **403 wall** → counts are lower-bound proxies.
- AliExpress item cost = **CAPTCHA wall** → costs ESTIMATE until owner URL / visible browser.
- These two walls gate nearly every "verify margin/demand" step → the structural reason research stays LOW-SAMPLE.

## Net intelligence (what to do with it)
Concentrate on ~13 winners → reprice to market → re-source pool/water + ham on AliExpress (margin+survival) → fix fulfillment (GO) → only then ads at ≤3%. Everything else (commodity hunting, more automation) is noise until the engine is operational.

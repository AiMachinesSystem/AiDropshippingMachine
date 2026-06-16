---
machine: "eBay / AutoDS Dropshipping Machine"
type: data_intake_report
module: 10_OUTPUTS
status: complete
date: 2026-06-15
created_real: 2026-06-15
mission: DATA_COLLECTION_PUBLIC_RESEARCH
external_access: "public web, read-only (no login, no accounts, no credentials)"
live_changes: none
analysis: none
---

# Data Intake Report — eBay/AutoDS Public Policy/Fee/Feature Research (2026-06-15)

Path B (public research). **Stopped before analysis.** No login, no account access, no live changes, no strategy.
Evidence: every load-bearing fact `[OBSERVED — url, 2026-06-15 (cache: path)]`; **21 cache files** written before citation; WebSearch-only items quarantined as unverified.

## 1. Data collected (summary — detail in 02_DATA files)
- **eBay dropshipping policy:** allowed = own-inventory / wholesale agreement; **prohibited = retail/marketplace arbitrage** (buy from another retailer/marketplace shipped directly to buyer), any margin; seller liable for delivery + satisfaction; enforcement up to suspension + non-refundable fees.
- **eBay IP / items:** VeRO IP-reporting + enforcement; prohibited/restricted-items policy exists.
- **eBay seller standards:** levels (Top Rated/Above/Below), evaluated 20th monthly, 3-/12-mo lookback (400-sale split); defect rate ≤2%; cases-without-resolution ≤2 or ≤0.3%; **late-shipment ≤3% for Top Rated**; out-of-stock cancel = defect; Top Rated entry = ≥90d, ≥100 tx + $1,000 US/12mo.
- **eBay fees (US/eBay.com):** FVF most categories 13.6% (+ $0.30/$0.40 per order) on total sale; category-specific rates; insertion 250 free then $0.35; Store tiers $7.95–$349.95/mo; **regulatory operating fee 0.35% on eBay.it/EU listings**; EU-seller international fee table (0%–3.3%).
- **eBay returns/cancellations/shipping:** 30/60-day return options, free-returns = seller pays; MBG windows (30 cal days; seller pays return shipping for not-as-described); refund within 2 business days; buyer cancel ≤60 min; seller out-of-stock cancel = defect; handling time = payment→acceptance scan, ≤2 days recommended.
- **eBay selling limits:** account-specific (age/identity/site/performance/history/item-risk), monthly auto-review, active+sold+GTC count, blocks at limit.
- **AutoDS:** eBay automation (hourly price/stock scan, repricing, auto-fulfillment via Orders Processor add-on, auto-tracking); 8 channels; 30+ suppliers (many retailers); plans Import 200 $19.90/mo → Master 100K (USD); trial $0.99/3-day; vendor restatement of eBay policy (allowed wholesale / prohibited arbitrage, MC011).

## 2. Sources used
Official **eBay** (export.ebay.com EN/IN mirrors + ebay.com) and **AutoDS** (autods.com, help.autods.com) public pages — 21 cached. www.ebay.com `/help/` portal hit a fetch wall (timeouts) → official export mirrors used. Full list + walls: `02_DATA/source_access_notes.md`.

## 3. Files created (12)
- Raw: `02_DATA/01_RAW_DATA/policies/2026-06-15_ebay-policy-and-standards-raw.md`; `…/2026-06-15_ebay-returns-cancellations-shipping-limits-raw.md`; `02_DATA/01_RAW_DATA/autods_docs/2026-06-15_autods-features-pricing-policy-raw.md`
- Cleaned tables: `02_DATA/02_CLEANED_DATA/fee_table.md`; `policy_risk_table.md`; `autods_features_table.md`
- Notes/logs: `02_DATA/source_access_notes.md`; `data_quality_notes.md`; `02_DATA/03_MISSING_DATA/2026-06-15_public-research-missing-data-log.md`
- Mission: `00_SYSTEM_CONTROL/DATA_COLLECTION_PUBLIC_RESEARCH_MISSION.md`
- This report
- (+ 21 non-versioned cache files in `90_CACHE/fetches/`)

## 4. Files updated
- Cockpit (AUTO-REFRESH): `CURRENT_STATUS.md`, `ACTION_LOG.md`, `NEXT_ACTIONS.md`, `MASTER_DASHBOARD.md`, `RESEARCH_MEMORY_INDEX.md` (see commit).

## 5. Missing data
- **USER INPUT NEEDED:** confirm eBay market/site; account store-tier/level/limits/health; AutoDS plan/add-ons/currency; intended category.
- **PUBLIC RESEARCH REQUIRED:** eBay.it/EU localized fees+policy; verbatim US help pages (fetch wall); exact late-ship gate / TRS numerics / Below-Standard FVF uplift; US flat intl fee / +5% INAD / Promoted Listings rate; exact starter limits; AutoDS EUR pricing; eBay primary policy on Luca's site vs AutoDS restatement. Detail: `02_DATA/03_MISSING_DATA/2026-06-15_public-research-missing-data-log.md`.

## 6. Data quality risks
Market dependency (US vs eBay.it/EU) · export-mirror substitution for walled help pages · AutoDS = vendor restatement not eBay primary · AutoDS pricing USD/placeholder · some numerics absent · freshness (re-verify before action). Detail: `02_DATA/data_quality_notes.md`.

## 7. Current phase
Data Collection (public policy/fee/feature) **complete and cached**. Still at the **Data → Analysis gate**.

## 8. Next allowed step
Owner decides one of: **(a)** authorize **Analysis** of this collected data (still internal — interpret/compare/model against eBay rules and AutoDS capability); **(b)** approve a **follow-up public-research pass** to fill the [PUBLIC RESEARCH REQUIRED] gaps (esp. confirm eBay.it/EU schedule once market is given); **(c)** provide the **USER INPUT NEEDED** items (market, account, plan). No analysis performed until authorized.

## 9. Owner approval required?
- For the data collection done: already authorized (this GO); **complete**.
- To proceed: **YES** — Analysis is a separate gate (owner authorization), and the most useful single unblocker is **confirming Luca's eBay market** so the binding fee/policy schedule can be pinned.

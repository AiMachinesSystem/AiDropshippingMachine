---
machine: "eBay / AutoDS Dropshipping Machine"
type: operating_architecture
status: active (v1 — adopted 2026-06-24 from owner-provided 10-engine structure)
date: 2026-06-24
created_real: 2026-06-24
owner_input: "Luca 2026-06-24 — 10-engine structure to optimize product research → listing. 'vedi tu' how to integrate."
scope: "Architecture/routing artifact (AUTONOMIA EVOLUZIONE CONTROLLATA — allowed). Does NOT alter vision, GO gate,
  firewall, §0 rules, owner role, or live/external boundaries. Evidence labels & gates unchanged."
---

# ENGINE ARCHITECTURE — the machine's 10-engine operating model (v1)

The machine runs as **10 engines** from idea → live profitable listing → scale. This file is the canonical map:
what each engine does, its **honest status** in THIS machine, the **existing assets** that implement it, and the
**top gap** to improve next. The owner's current priority — *optimize product research for listing* — is the
chain **1 → 2 → 3 → 6 → 7** (see §Flow). Status legend: **BUILT** (real, used) · **PARTIAL** (some real assets,
gaps) · **STUB** (named/aspirational, not yet exercised).

## The 10 engines

| # | Engine | Purpose | Status | Existing machine assets | Top gap to improve |
|---|---|---|---|---|---|
| 1 | **Market Research** | Find niches, competitors, trends, customer problems | **BUILT** | Cracked AutoDS marketplace filter API (`marketplace_filter_probe*.py`); sourcing pulls `marketplace_source(_band/_pool/_summer).py` (demand-gated rating>4.3 & reviews>N = competitor "winning" feed); RUN-03 niche analysis; **price-band study** (`2026-06-24_price-band-analysis…`); `RESEARCH_MEMORY_INDEX`; skills `niche-intelligence-run`, `competitor-scan`, `ads-library-scan` | True customer-voice/pain mining (reviews, eBay Q&A); trend/seasonality signal beyond season heuristic |
| 2 | **Product Validation** | Scorecard: margin, policy risk, supplier risk, demand | **BUILT** | `rank_us_source.py` (scorecard: margin, VeRO, eBay-policy, warehouse, ship-time, TEST/HOLD/KILL); demand gate (>reviews); cost-gate **E-003**; price-band fit; warehouse rule **L-004** | Net-of-fee margin (eBay FVF) not just gross; sell-through prediction; auto VeRO/trademark check |
| 3 | **Supplier Intelligence** | Suppliers, lead time, stock, quality, samples | **PARTIAL** | `read_draft_economics.py` (cost/stock/region); `min_price_warehouse` US/CN; `max_shipping_time`; scrape-sentinel **E-012** (133.13/0 = failed import); multi-variant fail detection | No quality/defect/return tracking; no sample protocol; no supplier-rating history |
| 4 | **Offer** | Bundles, pricing, angle, guarantees, upsell | **STUB** | AutoDS pricing policy (markup, monitored — **E-011**); profit-mastery playbook (bundling lever); skill `offer-diagnosis` (stub) | No bundle builder; no guarantee/angle library; pricing not yet optimized per-item |
| 5 | **Creative** | Ads, UGC scripts, hooks, images, video | **STUB** | Skills `creative-brief-builder → higgsfield-prompt-builder → test-plan-builder` (GATED); Higgsfield MCP | Not exercised; eBay is search-led (creative lower priority than DTC) — keep STUB until an ads channel is opened |
| 6 | **Listing / Store** | Product pages, descriptions, SEO, FAQ | **BUILT** | `manage_draft.py` (import/title≤80/CKEditor desc/image); `publish_one_draft.py` (E-002 guarded); **`batch_publish.py`** (orchestrated batch, E-012/E-013/E-002 safeguards, desc-retry); title≤80 + VeRO-safe desc-rewrite rule; `copy_*.html` | Auto-generated titles still imperfect; no item-specifics optimizer; no FAQ block |
| 7 | **Testing** | Controlled tests, read metrics, kill/scale | **PARTIAL** | Publish-test batches (`PUBLISH_TOP_N_TEST`); cold-test discipline (E-011); Monte Carlo sim (`profit_montecarlo.py`); kill via `remove_oos_listings.py` / `delete_drafts_guarded.py` | No live sell-through readout loop per test cohort; no automated kill/scale trigger on metrics |
| 8 | **Operations** | Orders, tracking, returns, tickets, supplier issues | **STUB** | AutoDS auto-order (NOT functional — 0 buyer acct/$0 wallet, per notes); manual fulfillment | Auto-order pipeline; tracking/returns/ticket handling (owner-side today) |
| 9 | **Finance** | P&L, net margin, CPA, ROAS, refunds, cash flow | **PARTIAL** | Profitability model (`2026-06-22_profitability-model…`); Monte Carlo; margin/profit fields; reprice tooling (`reprice_all_dryrun.py`) | Live P&L from real orders; net-margin-after-fees; cash-flow tracking |
| 10 | **Learning** | Archive what works, patterns, errors, playbooks | **BUILT** | `07_LEARNING/*`; **ERROR_REGISTRY** (E-001…E-013); `sop_improvements` (L-001…L-004); `RESEARCH_MEMORY_INDEX`; skill `weekly-learning-update`; profit-mastery playbook | Win-pattern archive from live sales (waits on measurement data) |

**Honest read:** strong engines = **1 Research · 2 Validation · 6 Listing · 10 Learning** (real tooling, used).
Partial = **3 Supplier · 7 Testing · 9 Finance**. Stub = **4 Offer · 5 Creative · 8 Operations** (the latter two
gated on a sales channel / working auto-order — do NOT overbuild before they're exercised, per §9 anti-overbuilding).

## Flow — the optimized PRODUCT RESEARCH → LISTING pipeline (owner's priority: 1→2→3→6→7)
Canonical, repeatable, with the real tools + GO gates:

1. **[E1 Research]** Pull demand-gated candidates from the marketplace filter API into a niche/price-band:
   `marketplace_source(_band/_pool/_summer).py` (category-id + search_query + rating/reviews/price filters, US-warehouse).
2. **[E2 Validation]** Score + filter: `rank_us_source.py` → US-warehouse + on-niche + generic(VeRO-LOW) + margin + price-band fit → TEST/HOLD/KILL. Apply **L-004 US-warehouse-first** and the price-band study (prefer $40–140; $15–40 is the dead zone).
3. **[E3 Supplier]** Sanity per candidate at import: skip **E-012** sentinel ($133.13/stock0 = scrape fail / multi-variant); prefer single-config ASINs; verify warehouse via API not UI label.
4. **[E6 Listing]** `batch_publish.py` orchestrates: import → generic title ≤80 → VeRO-safe English desc (rewritten, **never** scraped) → verify `PERSISTED` (E-013 retry) → `publish_one_draft.py` (E-002 guard). **Publish = GO-CLASS.**
5. **[E7 Testing]** Verify live in `/products` (item_id + status=2); read sell-through over time; kill dead / scale winners (guarded). Feed results to **[E10 Learning]**.

**Gates that never move:** publish/price/spend/account = per-action owner GO; firewall between projects; evidence labels.

## Improvement backlog (prioritized — work the strong engines' gaps first)
1. **E2 net-of-fee margin** — add eBay FVF (~13.25%+$0.40) to `rank_us_source.py` so margin reflects real net, not gross. *(highest ROI: current "margin" overstates.)*
2. **E7 sell-through loop** — a reader that tags each published cohort and reads units-sold over time → kill/scale signal (turns Testing PARTIAL→BUILT). Needs measurement window.
3. **E1 customer-voice mining** — pull review pain-points per candidate niche (skill `customer-voice-mining`) to sharpen titles/desc + offer angle.
4. **E3 supplier quality history** — log defect/return/stock-out per supplier as orders accrue.
5. **E4 Offer** — only when a winner emerges: bundle + guarantee library. *(STUB until a proven winner — anti-overbuilding.)*

## Growth ladder (the path the engines feed)
Dropshipping **test** → validated **winner** → better **supplier** → **branded packaging** → proprietary
**bundle/offer** → **private label** → organic **content + ads** → **email/SMS** → **repeat buyers** →
**sellable brand**. Engines 1–3–6–7 (research→validation→listing→testing) drive the test→winner rungs; rungs
beyond "winner" unlock only on proven, measured success (anti-overbuilding §9). We are at **rung 1 (test)**.

## Core principle update (2026-06-24) — eBay-demand-first + NET margin
- **The Golden Rule:** never list a product just because it exists on Amazon. Amazon = source/DATA; **eBay = where
  demand is proven** (sold/sell-through). Validate eBay demand + NET margin + risk + seller safety before any draft.
- **NET, not gross:** margin uses the owner net-profit formula (eBay price − Amazon cost − ship/tax buffer − eBay FVF
  ~13.5%+$0.40 − promoted − AutoDS alloc − return reserve). Max safe ad spend = profit-before-ads. This is now Engine 2's
  core (supersedes gross-margin scoring — see backlog #1, now DONE in the profit-engine skill).
- **Canonical implementation:** skill **`ebay-amazon-autods-profit-engine`** (STEP-1) chains engines 1→2→3→6→7 with the
  12-step pipeline, scorecard, KPI table, report template (`REPORTS/EBAY_AUTODS/EBAY_AMAZON_AUTODS_PROFIT_TEST_*.md`),
  and kill/fix/scale rules. First run: `EBAY_AMAZON_AUTODS_PROFIT_TEST_001` (2026-06-24).
- **#1 capability gap (gating):** per-candidate eBay demand data (sold/sell-through) — no connected source yet.
  Unlock via **Terapeak** (owner Seller Hub) or **eBay API** (Browse + Marketplace Insights, GO-CLASS). Until then,
  eBay demand uses the account's own price-band/niche history as a labeled PROXY; external numbers are `[eBay-DATA REQUIRED]`.

## Governance
This is a routing/architecture artifact under AUTONOMIA EVOLUZIONE CONTROLLATA. It maps and organizes existing
capability; it does **not** modify vision, the GO gate, the firewall, §0 rules, the owner role, or any live/external
boundary, and introduces no new evidence labels. Per-engine playbooks/skills are added **only** as each engine is
exercised on a near, realistic scenario (anti-overbuilding §9) — most engines stay as mapped above until then.

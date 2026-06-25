---
name: ebay-amazon-autods-profit-engine
description: >
  STEP-1 eBay+Amazon AutoDS profitability research & validation engine. Use when the owner asks to research,
  validate, or score Amazon-sourced products for eBay listing ("trova prodotti", "profit engine test",
  "360 research", "valida prodotti per eBay"). Sources product DATA from Amazon (via AutoDS marketplace),
  validates DEMAND on eBay, simulates NET profit, scores policy/account risk, rewrites SEO, and proposes
  AutoDS draft settings. Research/draft only — never publishes without explicit OWNER_GO.
owner_input: "Luca 2026-06-24 — full STEP-1 spec (net-profit formula, 12-step pipeline, KPI table, report template, eBay-demand-first rule)."
status: active v1 (eBay-demand DATA SOURCE is a PARTIAL capability — see §0 Data Sources)
---

# eBay + Amazon AutoDS Profit Engine — STEP 1 (research & validation)

Act as an eBay dropshipping profitability machine using **Amazon.com as the product/DATA source** and
**eBay.com as the DEMAND marketplace**, automated via **AutoDS**. Goal: import ONLY products that survive
demand, margin, policy-risk, SEO and seller-account-safety validation. TEST RUN; draft/research only;
**no live publishing without explicit OWNER_GO**; no mass upload; no IP/restricted/fragile/high-return products;
no fabricated numbers.

## THE GOLDEN RULE
**Do NOT list a product because it exists on Amazon. List ONLY if eBay demand + net margin + risk score +
seller safety are ALL acceptable.** Amazon = where we source & read product data. eBay = where we prove demand.

## §0 DATA SOURCES — honest capability map (read first; never fabricate)
| Field group | Source we HAVE | Status |
|---|---|---|
| Amazon product (title, ASIN, price, rating-gate, reviews-gate, images, warehouse US/CN, ship-time, variation hints) | AutoDS marketplace filter API (`marketplace_source*.py`) | **HAVE** |
| Amazon deep (negative reviews, coupon, Prime estimate, Amazon competition level, package weight) | Amazon page scrape (captcha-walled) or a paid Amazon data API | **GAP — GO needed** |
| eBay demand for OUR niches/price-bands (sell-through by band, avg sold) | the account's OWN sales history (RUN-03, price-band study) = real eBay demand PROXY | **HAVE (proxy)** |
| eBay demand PER candidate (sold listings, sell-through, avg sold price, competitor density, promoted density, buyer complaints) | eBay Browse + **Marketplace Insights API** (dev keys+auth) OR **Terapeak** (owner Seller Hub) OR eBay sold-search scrape (likely walled) | **GAP — #1 unlock, GO/owner needed** |

**Rule:** every eBay-demand number that is NOT from the account's own data or a connected eBay source is marked
`[eBay-DATA REQUIRED]`, never invented. The engine runs fully on the Amazon-side + net-margin + risk + SEO today;
the per-candidate eBay-demand step is **gated on unlocking an eBay data source** (recommend: eBay API or Terapeak).

## NET PROFIT FORMULA (owner, conservative)
```
Net Profit = eBay selling price
           − Amazon product cost
           − Amazon shipping/tax buffer        (default $3.00; use real if known)
           − eBay final value fee + payment fee (≈ 13.5% × price + $0.40)
           − promoted listing cost             (0 for "profit before ads")
           − AutoDS cost allocation            (default $0.50)
           − return/refund reserve             (default $2.00, or % of price)
Profit before ads = the above with promoted = 0.
Max SAFE promoted/ad cost = Profit before ads.   (never spend more on ads than the per-unit profit)
Net margin % = Net Profit / eBay selling price.
Min profitable eBay price = price where Net Profit = 0.
Max safe Amazon source cost = cost where Net Profit hits the target floor (default $4).
```
Worked check (owner): $49.99 − $29.99 − $3.00 − $7.00 − $2.00 − $0.50 = **$7.50 before ads → max ad < $7.50.**
If data is missing → mark `ESTIMATE` and state the assumption.

## EXECUTION PIPELINE (12 steps)
1. **Amazon Product Scan** — `marketplace_source*.py`: price $15–80, rating ≥4.2, reviews ≥300, not famous-brand-dominated,
   not medical/supplement/cosmetic/weapon/adult/IP/counterfeit/fragile/restricted, clear utility/gift/hobby/home value,
   good image appeal, avoid defect/breakage/wrong-size/missing-parts/late-delivery complaints. Extract the Amazon field set (§Amazon fields).
2. **eBay Sold Demand Check** — per candidate, eBay field set (§eBay fields). `[eBay-DATA REQUIRED]` until a source is connected;
   use account price-band/niche sell-through as the PROXY meanwhile.
3. **Margin Simulation** — apply the NET PROFIT FORMULA. Conservative. Reject if net < $4 or net margin < ~10%.
4. **Competitor Gap Check** — competitor count, listing quality, promoted density, price floor/ceiling. `[eBay-DATA REQUIRED]`/proxy.
5. **Policy / IP / Brand Risk Check** — VeRO, brand/IP, counterfeit, restricted category, Amazon-seller-of-record risk.
6. **Shipping & Return Risk Check** — warehouse US (L-004), ship-time ≤5 preferred, fragility, return-prone categories.
7. **SEO Rewrite** — eBay title ≤80, never copy Amazon title; 5 benefit bullets; clean desc; item specifics; keywords.
8. **Pricing Strategy** — eBay price from demand band + competitor floor; min-profitable + max-source-cost; promoted ≤ profit-before-ads.
9. **AutoDS Draft Creation** — `batch_publish.py`/`manage_draft.py` (DRAFT only): monitoring, min-stock, price-change, OOS action, reprice, profit-protect.
10. **Manual/Owner GO before publishing** — HARD gate. Publish = GO-CLASS.
11. **7-day performance measurement** — impressions, views, watchers, clicks, price movement (KPI table).
12. **Kill / Fix / Scale decision** — per the kill/fix/scale rules.

## SCORECARD per product
margin(net$) · net% · eBay-demand(score+evidence) · competition(score) · policy/IP risk · shipping/return risk ·
SEO(score) · final decision **TEST NOW | WATCHLIST | REJECT**. Risk class: LOW | MEDIUM | HIGH | REJECT.
**REJECT immediately if:** net margin too thin · fragile · high defect complaints · depends on famous-brand demand ·
IP/copyright risk · unreliable shipping · Amazon-packaging/third-party fulfillment risk · eBay competition makes profit unrealistic.

## KPIs (measurement loop)
Sell-through (real eBay demand?) · Gross margin (room?) · Net margin (actually profitable?) · Views (eBay visibility?) ·
Watchers (buyer interest) · CTR (title/photo strength) · Conversion (offer strength) · Return risk · Late-shipment risk · Defect risk.

## Amazon fields to extract
product name · ASIN · price · coupon/discount · Prime/shipping estimate · rating · review count · top positive patterns ·
top negative patterns · category · variation count · stock signals · brand/IP risk · fragile/return risk · package size/weight ·
Amazon competition level · reason it may work on eBay. *(Deep fields = GAP, see §0.)*

## eBay fields to extract `[eBay-DATA REQUIRED / account-proxy]`
active listings · sold listings · sell-through rate · average sold price · lowest competitor price · highest realistic price ·
number of competing sellers · competitor listing quality · common title keywords · common item specifics · common shipping terms ·
promoted listing density · buyer complaints · return policy patterns.

## REPORT (output)
Save to `REPORTS/EBAY_AUTODS/EBAY_AMAZON_AUTODS_PROFIT_TEST_<NNN>.md` with sections:
**A. Executive Summary** (best / safest / highest-margin / rejected-for-risk / overall rec) ·
**B. Product Comparison Table** (name · Amazon price · est eBay price · net profit · margin% · demand · competition · risk · SEO · decision) ·
**C. Top-3 Deep Dive** (why it works · eBay demand evidence · Amazon evidence · competitor weakness · margin sim · risk · optimized title · price · AutoDS settings · first test action) ·
**D. Rejected** (exact reason) · **E. 7-Day Test Plan** (Day1 research→Day7 kill/fix/scale) · **F. Kill/Fix/Scale Rules**.
Then update the machine index (RESEARCH_MEMORY_INDEX / cockpit) with: date · scanned · approved · rejected · top opportunity · highest risk · next action.

## 7-DAY TEST PLAN template
D1 research+validation · D2 supplier/source check · D3 eBay SEO draft creation · D4 pricing+AutoDS rules ·
D5 publish ONLY OWNER_GO listings · D6 monitor impressions/views/watchers/clicks/price · D7 kill/fix/scale.

## KILL / FIX / SCALE rules
- **Kill** if no impressions after 3–4 days (dead listing) OR net margin proven negative.
- **Fix title/SEO** if impressions low.
- **Fix price** if views exist but no watchers.
- **Fix offer/bundle** if watchers exist but no sales.
- **Scale** ONLY if net profit positive AND no account-health risk (late-shipment/cancellation/return/defect not rising).
- **Never scale** if late-shipment, cancellation, return, or defect risk increases.

## VISIBLE CONFIRMATION (what to show the owner)
1. Top 3 TEST NOW products · 2. Estimated NET profit per item · 3. Main eBay demand signal · 4. Main risk ·
5. Recommended AutoDS action · 6. Whether OWNER_GO is required before publishing (it always is for publish).

## GROWTH LADDER (the path this engine feeds)
Dropshipping test → validated winner → better supplier → branded packaging → proprietary bundle/offer →
private label → organic content + ads → email/SMS → repeat buyers → **sellable brand**. STEP 1 (this skill)
only finds & validates the test candidates; each later rung unlocks on proven, measured success (anti-overbuilding).

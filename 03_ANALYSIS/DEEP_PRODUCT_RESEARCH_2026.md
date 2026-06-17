---
machine: "eBay / AutoDS Dropshipping Machine"
type: deep_product_research
status: complete
scope: read-only product research (multi-tool funnel) — NO import, NO publish, NO live action
date: 2026-06-16
created_real: 2026-06-17
method: top-down + bottom-up funnel. web_search (macro trends + sub-niches) · Playwright AutoDS saved session (Marketplace product/supplier/cost data) · r.jina.ai proxy + web fetch (eBay demand cross-check). Multi-agent: 15 web-research agents + 2 read-only AutoDS Playwright runs, then synthesis.
evidence_cache:
  - 90_CACHE/fetches/autods/marketplace_2026-06-16_233945/   (AutoDS Marketplace: 121 products, API JSON + screenshots)
  - 90_CACHE/fetches/autods/products_2026-06-16_230501/ + drafts_2026-06-16_230951/   (account catalog reads)
  - workflow web-research output (macro trends, sub-niches, eBay cross-check) — transient agent results, key data transcribed below with source URLs
evidence_labels: "[OBSERVED]=fetched a page/API stating it (+source) · [ESTIMATE]=declared estimate · [INFERRED]=reasoned · [UNKNOWN]=source blocked, never invented"
---

# DEEP PRODUCT RESEARCH 2026 — eBay/AutoDS (US)

> **READ-ONLY.** No products were imported, listed, priced, or ordered. Every number carries an evidence label + source. Margins are computed at **eBay FVF 13.6% + $0.40/order**, shipping assumed included for light items (heavy/bulky items flagged).

## 0. Two honest walls hit this run (read these first)
1. **eBay aggregate sold/active counts are mostly [UNKNOWN].** eBay's `/sch` search and `LH_Sold=1` completed pages returned **403/429** on direct fetch AND via the r.jina.ai proxy (2026-06-16). So the gate *"≥200 eBay sold"* could **not** be confirmed as an aggregate for any product. What I **could** observe: **per-listing "X sold" badges** (lower-bound demand signals) and some **category/active-listing counts** via eBay `/b/` and `/shop/` proxy renders. Where blocked → marked [UNKNOWN], never invented. *(Independently re-verified by a verifier agent: no fabricated numbers.)*
2. **AutoDS's curated "Trending"/"Hand-Picked" research views are paywalled** behind the *Product Finding Hub* add-on (this account is on a trial) — [OBSERVED, cache `marketplace_2026-06-16_233945/01_trending.txt` + `02_hand_picked.txt` show the "Buy Product Finding Hub Addon" wall]. So AutoDS product data below comes from the **general Marketplace browse API** (`gw.autods.com/marketplace/api/products/`), which returned **121 real products** with supplier, cost, MSRP, category. The API's `is_winning_product` flag is the only AutoDS-native "winner" signal available (4 flagged).

---

## 1. LEVEL 1 — MACRO TRENDS (US, growing now, 2026) [OBSERVED]

| Macro trend | Growth | Demand signal (source) |
|---|---|---|
| **Pet supplies** | growing | US pet spend **$158B (2025), →$165B (2026, ~4.4%)**; dog ownership 51%→53% of households; small pets surging (birds +25%, reptiles +20% YoY). Source: APPA 2026 State of the Industry (americanpetproducts.org). |
| **Health & wellness / functional** | growing | High-protein RTD **+71% over 4 yrs**; protein-snacks **$32.01B (2025)→$34.44B (2026)**; GLP-1 tailwind. Source: Circana via feedstuffs.com; mordorintelligence.com. |
| **Outdoor & sports (pickleball/camping)** | growing | Pickleball **24.3M players 2025, +171.8% (2022-25)**; 80.5% of Americans 6+ active (all-time high). Source: SFIA 2026 (sfia.org); OIA. |
| **Automotive aftermarket** | growing | US light-duty aftermarket **+5.2% YoY 2026**, →>$500B by 2029; record vehicle age + e-commerce. Source: Auto Care Assoc./MEMA/S&P (thebrakereport.com); mordorintelligence.com. |
| **Home organization** | growing (moderate) | US organizers/storage **~$12.05B (2025)→$15.21B (2030), ~4.78% CAGR**; e-comm 22%→28% by 2026. Source: mordorintelligence.com; sourceready.com. |
| **Kitchen gadgets (PFAS-free/viral)** | growing | US small kitchen appliances **$4.98B (2024)→$7.8B (2033), ~5.12%**; TikTok-driven cheap single-problem gadgets. Source: sourceready.com; accio.com. |
| **Arts, crafts & DIY** | growing (global) | Global crafts **$47.35B (2025)→$50.7B (2026), ~7.1%**; DIY/personalized kits = 32% of craft purchases. US online sub-segment only +1.4%. Source: thebusinessresearchcompany.com; ibisworld.com. |

---

## 2. LEVEL 2 — SUB-NICHES (3 per macro) [OBSERVED unless noted]

- **Pet:** slow-feeder dog bowls (33.1K searches +22%, year-round); cat water fountains (NA $2.16B→$5.39B 2034, year-round, higher ASP); **dog cooling mats** (~$500M, ~12% CAGR, **strongly seasonal May-Aug — window opening now**).
- **Health & wellness:** red-light therapy devices (+59% YoY, ~2.5M searches, high comp); percussion massage guns (US $130.7M, **Dec peak**, $34-90 ASP); posture correctors ($1.46-1.68B 2026, evergreen+spikes).
- **Outdoor & sports:** camping rechargeable headlamps (eBay cat 44,662 active [OBSERVED]); **bicycle lights** (eBay cat **79,848 active** [OBSERVED], Apr-Oct); fishing tackle/lures (eBay Fishing cat 2.17M active [OBSERVED], strong summer).
- **Home org:** under-sink/cabinet pull-out organizers (eBay cat ~15,081 [OBSERVED-via-summary], Jan + spring lift); closet systems (cat ~71,358); garage wall/pegboard (Jul-Aug peak).
- **Automotive:** magnetic/wireless car phone mounts ($2.5B→$5.8B, ~10.8%, Dec+Aug-Sep peaks); car trunk/cargo organizers (summer peak Aug-Sep); LED interior/ambient lighting kits ($2.07B→$5.44B 2034).
- **Beauty:** LED light-therapy face masks (US $65.37M 2025, ~10.6% CAGR, L'Oréal CES 2026); gua sha / jade roller (gua sha +124% YoY, $487.6M 2026); men's beard grooming (US men's grooming $50.2B→$82.8B, beard-oil Dec peak).
- **Hobby/craft:** diamond painting kits (**Nov-Dec peak**, $248M by 2033); Cricut/die-cut accessories (consumables = steady replenishment); resin art supplies (~70% margins reported, Dec-Feb peak, most differentiable).
- **Kitchen:** espresso/coffee-bar accessories (Q4 peak, home-coffee-bar trend); electric milk frothers (Dec peak); **wireless Bluetooth meat thermometers** (smart-meat-thermometer $275.7M→$700M, **Father's Day + summer grilling — in season now**).

> **Seasonality note (today = mid-June 2026):** *in-season now* = dog cooling mats, meat thermometers, fishing/bike/camping, car cargo organizers, trampoline accessories. *Off-season now* = Christmas dog bandanas, diamond painting, winter dog coats, massage guns (Q4).

---

## 3. LEVEL 3 — AUTODS MARKETPLACE CROSS-CHECK [OBSERVED]
From the AutoDS Marketplace browse API (121 products, cache `marketplace_2026-06-16_233945/`): **29 products with supplier cost ≤ $8**, **4 flagged `is_winning_product`** (toilet seat covers, kids bow & arrow set, 3D anatomy torso, body-shaper). Supplier mix: ~53 Amazon, remainder AliExpress/CJ-style stores. The cheap-enough (≤$8) generic items concentrate in **beauty consumables, pet apparel, auto accessories, home consumables, smart-home** — and these are the ones cross-checked on eBay below.

---

## 4. LEVEL 4 — OPERATIONAL GATE CHECK (the funnel floor)

**Gate definitions:** ① eBay demand (target ≥200 sold) · ② AutoDS cost ≤ $8 · ③ margin ≥ 50% after fees · ④ no brand/VeRO · ⑤ AutoDS-available.
**Reality check on Gate ①:** aggregate eBay sold is [UNKNOWN] (blocked). I report the **best [OBSERVED] per-listing "X sold" badge** as a lower-bound. A product "passes ①" only where a single live listing already shows ≥200 sold [OBSERVED].

### TOP 15 — ranked (cost [OBSERVED AutoDS], sell [OBSERVED eBay], margin computed)

| # | Product (generic) | Niche | Cost ($) | eBay sell ($) | Margin | eBay demand (best [OBSERVED] / aggregate) | Comp. | Brand/VeRO | Season | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Phone anti-lost tether/lanyard** | mobile acc. | 1.64 | 10.99 | **67.8%** | 145 sold/listing · agg [UNKNOWN] | high | low | year-round | ✅ all gates exc ① agg |
| 2 | **3D human-body torso anatomy model (kids/edu)** | hobby/edu | 6.14 | 23.99 | **59.1%** | **204 sold/listing** ✅① · agg [UNKNOWN] | med | low | year-round | ✅ strong (bulky ship) |
| 3 | **Rubber duck car antenna topper (generic)** | auto novelty | 2.25 | 9.99 | **59.9%** | generic ~1 sold; form-factor 364 (Disney) | **low** | low* | year-round | ✅ best comp; thin demand |
| 4 | **Disposable mascara wands/spoolies** | beauty | 3.18 | 9.99 | **50.6%** | **529 sold/listing** ✅① · agg [UNKNOWN] | very high | low | year-round | ✅ huge demand, commodity |
| 5 | **Waterproof winter dog coat** | pet | 4.53 | 15.99 | **55.6%** | agg [UNKNOWN]; 6,357 active supply | high | low | **winter (off now)** | ✅ margin; seasonal+returns |
| 6 | **Kids bow & arrow archery toy set** ⭐win | outdoor/toy | 7.69 | 24.99 | **54.0%** | 34 sold/listing · agg [UNKNOWN] | med | low-med | gifting/summer | ✅ margin; child-safety |
| 7 | **Travel disposable toilet seat covers (50pc)** ⭐win | home/travel | 4.41 | 13.99 | **52.0%** | 49 sold/listing · agg [UNKNOWN] | high | low | year-round | ✅ margin; modest demand |
| 8 | **WiFi smart plug (Alexa/Google)** | smart home | 5.49 | 16.99 | **51.7%** | 85 sold/listing · agg [UNKNOWN] | high | **med (UL/FCC+Tuya TM)** | year-round | ⚠️ compliance-heavy |
| 9 | **Glitter liquid eyeliner (generic)** | beauty | 6.31 | 18.95 | **51.0%** | **486 sold/listing** ✅① · agg [UNKNOWN] | high | med (cosmetics) | year-round | ✅ at ≥$18; compliance |
| 10 | **WiFi door/window sensor** | smart home | 6.09 | 16.99 | 48.2% | agg [UNKNOWN] | high | med | year-round | ⚠️ margin <50% |
| 11 | **Trampoline spring pull tool** | outdoor | 3.99 | 9.99 | 42.5% | 15 sold/listing (weak) | low | low | summer (now) | ⚠️ add-on only, weak demand |
| 12 | **Christmas plaid dog bandana** | pet | 5.99 | 14.99 | 43.8% | 78 sold/listing · agg [UNKNOWN] | high | low | **Q4 only (off now)** | ⚠️ margin+season |
| 13 | **Spa bow headband set** | beauty | 7.99 | 17.99 | 39.8% | agg [UNKNOWN] | high | low | year-round | ⚠️ margin fragile |
| 14 | **Clear retainer/aligner case** | beauty/health | 5.79 | 9.95 | **24.2%** ❌ | 96 sold/listing · agg [UNKNOWN] | med | med (avoid "Invisalign") | year-round | ❌ fails margin at observed cost |
| 15 | **Bluetooth call smart watch (cheap)** | electronics | 4.22 | 25.00 | ~67% | agg [UNKNOWN] | very high | **HIGH (FCC, brand-impersonation, returns)** | year-round | ⚠️ margin great / risk high |

*Rubber duck: GENERIC duck = low risk; the high-selling 364-sold listing is **Disney-branded** = HIGH VeRO — sell only plain ducks.

**Failed the funnel (excluded, for the record):** car phone holder steering-wheel clip (cost $5.79 vs $4-6 eBay floor → ~24% margin ❌); disposable lash cleanser brush (cost $4.99 vs ~$7 sell → ~9% ❌); neoprene dumbbells & travel duffle & 3-pack socks (heavy/bulky ship and/or **brand-dominated search + VeRO**: Nike/Amazon Basics/Vera Bradley ❌); all natively-branded source items (Maybelline, Amazon Basics, BioSwiss, Instituto Español, "Edanta" eyeliner → source a generic equivalent instead).

---

## 5. TOP 5 — FULL LISTING CARDS (drafts only; nothing published)

### #1 — Phone Anti-Lost Tether / Lanyard Strap (Universal)
- **eBay title:** `Anti-Lost Phone Tether Strap Universal Safety Lanyard Holder Cord Patch Tab 3 Pack`
- **Category:** Cell Phones & Accessories › Cell Phone Accessories › Lanyards
- **Cost:** $1.64 [OBSERVED — AutoDS Marketplace, supplier AliExpress store, id `1005007102889900` → https://www.aliexpress.com/item/1005007102889900.html]
- **Suggested sell:** $10.99 → **margin 67.8% / profit $7.46** [computed, FVF 13.6%+$0.40]
- **Demand:** [OBSERVED] eBay listings at $10.99-$12.99 showing **145 / 143 / 117 sold** (source: r.jina.ai render of ebay.com/shop/phone-anti-lost-lanyard, 2026-06-16). Aggregate sold [UNKNOWN] (403).
- **Item specifics:** Brand: Unbranded · Type: Phone Tether/Lanyard · Material: TPU/nylon · Compatibility: Universal · Pack: 3.
- **Risk:** competition high (1,100+ active [OBSERVED]); commodity → differentiate via multipack/patch+carabiner combo. VeRO low. Lightest ship weight = best margin profile. **Strongest overall pick.**

### #2 — 3D Human Body Torso Anatomy Model (Educational / Kids)
- **eBay title:** `3D Human Body Torso Anatomy Model Educational Assembly Kit Kids Science Learning Toy`
- **Category:** Toys & Hobbies › Educational › Science & Nature (adult version: Business & Industrial › Healthcare › Anatomical Models)
- **Cost:** $6.14 [OBSERVED — AutoDS Marketplace, **`is_winning_product`**, id `3256802880094266` → https://www.aliexpress.com/item/3256802880094266.html]
- **Suggested sell:** $23.99 → **margin 59.1% / profit $14.19**
- **Demand:** [OBSERVED] eBay torso listings show **204 / 52 / 45 sold** (ebay.com/shop/anatomy-model-torso via jina, 2026-06-16) — **passes the ≥200 lower-bound**. Aggregate [UNKNOWN].
- **Item specifics:** Brand: Unbranded · Type: Anatomical Model · Age: 8+ · Material: PVC · Assembly: DIY.
- **Risk:** **bulky/heavier → verify AutoDS ship weight/cost before final margin**; medium competition (823 active [OBSERVED]); age-grading/safety copy for kids version. VeRO low.

### #3 — Rubber Duck Car Antenna Topper (Generic Yellow)
- **eBay title:** `Rubber Duck Car Antenna Topper Cute Yellow Duck Aerial Ball Auto Exterior Decoration`
- **Category:** eBay Motors › Parts & Accessories › Car & Truck Exterior › Antennas (or Novelty)
- **Cost:** $2.25 [OBSERVED — AutoDS Marketplace, supplier AliExpress, id `1005006027632555` → https://www.aliexpress.com/item/1005006027632555.html]
- **Suggested sell:** $9.99 → **margin 59.9% / profit $5.98** (room to $12-15 given low competition)
- **Demand:** [OBSERVED] **lowest competition of the set (~32 active for exact phrase)**; generic sold thin (1 sold seen); the form-factor's proven seller (364 sold) is **Disney-branded** — do NOT replicate. Aggregate [UNKNOWN].
- **Item specifics:** Brand: Unbranded · Type: Antenna Topper · Material: PVC/foam · Color: Yellow · Theme: Novelty.
- **Risk:** ⚠️ **VeRO split** — sell ONLY plain generic ducks; any Disney/Donald/Daisy duck = Disney VeRO takedown + account risk. Thin demand = impulse/novelty volume play; best margin headroom of the list.

### #4 — Disposable Mascara Wands / Eyelash Spoolies (Bulk)
- **eBay title:** `300 Pcs Disposable Mascara Wands Eyelash Brush Spoolies Applicator Makeup Tool Bulk`
- **Category:** Health & Beauty › Makeup › Eyes › Eyelash Tools / Makeup Tools & Accessories
- **Cost:** $3.18 (100pc) / $4.99 (300pc) [OBSERVED — AutoDS Marketplace; 100pc id `B081RM9B2M`, 300pc id `B089Q6Q7BG`]
- **Suggested sell:** $9.99 → **margin 50.6% / profit $5.05** (use the $3.18 cost tier; bundle to defend price)
- **Demand:** [OBSERVED] one eBay 50-pc listing shows **529 sold**; "Unbranded (1,406)" dominates supply (ebay.com/sch render, 2026-06-16) — **passes ≥200 lower-bound**. Aggregate [UNKNOWN].
- **Item specifics:** Brand: Unbranded · Type: Mascara Wand/Spoolie · Use: Eyelash/Brow · Qty: 100/300.
- **Risk:** **very high competition + $1.99 price floor** → margin is fragile if you chase the floor; win on pack size/bundle, not undercutting. VeRO low (avoid naming Chanel/Clinique/etc.).

### #5 — Smart WiFi Plug (Alexa & Google compatible)
- **eBay title:** `Smart WiFi Plug Socket Outlet Works with Alexa & Google App Voice Control Timer Mini`
- **Category:** Home & Garden › Smart Home › Smart Plugs
- **Cost:** $5.49 [OBSERVED — AutoDS Marketplace, supplier AliExpress (TNCE), id `1005006597670357` → https://www.aliexpress.com/item/1005006597670357.html]
- **Suggested sell:** $16.99 → **margin 51.7% / profit $8.79** (US single-plug; thin at the $12-14 floor)
- **Demand:** [OBSERVED] eBay tuya-plug listings show **85 / 34 / 22 sold**, ~562 active (ebay.com/shop/tuya-smart-plug via jina, 2026-06-16). Aggregate [UNKNOWN].
- **Item specifics:** Brand: Unbranded · Connectivity: WiFi 2.4GHz · Compatibility: Alexa/Google Assistant · Type: Smart Plug · Region: US (verify US plug + voltage).
- **Risk:** ⚠️ **highest compliance load** — powered US electrical device (UL/FCC), do NOT title as bare "Tuya" (trademark) → use "works with Tuya/Smart Life app", and don't reuse Alexa/Google logos. Source the **US-plug** variant (the captured SKU is EU).

---

## 6. RISK FLAGS (cross-cutting)
- **VeRO / brand:** biggest trap across the board. Generic = safe; the *highest-selling* listings are often branded (Disney duck 364, Nike socks, branded cosmetics) → **do not borrow brand equity**. Avoid trademarks in titles even "compatible-with" (Invisalign, Tuya, Apple Watch). Use **own photos** (supplier stock photos can trigger image-copyright VeRO).
- **Margin fragility:** the cheap commodities (mascara wands, toilet covers, smart plug, door sensor) sit **right on the 50% line** and collapse if you chase eBay's price floor. Margin holds only at the **mid/upper** observed sell price + bundling. Items #10-14 fall below 50% at observed costs.
- **Seasonality (mid-June):** OFF-peak now → Christmas dog bandana, winter dog coat, diamond painting, massage guns (all Q4/winter). IN-peak now → meat thermometers, cooling mats, fishing/bike/camping, trunk organizers, trampoline accessories.
- **Compliance beyond VeRO:** electronics (smart plug, door sensor, smart watch) = UL/FCC + honest assistant-compatibility; cosmetics (eyeliner, lash tools) = ingredient/safety; kids toys (bow & arrow, torso) = CPSIA/choking + projectile restrictions; apparel (dog coat, socks) = sizing/returns friction.
- **Shipping weight:** anatomy torso, dumbbells, duffle = bulky/heavy → AutoDS shipping can erase margin; verify supplier ship cost/weight before listing.
- **Evidence gaps:** aggregate eBay sold = [UNKNOWN] everywhere (403 wall) → **before committing budget, re-pull eBay sold + a current AliExpress/AutoDS supplier quote** for the chosen SKUs (jina was rate-limited; retry off-peak). The AutoDS curated "winning products" view needs the paid Product Finding Hub add-on to deepen this.

## 7. Recommended shortlist (risk-adjusted, launchable in June)
**Best 3 to validate first:** (1) **Phone anti-lost tether** — highest margin, proven per-listing demand, lowest risk, lightest ship; (2) **3D anatomy torso (kids)** — passes ≥200-sold lower-bound, ~59% margin, low VeRO (watch ship weight); (3) **Disposable mascara wands** — massive demand (529 sold), low VeRO, but defend margin via bundle. Hold seasonal items (dog coat, Christmas bandana) for Q4.

> **Nothing here is approved for listing.** Import/publish/pricing remain behind their GO gates (`GO_IMPORT_5_DRAFTS`, `GO_PUBLISH_5`). Next read-only step before any GO: re-pull eBay sold counts + live supplier costs for the top 3 (the eBay 403 wall today made aggregate demand [UNKNOWN]).

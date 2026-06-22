---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: profitability_model
status: complete (internal analysis — NO live action)
risk_class: INTERNA
date: 2026-06-22
created_real: 2026-06-22
method: deterministic unit-economics model built ONLY on OBSERVED account numbers (autods_status_report 2026-06-16) + margin canon (PROFITABILITY_VS_COMPETITION 2026-06-17). All projections labeled [ESTIMATE]; base sample = 1 week / 3 orders = LOW-SAMPLE.
measurement_criterion: net profit/day and net profit/month vs the OBSERVED baseline ($8.86/day · ~$268/mo gross). No new metric introduced.
---

# Profitability model — short / mid / long term (2026-06-22)

> **Mission (INTERNA).** Owner intent: "diventare profittevole col dropshipping, calcola breve/medio/lungo, al dettaglio." This is a projection from REAL account data. Nothing is published, priced, ordered or spent. Live levers (resubscribe, buyer account, wallet, import, publish) are flagged GO-CLASS but NOT executed here.

## 0. Baseline OBSERVED (the only hard numbers we own)
[OBSERVED — autods_status_report 2026-06-16]
| Metric | Value | Derived |
|---|---|---|
| Orders last 7d | **3** | 0.43 orders/day |
| Revenue last 7d | **$320** | AOV = **$106.67** |
| Profit last 7d | **$62** | profit/order = **$20.67** · net margin = **19.4%** |
| Lifetime orders | 23 (since catalog import 2025-12-18, ~26 wks) | lifetime avg ~0.88/wk → last week (3) = **~3.4× the lifetime average** (ramp OR noise — LOW-SAMPLE) |
| Active listings | 214 (+11 drafts) | velocity = **0.014 orders/listing/week** → each listing sells ~1× every **71 weeks** |
| **Baseline daily profit** | — | **$8.86/day gross** ($62/7) |

**Realized margin ≠ profile.** Profile is set to 27% markup-on-cost; that's ~21% margin-on-sale, ~19.4% net after FVF (13.6% + $0.40). Model the business on **~19% net today**, not 27%.

## 1. The three profit drivers (what the math actually depends on)
`Weekly profit = Orders/week × Profit/order` · `Profit/order = AOV × net margin`
- **N — productive listings** (today: 214 listing → only ~3 sales/wk; most are dead weight)
- **v — velocity** (orders per listing per week; today 0.014 — the real bottleneck)
- **p — profit/order** (today $20.67; AliExpress sourcing + differentiated bundles → $30–40 range per the margin canon)

The lever with the most slack is **velocity × better products**, then **margin via sourcing**. Adding random listings (N) without velocity just grows dead weight.

## 2. Projections — 3 horizons × 3 scenarios  [ESTIMATE — LOW-SAMPLE base]
Math is mechanical; the **assumptions** are the uncertain part. Net = gross profit − ~$30/mo AutoDS (eBay store fees not modeled separately; FVF already in margin).

### SHORT — 0–3 months (assumes blockers fixed in ~2 wks: resubscribe + buyer account + wallet)
| Scenario | Orders/wk | Profit/order | Net profit/mo | Net profit/day |
|---|---|---|---|---|
| Conservative | 3 → 5 | $20 | **~$400** | ~$13 |
| **Base** | 3 → 10 | $22 | **~$900** | ~$30 |
| Optimistic | 3 → 18 | $25 | **~$1,900** | ~$63 |

*Driver: clean catalog (remove OOS/VeRO), publish the 3 verified winners (jar opener / trunk organizer / grooming kit), restock proven winners (Dog Water Ramp).*

### MEDIUM — 3–6 months (sourcing partly shifted to AliExpress → margin up; winners scaled)
| Scenario | Orders/wk | Profit/order | Net profit/mo | Net profit/day |
|---|---|---|---|---|
| Conservative | 8 | $22 | **~$700** | ~$23 |
| **Base** | 20 | $28 | **~$2,300** | ~$77 |
| Optimistic | 40 | $32 | **~$5,400** | ~$180 |

### LONG — 6–12 months (AliExpress sourcing dominant → ~50% margin; multiple winners; auto-order functional)
| Scenario | Orders/wk | Profit/order | Net profit/mo | Net profit/day |
|---|---|---|---|---|
| Conservative | 15 | $25 | **~$1,500** | ~$50 |
| **Base** | 40 | $32 | **~$5,200** | ~$175 |
| Optimistic | 90 | $38 | **~$14,000+** | ~$480 |

**Daily-profit ladder (the "ogni giorno sempre di più" target):** $8.86 today → **$30/day** (short, base) → **$77/day** (medium, base) → **$175/day** (long, base).

## 3. Blockers that cap EVERY scenario (GO-CLASS — owner only)
1. **AutoDS trial EXPIRED 2026-06-18** (4 days ago). With no plan, scaling tooling is off. → decide upgrade (~$29.90/mo Starter).
2. **Auto-order NON-FUNCTIONAL** — ON but **0 buyer accounts + $0 wallet**. Orders can't auto-fulfill; today every sale needs manual ordering. → connect 1 buyer account + fund wallet.
3. **Sourcing = the margin ceiling.** Amazon→eBay caps at ~30–42% net (we realize ~19%); AliExpress/CJ on the same niches → 50%+ **and** drops the retail-arbitrage policy risk. This single lever moves profit/order from $20 → $35+.
4. **Catalog health** — OOS / On-Hold / supplier-title-changed listings + 1 VeRO draft ("alcohol"). Dead/at-risk listings drag velocity and risk policy hits.

## 4. The honest data gap ("ai migliaia di dati")
This model rests on **aggregate** weekly numbers (3 orders). True data-driven scaling needs the **granular pull**: per-listing views/impressions/sold, per-order realized margin, per-product velocity across the 214 listings. That's a Playwright **read** run (read-only path is OPERATIONAL) — it turns this LOW-SAMPLE estimate into a per-SKU decision engine (which listings to kill, restock, or scale). **Recommended next data step.**

## 5. Recommended path (sequenced, impact-first)
1. **[GO] Resubscribe AutoDS + connect buyer account + fund wallet** — without this nothing scales.
2. **[INTERNA, can run now] Granular read pull** of the 214 listings → kill/restock/scale list (the per-SKU data).
3. **[INTERNA→GO] Shift sourcing to AliExpress** on the verified winners → margin 19% → 35–50%.
4. **[GO] Publish the 3 verified winners** + restock proven winners; cut dead/VeRO listings.
5. **Re-measure weekly** against the baseline ($8.86/day) — same criterion, no metric inflation.

## Caveats
- All horizon numbers = **[ESTIMATE]** from a **1-week / 3-order** base = **LOW-SAMPLE**; treat as direction, not forecast. Re-baseline after the granular pull.
- Profit/order growth assumes the sourcing shift actually lands; if sourcing stays Amazon-only, cap profit/order at ~$20–25 and halve the medium/long net figures.
- No eBay store-subscription / promoted-listings ad cost modeled — add when those decisions are made.

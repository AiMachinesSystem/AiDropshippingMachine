---
machine: "eBay / AutoDS Dropshipping Machine"
type: analysis_report
module: 10_OUTPUTS
status: complete
date: 2026-06-15
created_real: 2026-06-15
phase: analysis_only
external_access: none
live_changes: none
strategy: none
recommendations: none
inputs: "02_DATA collected 2026-06-15 (cleaned tables + raw notes + data-quality/source/missing notes + owner_context)"
---

# Analysis — eBay.com/US + AutoDS Policy / Fee / Feature (2026-06-15)

> **ANALYSIS ONLY.** Interpretation/classification of already-collected data. No new research, no logins, no
> strategy, **no recommendations**, no product selection, **no profitability/margin math**. Stops before Strategy.
> **Evidence grades:** A = official eBay verbatim+cached · B = official export-mirror (walled-help substitute) ·
> C = AutoDS vendor claim · D = unverified/[PUBLIC RESEARCH REQUIRED]/[UNKNOWN] · DEP = seller-country-dependent.

## 1. Dataset summary
Source: the 2026-06-15 public-research run (21 cached official pages). Coverage:
- **eBay.com / US** policy (dropshipping, IP/VeRO, prohibited items), seller-performance standards, fees (FVF/insertion/store/international/regulatory), returns/MBG, cancellations, shipping/handling, selling limits.
- **AutoDS** (vendor): eBay automation features, supported channels/suppliers, plan pricing (USD), and AutoDS's restatement of eBay dropshipping policy.
- **Owner context (USER-PROVIDED):** buyer market = US only / eBay.com / USD; **seller registration country + physical location UNKNOWN**; eBay/AutoDS/suppliers NOT CONNECTED; no business data.
Boundaries: no competitor/product/supplier-price/market-demand data (out of the collection GO). Account-specific data absent (no login).

## 2. Evidence quality assessment
- **Strong (A):** eBay.com FVF schedule, per-order fee, store tiers, international-fee tables, returns/MBG/cancellation/handling windows, selling-limit mechanics — fetched verbatim from official eBay pages and cached; cold-verified traceable.
- **Moderate (B):** seller-performance thresholds (defect ≤2%, cases ≤2/0.3%, late-ship ≤3%, Top-Rated entry) — from official **export.ebay.com** mirrors because www.ebay.com `/help/` pages were a fetch wall; numerically consistent but should be re-confirmed verbatim from the live US help pages.
- **Vendor (C):** all AutoDS capability/pricing facts and AutoDS's eBay-policy statements — single vendor source; the policy restatement aligns with eBay's own text (A) but AutoDS is not the primary authority.
- **Unverified (D):** US flat international fee (1.65%), +5% Below-Standard/INAD surcharge, Promoted Listings ad-rate, exact starter selling-limit counts, eBay.it/EU localized schedule, AutoDS EUR pricing — WebSearch-only or not captured; never treated as observed.
- **Freshness:** all dated 2026-06-15; eBay/AutoDS fees & policies change (a Feb-2025 FVF change was noted as context). Re-verify before any action.
- **Overall:** sufficient as a **policy/fee/feature reference baseline**; insufficient for economics (no supplier costs, no confirmed binding seller schedule).

## 3. Policy constraint map (constraints, not actions)
| Constraint | Rule (as collected) | Grade |
|---|---|---|
| Retail-arbitrage prohibition | Sourcing from another retailer/marketplace that ships directly to the buyer is **prohibited**, any margin | A |
| Allowed model | Own-inventory or wholesale-supplier agreement; seller-of-record on documentation | A |
| Delivery responsibility | Seller liable for safe delivery within stated timeframe + buyer satisfaction even when dropshipping | A |
| Enforcement exposure | end/cancel listings · search demotion · rating cut · selling restrictions · loss of protections · suspension · fees non-refundable | A |
| IP / VeRO | rights-owner IP reporting; infringing listing removal; repeat → restriction/suspension | A |
| Prohibited/restricted items | some categories restricted/banned (country/state-law dependent) | A |
| AutoDS alignment | AutoDS restates the same allowed/prohibited split, names penalties incl. MC011 | C |

**Conclusion (analysis):** the policy regime treats the *sourcing channel* (wholesale vs retail-arbitrage) and *seller-of-record + delivery duties* as the binding compliance axes; these are buyer-market/marketplace-level and apply now on eBay.com.

## 4. Fee / margin pressure map (factors only — NO margins computed)
| Fee/cost factor | As collected (eBay.com/US) | Pressure lever | Grade |
|---|---|---|---|
| Final value fee | most categories 13.6% of total sale (item+ship+handling+tax) | scales with gross sale incl. shipping/tax | A |
| Per-order fee | $0.30 (≤$10) / $0.40 (>$10) | fixed per order — heavier on low-price items | A |
| Category variance | e.g. Books/Music 15.3%, Jewelry 15%/9%, Athletic Shoes 8% (≥$150) | FVF differs sharply by category | A |
| Store subscription | $7.95–$349.95/mo; lowers FVF to ~12.7% (most cat.) + bigger free-listing allotment | fixed cost vs FVF reduction tradeoff | A |
| Insertion | 250 free/mo then $0.35 (no store) | listing-volume cost | A |
| International fee | applies on cross-border; EU-seller table 0%–3.3% | **DEP** on seller registration country | A/DEP |
| Regulatory operating fee | 0.35% on UK/EU listing sites incl. eBay.it | **DEP** on seller's listing site | A/DEP |
| Below-Standard surcharge | "higher final value fees" if Below Standard; reported +5% INAD surcharge | account-health-linked cost | A (qual.) / D (the 5%) |
| Promoted Listings | exists; ad-rate mechanics not captured | optional ad cost | D |

**Conclusion (analysis):** margin pressure stacks **FVF % + fixed per-order + category rate + (seller-country) international/regulatory fees + account-health-linked surcharges**. The *binding* total cannot be fixed because (a) the seller-country-dependent fees are unresolved (DEP) and (b) supplier costs were out of scope. **No profitability inference is possible or attempted.**

## 5. AutoDS feature / limitation map
| eBay operational need (from §3/§6/§7) | AutoDS capability claimed | Limitation / caveat | Grade |
|---|---|---|---|
| Avoid out-of-stock cancellations (=defect) | hourly supplier price/stock monitoring | vendor claim; effectiveness/latency unverified; depends on supplier coverage | C |
| Upload valid tracking within handling time | automated tracking-number updates (24/7) | vendor claim; carrier validity not guaranteed by AutoDS | C |
| Ship within handling time | automated fulfillment / Orders Processor (auto-order) | add-on; actual ship speed depends on supplier | C |
| Listing volume vs selling limits | bulk import / 1-click listing; plan caps (eBay Starter = 400 products) | plan-capped; cost scales with cap | C |
| Repricing within margin guardrails | auto price optimization / charm pricing | vendor claim; guardrail behavior not analyzed (no economics) | C |
| Compliance support | "Fulfilled by AutoDS", overselling prevention; suggests wholesale suppliers | AutoDS asserts compliance — **not eBay-confirmed**; many listed suppliers are retailers (Amazon/Walmart) | C |
| Cost | Import 200 $19.90/mo → Master 100K; eBay Starter ≈$29.90/mo; add-ons separate | USD only; EUR + Luca's plan unknown | C / DEP |

**Limitations (analysis):** every AutoDS fact is single-vendor (C); AutoDS's supplier catalogue is **retailer-heavy**, which is in direct tension with eBay's retail-arbitrage prohibition (§3); pricing is USD/placeholder and plan-capped; "compliance" is a vendor assertion, not an eBay confirmation.

## 6. Dropshipping risk map (eBay.com), classified
| Risk | Basis | Evidence | Dependency |
|---|---|---|---|
| **Retail-arbitrage policy breach** | prohibition (§3) vs AutoDS retailer-heavy suppliers (§5) | A (policy) + C (supplier list) | sourcing-channel choice |
| **Out-of-stock cancellation → defect** | supplier stock volatility vs defect-on-cancel rule | A | supplier reliability |
| **Late-shipment breach (≤3% TRS)** | supplier handling/ship time vs eBay handling-time + late-ship metric | A | supplier + handling-time set |
| **Tracking-upload shortfall** | valid-tracking requirement vs supplier tracking quality | A | supplier tracking |
| **Return/refund cost & defect** | seller pays return shipping for not-as-described; MBG windows | A | supplier returns + product quality |
| **IP / VeRO takedown** | VeRO program + counterfeit/replica exposure | A | product/listing choice |
| **Account-health cascade** | Below-Standard → search demotion, limit cuts, funds held, higher FVF | A | aggregate of above |
| **Vendor-compliance overreliance** | acting on AutoDS's policy claims without eBay confirmation | C/D | verification gap |

**Conclusion (analysis):** the structural risks of eBay dropshipping concentrate where **third-party supplier behavior meets eBay's seller-side liability** (stock, ship speed, tracking, returns) — and the single highest *policy* risk is the sourcing channel given AutoDS's retailer-heavy catalogue. (Stated as risk classification only — no mitigation recommended.)

## 7. Account-health risk map
| Standard (eBay.com) | Threshold | Dropshipping exposure | Grade |
|---|---|---|---|
| Transaction defect rate | ≤ 2% | out-of-stock cancels + unresolved cases feed this | B |
| Cases closed w/o resolution | ≤ 2 or ≤ 0.3% | slow supplier/return handling | B |
| Late-shipment rate (TRS) | ≤ 3% | supplier ship latency | A/B |
| Top Rated entry | ≥90d, ≥100 tx, $1,000 US/12mo | volume/time gate | B |
| Below-Standard effects | search demotion, reduced limits, ad-tools blocked, funds held, higher FVF | compounding revenue+cashflow effect | B |

**Conclusion (analysis):** thresholds are **tight relative to dropshipping's structural cancellation/late-ship exposure**; the consequences are self-reinforcing (a health drop simultaneously cuts visibility, capacity, cashflow, and raises fees). Evidence is B (mirror) for the exact numerics → flagged for verbatim re-confirmation.

## 8. Buyer-market vs seller-country dependency map (the key split)
| Item | Applies NOW (buyer market = US / eBay.com) | DEPENDS on seller country (UNKNOWN) |
|---|---|---|
| Dropshipping / IP / prohibited-items policy | ✔ marketplace-level | — |
| Returns/MBG, cancellations, handling-time rules, selling-limit mechanics | ✔ marketplace-level | — |
| Seller-performance standards/thresholds | ✔ as eBay.com program | exact program may differ if seller registered on a non-US site → DEP |
| FVF base schedule (13.6% etc.) | ✔ as the eBay.com marketplace reference | which schedule **binds** the account (US-registered vs not) → DEP |
| International / cross-border seller fee | — | ✔ DEP (e.g. non-US seller shipping to US buyers) |
| Regulatory operating fee (0.35%) | — | ✔ DEP (applies if listing on eBay.it/EU/UK) |
| Taxes / VAT / payout / payment rules | — | ✔ DEP |

**Conclusion (analysis):** **policy + buyer-experience rules are fixed now; the fee/tax/payment economics cannot be pinned until seller registration country is known.** This is the single largest analytical dependency.

## 9. Missing data / blockers (before Strategy)
- **USER INPUT NEEDED:** seller registration country + physical location (largest); eBay account store-tier/level/limits/health; AutoDS plan/add-ons/currency; intended product category; target margin & business data.
- **PUBLIC RESEARCH REQUIRED:** seller-country fee schedule (if non-US); verbatim US help-page numerics (fetch wall); exact late-ship volume gate / Below-Standard FVF uplift / US flat international fee / +5% INAD / Promoted Listings rate / starter-limit counts; AutoDS EUR pricing; eBay primary policy confirmation vs AutoDS restatement.
- **Out of scope (not collected):** competitor listings, product demand, supplier prices/stock/terms → no economics or product feasibility possible.

## 10. Analysis conclusions (only — no actions)
1. The eBay.com policy regime is **clear and binding now**: retail arbitrage prohibited, wholesale/owned allowed, seller is seller-of-record and liable for delivery/satisfaction [A].
2. The **dominant compliance tension** is structural: AutoDS's supplier catalogue is retailer-heavy [C] while eBay prohibits retail-arbitrage sourcing [A].
3. **Account-health thresholds are tight** versus dropshipping's inherent cancellation/late-ship/return exposure, with self-reinforcing penalties [A/B].
4. **Fee pressure is multi-component**; the *binding* fee/tax/payment economics are **undetermined** until seller country is known [A + DEP].
5. **AutoDS evidence is entirely single-vendor [C]** and its compliance claims are not eBay-confirmed.
6. The dataset is **sufficient to frame strategy constraints but not to model economics or select products** (no supplier costs, no confirmed schedule, no product data).
7. The largest single unblocker is **confirming seller registration country**; the second is supplier/economic data (a separate future GO).

## 11. Strategy gate status
**CLOSED.** Strategy requires explicit owner authorization AND the missing inputs in §9 (at minimum seller country + supplier/economic data). This report performs **no** strategy, recommendations, product selection, or profitability inference. Next phase (Strategy) does not begin without an owner GO.

---
machine: "eBay / AutoDS Dropshipping Machine"
type: cleaned_data_table
module: 02_DATA
topic: eBay selling fees
status: cleaned
date: 2026-06-15
created_real: 2026-06-15
market: "eBay.com (US) unless noted — Luca's market USER INPUT NEEDED"
analysis: none
---

# CLEANED — eBay Selling Fees (2026-06-15)

> Data only, no analysis (no margin/breakeven modelling — that is the Analysis phase).
> **ALL figures = eBay.com (US) schedule unless noted.** Market/category/store-tier/account dependent and
> change over time. Luca's registered eBay site, category, and Store tier = **USER INPUT NEEDED**.
> Source for every [OBSERVED] row: `export.ebay.com` fee pages, cached under `90_CACHE/fetches/ebay.com/` (2026-06-15).

## Final value fee (FVF) — by category (no Store subscription)

| Category | FVF rate | Threshold note | Label | Cache |
|---|---|---|---|---|
| Most categories | 13.6% | up to $7,500/item; 2.35% on portion above | [OBSERVED] | 2026-06-15_final-value-fees.txt |
| Books, Movies & TV, Music | 15.3% | up to $7,500; 2.35% above | [OBSERVED] | _final-value-fees.txt |
| Jewelry & Watches | 15% / 9% | 15% up to $5,000; 9% above | [OBSERVED] | _final-value-fees.txt |
| Athletic Shoes | 8% / 13.6% | 8% if sale ≥$150 (NO per-order fee); 13.6% if <$150 | [OBSERVED] | _final-value-fees.txt |
| Heavy Equipment / Commercial Printing / Food Trucks | 3% | up to $15,000; 0.5% above | [OBSERVED] | _final-value-fees.txt |

- FVF basis: % of **total sale = item + handling + shipping collected + sales tax + other applicable fees** [OBSERVED — _final-value-fees.txt].
- Per-order fixed fee: **$0.30** (order ≤$10) / **$0.40** (order >$10) [OBSERVED — _final-value-fees.txt].

## Insertion fees & Store subscriptions

| Item | Value | Label | Cache |
|---|---|---|---|
| Insertion (no Store) | 250 free listings/month; $0.35/listing beyond | [OBSERVED] | 2026-06-15_seller-fees-export.txt |
| Store FVF — most categories | 12.7% up to $2,500; 2.35% above; + $0.40/order | [OBSERVED] | 2026-06-15_store-subscriptions-fees.txt |
| Store tier price (monthly / yearly-per-month) | Starter $7.95/$4.95 · Basic $27.95/$21.95 · Premium $74.95/$59.95 · Anchor $349.95/$299.95 · Enterprise –/$2,999.95 | [OBSERVED] | _store-subscriptions-fees.txt |
| Store zero-insertion allotment (fixed-price, all categories) | Basic 1,000 · Premium 10,000 · Anchor 25,000 · Enterprise 100,000 | [OBSERVED] | _store-subscriptions-fees.txt |

## International / regulatory fees (relevant to EU/Italy listing)

| Item | Value | Label | Cache |
|---|---|---|---|
| International fee — applies when | buyer delivery OR registered address is outside seller's registered country; % of total sale | [OBSERVED] | 2026-06-15_international-fees.txt |
| Intl fee — EU-registered seller | Eurozone & Sweden 0% · UK 1.2% · Europe-other / USA / Canada 1.6% · all other 3.3% | [OBSERVED] | _international-fees.txt |
| Intl fee — non-EU unsited seller | Japan 1.35% · S.Korea 1.45% · India 1.70% · NZ 1.00% · Rest APAC 1.30% · Europe-unsited 1.30% · RoW 1.55% | [OBSERVED] | _international-fees.txt |
| Regulatory operating fee | **0.35% fixed** on listings on UK + EU sites **including Italy (eBay.it)** & Switzerland (since 8 Apr 2024); +VAT where applicable | [OBSERVED] | _international-fees.txt |

## Flagged / unverified (NOT captured verbatim from a fetched page → do not treat as confirmed)
- US-registered seller international fee **1.65%** (single flat rate) — WebSearch summary; ebay.com/help id=5224 timed out → [PUBLIC RESEARCH REQUIRED].
- Below-Standard / "Item not as described" **+5%** FVF surcharge (category-level, when INAD rate "Very High") — WebSearch summary → [PUBLIC RESEARCH REQUIRED].
- Promoted Listings ad rate (Standard % / Priority CPC mechanics) — not captured → [PUBLIC RESEARCH REQUIRED].
- Reported Feb 14 2025 FVF increase (up to +0.35% most categories) — context only; values above are the export.ebay.com figures live on 2026-06-15.
- Managed-payments payment-processing line (bundled vs separate) — not captured verbatim → [PUBLIC RESEARCH REQUIRED].
- **eBay.it / EUR fee schedule** for Luca's actual market — [PUBLIC RESEARCH REQUIRED] + market confirmation USER INPUT NEEDED.

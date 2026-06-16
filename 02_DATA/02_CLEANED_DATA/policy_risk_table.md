---
machine: "eBay / AutoDS Dropshipping Machine"
type: cleaned_data_table
module: 02_DATA
topic: eBay policy + operational constraints (factual register)
status: cleaned
date: 2026-06-15
created_real: 2026-06-15
analysis: none
note: "Factual constraint register. NOT a risk assessment/diagnosis — that is the Analysis phase. No scoring, no recommendations."
---

# CLEANED — eBay Policy & Operational-Constraint Register (2026-06-15)

> Data only: the rules a seller must operate within, as stated on official pages. **No risk scoring, no
> recommendations, no application to Luca's account** (Analysis phase). Sources cached under
> `90_CACHE/fetches/` (2026-06-15). Market caveat applies throughout: figures are eBay EN/US/export-mirror text;
> Luca's governing eBay site (eBay.it/eBay.co.uk/eBay.com) = **USER INPUT NEEDED**. Full raw: `01_RAW_DATA/policies/`.

## 1. Dropshipping & sourcing policy
| Rule | Detail | Label |
|---|---|---|
| Allowed | Own item before listing OR wholesale-supplier agreement; fulfill from wholesale supplier; seller-of-record on docs | [OBSERVED — eBay] |
| Prohibited | Buy from another **retailer/marketplace** that ships directly to your buyer (retail arbitrage) — regardless of margin | [OBSERVED — eBay] |
| Seller duty | Responsible for safe delivery within stated timeframe + buyer's overall satisfaction even when dropshipping | [OBSERVED — eBay] |
| Enforcement | End/cancel listings · hide/demote in search · lower rating · buying/selling restrictions · loss of protections · suspension · fees non-refundable | [OBSERVED — eBay] |
| AutoDS restatement | Same allowed/prohibited split; cites **MC011** restriction + suspension (vendor source — verify vs eBay primary) | [OBSERVED — AutoDS] |

## 2. IP / prohibited items
| Rule | Detail | Label |
|---|---|---|
| VeRO | Rights owners report IP infringement, counterfeit/fakes/replicas, unauthorized copyrighted content | [OBSERVED — eBay] |
| IP enforcement | Infringing listing removed + notice; repeat/continued → restrictions/suspension | [OBSERVED — eBay] |
| Prohibited/restricted items | Policy exists; some categories restricted/banned (country/state-law dependent); violations → remove/warn/restrict/suspend | [OBSERVED — eBay] |

## 3. Seller performance / account-health thresholds
| Metric | Threshold | Window | Label |
|---|---|---|---|
| Seller levels | Top Rated / Above Standard / Below Standard | evaluated 20th of month | [OBSERVED — eBay] |
| Lookback | 3 months if ≥400 sales in prior 3 mo; else 12 months | — | [OBSERVED — eBay] |
| Transaction defect rate | ≤ 2% (minimum standard) | per window | [OBSERVED — eBay] |
| Cases closed w/o seller resolution | ≤ 2, or ≤ 0.3% (higher applies) | per window | [OBSERVED — eBay] |
| Late shipment rate (Top Rated) | ≤ 3% | per window | [OBSERVED — eBay] |
| Defect triggers | out-of-stock/unexpected seller cancellation; case closed without resolution | — | [OBSERVED — eBay] |
| Top Rated entry (US program) | account ≥90 days; ≥100 transactions + $1,000 US sales / 12 mo | — | [OBSERVED — eBay] |
| Below Standard effects | lower search · reduced limits · ad-tools blocked · funds held until tracked · higher FVF | — | [OBSERVED — eBay] |

## 4. Returns / Money Back Guarantee
| Rule | Detail | Label |
|---|---|---|
| Seller return options | No returns · 30/60-day · buyer-paid or free | [OBSERVED — eBay] |
| Free returns | seller pays return shipping, any reason, no restocking fee | [OBSERVED — eBay] |
| Refund timing | 2 business days after receiving return (else eBay auto-refunds) | [OBSERVED — eBay] |
| MBG — Not Received | open up to 30 cal days after est. delivery; full item + shipping refund | [OBSERVED — eBay] |
| MBG — Not As Described | report ≤30 cal days (or seller window if longer); **seller pays return shipping** | [OBSERVED — eBay] |
| MBG — seller response | within 3 business days or eBay may step in | [OBSERVED — eBay] |

## 5. Cancellations
| Rule | Detail | Label |
|---|---|---|
| Buyer cancel window | up to 60 min after commit | [OBSERVED — eBay] |
| Seller cancel reasons | buyer-asked (pre-ship) · no payment · wrong address · out of stock | [OBSERVED — eBay] |
| **Out-of-stock cancel** | = transaction defect, affects Seller Level | [OBSERVED — eBay] |
| Seller response/init windows | respond to buyer cancel ≤3 cal days; seller-init ≤30 cal days after sale | [OBSERVED — eBay] |
| Misuse | false non-payment etc. → suspension/restrictions/rating cuts/fees | [OBSERVED — eBay] |

## 6. Shipping / handling
| Rule | Detail | Label |
|---|---|---|
| Handling time | business days from payment to carrier acceptance scan | [OBSERVED — eBay] |
| 1-day handling | acceptance scan by next day 11:59:59 p.m. local | [OBSERVED — eBay] |
| Recommendation | ≤ 2 days handling | [OBSERVED — eBay] |
| On-time protection | shipped within handling time + acceptance scan + valid tracking | [OBSERVED — eBay] |

## 7. Selling limits
| Rule | Detail | Label |
|---|---|---|
| Existence | all new sellers have a selling limit | [OBSERVED — eBay] |
| Drivers | account age, identity, registered address, site, performance, sales history, item-type risk | [OBSERVED — eBay] |
| Review | monthly auto-adjust on sales volume + feedback; active+sold+GTC count | [OBSERVED — eBay] |
| At-limit effect | cannot add listings / raise prices until listings end or next month | [OBSERVED — eBay] |

> **Not collected / flagged:** exact late-ship % minimum-volume gate, Below-Standard FVF uplift %, US 1.65% intl fee, +5% INAD fee, Promoted Listings ad rate, exact starter-limit numbers → [PUBLIC RESEARCH REQUIRED] (see missing-data log). eBay.it/EU localized text → [PUBLIC RESEARCH REQUIRED] + Luca's site USER INPUT NEEDED.

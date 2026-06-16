---
machine: "eBay / AutoDS Dropshipping Machine"
type: raw_source_notes
module: 02_DATA
topic: AutoDS features / suppliers / pricing / eBay-policy guidance
status: raw
date: 2026-06-15
created_real: 2026-06-15
collection: public_web_readonly
analysis: none
source_class: "AutoDS-official (vendor). eBay-policy items = AutoDS restatement, NOT eBay primary text."
---

# RAW — AutoDS Features / Pricing / Policy Guidance (2026-06-15)

> Raw capture, facts only. `[OBSERVED — autods url, 2026-06-15 (cache: 90_CACHE/fetches/autods.com/...)]`.
> All AutoDS-official (vendor) sources. **eBay-policy statements here are AutoDS's restatement of eBay policy, not eBay's
> own page** → confirm against eBay primary policy. Prices USD, plan/channel-dependent, change over time. Luca's plan = **USER INPUT NEEDED**.

## eBay automation features
| Fact | Value | Label | Cache |
|---|---|---|---|
| Product finding/import: 1-click listing (single/bulk variations), Products importer, marketplace (page: 800M+ products). | import/1-click | [OBSERVED] | 2026-06-15_ebay-automation-features.txt |
| Automated price & stock monitoring — "scans suppliers' price and stock changes every hour". | hourly scan | [OBSERVED] | _ebay-automation-features.txt |
| Automatic price optimization + "Psychologic Pricing System" (charm pricing). | repricing | [OBSERVED] | _ebay-automation-features.txt |
| Automated fulfillment ("100% hands-free") / "Automated order workflows" (processing, tracking, returns); auto-ordering = Orders Processor add-on. | auto-fulfillment | [OBSERVED] | _ebay-automation-features.txt |
| Automated tracking-number updates (24/7); case management; AI copy editor; bulk changes; poor-product remover. | tracking/support | [OBSERVED] | _ebay-automation-features.txt |

## Channels & suppliers
| Fact | Value | Label | Cache |
|---|---|---|---|
| Supported selling channels. | eBay, Shopify, Facebook Marketplace, Wix, WooCommerce, Etsy, Amazon, TikTok Shop | [OBSERVED] | 2026-06-15_suppliers-and-channels.txt |
| Supported suppliers (sourcing). | AliExpress, Amazon, Walmart, Alibaba, CJdropshipping, Banggood, Home Depot, eBay, Costco, Wayfair, Target, vidaXL, Overstock, Lowe's, Costway, Sam's Club, Wish, DHgate, Shein, Macy's, Kohl's, Cdiscount + more | [OBSERVED] | _suppliers-and-channels.txt |
| Help Center: 33 product-upload suppliers w/ regional variants; **Italy region** supported for Alibaba, AliExpress, Amazon, CJ Dropshipping, Costway, DHgate, eBay-Supplier. Walmart US-only. | regional map | [OBSERVED] | 2026-06-15_product-upload-supported-suppliers-regions.txt |

> Note (data, not analysis): many listed suppliers are **retailers/marketplaces** (Amazon, Walmart, Target, Costco…) — see eBay retail-arbitrage prohibition in the policy table. Recording the fact only.

## Pricing (USD, from AutoDS Help Center billing article; live pricing page rendered placeholders)
| Plan | Price | Cap | Label | Cache |
|---|---|---|---|---|
| Import 200 (all channels) | $19.90/mo annual ($26.90 monthly); Amazon ch. $49.90/$64.90 | 200 product variations | [OBSERVED] | 2026-06-15_subscription-pricing-addons.txt |
| Starter (eBay = "Starter 400") | $29.90/mo annual ($39.90 monthly); Amazon ch. $69.90/$89.90 | 400 products (eBay) | [OBSERVED] | _subscription-pricing-addons.txt |
| Advanced 800–1K | $49.90–$69.90/mo annual; Amazon ch. up to $119/mo | 800–1,000 | [OBSERVED] | _subscription-pricing-addons.txt |
| Higher tiers | up to "Master 100K"; $106–$2,787/mo by channel; annual up to 25% off | scales w/ cap | [OBSERVED] | _subscription-pricing-addons.txt |
| Add-ons | Orders Processor $9.90/mo · Product Finding Hub $14.97/mo · Mentorship $39.97/mo · VA Users $14.97/mo · Create UGC $39.90/mo · Bundle $55/mo | separate billing | [OBSERVED] | _subscription-pricing-addons.txt |
| Trial | $0.99 / 3-day (public page: "$1, 3-day"), per channel, non-refundable | trial | [OBSERVED] | _subscription-pricing-addons.txt |

## AutoDS restatement of eBay dropshipping policy (vendor source — verify vs eBay primary)
| Fact | Value | Label | Cache |
|---|---|---|---|
| AutoDS says ALLOWED: wholesale agreements + third-party fulfillment of owned inventory, seller-of-record on invoices/packing slips, deliver in promised timeframe. | allowed | [OBSERVED] | 2026-06-15_ebay-dropshipping-policy-guidance.txt |
| AutoDS says PROHIBITED: retail arbitrage (buy from Amazon/Walmart after sale, ship to customer); selling items you don't own/can't sell. Penalties incl. removed listings, **MC011 account restriction**, suspension. | prohibited | [OBSERVED] | _ebay-dropshipping-policy-guidance.txt |
| AutoDS supplier guidance: be seller of record; use wholesale/private-label (names CJdropshipping, Alibaba, Wholesale2B); claims compliance support via auto-fulfillment, tracking, overselling-prevention, "Fulfilled by AutoDS". | guidance | [OBSERVED] | _ebay-dropshipping-policy-guidance.txt |

## Unverified / flagged
- AutoDS EUR pricing for Italy; Luca's actual plan/add-ons → USER INPUT NEEDED / [PUBLIC RESEARCH REQUIRED].
- Live pricing page (autods.com/pricing) rendered "$__" placeholders → figures from Help Center article instead; reconfirm live → [PUBLIC RESEARCH REQUIRED].
- AutoDS's eBay-policy claims are vendor restatement; **eBay.it/EU primary policy NOT fetched** → [PUBLIC RESEARCH REQUIRED].
- Whether "Fulfilled by AutoDS"/AliExpress/CJ sourcing is compliant on Luca's eBay.it/EU site — AutoDS asserts, not eBay-confirmed → [PUBLIC RESEARCH REQUIRED].
- autods.com/ebay-dropshipping/ and /supported-suppliers/ returned HTTP 404.

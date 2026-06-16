---
machine: "eBay / AutoDS Dropshipping Machine"
type: owner_context
module: 02_DATA
status: active
date: 2026-06-15
created_real: 2026-06-15
label: USER-PROVIDED CONTEXT
analysis: none
---

# Owner Context — US Buyer-Market Selection (USER-PROVIDED CONTEXT)

> Recorded as **USER-PROVIDED CONTEXT** (owner statement, not researched, not analysed). Saved 2026-06-15.
> Stop after saving. No external data, no analysis, no strategy.

## Provided by owner (Luca)
| Field | Value | Label |
|---|---|---|
| Owner name | Luca | USER-PROVIDED CONTEXT |
| Primary eBay marketplace | eBay.com | USER-PROVIDED CONTEXT |
| Target **buyer** market | United States only | USER-PROVIDED CONTEXT |
| Secondary eBay marketplace | NONE | USER-PROVIDED CONTEXT |
| Primary operating currency (research reference) | USD | USER-PROVIDED CONTEXT |
| eBay account access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| AutoDS access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| Supplier access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| Current business data | NOT PROVIDED YET | USER-PROVIDED CONTEXT |

## Still open (NOT provided)
| Field | Label |
|---|---|
| Seller **account registration country** | USER INPUT NEEDED |
| Seller **physical location** | USER INPUT NEEDED |

## CRITICAL DISTINCTION (binding interpretation rule for this machine)
- **Confirmed:** the business sells to the **United States buyer market only**, on **eBay.com**, with **USD** as the research reference currency. → eBay.com / US is the correct **marketplace and buyer-market reference** for all future work.
- **NOT confirmed / do NOT assume:** that the **seller is located in the US**, or that **US seller fee/tax/payment rules apply to Luca's account**. The seller account registration country and physical location are **UNKNOWN**.
- Therefore, **seller-location-dependent** items remain unresolved and labelled accordingly:
  - Which fee schedule actually **binds** the account (US-registered vs non-US-registered seller selling on eBay.com) → USER INPUT NEEDED / PUBLIC RESEARCH REQUIRED.
  - **International / cross-border seller fee** applicability (e.g. a non-US seller shipping to US buyers) → USER INPUT NEEDED.
  - **Taxes / VAT / payment-payout rules** tied to seller country → USER INPUT NEEDED / PUBLIC RESEARCH REQUIRED.
  - eBay **regulatory operating fee** (applies to listings on eBay.it/EU/UK sites) → applicability depends on the seller's listing site, still unconfirmed.

## Effect on already-collected data (2026-06-15 research)
- The eBay.com (US) fee/policy figures in `02_DATA/02_CLEANED_DATA/` are now the **correct buyer-market/marketplace reference**.
- They are **NOT yet confirmed as the binding seller-side schedule** for Luca's account until seller registration country is known. Keep that caveat on any fee figure used for the account.

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

# Owner Context — US Buyer-Market + US Seller (USER-PROVIDED CONTEXT)

> Recorded as **USER-PROVIDED CONTEXT** (owner statement, not researched, not analysed).
> Saved 2026-06-15; updated 2026-06-15 with seller country/location. No external data, no analysis, no strategy.

## Provided by owner (Luca)
| Field | Value | Label |
|---|---|---|
| Owner name | Luca | USER-PROVIDED CONTEXT |
| Primary eBay marketplace | eBay.com | USER-PROVIDED CONTEXT |
| Target **buyer** market | United States only | USER-PROVIDED CONTEXT |
| Secondary eBay marketplace | NONE | USER-PROVIDED CONTEXT |
| **Seller account registration country** | **United States** | USER-PROVIDED CONTEXT |
| **Seller physical location** | **United States** | USER-PROVIDED CONTEXT |
| Primary operating currency | USD | USER-PROVIDED CONTEXT |
| Italy / EU context | NOT RELEVANT unless explicitly reintroduced by owner | USER-PROVIDED CONTEXT |
| eBay account access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| AutoDS access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| Supplier access | NOT CONNECTED | USER-PROVIDED CONTEXT |
| Current business data | NOT PROVIDED YET | USER-PROVIDED CONTEXT |

## Resolved (2026-06-15)
- Seller registration country + physical location = **United States** → previously "USER INPUT NEEDED", now provided.
- **Italy / EU seller context is dropped** (NOT RELEVANT) unless the owner explicitly reintroduces it later.

## Binding interpretation (direct consequence of the provided context — NOT analysis)
- The scenario is **US-registered seller → US buyers on eBay.com** (a US-domestic setup, USD).
- The eBay.com (US) fee/policy data in `02_DATA/02_CLEANED_DATA/` is now the **binding seller-side reference**, not merely a buyer reference.
- Items previously marked **seller-country-DEPENDENT** now resolve to the **US seller** context. Re-deriving the analysis's dependency conclusions (e.g. which previously-DEP fees apply) is deferred to the **Analysis Delta** next step — **not performed here**.
- eBay.it / EU localized schedule and EU-seller international-fee table = **NOT RELEVANT** for this machine going forward.

## Still open (account-specific — USER INPUT NEEDED / for later phases)
| Field | Label |
|---|---|
| eBay account: store tier, seller level, selling limits, account health, payment/account settings | USER INPUT NEEDED |
| AutoDS: plan/add-ons/settings | USER INPUT NEEDED |
| Suppliers, product category, target margins, business/economics data | USER INPUT NEEDED |
| Exact US-seller fee/tax/payment specifics not captured verbatim (walled US-help numerics) | PUBLIC RESEARCH REQUIRED |

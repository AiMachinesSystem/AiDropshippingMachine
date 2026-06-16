---
machine: "eBay / AutoDS Dropshipping Machine"
type: data_map
module: 02_DATA
status: initialized
date: 2026-06-15
external_collection: not_started
---

# Data Map — eBay / AutoDS Dropshipping Machine

## Data Rule

Data must be collected before analysis, strategy, execution, measurement, learning, or scaling.

No data below has been collected yet. This file defines required data only.

## Required Data Types

| Data Type | Source | Purpose | Storage Location | Update Frequency | Data Quality Risks | Used By Module |
|---|---|---|---|---|---|---|
| eBay account data | eBay Seller Hub / owner export | Understand account type, marketplace, limits, status, business policies, store structure | 02_DATA/01_RAW_DATA/eBay_account_raw.md and 02_DATA/02_CLEANED_DATA/eBay_account_cleaned.md | Initial + weekly after launch | USER INPUT NEEDED; LIVE ACCESS REQUIRED if not owner-provided; account data may be incomplete | System, Data, Analysis, Strategy, Measurement |
| eBay account health data | eBay Seller Hub account health / performance dashboard | Detect suspension/defect/late shipment/cancellation risk | 02_DATA/01_RAW_DATA/account_health_raw.md and 06_MEASUREMENT/account_health_reports/ | Weekly; daily if warning signal appears | USER INPUT NEEDED; metrics may depend on current eBay definitions; PUBLIC RESEARCH REQUIRED | Measurement, Learning, Scaling |
| AutoDS data | AutoDS dashboard / owner export | Understand connected store, automation settings, supplier setup, repricing, order automation, tracking | 02_DATA/01_RAW_DATA/autods_raw.md and 02_DATA/02_CLEANED_DATA/autods_cleaned.md | Initial + weekly after setup | USER INPUT NEEDED; LIVE ACCESS REQUIRED; automation settings may change | System, Execution, Measurement |
| Supplier data | Supplier platforms, AutoDS supplier list, owner input | Validate stock reliability, price stability, shipping times, return terms, tracking quality | 02_DATA/01_RAW_DATA/supplier_raw.md and 02_DATA/02_CLEANED_DATA/supplier_cleaned.md | Initial + weekly for active suppliers | Public terms may be stale; supplier stock/price changes quickly; PUBLIC RESEARCH REQUIRED | Data, Analysis, Strategy, Execution, Measurement |
| Product research data | AutoDS product finder, eBay search, Terapeak/product tools if available, supplier catalogs | Identify candidate SKUs before validation | 02_DATA/01_RAW_DATA/product_research_raw.md and 02_DATA/02_CLEANED_DATA/product_research_cleaned.md | Per research cycle | Demand signals may be incomplete; sales estimates may be tool-dependent; avoid assuming profitability | Data, Analysis, Strategy |
| Competitor listing data | eBay search results, competitor listings | Compare titles, images, prices, shipping, returns, sold signals if visible, trust signals | 02_DATA/01_RAW_DATA/competitor_listings_raw.md and 02_DATA/02_CLEANED_DATA/competitor_listings_cleaned.md | Per research cycle; refresh before listing | Public data cannot prove profit, conversion, or true volume | Data, Analysis, Strategy |
| Pricing data | eBay listings, supplier cost, AutoDS pricing rules, fee calculators | Build margin model and price guardrails | 02_DATA/02_CLEANED_DATA/pricing_table.md | Before listing + weekly for active SKUs | Fees/discounts/taxes/shipping may be missing; PUBLIC RESEARCH REQUIRED | Analysis, Strategy, Execution, Measurement |
| Fee data | eBay fee pages/calculators, payment fee sources, AutoDS plan costs | Calculate gross and net margin | 02_DATA/02_CLEANED_DATA/fee_table.md | Initial + monthly/policy change | Current fees require verification; market/category dependent | Analysis, Strategy, Measurement |
| Shipping data | Supplier shipping estimates, AutoDS shipping settings, eBay business policy, tracking sources | Control late shipment, tracking, customer expectation risk | 02_DATA/02_CLEANED_DATA/shipping_table.md | Before listing + weekly for active SKUs | Delivery estimates may change; tracking compatibility may vary | Analysis, Execution, Measurement |
| Return/refund data | eBay return settings, supplier return terms, owner policy, customer cases | Control refund, defect, and margin risk | 02_DATA/02_CLEANED_DATA/returns_refunds_table.md | Initial + monthly + after incident | Policy mismatch risk; current policy requires verification | Strategy, Execution, Measurement, Learning |
| Policy/risk data | eBay policy pages, AutoDS documentation, supplier terms | Prevent prohibited workflows, account risk, policy mismatch | 02_DATA/00_SOURCE_DISCOVERY/policy_source_plan.md and 02_DATA/02_CLEANED_DATA/policy_risk_table.md | Before strategy + monthly refresh | PUBLIC RESEARCH REQUIRED; cannot use memory | System, Analysis, Strategy, Execution |
| Performance data | eBay Seller Hub, AutoDS orders, owner reports | Measure revenue, margin, conversion, orders, cancellations, returns, tracking, defects | 06_MEASUREMENT/kpi_reports/ | Daily after launch; weekly summary | USER INPUT NEEDED; data may be delayed or incomplete | Measurement, Learning, Scaling |
| Customer message data | eBay messages / owner export | Detect objections, listing confusion, service load | 02_DATA/01_RAW_DATA/customer_messages_raw.md and 07_LEARNING/customer_objections.md | Weekly after launch | PII must be excluded/redacted; LIVE ACCESS REQUIRED if not owner-provided | Learning, Execution, Strategy |
| Customer feedback/review data | eBay feedback, product reviews, competitor review sources | Understand trust signals, complaints, defects, supplier/product issues | 02_DATA/01_RAW_DATA/reviews_feedback_raw.md and 02_DATA/02_CLEANED_DATA/reviews_feedback_cleaned.md | Per research cycle + weekly for own account | Public reviews may not represent all buyers; avoid overgeneralization | Data, Analysis, Learning |
| Order fulfillment data | AutoDS order records, supplier order records, eBay orders | Measure handling time, shipping time, tracking upload, supplier failures | 06_MEASUREMENT/fulfillment_reports/ | Daily after orders exist | Requires access/export; supplier records may not align with eBay data | Measurement, Learning, Scaling |
| Automation error data | AutoDS logs, owner incident notes | Detect repricing, stock sync, order, tracking, or mapping errors | 07_LEARNING/automation_errors.md | After each incident + weekly | Error logs may be incomplete; owner notes needed | Learning, Execution, Scaling |

## Data Handoff Requirements

Before Analysis can begin:

- Raw and cleaned data must be separated.
- Source list must be documented.
- Missing data must be logged.
- Data quality risks must be documented.
- Account-specific assumptions must be avoided.
- Owner must authorize Analysis.

---
machine: "eBay / AutoDS Dropshipping Machine"
type: kpi_map
module: 06_MEASUREMENT
status: initialized_foundation
date: 2026-06-15
measurement_status: not_started
---

# KPI Map — eBay / AutoDS Dropshipping Machine

## Measurement Rule

KPIs must be measured before learning and scaling.
Exact numeric thresholds are not invented here. Where account/platform limits are needed, mark `USER INPUT NEEDED` or `PUBLIC RESEARCH REQUIRED`.

| KPI | Formula | Data Source | Frequency | Decision Threshold | Related Phase |
|---|---|---|---|---|---|
| Revenue | Sum of completed eBay order revenue for period | eBay Seller Hub / order export | Daily after launch; weekly report | USER INPUT NEEDED: owner revenue target; do not use revenue alone for scaling | Measurement |
| Gross Profit | Revenue minus supplier product cost minus supplier shipping cost minus marketplace/payment fees where available | eBay orders + supplier cost + fee table + AutoDS/order records | Per order + weekly | Must be positive per SKU before scale consideration; exact minimum target USER INPUT NEEDED | Measurement, Scaling |
| Net Margin | Net profit divided by revenue | eBay orders + supplier cost + shipping + fees + AutoDS/software costs + refunds | Weekly/monthly | Owner minimum margin required; USER INPUT NEEDED | Measurement, Scaling |
| Order Volume | Count of completed orders in period | eBay Seller Hub / AutoDS orders | Daily/weekly | Growth signal only if margins and account health are stable | Measurement |
| Sell-Through Rate | Units sold divided by active listing quantity or available listing exposure basis | eBay listing/order data | Weekly | PUBLIC RESEARCH REQUIRED / USER INPUT NEEDED depending data availability | Analysis, Measurement |
| Listing Conversion Rate | Orders divided by listing views or sessions | eBay Seller Hub traffic/listing data | Weekly | USER INPUT NEEDED baseline; low conversion triggers listing review, not scaling | Measurement, Learning |
| Cancellation Rate | Cancelled orders divided by total orders | eBay Seller Hub / AutoDS orders | Daily/weekly | Must remain within current eBay/account-safe limits; PUBLIC RESEARCH REQUIRED | Measurement, Scaling Gate |
| Late Shipment Rate | Late shipments divided by total shipments | eBay Seller Hub account health / orders | Daily/weekly | Must remain within current eBay/account-safe limits; PUBLIC RESEARCH REQUIRED | Measurement, Scaling Gate |
| Return Rate | Returned orders divided by delivered orders | eBay returns / seller hub | Weekly/monthly | Rising trend triggers product/supplier/listing review; exact threshold USER INPUT NEEDED | Measurement, Learning |
| Defect Rate | Defective transactions divided by total transactions using current eBay definition | eBay account health | Weekly | Must remain within current eBay/account-safe limits; PUBLIC RESEARCH REQUIRED | Measurement, Scaling Gate |
| Tracking Upload Rate | Orders with valid tracking uploaded on time divided by shipped orders | eBay Seller Hub / AutoDS tracking logs | Daily/weekly | Must be high enough to protect account health; exact eBay requirement PUBLIC RESEARCH REQUIRED | Measurement, Scaling Gate |
| Supplier Failure Rate | Supplier-related failures divided by supplier-attempted orders | AutoDS orders + supplier issue log | Weekly | Any repeated supplier failure blocks scaling for that supplier until resolved | Measurement, Learning, Scaling |
| Account Health Status | Current status/level/warnings from eBay account health | eBay Seller Hub | Daily if warning; weekly otherwise | Must be healthy/stable before scaling; current account status USER INPUT NEEDED | Measurement, Scaling Gate |
| Average Handling Time | Sum of order handling times divided by shipped orders | eBay orders + AutoDS + supplier timestamps | Daily/weekly | Must fit listing promise and account health requirements; policy/account limits PUBLIC RESEARCH REQUIRED | Execution, Measurement |
| Customer Message Response Time | Average time from buyer message to first response | eBay messages / owner log | Daily/weekly | Must remain inside owner capacity and platform expectations; exact benchmark USER INPUT NEEDED/PUBLIC RESEARCH REQUIRED | Execution, Measurement, Scaling |

## KPI Handoff Rules

| Result | Handoff |
|---|---|
| KPI stable and profitable | Measurement → Learning |
| KPI unstable or risky | Measurement → Learning + Execution fix |
| KPI validated across SKU/supplier/workflow | Learning → Scaling Gate review |
| KPI missing or unreliable | Return to Data |

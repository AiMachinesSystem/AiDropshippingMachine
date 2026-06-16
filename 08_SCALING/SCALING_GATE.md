---
machine: "eBay / AutoDS Dropshipping Machine"
type: scaling_gate
module: 08_SCALING
status: closed
date: 2026-06-15
scaling_status: forbidden_until_validation
---

# Scaling Gate — eBay / AutoDS Dropshipping Machine

## Core Rule

Scaling is forbidden until Measurement validates the result.

## Scaling Readiness Requirements

All conditions must pass before any scaling decision:

| Requirement | Status Now | Evidence Needed |
|---|---|---|
| Profitable SKU performance | Not validated | Revenue, gross profit, net margin, fee/shipping/refund-adjusted data |
| Stable supplier performance | Not validated | Supplier failure rate, late shipment rate, stock stability, tracking success |
| Acceptable cancellation rate | Not validated | eBay order/account health data; current thresholds PUBLIC RESEARCH REQUIRED |
| Acceptable late shipment rate | Not validated | eBay account health/order data; current thresholds PUBLIC RESEARCH REQUIRED |
| Acceptable return/refund rate | Not validated | Return/refund data and owner target |
| Acceptable defect rate | Not validated | eBay account health data; current thresholds PUBLIC RESEARCH REQUIRED |
| Healthy account status | USER INPUT NEEDED | eBay Seller Hub account health |
| Repeatable fulfillment workflow | Not validated | Fulfillment SOP executed and measured |
| Controlled customer support load | Not validated | Message response time, open cases, owner capacity |
| Automation stability | Not validated | AutoDS error logs, tracking upload rate, repricing incidents |
| Rollback option defined | Not created | Scaling plan with stop condition |
| Owner approval | Not granted | Explicit owner approval |

## Allowed Scaling Types Later

| Scaling Type | Allowed Only If |
|---|---|
| Add more quantity/listings for winning SKU pattern | SKU is profitable, supplier stable, account health healthy |
| Add related SKUs | Winning product pattern is validated and supplier/category risk controlled |
| Add new supplier | Supplier validation passes and current supplier dependency risk is high |
| Increase automation | Manual workflow is stable and errors are low |
| Increase listing volume | Account limits, health, support capacity, and fulfillment process are stable |
| Expand categories | Data and analysis validate category opportunity; policy risk reviewed |
| Outsource support/operations | Support load measured and SOPs are stable |

## Stop / Rollback Triggers

| Trigger | Action |
|---|---|
| Account health warning | Pause scaling review; return to Measurement/Learning |
| Rising cancellation rate | Freeze affected SKU/supplier; investigate |
| Rising late shipment rate | Freeze affected SKU/supplier; investigate |
| Supplier failure repeat | Remove supplier from scaling candidates |
| Margin below owner threshold | Stop SKU scaling; review pricing |
| Return/refund spike | Stop SKU/category scaling; review product/listing |
| Automation errors repeat | Disable scaling of automation workflow until fixed |
| Support load exceeds capacity | Stop catalog/listing volume expansion |

## Handoff

Scaling → New Data Cycle only after:

1. Scaling decision is approved.
2. Monitoring plan is defined.
3. Rollback trigger is defined.
4. Owner GO is explicit for any live action.

---
machine: "eBay / AutoDS Dropshipping Machine"
type: execution_gate_structure
module: 05_EXECUTION
status: gate_defined_not_authorized
date: 2026-06-15
execution_status: not_authorized
---

# Execution Gate Structure — eBay / AutoDS Dropshipping Machine

## Rule

Execution plans may be created later only after:

1. Required data exists.
2. Analysis is authorized and completed.
3. Strategy is authorized and approved.
4. Owner authorizes execution planning.
5. Every SOP includes measurement links.
6. Live platform action remains blocked until explicit owner GO.

## Future Execution Plans / SOPs

| SOP / Execution Plan | Purpose | Required Inputs | Output | Measurement Link | Current Status |
|---|---|---|---|---|---|
| AutoDS Setup SOP | Define safe setup workflow for store connection, suppliers, monitoring, templates, repricing, and automation settings | Approved strategy, AutoDS account data, policy/source verification, owner GO for live changes | Step-by-step setup checklist | Automation error count; tracking upload rate; supplier failure rate | Gate defined only |
| eBay Listing SOP | Define listing creation workflow: title, category, item specifics, images, price, shipping, returns, compliance check | Product data, competitor data, fee/margin model, policy verification | Listing draft workflow | Listing conversion rate; return rate; defect rate | Gate defined only |
| Product Research SOP | Define how candidate products are researched and scored | Source plan approval, product research sources, competitor listings, supplier data | Candidate SKU table | Sell-through rate; gross profit; return rate | Gate defined only |
| Supplier Validation SOP | Define supplier reliability, stock, price, shipping, tracking, return validation | Supplier source data, shipping data, return data, owner criteria | Supplier scorecard | Supplier failure rate; late shipment rate; cancellation rate | Gate defined only |
| Pricing / Repricing SOP | Define pricing floor, margin model, fee inclusion, repricing guardrails | Fee table, supplier cost, competitor price, owner margin target | Pricing rule and review checklist | Gross profit; net margin; price-change incidents | Gate defined only |
| Order Fulfillment SOP | Define order review, supplier order placement, tracking upload, exception handling | AutoDS order settings, supplier workflow, eBay order data | Fulfillment checklist | Average handling time; tracking upload rate; late shipment rate | Gate defined only |
| Customer Service SOP | Define response handling, message categories, escalation rules, tone, response SLA | eBay messages, customer objections, policy/returns info | Response workflow and templates | Customer response time; case count; defect rate | Gate defined only |
| Return / Refund SOP | Define return request, refund, supplier return compatibility, documentation, escalation | eBay return policy, supplier return terms, owner rules | Return/refund workflow | Return rate; refund rate; defect rate | Gate defined only |
| Account Health Monitoring SOP | Define daily/weekly account health checks and stop actions | eBay account health data, KPI Map, policy thresholds | Monitoring checklist | Account health status; defect rate; cancellation rate; late shipment rate | Gate defined only |
| Daily / Weekly Operations Checklist | Define recurring operating rhythm | Active listings, orders, messages, AutoDS alerts, account health | Daily/weekly checklist | All operational KPIs | Gate defined only |

## Live Action Lock

Even after execution SOPs are created, the following remain locked until explicit owner GO:

- Publishing eBay listings.
- Editing live eBay listings.
- Changing prices.
- Changing eBay policies/settings.
- Changing AutoDS settings.
- Enabling automation.
- Placing supplier orders.
- Issuing refunds.
- Sending customer messages as owner.

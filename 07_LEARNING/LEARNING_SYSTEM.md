---
machine: "eBay / AutoDS Dropshipping Machine"
type: learning_system
module: 07_LEARNING
status: initialized_foundation
date: 2026-06-15
learning_status: not_started
---

# Learning System — eBay / AutoDS Dropshipping Machine

## Rule

Learning begins only after Measurement produces results or after owner provides incident/performance context.
Learning records must improve future Data, Analysis, Strategy, Execution, Measurement, or Scaling.

## Learning Record Categories

| Category | What To Record | Source | Output File |
|---|---|---|---|
| Winning product patterns | SKU/category/listing/supplier traits linked to profitable measured performance | KPI reports, product data, order data | 07_LEARNING/winning_product_patterns.md |
| Failed product patterns | Traits linked to low conversion, losses, returns, cancellations, support issues | KPI reports, returns, cancellations, messages | 07_LEARNING/failed_product_patterns.md |
| Supplier issues | Stock, price, shipping, tracking, quality, return, or order issues | Supplier logs, AutoDS errors, customer cases | 07_LEARNING/supplier_issues.md |
| Listing mistakes | Title, image, item specifics, policy, expectation, category, or copy issues | Listing performance, messages, returns, defects | 07_LEARNING/listing_mistakes.md |
| Pricing mistakes | Margin failure, repricing error, competitor mismatch, fee omission | Pricing reports, AutoDS logs, fee table | 07_LEARNING/pricing_mistakes.md |
| Policy risks | Warnings, removals, compliance ambiguity, account health impact | Account health, policy research, platform warnings | 07_LEARNING/policy_risks.md |
| Customer objections | Repeated buyer questions, complaints, confusion, trust objections | eBay messages, feedback, returns | 07_LEARNING/customer_objections.md |
| Operational errors | Fulfillment, tracking, automation, customer service, return handling mistakes | AutoDS logs, order logs, owner notes | 07_LEARNING/operational_errors.md |
| Reusable SOP improvements | Workflow changes that reduce errors or improve KPIs | Measurement + incident learning | 07_LEARNING/sop_improvements.md |

## Learning Entry Schema

| Field | Required |
|---|---|
| Date | Yes |
| Source action | Yes |
| Source KPI/report | Yes |
| What happened | Yes |
| Evidence label | Yes |
| Affected module | Yes |
| KPI impact | Yes |
| Root cause | Yes if known |
| Prevention rule | Yes for errors |
| Repeatability condition | Yes for wins |
| SOP update needed | Yes/No |
| Scaling relevance | Validated only |

## Learning Handoff Rules

| Condition | Handoff |
|---|---|
| Repeated error pattern | Learning → Execution fix |
| Missing evidence | Learning → Data |
| Validated success pattern | Learning → Scaling Gate review |
| Policy uncertainty | Learning → Data Source Discovery / Public Research approval |
| Supplier failure | Learning → Supplier Validation update |

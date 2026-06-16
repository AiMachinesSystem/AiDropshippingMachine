---
machine: "eBay / AutoDS Dropshipping Machine"
type: risk_map
module: 03_ANALYSIS
status: initialized_foundation
date: 2026-06-15
analysis_status: not_authorized
---

# Risk Map — eBay / AutoDS Dropshipping Machine

## Rule

This is a risk control foundation, not a current account diagnosis.
No live data has been collected.
Policy-specific details are `PUBLIC RESEARCH REQUIRED`.

| Risk | Cause | Impact | Early Warning Signal | Prevention Rule | Measurement KPI |
|---|---|---|---|---|---|
| eBay policy risk | Dropshipping workflow, supplier model, listing content, tracking, shipping, or return process may conflict with current eBay rules | Listing removal, account restriction, reduced visibility, suspension risk | Policy warning, listing takedown, account notification, increased defects | Verify current eBay policies before strategy/execution; no policy assumptions from memory | Account health status; policy warning count; listing removal count |
| Supplier reliability risk | Supplier cannot consistently fulfill, ship, track, or maintain quality | Late shipments, cancellations, refunds, negative feedback, defects | Supplier stock instability, delayed dispatch, tracking gaps, customer complaints | Validate supplier before listing; maintain supplier failure log; avoid unvalidated supplier scaling | Supplier failure rate; late shipment rate; cancellation rate; return rate |
| Late shipment risk | Handling time mismatch, supplier delay, automation delay, inaccurate shipping promise | Defects, buyer complaints, negative feedback, account health damage | Orders pending beyond handling time; supplier delay notices; tracking not uploaded | Only list SKUs with verified handling/shipping reliability; monitor daily after launch | Late shipment rate; average handling time; tracking upload rate |
| Tracking risk | Supplier does not provide acceptable tracking or AutoDS/eBay tracking sync fails | Buyer disputes, defects, account health issues, support load | Missing tracking, invalid tracking, tracking uploaded late, AutoDS sync errors | Validate tracking availability before listing; monitor tracking upload daily | Tracking upload rate; tracking error count; customer message rate |
| Cancellation risk | Out-of-stock, price spike, supplier restriction, automation failure, incorrect listing | Defects, lost revenue, poor buyer experience, account health damage | Stock mismatch, order cannot be fulfilled, supplier price change, AutoDS stock sync warning | Use stock monitoring; block SKUs with unstable stock; define cancellation prevention checklist | Cancellation rate; out-of-stock incident count; supplier failure rate |
| Out-of-stock risk | Supplier inventory changes faster than listing/AutoDS sync | Cancellations, delayed fulfillment, customer dissatisfaction | Supplier stock status changes, AutoDS stock warning, sudden sales spike | Validate stock stability; monitor active SKU stock; avoid low-stock suppliers | Out-of-stock incident count; cancellation rate |
| Price change risk | Supplier price changes, shipping cost changes, eBay fees change, AutoDS repricing fails | Margin compression, losses, incorrect prices | Supplier price increase, repricing error, margin below floor | Set price floor and margin guardrail before listing; monitor supplier price changes | Gross profit per order; net margin; price-change incident count |
| Return/refund risk | Product mismatch, quality issue, buyer remorse, supplier return limitations, policy mismatch | Profit loss, disputes, support load, negative feedback | Return requests, refund requests, repeated product complaints | Align eBay return promise with supplier reality; define return/refund SOP before launch | Return rate; refund rate; return reason frequency |
| Account suspension risk | Accumulated defects, policy violations, late shipments, cancellations, poor service metrics | Business interruption, frozen growth, loss of channel access | Account health warnings, seller level decline, restriction notice | Monitor account health; stop risky SKU/supplier before threshold breach; require policy verification | Account health status; defect rate; late shipment rate; cancellation rate |
| Margin compression risk | Competition lowers price, supplier cost rises, fees/shipping higher than expected | Unprofitable orders, cash drain, scaling failure | Net margin below target, competitor undercutting, fee/shipping variance | No SKU launch without margin model; define minimum margin rule | Gross profit; net margin; fee variance; shipping cost variance |
| Automation error risk | AutoDS mapping, stock sync, repricing, order automation, tracking upload, or template error | Wrong price, wrong item, failed order, late tracking, customer issue | AutoDS alerts, unusual price changes, failed automation logs | Review automation settings before enabling; no live config without owner GO; maintain error log | Automation error count; failed order automation count; repricing incident count |
| Customer service risk | Buyer questions, complaints, shipping confusion, returns, product mismatch | Response delays, defects, negative feedback, support overload | Message volume spike, repeated objections, unresolved cases | Define customer service SOP before launch; monitor response time | Customer message response time; open case count; feedback score/status |

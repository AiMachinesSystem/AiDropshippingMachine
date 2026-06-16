---
machine: "eBay / AutoDS Dropshipping Machine"
type: approval_gate_register
module: 00_SYSTEM_CONTROL
status: active
date: 2026-06-15
---

# Approval Gates — eBay / AutoDS Dropshipping Machine

| Action Type | Allowed Now? | Approval Required | Notes |
|---|---:|---|---|
| Internal foundation setup | Yes | No | Current task scope |
| Create/update internal Markdown files | Yes | No | No external accounts touched |
| Define data requirements | Yes | No | Planning only |
| Define source discovery plan | Yes | No | No collection |
| Public web research | No | Owner approval required | Must be explicitly authorized |
| eBay policy verification | No | Owner approval required | Mark `PUBLIC RESEARCH REQUIRED` until approved |
| AutoDS feature/policy verification | No | Owner approval required | Mark `PUBLIC RESEARCH REQUIRED` until approved |
| Read eBay Seller Hub | No | Owner approval + access required | Read-only collection only |
| Read AutoDS dashboard | No | Owner approval + access required | Read-only collection only |
| Read supplier accounts | No | Owner approval + access required | Read-only collection only |
| Export account data | No | Owner approval required | Owner may provide export manually |
| Create strategy | No | Owner must approve Analysis → Strategy gate | Requires data and analysis first |
| Create execution plans/SOPs beyond gate structure | No | Owner must approve Strategy → Execution gate | This initialization only defines future SOPs |
| Change eBay settings | No | Explicit owner GO required | Live platform write |
| Publish/edit listings | No | Explicit owner GO required | Live platform write |
| Change AutoDS settings | No | Explicit owner GO required | Live platform write |
| Place supplier order | No | Explicit owner GO required | Money/live action |
| Issue refund/return decision | No | Explicit owner GO required | Money/customer action |
| Scale SKU/catalog/automation | No | Measurement validation + owner approval required | Scaling currently forbidden |

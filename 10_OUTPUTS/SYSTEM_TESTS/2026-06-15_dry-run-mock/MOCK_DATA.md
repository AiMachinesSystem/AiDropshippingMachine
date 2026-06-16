---
machine: "eBay / AutoDS Dropshipping Machine"
type: mock_test_data
module: 10_OUTPUTS/SYSTEM_TESTS
status: mock
date: 2026-06-15
created_real: 2026-06-15
DATA_CLASS: "MOCK DATA / NOT REAL"
isolation: "test-only; MUST NOT be copied into 02_DATA / 03_ANALYSIS or treated as business evidence"
---

# ⚠️ MOCK DATA / NOT REAL — Dry-Run Test Scenario (2026-06-15)

> **EVERY item below is FABRICATED for a system gate-test. NOT real. NOT business evidence.**
> Do not mix with real data. Do not act on it. Scenario deliberately includes policy/supplier/health
> stressors to exercise the machine's risk flags and gates.

| # | Mock item | MOCK value (NOT REAL) |
|---|---|---|
| 1 | **MOCK eBay account status** | Seller "MOCK-SELLER-01"; buyer market eBay.com/US; **seller registration country = Germany (MOCK)**; store = none; level = Above Standard (MOCK); defect 1.2%, late-ship 2.1% (MOCK baseline) |
| 2 | **MOCK AutoDS plan/settings** | Plan = Advanced 800 (MOCK); Orders Processor add-on ON; eBay.com store connected (MOCK); auto-repricing ON; auto-tracking ON |
| 3 | **MOCK supplier profile** | "MOCK-SUPPLIER FastShipCN"; channel = AliExpress-type; ship-from China; handling 2d; delivery 12–20d; stock volatility = MEDIUM; tracking validity = INTERMITTENT (MOCK) |
| 4 | **MOCK product candidate** | "MOCK LED Galaxy Projector"; **sourced by AutoDS from Amazon US (a retailer) (MOCK)**; variant count 3 |
| 5 | **MOCK competitor listing snapshot** | "MOCK-COMP-01" sells equivalent at $24.99, free 30-day returns, 1-day handling, "500 sold" (MOCK) |
| 6 | **MOCK pricing inputs** | supplier cost $18.50; intended price $24.99; shipping = free to buyer; eBay fees apply (FVF 13.6% + $0.40); seller=DE → intl + regulatory fees apply (MOCK inputs) |
| 7 | **MOCK order** | Order #MOCK-TEST-0001; item = MOCK Galaxy Projector; $24.99; US buyer (MOCK) |
| 8 | **MOCK shipment/tracking event** | Tracking uploaded on **day 3** (AFTER the 2-day handling window) → LATE; carrier-validated (MOCK) |
| 9 | **MOCK return/refund case** | INAD case #MOCK-RET-0001 "item not as described"; seller pays return shipping (MOCK) |
| 10 | **MOCK customer message** | "MOCK: Where is my order? 15 days, still not arrived." → Item-Not-Received risk (MOCK) |
| 11 | **MOCK KPI result** | defect rate 2.4% (>2%), late-ship 3.8% (>3%), cancellation 1.1%, INR 1 open, INAD 1 open — **MOCK metrics, NOT real** |
| 12 | **MOCK learning entry** | "MOCK: FastShipCN late shipments correlate with INR cases and the late-ship breach" — **MOCK learning, NOT a real machine learning** |

> **Reminder:** mock KPIs (#11) failing thresholds do NOT make the account "Below Standard" in reality — there is no real account. Mock results are inputs to the gate test only.

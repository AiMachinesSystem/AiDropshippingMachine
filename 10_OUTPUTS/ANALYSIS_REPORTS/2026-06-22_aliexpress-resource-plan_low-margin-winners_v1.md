---
machine: "eBay / AutoDS Dropshipping Machine"
type: aliexpress_resource_plan
date: 2026-06-22
created_real: 2026-06-22
status: DRAFT — BLOCKED at data gate (AliExpress CAPTCHA-wall) · import/order = GO
source: 90_CACHE/fetches/autods/audit_2026-06-22_044324/_products_list.json
---

# AliExpress Re-Source Plan — low-margin proven winners

**Why these:** RUN-03 showed the demand/margin inversion — Pool/Water + Kitchen carry **66% of sales but the thinnest margins**. Re-sourcing them on AliExpress is the **#1 leverage point**: it lifts margin AND removes the Amazon→eBay TBA-tracking suspension risk (~45% of eBay terminations). Survival + profit on the exact SKUs that already sell.

## Targets + cost thresholds
Target = **50% net margin** after eBay FVF (13.6% + $0.30). `AE_max$` = the max AliExpress landed cost that hits that target.

| SKU (winner) | sell $ | now Amazon $ | now margin | **AE max cost $** | margin gain |
|---|---:|---:|---:|---:|---:|
| Deck Jet Pool Fountain Jet | 138 | 96 | 15% | **≤ 50** | +35 pt |
| Dog Water Ramp Boats/Pools | 202 | 135 | 18% | **≤ 73** | +32 pt |
| Inline Chlorine Feeder | 70 | 48 | 15% | **≤ 25** | +35 pt |
| 8.8in PC Display Screen | 117 | 78 | 18% | **≤ 42** | +32 pt |
| Stock Tank Pool Cover 8ft round | 95 | 60 | 21% | **≤ 34** | +29 pt |
| Stock Tank Pool Cover 8ft solar | 70 | 44 | 22% | **≤ 25** | +28 pt |
| Ham Maker Meat Press v1 | 42 | 27 | 20% | **≤ 15** | +30 pt |
| Ham Maker Meat Press v2 | 47 | 30 | 20% | **≤ 17** | +30 pt |

If AliExpress (US-warehouse preferred) lands ≤ these costs, each winner roughly **doubles its margin** AND becomes compliant.

## Generic search terms (VeRO-safe, no brand)
- Deck Jet → `pool fountain jet nozzle inground deck spray fitting`
- Dog Water Ramp → `dog pool ramp pet swim ladder boat dock`
- Chlorine Feeder → `automatic chlorine feeder inline pool chlorinator dispenser`
- PC Display → `mini pc display screen argb usb temp monitor secondary case`
- Stock Tank Cover (round) → `stock tank pool cover round wire rope winch`
- Stock Tank Cover (solar) → `solar stock tank pool cover heavy duty winch`
- Ham Maker (both) → `ham press maker meat press stainless steel deli mold`

## Verify-before-import checklist (skill rule)
For each candidate URL: cost ≥40% below eBay sell · ≥~1000 orders or strong rating · light-to-ship · **real per-unit price (exclude $X.99 first-order trap)** · generic (no brand).

## ⛔ BLOCKER — data gate (Hard Block, not retried-to-death)
AliExpress item pages are **CAPTCHA-walled** (confirmed wall, 3 channels prior). I **cannot read AE costs autonomously** → I cannot verify which candidate hits the `AE_max$` threshold. Two ways forward, **owner-side**:
1. Paste 1 AliExpress URL per target (I extract cost + verify against the table), **or**
2. Open a visible/owner-assisted browser session so the finder can read the pages.

Until then this plan is **structurally complete but cost-unverified**. Next gates after URLs: import as DRAFT = GO · publish = GO · supplier order = GO.

## Measurement
Per SKU: margin now → margin after re-source (target 50%). Catalog effect if all 8 re-sourced: the proven-demand 66%-of-sales block moves from ~18% to ~50% margin = the single biggest $/unit lift available, with suspension risk removed.

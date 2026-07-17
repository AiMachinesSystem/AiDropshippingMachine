---
tags: [machine, research, product-research]
type: report
status: active
date: 2026-07-12
created_real: 2026-07-12
description: "Prima ricerca prodotto WEB-LED (demand-first dal web aperto, non dallo store) su correzione owner 2026-07-12. 6 candidati validati su domanda web + prezzo eBay, filtrati per i nostri gate, con cost-ceiling per net>=$4. Pronti per il gate sourcing."
---

# Web-led demand-first product shortlist — 2026-07-12

> **Metodo nuovo (correzione owner 2026-07-12, memoria `product-research-web-first`):** la domanda si scopre sul **web aperto** (Google Trends/Summergeist Tier1 → eBay trend Tier2 → social Tier3), NON da AutoDS Marketplace/nostro store. Poi si filtra per i nostri gate, poi si mappa al sourcing. Il web trova COSA; lo store è solo il layer di fulfillment.
> **Verdetto:** 6 candidati generici/VeRO-safe/light-ship con domanda in salita reale e margine ≥$4 fattibile. **Non ancora sourced** — prossimo gate = import per leggere il costo reale.

## Evidence tiers (onestà sulle fonti)
- **Tier 1 (fidato) — dato di Google stesso:** `Summergeist 2026` (rising-search). [OBSERVED — blog.google, 2026-07-12]
- **Tier 2 (valida) — eBay stesso:** high-demand guide + Watchlist Trend Report. [OBSERVED — ebay.com, 2026-07-12]
- **Tier 3 (scettico, solo idee) — blog dropship:** sellthetrend/cj/tradelle. I loro "$X profit" = marketing NON verificato, mai citati come margine reale.
- **Prezzo eBay:** range dai listing attivi [OBSERVED — ebay.com, 2026-07-12]. **Sold-velocity esatta = dietro muro 403** → confidenza domanda da trend+densità listing, NON da sold-count. Conferma con `read_ebay_demand.py` (GO-light) prima del batch.
- **Costo fonte:** [ESTIMATE] da prezzo di mercato → **da confermare all'import** (rischio placeholder $133.13/ASIN sbagliato, E-003).

## Shortlist (ranked)

| # | Prodotto (generico) | Segnale domanda | Prezzo eBay [OBS] | Costo est. [EST] | Cost-ceiling net≥$4 | Peso/resi | Conf. |
|---|---|---|---|---|---|---|---|
| 1 | **Toe spacers / separators (gel/silicone, set)** | TikTok 2.5B views, Summergeist viral; evergreen podologia | $14–19 (P=$17.99) | ~$5–8 | **≤$11.07** | light / bassi | **ALTA** |
| 2 | **Dorm shower caddy / back-to-school organizer (mesh portatile)** | Stagionale **AGOSTO back-to-school** (finestra ORA) | $12–20 (P=$18.99) | ~$6–10 | **≤$11.93** | light / bassi | **ALTA** |
| 3 | **Ice roller / cooling globes viso (set 2pz)** | Beauty in salita + cooling estivo; Summergeist | $7–47, core $13–22 (P=$21.99) | ~$8–12 | **≤$14.51** | light / bassi | MED-ALTA |
| 4 | **Tea infuser tumbler insulated (steel)** | "tea infuser tumbler" trend wellness/fibermaxxing | $25–40 (P=$27.99) | ~$12–18 | **≤$19.67** | medio / bassi | MED-ALTA |
| 5 | **Hand grip strengthener — KIT/bundle 3-5pz** | Fitness evergreen + "finger grip" viral | single $9–15 (thin) → **KIT P=$19.99** | ~$6–10 | **≤$12.79** | light / bassi | MED *(solo bundle; single = thin)* |
| 6 | **Yellow-lens sunglasses** | Summergeist: top-trend lente gialla | $10–20 (P=$16.99) | ~$4–8 | **≤$10.21** | light / **resi-fashion + saturo** | WATCH |

## Note per candidato
1. **Toe spacers** — il best pick: virale, cost-to-market largo, light, VeRO-safe, resi bassi (non fashion-sizing). Angolo: multipack + bunion/alignment keyword.
2. **Dorm caddy** — time-sensitive: la domanda BTS picca ad agosto → pubblicare ORA. Angolo: mesh anti-muffa + handle.
3. **Ice globes** — evitare brand (EcoTools/Saian); listare set generico. Angolo: cooling de-puff estivo.
4. **Tea tumbler** — miglior AOV; leggermente più pesante (bottiglia steel). Angolo: insulated "hot for hours" + infuser removibile.
5. **Grip strengthener** — il singolo è thin ($8-15): vale **solo come kit** (grip + finger + wrist) per alzare AOV sopra il floor.
6. **Yellow sunglasses** — trend Tier-1 forte MA prodotto fashion (resi taglia/stile) + saturo + rischio knockoff/VeRO → **watch-list**, non batch.

## Gate & prossimo passo
- **INTERNO fatto:** discovery web + filtro + cost-ceiling. 
- **GO-light (prossimo):** `read_ebay_demand.py` sui top-4 → conferma sell-through reale; poi import ASIN Amazon-US per leggere costo reale ≤ ceiling.
- **GO-CLASS:** import draft (`GO_IMPORT`) → titolo ≤80 + desc riscritta → publish (`GO_PUBLISH`).

## Fonti
- Google Summergeist 2026 · eBay high-demand 2026 · eBay Watchlist Trend Report · Sell The Trend (July 2026) · CJdropshipping (July 2026) · eBay category price ranges (toe spacers/sunglasses/tea tumbler/grip/ice roller/dorm caddy), tutti fetchati 2026-07-12.

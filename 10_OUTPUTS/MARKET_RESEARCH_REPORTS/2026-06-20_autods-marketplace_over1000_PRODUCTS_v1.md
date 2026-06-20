---
machine: "eBay / AutoDS Dropshipping Machine"
type: market_research
status: complete
date: 2026-06-20
created_real: 2026-06-20
description: "Pull dal Marketplace AutoDS (accesso owner-autorizzato) dei prodotti winning con rating_count>1000 (proxy >1000 venduti), sul nostro tema, con categoria · nicchia · recency (data aggiunta) · costo→retail. Read-only via API gw.autods.com."
---

# Prodotti >1000 venduti (AutoDS Marketplace) — 2026-06-20

> Richiesta owner: *"vedi se su tema ci sono prodotti interessanti over 1000 venduti, tabella categoria/nicchia/recenti. Se serve l'accesso sei autorizzato."*
> **Accesso usato (autorizzato):** API Marketplace AutoDS `gw.autods.com/marketplace/api/products/` (POST, Bearer di sessione), read-only.
> **Proxy ">1000 venduti" = `rating_count > 1000`** (recensioni sul source Amazon; di norma il venduto è ≥ recensioni). Sort per popolarità (`spv_param`). 200 prodotti estratti, **170 sul nostro tema**.
> **"Recenti" = data di aggiunta al catalogo AutoDS** (decodificata dall'ObjectId). Realtà del catalogo: 95 del 2021 · 64 del 2022 · 6 del 2023 · **5 del 2025** → i winning AutoDS sono sellers consolidati, pochi nuovi.

## ⚠️ Nota qualità
Molti sono prodotti **branded Amazon** (Yes4All, PetAmi, Dove, IAMS…) = **rischio VeRO** + non ideali per dropship. Sotto privilegio i **generici / no-brand problem-solving**; i branded li escludo o li flaggo `[BRAND]`.

## Tabella — prodotti interessanti >1000 recensioni (curati, ordinati per recency)

| Recenti | Categoria | Nicchia | Prodotto (generico) | Costo→Retail | Note |
|---|---|---|---|---|---|
| **2025-03** | Home & Garden | Storage & Organization | Water Bottle Organizer for Cabinet (2-pack) | $17.99→$39 | recente, organizer cucina |
| **2025-03** | Sports & Fitness | Game Room / Backyard | Trampoline Spring Pull Tool | $3.99→$7 | recente, tool economico |
| 2023-12 | Pets | Dogs | Light-Up LED Dog Collar (rechargeable, reflective) | $12.99→$17.5 | sicurezza cane |
| 2023-12 | Pets | Dogs | Dog Tag Clips 304 Stainless (2-pack) | $12.99→$22 | accessorio leggero |
| 2023-12 | Pets | Fish | Aquarium Bio Sponge Filter (Betta/shrimp) | $6.68→$18 | acquario |
| 2023-12 | Electronics & Gadgets | Computer access. | PU Leather Mouse Pad stitched-edge | $9.99→$17 | desk gadget |
| 2022-11 | Electronics & Gadgets | Desk | Oversized Desk Mat 35.4×15 / Leather Desk Pad | $6.29→$32 | desk mat (trend) |
| 2022-11 | Electronics & Gadgets | Desk | Keyboard Wrist Rest / Ergonomic Pad | $16.99→$25 | ergonomia |
| 2022-07 | Pets | Cats | Cat Water Fountain Filter (16-pack) | $10.99→$33 | ricambio ricorrente |
| 2022-03 | Pets | Cats | Collapsible Travel Dog/Cat Bowls (2-pack) | $5.98→$20 | viaggio pet |
| 2022-03 | Pets | Dogs | Car Seat Protector Non-Slip | $12.99→$38 | auto+pet |
| 2022-03 | Pets | Small Animals | Portable Cat Travel Litter Box (foldable) | $25.99→$43 | viaggio gatto |
| 2022-03 | Home Improvements & Tools | Wood Working | Cabinet Pull Drawer Handles (10-pack, black) | $7.34→$145* | hardware casa (*msrp variante) |
| 2022-03 | Sports & Fitness | Exercise | Hand Grip Strength Trainer | $6.99→$9.8 | fitness economico |
| 2022-03 | Sports & Fitness | Exercise | Pull-Up Assistance Resistance Bands (loop) | $15.95→$31 | fitness |
| 2022-03 | Sports & Fitness | Golf/Agility | Training Traffic Cones 9" (set) | $16.99→$32 | sport outdoor |
| 2022-03 | Electronics & Gadgets | Computer access. | RJ45 Coupler / Ethernet Extender | $3.99→$9 | tech accessorio |
| 2022-02 | Home & Garden | Furniture | MagSafe Charger Stand (15/25W) | $14.99→$21 | tech desk |

\* il "retail" è `max_msrp` (può riferirsi a una variante/quantità superiore) → indicativo, non margine garantito.

## Branded esclusi (visti ma scartati — VeRO)
Yes4All (mace bell, kettlebell, cable attachments), PetAmi (dog backpack/blanket — molti), IAMS, Dove/Aveeno/Hawaiian Tropic (beauty, fuori tema), Retrospec/Primasole yoga mat, NICREW/Pawfly (aquarium brand), Goldenwarm. = prodotti veri e venduti, ma **brand nel titolo = rischio VeRO**, non da copiare.

## Lettura strategica
- Il catalogo "winning >1000 review" AutoDS è dominato da **prodotti consolidati e spesso branded** → conferma la tesi della market research: i mercati facili sono saturi/brandizzati; lo spazio per noi è **generico + angolo**, non copiare il branded.
- I **pochi generici interessanti**: organizer (water bottle/cabinet), desk mat/pad (trend desk-setup), pet-accessori ricorrenti (filtri fontana, collari LED), tool economici. Margine vero da confermare (costo AutoDS reale + fee).
- "Recenti" reali (2025): pochissimi → se vuoi *novità*, meglio la pipeline AliExpress orders-sold (già usata) che cattura i trend freschi, mentre questo catalogo dà i *sellers consolidati*.

## BLOCKERS
- `rating_count` = recensioni (proxy venduto), non venduto eBay; il venduto reale eBay resta da confermare col filtro Sold.
- `max_msrp` può riferirsi a varianti → prezzo retail indicativo.
- Publish bloccato (account eBay) — questa è solo intel.
- Fonte: AutoDS Marketplace API (accesso autorizzato), 200 prodotti, 2026-06-20.

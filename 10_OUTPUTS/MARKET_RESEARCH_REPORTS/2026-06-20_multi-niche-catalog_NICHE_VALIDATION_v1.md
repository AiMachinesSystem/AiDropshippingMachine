---
machine: "eBay / AutoDS Dropshipping Machine"
type: market_research
status: complete
date: 2026-06-20
created_real: 2026-06-20
niche_slug: multi-niche-catalog
run: v1
description: "Censimento di mercato multi-nicchia su tutte le 15 nicchie-prodotto del catalogo (eBay demand + supply density + sold + verdetto PROVEN + spazio). Workflow 30 agenti, dati citati, verifica avversariale qualità-dato. Owner: 'prendi dati e fai una ricerca di mercato' (tutti)."
---

# Market Research — Catalogo multi-nicchia (15 nicchie) — 2026-06-20

> Richiesta owner: *"prendi dati e fai una ricerca di mercato"* → **tutti** → censimento su tutte le nostre nicchie.
> Metodo: workflow 30 agenti (15 nicchie × censimento + verifica avversariale qualità-dato). Mercato = **eBay** (non Meta ads). Ogni numero con URL fonte + data; eBay/AliExpress walls → lower bound dichiarati.

## VERDICT (sintesi)
**14 nicchie su 15 = MARKET PROVEN (domanda reale), ma TUTTE con spazio TIGHT o NO.** Cioè: i mercati esistono e vendono, ma sono **commodity saturi** dove il floor di prezzo è una corsa al ribasso su SKU AliExpress identici per tutti. **In nessuna nicchia si entra come "me-too" generico** — si entra solo con un **ANGOLO** (tier premium/decor, bundle, compatibilità precisa nel titolo, formato XL, foto/copy migliori). 1 nicchia (book light) è risultata **UNPROVEN** come mercato per un nuovo entrante (domanda spalmata su migliaia di listing identici).

## CONFIDENCE
Media-alta sui verdetti di domanda (densità eBay + ordini AliExpress = forti, citati). Bassa sui **margini** (non valutati in questo run) e sugli **esatti conteggi sold/active** (muri eBay 403/429 → lower bound da snippet/category render, non da filtro Sold).

## DOMINANT MARKET PATTERN
Stesso pattern in 15/15: **domanda PROVEN + saturazione alta + floor commodity da $0.99–$10 AliExpress rivenduto a prezzi schiacciati**, con anchoring "was/now" diffuso. Lo spazio difendibile è SEMPRE nel **tier superiore** (premium/bundle/decor/compatibilità), mai sotto il floor.

## CLASSIFICA per opportunità (score 0-10 dal verificatore avversariale)

| # | Nicchia | Verdetto | Spazio | Score | Domanda | Satur. | Mossa |
|---|---|---|---|---|---|---|---|
| 1 | **Coffee pod holders** | PROVEN | TIGHT | **5.5** | growing | high | entra solo tier **station/decor** ($25-50) o **bundle macchina-specifico** (Vertuo/K-Cup/Dolce Gusto nel titolo); salta i vassoi acrilici |
| 2 | Silicone shower squeegees | PROVEN | TIGHT | 4.5 | stable | high | bundle/premium; mai il singolo squeegee nero $8. Filler di margine |
| 3 | No-spill dog water bowls | PROVEN | TIGHT | 4.5 | stable | high | stainless **grande capacità** + bundle + garanzia anti-spill; salta il plastica-piccolo |
| 4 | Stove counter gap covers | PROVEN | TIGHT | 4.5 | stable | high | **oversized/extra-long** o bundle; mai il 21" 2-pack me-too |
| 5 | Dog booster car seats | PROVEN | TIGHT | 4.5 | growing | high | premium **small-dog safety** ($45-60, frame metallo/fino 40lb) + bundle; salta il $20-34 |
| 6 | Microwave splatter covers | PROVEN | TIGHT | 4.5 | stable | high | tier **magnetico/collassabile 12"** ($18-28); salta il vented-plastica $3.99 |
| 7 | Mini travel flat irons | PROVEN | TIGHT | 4.5 | growing | medium | **cordless/USB 2-in-1 travel** ($22-29) + pouch + dual-voltage; salta corded $8-15 |
| 8 | Wall-climbing gecko RC toys | PROVEN | TIGHT | 4.5 | growing | medium | **gift bundle/2-pack** + hook "prank toy"; trend cross-platform **late-stage** → muoviti veloce o salta |
| 9 | Slow feeder dog bowls | PROVEN | TIGHT | 4.5 | growing | high | **XL/large-breed** o bundle o ceramica/maze premium; salta il $10-17 |
| 10 | Collapsible water bottles | PROVEN | TIGHT | 3.5 | stable | high | (bassa priorità) solo bundle premium leakproof; altrimenti evita |
| 11 | Baby bath thermometers | PROVEN | TIGHT | 3.5 | growing | high | entra con angolo (multifunzione/sicurezza/gift); copy come aiuto, mai garanzia medica |
| 12 | Portable neck fans | PROVEN | **NO** | 3.5 | growing | high | **STAGIONALE** (picco giu-ago, ora): premium semiconductor-cooling/high-mAh $35-45; finestra chiude dopo agosto; salta sub-$15 |
| 13 | Orthopedic dog beds | PROVEN | TIGHT | 3.5 | stable | high | **XXL/giant-breed** o chew-proof + angolo senior-dog ($70-110); salta medium/large commodity |
| 14 | Self-adhesive cable clips | PROVEN | TIGHT | 3.0 | stable | high | **bundle/kit** + adesivo-premium provato; mai il floor $4-7 |
| 15 | **Clip-on book lights** | **UNPROVEN** | **NO** | 2.5 | stable | high | mercato saturo (migliaia di listing identici, floor $0.99, sold per-listing bassissimi) → **evita** salvo angolo spec-backed (Kindle/music-stand + gift 2-pack, $10-12) |

## DEMAND SIGNAL (esempi citati)
- Coffee pod holders: eBay **5.376 listing attivi** (cat 46283); un listing **1.594 venduti**; AliExpress 700-900+ ordini su più SKU. [OBSERVED 2026-06-20]
- Shower squeegees: AliExpress più SKU **10.000+ ordini**; eBay 20+ listing distinti. [OBSERVED]
- Book light: AliExpress **5.000+ ordini**; eBay "3.726 rechargeable + 4.393 clip-on" listati MA sold per-listing 1-4 (domanda spalmata). [OBSERVED]
- (Dettaglio per-nicchia con URL+data nei `data_basis` del workflow — vedi `90_CACHE`/output run.)

## RECOMMENDED MOVE (strategia, regola §8)
1. **Cambio di strategia, non di nicchia:** il problema non è "quale nicchia" (sono tutte valide come domanda) ma **COME entrare**. Smettere di listare lo SKU generico (è ciò che ci ha dato margini sottili e annunci che non vendono) e passare a **1 angolo per nicchia**: tier premium / bundle / formato XL / compatibilità precisa nel titolo / foto+copy originali.
2. **Priorità (relative):** Coffee pod holders (station/decor) #1; poi i gadget pulizia/pet a 4.5 (squeegee, dog bowls, microwave covers, flat iron) con bundle. **Stagionale ORA:** neck fan (finestra estiva, premium).
3. **De-prioritizzare/evitare come me-too:** book light (UNPROVEN), cable clips (3.0), collapsible bottle (3.5) — entrare solo con bundle forte o lasciar perdere.
4. **Prima di qualunque lancio:** check **margine** (costo AutoDS reale + fee eBay) — non valutato qui; e il **blocco account eBay** va risolto (vedi cockpit) prima di pubblicare.

## REJECTED ALTERNATIVES
- "Listare più SKU generici per volume" → **rifiutato**: è la corsa al floor che genera margini ~$0 e annunci morti (confermato dai 15 verdetti TIGHT/NO).
- "Puntare sulla nicchia con più domanda prodotto (book light)" → **rifiutato**: a livello mercato è UNPROVEN/NO-space (domanda spalmata su migliaia di listing). **Lezione: domanda-prodotto ≠ opportunità-mercato.**

## OWNER ROLE
Decidere: (a) adottare la strategia "1 angolo per nicchia" e su quali 2-3 nicchie partire; (b) sbloccare l'account eBay; (c) confermare i margini sugli SKU-angolo prima di lanciare. Nessuna azione live parte senza GO.

## MEASUREMENT PLAN
Per ogni nicchia scelta: confermare col **filtro Sold eBay** (sell-through reale 90gg) e il **margine** (costo AutoDS + fee) prima del lancio; poi misurare impressions/sell-through del listing-angolo vs il floor.

## BLOCKERS / OPEN ITEMS (owner-manual checklist)
- eBay sch/itm **403/429** → conteggi active/sold = lower bound da snippet/category; confermare i top col filtro Sold.
- AliExpress item-page **CAPTCHA** → ordini dalla search-render (lower bound); costo reale da confermare in AutoDS.
- Google Trends non aperto direttamente → direzione domanda = [INFERRED] da report secondari.
- **Margini non valutati** in questo run (solo domanda/supply/verdetto). Da fare prima del lancio.

## FILES UPDATED
- Questo report. + RESEARCH_MEMORY_INDEX (blocco nicchia) + cockpit (MASTER_DASHBOARD + NEXT_ACTIONS).

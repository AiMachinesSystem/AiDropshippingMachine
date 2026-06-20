---
tags:
  - machine
type: hub
status: active
description: "Cockpit unico della macchina: stato, decisioni owner pendenti, top azioni con minuti, ultimi run con verdetti, KPI vault, Bases live. Refreshato a ogni fine run. Popolato 2026-06-15 (post-import foundation eBay/AutoDS)."
---

# Master Dashboard — COCKPIT

> Sala di controllo unica. Aggiornata a ogni fine run (regola AUTO-REFRESH).
> Dettaglio stato/gate: [[CURRENT_STATUS]] · prossime azioni: [[NEXT_ACTIONS]].

## 1 · Stato macchina

| Voce | Stato |
|---|---|
| Costruzione | iniziata — foundation eBay/AutoDS importata e integrata (2026-06-15) |
| Vision (criterio dichiarato) | n/d — `VISION_ALIGNMENT`/`VISION_GAP_MATRIX` non ancora compilate dall'owner |
| Skill di business | 14 (toolkit del template, non specifiche eBay) — [[MACHINE_STATE]] |
| Integrazioni | **AutoDS read-only via Playwright OPERATIVO** (sessione salvata, 2026-06-16): letti store/catalogo/ordini/settings. API REST AutoDS = a pagamento/gated (no key). n8n = solo blueprint. **Zero scritture live.** |
| Progetto: store eBay/AutoDS (**US seller → US buyers**, eBay.com, USD) | **2026-06-17: rimossi 37 listing OOS morti (AutoDS+eBay) → 177 attivi** (tenuti 13 venditori + 5 OOS-winner da ristoccare + margine-bassi). **Trial NON rinnovato (owner) → scade 18/06, monitoraggio cessa.** Import 3 nuovi SKU in **HOLD** (conflitto: non si importa in account che scade). |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 🛑 | **eBay BLOCCA le nuove inserzioni (2026-06-20)** — *"violation of eBay selling policy or a restriction on your eBay account"*. Controllare **eBay Seller Hub → Account/restrizioni/limiti di vendita/messaggi** e risolvere. | nessun publish nuovo possibile finché l'account eBay non è sbloccato; i 5 draft pronti restano in attesa |
| 1 | **Trial AutoDS NON rinnovato (owner 2026-06-17) → scade 18/06.** Decidere: wind-down AutoDS / gestione eBay manuale / altro tool | i 177 restano senza stock-price sync dal 18/06 (rischio oversell) |
| 2 | **Conflitto da sciogliere:** import 3 nuovi SKU mid-ticket in un account che scade domani = inutile/rischioso; + sourcing Amazon = rischio policy. Decidere se/come | blocca l'import dei nuovi prodotti |

> **Risolte 2026-06-15 (governance closeout):** identità owner = **Luca**; etichette evidenza = **solo set costituzionale §0.4** (il superset di `OPERATING_RULES §3` resta in **quarantena**, NON ratificato); compilazione `VISION_ALIGNMENT` **rinviata** per scelta owner.
> **Risolte 2026-06-15 (owner context):** buyer = **US / eBay.com** (USD), secondario NESSUNO; **seller = US-registrato + US-located**; Italy/EU **NON rilevante**. Lo schema eBay.com/US è ora il riferimento **vincolante**.

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Decidere **rinnovo trial AutoDS** (piano minimo) o lasciar scadere | 👤 owner | ~10 | **entro 2026-06-18** |
| 2 | Dare GO al **fix VeRO + tally salute dei 214 listing** (read-only tally = senza GO; fix/rimozioni = GO) | 👤 owner | ~10 | protegge account |
| 3 | Approvare il **test 3 SKU alto-margine** (phone tether · torso anatomico · duck topper) — import = `GO_IMPORT_5_DRAFTS` | 👤 owner | ~10 | dopo decisione strategica |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| 2026-06-20 | **Info-gathering 8 segnali-trend** (workflow 16 agenti) | Nessun "pursue". **Maybe:** AirTag insole (4.5, rising, **VeRO HIGH**), sun shade umbrella (4.2, **stagionale estate**), fridge bins, chicken shredder, ultrasonic cleaner. **Avoid:** sunset lamp (declining), drain hair catcher (saturo), mini vacuum sealer (overlap). Dato eBay = proxy (muri 403). Report: `…/MARKET_RESEARCH_REPORTS/2026-06-20_trend-signals_INFO_GATHERING_v1.md`. |
| 2026-06-20 | **Scan competitor eBay + nuovi prodotti → 6 draft Amazon** (workflow 28 agenti) | 17 competitor eBay mappati + **6 NUOVI prodotti** (fuori dalle nicchie sature) importati come DRAFT da Amazon, titolo ≤80 + desc VeRO-safe: Faucet Splash Mat (7), Roll-Up Dish Rack (7), Stretch Lids, Sink Caddy, Hinge LED Light, Backpack Stool. Drafts 13→19. Publish = GO + sblocco account eBay. File: `…/listings/NEW_PRODUCTS_6_drafts_2026-06-20.md`. |
| 2026-06-20 | **Market research multi-nicchia — 15 nicchie del catalogo** (workflow 30 agenti, dati citati) | **14/15 PROVEN ma TUTTE sature** (space TIGHT/NO). Top opportunità: **coffee pod holders 5.5** (solo tier station/decor); poi cleaning/pet gadgets 4.5. **Book light UNPROVEN** (domanda-prodotto ≠ opportunità-mercato). **Strategia:** si vince solo con un **ANGOLO** (premium/bundle/XL/compatibilità), mai me-too sul floor. Margini non valutati. Report: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-20_multi-niche-catalog_NICHE_VALIDATION_v1.md`; indice aggiornato. |
| 2026-06-20 | **Import 5 draft (post re-login manuale)** (GO owner) | Sessione AutoDS scaduta (Google-SSO) → **login manuale owner** la ripristina (E-004 fixato nel login script). **5 prodotti ricercati importati come DRAFT** (AliExpress): Book Light, Water Bottle, Shower Squeegee, No-Spill Dog Bowl, Baby Thermometer — titolo ≤80 + descrizione VeRO-safe applicati+verificati. Resistance Bands non importato (margine sottile). **🛑 Publish dei 5 tentato (GO): costi sani (~$7 profit), ma BLOCCO eBay — *"eBay Error: item can not be listed... violation of eBay selling policy or a restriction on your eBay account"*. eBay rifiuta le nuove inserzioni (limite vendite o flag policy). STOP publish; owner deve controllare eBay Seller Hub (restrizioni/limiti). I 5 draft restano pronti.** |
| 2026-06-20 | **Ricerca data-first 10 prodotti (gate qualità-dato)** (workflow 33 agenti) | **6/16 passati**: Clip-On Book Light (conf ALTA), Collapsible Water Bottle, Shower Squeegee, No-Spill Dog Bowl, Baby Bath Thermometer, Resistance Bands. Fonte AliExpress, dati citati (URL+data). 10 scartati per dato non tracciabile all'SKU (CAPTCHA item-page) / margine negativo / titolo>80. Report con tabelle dati: `…/listings/LISTING_RESEARCH_10_2026-06-20.md`. 0 import. |
| 2026-06-20 | **Publish (verifica titolo≤80+descrizione+costo PRIMA) + cleanup esauriti** (GO owner) | **8 listing pubblicati** (confermati): Neck Fan, Coffee Pod Holder, Slow Feeder, Dog Booster, Ortho Dog Bed, Cable Clips, Microwave 2-in-1, Collapsible Microwave. **🗑️ 11 draft esauriti cancellati** (Remove from list, guard, verificato; asset nel repo → ri-importabili). **3 stragglers non pubblicabili** (Gecko/Magnetic/Flat Iron: 4 metodi tentati → publish fallisce lato AutoDS). Under-sink flaggato (costo gonfiato → propongo cancellazione). **Monitoraggio AutoDS degradato** = blocco di fondo. Verifica-prima ha evitato ~12 annunci rotti. |
| 2026-06-19 | **Routine "source N → draft" + ricerca 3 nuovi prodotti** (workflow 17 agenti, verifica avversariale) | Creata routine riusabile `source-products-to-draft` (dispatcher aggiornato). 3 draft-ready NUOVI (esclusi ~16 già a draft + 1 duplicato): Silicone Stove Gap Cover (`B09TT744X9`, costo $9.49 OBSERVED), Drill Brush Scrubber 3pc (`B0789K37SV`), Under-Sink Organizer 2-tier (`B0C5DBMYZF`); titoli 74/79/78 + descrizioni riscritte. **✅ Import + PUBLISH (GO owner): 3 live su eBay `divinit-92-us`**. Economics reali: **stove $9.49→$19.97 ✅**; **drill $133.13→$199.99 ❌ · under-sink $43.99→$65.97 ❌** (costi import errati/alti, non venderanno; policy ha evitato la perdita). ⚠️ **E-003** (publish accidentale stove via probe). **FIXA (GO):** drill+under-sink **deattivati** (AutoDS+eBay); **re-source bloccato** — AutoDS riporta costi inaffidabili (drill placeholder $133.13/OOS, under-sink $68.99 vs $17 reale) → auto-pricing rotto, non ri-pubblicato. **Catalogo nuovi = 1 valido (stove)**. File: `…/listings/LISTING_COPY_3_drafts_2026-06-19.md`. |
| 2026-06-17 | **Import 4 draft batch-2 (Temu-validati, fonte Amazon) + titolo≤80 + descrizione CKEditor** (GO owner) | Winner validati via Temu (fabric shaver, mini vacuum, magnetic window cleaner, motion closet light) presi da Amazon (AutoDS importa solo AliExpress/Amazon); draft 19→**23**; titoli + descrizioni applicati e persistiti (×4); pronti per publish (publish = GO). |
| 2026-06-17 | **Import 3 nuovi draft + titolo≤80 + descrizione VeRO-safe** (GO owner) | Playwright riattivato; ricercati 3 prodotti generici (slow feeder bowl, coffee pod holder, neck fan) con URL Amazon live; draft 16→**19**; titoli 80/79/79 applicati e persistiti; **descrizioni applicate via CKEditor API (muro caduto)** e persistite; 0 publish. |
| 2026-06-17 | **Rimozione 37 listing OOS morti** (GO owner) | 214→**177** attivi; chiusi anche su eBay ("AutoDS+Selling Platform"); 13 venditori + 5 OOS-winner protetti; verificato. Trial non rinnovato. |
| 2026-06-17 | Listing audit + mid-ticket research + strategy update | lista azioni per-listing; top 3 mid-ticket; downgrade torso |
| 2026-06-16 | Decisione strategica autonoma (7gg) | Verdetto su prodotto/trial/sequenza/fix; piano prioritizzato GO vs no-GO → `04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md` |
| 2026-06-16 | Deep Product Research (funnel multi-tool) | 7 trend → 24 nicchie → 121 prodotti AutoDS → 20 cross-check eBay; TOP 15 + 5 schede; muri eBay/AutoDS dichiarati [UNKNOWN] |
| 2026-06-16 | Capability audit (read-only, 7 agenti) | Governance/memoria/analisi + AutoDS read-only PROVATE; motore vendite 0% operativo; ~60% reale/40% scaffold |
| 2026-06-16 | AutoDS read-only via Playwright (login + status + counts) | Sessione salvata; letti 214 listing/11 draft/23 ordini; auto-order ON ma non operativo; trial scade 2026-06-18; 0 scritture |
| 2026-06-16 | Playwright integration scaffold + smoke test | Browser headless funziona (HTTP 200 su platform.autods.com); venv isolato; safety contract read-only |
| 2026-06-15 | Import foundation eBay/AutoDS | Foundation importata e integrata; 0 azioni live; gate Data Collection in attesa di GO |
| 2026-06-15 | Ricerca pubblica policy/fee/feature (eBay+AutoDS) | 21 fonti in cache; 6 output dati + intake report; 0 azioni live; stop prima dell'analisi |
| 2026-06-15 | Analisi policy/fee/feature (eBay+AutoDS) | Mappe constraint/fee/risk/account-health/dependency evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni; verifica adversarial PASS; gate Analysis→Strategy chiuso |
| 2026-06-15 | Contesto seller (USER-PROVIDED) | seller US-registrato + US-located, USD; Italy/EU non rilevante; dependency principale dell'analisi risolta; Strategy ancora bloccata |
| 2026-06-15 | AutoDS Read-Only Data Intake Plan | piano (categorie/cattura/storage/forbidden/checklist/prereq) + report; 0 accessi/login/dati; intake non avviato |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS / analysis | 9 (init · stabilization · data-collection · analysis · autods-intake-plan · autods-status · capability-audit · deep-product-research · strategic-decision) |
| Note attive nel vault | n/d (non conteggiate) |
| % vision realizzata | n/d (vision non compilata) |
| Scritture live eseguite | **Import draft** (più batch, 2026-06-17/19) + **rimozione 37 OOS** (2026-06-17) + **PUBLISH 3 listing** (2026-06-19, GO owner) · prezzi via pricing policy AutoDS · **ordini/auto-order = mai** · letture read-only via Playwright |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]

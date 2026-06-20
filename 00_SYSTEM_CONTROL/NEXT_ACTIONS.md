---
tags:
  - machine
type: log
status: active
description: "Lista chiara delle prossime azioni. Refreshata a fine run (regola AUTO-REFRESH). Popolata 2026-06-15 con lo stato post-import foundation eBay/AutoDS."
---

# Next Actions

> Modulo: 00_SYSTEM_CONTROL. Aggiornata a ogni fine run insieme a MASTER_DASHBOARD
> (regola AUTO-REFRESH: run senza refresh = INCOMPLETO). Dettaglio fase in [[CURRENT_STATUS]].

## ⚡ CHECKLIST MANUALE BROWSER OWNER
<!-- Azioni che solo l'owner può fare a mano (login, dropdown geo/reach, ecc.), con URL espliciti. -->
- Nessuna azione browser autorizzata in questa fase: nessun login, nessun accesso a eBay/AutoDS/fornitori. Ogni azione esterna richiede GO esplicito.

## Exact Next Step
> **2026-06-20 (sera) — RISOLTO + 5 DRAFT IMPORTATI.** La sessione AutoDS era scaduta (Google-SSO); re-login automatico fallito (E-004, ora **fixato** nel login script). **Login MANUALE owner → sessione ripristinata** (`status`=9, ok). **Import 5 prodotti come DRAFT (GO owner):** Book Light, Collapsible Water Bottle, Shower Squeegee, No-Spill Dog Bowl, Baby Bath Thermometer — fonte AliExpress, **titolo ≤80 + descrizione VeRO-safe applicati e verificati** (ids in `LISTING_RESEARCH_10_2026-06-20.md`). Resistance Bands NON importato (margine sottile).
> **🛑 BLOCCO eBay (account) — causa vera dei publish falliti.** Publish dei 5 tentato (GO): costi AutoDS verificati sani (~$7 profit, in stock). Diagnostica su pagina dedicata (Book Light, draft giusto) → errore **eBay**: *"Product import failed. eBay Error: The item can not be listed or modified due to violation of the eBay selling policy or a restriction on your eBay account."* → **eBay sta rifiutando le nuove inserzioni** (probabile **limite di vendita** raggiunto pubblicando ~13 oggi, o **flag di policy** retail-sourcing). Stamattina pubblicava, ora no. **STOP publish** (ritentare peggiora lo standing). **AZIONE OWNER:** controllare **eBay Seller Hub → Account / restrizioni / limiti di vendita / messaggi policy** e risolvere lì. I 5 draft restano pronti (titolo+descrizione+costo OK), si pubblicheranno quando l'account eBay è sbloccato.
>
> **2026-06-20:** Pubblicazione draft (GO owner) con verifica titolo≤80 + descrizione rifatta + **costo AutoDS PRIMA del publish**. **8 listing pubblicati e confermati in /products** oggi: Neck Fan $25.61→$38.97 · Coffee Pod Holder $13.99→$25.97 · Slow Feeder Bowl $9.99→$20.97 · Dog Booster Seat $49.99→$74.97 · Orthopedic Dog Bed $29.99→$44.97 · Cable Clips $5.99→$15.97 · Microwave Cover 2-in-1 $13.99→$25.97 · Collapsible Microwave Cover $16.99→$28.97. (+ stove = **9 nuovi live**).
> - 🗑️ **2026-06-20 (GO owner): cancellati 11 draft ESAURITI** (Remove from list, dry-run+guard, verificato 0 rimasti): EZ drill, cheese board, motion light, magnetic window, mini vacuum, fabric shaver, koi aerator, neck massager, jar opener, trunk organizer, dog grooming arm. **Asset (titoli/descrizioni/immagine fabric shaver) restano nel repo → ri-importabili.**
> - ❌ **3 stragglers NON pubblicabili** (Gecko RC, Microwave Magnetic, Mini Flat Iron): tentati **4 metodi** (card Import, Save&Import dedicato, ricerca paginata) → publish non si completa lato AutoDS (silenzioso). Gecko rifiutato; flat iron click-ma-non-pubblica; magnetic non rintracciabile. = **fallimento AutoDS**, non risolvibile da qui ora. Da fare a mano nella UI AutoDS o quando AutoDS è stabile.
> - ⏸️ **Under-sink** (`B0CR2LF5FQ`): titolo 200char scrapato + costo gonfiato $68.99→$102.97 (non venderebbe). **Raccomando di cancellarlo** invece di pubblicarlo; in attesa di tua conferma.
> - **Blocco di fondo:** monitoraggio costo/stock AutoDS **degradato** (placeholder $133.13 + molti OOS + publish a singhiozzo) → catalogo non pubblicabile in blocco finché AutoDS non è affidabile. Decisione owner: sistemare/rifare l'accesso AutoDS.
>
> **2026-06-19:** Creata routine riusabile **`source-products-to-draft`** (intento owner: "ricerca N prodotti e mettili in draft") + ricercati **3 nuovi draft-ready** (Silicone Stove Gap Cover · Drill Brush Scrubber 3pc · Under-Sink Organizer 2-tier) → `…/listings/LISTING_COPY_3_drafts_2026-06-19.md`. **✅ Import + PUBLISH (GO owner): 3 listing live su eBay `divinit-92-us`**. Economics reali [OBSERVED AutoDS API]: **stove $9.49→$19.97 (profit $7.13) ✅ viable**; **drill `B0789K37SV` costo $133.13→$199.99 ❌** e **under-sink `B0C5DBMYZF` costo $43.99→$65.97 ❌** = importati a costi errati/alti (i 2 non confermati per CAPTCHA) → non venderanno (policy ha evitato la perdita, non la non-vendibilità). ⚠️ **E-003**: stove pubblicato da un probe diagnostico. **FIXA eseguito (GO owner):** drill+under-sink **deattivati** (AutoDS+eBay, verificato). **Re-source BLOCCATO:** AutoDS riporta costi inaffidabili — drill candidato `B07FPV8F72` costo **$133.13** (placeholder, = al vecchio; anche OOS), under-sink `B0CR2LF5FQ` **$68.99** (gonfiato ~4× vs ~$17 reale) → auto-pricing rotto, **non ri-pubblicato**. **Catalogo nuovi = 1 valido (stove)**. Prossimo: re-publish solo con costo AutoDS affidabile o fonte/costo confermato owner; 2 draft test parcheggiati (`6a35fc72…`, `6a35fc97…`).
>
> **Stato 2026-06-17:** rimossi 37 OOS morti (AutoDS+eBay) → **177 attivi**. **Trial AutoDS NON rinnovato (owner) → scade 18/06**: il monitoraggio stock/prezzo cessa sui 177.
> 1. ⏰ **DECISIONE OWNER:** wind-down AutoDS? Se sì → piano per i 177 su eBay (gestione manuale / altro tool / chiusura graduale). Se no → riconsiderare un rinnovo minimo prima del 18/06.
> 2. **HOLD — import 3 mid-ticket (PC temp display / amaca cane / ham press):** non importare in un account che scade domani; + sourcing **Amazon = rischio policy** (consigliato **AliExpress alto-recensioni**). Sbloccare solo dopo la decisione su AutoDS.
> 3. **Da fare solo se l'account resta gestito (GO/manuale):** ristoccare i 5 OOS-winner (Dog Water Ramp $202, Pet Grooming Loops $286, Ham Maker…); fix VeRO ('alcohol' draft + 63 attivi) + 100 titoli cambiati.

## Parked Options (each needs its own explicit GO)
1. **Avviare l'intake AutoDS read-only** — pending prerequisiti (§6 del piano) + GO; metodo: export/screenshot/guided. (Controlled login = GO separato.)
2. **Analysis Delta Only** — aggiornare le conclusioni di dependency dell'analisi al contesto US-seller (interno).
3. **Strategy** (offer/pricing/listing/supplier/risk) — BLOCCATA: richiede GO owner + dati fornitori/economici.
4. **Raccolta dati owner** (eBay Seller Hub, AutoDS, fornitori da export/screenshot) — GO classe: accesso a dati owner.
5. **Raccolta dati fornitori/competitor/prodotto** (economics) — GO classe: ricerca esterna (nuovo scope).
6. **Ricerca pubblica di follow-up** (numerici US-help esatti; pricing AutoDS) — GO classe: ricerca esterna. (eBay.it/EU NON più rilevante.)
7. Sempre bloccate finché non c'è strategia approvata: execution/SOP oltre la gate structure · pubblicazione/modifica listing · automazioni AutoDS · ordini/pagamenti fornitori · scaling.

## Comando pronto (data collection, GATED — copia/incolla per dare il GO)
```text
APPROVE DATA COLLECTION ONLY

Machine: eBay / AutoDS Dropshipping Machine

Scope:
Use owner-provided screenshots/exports only.
Do not access accounts. Do not browse public web.
Do not analyze. Do not create strategy. Do not create execution plans.
Do not modify eBay, AutoDS, suppliers, payment accounts, or any live platform.

Inputs I will provide:
1. eBay Seller Hub screenshots/exports: [attach]
2. AutoDS dashboard screenshots/exports: [attach]
3. Supplier list or screenshots: [attach]
4. Fee/shipping/return/account health screenshots if available: [attach]

Output:
Raw data notes, cleaned data tables, missing data log, data quality notes, source access notes, final data intake report.
Stop before analysis.
```

## Waiting / Blocked
- Dati account-specifici eBay/AutoDS/fornitori/economics (account health, limiti, store tier, payment settings, piano AutoDS, fornitori, categoria, margini, dati business) — USER INPUT NEEDED ([[MISSING_OWNER_INPUTS]]).
- Numerici US-seller esatti dietro le pagine US-help (fetch wall) — PUBLIC RESEARCH REQUIRED. (eBay.it/EU non più rilevante.)

## Completed
- [x] 2026-06-20 — **Market research multi-nicchia (15 nicchie del catalogo)** (workflow 30 agenti, dati citati + verifica avversariale): **14/15 PROVEN ma TUTTE sature** (space TIGHT/NO). Classifica opportunità: coffee pod holders 5.5 (tier station/decor) > cleaning/pet gadgets 4.5 > … > cable clips 3.0 > **book light 2.5 UNPROVEN**. **Insight strategico:** domanda-prodotto ≠ opportunità-mercato; si vince solo con un **ANGOLO** (premium/bundle/XL/compatibilità precisa), mai come me-too sul floor — questo spiega i margini sottili dei lanci finora. Report: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-20_multi-niche-catalog_NICHE_VALIDATION_v1.md` + RESEARCH_MEMORY_INDEX (blocco "Catalog multi-niche census"). **Aperto owner:** scegliere 2-3 nicchie su cui partire con angolo + valutare i margini.
- [x] 2026-06-20 — **Ricerca data-first 10 prodotti** (workflow 33 agenti, 16 candidati, gate qualità-dato avversariale): **6 PASSATI / 10 scartati**. I 6 (fonte AliExpress, dati citati): Clip-On Book Light (conf ALTA, eBay 4.749 sold su un listing), Collapsible Water Bottle (50k+ ordini fonte), Silicone Shower Squeegee, No-Spill Dog Water Bowl, Baby Bath Thermometer, Resistance Bands (margine sottile). 10 scartati quasi tutti per **dato non tracciabile all'SKU** (item-page AliExpress CAPTCHA-walled → numeri dalla search-page) o margine negativo/titolo>80. Report con tabelle dati citati: `…/listings/LISTING_RESEARCH_10_2026-06-20.md` + `copy_2026-06-20/*.html`. **0 import** (import = GO + caveat AutoDS degradato).
- [x] 2026-06-20 — **LIVE PUBLISH (GO owner): 8 listing** su eBay `divinit-92-us`, con verifica titolo≤80 + descrizione rifatta + **costo AutoDS PRIMA del publish** (protocollo nato da E-003). Confermati in /products: Neck Fan, Coffee Pod Holder, Slow Feeder Bowl, Dog Booster Seat, Orthopedic Dog Bed, Cable Clips, Microwave Cover 2-in-1, Collapsible Microwave Cover (margini positivi, in stock). Tool: per-card Import + dedicated Save&Import, guard E-002/E-003. **3 publish falliti silenziosamente** (Gecko RC, Microwave Magnetic, Mini Flat Iron → ritentare). **NON pubblicati (corretto):** 6 costo-placeholder $133.13/OOS + 5 OOS-real-cost + under-sink (titolo 200char) + 2 doppioni. La verifica-prima ha evitato ~12 annunci mal-prezzati/esauriti. **Monitoraggio costo/stock AutoDS degradato** = blocco di fondo.
- [x] 2026-06-19 — **Routine "source N → draft" creata** (`02_DATA/_ROUTINES/source-products-to-draft.md` + riga `MASTER_ROUTINE`) su richiesta owner + **ricerca 3 NUOVI prodotti draft-ready** (workflow 17 agenti, 8 candidati → verifica avversariale → 5 pass; esclusi i ~16 già a draft + 1 duplicato car-seat). Vincitori: Silicone Stove Gap Cover (Amazon `B09TT744X9`, costo **$9.49 OBSERVED**), Drill Brush Scrubber 3pc (`B0789K37SV`, costo ~$7.50 da confermare), Under-Sink Organizer 2-tier L-shape (`B0C5DBMYZF`, costo da confermare). Titoli 74/79/78 (≤80) + descrizioni VeRO-safe riscritte (`listings/copy_2026-06-19/*.html`). Copy+comandi: `…/listings/LISTING_COPY_3_drafts_2026-06-19.md`.
  - ✅ **LIVE WRITE (GO owner `GO_IMPORT_5_DRAFTS`): 3 draft importati** → drafts **26→29** (Add-as-Draft); titoli ≤80 + descrizioni CKEditor applicati e persistiti (×3). ID: stove `6a35e9dbfc48b38c8a55487c` · drill `6a35ea532dec65c173126208` · under-sink `6a35eabf18a6518dcc0ca4d6`. Tool: `manage_draft.py`. Under-sink ha richiesto set-title/set-desc separati (scrape titolo non pronto al 1° tentativo).
  - ✅ **LIVE PUBLISH (GO owner): 3 listing live su eBay `divinit-92-us`** — pricing dinamico AutoDS: stove **$19.97** (profit $7.13, costo $9.49) [OBSERVED]; drill+under-sink prezzo in verifica. ⚠️ **E-003**: stove pubblicato accidentalmente da un probe diagnostico (card "Import" = publish immediato) — esito ok, errore registrato. Drill+under-sink pubblicati deliberatamente (`_pub_one.py`).
- [x] 2026-06-17 — **Import 3 nuovi draft (GO owner) con titolo≤80 + descrizione VeRO-safe**: slow feeder dog bowl (B0CJXNXMMY), coffee pod holder (B0CZ6DX9YJ), portable neck fan (B09PCSR9SX). Draft 16→19; titoli 80/79/79 persistiti; descrizioni applicate via CKEditor API su pagina dedicata e persistite (×3); 0 publish. Tool: `import_drafts.py`, `apply_titles_3.py`, `apply_desc_ckeditor_3.py`, `discover_draft_ids.py`. Copy: `…/listings/LISTING_COPY_3_drafts_2026-06-17.md`.
  - ✅ **MURO CADUTO**: la descrizione draft AutoDS È automatizzabile via `/upload/<id>` + `window.CKEDITOR.instances[0].setData(html)` (prima ritenuta solo-manuale). Aggiornare VAULT_CONVENTIONS muri noti.
- [x] 2026-06-15 — Import e merge della foundation eBay/AutoDS nella struttura della macchina (Phase 1 — system initialization completata).
- [x] 2026-06-15 — Governance closeout: owner = Luca; etichette = solo set §0.4 (superset `OPERATING_RULES §3` in quarantena, non ratificato); compilazione `VISION_ALIGNMENT` rinviata.
- [x] 2026-06-15 — Ricerca pubblica policy/fee/feature eBay+AutoDS (percorso B): 21 fonti in cache → 3 raw + 3 tabelle pulite + note fonti/qualità/missing + data intake report. Stop prima dell'analisi.
- [x] 2026-06-15 — Contesto owner salvato (USER-PROVIDED): buyer market = US / eBay.com, USD; seller country/location restano USER INPUT NEEDED. Gate Data → Analysis preservato.
- [x] 2026-06-15 — Analisi policy/fee/feature completata (evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni/profittabilità; verifica adversarial 3-agent = PASS). Gate Analysis → Strategy chiuso.
- [x] 2026-06-15 — Contesto seller salvato (USER-PROVIDED): seller US-registrato + US-located, USD; Italy/EU non rilevante. Dependency principale dell'analisi risolta; Strategy resta bloccata.
- [x] 2026-06-15 — AutoDS Read-Only Data Intake Plan creato (piano + prerequisiti + report). Solo piano; nessun login/accesso/dato AutoDS; intake non avviato.
- [x] 2026-06-16 — Playwright installato (venv isolato) + smoke test connettività (HTTP 200 su platform.autods.com). Read-only, nessun login.
- [x] 2026-06-16 — Login AutoDS + sessione salvata (`storage_state.json`, gitignored) sotto GO_PLAYWRIGHT_LOGIN; sessione riutilizzabile verificata.
- [x] 2026-06-16 — AutoDS read-only status (GO_AUTODS_READ_SESSION): store Divinit-92-Us, 214 listing/11 draft/23 ordini, auto-order ON ma non operativo, trial scade 2026-06-18 → `10_OUTPUTS/autods_status_report.md`.
- [x] 2026-06-16 — Capability audit read-only (7 agenti) → `10_OUTPUTS/DROPSHIPPING_MACHINE_CAPABILITY_AUDIT_2026-06-16.md`.
- [x] 2026-06-16 — Deep Product Research (funnel multi-tool) → `03_ANALYSIS/DEEP_PRODUCT_RESEARCH_2026.md`; TOP 15 + 5 schede; muri eBay/AutoDS dichiarati.
- [x] 2026-06-16 — Decisione strategica autonoma (7gg) → `04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md`. Solo piano; nessuna azione live.
- [x] 2026-06-17 — Tally read-only dei 214 + lista azioni per-listing (201 close / 13 keep / 63 VeRO / 100 title) → `05_EXECUTION/.../listings/LISTING_AUDIT_2026-06-17.md` + CSV. Da rivedere prima di GO.
- [x] 2026-06-17 — Update strategia (insight mid-ticket + downgrade torso) + Mid-Ticket Product Research (top 3: PC temp display, dog car hammock, ham press) → `03_ANALYSIS/MIDTICKET_PRODUCT_RESEARCH_2026-06-17.md`. Read-only; costi [ESTIMATE] da confermare prima di GO.
- [x] 2026-06-17 — **LIVE WRITE (GO owner): rimossi 37 listing OOS mai venduti** (AutoDS + eBay, opzione "AutoDS and Selling Platform"), 214→**177**; 13 venditori + 5 OOS-winner protetti (keep-list hard-bloccata); test 2 + batch verificati (count 177, 0 target residui). Tool: `integrations/autods/playwright/remove_oos_listings.py`.
- [x] 2026-06-17 — Owner: **NON rinnovare il trial AutoDS** (scade 18/06).
- [x] 2026-06-17 — **Import draft (GO owner): duck topper AliExpress** (`1005006027632555`, generico, ~60% margine, AliExpress CN) → Drafts 11→**12**. Solo draft, NON pubblicato (publish = GO separato). Tool: `import_drafts.py` (Add-as-Draft only). Pipeline import provata end-to-end.
  - ⛔ Import dei 2 mid-ticket (amaca cane / PC display) **bloccato**: URL AliExpress del finder risultati morti (CAPTCHA wall → non verificabili live). Serve: owner incolla URL validi, OPPURE browser visibile per passare il CAPTCHA AliExpress. Ham press = **ristoccare il vincitore esistente**, non re-importare.
- [x] 2026-06-17 — Profitability-vs-competition study → `04_STRATEGY/PROFITABILITY_VS_COMPETITION_2026-06-17.md` (canon: Amazon→eBay netto ~30-42%, non 50%; 6 leve; top niche+ASIN verificati).
- [x] 2026-06-17 — **Import draft (GO): 4-6 ASIN Amazon** → Drafts 12→16+: jar opener `B07P1SKJV4`, neck massager `B0D3DN6CDS`, koi aerator `B0CQXHB27H`, dog grooming arm `B0DDBR98MB`; trunk organizer `B0DZBFNVZ3` + pegboard `B07QR36Z76` entrati in ritardo (import asincrono). Solo draft, non pubblicati.
- [x] 2026-06-17 — Duck topper: **titolo+descrizione ottimizzati VeRO-safe** → `…/listings/LISTING_COPY_duck_topper_2026-06-17.md` (pronti da applicare).
  - ⛔ **Higgsfield immagine BLOCCATA**: "User not found" → ricollegare il **connettore Higgsfield** nelle impostazioni/connettori dell'app Claude (è MCP, non sbloccabile via browser/Playwright). Prompt immagine salvato, pronto.
  - ✅ **Titolo applicato e SALVATO sul draft duck** (chiave: serve il pulsante **"Save"** scoping sul card — `apply_duck_title.py`; verificato persistente). Titolo live: "Rubber Duck Car Antenna Topper Aerial Ball Cute Yellow Dashboard Buddy Gift".
  - ⛔ **Descrizione**: rich-editor custom non automatizzabile (2 tentativi) → **incolla manuale** dal file copy nel tab Description del draft.
- [x] 2026-06-17 — **Immagine duck generata via Higgsfield** (dopo riconnessione owner): papera gialla generica + casco, fondo bianco, VeRO-safe → `…/listings/images/duck_topper_main.png` (1024², committata `050c7c4`).
  - ⛔ **AutoDS draft "Simple page" NON ha upload immagine custom** (tab Images = solo "Browse in Marketplace") → la nuova immagine va aggiunta **su eBay dopo il publish** (o nella descrizione come img hostata). Le immagini fornitore restano nel draft come fallback.

---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: reference
status: research
date: 2026-06-20
created_real: 2026-06-20
description: "Ricerca data-first di prodotti per draft AutoDS (richiesta owner: 10, priorità = dati rigorosi e tracciabili). Workflow 33 agenti, 16 candidati, gate qualità-dato avversariale → 6 PASSATI / 10 scartati (quasi tutti per dato non tracciabile all'SKM importabile). Fonte = AliExpress (policy-safer + dati leggibili). Import = GO-class. Esegue routine source-products-to-draft."
---

# Ricerca 10 prodotti (data-first) — 2026-06-20

> Richiesta owner: *"ricerca 10 prodotti da mettere in draft; l'importante è la ricerca fatta bene e dati presi bene; voglio sapere su che dati hai basato la decisione."*
> Metodo: workflow multi-agente (33 agenti) → 16 candidati → raccolta dati **citati** → **verifica avversariale con gate qualità-dato** (boccia ogni numero non riconducibile a una fonte aperta).
> Esito: **6 passati / 16**. I 10 scartati: vedi sezione dedicata (motivo dominante = dato non tracciabile all'SKU).

## ⚠️ Limiti del dato (leggere — vale per TUTTI i 6)
1. **Pagina-prodotto AliExpress = CAPTCHA/login-walled.** Costo + ordini-venduti vengono dalla **pagina dei risultati di ricerca** AliExpress (aperta davvero, via proxy `r.jina.ai`), non dalla pagina del singolo item. → **il costo esatto e lo SKU vanno riconfermati in AutoDS all'import.**
2. **eBay sold/active esatti = muro noto** (403/timeout su sch/itm). I "sold" sono **lower bound** da snippet di ricerca; il conteggio attivi è inferito. → **confermare col filtro "Sold" eBay** prima di fissare il prezzo.
3. **Costo fonte → costo AutoDS reale** può divergere (lo abbiamo visto: placeholder $133.13). → il prezzo finale dipende dal costo che AutoDS scrapa all'import; **verificare prima di publish** (publish degradato lato AutoDS, vedi cockpit).
4. Margini = **[ESTIMATE]** con assunzioni dichiarate (fee eBay ~13,25% + $0,40; spedizione inbound spesso non confermata). Conteggi = lower bound.

## I 6 prodotti (ordinati per solidità)

### 1 · Clip-On Rechargeable LED Book Light — **confidence ALTA** (la più solida)
- **Fonte:** AliExpress `3256806823944476` · costo **$2.49** · vendita **$11.99** · margine **~$7.11 (~59%) [ESTIMATE]**.
- **Titolo (75):** `Clip On Book Light Rechargeable LED Reading Lamp Dimmable Flexible Eye Care` · **Desc:** `copy_2026-06-20/clip_book_light.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $2.49 | OBSERVED (search render) | aliexpress.com/w/wholesale-clip-on-book-reading-light-rechargeable | 2026-06-20 |
| Ordini AliExpress | 10.000+ (lower bound), 4.9★ | OBSERVED | stessa pagina | 2026-06-20 |
| eBay sold (listing $9.99) | **4.749 venduti** | OBSERVED (snippet) | ebay.com/shop/book-light-clip-on-rechargeable | 2026-06-20 |
| eBay sold (listing $12.98) | 2.996 venduti | OBSERVED (snippet) | idem | 2026-06-20 |
| eBay range prezzo | $7.19–$16.99 | OBSERVED (snippet) | ebay.com/b/clip-on-reading-light | 2026-06-20 |
- **Perché #1:** domanda eBay **provata da venduti reali a 4 cifre** (4.749 / 2.996 su singoli listing) — il segnale più forte del batch. VeRO-safe, leggero (Li-ion → spedizione standard), margine alto.

### 2 · Collapsible Silicone Water Bottle — confidence media (domanda fonte enorme)
- **Fonte:** AliExpress `1005007306587993` · costo **$1.53** · vendita **$9.99** · margine **~$5.20–6.74 (~52–62%) [ESTIMATE]**.
- **Titolo (80):** `Collapsible Silicone Water Bottle Foldable Leak-Proof Travel Sports BPA-Free Cup` · **Desc:** `copy_2026-06-20/collapsible_water_bottle.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $1.53 | OBSERVED (search render) | aliexpress.com/w/wholesale-collapsible-silicone-water-bottle-outdoor | 2026-06-20 |
| Ordini AliExpress | **50.000+** (lower bound), 4.9★ | OBSERVED | stessa pagina | 2026-06-20 |
| eBay sold (per-listing) | 16 / 9 / 3 venduti | OBSERVED (snippet) | ebay.com/itm/305870495285 | 2026-06-20 |
| eBay range prezzo | $8.49–$13.98 | OBSERVED (snippet) | ebay.com/itm/356837850889 | 2026-06-20 |
| eBay attivi | 25+ listing distinti | OBSERVED (lower bound) | ebay.com/shop/collapsible-silicone-water-bottle | 2026-06-20 |
- **Nota:** mercato molto commoditizzato (prezzi già a $8.49) → margine c'è ma competizione di prezzo alta.

### 3 · Silicone Shower Squeegee (+ hook) — confidence media
- **Fonte:** AliExpress `1005007805413884` · costo **$3.33** · vendita **$8.99** · margine **~$4.07 (~45%) [ESTIMATE]**.
- **Titolo (78):** `Silicone Shower Squeegee Streak-Free Wiper for Glass Doors Mirrors Tiles + Hook` · **Desc:** `copy_2026-06-20/shower_squeegee.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $3.33 | OBSERVED (item/search render) | aliexpress.com/item/1005007805413884 | 2026-06-20 |
| Ordini AliExpress | 10.000+ (lower bound), 4.9★ | OBSERVED | aliexpress.com/w/wholesale-silicone-shower-squeegee-bathroom | 2026-06-20 |
| Corroboro categoria | più listing 10.000+/5.000+/4.000+ sold | OBSERVED | stessa pagina | 2026-06-20 |
| eBay sold (per-listing) | 7 / 2 / 2 / 1 venduti | OBSERVED (snippet) | ebay.com/itm/353598525632 | 2026-06-20 |
| eBay range prezzo | $2.99–$9.65 | OBSERVED (snippet) | ebay.com/sch silicone shower squeegee | 2026-06-20 |
- **Nota:** ticket basso; il venduto eBay per-listing è modesto (singole cifre) → domanda fonte forte, domanda eBay da confermare col filtro Sold.

### 4 · No-Spill Floating-Disk Dog Water Bowl — confidence media
- **Fonte:** AliExpress `1005010052499206` · costo **$6.93** · vendita **$16.99** · margine **~$7.41 (~44%) [ESTIMATE]**.
- **Titolo (76):** `No Spill Dog Water Bowl Floating Disk Anti Splash Slow Drink Stainless Steel` · **Desc:** `copy_2026-06-20/dog_water_bowl_nospill.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $6.93 (un render) / $10.87 promo (altro) | OBSERVED (search render) | aliexpress.com/w/wholesale-dog-water-bowl-anti-spill-floating-disk | 2026-06-20 |
| Ordini AliExpress (SKU) | 245 ordini, 4.9★ | OBSERVED | stessa pagina | 2026-06-20 |
| Corroboro categoria | 195 / 1.000+ / 1.000+ ordini | OBSERVED (lower bound) | stessa pagina | 2026-06-20 |
| eBay sold (per-listing) | 15 + 30 = 45+ venduti | OBSERVED (snippet) | ebay.com/itm/365364296489 | 2026-06-20 |
| eBay range prezzo | std ~$12–$20; varianti XL $36–$43 | OBSERVED (snippet) | ebay.com/itm/205905333409 | 2026-06-20 |
- **Nota:** ordini fonte sul SKU specifico più bassi (245) ma corroborati dalla categoria; verificare il prezzo della variante standard (non XL).

### 5 · Baby Bath Thermometer (floating) — confidence media
- **Fonte:** AliExpress `3256811531686162` · costo **$6.26** · vendita **$14.99** · margine **~$6.34 (~42%) [ESTIMATE]**.
- **Titolo (78):** `Baby Bath Thermometer Floating Waterproof Water Temperature Gauge Safe Bath Tub` · **Desc:** `copy_2026-06-20/baby_bath_thermometer.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $6.26 | OBSERVED (search render) | aliexpress.com/w/wholesale-baby-bath-thermometer-float | 2026-06-20 |
| Ordini AliExpress | 10.000+ (lower bound), 4.9★ | OBSERVED | stessa pagina | 2026-06-20 |
| eBay prezzo (delivered) | ~$10–$20 ($16.91 / $19.18 visti) | OBSERVED (snippet) | ebay.com/itm/165791275514 | 2026-06-20 |
| eBay sold | presenza-vendite (lower bound), volume non confermato | OBSERVED/PRR | ebay.com/itm/236197650350 | 2026-06-20 |
- **Note:** categoria baby/sicurezza → copy come **aiuto, mai garanzia medica** (già nel draft); verificare immagine senza brand prima del publish.

### 6 · Resistance Bands Set (handles + door anchor) — confidence media, **MARGINE SOTTILE**
- **Fonte:** AliExpress `3256811843677080` · costo **$17.19** · vendita **$26.99** · margine **~$5.82 (~21%) [ESTIMATE]** (scende a ~10% con spedizione).
- **Titolo (74):** `Resistance Bands Set with Handles Door Anchor Ankle Straps Home Gym Workout` · **Desc:** `copy_2026-06-20/resistance_bands.html`
- **DATA BASIS:**

| Metrica | Valore | Etichetta | Fonte | Data |
|---|---|---|---|---|
| Costo fonte | $17.19 | OBSERVED (search render) | aliexpress.com/w/wholesale-resistance-bands-set-fitness | 2026-06-20 |
| Ordini AliExpress | 10.000+ (lower bound), 4.9★ | OBSERVED | stessa pagina | 2026-06-20 |
| eBay attivi | 10+ listing, più venditori | OBSERVED | ebay.com/itm/313180458674 | 2026-06-20 |
| eBay range prezzo | $9.72–$40.50 (set 11pz ~$18–$30) | OBSERVED (snippet) | ebay.com/itm/324890939577 | 2026-06-20 |
| eBay sold | UNKNOWN (muro filtro Sold) | PUBLIC RESEARCH REQUIRED | ebay sold filter | 2026-06-20 |
- **⚠️ Raccomandazione:** a $17.19 di costo il margine è sottile. **Cercare una variante AliExpress più economica ($9–12 esistono) o prezzare a $29.99+** prima di listare. Il più debole dei 6.

## Perché 6 e non 10 — gli scartati (motivo dominante: dato non tracciabile)
Il gate avversariale ha bocciato 10 candidati. Sintesi:

| Prodotto | Motivo principale |
|---|---|
| Car Headrest Hook Organizer | titolo 81 char + fonte = pagina search (no item) + costo su SKU diverso (2-pack vs 4-pack) |
| Silicone Stretch Lids 6pc | costo/domanda dalla search-page, non riconducibili all'item importabile |
| High-Pressure Shower Head | costo $11.63 non letto dall'item (CAPTCHA), citazioni a URL mai aperti |
| Toothpaste Tube Squeezer | domanda (10k) appartiene a un SKU $12.05, ma l'import era SKU $1.70 (62 sold) → decoupling |
| Foldable Aluminum Laptop Stand | costo/ordini attribuiti a item mai aperto |
| Sink Drain Strainer | **margine NEGATIVO** (sell $9.99 vs costo 10-pack $13.68) + pack mismatch |
| Foldable Car Trunk Organizer | dato non legato all'item + nicchia già toccata |
| Precision Screwdriver Bit Set | titolo 82 + **margine NEGATIVO** ($27.42 costo) |
| Electric Callus Remover | costo $3.93 non confermato sull'item |
| Tongue Scraper Set | item page 429 (non importabile confermato) + dato alla search-page |

**Lezione:** il muro CAPTCHA delle pagine-prodotto AliExpress è il vincolo strutturale. I 6 passati hanno corroborazione multipla (search render + segnali eBay) che li rende i più difendibili; gli altri no.

## Comandi import (SOLO sotto GO_IMPORT_5_DRAFTS — e con caveat AutoDS degradato)
Dalla cartella `…/integrations/autods/playwright/`. **PRIMA dell'import:** riconfermare in AutoDS costo reale + stock di ogni SKU (il monitoraggio AutoDS è degradato).
```bash
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full --url "https://www.aliexpress.com/item/3256806823944476.html" --match "book light|reading" --title "Clip On Book Light Rechargeable LED Reading Lamp Dimmable Flexible Eye Care" --desc-file "<repo>/05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/copy_2026-06-20/clip_book_light.html"
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full --url "https://www.aliexpress.com/item/1005007306587993.html" --match "water bottle|collapsible|silicone" --title "Collapsible Silicone Water Bottle Foldable Leak-Proof Travel Sports BPA-Free Cup" --desc-file ".../collapsible_water_bottle.html"
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full --url "https://www.aliexpress.com/item/1005007805413884.html" --match "squeegee|wiper" --title "Silicone Shower Squeegee Streak-Free Wiper for Glass Doors Mirrors Tiles + Hook" --desc-file ".../shower_squeegee.html"
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full --url "https://www.aliexpress.com/item/1005010052499206.html" --match "dog water bowl|floating|no spill" --title "No Spill Dog Water Bowl Floating Disk Anti Splash Slow Drink Stainless Steel" --desc-file ".../dog_water_bowl_nospill.html"
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full --url "https://www.aliexpress.com/item/3256811531686162.html" --match "bath thermometer|baby" --title "Baby Bath Thermometer Floating Waterproof Water Temperature Gauge Safe Bath Tub" --desc-file ".../baby_bath_thermometer.html"
# Resistance bands: prima trovare variante piu' economica o prezzare $29.99+ (margine sottile a $17.19)
```

## Raccomandazione (regola §8)
- **Verdict:** 6 prodotti draft-ready con dati corroborati; 4 mancano al "10" perché i dati non erano tracciabili (non li gonfio).
- **Recommended move:** procedere con i **5 forti** (book light, water bottle, squeegee, dog bowl, baby thermometer); resistance bands solo dopo aver trovato un costo più basso. Import = GO; e i costi reali vanno verificati in AutoDS al momento dell'import (monitoraggio degradato).
- **Per arrivare a 10:** o un 2° giro di ricerca (colpirà lo stesso muro CAPTCHA → resa simile), o l'owner fornisce URL AliExpress specifici di prodotti che vuole (così salto il muro).

## STATO IMPORT (2026-06-20, GO owner)
- ⚠️ Sessione AutoDS era scaduta (Google-SSO) → **ripristinata con login manuale owner** (E-004 fix nel login script). `manage_draft status` = numero ✓.
- ✅ **5 IMPORTATI come DRAFT** (AliExpress) con titolo ≤80 + descrizione VeRO-safe applicati e **verificati** (×5):
  - Book Light `6a36f3e934ccb3112fdcf3a2` · Water Bottle `6a36f440bdd8f0f8c4fd3f2a` · Squeegee `6a36f4671ea3c3e963fd35fa` · Dog Bowl `6a36f48ebdd8f0f8c4fd3f30` · Thermometer `6a36f4b66b71e506fe2aabd4`.
  - Nota: titoli/descrizioni applicati con set-title/set-desc separati (scrape-lag) + **guard per-draft** (dopo che un primo giro senza guard aveva rischiato di scrivere su draft sbagliati — verificato: nessuna contaminazione persistita).
- ⏸️ **Resistance Bands NON importato** (margine sottile a $17.19 — in attesa di fonte più economica).
- ⛔ **Publish = GO separato** + il publish AutoDS resta instabile (vedi cockpit); prima del publish riconfermare costo reale AutoDS di ogni SKU.

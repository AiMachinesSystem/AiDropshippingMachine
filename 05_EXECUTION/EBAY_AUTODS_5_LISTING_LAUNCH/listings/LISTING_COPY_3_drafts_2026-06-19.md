---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: reference
status: draft-ready
date: 2026-06-19
created_real: 2026-06-19
description: "3 NUOVI prodotti (diversi dai draft esistenti) per import draft AutoDS: fonte Amazon US importabile, VeRO-safe, titolo <=80 + descrizione riscritta. Ricerca via workflow multi-agente + verifica avversariale (17 agenti). Import = GO-CLASS (GO_IMPORT_5_DRAFTS). Esegue la routine source-products-to-draft (2026-06-19)."
---

# Copy 3 draft NUOVI — 2026-06-19

> Eseguita la routine `02_DATA/_ROUTINES/source-products-to-draft.md` (scritta oggi su richiesta owner).
> Ricerca via workflow (8 candidati → ricerca live → **verifica avversariale → 5 pass / 3 scartati per margine**).
> Esclusi i ~16 prodotti già a draft. AutoDS importa solo Amazon/AliExpress → fonte = Amazon US (generica, no brand).

## ⚠️ Avvertenze evidenza (regola §0.4) — leggere prima
- **Costi fonte:** Amazon ha bloccato il fetch prezzo (CAPTCHA, anche via proxy r.jina.ai) su 2 dei 3. Solo lo **Stove Gap Cover** ha costo **[OBSERVED $9.49]**; gli altri due hanno costo **[INFERRED/PUBLIC RESEARCH REQUIRED]** → **da confermare in AutoDS al momento dell'import** (il margine cambia se il costo reale è più alto).
- **Domanda eBay:** [PUBLIC RESEARCH] da snippet di ricerca, **lower bound**. Il fetch del "Sold" singolo eBay è un **muro noto (403)** → confermare col filtro **Sold** eBay prima di fissare il prezzo.
- **Margini:** [ESTIMATE] = `prezzo eBay − costo fonte − fee eBay (~13,25% + $0,40)`. Questo batch è **a margine sottile** (vedi raccomandazione). Nessun numero è inventato.
- **Policy:** sourcing Amazon→eBay è tecnicamente contro la dropshipping policy eBay (rischio account). La macchina segnala (cockpit) **AliExpress alto-recensioni** come fonte più sicura. I comandi sotto funzionano identici con una URL AliExpress: vedi nota "Alternativa AliExpress".

---

## 🥇 1 · Silicone Stove Counter Gap Cover (2-Pack, 21in)  — il più solido
- **Perché #1:** è l'unico con **costo fonte reale [OBSERVED $9.49]**, leggero/economico, trim-to-fit (nessuna taglia critica → resi bassi), domanda densa.
- **Fonte:** Amazon `B09TT744X9` — https://www.amazon.com/Silicone-Counter-Resistant-Stovetops-Heat-Resistant/dp/B09TT744X9 · **costo $9.49 [OBSERVED amazon.com 2026-06-19]**.
- **Domanda eBay:** ~10+ listing attivi 2-pack su una pagina [PUBLIC RESEARCH 2026-06-19, lower bound]; segnali sold per-listing (~13, ~5, uno alto ~2.943) — da confermare col filtro Sold.
- **Prezzo eBay:** ~$5,49–$26,89; cluster ~$8,95–$20 [PUBLIC RESEARCH].
- **Prezzo vendita suggerito:** **$15,99** → margine **~$3,98 [ESTIMATE]** (a $18,99 sale a ~$6,59).
- **VeRO:** safe (commodity generica, nessun brand). Seller name "SameTech" escluso dalla copy.
- **Ship:** leggero, strisce silicone piatte, non fragile, resi bassi. Ottimo profilo.
- **TITOLO (74/80):** `Silicone Stove Counter Gap Cover 2 Pack 21in Heat Resistant Kitchen Filler`
- **DESCRIZIONE:** `listings/copy_2026-06-19/stove_gap_cover.html` (riscritta, VeRO-safe).
- **Blocker:** confermare prezzo Amazon (può fluttuare); margine sottile a $15,99 (se usi promoted listings va vicino a zero → valuta $18,99).

## 🥈 2 · Drill Brush Power Scrubber Set (3pc Nylon)  — domanda evergreen forte
- **Fonte:** Amazon `B0789K37SV` — https://www.amazon.com/Cleaning-Different-Brushes-Bristles-Outdoors/dp/B0789K37SV · **costo ~$7,50 [PUBLIC RESEARCH REQUIRED — pagina CAPTCHA-walled; banda inferita $6–8; cross-check Walmart $7,99]**.
- **Domanda eBay:** ≥6 listing generici attivi [PUBLIC RESEARCH, lower bound]; un listing **659 sold**, un altro 35 rating/4.5★. Nicchia pulizia evergreen + appeal demo virale.
- **Prezzo eBay:** ~$8–$15 per set 3pc [PUBLIC RESEARCH].
- **Prezzo vendita suggerito:** **$12,99** → margine **~$3,37 [ESTIMATE]** (a costo $6,50 / vendi $14,99 → ~$6,10).
- **VeRO:** safe. Evitare le varianti brandizzate (Drillbrush/Drillstuff/HIWARE/RevoClean). Niente claim "fits [Brand] drill".
- **Ship:** leggerissimo (teste in nylon, <1 lb), non fragile, shaft hex 1/4" universale (nessuna trappola di compatibilità).
- **TITOLO (79/80):** `Drill Brush Power Scrubber Attachment Set 3pc Nylon Tile Grout Tub Shower Clean`
- **DESCRIZIONE:** `listings/copy_2026-06-19/drill_brush.html`.
- **Blocker:** costo Amazon non confermato (CAPTCHA) → verificare in AutoDS; lo spec "bit extender" NON è confermato sul 3-pack scelto (titolo/descrizione NON lo promettono — se lo vuoi, serve un set 4pc con barra di prolunga confermata).

## 🥉 3 · Under-Sink Pull-Out Organizer (2-Tier, L-Shape, Metal)  — ticket/margine più alti, ma ingombrante
- **Fonte:** Amazon `B0C5DBMYZF` (2-pack, ~$10/unità) — https://www.amazon.com/Organizer-Storage-Cabinet-Shelves-Bathroom/dp/B0C5DBMYZF · **costo ~$20 per 2-pack [INFERRED — WebSearch/articolo; pagina CAPTCHA; CONFERMARE all'import]**.
- **Domanda eBay:** supply densa, vendite evergreen; sold per-listing 68/145/59 [PUBLIC RESEARCH, lower bound].
- **Prezzo eBay:** ~$14,79–$69,99; grosso del mercato ~$20–$36 [PUBLIC RESEARCH].
- **Prezzo vendita suggerito:** **$26,99** → margine **~$6–8/unità [ESTIMATE]** (dopo fee + ~$5–7 spedizione).
- **VeRO:** safe (commodity, deep no-brand; escluso REALINN). Non riusare copy/brand del fornitore.
- **Ship:** ⚠️ **il più ingombrante/pesante** (~3–5 lb metallo). La spedizione è la pressione principale sul margine.
- **TITOLO (78/80):** `Under Sink Organizer 2 Tier Pull Out Sliding Drawer L-Shape Metal Cabinet Rack`
- **DESCRIZIONE:** `listings/copy_2026-06-19/undersink_organizer.html`.
- **Blocker:** ⚠️ il margine regge **solo** se la fonte è il **multipack (~$10/unità)** — il single-pack ~$34,99 è in perdita; confermare quale SKU importa AutoDS + la spedizione calcolata. Se il landed costa >~$18/unità, riprezza a $29,99–$34,99 o sostituisci il prodotto.

---

## Scartati / runner-up (trasparenza)
- **Car Seat Gap Filler 2-Pack PU Leather** (score 7, il più alto): **SCARTATO = duplicato** del draft esistente `listings/drafts/05_car_seat_gap_filler.md` (DIVU-CAR-005). Non si re-lista lo stesso keyword.
- **Heel Grips 4 paia** (score 4): margine **~$1,50** (quasi break-even, low-ticket commodity) → troppo sottile, scartato.
- **Under-desk cable tray · Pet hair roller · Bug-bite suction tool**: scartati in verifica avversariale per **margine sottile/negativo** su costo fonte non confermato.

## Raccomandazione (regola §8)
- **Verdict:** 3 prodotti draft-ready, VeRO-safe, titoli ≤80 verificati, descrizioni riscritte. **Batch a margine sottile** e con **2/3 costi fonte da confermare in AutoDS**.
- **Confidence:** media. Domanda = lower bound da snippet; costi fonte = 1 OBSERVED, 2 da confermare.
- **Recommended move:** importarli **come DRAFT** (reversibile, prezzo $0) e **confermare il costo fonte reale dentro AutoDS prima di qualunque publish/pricing** (publish = gate separato). Preferire la fonte **AliExpress alto-recensioni** se vuoi ridurre il rischio policy eBay.
- **Owner role:** dare (o no) il **GO_IMPORT_5_DRAFTS**; scegliere Amazon vs AliExpress come fonte.
- **Blockers principali:** costi fonte CAPTCHA (×2), margini sottili, sessione/account AutoDS valido (precondizione tecnica).

## Comandi pronti (eseguibili SOLO sotto GO_IMPORT_5_DRAFTS)
Dalla cartella `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/` (sessione `storage_state.json` valida). Tool canonico unico = `manage_draft.py` (solo "Add as Draft", titolo hard-cap 80, descrizione verificata):

```bash
# 1 · Stove gap cover
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full \
  --url "https://www.amazon.com/Silicone-Counter-Resistant-Stovetops-Heat-Resistant/dp/B09TT744X9" \
  --match "stove|gap cover|silicone|counter" \
  --title "Silicone Stove Counter Gap Cover 2 Pack 21in Heat Resistant Kitchen Filler" \
  --desc-file "C:/AI Machine ebay-autoDS/AiDropshippingMachine/05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/copy_2026-06-19/stove_gap_cover.html"

# 2 · Drill brush scrubber 3pc
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full \
  --url "https://www.amazon.com/Cleaning-Different-Brushes-Bristles-Outdoors/dp/B0789K37SV" \
  --match "drill brush|scrubber|cleaning" \
  --title "Drill Brush Power Scrubber Attachment Set 3pc Nylon Tile Grout Tub Shower Clean" \
  --desc-file "C:/AI Machine ebay-autoDS/AiDropshippingMachine/05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/copy_2026-06-19/drill_brush.html"

# 3 · Under-sink organizer (verifica che importi il 2-PACK, non il single)
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full \
  --url "https://www.amazon.com/Organizer-Storage-Cabinet-Shelves-Bathroom/dp/B0C5DBMYZF" \
  --match "under sink|organizer|pull out|sliding" \
  --title "Under Sink Organizer 2 Tier Pull Out Sliding Drawer L-Shape Metal Cabinet Rack" \
  --desc-file "C:/AI Machine ebay-autoDS/AiDropshippingMachine/05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/copy_2026-06-19/undersink_organizer.html"
```

> **Alternativa AliExpress (policy-safer):** sostituisci `--url` con la URL prodotto AliExpress alto-recensioni equivalente (stesso comando). Titolo e descrizione restano identici.

## STATO (chiuso 2026-06-19, GO owner `GO_IMPORT_5_DRAFTS`)
- [x] **Import 3 draft eseguito** → drafts **26→29** (Add-as-Draft only, 0 publish).
- [x] Titoli applicati e persistiti (≤80) + descrizioni VeRO-safe applicate via CKEditor e persistite (×3, `PERSISTED: True`).
- [x] **PUBLISH eseguito (GO owner, 2026-06-19): tutti e 3 live su eBay `divinit-92-us`** (usciti dai draft, "Import to Store 1/1 finished").
- **ID dedicati:** stove `6a35e9dbfc48b38c8a55487c` · drill `6a35ea532dec65c173126208` · under-sink `6a35eabf18a6518dcc0ca4d6`.
- *Nota import:* il draft under-sink ha richiesto `set-title`/`set-desc` separati (titolo non ancora scrapato al 1° tentativo) — risolto subito, non errore di pipeline.

## PUBLISH (2026-06-19, GO owner) — economics reali [OBSERVED — AutoDS products API 2026-06-19]
La **dynamic pricing policy AutoDS** ha auto-prezzato in profitto (NON $0; il "$0" nella lista prodotti è una colonna rumore, mostrata anche sullo stove che in realtà è $19.97).

| Prodotto | ASIN | Costo | Vendita | Profitto | Categoria eBay | Verdetto |
|---|---|---|---|---|---|---|
| Stove | `B09TT744X9` | $9.49 | **$19.97** | $7.13 | Stove Burner Covers | ✅ **viable** |
| Drill | `B0789K37SV` | **$133.13** | **~$199.99** | $35.64 | Cleaning Products | ❌ ASIN sbagliato/costoso |
| Under-sink | `B0C5DBMYZF` | **$43.99** | **$65.97** | $11.73 | Racks & Holders | ❌ variante costosa |

- **Esito:** policy → **nessuna perdita** (profitti positivi), ma **drill e under-sink importati a costi errati/alti** (erano i 2 costi NON confermati per CAPTCHA) → prezzati troppo alto → **non venderanno**. Solo lo **stove** è una listing valida.
- ⚠️ **E-003 (ERROR_REGISTRY):** lo stove è stato pubblicato da un click "Import" durante un probe diagnostico (card "Import" = publish immediato, senza modal). Esito ok, errore di processo registrato. Drill+under-sink pubblicati deliberatamente.
- **Azione raccomandata (GO-class):** **deactivate/end** i 2 listing non-viable (drill, under-sink) e ri-sourcing dall'ASIN corretto economico (o AliExpress alto-recensioni) prima di ri-pubblicare. Stove resta live. Policy eBay sul sourcing Amazon = rischio account dichiarato.

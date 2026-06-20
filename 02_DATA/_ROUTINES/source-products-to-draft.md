---
tags:
  - machine
  - routine
type: playbook
status: active
date: 2026-06-19
created_real: 2026-06-19
description: "Routine owner: 'ricerca N prodotti e mettili in draft'. Pipeline canonica end-to-end — ricerca winner (fonte importabile AutoDS) → import draft + titolo <=80 + descrizione VeRO-safe riscritta. Codifica la richiesta owner del 2026-06-19 cosi' non si riscrive da capo ogni volta."
---

# Routine — Source N Products → AutoDS Draft

Routine riusabile per l'intento ricorrente owner: **"ricerca N prodotti e mettili in draft, titolo <=80 + descrizione riscritta"**.
Da qui in poi l'owner dice solo l'intento (es. *"ricerca 3 prodotti e mettili in draft"*) e la macchina esegue questa routine senza ridefinire nulla.

## Trigger (dispatcher)
"ricerca N prodotti e mettili in draft" · "trovami N winner e mettili a draft" · "N nuovi draft" · "fai N draft nuovi (titolo <=80 + descrizione)".
Registrata in `02_DATA/_ROUTINES/MASTER_ROUTINE.md` (INTENT MAP).

## Input
- **N** = numero prodotti (default 3 se non detto).
- **Fonte** = Amazon US (default) oppure AliExpress. **VINCOLO DURO:** AutoDS importa SOLO Amazon + AliExpress → ogni prodotto deve avere una URL prodotto Amazon/AliExpress reale. **Temu NON e' importabile** (resta sourcing manuale → [[temu-manual-sourcing]]).
- **Nicchia** (opzionale) = se l'owner indica un tema; altrimenti gadget problem-solving generici.

## Profilo prodotto (selezione)
Preferisci: gadget problem-solving · leggero/economico da spedire · bassi resi · **VeRO-safe (nessun brand/personaggio)**. **Evita** abbigliamento (taglie/resi), oggetti fragili e compatibilita' critica (es. window cleaner = piu' resi).

## Procedura (5 step)

1. **Anti-duplicato.** Leggi i draft gia' esistenti (`05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/drafts/*.md`, i `LISTING_COPY_*` e `TEMU_MANUAL_SHORTLIST_*`) ed escludi i prodotti gia' lavorati. I nuovi N devono essere diversi.

2. **Ricerca + validazione domanda (interno, autonomo).** Per ogni candidato:
   - **Domanda:** proxy di domanda da recensioni/sold (Temu/Amazon review count come proxy, eBay sold/active range). [PUBLIC RESEARCH] / [OBSERVED — url+data]. Conteggi = lower bound. Fetch "Sold" singolo eBay = muro noto → usa range + nota "confermare col filtro Sold".
   - **Fonte + costo:** URL prodotto Amazon/AliExpress + costo [OBSERVED — url+data]. Costo volatile → "riverifica live prima di importare".
   - **Margine** [ESTIMATE dichiarato]: `prezzo eBay − costo fonte − fee eBay (~13,25% + $0,40)`.
   - **VeRO check:** titolo e descrizione senza brand/trademark/personaggi.

3. **Copy (regola listing — [[listing-title-description-rule]]).** Per ogni prodotto:
   - **Titolo <=80 char** (verificato, keyword-rich, brand-free). `manage_draft.py` rifiuta titoli >80.
   - **Descrizione SEMPRE riscritta** da zero, benefit-led, VeRO-safe (mai la scrapata).

4. **Output interno.** UN file datato `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/LISTING_COPY_<N>_drafts_<data>.md`: per prodotto = domanda, fonte+costo, prezzo eBay, margine, VeRO, titolo (len), descrizione. + i comandi `manage_draft.py full` pronti. Refresh cockpit (MASTER_DASHBOARD + NEXT_ACTIONS) per regola AUTO-REFRESH.

5. **Import draft (GO-CLASS — STOP & ASK).** Il write su AutoDS e' azione live: si esegue SOLO con GO esplicito owner, citando il gate **`GO_IMPORT_5_DRAFTS`** ([[GO_GATES]]). Tool unico canonico (niente script one-off):
   ```
   PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py full \
     --url <amazon/aliexpress URL> --match "<regex titolo scrapato>" \
     --title "<titolo <=80>" --desc-file <copy.html>
   ```
   (cartella `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/`). Solo "Add as Draft" — mai publish/prezzi/ordini (gate separati). Vedi [[autods-draft-management]].
   > Precondizione pratica: sessione AutoDS valida (`storage_state.json`) e account attivo. Se la sessione e' scaduta, rilancia `login_and_save_session.py` (GO-class) — senza ri-litigare decisioni di account.
   > **Recovery noto (scrape-lag, verificato 2026-06-19):** se `full` stampa `[MISS] no draft title matches` subito dopo l'import, il titolo fornitore non era ancora stato scrapato. **NON ri-eseguire `full`** (creerebbe un duplicato): lista i draft (`_list_drafts.py` usa-e-getta o `find-id`), prendi l'id del nuovo draft, poi applica a parte `set-title --match "<frammento unico del titolo scrapato>"` e `set-desc --id <id> --desc-file <f>`.
   > **CRITICO — verifica costo reale prima del publish (lezione 2026-06-19):** il **costo che AutoDS scrapa può divergere ENORMEMENTE** dalla stima di ricerca (es. drill brush: stima ~$7.50 → costo AutoDS reale **$133.13**; AutoDS può agganciare un ASIN/variante/bundle sbagliato). Se la fonte ha avuto il prezzo bloccato da CAPTCHA in ricerca, **leggi il costo reale dalla `/products` API AutoDS PRIMA di pubblicare**: la dynamic pricing policy pubblica comunque (in profitto, non a $0), ma a un prezzo assurdo se il costo è sbagliato → listing che non vende. Niente publish finché il costo reale non è sano.
   > **PUBLISH = azione live (`GO_PUBLISH_5`), card "Import" pubblica IMMEDIATO senza conferma** ([[ERROR_REGISTRY]] E-002/E-003): pubblica un draft alla volta, ancorato al titolo, con assert `card_title == target` prima del click; mai "Import All".

## Confini (regole §0)
- Step 1-4 = **INTERNI**: la macchina li fa in autonomia, fino al pacchetto draft-ready.
- Step 5 = **GO-CLASS**: stop al gate, GO citato. L'approvazione non si trasferisce ad azioni successive (publish/prezzi/ordini restano i loro gate).
- Evidenze sempre etichettate; mai numeri inventati; policy eBay su sourcing da marketplace dichiarata, non nascosta.

## Collegamenti
- Regola copy: [[listing-title-description-rule]] · Tool import: [[autods-draft-management]] (`manage_draft.py`) · Sourcing Temu manuale: [[temu-manual-sourcing]] · Gate: [[GO_GATES]] · Dispatcher: `MASTER_ROUTINE.md`.
- Run sorgente di questa routine: richiesta owner 2026-06-19 ("ricordatela come routine").

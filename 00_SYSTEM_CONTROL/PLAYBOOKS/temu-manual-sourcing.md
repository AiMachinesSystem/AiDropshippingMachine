---
tags:
  - machine
type: entity
status: active
date: 2026-06-17
description: "Playbook: ricerca winner Temu per dropshipping MANUALE su eBay (Temu non e fornitore AutoDS). Demand da recensioni/sold, costo Temu reale, prezzo eBay range, margine stimato, copy eBay pronta (titolo<=80 + descrizione VeRO-safe). Codifica il run del 2026-06-17."
---

# Temu Manual Sourcing (eBay)

Workflow della macchina per trovare prodotti winning su **Temu** e listarli **a mano** su eBay US, quando il sourcing automatico via AutoDS non e disponibile.

## Quando usarlo
- L'owner chiede prodotti da Temu / "winner Temu" / dropship manuale da Temu.
- Serve validare domanda + margine prima di listare a mano su eBay.
- NON usarlo per import AutoDS: vedi gate sotto.

## Gate zero — fornitore supportato (verificare SEMPRE prima)
AutoDS sul nostro account importa SOLO **AliExpress + Amazon** [OBSERVED — modale "Add product with link", check 2026-06-17; tool `check_supported_suppliers.py`]. **Temu NON e importabile** → ogni prodotto Temu e dropship MANUALE: liste, ordini, stock e prezzo li gestisce l'owner; nessun sync AutoDS.
> Riverificare il gate se AutoDS aggiunge Temu (forum AutoDS citava un rilascio): rilancia `check_supported_suppliers.py`.

## Procedura
1. **Demand su Temu** — fetch delle pagine CATEGORIA Temu (`temu.com/<keyword>-...-s.html`): mostrano prezzo + n. recensioni per prodotto. Recensioni alte (migliaia) = domanda validata [OBSERVED]. Le pagine PRODOTTO (`...-g-<id>.html`) spesso NON rendono prezzo/recensioni via fetch.
2. **Costo Temu** — prendi il range di prezzo dalla categoria. E [OBSERVED] ma volatile (coupon/quantita) → **riverifica live prima di listare**.
3. **Prezzo eBay** — ricerca eBay del prodotto: range prezzi attivi + sold count. Il fetch del singolo prezzo "Sold" e un **muro noto** (eBay blocca/timeout) → resta [PUBLIC RESEARCH] range; confermare col filtro "Sold" eBay prima di fissare il prezzo.
4. **Margine** [ESTIMATE dichiarato]: `prezzo eBay − costo Temu − fee eBay (~13,25% + $0,40)`. Temu spedisce gratis al cliente (US); handling time onesto su eBay (Temu ~1-2 settimane).
5. **Selezione** — preferisci: gadget problem-solving · leggeri/economici da spedire · bassi resi · VeRO-safe (nessun brand). **Evita abbigliamento** (taglie/resi) e oggetti fragili/compatibilita critica (es. window cleaner = piu resi).
6. **Copy eBay** — per ogni prodotto scelto: **titolo <=80 char** (verificato) keyword-rich, e **descrizione SEMPRE riscritta** VeRO-safe (mai la scrapata). Vedi [[listing-title-description-rule]] / regola listing.
7. **Output** — UN file shortlist datato in `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/TEMU_MANUAL_SHORTLIST_<data>.md`: per prodotto = demand, costo Temu, prezzo eBay, margine, VeRO, titolo, descrizione. Raccomandazione finale rankata.

## Evidenze (regola §0.4)
Costi Temu = [OBSERVED — url + data]; prezzi eBay = [PUBLIC RESEARCH range]; margini = [ESTIMATE con assunzioni]. Mai numeri inventati. Recensioni/sold = lower bound dichiarati.

## Policy (dichiarare, non nascondere)
Vendere su eBay con sourcing da marketplace consumer (Temu, come Amazon/AliExpress) e tecnicamente contro la dropshipping policy eBay → rischio account. La shortlist e interna; il publish/listing live e decisione + azione dell'owner (GO-class).

## Muri noti
- AutoDS non importa Temu (gate zero).
- Fetch prezzo "Sold" eBay = bloccato → usare range + filtro Sold manuale.
- Pagine PRODOTTO Temu spesso non rendono prezzo via fetch → usare pagine CATEGORIA.

## Collegamenti
- Run sorgente: `05_EXECUTION/.../listings/TEMU_MANUAL_SHORTLIST_2026-06-17.md`
- Tool: `integrations/autods/playwright/check_supported_suppliers.py`
- Regola copy: [[listing-title-description-rule]] · convenzioni: [[VAULT_CONVENTIONS]]
- Pipeline import AUTOMATICO (AliExpress/Amazon): `import_drafts.py` + `apply_titles_3.py` + `apply_desc_ckeditor_3.py`

# Publish outcome — batch 4 (2026-08-28 ~02:55Z)

Verdict: **14 nuovi listing LIVE** · **6 bloccati item-specific (tutti hard-block: dato assente dal titolo)** · 0 errori.

## LIVE (14, status=PUBLISHED)

| SKU | listingId | prodotto | categoria |
|---|---|---|---|
| US-B08HCMKN8P | 407175704637 | 50" electric fireplace | 175756 |
| US-B002WP1R1W | 407175705189 | Indoor/outdoor golf mat | 50876 |
| US-B0063879QQ | 407175706232 | Roller city panniers | 177833 |
| US-B07SQH3FCT | 407175706476 | Cooling gel dog bed | 20744 |
| US-B07JYW65Y5 | 407175706696 | Hanging glass tealight holders (100pcs) | 16102 |
| US-B07WD9YQZG | 407175707159 | Cast aluminum post light 24" | 94940 |
| US-B0DBYLD9WY | 407175708436 | Area rug 8x10 | 262983 |
| US-B0GHNFQGN1 | 407175708672 | Rolling ice chest | 79691 |
| US-B08HCMQ1H6 | 407175708886 | 36" electric fireplace | 175756 |
| US-B07YF74Z4T | 407175709060 | Dog gate 144" (door) | 117029 |
| US-B07YF53FFD | 407175709247 | Dog gate 144" (door, white) | 117029 |
| US-B07ZTFVZXJ | 407175709439 | Rolling tool chest 40" | 33089 |
| US-B00K027D0S | 407175709623 | Orthopedic memory foam pet bed | 20744 |
| US-B001ESO9KO | 407175709840 | Jumbo memory foam dog bed | 20744 |

## BLOCKED (6, item-specific assente nel titolo → hard block)

| SKU | categoria | richiesto | perché non inferibile |
|---|---|---|---|
| US-B0D59WHNGP | Beds & Bed Frames 175758 | Compatible Mattress Size → **Frame Material** | "King Size Bed Frame" ha King ma non il materiale del telaio |
| US-B07MBFMG5W | Mirrors 20580 | Item Length | "Decorative Wall Mirror" — nessuna dimensione |
| US-B074W2DT3N | Gloves & Mittens 62172 | Color | "Heated Gloves for Men Women" — nessun colore |
| US-B071X64XQX | Gloves & Mittens 62172 | Color | (duplicato, stesso titolo) |
| US-B072N2BSGD | Gloves & Mittens 62172 | Color | (duplicato, stesso titolo) |
| US-B09VX9MGX7 | Pan Sets 98847 | Stove Type Compatibility | "18/10 Stainless Steel Cookware" — nessun tipo fornello |

## Finding strutturale (rafforza il pattern up-ticket)

1. **Failure rate 30% (6/20), e 6/6 sono HARD BLOCK** — l'item-specific richiesto NON è
   nel titolo. Il title-inference (Material/Color/Size/Firmness) copre solo una frazione.
2. **Gli item-specific sono categoria-specifici e imprevedibili**: Beds="Compatible Mattress
   Size"+"Frame Material", Mirrors="Item Length", Gloves="Color", Pan Sets="Stove Type
   Compatibility". Nessun mapping generico "Size"→eBay vale: ogni categoria ha i SUOI nomi.
3. **Il draft AutoDS porta solo title/category/price/image** — NESSUN campo spec. Verificato
   sui keys del draft: nessuna descrizione, nessuna dimensione, nessun materiale/colore.
4. **Leva vera (non il title-inference): fetch della pagina Amazon via `sell_site_url`.**
   La tabella spec della product page Amazon (Item Dimensions, Color, Material, Stove Type)
   contiene ESATTAMENTE i dati che eBay chiede. AutoDS non li salva, ma l'URL c'è.
5. **Il bed frame ha mostrato il discovery a catena**: "Compatible Mattress Size"=King (sbloccato
   con -B) → poi "Frame Material" (assente) → hard block. Conferma il SET non uno.

## Ceiling onesto verso 999

Pool draft = **423 candidati** superano il gate net-profit (sell≥$50, net≥$30). A ~30% di
hard-block item-specific, il soffitto reale dal pool attuale è **~300 listing publishable
(~45 già live)**, NON 999. Per superarlo servono in ordine:
(a) **fetch spec Amazon** per i ~120 bloccati (leva #1, $0, interna);
(b) **pool sorgente più grande** (nuovi draft AutoDS / partner wholesale — delegato a DATA);
(c) **scope Taxonomy** sul token OAuth (serve elenco item-specific + enum validi; è un GO live).

## Cosa è cambiato nel codice

- `tools/build_more.py`: aggiunti `SIZE_MAP` + `FIRMNESS_MAP` con gate `_bedding_context`
  (inferisce Size/Firmness solo in contesto bedding/towel/rug). Conservativo: nessuna
  inferenza dimensionale (Length/Width/Height = fabricazione se parziale).
- `publish-batch-4.sh`: batch dinamico (dry-run → sha → 3 fasi, non aborta sui singoli).

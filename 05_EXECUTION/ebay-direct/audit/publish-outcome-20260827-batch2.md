# Publish outcome — batch 2 (2026-08-27 ~21:55Z)

Verdict: **14 nuovi listing LIVE · goal "altri10" SUPERATO · 3 offer UNPUBLISHED (item specific) · 5 scartati pre-publish.**

## LIVE (14, status=PUBLISHED verificato read-only via Sell Inventory API)

| SKU | listingId | prodotto | categoria |
|---|---|---|---|
| US-B07F75FBNZ | 407174838681 | Pet fountain filters (8pcs) | 177789 |
| US-B08735MYHT | 407174839303 | Hooded baby bath towels | 45453 |
| US-B0915X5K6W | 407174839403 | Groove joint pliers 12" | 82251 |
| US-B098NTSJ6W | 407174839511 | Gaming mouse pad XXL | 23895 |
| US-B09B3K1K7N | 407174839552 | Toiletry bag | 36413 |
| US-B09KV8VD99 | 407174839610 | Wood chain / knot decor | 10034 |
| US-B0CXX3JDZ2 | 407174839695 | Keyboard wrist rest | 23895 |
| US-B0GL1BJKG9 | 407174839774 | Stainless steel face roller | 36449 |
| US-B091ZGB8RJ-C | 407174850704 | Peshtemal towel (Cotton/Gray/Hand Towel) | 40587 |
| US-B0CGZ95KFZ | 407174853700 | Canvas makeup bags (20pcs) | 36413 |
| US-B0B5QGCJ9J | 407174853857 | Mouse pad + wrist rest set | 23895 |
| US-B0BG1S6NNJ | 407174853995 | Gaming mouse pad 4-in-1 | 23895 |
| US-B09PYGBZ4R | 407174854124 | Classroom mailbox (30 pockets) | 25346 |
| US-B07YTYFHF1 | 407174854299 | Dry bag / floating backpack | 87089 |

## UNPUBLISHED (3, offer esistenti ma bloccate — item specific mancante)

| SKU | offerId | blocker |
|---|---|---|
| US-B08CM88MPR | 247400741011 | "Item Width" mancante (lunch bag; nessuna dimensione nel sorgente) |
| US-B091ZGB8RJ | 247400843011 | "Material" → "Size" mancanti (superseded da -C) |
| US-B091ZGB8RJ-B | 247404959011 | "Size" mancante (superseded da -C) |

Il token OAuth non ha scope Taxonomy ⇒ i valori validi degli item specific non sono
recuperabili via API. I valori inferiti dal titolo (Material=Cotton, Color=Gray,
Size=Hand Towel) hanno sbloccato il towel; il lunch bag resta bloccato (manca Width).

## Scartati pre-publish (5, nessuna offer creata)

| SKU | motivo |
|---|---|
| US-B08YGYMFVZ | "BURT'S BEES FOR PETS" — brand nel titolo, VeRO risk |
| US-B06XRHMH78 | "Spoontiques" brand + "Grandma s" (apostrofo perso nel sorgente) |
| US-B09YCPJL5V | categoria errata (fiber optic wands → Chandeliers) |
| US-B08GY2MSY3 | activewear → richiede Size/Color item specific |
| US-B07DZSTTNT | dry-run fallito in validazione (corner cushions) |

## Finding — pattern strutturale (per il loop)

1. **Item-specific failure ~17%** (3/17 tentativi). I manifest portano solo
   {Brand, Type} + Material/Color inferiti dal titolo. Categorie come Lunch
   Containers (Width), Towels (Size) e abbigliamento richiedono item specific
   assenti nel sorgente AutoDS (che ha solo title/category/price/image).
2. **Margine uniforme**: tutti i candidati ~$31.97 sell / ~$18.99 cost / ~$7.83 net
   = markup AutoDS uniforme ~1.68×. I "474 che passano il gate" non sono
   differenziati per profitto: stessa fascia sottile. La leva non è il singolo
   margine ma il volume + la selezione di categorie a bassa competizione.
3. **VeRO/brand**: clean_title rimuove solo il pattern "Brand - "; brand ALL-CAPS
   senza separatore (BURT'S BEES) e brand a inizio titolo senza dash restano.
4. **Skill del tool `tools/build_more.py`**: inferisce Material/Color dal titolo e
   salta gli ASIN già usati — riduce ma non azzera i failure item-specific.

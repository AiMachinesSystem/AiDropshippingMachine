---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: listing_prep
status: draft_prepared
date: 2026-08-17
created_real: 2026-08-17
item_id: 407113382755
---

# Listing prep — 407113382755 · Pool Chlorine Feeder (9 lb)

> **Stato:** preparazione INTERNA completata fino al gate live. Niente è stato applicato né
> pubblicato. Ogni campo live mancante è marcato e richiede il GO dedicato sotto.

## Scheda candidato

| Campo | Valore | Fonte / evidenza |
|---|---|---|
| item_id (live, rilistato 13/08) | 407113382755 | `top20_titles_rewritten.csv` [OBSERVED] |
| Prodotto | In-line automatic pool chlorine feeder, 9 lb, inground | titolo originale [OBSERVED] |
| Prezzo attuale | $82.97 | CSV top20 [OBSERVED] |
| Impressions / views | 1077 / 8 (CTR 0,74%) | CSV top20 [OBSERVED] |
| Categoria eBay | Pool Equipment Parts (181070) | catalogo luglio [OBSERVED] |
| Prezzo/costo luglio | $76.98 / $42.92 (net ~$22, 28.8%) | `catalog_2026-07-27.csv` [OBSERVED — STALE 27/07] |
| Ceiling sold-median nicchia | $39.31 | RESEARCH_MEMORY_INDEX [OBSERVED — STALE 28/06, >30gg] |

## 1 · Titolo (PRONTO, già riscritto)

> `Inline Automatic Pool Chlorine Feeder 9 lb Chlorinator Inground Tablet Dispenser` — **80/80 char**

- Front-loaded sulle keyword chiave (`Inline Automatic Pool Chlorine Feeder`) [VERIFIED — pattern winner pool].
- Brand-free: nessun marchio ("Hydrotools" rimosso/assente) [VERIFIED].
- "Tablet Dispenser" recuperato da Item Form degli specifics [INFERRED — dalla nota di riscrittura CSV, riga 4].
- Non troncato a metà parola (gate E-033) [VERIFIED — termina su "Dispenser"].

## 2 · Descrizione (VeRO-safe, PRONTA — copy EN)

> Copy per il marketplace (inglese americano). De-brand, benefit-led, zero claim non sostanziato.

```
Automatic In-Line Pool Chlorinator — 9 lb Capacity

Keep your inground pool water clean and clear with less daily work. This
automatic in-line chlorinator installs directly into your pool's return line
and feeds chlorine steadily, so the water stays treated without constant
attention.

- 9 lb capacity holds a large supply of tablets, meaning fewer refills
- In-line design connects straight into your existing pool plumbing
- Automatic feed keeps chlorine levels steady instead of up-and-down
- Built for inground pool systems

What's in the box
- 1 automatic in-line chlorinator (9 lb capacity)

Note
Compatible with standard pool plumbing. Always confirm your pool size and
plumbing fit before ordering.
```

- Ogni claim (9 lb, in-line, automatic, inground, chlorinator) è nel titolo originale del
  prodotto [VERIFIED]. Nessun brand/trademark citato [VERIFIED]. Nessuna prova finta (§0.8) [VERIFIED].
- "holds a large supply / fewer refills" = INFERENZA ragionevole da "9 lb capacity".

## 3 · Item specifics (GAP — serve pull reale)

Rilievo 13/08 su 75 listing con specifics: `Brand="Does not apply"` (73/75), MPN assente (75/75),
Type analogo, Model 71, Size 37 [OBSERVED — NEXT_ACTIONS 13/08]. Il candidato quasi certamente
ricade in questo pattern, ma **non ho in mano le sue specifics reali**: il pull del 13/08 non è
salvato in cache come file e il JSON di luglio (`products_live_2026-07-27`) non contiene item
specifics (solo `configuration` con location/shipping) [VERIFIED — ispezionato].

→ **Non scrivo/forzo specifics inventate** (E-031: pairing proof richiesto; §0.8: claim con fonte
o NOT USABLE). Il fix corretto richiede un pull fresco del listing da AutoDS.

## 4 · Prezzo (GAP — serve refresh sold-comp)

- $82.97 attuale è **sopra** il ceiling sold-median $39.31 — ma quel comp è del 28/06 (>30gg
  STALE) e potrebbe riferirsi a feeder di capacità inferiore. Il prezzo di listino reale del
  prodotto era $76–83 [OBSERVED catalogo].
- **Data-first:** non fisso un numero senza refresh dei sold-comp freschi del chlorinator 9 lb
  (playbook: "prezzo sopra sold-median = punito"). Il target va ancorato al nuovo sold-median.

## 5 · Gate live (STOP)

Non applico nulla finché non ho: (a) specifics reali del listing, (b) sold-comp freschi.

**Riga GO pronta — step 1 (pull dati, read-only):**
> GO: pull specifics del listing 407113382755 da AutoDS + refresh sold-comp eBay del chlorinator 9 lb.

I passi successivi (apply titolo+descrizione+specifics+prezzo, poi verifica API-census a freddo)
restano GO-gated, uno alla volta.

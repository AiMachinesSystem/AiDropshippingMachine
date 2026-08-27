# Finding — il gate di selezione era invertito (2026-08-27)

## Il fatto

`tools/build_more.py` selezionava i candidati con gate **a margine percentuale**:

```
if sell <= 0 or profit < 5 or (profit / sell) < 0.20: skip
```

La North Star della macchina è **NET PROFIT assoluto**, non %. Il gate al 20% ha
prodotto sistematicamente la **commodity** (~24% margine, ma ~$7.83 net su $31.97
sell) ed ha **escluso gli up-ticket** (~18% margine, ma $40–150 net su $200–832 sell).

È l'esatto inverso della conclusione registrata 3-4× nella ricerca passata
(2026-06-17 → 2026-07-27): la commodity è il "resto" che non vende (~0,7%
sell-through/mese, margine lordo ≈ canone AutoDS), e l'unica via di margine reale
sono gli **up-ticket funzionali** pool/pet/outdoor ($50-90+).

## La prova (pool AutoDS _drafts_full.json, 1587 ASIN dedup)

| banda | count | margine % | net tipico |
|---|---|---|---|
| commodity ($14-38) | ~472 | ~24% | ~$7.83 |
| **up-ticket ≥$60** | **689** | ~18% | **$40-150** |
| **up-ticket ≥$50** | **819** | ~18% | **$30-150** |
| **up-ticket ≥$40** | **1005** | ~18% | **$30-150** |

Filtrando col profilo winner (sell ≥$50, net ≥$30, margine ≥10%, no-brand):

- **421 item winner-profile** nel pool
- **357/421 brand-safe** (esclusi LUMBERJACK, Max & Lily, FLEXISPOT, KRAUS, Flying Pig, etc.)
- **239/357 funzionali** pool/pet/outdoor/kitchen — il profilo provato

## Il fix (applicato a `tools/build_more.py`)

1. Gate → net-profit assoluto: `sell >= 50 and profit >= 30 and profit/sell >= 0.10`.
2. Aggiunto `BRAND_BLOCK` (VeRO/trademark) + `has_brand()` → skip titoli brandizzati.

Output del nuovo gate (12 manifest generati): sell $268-374, net $48-67 → **6-9× il net
della commodity**, senza toccare il pricing (stesso markup AutoDS 1,68×).

## Limite non ancora superato

Il pool AutoDS è **retail Amazon→eBay**: il `min_profit` di AutoDS è calcolato su
prezzo Amazon + markup, NON sul prezzo di vendita reale su eBay. La ricerca passata ha
già falsificato il retail arbitrage a net ~$0 per la commodity generica
(`retail-dropship-margin-dead`), ma ha SEPARATAMENTE identificato negli up-ticket
funzionali (pool/pet specialisti) l'eccezione: lì il compratore eBay paga un prezzo che
regge sopra Amazon per funzionalità/specializzazione. Verificare la domanda eBay reale
(Terapeak/API = gap #1 registrato) resta il gate prima di scalare su questi up-ticket.

## Azione raccomandata

Pivot del publish dal commodity al **up-ticket funzionale generico** (dog bed, paddle
board, sauna, golf mat, pet gate, heated gloves, ice chest, landscape light). NON è un
cambio nicchia: stessa fonte (AutoDS), stesso pipeline, solo il filtro corretto che
esegue la strategia già registrata. Rischio residuo: item-specific più complessi
(dimensioni/materiale) sugli up-ticket — va misurato col primo batch.

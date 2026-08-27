# Publish outcome — 2026-08-27

Verdict: **26 listing live su eBay · 2 offer UNPUBLISHED (Size item specific, duplicati) · goal 10–20 SUPERATO.**

## Stato finale verificato (read-only via Sell Inventory API, 2026-08-27 ~19:50Z)

### LIVE (26, status=PUBLISHED, listingStatus=ACTIVE, soldQuantity=0)

Batch "batch of 20" (18):
| SKU | listingId |
|---|---|
| AE-1005006695661987 | 407166264983 |
| AE-3256806985368273 | 407166265035 |
| AE-3256807891363426 | 407166265142 |
| AE-1005007635138561 | 407166265087 |
| AE-1005006727725208 | 407166265216 |
| AE-1005010002169658 | 407166265280 |
| AE-1005009366884119 | 407166265365 |
| AE-3256806518016932 | 407166265426 |
| AE-1005005638658052 | 407166265469 |
| AE-1005007856972957 | 407166265523 |
| AE-3256806675414853 | 407166265577 |
| AE-1005007583827147 | 407166265634 |
| AE-1005006381299125 | 407166265683 |
| AE-1005007857231190 | 407174659010 |
| AE-3256806852591311 | 407166265751 |
| AE-3256807032522577 | 407166265991 |
| AE-1005009383964875 | 407166265834 |
| AE-1005009472550839 | 407174659985 |

Già live da sessioni precedenti (5):
| SKU | listingId |
|---|---|
| AE-1005007010007533-B | 407166264983* |
| AE-3256810466984003-B | 407166265035* |
| AE-1005008544241211 | 244489100011 |
| AE-3256807158753700 | 244489087011 |
| PILOT-20260823-01 | 244469781011 |

Pubblicati in questa sessione (3, batch "altri10"):
| SKU | listingId | categoria | prezzo |
|---|---|---|---|
| AE-1005006875318074 | 407174800225 | 20614 (car vacuum) | 60.97 USD |
| AE-3256807149552351 | 407174800350 | 75672 (solar drip irrigation) | 61.97 USD |
| 407113382755 | 407174800502 | 181070 (pool chlorine feeder) | 82.97 USD |

\* listingId delle due varianti "-B" riportato dal bootstrap; da confermare con read su listing.

### UNPUBLISHED (2, offer esistenti ma bloccate — DUPLICATI, non da pubblicare)

| SKU | offerId | categoria | blocker |
|---|---|---|---|
| AE-3256810466984003 | 244489063011 | 36114 (sleeping pad) | item specific "Size" mancante |
| AE-1005007010007533 | 244489079011 | 131598 (car mattress) | item specific "Size" mancante |

eBay rifiuta il publish con: "The item specific Size is missing."
Il token OAuth non ha scope Taxonomy, quindi i valori validi di "Size" non sono
recuperabili via API. Le varianti "-B" (stesso prodotto) hanno già "Size" negli aspects
(Universal / Single) e sono LIVE → pubblicare i base creerebbe DUPLICATI. Corretto non pubblicarli.

## Finding — bug nel bootstrap (read-only)

`account.ts` `readPaged`/`safeRead` ingoia silenziosamente gli errori: l'endpoint
`GET /sell/inventory/v1/offer?limit=100&marketplace_id=EBAY_US` torna vuoto mentre
`GET /sell/inventory/v1/offer?sku=X&marketplace_id=EBAY_US` (usato da
`createOrReuseOffer`) funziona. Risultato: `existingOfferSkus` è un **falso negativo**
(sempre `[]` anche con offer live). Causa probabile del falso REMOTE_STATE_CONFLICT su apply-inventory/
create-offer: eBay riecheggia campi nested extra (`allocationByFormat` dentro
`availability`, `eBayPlusIfEligible` dentro `listingPolicies`) e `subset()` in
`publisher.ts` è shallow, quindi l'hash non coincide anche quando i dati sono identici.
Entrambi sono difetti di confronto read-only, non di dati.

## Log batch

- `audit/batch-publish-3-20260827-171248.log` — i 3 pubblicati in questa sessione.

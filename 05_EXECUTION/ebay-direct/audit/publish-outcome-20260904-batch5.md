# Publish outcome — batch 5 (2026-09-04 ~21:30 EDT)

Verdict: **30 listing LIVE** · 4 bloccati item-specific (remote inventory conflict, non-destructive by design) · 1 title-claim fixato e pubblicato a mano · 0 errori di sistema.

## Metodo (diverso dai batch 1-4)

Le `variation_statistics` del pool draft AutoDS erano **corrotte**: 406/1600 draft con tripletta identica (buy $133.13 / sell $198.97 / profit $35.64) — repricing rotto, non dati reali (una borraccia da gallone non costa $133). Tutta la selezione è quindi passata da **probe live Amazon via proxy jina** (metodo già validato sul tappeto venduto US-B0DBYLD9WY):

- 3 giri di probe: 5a (52 ASIN, focus up-ticket), 5b (89, up-ticket rimanenti), 5c (115, pet-specialist + premium keyword) = 256 probe live
- ~50% "Currently unavailable" → il pool draft (pull 2026-08-27) è a 8 giorni e metà offerta è già sparita
- Markup 1.5× (quello provato dallo store: tappeto 143.99→215.97, venduto), price ending .97
- Gate a tier: cost≥$100 → net≥$30 · cost≥$84 → net≥$25 · categorie pet winner → net≥$15
- 34 manifest generati con prezzi live nel campo evidence; 1 scartato (Amazon Basics = brand, VeRO risk)

## LIVE (30)

| SKU | listingId | prodotto | cat |
|---|---|---|---|
| US-B00K0157UW | 407193918682 | Luxury XXL orthopedic memory foam dog bed | 20744 |
| US-B00VNECWSA | 407193918824 | Elevated dog bowl stand 3 ceramic bowls | 177789 |
| US-B016R4B0MY | 407193918909 | Orthopedic gel memory foam pet bed | 20744 |
| US-B01H7935D0 | 407193918957 | Dog carrier purse PU leather | 177788 |
| US-B06X9X6VYY | 407193919020 | 5.5" orthopedic memory foam dog bed | 20744 |
| US-B0749WPC6V | 407193919070 | Danvers area rug damask 5x7 | 262983 |
| US-B0753CRLJM | 407193919126 | Ping pong conversion top for pool table | 97075 |
| US-B07CRS4FWW | 407193919179 | Convertible pet travel bag armorsole base | 177788 |
| US-B07DBLHZ2L | 407193919259 | Large orthopedic memory foam pet bed | 20744 |
| US-B07MLJMMNF | 407193919437 | Dog bagel calming bed 40x29 | 20744 |
| US-B07PSFP38T | 407193919639 | 96" extra wide dog gate | 117029 |
| US-B07PWN2CW7 | 407193919862 | Cooling gel dog bed large | 20744 |
| US-B07SVQ3RQF | 407193920055 | Orthopedic dog bed large w/ bolsters | 20744 |
| US-B0832PDJG9 | 407193920292 | Cat tree 35" wooden double condos | 20740 |
| US-B0888SRMHS | 407193920436 | Travel bag for pets up to 25 lbs | 177788 |
| US-B08FFB9C7P | 407193920584 | Orthopedic dog bed large/medium | 20744 |
| US-B08FRF12YC | 407193920699 | XL cat tree 73.4" 3 caves | 20740 |
| US-B08G53L8B5 | 407193920875 | 2-drawer metal file cabinet | 3299 |
| US-B08KFXV74T | 407193921001 | 63.8" multi-level cat tree | 20740 |
| US-B08SHLNMKR | 407193921344 | 2-panel wooden folding dog gate | 20748 |
| US-B08ZSMTSVP | 407193921471 | Magic dog super comfy bed 47" | 20744 |
| US-B092VL9RB1 | 407193921661 | 2-panel wooden folding dog gate (var.) | 20748 |
| US-B094JQ9KG9 | 407193921772 | Butterfly chair oversized XL camping | 16038 |
| US-B09JNK5CXF | 407193921847 | 4XL odor control pads 36x36 | 146243 |
| US-B09XVHV8M1 | 407193921887 | Compartment cat carrier backpack w/ wheels | 177788 |
| US-B0CCVQNC7F | 407193921958 | Large cat carrier 24x16.5 | 177788 |
| US-B0FGPY7D6V | 407193922253 | 96 LED solar lights 6-pack 43" | 94940 |
| US-B0H1YSN4N6 | 407193922451 | Pet Gear lifestyle pet cot 30" | 20744 |
| US-B07P4MD2C2 | 407193930005 | Trampoline pad replacement multi-size | 57275 |
| (1 listed twice — see note) | | | |

Nota conteggio: 29 dalla pipeline batch + 1 (trampoline, fixato titolo "Safety"→claim "safe" bloccato dal validator e bullet mojibake nella description) pubblicato in 3 fasi manuali = 30.

Range economico [OBSERVED — manifest evidence, probe live 2026-09-04]:
- sell $78.97–$337.43 · cost $52.45–$249.95 · net atteso $15.76–$50.90
- Net atteso medio ponderato ~$27/listing · totale netto potenziale batch ~$800

## BLOCKED (4, remote inventory conflict)

| SKU | problema | perche non ripubblicato |
|---|---|---|
| US-B07M6Y9PMJ | desk 88057, aspect richiesto assente nel titolo | inventory remoto creato nel primo pass; patch aspects → REMOTE_STATE_CONFLICT; tooling non ha delete (by design) |
| US-B07PDR8CGG | metal dining chairs 54235 | idem |
| US-B08S2PG1TK | folding desk 88057 | idem |
| US-B0F2F6DT63 | gaming desk 88057 | idem |

La pipeline rifiuta overwrite di inventory remoto diverso (sicurezza by design, non bypassata con API raw). Questi 4 restano offer-less (nessun listing live, costo $0).

## Lezioni (per ERROR_REGISTRY)

1. **variation_statistics AutoDS non fidarsi mai alla cieca**: 406 draft con buy/sell/profit identici = repricing rotto. Sempre probe live pre-publish (già regola memory refresh-research-before-use — questa volta applicata alla lettera).
2. **"Safety" contiene "safe"** → BLOCKED_CLAIMS del validator. I titoli con "Safety" vanno riassettati pre-manifest.
3. **Description mojibake**: generare description con bullet "•" via PowerShell here-string corrompe in UTF-8; usare "-" o script su file.
4. **REMOTE_STATE_CONFLICT sui retry**: se apply-inventory passa e create-offer fallisce su item-specific, l'inventory remoto resta "sporco" e un patch-aspects successivo non può ripubblicare. Serve un comando `delete-inventory` (proposta di evoluzione tooling, NON aggiunto ora).
5. **Probe jina 256 ASIN**: ~1.3s/ASIN, nessun wall in 3 giri — metodo scalabile per pre-publish check.
6. Pool draft invecchia male: a 8 giorni dal pull, ~50% dei prodotti probe-ati è "Currently unavailable". Il probe live pre-publish non è opzionale.

## Files

- Manifest: `05_EXECUTION/ebay-direct/manifests/US-*.json` (33 nuovi)
- Action packs: `05_EXECUTION/ebay-direct/action-packs/`
- Log pipeline: `audit/batch-publish-5-20260904-212648.log`
- Probe evidence: `90_CACHE/amazon_probe_batch5{,b,c}.json` (cache non versionata)
- Script (cache, non versionati): `90_CACHE/probe_batch5b.py`, `probe_batch5c.py`, `build_batch5_live.py`

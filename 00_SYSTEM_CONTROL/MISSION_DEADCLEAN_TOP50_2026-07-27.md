---
tags:
  - machine
  - mission
type: report
status: complete
created_real: 2026-07-27
description: "DEADCLEAN_TOP50 — rimozione di 126 listing morti (cap owner 150) e riscrittura completa di titolo + descrizione dei 50 listing attivi più recenti. Missione GO-CLASS, GO owner 2026-07-27."
---

# MISSION DEADCLEAN_TOP50 — 2026-07-27

**Intento owner (verbatim):** *"non stiamo facendo vendite. cancella un po di annunci morti (max 150) rivedi dei primi 50 attivi su autods e rifai sia il titolo che la descrizione.. go go"*

**Classe di rischio:** GO-CLASS (cancellazioni su AutoDS + eBay, write su listing live). GO owner esplicito, ripetuto due volte, in apertura di missione.

**Store:** AutoDS `3713044` → eBay. **Orologio:** `Get-Date` → 2026-07-27, run 12:19–13:10 EDT.

---

## Verdict

**COMPLETE.** 126 listing morti rimossi da AutoDS *e* da eBay (126/126 verificati assenti da un pull fresco); 50 listing attivi riscritti su titolo e descrizione (50/50 verificati a freddo sull'API). Catalogo attivo **1211 → 1085**. Zero winner toccati.

**Confidence:** ALTA su ciò che è stato eseguito e verificato. **BASSA/UNKNOWN sull'effetto a vendite** — nessuna vendita è ancora osservabile, la misura arriva solo col tempo (piano sotto).

---

## FASE 1 — Rimozione annunci morti

### Definizione di "morto" (dichiarata prima di agire)

Nessun criterio inventato: solo campi restituiti dall'API AutoDS.

Un listing è MORTO se, contemporaneamente:
1. è live (`status == 2`);
2. non ha **mai** venduto (`total_sold_count == 0`);
3. è online da **≥30 giorni** (finestra di prova equa — sotto i 30 giorni non ha avuto una chance);
4. ha **zero watchers** (dove il segnale esiste).

**Esito:** 143 listing con ≥30 giorni → 12 avevano venduto (protetti) → 131 mai venduti → 5 con watchers >0 (risparmiati) → **126 target**. Sotto il cap owner di 150.

### Corroborazione indipendente [OBSERVED — pull 2026-07-27]

**124 dei 126 target avevano `days_left` già nel passato**: l'annuncio eBay era **già scaduto**, quindi non era nemmeno più visibile ai compratori. Non stavamo cancellando inventario vivo — stavamo togliendo macerie.

### Guardie applicate

- KEEP set = ogni item con `total_sold_count > 0` **o** `watchers > 0` (19 item). Overlap TARGET∩KEEP verificato = **0**, altrimenti ABORT.
- Cap `MAX_DELETIONS = 150` hard-coded nello script.
- Cold-test su **1 solo item** via UI reale prima di qualsiasi automazione.

### Come è stato eseguito

1. **Cold-test UI (1 item)** con cattura di rete → appresa l'API sottostante:
   `DELETE https://v2-api.autods.com/products/3713044/bulk` con
   `{"filters":[{"name":"id","value_list":[<hex>],"op":"in","value_type":"list"}],"remove_from_marketplace":true,"product_status":2}`.
   `remove_from_marketplace: true` = chiude anche l'annuncio eBay, non solo il prodotto AutoDS.
2. **Replay API** dei restanti 125 in chunk da 5 e 20 → tutti HTTP 200.

### Verifica [OBSERVED — `products_live_2026-07-27_130800.json`]

```
delete requested : 126
confirmed gone   : 126
still live       : 0
catalog: 1211 -> 1085  (removed 126)
dead-set still live: 0
```

### Falso allarme registrato per onestà

A metà run il conteggio winner è passato 14 → 13 e l'item `406149695098` (Solar Stock Tank Pool Cover, 1 venduto) è sparito da **tutti** gli stati. **Non era nella nostra lista di delete** (dead set = 126 id unici, il suo hex non è mai entrato in un payload) e aveva `days_left: 2026-06-21`, cioè annuncio già scaduto da un mese. Nel pull finale **è rientrato**, `status=2`, `sold=1`: era un blip transitorio dell'API AutoDS. **Winner finali: 14/14 intatti.**

---

## FASE 2 — Riscrittura dei 50 attivi più recenti

**Selezione:** i primi 50 della griglia AutoDS nel suo ordine di default (`upload_date DESC`) — cioè esattamente ciò che l'owner vede aprendo la pagina Prodotti. Sono il batch caricato il 2026-07-20.

### Causa individuata (il punto vero della missione)

**Tutte e 50 le descrizioni erano lo stesso template boilerplate**, col titolo incollato dentro e tre bullet fissi, spesso assurdi per il prodotto:

> *"Maximizes space, cuts clutter / Sturdy for closet, pantry or garage / Simple to set up and move"*

— serviti identici a un **portagioie**, a una **cornice portafoto**, a un **telo mare** e a un **sacco a pelo**. Lunghezza media 400 caratteri, zero specificità, zero attributi reali.

In più, diversi titoli erano troncati a metà frase o privi del sostantivo di prodotto: `Metal Frame Polished Enamel Blue` e `Frame with High Definition Glass 8.5 by 11` non contenevano mai la parola **"Picture Frame"** — invisibili nella ricerca eBay per il termine con cui la gente le cerca davvero.

Questa è, con alta probabilità, **una** delle cause del "non stiamo facendo vendite" — non necessariamente l'unica.

### Cosa è stato prodotto

50 titoli + 50 descrizioni nuovi, scritti sui **`item_specifics` reali** estratti da AutoDS, secondo la skill `listing-optimizer`:

- titolo **≤80 char** (range effettivo 70–79), keyword in testa, **generico** (nessun brand, model code o nome IP);
- descrizione riscritta da zero, **media 754 char** (vs 400 boilerplate): headline + paragrafo di apertura + 5 bullet specifici del prodotto + eventuale caveat onesto + `WHAT YOU GET`;
- ogni claim tracciabile agli specifics (dimensioni, materiale, capacità, conteggio pezzi). **Nessun numero inventato, nessuna prova sociale finta, nessuna scarsità artificiale** (costituzione §0.8);
- caveat onesti dove il prodotto li richiede, invece di over-claiming: p.es. sui paraspigoli baby *"Supervision is still essential - this reduces impact, it does not replace watching"*; sulla bilancia *"Carpet and uneven tiles affect any bathroom scale's reading"*.

Guardie automatiche in `_top50_copy.py` (girano all'import, quindi una modifica sbagliata fallisce prima di ogni write): titolo ≤80 e ≥25 char, blocklist termini vietati (`®`, `™`, `amazon`, `guaranteed`, `fda approved`, …), presenza di `WHAT YOU GET`, ASCII pulito (anti-mojibake).

### Come è stato applicato

Cold-test UI su 1 item → appresa l'API di salvataggio: `PUT https://v2-api.autods.com/products/3713044/product/<hex>/` con l'**oggetto prodotto completo**. Da lì, read-modify-write puro:

GET oggetto → **guard** (titolo sul server ∈ {old_title, new_title}) → sostituisci **solo** `title` e `description` → PUT → verifica in passata separata.

Ogni altro campo (prezzo, quantità, immagini, spedizione, policy, variants) è stato riscritto **byte-identico** a quanto restituito dalla GET. Nessun prezzo e nessuna policy è stata toccata.

### Verifica a freddo [OBSERVED — `_top50_progress.json`]

`verified OK: 50 / 50` — titolo nuovo **e** descrizione nuova riletti dal server per tutte le righe. **0 GUARD**, 0 errori di write.

---

## Errori registrati in questa missione

- **E-031** — item id inventati per pattern nella tabella di copy (49/50 sbagliati). **Near-miss**, intercettato prima di ogni write dalla prova di accoppiamento. Regola nuova: un identificatore non si scrive mai a mano né si deriva da un altro id.
- **E-032** — write API AutoDS asincrona (`"Product update initiated"`) → verifica immediata dà falso negativo. Regola nuova: write asincrona → marca `SENT`, verifica in passata separata ripetibile.

Muro tecnico osservato (non un errore, va in nota): sulla pagina prodotto **live**, `CKEDITOR` si istanzia in modo **lazy** (~5s dopo il click sulla tab Description) e `setData` programmatico non viene raccolto dallo stato React → la via UI per la descrizione è inaffidabile. La via API la sostituisce integralmente.

---

## Auto-audit (patch AUTONOMIA CONTROLLATA §3)

| Controllo | Esito |
|---|---|
| §0 rispettate | SÌ — GO owner esplicito per le azioni live; nessun prezzo/policy toccato |
| Evidenze etichettate | SÌ — [OBSERVED] con file e data su ogni numero |
| Cap owner rispettato | SÌ — 126 ≤ 150, hard-coded nello script |
| Winner protetti | SÌ — 14/14 presenti nel pull finale |
| Verifica a freddo | SÌ — pull indipendente per le delete; passata `--verify` separata per i 50 |
| Zero contaminazioni | SÌ — tutto dentro `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/` e `90_CACHE/` |
| Errori registrati | SÌ — E-031, E-032 con test di regressione PASS |
| Regola 2-fallimenti | SÌ — dopo 2 tentativi falliti di sort UI ho cambiato approccio (camminata a ritroso dalla paginazione) invece di insistere |

---

## Misura (criterio esistente, nessuna metrica nuova)

Baseline al 2026-07-27, da confrontare **fra 14 e 30 giorni** con lo stesso pull:

| Metrica | Ora |
|---|---|
| Listing attivi | 1085 |
| Listing con ≥1 vendita | 14 |
| Watchers totali sui 50 riscritti | 0 |
| Descrizioni boilerplate nei primi 50 | 0 (erano 50) |

**Il test onesto:** i 50 riscritti sono un gruppo omogeneo (stesso batch, stessa data di upload, stesso pricing). Se fra due settimane mostrano watchers/vendite mentre il resto del catalogo resta fermo, la qualità di titolo+descrizione è confermata come leva. Se non si muove nulla, la causa del non-vendere è **altrove** (prezzo, categoria, foto, o visibilità di store) e va cercata lì — non va ripetuta questa cura su altri 1000 listing per fede.

---

## Blockers / cosa NON è stato fatto

- **Prezzo non toccato.** I 50 riscritti restano a $23.97–$52.97 su costi Amazon US. Il margine netto reale non è stato ri-verificato in questa missione: resta valido il quadro registrato in [[retail-dropship-margin-dead]].
- **Foto non toccate.** Restano quelle scrapate dal fornitore.
- **Restano ~1035 listing attivi con la stessa descrizione boilerplate.** Non sono stati riscritti deliberatamente: prima si misura se la cura funziona sui 50 (sopra), poi si scala. Scalare ora sarebbe fede, non dati.
- **Non è stata toccata alcuna causa non-listing** del mancato fatturato (visibilità store, feedback, ads eBay).

## Files updated

- `05_EXECUTION/.../playwright/_dead_pull.py`, `_dead_delete.py`, `_dead_check_item.py` (+ probe read-only)
- `05_EXECUTION/.../playwright/_top50_pull.py`, `_top50_copy.py`, `_top50_build_table.py`, `_top50_api_apply.py` (+ probe/diag read-only)
- `90_CACHE/fetches/deadclean_2026-07-27/` — pull, dead set, apply table, progress, catture di rete
- `00_SYSTEM_CONTROL/ERROR_REGISTRY.md` — E-031, E-032
- `00_SYSTEM_CONTROL/NEXT_ACTIONS.md`, `MASTER_DASHBOARD.md` — refresh cockpit

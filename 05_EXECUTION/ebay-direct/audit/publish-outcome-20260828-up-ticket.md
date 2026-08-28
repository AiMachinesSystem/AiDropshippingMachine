# Publish outcome — batch up-ticket (2026-08-28 ~01:50Z)

Verdict: **9 nuovi listing LIVE** (8 dal primo run + 1 mattress sbloccato) · **3 bloccati da item-specific dimensionali assenti nel sorgente**.

Primo run (dopo il fix del gate invertito): **8 PUBLISHED** + **4 bloccati item-specific**.
Secondo pass (title-inference): **1 sbloccato (mattress)**, 3 restano bloccati — servono item-specific NON presenti nel titolo AutoDS.

## LIVE (9, status=PUBLISHED)

| SKU | listingId | prodotto | net stimato |
|---|---|---|---|
| US-B002NTP6B4 | 407175197710 | Buddha statue | up-ticket |
| US-B0881X64L5 | 407175198037 | Dog bed | up-ticket |
| US-B01JAVL5OE | 407175198342 | Cat6 cable | up-ticket |
| US-B0D5H6DTV3 | 407175198571 | Vinyl wall base | up-ticket |
| US-B072LTYJ6P | 407175198768 | Sauna | up-ticket |
| US-B01N9JZADA | 407175198847 | Baby carrier | up-ticket |
| US-B07GY27KPC | 407175198913 | Baby carrier | up-ticket |
| US-B0728DF739 | 407175199368 | Paddle board | up-ticket |
| US-B0DHPMHJXB-C | 407175223822 | King Mattress (10" Hybrid) | $56.53 |

## BLOCKED (3, item-specific dimensionali non inferibili)

| SKU | richiesto dopo il fix | perché bloccato |
|---|---|---|
| US-B09YM9SQ61 (gaming desk) | Item Width | "Item Length=60 in" inferito dal titolo ("60 Inch"), ma la larghezza NON è nel titolo |
| US-B01KBAF00S (walnut tray) | Color | "Material=Wood" inferito ("Solid Walnut"), ma il colore NON è nel titolo |
| US-B098SYBSVZ (full-length mirror) | Item Width | nessuna dimensione nel titolo |

## Finding strutturale (per il loop)

1. **Le categorie up-ticket dimensionali (desk, mattress, mirror, tray) richiedono un SET di item-specific obbligatori, non uno.** Ogni valore inferito rivela il prossimo mancante via errore publish: desk = Length→Width, mattress = Firmness→Size, tray = Material→Color, mirror = Width.
2. **Il title-inference sblocca SOLO ciò che è esplicito nel titolo** ("60 Inch"→Item Length, "King"→Size, "Medium"→Firmness, "Walnut"→Material). Gli item-specific NON espliciti (Item Width, Color, Item Height) sono assenti nel sorgente AutoDS, che porta solo title/category/price/image.
3. **Il token OAuth non ha scope Taxonomy** ⇒ non posso recuperare la lista completa dei required né i valori enum validi via API. Scoperta per tentativi = costosa e frammentaria.
4. **Inventare dimensioni/colori = fabbricare dati di compliance** (CONSTITUTIONAL FILTER §5) ⇒ non lo faccio. Questi 3 sono un Hard Block reale, non risolvibile col title-inference.
5. **Il CLI è fail-closed**: `applyInventory`/`createOrReuseOffer` rifiutano di sovrascrivere inventory/offer esistenti con campi diversi ⇒ ogni fix item-specific richiede un nuovo SKU con suffisso (`-B`, `-C`), accumulando offer unpublished. Pattern già visto nel batch2 (`US-B091ZGB8RJ` → `-B` → `-C`).

## Leva corretta (non il title-inference)

Il gate item-specific non si risolve inferendo dal titolo ma **al sourcing**: o (a) ottenere dimensioni fisiche (Length/Width/Height) e colore dal fornitore, o (b) restringere gli up-ticket alle categorie i cui item-specific richiesti sono inferibili dal titolo (come il mattress: taglia + fermezza sono nel titolo). Questo è il "Rischio residuo" già segnalato nel finding gate-inversion: *"item-specific più complessi (dimensioni/materiale) sugli up-ticket — va misurato col primo batch"*. Misurato: ~3/12 up-ticket (25%) restano bloccati da dimensioni assenti nel sorgente.

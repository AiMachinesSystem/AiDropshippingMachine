---
tags:
  - machine
  - diagnosis
type: report
status: complete
created_real: 2026-07-27
description: "MACHINE_HEART su 'perché non stiamo vendendo'. Risposta: il base rate di sell-through è ~0.7%/listing/mese e il tetto di margine dell'intero store ≈ il canone AutoDS. Prezzi +57–113% sopra il venduto eBay, ma i winner lo erano ugualmente → abbassare il prezzo NON è il fix provato; al prezzo di mercato 11/12 prodotti vanno in perdita."
---

# Perché non stiamo vendendo — diagnosi MACHINE_HEART, 2026-07-27

> Ciclo completo eseguito su richiesta owner ("perché non stiamo vendendo qual è il problema? ci serve la grana"). Tutte le cifre sono [OBSERVED] con file e data. Dove il dato manca è scritto [UNKNOWN], non stimato.

---

## Risposta in una riga

**Non è rotto niente di nuovo: lo store sta rendendo esattamente al suo tasso storico, e quel tasso produce circa quanto costa il canone AutoDS.** Ogni annuncio vende ~0,7% al mese, il netto è ~$15 a vendita, quindi 1085 annunci valgono **~$114/mese di margine lordo** — contro i **$113,44** addebitati da AutoDS a luglio. Stiamo correndo per restare fermi.

---

## 1 · DATA — cosa dicono i numeri

### Il base rate (il numero che conta)

| Coorte | Listing | Con ≥1 vendita | Tasso |
|---|---|---|---|
| ≥30 giorni (fotografata stamattina, **prima** della pulizia) | 143 | 12 | **8,4%** su ~1 anno di esposizione |
| 0–30 giorni (catalogo attuale) | 1068 | 2 | **0,19%** in <30 giorni |

Le due righe sono **coerenti fra loro**: 8,4% spalmato su un anno ≈ **0,7% per annuncio al mese**; su 1068 annunci giovani ci si aspettano ~2–4 vendite in un mese, e ne abbiamo 2. **Nessuna rottura recente — il tasso è sempre stato questo.**

> ⚠️ Trappola statistica evitata: le coorti vecchie oggi mostrano 100% e 61,5% di conversione. È **survivorship bias** — i non-venditori di quelle coorti sono esattamente i 126 che abbiamo cancellato stamattina. Quel numero non va usato.

### L'aritmetica del tetto

```
1068 listing × 0,7%/mese      ≈ 7,5 vendite/mese
× $15,18 netto mediano/vendita ≈ $114/mese di margine lordo
AutoDS addebitato a luglio      = $113,44
```

Netto mediano calcolato su fee eBay 13,6%; **esclude** tasse d'acquisto Amazon (~7–10%), resi e spedizioni. Il margine reale è quindi **sotto** $114.

### Prezzo vs mercato — 12 campioni, comps SOLD reali

Confronto col prezzo **davvero pagato** su eBay (non i prezzi richiesti). Doppia misura per onestà: contro l'estremo basso e contro l'estremo alto dei range multi-variante.

| | scostamento mediano |
|---|---|
| vs estremo **basso** del venduto | **+113%** |
| vs estremo **alto** del venduto | **+57%** |

11 campioni su 12 sopra mercato anche nella lettura più generosa; 9 su 12 oltre +25%. Esempi: tappetino mouse $28,97 vs $9,98 · pattumiera auto $36,97 vs $12,45 · coprivaso silicone $26,97 vs $10,13.

### Il test che decide: e se abbassassimo al prezzo di mercato?

| | risultato |
|---|---|
| Prodotti in **profitto** a prezzo di mercato | **1 / 12** |
| Prodotti in **perdita** a prezzo di mercato | **11 / 12** |
| Netto mediano a prezzo di mercato | **−$6,63 a vendita** |

**Il costo d'acquisto su Amazon US è più alto del prezzo che il mercato eBay paga.** Non possiamo comprare la competitività: a prezzo pieno non vendiamo, a prezzo di mercato perdiamo.

### L'ipotesi che ho dovuto scartare

Avevo formulato: *"i winner vendono perché sono a prezzo di mercato"*. **FALSO.** I 9 winner testati sono **+114% sopra il mercato** — praticamente identico ai non-venditori (+113%). Quindi **"abbassa i prezzi" non è un fix dimostrato** da questi dati.

*Limite del metodo, dichiarato:* le query generiche restituiscono prodotti eterogenei, quindi la mediana di mercato include articoli diversi dai nostri. Il limite pesa **allo stesso modo** su winner e perdenti, per questo il confronto fra i due gruppi resta valido anche se il valore assoluto è impreciso.

### Cosa distingue davvero i 14 winner

| | Winner (14) | Resto (1071) |
|---|---|---|
| Prezzo mediano | **$63,96** | $42,97 |
| Quota sopra $60 | **50%** | 27% |
| Categorie | specialistiche | commodity generiche |

**Winner:** Pool Equipment Parts · Pool Covers & Reels · Ramps & Stairs (rampa cane per barche) · Leashes & Head Collars · Safety Vests · Monitors (display secondario) · Crochet Kits · Ham press. **8 su 14 sono pool o pet.**

**Resto:** Beds(23) · Racks & Holders(22) · Blankets & Throws(22) · Pillows(19) · Food Storage(19) · Candles(19) · Bathtub Caddies(18) · Jewelry Boxes(16).

I winner sono cose che si cercano **per funzione precisa** e di cui esiste **una** versione giusta. Il resto sono oggetti intercambiabili dove 500 venditori competono e chi compra sceglie su prezzo e foto.

### Struttura del catalogo che rema contro

**387 categorie distinte per 1071 annunci** = 2,8 annunci per categoria. eBay (Cassini) premia la velocità di vendita *dentro* una categoria: spalmati così non costruiamo autorità da nessuna parte.

### Il nostro punto cieco

**Non abbiamo NESSUN dato di traffico sugli annunci attivi.** Verificato: AutoDS popola `views`/`watchers` **solo sugli annunci finiti** — le 17 righe che espongono watchers sono *esattamente* le 17 con annuncio eBay scaduto (insiemi identici). E il Seller Hub di eBay è dietro **CAPTCHA** per l'accesso automatico (3 URL testati, tutti reindirizzati; la sessione è viva, è Seller Hub a bloccare).

Quindi **non possiamo distinguere** fra:
- **(A)** ci vedono ma non cliccano → problema di offerta (prezzo/foto/titolo)
- **(B)** non ci vedono proprio → problema di ranking/account/categoria

Questa è la domanda più importante rimasta aperta, e costa 5 minuti all'owner.

---

## 2 · ANALYSIS — la catena causale

1. Il pricing AutoDS è **cost-plus** (~1,88× il costo Amazon), non market-based → ignora cosa paga davvero il mercato.
2. Il costo Amazon US retail è **già sopra** il prezzo di mercato eBay per le commodity → nessun prezzo rende contemporaneamente competitivi e profittevoli.
3. Sell-through resta a ~0,7%/mese → nessuna velocità di vendita.
4. Nessuna velocità → Cassini non ci spinge → ancora meno traffico. **Ciclo che si autoalimenta.**
5. Il volume è stato la risposta sbagliata: 1000+ annunci moltiplicano un tasso che non funziona, e moltiplicano anche il rischio (294 annunci portano errori di supplier).

**Nota istituzionale onesta:** questa conclusione **era già registrata** in memoria il **2026-06-29** (`retail-dropship-margin-dead`, "i nostri prezzi sono 2,5×–3,75× sopra il sold-median eBay… o prezzo-fantasia (0 vendite) o prezzo-mercato (perdita)"). Oggi l'ho ri-confermata su un campione fresco. **Nel frattempo la macchina ha continuato a pubblicare più di mille annunci con lo stesso difetto.** Il fallimento non è stato di analisi: è stato che una conclusione registrata non ha fermato la produzione.

---

## 3 · STRATEGY — dove sta la grana, se c'è

Non serve ottimizzare: serve cambiare la variabile che vincola.

**A — Misurare il punto cieco (costo: 5 minuti owner).** Aprire Seller Hub → Performance → Traffic, ultimi 30 giorni. Se le impressions sono alte e i click ~0 → è l'offerta. Se le impressions sono ~0 → è la visibilità. Ogni euro speso dopo questo dato è meglio speso.

**B — Smettere di allargare.** Ogni nuovo annuncio commodity aggiunge ~$0,10/mese di margine atteso e un po' di rischio. Il volume è già stato testato a 1000+: non funziona.

**C — Replicare il pattern winner, deliberatamente.** 8 su 14 winner sono **pool** e **pet**, categorie funzionali, prezzo mediano $64. Sourcing mirato di 20–30 articoli con quel profilo vale più di altri 1000 commodity.

**D — Test di prezzo controllato.** Poiché i winner vendevano *anche* a +114%, non sappiamo se il prezzo muova davvero il sell-through. È rispondibile solo sperimentalmente: 40 annunci a prezzo di mercato vs 40 gemelli invariati, 30 giorni. Costo: qualche vendita in perdita in cambio della risposta.

**E — Decisione economica sul canone.** Se il margine lordo ≈ il canone, lo store oggi non paga se stesso. Va deciso consapevolmente, non per inerzia.

---

## 4 · Cosa è stato fatto in questo run

- Diagnosi completa con prove a due lati (nostro catalogo + venduto reale eBay). Cache: `90_CACHE/fetches/ebay/pricecheck_2026-07-27/`, `winners_2026-07-27/`, `traffic_2026-07-27/`.
- Ipotesi "il prezzo è il discriminante" **testata e scartata** invece di essere assunta.
- Survivorship bias identificato e neutralizzato prima di entrare nel report.
- **2 muri registrati** in `VAULT_CONVENTIONS`: Seller Hub CAPTCHA (nuovo) e selettori CSS eBay obsoleti (con il parser di testo che li aggira, già funzionante).
- Strumenti riutilizzabili: `_why_no_sales_pricecheck.py`, `_why_no_sales_winners.py`, `_why_no_sales_traffic.py`.

## 5 · Gate aperti per l'owner

1. **GO / MANUALE** — leggere Seller Hub → Performance → Traffic (30gg) e riferire impressions e click. Sblocca la scelta fra (A) offerta e (B) visibilità. *Non automatizzabile: CAPTCHA.*
2. **GO** — avviare il test di prezzo controllato su 40+40 annunci gemelli (comporta vendite in perdita per acquisire la risposta).
3. **DECISIONE** — canone AutoDS: mantenere, sospendere, o rinegoziare, alla luce di margine lordo ≈ canone.

**Stato finale: COMPLETE** (diagnosi), **NEEDS_OWNER_DECISION** (le tre voci sopra).

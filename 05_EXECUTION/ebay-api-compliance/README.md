# eBay Marketplace Account Deletion — endpoint di compliance

Sblocca il keyset **Production** `LucaDeFe-LucaDeFe-PRD-e017de36f-531d1bfd`, oggi
`Non Compliant` e quindi **disabilitato**: finché resta così eBay non espone alcun
controllo per generare user token e nessuna chiamata API Production è possibile.

Spec: <https://developer.ebay.com/develop/guides-v2/marketplace-user-account-deletion>
— letta live 2026-08-14. [OBSERVED — developer.ebay.com, 2026-08-14]

## Perché endpoint e non esenzione

L'esenzione richiede di dichiarare **"I do not persist eBay data"**, sotto avviso
esplicito di eBay: *failure to provide correct information may result in penalties or
having your account disabled*. Scope dichiarato dall'owner per questa chiave: "tutto"
— inclusi gli ordini, quindi dati personali di acquirenti che finiscono su disco nei
report della macchina. La dichiarazione sarebbe falsa. [OWNER — 2026-08-14]

## Stato

| passo | stato |
|---|---|
| codice endpoint | ✅ scritto, `main.ts` |
| verification token (64 char, CSPRNG) | ✅ generato, in `.env.local` (gitignored) |
| test challenge/POST/health in locale | ✅ 3/3 passati |
| deploy su HTTPS pubblico | ⬜ serve un account hosting (GO owner) |
| registrazione nel portale eBay | ⬜ dopo il deploy (GO owner) |
| cancellazione reale dei dati utente | ⬜ **non implementata** — vedi sotto |

## Verifica eseguita (2026-08-14 20:58 -04:00)

```
GET  /?challenge_code=abc123XYZ
  status 200 · content-type application/json
  {"challengeResponse":"15d6e45cdad475d399dbcba984bb00433946fd9fbe837a15bd76d5ed002f1215"}
  identico a hashlib.sha256(code+token+endpoint).hexdigest() calcolato a parte  -> MATCH
POST /   -> 204   (eBay accetta 200/201/202/204)
GET  /   -> 200 "ok"  (health)
```

Nota: la porta 8000 su questa macchina è occupata dal container **SurrealDB di
open-notebook** (`open-notebook-surrealdb-1`, pubblicato da Docker su
`127.0.0.1:8000`; il listener risulta di `com.docker.backend`, che è il proxy di
porta). Il primo test interrogava quella UI, non l'endpoint. Usare `PORT` per i
test locali.

## ⚠️ PRIMA DI DEPLOYARE — potrebbe non servire

Verificato 2026-08-14 nella memoria di questa macchina: il path **AutoDS è già
operativo e ha già eseguito write live su eBay** senza alcun keyset eBay Developer
— reprice (`PUT v2-api.autods.com/products/3713044/bulk`), update prodotto completo
(`PUT .../product/<hex>/`), delete (`DELETE .../bulk`), ricerca marketplace
(`POST gw.autods.com/marketplace/api/products/`), auth Bearer da sessione Playwright
salvata. 1098 listing live gestiti così.
[OBSERVED — MASTER_DASHBOARD.md, ERROR_REGISTRY.md E-032, MISSION_DEADCLEAN_TOP50,
MISSION_APPLY_REPRICE_AND_CLEANUP_RUN_LOG, RESEARCH_MEMORY_INDEX:121]

Quindi "Claude crea e gestisce gli annunci" **non richiede** questo endpoint. Il
keyset eBay Developer serve solo per ciò che AutoDS non copre (API eBay dirette,
Terapeak, dati ordine da eBay, indipendenza dall'abbonamento AutoDS). Deployare
questo endpoint significa accettare un obbligo di uptime e un obbligo legale di
cancellazione dati: farlo solo se quella capacità extra serve davvero.

## Deploy

L'endpoint deve stare su HTTPS pubblico, **non** localhost/IP interno, e reggere GET
e POST. Se resta irraggiungibile 24h eBay lo marca down; 30 giorni senza fix =
developer non compliant. Un tunnel sul PC dell'owner non è adatto: quando il PC è
spento l'endpoint è giù.

Opzione consigliata: **Deno Deploy** (free tier, `deno` già installato su questa
macchina, HTTPS immediato su `*.deno.dev`).

```powershell
# 1. account su https://deno.com/deploy  (login GitHub)  <- passo owner, non automatizzabile
# 2. deploy
deno install -gArf jsr:@deno/deployctl
deployctl deploy --project=<nome-progetto> --prod main.ts
# 3. imposta le env var nel dashboard del progetto:
#    EBAY_VERIFICATION_TOKEN  = valore in .env.local
#    EBAY_ENDPOINT_URL        = l'URL pubblico esatto, byte per byte
```

`EBAY_ENDPOINT_URL` deve coincidere **esattamente** con l'URL registrato nel portale
eBay: un carattere di differenza cambia l'hash e la subscription viene rifiutata.

## Registrazione nel portale eBay

`Alerts & Notifications` → env **Production** → radio `Marketplace Account Deletion`:

1. email di alert (già presente: `divinitaestreme@gmail.com`) → `Save`
2. `Marketplace account deletion notification endpoint` = URL pubblico
3. `Verification token` = valore in `.env.local`
4. `Save` → eBay manda subito la challenge GET; se l'hash torna corretto la
   subscription è salvata
5. `Send Test Notification` per la prova finale

## Debito aperto — la parte che conta davvero

`deleteUserData()` in `main.ts` **logga e basta**. Rispondere 204 supera il controllo
meccanico di eBay ma **non** assolve l'obbligo: eBay richiede di cancellare i dati
dell'utente *in a manner such that even the highest system privilege cannot reverse
the deletion*. Finché lo storage ordini/acquirenti della macchina non è collegato qui
dentro, la compliance è formale e non sostanziale. Va chiuso prima di trattare volumi
reali.

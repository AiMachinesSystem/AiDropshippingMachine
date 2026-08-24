# eBay Production — endpoint di compliance

Pacchetto che sblocca il keyset Production eBay senza dichiarare una falsa
esenzione dal processo Marketplace Account Deletion/Closure.

Fonte canonica: <https://developer.ebay.com/develop/guides-v2/marketplace-user-account-deletion>
— verificata live 2026-08-15. eBay attiva il keyset solo dopo una subscription
valida oppure un opt-out approvato.

## Decisione

Usare un endpoint HTTPS con coda persistente. Non usare l'esenzione: la macchina
conserva dati eBay/AutoDS relativi agli ordini (incluse informazioni buyer), quindi
la dichiarazione “I do not persist eBay data” non sarebbe corretta.

Le Sandbox keys non devono essere cancellate. Una volta attivato Production, i
client devono usare `api.ebay.com` e le credenziali PRD; la Sandbox può restare come
ambiente di test separato.

## Stato verificato — 2026-08-15

| Passo | Stato |
|---|---|
| Production keyset | attivo; `Non Compliant` rimosso dopo validazione eBay |
| Form eBay Production | endpoint e verification token salvati; validation error assente |
| Deno organization | `aimachinessystem`; Deno CLI autorizzata con token revocabile 24h |
| Deno app | `ebay-deletion-hook`; Production URL live, revision `8s88mjp54c9f` routed |
| Deno KV | `ebay-deletion-kv`; database Production ready e assegnato all'app |
| Endpoint | deploy live; `/health` 200, challenge 64-hex valida, coda privata 401 senza token |
| Deno env hardening | alias `*_SECRET` e `EBAY_CLIENT_SECRET` protetti come secret; vecchie variabili token in chiaro eliminate |
| Protezione PII | nessun buyer identifier nei log; dati rimossi dalla coda dopo il purge |
| Signature verification | validatore ECC isolato; processor PII escluso e logger errori SDK soppresso; `EBAY_REQUIRE_SIGNATURE=true` live e POST senza firma rifiutato `412` |
| Purge locale | preview read-only ed esecuzione controllata per notification ID implementati |
| Test locali | 9/9 PASS; end-to-end challenge → webhook → queue → complete PASS |
| Registrazione eBay | completata e verificata dopo reload; `Send Test Notification` abilitato |

## Contratto HTTP

- `GET /?challenge_code=...` → hash SHA-256 di
  `challengeCode + verificationToken + endpointUrl`, nel formato JSON richiesto
  da eBay.
- `POST /` → valida topic/payload, verifica `X-EBAY-SIGNATURE` quando armata,
  accoda la richiesta in Deno KV e risponde `204`.
- `GET /internal/deletions` → coda privata, solo Bearer token.
- `POST /internal/deletions/{notificationId}/complete` → elimina la PII dalla
  coda dopo il purge locale e conserva soltanto un audit privo di buyer data.
- `GET /health` → health check senza segreti.

## Sequenza live corretta

1. ~~Creare app, assegnare Deno KV, configurare i secret di bootstrap e fare il
   deploy Production.~~ Completato e verificato live.
2. ~~Inserire URL e verification token nel form eBay Production e premere
   `Save`.~~ Completato; keyset validato e stato persistito dopo reload.
3. ~~Dopo l'attivazione del keyset, aggiungere le credenziali PRD come secret,
   impostare `EBAY_REQUIRE_SIGNATURE=true` e ridistribuire.~~ Completato e
   verificato live sulla revision `8s88mjp54c9f`.
4. Premere `Send Test Notification`; verificare risposta `204` e job in coda.

Ogni riga sopra modifica una superficie esterna e richiede un OWNER GO specifico
immediatamente prima dell'esecuzione.

## Bootstrap sicuro

La finestra di bootstrap è stata chiusa: le credenziali PRD sono configurate e
`EBAY_REQUIRE_SIGNATURE=true` è attivo. Non riportare il flag a `false` salvo una
nuova procedura di recovery esplicitamente autorizzata.

## Variabili

Vedere `.env.example`. In Production usare `EBAY_VERIFICATION_TOKEN_SECRET`,
`EBAY_PURGE_API_TOKEN_SECRET` e `EBAY_CLIENT_SECRET` come secret; non vanno
committati, mostrati nei log o copiati in report. Anche `DENO_DEPLOY_TOKEN` vive
soltanto in `.env.local`; il launcher `deno_deploy.ps1` lo carica nel processo
senza inserirlo nella command line.

Esempio di verifica CLI sicura:

```powershell
.\deno_deploy.ps1 whoami --json --non-interactive
```

## Verifica locale

```powershell
deno task check
```

## Nota operativa sulla cancellazione

Il webhook non esegue cancellazioni automatiche. Ogni job resta in coda finché
l'operatore prepara l'elenco dei record corrispondenti e riceve il GO distruttivo
per quel notification ID. Solo dopo la cancellazione verificata si chiama
`/complete`, che rimuove anche gli identificatori dalla coda.

La preview è il default e non modifica file:

```powershell
deno task purge --notification-id <notification-id>
```

L'esecuzione richiede il GO specifico per lo stesso notification ID; `--ack` va
usato soltanto dopo la verifica automatica che non restino corrispondenze:

```powershell
deno task purge --notification-id <notification-id> --execute --owner-go <notification-id> --ack
```

---
tags:
  - machine
type: log
status: template
description: "Registro errori della macchina (protocollo AUTONOMIA CONTROLLATA v0.1). Formato vincolante: ERRORE → CAUSA → REGOLA → TEST DI REGRESSIONE, con commit del fix. Le regole nate qui vincolano come la costituzione. PARTE VUOTO in una nuova macchina."
---

# ERROR REGISTRY — la macchina si istruisce dai propri errori

> Una voce per errore reale, ID stabile `E-NNN`, più recente in alto.
> Formato obbligatorio: **ERRORE → CAUSA → REGOLA → TEST DI REGRESSIONE** + commit del fix.
> Una voce si chiude solo con test di regressione PASSATO (a freddo dove applicabile, regola patch §5).
> Le regole nate da questo registro vincolano come la costituzione (patch AUTONOMIA CONTROLLATA §4).

> **NOTA TEMPLATE:** le regole nate dagli errori della macchina madre che ha generato questo
> template sono già incorporate nei protocolli e nelle convenzioni (REGOLA OROLOGIO, numeri
> canonici, cache evidenze, root-verification git, ecc.). Il registro di una NUOVA macchina
> parte VUOTO: si popola con i propri errori reali.

---

## FORMATO (copia questo blocco per ogni nuovo errore)

## E-NNN — `<titolo sintetico dell'errore>`
- **Data:** `<YYYY-MM-DD>` (`<contesto/missione>`) · **Fix:** `<commit hash>`
- **ERRORE:** `<cosa è andato storto, con il danno reale>`
- **CAUSA:** `<causa radice, etichettata [OBSERVED] dove possibile>`
- **REGOLA:** `<la regola che impedisce il ripetersi; vincola come la costituzione>`
- **TEST DI REGRESSIONE:** `<come si verifica che non si ripeta; PASS/FAIL + evidenza>`

---

## E-004 — Falso "PASS" del login AutoDS (account Google-SSO, rilevamento debole)
- **Data:** 2026-06-20 (re-login per sbloccare import; GO owner) · **Fix:** `login_and_save_session.py` hardened (successo = URL `platform.autods.com` autenticato, non `signin`/`/login`) + login manuale Google completato → sessione valida (`status`=9). **CHIUSO** (regression sotto PASSATO).
- **ERRORE:** `login_and_save_session.py` ha stampato "PASS — session saved", ma il browser era fermo su una pagina **Google OAuth signin** (`accounts.google.com/v3/signin`), NON loggato in AutoDS. La `storage_state.json` salvata era **fasulla** → `manage_draft status` = `None` (sessione invalida). Step sprecato + sovrascritta la vecchia sessione (già logged-out) con una bislacca.
- **CAUSA:** [OBSERVED] il rilevamento di successo è `wait_for_url(u: "/login" not in u)`. L'account AutoDS usa **"Sign in with Google"**: l'auto-fill del form AutoDS reindirizza a `accounts.google.com/...signin` (URL senza "/login") → il check debole passa per sbaglio. L'auto-fill credenziali **non può** completare l'OAuth Google (serve login Google interattivo/2FA).
- **REGOLA:** il successo del login si verifica **atterrando su un URL AutoDS autenticato** (host `platform.autods.com` E non `accounts.google.com`/`auth.autods.com`/`*signin*`), mai col solo "no /login". Per account Google-SSO l'auto-credential-fill NON completa il login → usare `--manual` e far finire all'owner il flusso Google fino alla dashboard AutoDS prima di salvare. **Conferma sessione SEMPRE con un `status` che ritorni un conteggio numerico prima di dichiararla valida.**
- **TEST DI REGRESSIONE:** dopo ogni login, `manage_draft status` deve dare un numero (non `None`/0-da-logout) → solo allora la sessione è valida. [DA ESEGUIRE dopo il prossimo login manuale].

## E-003 — Publish accidentale di un draft durante un probe "diagnostico"
- **Data:** 2026-06-19 (missione SOURCE_3_TO_DRAFT; owner GO `GO_IMPORT_5_DRAFTS` + GO publish) · **Fix:** regola sotto (probe rimossi; nessun commit di codice)
- **ERRORE:** in `_pubdiag.py`, inteso come "apri il modal di publish dello stove SENZA confermare", il click sul bottone **"Import"** della card ha **pubblicato immediatamente** lo stove su eBay live (drafts 29→28). Nessun modal di conferma è apparso. Danno reale: 1 publish live avvenuto in fase diagnostica e **prima di impostare il prezzo**. Mitigazione [OBSERVED]: la dynamic pricing policy AutoDS lo ha prezzato a **$19.97** (buy $9.49, profit $7.13), non $0.
- **CAUSA:** [OBSERVED] assunzione errata (ereditata da `publish_duck.py`, che attendeva un dialog di conferma) che "Import" apra un modal confermabile. In realtà la card **"Import" = publish immediato, senza conferma** → ho cliccato un controllo mutante credendolo ispezione read-only.
- **REGOLA:** (1) un probe DIAGNOSTICO non clicca MAI controlli che mutano stato (Import/Save/Publish/Delete/Reprice); per ispezionare il flusso si legge il DOM **senza attivare** i bottoni. (2) "Import" su card AutoDS è **azione live immediata** → eseguibile solo deliberatamente sotto GO e con l'assert di scoping **E-002** (il card che possiede il bottone deve contenere l'identificativo del target) **fatto PRIMA** del click. (3) Publish va sempre preceduto da verifica del **prezzo** (mai pubblicare a $0; affidarsi alla pricing policy solo dopo averla confermata attiva).
- **TEST DI REGRESSIONE:** prima di eseguire qualunque probe `_*.py` read-only → grep di `.click(` su Import/Save/Publish/Delete = deve dare **ZERO**. Publish solo via script che stampa e **asserisce** `card_title == target` prima del click (regola E-002). [DA ESEGUIRE a freddo prima del prossimo publish automatizzato].

## E-002 — Publish del draft SBAGLIATO su eBay live (scoping per-card difettoso)
- **Data:** 2026-06-17 (GO_PUBLISH duck topper) · **Fix:** (questo commit) + regola sotto
- **ERRORE:** doveva pubblicarsi il draft **duck topper**; invece è stato pubblicato il draft **pegboard** (`B07QR36Z76`) su eBay live. Danno reale: 1 listing eBay non voluto andato live (Prodotti attivi 177→178); il duck è rimasto draft. Non un near-miss: azione live su store reale sull'item sbagliato.
- **CAUSA:** [OBSERVED] in `publish_duck.py` lo scoping del bottone "Import" risaliva gli antenati dell'input-titolo del duck e cliccava **il PRIMO bottone "Import" trovato nel DOM** a un livello antenato condiviso → quel bottone apparteneva a un altro card (pegboard, precedente in DOM). L'ancestor-climb ha superato il confine del card.
- **REGOLA:** per QUALSIASI azione live per-item (publish/delete/reprice) il controllo da cliccare va scelto **verificando che il SUO card contenga l'identificativo univoco del target** (titolo/item-id), non con "risali-e-clicca-il-primo-match". Pattern corretto = matching per-riga/per-card sul contenuto (come `remove_oos_listings.py`, che leggeva gli item-id di ogni riga e ha targettizzato correttamente 37 item). **Prima di ogni publish automatizzato: dry-run che stampa il TITOLO del card proprietario del bottone trovato e asserisce == target; nessun click se non combacia.** Su store live, in caso di dubbio sullo scoping → azione manuale dell'owner.
- **TEST DI REGRESSIONE:** dry-run scoper che, per il target, restituisce il titolo del card che possiede il bottone "Import"/azione e verifica l'uguaglianza col titolo atteso → deve dare MATCH prima di qualsiasi click live. [DA ESEGUIRE prima del prossimo tentativo di publish automatizzato] — stato attuale: automazione publish SOSPESA, recovery in corso.

## E-001 — Import incompleto evitato: glob troppo stretto sui file d'archivio
- **Data:** 2026-06-15 (missione EBAY-IMPORT / foundation merge) · **Fix:** c994aed
- **ERRORE:** durante il merge della foundation, il glob di copia `STERILE_BASELINE__*.md` non includeva `99_ARCHIVE/README.md` (1 file su 42). Near-miss: intercettato dalla reconciliation per-file PRIMA del commit, danno reale = zero (file poi copiato e committato).
- **CAUSA:** [OBSERVED] copia per pattern (glob) invece di copia per inventario completo; il pattern copriva solo i baseline e non gli altri file della stessa cartella.
- **REGOLA:** prima di committare qualunque import/merge, eseguire una reconciliation per-file sorgente→target che deve dare 0 mancanti su N totali; mai fidarsi di un glob come prova di copertura completa.
- **TEST DI REGRESSIONE:** script di reconciliation (find su sorgente → check esistenza target) = `UNRESOLVED MISSING: 0 / 42` → PASS (evidenza nel report d'import e nel run log della missione). Ri-verificato in stabilization sprint: PASS.

<!-- Nessun errore registrato. La prima voce reale va sopra questa riga. -->

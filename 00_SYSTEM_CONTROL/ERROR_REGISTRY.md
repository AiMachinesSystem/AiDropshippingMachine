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

## E-011 — Bulk `percentage_profit` IMPOSTA il margine (non "aggiunge 2%") → crollo prezzo; cold-test l'ha intercettato
- **Data:** 2026-06-24 (reprice +2% "fallo tu", GO owner) · **Fix:** nessun danno persistente — listing ripristinato + regola; tool `reprice_apply.py`.
- **ERRORE:** per fare "+2% sul prezzo" ho impostato via AutoDS Bulk Edit `Additional profit % = 2` su 1 solo annuncio (cold-test). Risultato [OBSERVED]: Splatter Screen **$20.97 → $12.97** (−38%, margine netto $7.48 → $0.68). Il campo **SETta** il margine di profitto al 2%, non "aggiunge 2% al prezzo". **Se applicato ai 96, avrebbe azzerato il margine di tutto il negozio live.** Il cold-test su 1 lo ha intercettato; listing **ripristinato a $20.97** (calibrato `percentage_profit`=74, verificato con pull fresco indipendente).
- **CAUSA:** [OBSERVED — payload `PUT v2-api.autods.com/products/<store>/bulk` = `{"bulk_changes":{"percentage_profit":{"mode":"1","value":2}}}`] il prezzo AutoDS è **calcolato** (price-monitoring ON: sell = funzione di breakeven + profit). "Additional profit %" è il margine, non un delta sul prezzo finale. Modello empirico per-item ~lineare `sell = base + (breakeven/100)·p`, ma slope/intercetta variano per item (le fee scalano col prezzo) → un valore `percentage_profit` flat NON dà "+2% del prezzo" uniforme.
- **REGOLA:** **mai bulk-applicare un cambio prezzo/profitto senza cold-test su 1 annuncio + verifica del prezzo risultante con pull fresco PRIMA del rollout.** Un "+X% sul prezzo finale" in AutoDS NON è esprimibile con un singolo `percentage_profit` flat (collassa il margine); richiede calcolo per-item (leggere prezzo corrente → target ×1.02 → calibrare il profitto per item). La disciplina cold-test-first ha evitato il danno sui 96 → confermata, obbligatoria per ogni price-write bulk.
- **TEST DI REGRESSIONE:** `reprice_apply.py` default = `--cold-test` su 1 item con verifica before/after via list API; `--all` consentito SOLO dopo un cold-test verificato; HARD-safety: scrive solo se il campo numerico è settato al valore voluto, altrimenti Cancel. [PASS — cold-test ha rilevato il crollo, rollout NON eseguito, listing ripristinato 20.97 verificato 2026-06-24.]

## E-010 — Country Location del draft non persiste via automazione (UI mostra China, backend resta US) = MURO
- **Data:** 2026-06-23 (publish 5 AliExpress via location→origine, GO owner 100% ×4) · **Fix:** nessuno; muro documentato, automazione location SOSPESA.
- **ERRORE:** per far validare il servizio shipping (errore "service not available for this item location") ho provato a cambiare la **Country Location** del draft da United States → China. Due metodi: (1) `set_location_and_publish.py` click-opzione → **TimeoutError** sull'opzione virtualizzata; (2) `set_location_china_kbd.py` keyboard type "China"+Enter → la **UI mostra "China"** e Save stampa "saved", **ma la products API rilegge `item_country_location = United States`** → la modifica **non persiste**. 0 publish sbloccati per questa via.
- **CAUSA:** [OBSERVED] il select Country Location è un AntD controllato: il click-opzione headless non aggancia l'item virtualizzato; la selezione via keyboard aggiorna l'**etichetta visibile** ma **non fa scattare l'`onChange`** che committa lo state React → Save scrive il valore vecchio (US). (Contrasto: in `set_shipping_and_publish.py` lo Shipping Method fu **cliccato** con successo → onChange scattato → `type=4` persistito e verificato.) Possibile concausa: city `Las Vegas, NV` incoerente con country China → revert backend.
- **REGOLA:** la **Country Location del draft NON è cambiabile in modo affidabile via automazione headless** (muro, come reprice E-007 e dropdown shipping originale). Per cambiarla serve **un essere umano nella UI AutoDS** (o browser visibile guidato). Mai dichiarare la location cambiata senza **verifica via products API** (`item_country_location`), non dalla sola etichetta UI. Dopo 2 metodi falliti → STOP, handoff owner.
- **TEST DI REGRESSIONE:** `set_location_china_kbd.py <id> <guard> 0` → stampa `VERIFY item_country_location = <valore>`: è PASS solo se ritorna "China"; finché ritorna "United States" la via è murata. Evidenza: questa sessione (selector="China" ma API="United States"). **Anche in HEADED (browser visibile) la click sull'opzione fallisce (`clicked China option: False`) e il valore non persiste → muro confermato 3 volte (headless-click, headless-keyboard, headed).** [Riprovare SOLO via UI manuale dell'owner / o eBay Business Policy — NON ritentare l'automazione, headed inclusa.]

## E-009 — Workflow scout: 6/8 finder rate-limited (concorrenza di agenti Opus-1M pesanti)
- **Data:** 2026-06-23 (missione us-product-scout-run, `wf_1b7e7c8e-880`, GO owner "DO EVERYTHING") · **Fix:** re-run throttled (sonnet + batch); nessun codice macchina toccato.
- **ERRORE:** workflow scout con 8 finder lanciati in parallelo → **6 falliti** con `API Error: Server is temporarily limiting requests (not your usage limit) · Rate limited` (kitchen, pet, garden, fitness, tools, bath). Solo `auto` + `organization` completati. Rischio reale: il verdetto "0 GOOD" copre **2/8 categorie**, e senza dichiararlo parziale sarebbe stato letto come l'intero universo (copertura gonfiata).
- **CAUSA:** [OBSERVED] 8 agenti `claude-opus-4-8[1m]` avviati concorrenti (cap workflow min(16, cores-2)), ognuno con ~9-20 tool-call web → **throttle server-side da concorrenza**, NON limite d'uso owner. Modello pesante + alta concorrenza = rate limit transitorio.
- **REGOLA:** i finder di un workflow di ricerca web si lanciano con **modello leggero (sonnet)** e **concorrenza ridotta** (batch ≤3 con await tra i gruppi, o sequenziale), mai N agenti Opus-1M pesanti in parallelo. E: **un run parziale si DICHIARA parziale** (X/N categorie coperte) nel report e nel log — il verdetto non si estende mai alle categorie non coperte.
- **TEST DI REGRESSIONE:** re-run delle 6 categorie fallite con `model:'sonnet'` + batch ≤3 → atteso 0 rate-limit, 6/6 finder done. [DA ESEGUIRE: workflow re-run di questa stessa sessione; PASS quando le 6 categorie tornano candidati senza errori di throttle].

## E-008 — Root-cause "shipping type 2→4 fixa i 5 AliExpress" FALSIFICATA (verifica solo lato AutoDS, mai su eBay)
- **Data:** 2026-06-23 (publish 5 AliExpress, GO owner 100%) · **Fix:** nessun codice; root-cause corretta + regola di verifica end-to-end.
- **ERRORE:** la sessione precedente aveva dichiarato come CAUSA PRIMARIA dei 5 draft non pubblicabili il `preferred_shipping_type 2→4` e scritto in NEXT_ACTIONS il "FIX (deciso)". Test reale: ho impostato e **verificato `type=4`** su Book Light e Squeegee (letto dalla products API), poi pubblicato → **eBay ha restituito gli STESSI errori**: Squeegee ancora *"This shipping service is not available for this item location"*, Book Light ancora `EbayViolation`. Il fix "deciso" non pubblica nulla. ~0/5 sbloccati, ~4 tentativi di publish/shipping spesi su una diagnosi sbagliata ereditata.
- **CAUSA:** [OBSERVED] (1) il `type` è un'astrazione AutoDS (`Cheapest/Fastest with tracking`) che risolve a un **servizio origine-Cina**; con **Country Location = United States** sul draft eBay rifiuta (nessun servizio valido per quella location) — il numero di type non è la leva. (2) Lo store ha **business_policy = NULL** (Payment/Shipping/Return Policy tutte vuote sul draft). (3) Errori distinti per item (shipping-location vs `EbayViolation` generico) → NON un blocco account (account 503 live attivo). La diagnosi precedente ha confuso "type=4 salvato in AutoDS" con "accettato da eBay".
- **REGOLA:** una root-cause di un publish-fail si dichiara VERA **solo dopo aver applicato il fix a UN draft e letto il `error_list` per-item DOPO un tentativo reale di publish** (verifica end-to-end su eBay, non solo lo stato salvato in AutoDS). "Verificato in AutoDS" ≠ "accettato da eBay". Mai scrivere "FIX (deciso)" in NEXT_ACTIONS senza questo giro su 1 item. Vale anche §0.4 (claim load-bearing = etichetta evidenza + test).
- **TEST DI REGRESSIONE:** Book Light/Squeegee con `type=4` verificato → publish → `error_list` invariato (EbayViolation / "service not available for item location"). FALSIFICA registrata. Evidenza: output tool di questa sessione + `90_CACHE/fetches/autods/draft_econ_2026-06-23_232632`. Il fix vero (US business policy O location=origine) sale a decisione owner.

## E-007 — Reprice via AutoDS Bulk Edit = MURO (search non filtra → targeting sbagliato)
- **Data:** 2026-06-22 (tentativo reprice 2 Ham Maker, GO owner) · **Fix:** nessuno; muro documentato, attempt abortito senza write.
- **ERRORE:** per riprezzare un listing specifico via Bulk Edit serve selezionarlo; ma la "Search anything" di AutoDS **non filtra la griglia /products**. La verifica ha letto prezzi di **altri prodotti** ($9.99/$20.97/$7.48/$9.88) invece del Ham Maker ($41.83) → la checkbox spuntata era del prodotto sbagliato. **Se avessi premuto Update avrei riprezzato il listing sbagliato su un negozio live.** Inoltre il modale Bulk Edit non espone il campo prezzo nel dump (UI non mappata).
- **CAUSA:** [OBSERVED] la search-box è globale (header), non un filtro-griglia; il filtro per item_id richiede il flow "Add Filter" (non mappato). Selezione per-riga senza filtro affidabile = non deterministica.
- **REGOLA:** **non eseguire price-write per-listing finché il targeting non è deterministico** (filtro item_id verificato → 1 sola riga → match id confermato PRIMA di toccare il prezzo). La disciplina "osserva prima di scrivere" ha evitato un mis-pricing live: confermata. 2 tentativi → MURO, stop.
- **TEST DI REGRESSIONE:** `reprice_one.py` aborta senza write se non trova affordance fixed-price univoca; verifica before/after del prezzo del **giusto** item_id obbligatoria. [Re-tentare solo dopo aver risolto il filtro griglia.]

## E-006 — skill-creator `run_loop` non gira su Windows (claude.ps1) → metriche trigger fasulle
- **Data:** 2026-06-22 (ottimizzazione description di `dropship-profit-run`) · **Fix:** nessuno applicato; muro documentato + regola di non-fiducia.
- **ERRORE:** `python -m scripts.run_loop` (skill-creator) → exit 1. **Ogni** query di trigger ha dato `WinError 2`, producendo un **recall=0% FASULLO** (sembrava che la skill non si attivasse mai). Il crash finale è in `improve_description.py`.
- **CAUSA:** [OBSERVED] su Windows `claude` è `claude.ps1`, non un `.exe`; lo script fa `subprocess.run(["claude", ...])` senza shell → `CreateProcess` non trova un eseguibile `claude` nudo. Tutte le invocazioni `claude -p` falliscono.
- **REGOLA:** l'ottimizzazione automatica delle description via `run_loop` è un **MURO NOTO** su questa macchina Windows. Le sue metriche di trigger qui sono **artefatti, mai citabili**. Per verificare una skill usare il **subagent sanity-test reale** (osservato funzionante); per ottimizzare la description, girare dove `claude` è un eseguibile diretto o wrappare `claude.ps1`. 2 tentativi → [BLOCKED], avanti.
- **TEST DI REGRESSIONE:** ri-eseguire riprodurrebbe `WinError 2` finché l'harness non invoca claude via shell. Baseline documentata; recall del log scartato.

## E-005 — Contatore delete inaffidabile + righe non-spuntabili (bulk-delete AutoDS)
- **Data:** 2026-06-22 (KILL 120 morti+errati, GO owner "all of them") · **Fix:** nessuna modifica al tool necessaria; regola di verifica obbligatoria (sotto). Verifica a freddo PASSATA.
- **ERRORE:** il loop `remove_oos_listings.py --confirm` ha stampato `deletions performed: 158 / 113` (impossibile, >target), con id duplicati ripetuti nel log (es. `407007332384` "deleted" 6×, un batch di 11 contato 5×). 4 righe (`406103165492`, `406103155439`, `406096432417`, `406092459629`) non si spuntano mai (TimeoutError sul check) → non cancellabili dal tool.
- **CAUSA:** [OBSERVED] il loop reload-rescan ri-trova gli stessi id PRIMA che la griglia AntD si riflussi dopo il delete (o dopo un batch fallito a metà via TimeoutError) → il contatore `total` doppio-conta; **il numero stampato NON è un conteggio reale di cancellazioni**. Le 4 righe ostinate hanno checkbox detached/overlay non interagibili headless.
- **REGOLA:** mai fidarsi del contatore del tool di delete. **Ogni azione distruttiva si VERIFICA con un read indipendente a freddo** (conteggio live + sopravvivenza della keep-list) prima di dichiararla fatta. Righe non-spuntabili dopo 2 passate → lasciare all'owner (manuale), non loopare (regola STOP 2-fallimenti).
- **TEST DI REGRESSIONE:** audit fresco `90_CACHE/.../audit_2026-06-22_044324` → **99 listing vivi (da 207, ~108 rimossi), 13/13 winner presenti, errori 129→21, vendite totali invariate (35)**. PASS (verificato indipendentemente dal log del tool).

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

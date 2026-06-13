---
tags:
  - machine
  - mission
type: mission
status: template
description: "Scheletro riutilizzabile per una missione autonoma (es. run notturno). Ricostruito come template: struttura, regole di ingaggio, fasi, recovery e report — nessuna domanda, competitor, dato o risposta attesa di una macchina specifica."
---

# `<MISSION_NAME>` — RUN AUTONOMO (`<YYYY-MM-DD>`)

**Owner:** `<OWNER_NAME>` · **Autorizzazione:** missione intera, entro le Regole di Ingaggio §0.
**Durata target:** `<es. 2,5–3 ore>`. **Modalità:** autonoma.
**Principio:** il bypass dei popup NON toglie le regole. Le regole §0 sono vincolanti.

---

## §0 · REGOLE DI INGAGGIO (vincolanti, prevalgono su tutto il resto)

**VIETATO in qualunque fase:**
1. Azioni live esterne: acquisti, registrazioni (domini inclusi), login, creazione account, invio email/messaggi, contatti con persone, qualunque spesa.
2. Scritture su integrazioni esterne (store, ads, email, ecc.). Il web è SOLO lettura di pagine pubbliche (metodo proxy già in uso).
3. Toccare i file dei progetti sotto FIREWALL (`<FIREWALL_PROJECT>` e gate di lancio): firewall totale tra progetti, nessun travaso.
4. Cancellazioni fuori dalle cartelle create da questa missione. Mai `git push --force`, mai riscrivere la history, mai toccare `.git` a mano.
5. Installazioni: solo pacchetti locali dev e SOLO se una task li richiede davvero; ogni install loggata con motivazione. Preferenza: zero install.

**OBBLIGATORIO:**
- Disciplina evidenze invariata: [OBSERVED — fonte+data] / [INFERRED — base] / [UNKNOWN]. Conteggi = lower bound. Assenze = LOW-SAMPLE. Mai inventare, mai stimare.
- `git commit` a fine di OGNI fase, messaggio con prefisso `<MISSION_PREFIX>:`.
- Log continuo in `00_SYSTEM_CONTROL\<MISSION_NAME>_RUN_LOG.md`: dopo ogni step scrivi progresso, decisioni, file toccati. **Se la sessione si compatta: rileggi questo file di missione + il run log e riprendi dall'ultimo step loggato.**
- REGOLA OROLOGIO: ogni data/ora da `Get-Date` al momento della scrittura, mai aritmetica sui timebox.
- Timebox per fase (sotto). Muro o fetch fallito ≥2 volte → [UNKNOWN] + avanti. Niente loop.
- STOP CONDITION: stato git anomalo o qualunque ambiguità che richiederebbe un'azione vietata → interrompi e salta alla Fase finale (report), spiegando.

---

## FASE 1 · `<NOME FASE>` (~`<min>`)
`<obiettivo della fase, input, output, criterio di chiusura>`
> (Se la fase include un self-test QUERY MODE, definisci le domande dai TUOI canoni registrati — mai da dati di altre macchine.)

## FASE 2 · `<NOME FASE>` (~`<min>`)
`<...>`

## FASE 3 · `<NOME FASE>` (~`<min>`)
`<... eventuali sotto-fasi 3A/3B/3C, ognuna alimenta la successiva>`

## FASE N · REPORT (OBBLIGATORIA, anche se le fasi prima sono incomplete)
Crea `00_SYSTEM_CONTROL\<MISSION_NAME>_RUN_REPORT_<YYYY-MM-DD>.md` con: fasi completate/saltate e perché · OGNI file creato/modificato con path · OGNI commit con hash · install effettuate (se nessuna: dichiaralo) · top finding · decisioni che restano all'owner · cosa richiede GO esplicito · UNKNOWN residui. Ultima riga del run log: `DONE — <ora reale>`.

---

**Promemoria:** la qualità si misura in evidenze etichettate e reversibilità, non in quantità di file. Meglio una fase saltata e dichiarata che una riempita di contenuto inventato. Le decisioni live/GO restano dell'owner.

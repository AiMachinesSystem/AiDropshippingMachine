# Skill della macchina — toolkit di metodo (template)

Questo `.claude\` contiene il **toolkit di metodo** universale della macchina: command + skill di
intelligence/execution riutilizzabili su QUALSIASI dominio. Sono sterilizzati — nessun dato,
brand, nicchia o numero di una macchina specifica.

## Come usarle
- Le skill possono vivere globalmente in `~\.claude\skills\` (disponibili a tutti i progetti della
  macchina) oppure dentro il repo in `.claude\skills\` (versionate col template). Questo template le
  porta nel repo per portabilità; se preferisci, copiale in `~\.claude\`.
- I command in `.claude\commands\` sono wrapper sottili che invocano le skill omonime.

## Skill incluse (metodo, sterili)
- **niche-intelligence-run** · **competitor-scan** · **ads-library-scan** — motore di ricerca mercato/competitor/ads.
- **launch-prep** — launch pack GATED (gate zero = provenienza/diritti prodotto).
- **creative-brief-builder** → **higgsfield-prompt-builder** → **test-plan-builder** — pipeline creativa data-driven (generazione/spesa = GO).
- **landing-page-review** · **offer-diagnosis** · **customer-voice-mining** — audit/diagnosi/voce cliente.
- **weekly-learning-update** · **vault-librarian** · **vision-check** — manutenzione e allineamento.
- **portfolio-review** — STUB dichiarato: si attiva con ≥2 progetti live + connettori dati.

## NON incluse (dipendenze esterne, da installare per macchina)
Le skill di terze parti installate globalmente (es. set Obsidian come `kepano/obsidian-skills`, e i
built-in di Claude Code) **non fanno parte di questo template**: sono dipendenza personale/globale.
Installale separatamente nella nuova macchina se le vuoi; non vengono ereditate dal template.

## Disciplina
Ogni skill rispetta: GO gate · etichette evidenza · cache evidenze prima di citare · QUERY MODE prima
di RUN MODE · registrazione indice + AUTO-REFRESH cockpit a fine run · firewall tra progetti.

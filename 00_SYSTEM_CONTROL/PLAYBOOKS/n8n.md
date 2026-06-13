---
tags:
  - machine
type: playbook
status: active
date: 2026-06-12
---

# PLAYBOOK — n8n locale via npm (studiato 2026-06-12, NON installato)

**Gap che chiuderebbe:** Layer 5 (automazione) — classe A per criteri 1-4 §0.1,
**BLOCKED dal criterio 5 (budget)**: install globale reale ≈ 0,8–1,5 GB di
node_modules [INFERRED — nessuna cifra ufficiale; pacchetto solo = 15 MB
OBSERVED registry] > budget missione 500 MB. → Install rinviata a roadmap.

- **Requisiti:** Node 20.19–24.x ("inclusive" [OBSERVED — docs.n8n.io npm
  installation, 2026-06-12]) → Node 24.16.0 locale OK.
- **Install (quando autorizzata):** `npm install n8n -g` — NESSUN account/
  chiave richiesto per installare; l'owner account si crea solo al PRIMO
  AVVIO del server, in locale [OBSERVED — docs user-management-self-hosted].
- **Verifica senza avviare nulla:** `npm list -g n8n` (zero side-effect);
  `n8n --version` stampa la versione senza avviare il webserver ma può creare
  `%USERPROFILE%\.n8n` (config+SQLite) [INFERRED — CLI oclif standard].
- **MAI usare** `npx n8n` per provare: scarica E AVVIA il server.
- **Workflow come file:** i workflow sono JSON; import a server spento via
  `n8n import:workflow --input=file.json` (di default importati DISATTIVATI)
  [OBSERVED — docs CLI commands]. → autorabili ora, eseguibili poi.
- **Uninstall pulito:** `npm uninstall -g n8n` + cancellare manualmente
  `%USERPROFILE%\.n8n` se creata.
- **Servizi/autostart:** nessuno creato dall'install [OBSERVED — omissione
  docs + i docs raccomandano PM2/systemd manuali per tenerlo su].
- **Rischi noti:** telemetria di default al primo avvio (disattivabile via
  env var); footprint disco non documentato; edge case `isolated-vm` su Node
  24 segnalati dalla community [INFERRED — non confermati dai docs].
- **Workflow d'esempio pronti (non connessi):** `PLAYBOOKS\n8n_workflows\`.

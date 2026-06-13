# machine-template — scheletro madre per macchine di intelligence & execution

Template **sterile e riutilizzabile** per creare nuove macchine (Claude Code + Obsidian) con la
stessa OS di governance: costituzione, GO gate, autonomia controllata, disciplina evidenze,
firewall tra progetti, registro errori → regole → regression, recovery da compaction, convenzioni
vault, template di output, playbook strumenti e un toolkit di skill/command di metodo.

**Questo template NON contiene dati, brand, nicchie, output, numeri o decisioni di nessuna macchina
di dominio.** È solo lo strato sistema, genericizzato con placeholder.

---

## ISTANZIARE UNA NUOVA MACCHINA (5 passi)

1. **Copia** `machine-template` in una cartella nuova (es. `C:\Ai Machines\<nome-macchina>\`).
2. **Rinomina** la cartella col nome della macchina.
3. **Sostituisci i placeholder principali** (cerca `<...>` in tutto il repo): almeno
   `<MACHINE_NAME>`, `<OWNER_NAME>`, `<OWNER_LANGUAGE>`, `<DOMAIN_NAME>`, `<PRIMARY_OBJECTIVE>`,
   `<NORTH_STAR>`, `<DATA_SOURCES>`, `<LIVE_ACTION_RULES>`, `<PROJECT_A/B>`, `<NICHE>`,
   `<VAULT_ROOT>`, `<DATA_ESTRAZIONE>`. (Tabella completa sotto.)
4. **Inizializza/resetta git** nella nuova macchina (`git init`; nuovo repo, storia pulita; il
   remote NON è ereditato).
5. **Battesimo iniziale** con `00_SYSTEM_CONTROL\SESSION_START_PROTOCOL_v0.1.md`, poi compila
   `VISION_ALIGNMENT.md` (vision/North Star/asset map reali) e `VISION_SCHEMA.md` (stack reale).

---

## COSA CONTIENE IL TEMPLATE

- **Costituzione operativa** (`CLAUDE.md`): regole permanenti §1–9 + AUTONOMIA CONTROLLATA v0.1.
- **00_SYSTEM_CONTROL**: VISION_ALIGNMENT · VISION_SCHEMA · VISION_GAP_MATRIX (skeleton) ·
  RESEARCH_MEMORY_INDEX (schema vuoto + CANONE/STORICO) · MACHINE_STATE (sola genealogia) ·
  BACKLOG · NEXT_ACTIONS · MASTER_DASHBOARD (scheletri vuoti) · ERROR_REGISTRY (vuoto + formato) ·
  SESSION_START_PROTOCOL · VAULT_CONVENTIONS · TEMPLATES\ · PLAYBOOKS\ (+ n8n_workflows) ·
  BASES\ · MISSION_TEMPLATES\ · TASKS\ · DECISIONS\.
- **09_TEMPLATES**: template di output riutilizzabili (analysis, kpi, strategy, sop, learning, ecc.).
- **.claude\**: 5 command + toolkit di skill di metodo sterilizzate (vedi `.claude\skills\README.md`).
- **Alberatura completa** dei moduli (00→99 + `_ARCHIVE`) con `.gitkeep`; `90_CACHE` non versionata.

## COSA NON CONTIENE

Nessun output (`10_OUTPUTS` vuoto) · nessuna cache · nessun report storico · nessuna nota
entità/task/decisione di dominio · nessun dato business (brand, nicchie, competitor, customer
voice, ads, store, metriche, revenue, prezzi, CAC/ROAS/margini) · nessun ERROR_REGISTRY popolato ·
nessuno SKILL_SNAPSHOTS · nessuna credenziale/token · nessun contenuto della macchina sorgente.
Il modulo `01_SYSTEM` è uno scheletro vuoto: i protocolli di dettaglio della macchina sorgente NON
sono inclusi (il loro metodo universale è consolidato nella costituzione `CLAUDE.md`).

## COME EVITARE CONTAMINAZIONE

- **Non copiare dati dalla macchina sorgente.** Il template è la SOLA base; non importare output,
  decisioni, asset o canoni di una macchina esistente.
- Ogni nuova macchina parte con `RESEARCH_MEMORY_INDEX`, `MACHINE_STATE`, `BACKLOG`,
  `MASTER_DASHBOARD` e `ERROR_REGISTRY` **vuoti**.
- Il **firewall tra progetti** vale dal giorno uno: nessun travaso tra progetti/nicchie/dati.
- La **genealogia** in `MACHINE_STATE.md` dichiara solo l'origine TECNICA del template, non
  un'identità: la nuova macchina non è la macchina sorgente.

## CREARE UNA NUOVA MACCHINA DI DOMINIO

Dopo i 5 passi: definisci `<DOMAIN_NAME>` e il `<NORTH_STAR>` in `VISION_ALIGNMENT.md`, registra i
primi progetti nell'asset map, configura `<DATA_SOURCES>` e i connettori (read-only first), poi
lavora per INTENTI (la macchina propone missione + classe di rischio e procede sull'interno fino
alla raccomandazione). Nessuna azione live senza GO.

## SKILL GLOBALI ESTERNE (NON parte del template)

Le skill di terze parti installate globalmente in `~\.claude\skills` (es. set Obsidian come
`kepano/obsidian-skills`) e i built-in di Claude Code sono **dipendenza personale/globale**: non
sono incluse nel repo template e non vengono ereditate. Installale separatamente se le vuoi.

---

## TABELLA PLACEHOLDER

| Placeholder | Significato |
|---|---|
| `<MACHINE_NAME>` | nome della macchina istanza |
| `<MACHINE_TYPE>` | tipo (es. "portfolio-level intelligence & execution machine") |
| `<OWNER_NAME>` | nome dell'owner |
| `<OWNER_LANGUAGE>` | lingua delle comunicazioni con l'owner |
| `<DOMAIN_NAME>` | dominio/verticale di business |
| `<PRIMARY_OBJECTIVE>` | obiettivo primario (il "perché" della macchina) |
| `<NORTH_STAR>` | obiettivo di portafoglio (target di lungo periodo) |
| `<PROJECT_A>` / `<PROJECT_B>` | progetti/asset; `<project-slug>` per le cartelle |
| `<FIREWALL_PROJECT>` | progetto sigillato dal firewall (esempio) |
| `<NICHE>` | una nicchia di mercato |
| `<DATA_SOURCES>` | fonti dati collegate (es. store, ads, analytics, email) |
| `<LIVE_ACTION_RULES>` | cosa conta come azione live/esterna (GO-gated) |
| `<RISK_RULES>` | regole di classificazione del rischio |
| `<DOMAIN_REGISTRY>` / `<ASSET_REGISTRY>` | registri di domini/asset |
| `<PROJECT_A_TAG>` / `<PROJECT_B_TAG>` | tag Obsidian dei progetti (per le Bases) |
| `<VAULT_ROOT>` | path filesystem della root del vault |
| `<DATA_ESTRAZIONE>` | data di estrazione del template (genealogia) |
| `<DATE>` / `<YYYY-MM-DD>` | segnaposto data (sempre da `Get-Date`) |
| `<vN>` | versione (skill, documento) |

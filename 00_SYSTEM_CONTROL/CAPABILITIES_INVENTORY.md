---
tags:
  - machine
type: reference
status: active
created_real: 2026-06-17
description: "Inventario completo delle capacità della macchina: skill di business, skill di sviluppo, utility, comandi harness, integrazioni operative reali. Più analisi delle COMBINAZIONI (catene di skill) e di cosa la macchina è in grado di fare end-to-end. Snapshot 2026-06-17."
---

# CAPABILITIES INVENTORY — cosa la macchina sa fare

> Snapshot creato 2026-06-17 20:52 (ora di sistema). Inventario + analisi delle combinazioni.
> Aggiornare quando si installano/rimuovono skill o integrazioni.

---

## A · SKILL DI BUSINESS (eBay/AutoDS Dropshipping)

### A1 · Ricerca & analisi di mercato (interne, no GO)
| Skill | Cosa fa | Output |
|---|---|---|
| niche-intelligence-run | valida nicchia/mercato (da nicchia, URL prodotto o competitor): dimensione, censimento competitor, domanda/dolore | verdetto entra/non-entra + confidenza |
| competitor-scan | teardown brand/batch: posizionamento, offerta, funnel, creatività, trust/compliance | score 1-5 + minaccia |
| ads-library-scan | Meta Ad Library: ads attive, longevità (proxy performance), hook, copy, cluster vincitori | conteggi lower-bound + pattern |
| customer-voice-mining | voce reale clienti da fonti pubbliche (recensioni, Reddit, forum) | quote bank con fonte+data |
| landing-page-review | audit landing pubblica: hook, offerta, prove, attrito, integrity | punteggio 1-5 con rubrica |
| offer-diagnosis | diagnosi offerta vs canone mercato: prezzo, anchor, garanzia, claim | gap + raccomandazione |

### A2 · Diagnosi asset posseduti (read-only, raccomandano)
| Skill | Cosa fa |
|---|---|
| store-diagnosis | Shopify: revenue/AOV/trend, performance prodotti, resi, leakage sconti, funnel |
| meta-ads-diagnosis | Meta: spesa/ROAS/CPA/CTR per ad, vincitori vs perdenti, fatica creativa |
| google-ads-diagnosis | STUB — manca connettore Google Ads |
| portfolio-review | STUB — si attiva con ≥2 progetti live con metriche |

### A3 · Pipeline creativa & lancio (catena drafting; spesa/publish = GO)
| Skill | Cosa fa |
|---|---|
| creative-brief-builder | brief creativo data-driven per testare ad/asset |
| higgsfield-prompt-builder | brief → prompt pronti per Higgsfield (immagine/video) |
| test-plan-builder | piano test misurabile: variabili, metriche pre-spesa, kill criteria |
| launch-prep | launch pack GATED; gate zero = provenienza/diritti prodotto |

### A4 · Governance & manutenzione
| Skill | Cosa fa |
|---|---|
| daily-brief | brief del giorno dal cockpit |
| vault-librarian | audit/riordino alberatura e indici del vault |
| vision-check | check piano/azione vs costituzione e gate |
| weekly-learning-update | sintesi settimanale: delta indici, muri, drift backlog |

---

## B · SKILL DI SVILUPPO (Superpowers)
brainstorming · writing-plans · executing-plans · subagent-driven-development · test-driven-development ·
systematic-debugging · verification-before-completion · requesting-code-review · receiving-code-review ·
using-git-worktrees · finishing-a-development-branch · dispatching-parallel-agents · writing-skills · using-superpowers
→ disciplina per costruire/riparare codice, automazioni e nuove skill.

---

## C · SKILL OBSIDIAN & UTILITY
graphify (input → grafo di conoscenza interrogabile) · obsidian-cli · obsidian-markdown · obsidian-bases ·
json-canvas · defuddle (estrazione web pulita).

---

## D · COMANDI HARNESS (Claude Code)
code-review · simplify · security-review · review · verify · run · deep-research · loop · schedule ·
init · update-config · keybindings-help · fewer-permission-prompts · claude-api · ralph-loop.

---

## E · INTEGRAZIONI OPERATIVE REALI
| Integrazione | Stato | Cosa permette |
|---|---|---|
| AutoDS via Playwright | OPERATIVO (sessione salvata) | leggere store/listing/draft/ordini + scrivere (rimozioni, import draft) — write = GO |
| Higgsfield (MCP) | OPERATIVO | generazione reale immagini/video — crediti = GO |
| Shopify (MCP) | disponibile, non usato (firewall) | gestione store completa |
| Web pubblico | OPERATIVO | proxy r.jina.ai, evidenze in cache |

---

## F · CAPACITÀ DI SISTEMA
Scrittura/debug codice (Python, automazioni) · orchestrazione multi-agente (squadre in parallelo) ·
memoria interrogabile QUERY MODE (RESEARCH_MEMORY_INDEX) · governance & versioning git.

---

## G · LIMITE INVALICABILE
Niente di live/esterno senza GO esplicito owner (publish/modifica listing, prezzi, ordini, spese, login).
Gate per-azione: un GO non si trasferisce mai allo step successivo.

---

# H · ANALISI — COSA SO FARE COMBINANDO LE SKILL (catene end-to-end)

> Il valore non sta nelle singole skill ma nelle CATENE. Qui le combinazioni che la macchina
> può eseguire realmente oggi, con il punto esatto in cui scatta il GO.

### Catena 1 · DA "NICCHIA IGNOTA" A "DRAFT PRONTO" (validazione → lancio)
niche-intelligence-run → competitor-scan → ads-library-scan → customer-voice-mining → offer-diagnosis
→ creative-brief-builder → higgsfield-prompt-builder → [Higgsfield genera = GO] → launch-prep + test-plan-builder
→ [AutoDS import draft via Playwright = GO] → [publish eBay = GO].
**Risultato:** posso portare un prodotto da "idea" a "draft pronto + creatività + piano di test", fermandomi a ogni gate live.

### Catena 2 · OTTIMIZZAZIONE DI UN LISTING ESISTENTE
AutoDS read (Playwright) legge il listing → landing-page-review / offer-diagnosis valutano copy e prezzo
→ customer-voice-mining alimenta il copy con linguaggio reale → riscrittura titolo (≤80) + descrizione VeRO-safe
→ higgsfield genera immagine pulita (GO) → [apply su draft / publish = GO].
**Risultato:** ciclo completo di miglioramento di un listing già attivo, dall'analisi all'asset.

### Catena 3 · INTELLIGENCE COMPETITIVA CONTINUA
ads-library-scan (cosa girano i competitor) + competitor-scan (come vendono) + customer-voice-mining (cosa odiano i clienti)
→ sintesi in RESEARCH_MEMORY_INDEX → weekly-learning-update tiene il polso nel tempo.
**Risultato:** monitoraggio del mercato che si accumula come memoria interrogabile.

### Catena 4 · DIAGNOSI E DECISIONE SU ASSET POSSEDUTI
store-diagnosis / meta-ads-diagnosis leggono i dati reali → offer-diagnosis confronta col canone
→ test-plan-builder definisce l'esperimento di fix → vision-check valida prima di agire.
**Risultato:** dal dato grezzo alla decisione scale/pause/refresh con un piano misurabile.

### Catena 5 · SCALA TRAMITE ORCHESTRAZIONE MULTI-AGENTE
dispatching-parallel-agents lancia N agenti che eseguono in parallelo niche-run/competitor-scan/ads-scan
su nicchie diverse → sintesi unica.
**Risultato:** non analizzo 1 nicchia per volta ma 10 in parallelo (es. capability audit 7-agenti, deep product research).

### Catena 6 · COSTRUZIONE DI NUOVE CAPACITÀ (auto-evoluzione)
Un pattern ricorrente → brainstorming → writing-plans → test-driven-development → writing-skills
→ nuova skill/tool Python (es. i tool Playwright AutoDS) → verification-before-completion.
**Risultato:** la macchina costruisce i propri strumenti operativi (è già successo per Playwright/AutoDS).

---

# I · LETTURA CRITICA (dove sono forte, dove sono debole)

**FORZA REALE (provata):**
- Pipeline di ricerca/analisi completa e disciplinata, con evidenze etichettate e memoria.
- Integrazione AutoDS read+write OPERATIVA (non teorica): rimozioni e import draft già eseguiti.
- Generazione asset reale (Higgsfield) e orchestrazione multi-agente provate.

**DEBOLEZZA / DIPENDENZE:**
- Il motore vendite live dipende da gate owner per ogni write → la velocità è limitata dalle tue decisioni, non dalle mie capacità.
- Higgsfield "Simple page" AutoDS non accetta upload immagine custom → l'immagine va su eBay post-publish.
- Descrizione draft AutoDS con rich-editor = non automatizzabile (incolla manuale).
- Diagnosi Google Ads e portfolio-review = STUB (non eseguibili).
- I numeri di mercato sono lower-bound da proxy, non dati ufficiali → confidenza dichiarata, mai gonfiata.

**CONCLUSIONE:** la macchina è oggi un sistema completo di **ricerca → strategia → produzione asset → draft**,
con il braccio operativo AutoDS reale. Il collo di bottiglia non è la capacità ma il numero di GO che servono
per passare da "draft pronto" a "vendita live".

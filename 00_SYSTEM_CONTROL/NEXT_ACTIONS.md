---
tags:
  - machine
type: log
status: template
description: "Lista chiara delle prossime azioni. Refreshata a fine run (regola AUTO-REFRESH). PARTE VUOTO in una nuova macchina."
---

# Next Actions

> Modulo: 00_SYSTEM_CONTROL. Aggiornata a ogni fine run insieme a MASTER_DASHBOARD
> (regola AUTO-REFRESH: run senza refresh = INCOMPLETO).

## ⚡ CHECKLIST MANUALE BROWSER OWNER
<!-- Azioni che solo l'owner può fare a mano (login, dropdown geo/reach, ecc.), con URL espliciti. -->
- `<azione manuale owner + URL>`

## Exact Next Step
> `<lo step successivo più ad alto impatto, una sola azione>`

## Parked Options (each needs its own explicit GO)
1. `<opzione parcheggiata + gate>`

## Waiting / Blocked
- `<item bloccato + da chi>`

## Completed
<!-- [x] YYYY-MM-DD — azione completata -->

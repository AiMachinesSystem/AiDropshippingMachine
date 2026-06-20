---
type: reference
status: active
date: 2026-06-19
created_real: 2026-06-19
description: "Workflow n8n scaricabili/importabili per chi vende prodotti digitali online: 1 template ufficiale gratuito reale (3391) + 1 scheletro su misura (vendita -> consegna automatica via email). + indice fonti verificate. Ricerca pubblica owner 2026-06-19. NON legato al progetto eBay/AutoDS (firewall)."
---

# n8n per vendere prodotti digitali — workflow importabili

> Ricerca pubblica del 2026-06-19. I file `.json` in questa cartella si importano in n8n:
> **Workflows -> Import from File -> seleziona il `.json` -> configura le credenziali -> Activate.**

## File in questa cartella (pronti da importare)

### 1. `stripe-order-sync-3391.json` — template UFFICIALE n8n, GRATUITO
- **Cos'è:** dopo un pagamento Stripe riuscito, recupera automaticamente cliente (nome/email) + prodotto acquistato e li prepara per CRM/inventario/notifiche.
- **Nodi (3):** Stripe Trigger on Payment Event -> Extract Session Information -> Filter Information.
- **Uso:** è il **mattone "incasso -> dati ordine"**; ci attacchi sopra l'email di consegna.
- **Fonte** [OBSERVED — scaricato via API ufficiale `api.n8n.io/api/templates/workflows/3391`, 2026-06-19, gratis "Use for free"]: https://n8n.io/workflows/3391-stripe-payment-order-sync-auto-retrieve-customer-and-product-purchased/

### 2. `digital-product-delivery-skeleton.json` — SCHELETRO su misura (costruito qui)
- **Cos'è:** flusso completo **vendita -> consegna automatica del prodotto digitale**, provider-agnostico (Stripe / Gumroad / Lemon Squeezy / Paddle via webhook).
- **Nodi (6):** Webhook (riceve la vendita) -> Map Buyer & Product (estrae email/nome/prodotto/ordine) -> Lookup Download Link / License (mappa prodotto -> URL download + genera licenza) -> Deliver Product Email (email HTML con link) -> Log Sale (Google Sheets, opzionale, disattivato) -> Setup Notes.
- **Da configurare:** URL webhook nel provider · credenziali SMTP nel nodo email · i tuoi prodotti->link nel nodo Lookup · (opz.) Google Sheet ID.
- **Nota Stripe:** il payload Stripe è annidato — per Stripe conviene usare il **Stripe Trigger** (vedi file 3391) e adattare le espressioni del nodo Map.
- [INFERRED — costruito da me su nodi core n8n; JSON validato, struttura importabile; da testare nella tua istanza n8n].

## Come importare (qualsiasi `.json`)
1. Apri n8n (cloud o self-hosted).
2. **Workflows -> Import from File** -> seleziona il `.json`.
3. Apri i nodi con credenziali (Stripe, SMTP/email, Google Sheets) e collega le tue credenziali.
4. Per il webhook: copia la **Production URL** del nodo Webhook e incollala nel tuo provider (Gumroad: Settings -> Advanced -> **Ping**; Stripe: Developers -> Webhooks; ecc.).
5. **Activate** + test ("Listen for test event" + una vendita sandbox).

## Altre fonti (cataloghi importabili)
- **Libreria ufficiale n8n** (1000+ template, molti gratis — filtra "Stripe", "Gumroad", "digital product", "ecommerce") [OBSERVED 2026-06-19]: https://n8n.io/workflows/categories/sales/
- **GitHub — collection gratuite di JSON** (Import from File):
  - `enescingoz/awesome-n8n-templates` (280+, gratis) [OBSERVED — pagina aperta 2026-06-19]: https://github.com/enescingoz/awesome-n8n-templates
  - `ScraperNode/awesome-n8n-templates` (~8.697) · `Danitilahun/n8n-workflow-templates` (2.053) [PUBLIC RESEARCH — da risultati ricerca, non singolarmente verificati].
- **Integrazioni native** per costruirti il flusso: Gumroad (`n8n.io/integrations/gumroad/`), Stripe (`n8n.io/integrations/stripe/`) [OBSERVED 2026-06-19].

## Turnkey a PAGAMENTO (consegna digitale completa, se preferisci pronto)
- **n8n 9063** "Automate digital product sales & delivery (Stripe + Email)" — **$29** [OBSERVED]: https://n8n.io/workflows/9063-automate-digital-product-sales-and-delivery-with-stripe-and-email/
- **n8n 8588** "...delivery & sales tracking (Stripe + Email + Notion + Telegram)" — **$79** [OBSERVED]: https://n8n.io/workflows/8588-automate-digital-product-delivery-and-sales-tracking-with-stripe-email-notion-and-telegram/
- Mega-pack su Gumroad (4.000+/5.000+ JSON) — [PUBLIC RESEARCH] esistono, terzi, qualità variabile.

## Avvertenze
- Conteggi e prezzi = letti **2026-06-19**, cambiano. I link n8n ufficiali + `enescingoz` + l'API 3391 sono stati aperti/verificati; le collection più grandi vengono dai risultati di ricerca.
- Lo scheletro è un punto di partenza valido ma **va testato** nella tua istanza n8n con le tue credenziali.

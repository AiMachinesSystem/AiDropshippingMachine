---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: reference
status: drafts-imported
date: 2026-06-20
created_real: 2026-06-20
description: "Scan eBay competitor + nuovi prodotti/tendenze (fuori dalle 15 nicchie sature) → 6 NUOVI prodotti verificati, importati come DRAFT da Amazon (titolo ≤80 + descrizione VeRO-safe). Workflow 28 agenti, dati citati + verifica avversariale. Richiesta owner 2026-06-20."
---

# Nuovi prodotti + competitor eBay — 2026-06-20

> Richiesta owner: *"trova su eBay competitor potenziali e vedi nuovi prodotti/tendenze; per ogni nuovo risultato metti in draft un prodotto da Amazon."*
> Workflow 28 agenti: scoperta multi-angolo (escluse le 15 nicchie sature) → fonte Amazon + copy → verifica avversariale. **6/12 candidati passati.**
> ⚠️ Costi Amazon spesso CAPTCHA → da confermare in AutoDS prima del publish. Publish = bloccato lato eBay (vedi cockpit). Sourcing Amazon = rischio policy eBay dichiarato.

## ✅ 6 NUOVI prodotti — IMPORTATI come DRAFT (titolo ≤80 + descrizione riscritta, verificati)

| # | Prodotto | Amazon ASIN | Draft ID | Costo | Vendita | Domanda eBay (lower bound) | Score |
|---|---|---|---|---|---|---|---|
| 1 | **Silicone Faucet Splash Mat** (dietro-rubinetto) | `B09QBVKFHS` | `6a37197fb9c931bd741d17ee` | ~$7.50 (da confermare) | $12.99 | 1 listing 297 sold / 35 watch; 197 watch su variante | **7** |
| 2 | **Over-Sink Roll-Up Dish Rack** (21x16, foldable) | `B07CJLSX27` | `6a3719aa1965e71cffe65152` | ~$13-17 (CAPTCHA) | $29.95 | 10+ listing attivi, $16.96–$33.58 | **7** |
| 3 | **Silicone Stretch Lids 6-pack** (food covers) | `B0FDQ54SFT` | `6a3719c84ee7478cd887fa44` | ~$7.50 (CAPTCHA) | $12.99 | comp set-3 237 sold; 6-pack 72 sold | 6.5 |
| 4 | **No-Drill Adhesive Sink Caddy** (sponge+brush) | `B08M3S94J8` | `6a3719f36b71e506fe2aae0f` | ~$8 (CAPTCHA) | $14.99 | 136 sold su un listing; supply densa | 6.5 |
| 5 | **LED Hinge Cabinet Sensor Light 12-pack** | `B08YD1MLWR` | `6a371a1836ecd8e3f187f8f2` | **$16.89 [OBSERVED]** | $24.95 | 4-pack 11 sold; categoria 149+ sold | 6 |
| 6 | **2-in-1 Foldable Backpack Stool** (seat+bag) | `B0GLHJBNZM` | `6a371a3db9c931bd741d17fa` | (CAPTCHA) | $15.99 | $10.99–12.99 attivi; proxy categoria 1.154 sold | 6 |

Titoli (tutti ≤80) e descrizioni VeRO-safe applicati e **verificati persistiti** (×6, con guard per-draft). HTML in `listings/copy_2026-06-20_new/`.

### Note per-prodotto (pre-publish)
- **#1 Faucet mat** (top, score 7): leggero/flat, resi bassi; margine sottile (~$3.37) finché costo non confermato.
- **#2 Roll-up rack**: ticket/margine più alti (~$8-10) ma **è la variante 21x16 più pesante** → verificare peso/spedizione in AutoDS (rischio margine).
- **#3 Stretch lids**: NON usare claim "FDA approved" (anti-pattern visto nei comp) → solo "food-grade silicone".
- **#5 Hinge light**: **batteria 12V/23A NON inclusa** + flag "reso per taglia inattesa" → dimensione dichiarata in descrizione; margine sottile (~$4.35).
- **#6 Backpack stool**: costo non aperto (CAPTCHA) → margine condizionale; frame rigido = dim-weight, verificare spedizione.

## 🏪 Competitor eBay individuati (intel)
| Seller / store | Cosa vende | Segnale |
|---|---|---|
| `sunshadesdepot` | car sun shades / sunshade umbrellas | 48K sold, 1.4K follower |
| Fridge storage-bin seller (itm 336386693827) | stackable fridge bins | **32K sold**, 99.6% |
| `gotenstoreus` | Home & Garden (kitchen org.) | 4K sold |
| Ultrasonic cleaner sellers | portable ultrasonic cleaners | 1.8K e ~8K sold |
| Mini vacuum-sealer seller (itm 205254309361) | handheld food vacuum sealer | 1.8K sold |
| Drain hair-catcher seller (itm 132871318520) | shower/sink drain hair catcher | 872 sold / 193 watch |
| `Leo General Merchandise` | faucet drain pad / kitchen gadgets | 297 sold (= nostro #1) |
| `householditems06` | sunset lamp projectors | 235 watch su un listing |
| `Dakota Direct` | AirTag shoe-insole holders | 247 sold (trend TikTok) |
| `dog-cats-shop` · `Pet*Supplies*Shop` · `Bargain Buy Pet Supply` | pet supplies / hammocks | dropship pet competitor |
| `WeatherTech…` | car accessories | **BRANDED** = da osservare, mai imitare (VeRO) |

> Altri segnali-prodotto emersi ma NON passati la verifica (idea per il futuro): sunset lamp projector, AirTag insole holder, chicken shredder, portable ultrasonic cleaner, stackable fridge bins, handheld vacuum sealer, drain hair catcher, car windshield sun umbrella. Tool di recon citato: WatchCount.com (ranking per watch-count, 403-walled).

## STATO
- ✅ **6 importati come DRAFT** (drafts 13→19), titolo+descrizione applicati/verificati.
- ⛔ **Publish = GO + sbloccare account eBay** (il publish è bloccato a livello account, vedi cockpit). Prima del publish: confermare costo reale AutoDS di ogni SKU.
- Comandi/asset: `listings/copy_2026-06-20_new/*.html`. Fonte workflow: wf_ddc8dc83-231.

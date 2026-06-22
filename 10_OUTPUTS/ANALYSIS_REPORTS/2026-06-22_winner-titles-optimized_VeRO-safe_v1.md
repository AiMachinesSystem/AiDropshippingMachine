---
machine: "eBay / AutoDS Dropshipping Machine"
type: listing_optimization
date: 2026-06-22
created_real: 2026-06-22
status: DRAFT (apply = GO; eBay new-listing restriction active 2026-06-20)
source: 90_CACHE/fetches/autods/audit_2026-06-22_044324/_products_list.json
---

# Winner Titles — Optimized & VeRO-safe (13 proven sellers)

**Scope:** the 13 listings with ≥1 lifetime sale (the only proven-demand SKUs). All new titles **≤80 char (counted, not eyeballed)**, keyword-front-loaded, generic. **Draft only** — applying = GO gate; eBay also blocks new/edited listings since 2026-06-20.

## Optimized titles
| eBay ID | sold | new title (chars) | fix |
|---|---:|---|---|
| 406382172143 | 6 | Pool Fountain Jet J-Style Replacement Fitting for Inground Pools Deck Spray (75) | keyword-front |
| 406174683287 | 5 | Dog Water Ramp for Boats Pools Holds 200lb Pet Swim Ladder with Pump 2025 (73) | — |
| 406103214230 | 5 | Ham Maker Stainless Steel Meat Press with Thermometer 20 Cooking Bags Deli (74) | drop `\|` pipes |
| 406247019968 | 4 | 2 Pack Pet Grooming Loops Nylon Restraint Noose Dogs Cats Hands-Free Tether (75) | **fix corrupted `�` chars** + cut 115→75 |
| 406391915026 | 3 | 8.8in PC Display Screen ARGB USB Temp Monitor Secondary Mini Case Screen (72) | **DE-BRAND "Lian Li"/"US88" (VeRO)** |
| 406169382444 | 3 | Reusable Dryer Balls Set of 2 Laundry Fabric Softener Spiky White Eco Wool (74) | dropped "Hedgehog" to be safe |
| 406103169166 | 3 | Homemade Ham Maker Deli Meat Press Stainless Steel Thermometer Cooking Bags (75) | drop `\|` pipes |
| 407007332522 | 1 | Beginner Crochet Kit Snail Amigurumi Plush DIY Starter Set with Video Guide (75) | **REMOVE "Dora" (trademark)** |
| 406382169074 | 1 | In-Line Automatic Chlorine Feeder 9lb Capacity Pool Chlorinator Inground (72) | **DE-BRAND "Hydrotools 8750" (VeRO)** |
| 406174659709 | 1 | Dog Life Jacket Ripstop American Flag Swim Vest High Buoyancy Small Dogs (72) | **cut 166→72**, drop "Shark Puppy" |
| 406149695098 | 1 | Solar Stock Tank Pool Cover 8ft Heavy Duty All Weather Wire Rope and Winch (74) | — |
| 406149693790 | 1 | 8ft Round Stock Tank Pool Cover Full Coverage Wire Rope Winch Blue Solar (72) | — |
| 406092460312 | 1 | Roller Idler Pulley Wheel 6x30x30mm with 626RS Bearing Black 1pc (64) | **fix corrupted `�` chars** |

## VeRO / integrity flags fixed (the load-bearing ones)
- **3 brand/trademark removals:** Lian Li (+ model US88), Hydrotools 8750, Dora → all dominant suspension triggers; generic versions still rank on the same keywords.
- **2 corrupted-char titles** (`�` from bad em-dash encoding) cleaned — these look broken to buyers and hurt CTR.
- **1 title 166→72 char** (Dog Life Jacket was truncated mid-word on eBay → lost search weight).
- **Pipes `|`** removed from 2 Ham Maker titles (eBay treats them as noise, wastes char budget).

## Not done here (next, separate)
- **Descriptions:** rule = rewrite ALL 13 fresh (never keep scraped — brand/claims/retailer fingerprints). Needs the scraped bodies pulled (read-only) → next pass.
- **Apply:** `apply_titles*.py` exists in the playwright integration, but apply = GO **and** eBay restriction (06-20) blocks it. Queued for owner unblock.

## Measurement
- KPI: of the 13, the 3 VeRO-flagged (Lian Li, Hydrotools, Dora) carried real suspension risk while selling — de-branding removes risk with **zero** keyword loss (same search terms retained). Success = applied titles persist + no VeRO notice; tracked on next audit.

---
tags: [listing, copy]
type: reference
created_real: 2026-06-17
description: "Copy pronta per 3 nuovi draft importati il 2026-06-17: titolo eBay <=80 char (verificato) + descrizione VeRO-safe riscritta. La descrizione rich-editor AutoDS non e automatizzabile (muro noto) -> incolla manuale nel tab Description di ogni draft."
---

# Copy 3 draft — 2026-06-17

> Regola listing: titolo <=80 char; descrizione SEMPRE riscritta (mai quella scrapata), VeRO-safe.
> Ogni claim e supportabile dalle specifiche generiche del prodotto. Nessun brand/IP nei titoli.
> Titolo = applicato via Playwright (apply_*_title). Descrizione = incolla manuale (rich-editor = muro noto).

---

## 1 · Slow Feeder Dog Bowl  (ASIN B0CJXNXMMY)

**TITOLO (80/80):**
`Slow Feeder Dog Bowl Silicone Puzzle Mat Anti-Choke Non-Slip Suction Cup Pet Cat`

**DESCRIZIONE (VeRO-safe):**
Slow Feeder Dog Bowl — Healthier Mealtimes, Less Mess

Help your pet eat at a calmer pace. The raised silicone maze turns fast gulping into a fun puzzle, which can help reduce bloating, choking, and vomiting caused by eating too quickly.

- Food-grade silicone, soft on gums and easy to clean
- Suction cups on the base keep the bowl in place — no sliding, no spills
- Maze design slows eating and adds light mental enrichment at every meal
- Suitable for small to medium dogs and cats; works with dry, wet, or raw food
- Dishwasher friendly — rinse or place on the top rack

Care: hand wash or dishwasher (top rack). Press firmly onto a clean, flat surface for the suction cups to grip.

What you get: 1 x Slow Feeder Bowl. Color/pattern may vary by availability.

---

## 2 · Coffee Pod Holder Countertop  (ASIN B0CZ6DX9YJ)

**TITOLO (79/80):**
`Coffee Pod Holder Organizer Countertop Storage Basket Wood Base Kitchen Display`

**DESCRIZIONE (VeRO-safe):**
Coffee Pod Holder — Tidy Counter, Coffee Within Reach

Keep your coffee station neat with a compact countertop holder that stores your pods upright and ready to grab. The sturdy metal frame and solid wood base add a clean, modern look to any kitchen, bar, or office desk.

- Holds standard single-serve coffee pods in an easy-access basket
- Solid wood base + powder-coated metal frame for a stable, premium feel
- Space-saving footprint fits on a counter, shelf, or breakroom table
- Open design lets you see and reach every pod at a glance
- Simple to assemble; wipe clean with a dry cloth

Note: compatible with common single-serve pods. Pods and machine shown are not included.

What you get: 1 x Coffee Pod Holder.

---

## 3 · Portable Neck Fan  (ASIN B09PCSR9SX)

**TITOLO (79/80):**
`Portable Neck Fan Bladeless Hands Free 360 Cooling Rechargeable 4000mAh 3-Speed`

**DESCRIZIONE (VeRO-safe):**
Hands-Free Neck Fan — Cool Air Wherever You Go

Stay comfortable on hot days without holding anything. This wearable neck fan rests around your neck and pushes a steady stream of air, leaving your hands completely free for work, travel, walking, or chores.

- Bladeless, hands-free design — safe around hair, comfortable for long wear
- 360 degree airflow cools the neck and face from multiple outlets
- 3 adjustable speeds to match a breeze or a stronger blast
- Rechargeable 4000mAh battery with USB charging — no disposable batteries
- Lightweight and quiet enough for the office, commute, or outdoors

Use: charge fully before first use. Choose your speed with the on-device button.

What you get: 1 x Portable Neck Fan + USB charging cable. Color may vary by availability.

---

## STATO APPLICAZIONE (chiuso 2026-06-17 21:xx)
- [x] Import draft (tutti e 3) — import_drafts.py --confirm → drafts 16→19
- [x] Titoli applicati ai draft (apply_titles_3.py, Save per card) → PERSISTED ×3
- [x] Descrizioni applicate via CKEditor API su pagina dedicata (apply_desc_ckeditor_3.py) → PERSISTED ×3
      MURO CADUTO: la descrizione È automatizzabile via /upload/<id> + window.CKEDITOR.instances[0].setData(html)
- [ ] Publish = GO separato (NON in questo scope)

ID pagine dedicate: slow feeder 6a33452c55f86e413f55b55d · coffee pod 6a334546c81e314488748fef · neck fan 6a334560d49bc5e7ee527b13
Source ASIN: B0CJXNXMMY · B0CZ6DX9YJ · B09PCSR9SX (Amazon — drafts only; publish da Amazon-source = rischio policy eBay, valutare alla pubblicazione)

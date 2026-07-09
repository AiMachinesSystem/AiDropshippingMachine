#!/usr/bin/env python3
"""
_seo_titles_run.py — Pull ALL active AutoDS products via the list API, generate
SEO-optimized titles ≤79 chars (no brand prefix, word-boundary truncation), apply
each via the /products/<hex_id>&2 edit page.  Single playwright session — no separate
audit step needed.

GO: owner 2026-07-08 "rifai tutti i titoli dei prodotti attivi ottimizzati seo max 79".
Safety: title field only + Save (never "Save & Import"), verify each write.
"""
import os, re, sys, json, collections
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE   = os.path.dirname(os.path.abspath(__file__))
STATE  = os.path.join(HERE, "storage_state.json")
BASE   = "https://platform.autods.com"

# ── SEO title generator ─────────────────────────────────────────────────────
BRAND_RE = re.compile(r"^[A-Z][A-Z0-9\-&.']{2,}$")

def make_seo(raw):
    """Strip brand prefix, truncate at word boundary ≤79 chars."""
    t = (raw or "").strip()
    words = t.split()
    # strip 1st word if all-caps brand (FUNPENY, RUNBOX, AUGO…)
    if words and BRAND_RE.match(words[0]):
        words = words[1:]
        if words and words[0] == "-":
            words = words[1:]
    # strip 2nd brand word if still all-caps (e.g. "SERMAN BRANDS -")
    if len(words) >= 2 and BRAND_RE.match(words[0]) and words[1] in ("-", "&"):
        words = words[1:]
    t2 = " ".join(words).strip()
    if len(t2) <= 79:
        return t2
    cut = t2[:79].rfind(" ")
    return t2[:cut].strip() if cut > 30 else t2[:79]

def needs_edit(old, new):
    return old.strip() != new.strip() and len(new.strip()) >= 10

# ── Pull product list via captured API ──────────────────────────────────────
from playwright.sync_api import sync_playwright

ts  = datetime.now().strftime("%Y-%m-%d_%H%M%S")
log = os.path.join(HERE, f"_seo_titles_run_{ts}.log")
print(f"SEO title run: {ts}")

products = []   # list of {id, title}

with sync_playwright() as p:
    b   = p.chromium.launch(headless=True)
    ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
    pg  = ctx.new_page()

    # ── Step 1: navigate /products page, capture live-product API responses ─
    list_items = {}   # dedup by hex id

    def on_resp(resp):
        try:
            u = resp.url
            if "autods.com" not in u:
                return
            ct = (resp.headers or {}).get("content-type", "")
            if "application/json" not in ct:
                return
            if "/products/" in u and "/list" in u:
                data = resp.json()
                rows = data.get("results") or data.get("items") or (data if isinstance(data, list) else [])
                for it in (rows or []):
                    k = it.get("id") or it.get("_id") or ""
                    if k:
                        list_items[k] = it
        except Exception:
            pass

    pg.on("response", on_resp)

    pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(5000)
    # dismiss upsell if redirected
    if "offer" in pg.url or "upgrade" in pg.url:
        for mk in [lambda: pg.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                   lambda: pg.get_by_text(re.compile(r"No Thanks", re.I))]:
            try: mk().first.click(timeout=5000); break
            except Exception: pass
        pg.wait_for_timeout(2500)
        pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(5000)

    # paginate through all pages (same logic as audit_listings.py)
    for _ in range(20):
        nxt = pg.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
        if nxt.count() == 0:
            break
        try:
            nxt.first.scroll_into_view_if_needed(timeout=3000)
            nxt.first.click(timeout=4000)
        except Exception:
            break
        pg.wait_for_timeout(2400)

    print(f"Products fetched: {len(list_items)}")

    for k, it in list_items.items():
        title = (it.get("title") or "").strip()
        if k and title:
            products.append({"id": k, "title": title})

    # ── Step 2: build work list ─────────────────────────────────────────────
    targets = []
    for pr in products:
        seo = make_seo(pr["title"])
        if needs_edit(pr["title"], seo):
            targets.append((pr["id"], pr["title"], seo))

    print(f"Titles to update: {len(targets)}/{len(products)}")
    if not targets:
        print("All titles already clean — done."); b.close(); sys.exit(0)

    # preview first 10
    for hex_id, old, new in targets[:10]:
        print(f"  [{len(old):2d}→{len(new):2d}] {old[:55]}")
        print(f"           → {new[:70]}")

    # ── Step 3: apply titles ────────────────────────────────────────────────
    results = []
    for i, (hex_id, old_title, new_title) in enumerate(targets):
        assert len(new_title) <= 79, f"OVER79 ({len(new_title)}): {new_title}"
        url = BASE + "/products/" + hex_id + "&2"
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(7000)

            ti = pg.locator("input[placeholder='Title']").first
            try:
                cur = ti.input_value(timeout=5000)
            except Exception:
                print(f"[{i+1:3d}/{len(targets)}] ABORT no-input | {hex_id[:24]}")
                results.append((hex_id, "ABORT"))
                continue

            if cur.strip() == new_title:
                print(f"[{i+1:3d}/{len(targets)}] ALREADY | {new_title[:60]}")
                results.append((hex_id, "ALREADY"))
                continue

            ti.click(); ti.press("Control+A"); ti.press("Delete")
            ti.fill(new_title); pg.wait_for_timeout(700)

            saved = False
            for mk in [
                lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)),
                lambda: pg.get_by_text(re.compile(r"^\s*Save\s*$", re.I)),
            ]:
                try:
                    mk().first.click(timeout=5000); saved = True; break
                except Exception:
                    pass

            pg.wait_for_timeout(4500)
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(6000)
            ok = pg.locator("input[placeholder='Title']").first.input_value(timeout=5000).strip() == new_title
            status = "OK" if ok else "UNVER"
            print(f"[{i+1:3d}/{len(targets)}] {'  OK' if ok else 'FAIL'} | {len(new_title):2d}ch | {new_title[:60]}")
            results.append((hex_id, status))

        except Exception as e:
            print(f"[{i+1:3d}/{len(targets)}] ERR | {hex_id[:24]} | {type(e).__name__}: {str(e)[:60]}")
            results.append((hex_id, "ERR"))

    b.close()

# ── Summary ──────────────────────────────────────────────────────────────────
c = collections.Counter(s for _, s in results)
print(f"\n=== SEO TITLE RUN COMPLETE ===")
print(f"Total processed : {len(results)}")
print(f"Updated (OK)    : {c['OK']}")
print(f"Already clean   : {c['ALREADY']}")
print(f"Unverified      : {c['UNVER']}")
print(f"Errors/Aborts   : {c['ERR'] + c['ABORT']}")
print(f"RUN_RESULT seo_ok={c['OK']} already={c['ALREADY']} fail={c['UNVER']+c['ERR']+c['ABORT']}")

with open(log, "w", encoding="utf-8") as fh:
    fh.write(f"SEO run {ts}\n")
    for hex_id, st in results:
        fh.write(f"{hex_id}\t{st}\n")
print(f"Log: {log}")

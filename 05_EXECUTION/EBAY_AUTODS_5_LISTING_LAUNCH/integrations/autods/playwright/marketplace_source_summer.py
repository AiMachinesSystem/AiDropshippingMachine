#!/usr/bin/env python3
"""READ-ONLY summer-outdoor/backyard sourcing (buffer for the pool+summer batch, owner GO 2026-06-24).
Pool-adjacent seasonal: solar/outdoor lights, patio, splash/water toys, outdoor games. Cracked filter API
+ US-warehouse. Output raw cache for the combined candidate extraction. SAFETY: read-only.
Usage: marketplace_source_summer.py [LO] [HI]"""
import os, re, sys, json
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"; API = "https://gw.autods.com/marketplace/api/products/"
PAGES, LIMIT, MIN_RATING, MIN_RC = 6, 50, 4.2, 150
CLUSTERS = [("solar lights outdoor", "search", "solar lights outdoor"), ("solar lantern", "search", "solar lantern"),
            ("outdoor string lights", "search", "outdoor string lights"), ("solar pathway lights", "search", "solar pathway lights"),
            ("patio furniture cover", "search", "patio furniture cover"), ("grill cover", "search", "grill cover"),
            ("splash pad", "search", "splash pad"), ("water toys kids", "search", "water toys kids"),
            ("sprinkler kids", "search", "sprinkler for kids"), ("outdoor games", "search", "outdoor yard games"),
            ("garden solar stake", "search", "garden solar stake lights"), ("inflatable lounger", "search", "inflatable lounger"),
            ("beach ball", "search", "beach ball"), ("water gun", "search", "water gun"),
            ("outdoor cushion", "search", "outdoor seat cushion"), ("hammock", "search", "outdoor hammock"),
            ("flamingo float", "search", "inflatable ride on"), ("solar string", "search", "solar fairy lights")]
PROJECTION = {"title": {}, "images": {}, "supplier_name": {}, "site_name": {}, "id_on_site": {},
              "product_details": {}, "region": {}, "private_supplier": {}, "is_winning_product": {},
              "is_free_winning_product": {}, "categories": {}}
def find_root(s):
    c = os.path.abspath(s)
    while c != os.path.dirname(c):
        if os.path.isdir(os.path.join(c, "10_OUTPUTS")): return c
        c = os.path.dirname(c)
    return s
def body(kind, value, off, lo, hi):
    f = [{"name": "rating", "value": str(MIN_RATING), "value_type": "float", "op": ">"},
         {"name": "rating_count", "value": str(MIN_RC), "value_type": "integer", "op": ">"},
         {"name": "variations.variation_details.price", "value": "%s,%s" % (lo, hi), "value_type": "float", "op": "between"}]
    f.append({"name": "search_query", "value_type": "string", "op": "search", "value": value})
    return {"projection": PROJECTION, "order_by": {"direction": "desc", "name": "spv_param"},
            "condition": "and", "limit": LIMIT, "offset": off, "filters": f}
def main():
    lo = sys.argv[1] if len(sys.argv) > 1 else "20"; hi = sys.argv[2] if len(sys.argv) > 2 else "120"
    from playwright.sync_api import sync_playwright
    root = find_root(HERE); ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_source_summer_" + ts); os.makedirs(cache, exist_ok=True)
    auth = {}; prods = {}
    def on_req(r):
        if not auth and r.url.startswith(API) and r.method == "POST":
            for k, v in (r.headers or {}).items():
                if k.lower() in ("authorization", "content-type", "accept") or k.lower().startswith("x-"): auth[k] = v
    print("SUMMER pull $%s-%s | clusters %d" % (lo, hi, len(CLUSTERS)))
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000}); pg = ctx.new_page(); pg.on("request", on_req)
        pg.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        for label, kind, value in CLUSTERS:
            got = 0
            for i in range(PAGES):
                try:
                    r = ctx.request.post(API, headers=auth, data=json.dumps(body(kind, value, i * LIMIT, lo, hi)), timeout=45000)
                    if r.status != 200: break
                    items = r.json().get("results") or []
                except Exception: break
                if not items: break
                for it in items:
                    if isinstance(it, dict) and it.get("_id"): it["_cluster"] = label; prods.setdefault(it["_id"], it)
                got += len(items)
                if len(items) < LIMIT: break
            print("  [%s] ~%d" % (label[:24], got))
        b.close()
    json.dump(list(prods.values()), open(os.path.join(cache, "_raw_products.json"), "w", encoding="utf-8"), ensure_ascii=False)
    us = sum(1 for it in prods.values() if (it.get("product_details") or {}).get("min_price_warehouse") == "US")
    print("-"*50); print("unique:", len(prods), "| US-WH:", us, "| cache:", cache)
if __name__ == "__main__": sys.exit(main())

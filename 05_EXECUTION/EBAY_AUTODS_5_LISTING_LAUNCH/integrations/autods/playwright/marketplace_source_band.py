#!/usr/bin/env python3
"""
marketplace_source_band.py — READ-ONLY targeted pull in a PRICE BAND (default $40-75) for the profitable
bands identified in the price-band study. Uses the cracked filter API with a server-side price filter
(variations.variation_details.price between LO,HI) across the proven niches (categories + search terms),
deeper pagination. Same auth-capture+replay + US-warehouse client filter as marketplace_source.py.
SAFETY: read-only research (GO_AUTODS_READ_SESSION). Output: raw cache for rank_us_source.py.
Usage: marketplace_source_band.py [LO] [HI]
"""
import os, re, sys, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
API = "https://gw.autods.com/marketplace/api/products/"
PAGES, LIMIT = 6, 50
MIN_RATING, MIN_RC = 4.3, 200

CLUSTERS = [  # (label, kind, value) ; kind in {cat, search}
    ("Kitchen Utensils & Gadgets", "cat", "6169735594f2b1708dccdbbd"),
    ("Cookware", "cat", "6169735594f2b1708dccdb84"),
    ("Bakeware", "cat", "6169735594f2b1708dccdb92"),
    ("Dining & Entertaining", "cat", "6169735594f2b1708dccdba5"),
    ("Pools hot tubs supplies", "cat", "6169735594f2b1708dccdcbe"),
    ("Grills & Outdoor cooking", "cat", "6169735594f2b1708dccdce9"),
    ("Home cleaning", "cat", "6169735694f2b1708dccdcfd"),
    ("Storage & Organization", "cat", "6169735694f2b1708dccdd4f"),
    ("search pool", "search", "pool"), ("search pool cover", "search", "pool cover"),
    ("search cast iron", "search", "cast iron"), ("search dutch oven", "search", "dutch oven"),
    ("search glass storage", "search", "glass food storage"), ("search laundry", "search", "laundry hamper"),
    ("search cookware set", "search", "cookware set"), ("search canister", "search", "kitchen canister"),
    ("search beach bag", "search", "beach bag"), ("search spice rack", "search", "spice rack organizer"),
]
PROJECTION = {"title": {}, "images": {}, "supplier_name": {}, "site_name": {}, "id_on_site": {},
              "product_details": {}, "region": {}, "private_supplier": {}, "is_winning_product": {},
              "is_free_winning_product": {}, "categories": {}}


def find_root(s):
    c = os.path.abspath(s)
    while c != os.path.dirname(c):
        if os.path.isdir(os.path.join(c, "10_OUTPUTS")):
            return c
        c = os.path.dirname(c)
    return s


def body(kind, value, off, lo, hi):
    f = [{"name": "rating", "value": str(MIN_RATING), "value_type": "float", "op": ">"},
         {"name": "rating_count", "value": str(MIN_RC), "value_type": "integer", "op": ">"},
         {"name": "variations.variation_details.price", "value": "%s,%s" % (lo, hi), "value_type": "float", "op": "between"}]
    if kind == "cat":
        f.append({"name": "categories.autods_category_id.$id", "value_type": "objectId", "op": "=", "value": value})
    else:
        f.append({"name": "search_query", "value_type": "string", "op": "search", "value": value})
    return {"projection": PROJECTION, "order_by": {"direction": "desc", "name": "spv_param"},
            "condition": "and", "limit": LIMIT, "offset": off, "filters": f}


def main():
    lo = sys.argv[1] if len(sys.argv) > 1 else "40"
    hi = sys.argv[2] if len(sys.argv) > 2 else "75"
    from playwright.sync_api import sync_playwright
    root = find_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_source_band_" + ts)
    os.makedirs(cache, exist_ok=True)
    auth = {}
    prods = {}

    def on_req(r):
        if not auth and r.url.startswith(API) and r.method == "POST":
            for k, v in (r.headers or {}).items():
                if k.lower() in ("authorization", "content-type", "accept") or k.lower().startswith("x-"):
                    auth[k] = v

    print("BAND pull $%s-%s | clusters %d | pages %d" % (lo, hi, len(CLUSTERS), PAGES))
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        pg.on("request", on_req)
        pg.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(7000)
        for label, kind, value in CLUSTERS:
            got = 0
            for i in range(PAGES):
                try:
                    r = ctx.request.post(API, headers=auth, data=json.dumps(body(kind, value, i * LIMIT, lo, hi)), timeout=45000)
                    if r.status != 200:
                        break
                    items = r.json().get("results") or []
                except Exception:
                    break
                if not items:
                    break
                for it in items:
                    if isinstance(it, dict) and it.get("_id"):
                        it["_cluster"] = label
                        prods.setdefault(it["_id"], it)
                got += len(items)
                if len(items) < LIMIT:
                    break
            print("  [%s] ~%d" % (label[:34], got))
        b.close()
    json.dump(list(prods.values()), open(os.path.join(cache, "_raw_products.json"), "w", encoding="utf-8"), ensure_ascii=False)
    us = sum(1 for it in prods.values() if (it.get("product_details") or {}).get("min_price_warehouse") == "US")
    print("-" * 60)
    print("unique:", len(prods), "| US-warehouse:", us, "| cache:", cache)
    return 0


if __name__ == "__main__":
    sys.exit(main())

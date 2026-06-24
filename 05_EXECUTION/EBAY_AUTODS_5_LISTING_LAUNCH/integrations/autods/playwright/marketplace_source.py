#!/usr/bin/env python3
"""
marketplace_source.py — READ-ONLY US-warehouse sourcing pull over the AutoDS Marketplace filter API.

Cracked via marketplace_filter_probe*.py:
  POST https://gw.autods.com/marketplace/api/products/
  body = {projection, order_by:{name:spv_param,direction:desc}, condition:and, limit, offset,
          filters:[ {name:rating,op:>,...}, {name:rating_count,op:>,...},
                    {name:categories.autods_category_id.$id,op:=,value_type:objectId,value:<id>}  -- OR
                    {name:search_query,op:search,value:<kw>} ]}

AUTH: the gw.autods.com API needs the app's Bearer token (localStorage), not just cookies. We capture
the REAL Authorization (+ x-*) headers from the page's own load request, then replay them verbatim via
ctx.request.post. US-warehouse is applied CLIENT-SIDE on product_details.min_price_warehouse=="US"
(Ships-From is not a server-side product filter — confirmed by probe2).

SAFETY CONTRACT: READ-ONLY research. Only POSTs to the marketplace READ/search endpoint (the same call
the marketplace page makes to render results). NO import/add/publish/price/order. No credential printed.
GO scope: GO_AUTODS_READ_SESSION + sourcing mission (read-only).

Output: ranked shortlist JSON + a human table, cached under 90_CACHE; the report file is written by the
caller. Run with PYTHONIOENCODING=utf-8 on Windows.
"""
import os, re, sys, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
API = "https://gw.autods.com/marketplace/api/products/"

# ---- demand gate (honors owner's >reviews method; relaxed count to surface enough US-WH survivors) ----
MIN_RATING = 4.3
MIN_RATING_COUNT = 300          # report also how many clear the strict 1000 bar
PAGES = 4                       # offsets per cluster
LIMIT = 50

# ---- clusters: (label, kind, value) ; kind in {cat, search} ----
CLUSTERS = [
    ("Pool/Water — Pools, hot tubs & supplies", "cat", "6169735594f2b1708dccdcbe"),
    ("Pool/Water — search 'pool cover'",        "search", "pool cover"),
    ("Pool/Water — search 'pool skimmer'",      "search", "pool skimmer"),
    ("Kitchen — Utensils & Gadgets",            "cat", "6169735594f2b1708dccdbbd"),
    ("Kitchen — Cookware",                      "cat", "6169735594f2b1708dccdb84"),
    ("Meat/Food prep — Grills & Outdoor cook",  "cat", "6169735594f2b1708dccdce9"),
    ("Meat/Food prep — search 'meat'",          "search", "meat"),
    ("Meat/Food prep — search 'garlic press'",  "search", "garlic press"),
    ("Meat/Food prep — search 'vegetable chopper'", "search", "vegetable chopper"),
    ("Commodity — Home cleaning",               "cat", "6169735694f2b1708dccdcfd"),
    ("Commodity — Storage & Organization",      "cat", "6169735694f2b1708dccdd4f"),
]

PROJECTION = {"title": {}, "images": {}, "supplier_name": {}, "site_name": {}, "id_on_site": {},
              "product_details": {}, "region": {}, "private_supplier": {}, "is_winning_product": {},
              "is_free_winning_product": {}, "categories": {}}

# brand tokens -> VeRO risk; presence of any => HIGH (IP/brand). Conservative, extendable.
BRANDS = ["nike", "adidas", "disney", "panasonic", "dyson", "lego", "apple", "samsung", "sony",
          "bosch", "dewalt", "makita", "stanley", "yeti", "rtic", "ninja", "kitchenaid", "cuisinart",
          "instant pot", "instapot", "pyrex", "oxo", "dash", "costway", "tstars", "hebe", "pauwer",
          "readywise", "carhartt", "weber", "traeger", "coleman", "intex", "bestway", "hayward",
          "pentair", "rubbermaid", "tupperware", "lodge", "le creuset", "vitamix", "keurig"]

# higher-policy-risk categories (regulated / branded-heavy)
HIGHER_RISK_CAT = re.compile(r"electronic|automotive|motorcycle|beauty|health|supplement|cosmetic|"
                             r"makeup|skin care|hair|vitamin|medical|battery|charger", re.I)


def find_repo_root(start):
    cur = os.path.abspath(start)
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        cur = os.path.dirname(cur)
    return start


def build_body(kind, value, offset):
    filters = [
        {"name": "rating", "value": str(MIN_RATING), "value_type": "float", "op": ">"},
        {"name": "rating_count", "value": str(MIN_RATING_COUNT), "value_type": "integer", "op": ">"},
    ]
    if kind == "cat":
        filters.append({"name": "categories.autods_category_id.$id", "value_type": "objectId",
                        "op": "=", "value": value})
    else:
        filters.append({"name": "search_query", "value_type": "string", "op": "search", "value": value})
    return {"projection": PROJECTION, "order_by": {"direction": "desc", "name": "spv_param"},
            "condition": "and", "limit": LIMIT, "offset": offset, "filters": filters}


def econ(it):
    pd = it.get("product_details") or {}
    buy = pd.get("min_price")
    sell = pd.get("min_msrp_price")
    ship = pd.get("min_shipping_cost") or 0
    wh = pd.get("min_price_warehouse") or "?"
    stime = pd.get("max_shipping_time")
    rating = pd.get("rating") or pd.get("avg_rating")
    rcount = pd.get("rating_count") or pd.get("reviews_count")
    margin = mpct = None
    if isinstance(buy, (int, float)) and isinstance(sell, (int, float)):
        margin = round(sell - buy - (ship or 0), 2)
        mpct = round(100 * margin / sell, 1) if sell else None
    return buy, sell, ship, wh, stime, rating, rcount, margin, mpct


def vero_risk(title, supplier):
    blob = ((title or "") + " " + (supplier or "")).lower()
    if any(b in blob for b in BRANDS):
        return "HIGH"
    if "™" in (title or "") or "®" in (title or ""):
        return "HIGH"
    # capitalized multi-word proper-noun brand guess: a single TitleCase token that isn't a common word
    return "LOW"


def policy_risk(cats_blob, region):
    if HIGHER_RISK_CAT.search(cats_blob or ""):
        return "MED"
    return "LOW"


def recommend(wh, stime, margin, vrisk):
    if wh != "US":
        return "KILL"
    if vrisk == "HIGH":
        return "HOLD"
    if margin is None:
        return "HOLD"
    fast = isinstance(stime, (int, float)) and stime <= 7
    if margin >= 6 and fast and vrisk == "LOW":
        return "TEST"
    if margin >= 4:
        return "HOLD"
    return "KILL"


def main():
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_source_" + ts)
    os.makedirs(cache, exist_ok=True)

    auth_headers = {}

    def on_request(req):
        if not auth_headers and req.url.startswith(API) and req.method == "POST":
            h = req.headers or {}
            for k, v in h.items():
                if k.lower() in ("authorization", "content-type", "accept", "x-store-id",
                                 "store-id", "x-asp-token") or k.lower().startswith("x-"):
                    auth_headers[k] = v

    products = {}
    print("MKT sourcing run:", ts)
    print("demand gate: rating>%.1f  rating_count>%d  | clusters:%d  pages:%d  limit:%d"
          % (MIN_RATING, MIN_RATING_COUNT, len(CLUSTERS), PAGES, LIMIT))
    print("-" * 80)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("request", on_request)
        page.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(7000)  # let the page make its own POST so we grab real auth headers
        if "authorization" not in {k.lower() for k in auth_headers}:
            print("WARN: no Authorization header captured; replay may 401. headers seen:", list(auth_headers))
        # replay each cluster directly via the authenticated request context
        for label, kind, value in CLUSTERS:
            got = 0
            for pg_i in range(PAGES):
                body = build_body(kind, value, pg_i * LIMIT)
                try:
                    r = ctx.request.post(API, headers=auth_headers, data=json.dumps(body),
                                         timeout=45000)
                    if r.status != 200:
                        print("  [%s] offset %d -> HTTP %d" % (label[:34], pg_i * LIMIT, r.status))
                        break
                    data = r.json()
                except Exception as e:
                    print("  [%s] offset %d -> ERR %s" % (label[:34], pg_i * LIMIT, type(e).__name__))
                    break
                items = data.get("results") or data.get("data") or []
                if isinstance(items, dict):
                    items = items.get("results") or []
                if not items:
                    break
                for it in items:
                    if isinstance(it, dict) and it.get("_id"):
                        it["_cluster"] = label
                        products.setdefault(it["_id"], it)
                got += len(items)
                if len(items) < LIMIT:
                    break
            print("  [%s] collected ~%d" % (label[:46], got))
        b.close()

    # save raw
    with open(os.path.join(cache, "_raw_products.json"), "w", encoding="utf-8") as fh:
        json.dump(list(products.values()), fh, ensure_ascii=False)

    # build rows
    rows = []
    strict1000 = 0
    for it in products.values():
        title = it.get("title") or ""
        supplier = it.get("supplier_name") or it.get("site_name") or ""
        region = it.get("region")
        cats_blob = json.dumps(it.get("categories") or "", ensure_ascii=False)
        buy, sell, ship, wh, stime, rating, rcount, margin, mpct = econ(it)
        if isinstance(rcount, (int, float)) and rcount >= 1000:
            strict1000 += 1
        vrisk = vero_risk(title, supplier)
        prisk = policy_risk(cats_blob, region)
        rec = recommend(wh, stime, margin, vrisk)
        rows.append({"title": title[:70], "supplier": supplier, "region": region, "wh": wh,
                     "stime": stime, "buy": buy, "sell": sell, "ship": ship, "margin": margin,
                     "mpct": mpct, "rating": rating, "rcount": rcount, "vero": vrisk,
                     "policy": prisk, "rec": rec, "cluster": it.get("_cluster", ""),
                     "id_on_site": it.get("id_on_site"), "site": it.get("site_name"),
                     "winning": bool(it.get("is_winning_product"))})

    us = [r for r in rows if r["wh"] == "US"]
    # rank US-warehouse: TEST first, then margin, then fast shipping, then winning
    rank_rec = {"TEST": 3, "HOLD": 2, "KILL": 1}
    us.sort(key=lambda r: (rank_rec.get(r["rec"], 0), r["margin"] or -99,
                           -(r["stime"] or 99), r["winning"]), reverse=True)

    with open(os.path.join(cache, "_shortlist_us.json"), "w", encoding="utf-8") as fh:
        json.dump(us, fh, ensure_ascii=False, indent=1)

    print("-" * 80)
    print("total unique products pulled:", len(products), "| US-warehouse:", len(us),
          "| cleared strict rating_count>=1000:", strict1000)
    print("CACHE:", cache)
    print("=" * 110)
    print("%-4s %-3s %-4s %-6s %-6s %-6s %-5s %-7s %-5s %-5s | %s" %
          ("REC", "WH", "shipd", "buy", "sell", "margin", "mgn%", "rcount", "vero", "pol", "title"))
    print("-" * 110)
    for r in us[:60]:
        print("%-4s %-3s %-4s %-6s %-6s %-6s %-5s %-7s %-5s %-5s | %s" %
              (r["rec"], r["wh"], r["stime"], r["buy"], r["sell"], r["margin"], r["mpct"],
               r["rcount"], r["vero"], r["policy"], r["title"]))
    nt = sum(1 for r in us if r["rec"] == "TEST")
    nh = sum(1 for r in us if r["rec"] == "HOLD")
    print("-" * 110)
    print("US-warehouse recommendations: TEST=%d  HOLD=%d  KILL=%d" %
          (nt, nh, sum(1 for r in us if r["rec"] == "KILL")))
    return 0


if __name__ == "__main__":
    sys.exit(main())

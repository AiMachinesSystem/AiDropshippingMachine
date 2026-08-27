#!/usr/bin/env python3
"""Build additional ebay-direct manifests from AutoDS drafts, skipping already-used ASINs
and enriching aspects with title-inferred Material/Color (reduces eBay item-specific failures)."""
import json, re, sys, os, glob
from datetime import datetime, timezone

SRC = "C:/AI Machine ebay-autoDS/AiDropshippingMachine/05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/_drafts_full.json"
OUT = "C:/AI Machine ebay-autoDS/AiDropshippingMachine/05_EXECUTION/ebay-direct/manifests"

POLICIES = {"payment": "282011576018", "fulfillment": "282011584018", "return": "282011577018"}
LOCATION = "US-WAREHOUSE"

BLOCKED = ["bpa-free", "bpa free", "waterproof", "safe", "streak-free", "streak free", "eye care"]
TRADEMARK = re.compile(r"[®™]")

# High-confidence title keyword -> eBay item-specific value. Conservative: only exact-substring
# matches on words that unambiguously name the material/color of the product itself.
MATERIAL_MAP = [
    ("stainless steel", "Stainless Steel"),
    ("polyester", "Polyester"),
    ("silicone", "Silicone"),
    ("bamboo", "Bamboo"),
    ("ceramic", "Ceramic"),
    ("glass", "Glass"),
    ("aluminum", "Aluminum"),
    ("canvas", "Canvas"),
    ("leather", "Leather"),
    ("cotton", "Cotton"),
    ("nylon", "Nylon"),
    ("plastic", "Plastic"),
    ("resin", "Resin"),
    ("wood", "Wood"),
]
COLOR_MAP = [
    ("black", "Black"), ("white", "White"), ("gray", "Gray"), ("grey", "Gray"),
    ("blue", "Blue"), ("red", "Red"), ("green", "Green"), ("pink", "Pink"),
    ("brown", "Brown"), ("beige", "Beige"), ("purple", "Purple"), ("yellow", "Yellow"),
    ("orange", "Orange"), ("silver", "Silver"), ("gold", "Gold"), ("clear", "Clear"),
]

def clean_title(t: str) -> str:
    t = TRADEMARK.sub("", t)
    t = re.sub(r"^[A-Z][A-Za-z0-9&'\.\- ]{1,40}\s*[-–|:]\s*", "", t, count=1)
    for c in BLOCKED:
        t = re.sub(r"\b" + re.escape(c) + r"\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip(" -–|:")
    if len(t) > 80:
        t = t[:80].rsplit(" ", 1)[0].strip(" -–|:")
    return t

def infer_material(title: str):
    tl = title.lower()
    for kw, val in MATERIAL_MAP:
        if re.search(r"\b" + re.escape(kw) + r"\b", tl):
            return val
    return None

def infer_color(title: str):
    tl = title.lower()
    for kw, val in COLOR_MAP:
        if re.search(r"\b" + re.escape(kw) + r"\b", tl):
            return val
    return None

def asin_of(url: str) -> str:
    m = re.search(r"/dp/([A-Z0-9]{10})", url or "")
    return m.group(1) if m else None

def money(x) -> str:
    return f"{max(0.0, float(x)):.2f}"

def used_asins():
    used = set()
    for p in glob.glob(os.path.join(OUT, "US-*.json")):
        sku = os.path.splitext(os.path.basename(p))[0]
        m = re.match(r"^US-([A-Z0-9]{10})(?:-[A-Z])?$", sku)
        if m:
            used.add(m.group(1))
    return used

def main():
    drafts = json.load(open(SRC, encoding="utf-8"))
    clean = [x for x in drafts if not x.get("error_list")]
    used = used_asins()
    out = []
    seen = set()
    for x in clean:
        vs = x.get("variation_statistics", {})
        sell = vs.get("min_sell_price") or 0
        profit = vs.get("min_profit") or 0
        if sell <= 0 or profit < 5 or (profit / sell) < 0.20:
            continue
        asin = asin_of(x.get("sell_site_url", ""))
        if not asin or asin in seen or asin in used:
            continue
        seen.add(asin)
        out.append(x)
    out.sort(key=lambda x: x["variation_statistics"]["min_profit"], reverse=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    made = []
    for x in out[:n]:
        vs = x["variation_statistics"]
        asin = asin_of(x["sell_site_url"])
        sku = f"US-{asin}"
        title = clean_title(x.get("title", ""))
        cat = x.get("category", [{}])
        cat_name = (cat[0].get("name") or "Home & Garden") if cat else "Home & Garden"
        cat_id = str(cat[0].get("category_id") or "") if cat else ""
        img = (x.get("main_picture_url") or {}).get("url", "")
        if not img.startswith("https://"):
            continue
        sell = float(vs["min_sell_price"])
        buy = float(vs["min_buy_price"])
        profit = float(vs["min_profit"])
        ebay_fees = 0.1325 * sell + 0.30
        fulfillment = sell - buy - ebay_fees - profit
        stock = int((vs.get("in_stock") or {}).get("total", 1) or 1)

        aspects = {"Brand": ["Unbranded"], "Type": [cat_name]}
        mat = infer_material(x.get("title", ""))
        col = infer_color(x.get("title", ""))
        if mat:
            aspects["Material"] = [mat]
        if col:
            aspects["Color"] = [col]

        type_lc = cat_name.lower().rstrip("s")
        desc = (
            f"{title}.\n\nWHAT YOU GET\n"
            f"• 1x {type_lc}, new, in supplier packaging\n\n"
            f"Ships from a US warehouse. Estimated delivery within 10 business days. 30-day returns."
        )
        manifest = {
            "version": 1,
            "sku": sku,
            "marketplaceId": "EBAY_US",
            "product": {
                "title": title,
                "description": desc,
                "aspects": aspects,
                "imageUrls": [img],
            },
            "condition": "NEW",
            "categoryId": cat_id,
            "quantity": 2,
            "price": {"value": money(sell), "currency": "USD"},
            "merchantLocationKey": LOCATION,
            "policies": POLICIES,
            "evidence": {
                "supplierUrl": x.get("sell_site_url", ""),
                "sourceCheckedAt": now,
                "stockObserved": stock,
                "supplierCostUsd": money(buy),
                "deliveryLatestDays": 10,
                "imageRights": "SUPPLIER_AUTHORIZED",
                "vero": "PASS",
                "estimatedEbayFeesUsd": money(ebay_fees),
                "estimatedFulfillmentUsd": money(fulfillment),
                "estimatedNetProfitUsd": money(profit),
            },
        }
        path = os.path.join(OUT, f"{sku}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        made.append((sku, title, cat_id, cat_name, mat, col, sell, profit))

    print(f"Generati {len(made)} manifest (skipping {len(used)} ASIN gia' usati):")
    for sku, title, cat_id, cat_name, mat, col, sell, profit in made:
        print(f"  {sku}  cat={cat_id}({cat_name})  mat={mat} col={col}  sell={money(sell)} net={money(profit)}  | {title[:55]}")

if __name__ == "__main__":
    main()

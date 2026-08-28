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

# Brand tokens to SKIP (VeRO/trademark risk). Up-ticket items are frequently branded;
# the machine's registered rule is generic-only titles. Matched case-insensitive.
BRAND_BLOCK = [
    "lumberjack", "max & lily", "breathesmart", "alen", "flying pig", "+posture",
    "flexispot", "kraus", "finer form", "best choice products", "neatfi", "teraves",
    "london", "aoc", "ust", "c24g1a", "suitical", "lodge", "blackstone", "carote",
    "benq", "dolphin", "maytronics", "pentair", "funboy", "intex", "beyondnice",
    "rosefray", "ucare", "royal gourmet", "icover", "porch shield", "stormaster",
    "skamper", "nike", "disney", "apple", "airtag", "sony", "lg", "samsung", "dyson",
    "lego", "barbie", "hot wheels", "funko", "yeti", "stanley", "crockpot",
    "instant pot", "kitchenaid", "le creuset", "oxo", "cuisinart", "ninja", "breville",
    "keurig", "nutribullet", "vornado", "hamilton beach", "mr coffee", "yaheetech",
    "kingfun", "zephyr", "isobar",
]

def has_brand(title: str) -> bool:
    tl = (title or "").lower()
    return any(b in tl for b in BRAND_BLOCK)

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

# Size/Firmness inferred ONLY when the title names them explicitly (up-ticket learnings:
# mattress needed Size="King" + Firmness="Medium"; towels needed Size="Hand Towel").
# Conservative — no dimension inference (Length/Width/Height): those categories require a
# full SET that titles almost never carry, and a partial value is a compliance fabrication.
SIZE_MAP = [
    ("california king", "California King"), ("king", "King"), ("queen", "Queen"),
    ("full", "Full"), ("twin xl", "Twin XL"), ("twin", "Twin"),
    ("x-large", "X-Large"), ("x large", "X-Large"), ("xx-large", "XX-Large"),
    ("large", "Large"), ("medium", "Medium"), ("small", "Small"),
    ("hand towel", "Hand Towel"), ("bath towel", "Bath Towel"), ("washcloth", "Washcloth"),
]
FIRMNESS_MAP = [
    ("extra firm", "Extra Firm"), ("medium firm", "Medium Firm"), ("medium", "Medium"),
    ("firm", "Firm"), ("soft", "Soft"), ("plush", "Plush"),
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

def _bedding_context(tl: str) -> bool:
    return any(k in tl for k in ("mattress", "towel", "sheet", "comforter", "duvet", "pillow", "topper", "rug"))

def infer_size(title: str):
    tl = title.lower()
    if not _bedding_context(tl):
        return None
    for kw, val in SIZE_MAP:
        if re.search(r"\b" + re.escape(kw) + r"\b", tl):
            return val
    return None

def infer_firmness(title: str):
    tl = title.lower()
    if not _bedding_context(tl):
        return None
    for kw, val in FIRMNESS_MAP:
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
        # Net-profit gate (not %-margin): the machine's North Star is NET profit.
        # A %-margin floor (profit/sell >= 0.20) selects cheap commodity (~24% margin,
        # ~$8 net) and EXCLUDES up-ticket winners (~18% margin, $40-150 net) — the
        # registered margin-escape profile. Absolute net >= $30, sell >= $50, and a
        # floor of 10% only to reject obviously mispriced rows.
        if sell < 50 or profit < 30 or (profit / sell) < 0.10:
            continue
        if has_brand(x.get("title", "")):
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
        size = infer_size(x.get("title", ""))
        firm = infer_firmness(x.get("title", ""))
        if mat:
            aspects["Material"] = [mat]
        if col:
            aspects["Color"] = [col]
        if size:
            aspects["Size"] = [size]
        if firm:
            aspects["Firmness"] = [firm]

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

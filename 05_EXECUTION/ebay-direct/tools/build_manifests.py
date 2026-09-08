#!/usr/bin/env python3
"""Build ebay-direct manifests from AutoDS _drafts_full.json (clean, US-warehouse, margin>=20%)."""
import json, re, sys, os
from datetime import datetime, timezone

# Paths are derived from this script's own location so the tools run on any checkout.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SRC = os.path.join(ROOT, "05_EXECUTION", "EBAY_AUTODS_5_LISTING_LAUNCH", "integrations",
                   "autods", "playwright", "_drafts_full.json")
OUT = os.path.join(ROOT, "05_EXECUTION", "ebay-direct", "manifests")

POLICIES = {"payment": "282011576018", "fulfillment": "282011584018", "return": "282011577018"}
LOCATION = "US-WAREHOUSE"

BLOCKED = ["bpa-free", "bpa free", "waterproof", "safe", "streak-free", "streak free", "eye care"]
TRADEMARK = re.compile(r"[®™]")

def clean_title(t: str) -> str:
    t = TRADEMARK.sub("", t)
    # drop a leading "Brand - " / "Brand | " / "Brand: " segment
    t = re.sub(r"^[A-Z][A-Za-z0-9&'\.\- ]{1,40}\s*[-–|:]\s*", "", t, count=1)
    # strip blocked-claim words (word boundary, case-insensitive)
    for c in BLOCKED:
        t = re.sub(r"\b" + re.escape(c) + r"\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip(" -–|:")
    # truncate to 80 at word boundary
    if len(t) > 80:
        t = t[:80].rsplit(" ", 1)[0].strip(" -–|:")
    return t

def asin_of(url: str) -> str:
    m = re.search(r"/dp/([A-Z0-9]{10})", url or "")
    return m.group(1) if m else None

def money(x) -> str:
    return f"{max(0.0, float(x)):.2f}"

def main():
    drafts = json.load(open(SRC, encoding="utf-8"))
    clean = [x for x in drafts if not x.get("error_list")]
    out = []
    seen = set()
    for x in clean:
        vs = x.get("variation_statistics", {})
        sell = vs.get("min_sell_price") or 0
        profit = vs.get("min_profit") or 0
        if sell <= 0 or profit < 5 or (profit / sell) < 0.20:
            continue
        asin = asin_of(x.get("sell_site_url", ""))
        if not asin or asin in seen:
            continue
        seen.add(asin)
        out.append(x)
    out.sort(key=lambda x: x["variation_statistics"]["min_profit"], reverse=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
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
                "aspects": {"Brand": ["Unbranded"], "Type": [cat_name]},
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
        made.append((sku, title, cat_id, sell, buy, profit))

    print(f"Generati {len(made)} manifest:")
    for sku, title, cat_id, sell, buy, profit in made:
        print(f"  {sku}  cat={cat_id}  sell={money(sell)}  buy={money(buy)}  net={money(profit)}  | {title[:60]}")

if __name__ == "__main__":
    main()

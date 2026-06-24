#!/usr/bin/env python3
"""
rank_us_source.py — second-pass analytic ranker over a marketplace_source.py raw cache.
Pure offline analysis (no network). Reads _raw_products.json, applies:
  - US-warehouse filter (product_details.min_price_warehouse == 'US')
  - serious VeRO/brand detection on the title (leading coined/ALLCAPS/proper-noun token)
  - niche classification (pool / kitchen / meat_food / cleaning / storage ; else dropped)
  - policy risk driven by site_name (amazon = retail-arbitrage risk; aliexpress = low) + regulated cats
  - TEST/HOLD/KILL recommendation matched to the owner's spec (generic, US-WH, fast, aliexpress-preferred)
Outputs a ranked shortlist JSON + Markdown table fragment to stdout and to the cache dir.
Usage: rank_us_source.py <cache_dir>   (defaults to newest mkt_source_* under 90_CACHE)
"""
import os, re, sys, json, glob

# common descriptive words a GENERIC title may start with -> not a brand signal
COMMON = set("""pool cover pump above ground submersible water swimming spa hot tub chlorine skimmer pond
solar inground filter cartridge kitchen cookware cook pot pots pan pans skillet frying saute nonstick non
stick stainless steel cast iron ceramic copper granite enameled glass food storage container containers
canister canisters meal prep airtight bpa free lid lids set piece pieces pcs utensil utensils gadget knife
cutting board colander strainer spatula whisk grater mixing bowl bowls measuring cup spoon ladle tongs
meat tenderizer grinder garlic press chopper slicer mincer ricer juicer grill grills bbq barbecue smoker
mop broom plunger brush bowl toilet microfiber cleaning scrub sponge squeegee duster laundry basket hamper
sorter organizer bin bins rack shelf shelves tote drawer hanging wall mounted heavy duty large extra small
oversized collapsible portable reusable bamboo wooden plastic silicone metal wire dish drying jewelry box
beach towel towels cotton turkish robe bathrobe wine tumbler tumblers stemless coffee maker french press
espresso braiser dutch oven casserole stockpot saucepan deep wide round square clear white black grey gray
green red blue pink purple kids adult sun shade fabric cloth grommets patio outdoor indoor home pre seasoned
with and the for new 2025 2024 inch inches quart oz ounce gallon liter ml count pack packs""".split())

ALLCAPS_OK = set("BPA USA PCS OZ LED XL XXL XS 3D 2D ML US UK EU DIY UV BBQ TV PC HD ABS PVC PP".split())

NICHE = [
    ("pool", re.compile(r"\bpool|hot tub|jacuzzi|\bspa\b|chlorine|skimmer|\bpond\b|swim|inflatable", re.I)),
    ("meat_food", re.compile(r"\bmeat\b|tenderizer|grinder|garlic press|\bchopper\b|mincer|ricer|"
                             r"\bgrill\b|\bbbq\b|smoker|sausage|jerky|vegetable cho", re.I)),
    ("kitchen", re.compile(r"cookware|skillet|frying pan|saute|stockpot|saucepan|dutch oven|braiser|"
                           r"\bpot\b|\bpan\b|colander|strainer|utensil|spatula|whisk|grater|"
                           r"food storage|meal prep|airtight|canister|cutting board|\bknife\b|"
                           r"\bbowl\b|french press|espresso|kettle|bakeware|baking", re.I)),
    ("cleaning", re.compile(r"\bmop\b|broom|plunger|toilet brush|microfiber|squeegee|scrub|cleaning|duster", re.I)),
    ("storage", re.compile(r"storage|organizer|\bbasket\b|hamper|\bbin\b|\brack\b|\bshelf\b|shelves|"
                           r"\btote\b|drawer|laundry", re.I)),
]

HIGHER_RISK_CAT = re.compile(r"electronic|automotive|motorcycle|beauty|health|supplement|cosmetic|"
                             r"makeup|skin care|hair|vitamin|medical|\bbattery|charger|transducer|"
                             r"fish finder|drill|blower|motor|protein|whey", re.I)

MEGABRANDS = ["nike","adidas","disney","panasonic","dyson","lego","apple","samsung","sony","bosch",
              "dewalt","makita","stanley","yeti","rtic","ninja","kitchenaid","cuisinart","instant pot",
              "pyrex","oxo","dash","costway","weber","traeger","coleman","intex","bestway","hayward",
              "pentair","rubbermaid","tupperware","lodge","le creuset","vitamix","keurig","lowrance",
              "worx","wen","fellowes","circulon"]


def is_brandish(token):
    t = token.strip(".,–-")
    if not t or len(t) < 2:
        return False
    low = t.lower()
    if low in COMMON:
        return False
    if t.isupper() and len(t) >= 3 and t not in ALLCAPS_OK and t.isalpha():
        return True
    # internal capital (coined CamelCase): SereneLife, NutriChef, SterlingPro, TowelSelections, VivoHome
    if re.search(r"[a-z][A-Z]", t):
        return True
    # apostrophe brand: Chef'n
    if "'" in t and t[0].isupper():
        return True
    # TitleCase proper noun not common and not purely numeric
    if t[0].isupper() and low not in COMMON and t.isalpha() and len(t) >= 4:
        return True
    return False


def vero_risk(title):
    tl = (title or "")
    low = tl.lower()
    if "™" in tl or "®" in tl:
        return "HIGH"
    if any(b in low for b in MEGABRANDS):
        return "HIGH"
    toks = re.findall(r"[^\s]+", tl)
    # check first 2 tokens for a coined brand
    lead = [t for t in toks[:2]]
    hits = sum(1 for t in lead if is_brandish(t))
    if hits >= 1:
        return "MED"   # likely a seller brand word; title would need a full generic rewrite
    return "LOW"


def niche_of(title):
    for name, rx in NICHE:
        if rx.search(title or ""):
            return name
    return None


def policy_risk(site, cats_blob, vrisk):
    risk = "LOW"
    if (site or "").lower() == "amazon":
        risk = "MED"   # retail-arbitrage account-health risk (playbook)
    if HIGHER_RISK_CAT.search(cats_blob or ""):
        risk = "MED" if risk == "LOW" else "HIGH"
    return risk


def recommend(wh, niche, site, stime, margin, vrisk, buy):
    # TEST = US-warehouse + on-niche + generic(VeRO LOW) + fast(<=5d) + margin>=5.
    # Fast US-warehouse items are predominantly site_name=amazon (FBA US): that is the proven amazon10
    # path. The retail-arbitrage account-health risk is surfaced in the policy column, not hidden.
    if wh != "US" or niche is None:
        return "KILL"
    if vrisk == "HIGH":
        return "KILL"            # branded megabrand -> not our VeRO-safe play
    if margin is None or margin < 4:
        return "KILL"
    fast = isinstance(stime, (int, float)) and stime <= 5
    if vrisk == "LOW" and fast and margin >= 5:
        return "TEST"
    if margin >= 4 and (fast or vrisk in ("LOW", "MED")):
        return "HOLD"            # slow aliexpress US-WH, or MED-brand fixable-by-rewrite, or thin margin
    return "HOLD"


def main():
    if len(sys.argv) > 1:
        cache = sys.argv[1]
    else:
        root = os.path.abspath(__file__)
        while root != os.path.dirname(root) and not os.path.isdir(os.path.join(root, "90_CACHE")):
            root = os.path.dirname(root)
        cands = sorted(glob.glob(os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_source_*")))
        cache = cands[-1]
    data = json.load(open(os.path.join(cache, "_raw_products.json"), encoding="utf-8"))

    rows = []
    for it in data:
        pd = it.get("product_details") or {}
        if pd.get("min_price_warehouse") != "US":
            continue
        title = it.get("title") or ""
        niche = niche_of(title)
        if niche is None:
            continue
        site = it.get("site_name") or ""
        supplier = it.get("supplier_name") or ""
        buy = pd.get("min_price"); sell = pd.get("min_msrp_price"); ship = pd.get("min_shipping_cost") or 0
        stime = pd.get("max_shipping_time")
        margin = round(sell - buy - ship, 2) if isinstance(buy,(int,float)) and isinstance(sell,(int,float)) else None
        mpct = round(100*margin/sell,1) if margin is not None and sell else None
        cats_blob = json.dumps(it.get("categories") or "", ensure_ascii=False)
        vrisk = vero_risk(title)
        prisk = policy_risk(site, cats_blob, vrisk)
        rec = recommend("US", niche, site, stime, margin, vrisk, buy)
        rows.append({"title": title[:78], "niche": niche, "site": site, "supplier": supplier[:24],
                     "wh": "US", "stime": stime, "buy": buy, "sell": sell, "margin": margin, "mpct": mpct,
                     "vero": vrisk, "policy": prisk, "rec": rec, "id_on_site": it.get("id_on_site"),
                     "winning": bool(it.get("is_winning_product")), "cluster": it.get("_cluster","")})

    rank_rec = {"TEST": 3, "HOLD": 2, "KILL": 1}
    def commodity_fit(b):
        return 1 if isinstance(b,(int,float)) and 8 <= b <= 35 else 0
    rows.sort(key=lambda r: (rank_rec.get(r["rec"],0),
                             1 if (r["site"] or "").lower()!="amazon" else 0,
                             1 if r["vero"]=="LOW" else 0,
                             commodity_fit(r["buy"]),
                             -(r["stime"] or 99),
                             r["margin"] or -99), reverse=True)

    # dedup near-identical titles (keep first = best after sort)
    seen_key = set(); deduped = []
    for r in rows:
        key = " ".join(re.sub(r"[^a-z0-9 ]", " ", (r["title"] or "").lower()).split()[:5])
        if key in seen_key:
            continue
        seen_key.add(key); deduped.append(r)
    rows = deduped

    json.dump(rows, open(os.path.join(cache, "_ranked_onniche.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

    test = [r for r in rows if r["rec"]=="TEST"]
    hold = [r for r in rows if r["rec"]=="HOLD"]
    print("on-niche US-warehouse products:", len(rows), "| TEST:", len(test), "HOLD:", len(hold),
          "KILL:", sum(1 for r in rows if r["rec"]=="KILL"))
    by_niche = {}
    for r in rows:
        by_niche.setdefault(r["niche"], [0,0])
        by_niche[r["niche"]][0]+=1
        if r["rec"]=="TEST": by_niche[r["niche"]][1]+=1
    print("by niche (total/TEST):", {k:tuple(v) for k,v in by_niche.items()})
    ali = sum(1 for r in test if (r["site"] or "").lower()=="aliexpress")
    print("TEST source split: aliexpress=%d amazon=%d other=%d" %
          (ali, sum(1 for r in test if (r["site"] or "").lower()=="amazon"), len(test)-ali-sum(1 for r in test if (r["site"] or "").lower()=="amazon")))
    print("="*120)
    print("%-4s %-9s %-10s %-4s %-6s %-6s %-6s %-5s %-5s %-5s | %s" %
          ("REC","niche","site","shp","buy","sell","margin","mgn%","vero","pol","title"))
    print("-"*120)
    for r in (test+hold)[:45]:
        print("%-4s %-9s %-10s %-4s %-6s %-6s %-6s %-5s %-5s %-5s | %s" %
              (r["rec"], r["niche"], (r["site"] or "")[:10], r["stime"], r["buy"], r["sell"],
               r["margin"], r["mpct"], r["vero"], r["policy"], r["title"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

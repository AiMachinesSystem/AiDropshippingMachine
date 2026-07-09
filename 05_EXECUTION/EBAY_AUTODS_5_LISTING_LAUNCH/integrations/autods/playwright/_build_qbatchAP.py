#!/usr/bin/env python3
"""
_build_qbatchAP.py — batch AP builder (2026-07-08): fresh july8 pull + july6c residuals.
Target: 80 candidates (cap 4/cluster) to ensure 36 publications despite ~45% skip rate.
Output: _qbatchAP.json + updates _attempted_asins.json.
"""
import json, re, sys, os, collections, math, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..", "..", "..")
CACHE = os.path.join(ROOT, "90_CACHE", "fetches", "autods")
ATT_FILE = os.path.join(HERE, "_attempted_asins.json")
OUT_FILE = os.path.join(HERE, "_qbatchAP.json")

CAND_CAP = 80
CLUSTER_CAP = 4

# Find the latest mkt_source dir (july8 pull + july6c as fallback)
def find_shortlists():
    dirs = sorted(glob.glob(os.path.join(CACHE, "mkt_source_*")), reverse=True)
    return [os.path.join(d, "_shortlist_us.json") for d in dirs
            if os.path.exists(os.path.join(d, "_shortlist_us.json"))]

SOURCES = find_shortlists()[:6]   # use 6 most recent pulls
print(f"Using {len(SOURCES)} source(s): {[os.path.basename(os.path.dirname(s)) for s in SOURCES]}")

attempted = set(json.load(open(ATT_FILE, encoding="utf-8"))) if os.path.exists(ATT_FILE) else set()
print(f"Attempted so far: {len(attempted)}")

# Hard KILL — dead at 1.5x OR VeRO/brand risk OR seasonal-dead
KILL = re.compile(r"\b(cable management|cable tray|cord organizer tray|pot lid|lid holder|lid rack|lid organizer|"
                  r"shaker bottle|shaker cup|blender ?bottle|"
                  r"led dog collar|led collar|light.?up collar|light.?up leash|"
                  r"drink holder|cup holder|"
                  r"pool float|inflatable lounger|swim ring|floaties|"
                  r"solar (garden )?stake|solar flower|"
                  r"slow feeder|lickimat|"
                  r"patriotic|american flag|july 4|4th of july|"
                  r"beach tent|beach wagon|misting fan|neck fan|portable ac|"
                  r"christmas|holiday lights|xmas|"
                  r"swimming trunks|swimwear|swimsuit)\b", re.I)

# Generic content/brand/consumable filter
BAD = re.compile(r"\b(food|treats?|freeze.?dried|kibble|rawhide|vitamin|supplement|edible|snack|formula|"
                 r"medicine|cream|serum|lotion|battery|charger|airtag|"
                 r"apple watch|samsung|nintendo|lego|disney|"
                 r"nfl|nba|mlb|nhl|ncaa|"
                 r"shorts?|sweatshirts?|hoodie|leggings?|necklaces?|bracelets?|sunglasses|"
                 r"shower head|kitchen faucet|centerset|water bottle|tumblers?|"
                 r"socks?|bodysuit|slipper|coat|clothes|apparel|shirt|underwear|bra|"
                 r"chlorine|bleach|whitener|chemicals?|pesticide)\b", re.I)

# Q3 cluster runway boosts
CLUSTER_BOOST = {
    "Halloween": 1.7,
    "BTS Dorm": 1.6,
    "BTS Desk": 1.5,
    "Bath": 1.4,
    "bathroom": 1.4,
    "Storage": 1.3,
    "Shoe": 1.3,
    "Kitchen": 1.3,
    "Auto": 1.25,
    "Garage": 1.2,
    "Pet": 1.2,
    "Craft": 1.2,
    "Kids": 1.2,
    "Sports": 1.15,
    "Outdoors": 1.1,
    "Garden": 1.1,
    "Health": 1.15,
}

# Title-level VIABLE boosts (proven eBay demand)
TITLE_BOOST = [
    (re.compile(r"shoe rack|shoe organizer|shoe storage", re.I), 1.45),
    (re.compile(r"car (seat|trunk|console) organizer", re.I), 1.35),
    (re.compile(r"air fryer (liner|basket|rack|silicone)", re.I), 1.40),
    (re.compile(r"pickleball paddle", re.I), 1.50),
    (re.compile(r"dart board|cornhole set", re.I), 1.40),
    (re.compile(r"tackle box|fishing rod holder", re.I), 1.20),
    (re.compile(r"knitting needle|crochet hook", re.I), 1.25),
    (re.compile(r"earring organizer|ring dish|jewelry (stand|tray|rack)", re.I), 1.30),
    (re.compile(r"pill organizer|medicine organizer|first aid", re.I), 1.20),
    (re.compile(r"socket organizer|wrench roll|tool roll", re.I), 1.25),
    (re.compile(r"reacher grabber|grabber tool", re.I), 1.30),
    (re.compile(r"curtain rod|tension rod|blackout liner", re.I), 1.25),
    (re.compile(r"crystal growing|slime kit|science (kit|experiment)", re.I), 1.30),
    (re.compile(r"instant pot|pressure cooker (rack|ring|trivet)", re.I), 1.40),
    (re.compile(r"halloween|pumpkin (decor|light|string)", re.I), 1.60),
    (re.compile(r"tea (chest|infuser|caddy|organizer)", re.I), 1.20),
    (re.compile(r"grooming brush|nail grinder|deshedding", re.I), 1.35),
    (re.compile(r"sun shade windshield|car sun shade", re.I), 1.30),
]

NICHE = {
    "Kitchen": "kitchen", "Cookware": "kitchen", "Utensils": "kitchen",
    "Pet": "kitchen", "dog": "kitchen", "cat": "kitchen",
    "Storage": "storage", "Closet": "storage", "Shoe": "storage",
    "Auto": "storage", "Garage": "storage", "Health": "storage",
    "Games": "storage", "Craft": "storage", "Kids": "storage",
    "Bath": "cleaning", "Laundry": "cleaning",
    "Outdoors": "pool", "Garden": "pool", "Sports": "pool",
    "Halloween": "pool", "Decor": "storage",
}


def niche_of(cl):
    for k, v in NICHE.items():
        if k.lower() in cl.lower():
            return v
    return "kitchen"


def weight(title, cluster):
    w = 1.0
    cl = cluster or ""
    for k, v in CLUSTER_BOOST.items():
        if k.lower() in cl.lower():
            w = max(w, v)
    for rx, v in TITLE_BOOST:
        if rx.search(title or ""):
            w = max(w, v)
    return w


def net_margin(buy, sell):
    if not buy or not sell or sell == 0:
        return 0
    return (sell * 0.86 - buy) / sell * 100


# Load all sources, dedupe by id_on_site
seen_ids = set()
pool = []
for src in SOURCES:
    if not os.path.exists(src):
        print(f"WARN: missing {src}")
        continue
    items = json.load(open(src, encoding="utf-8"))
    for x in items:
        aid = x.get("id_on_site", "")
        if not aid or aid in seen_ids or aid in attempted:
            continue
        seen_ids.add(aid)
        pool.append(x)

print(f"Pool after dedup+attempted filter: {len(pool)}")

# Filter
kept = []
killed = 0
for x in pool:
    t = (x.get("title") or "").strip()
    if not t or len(t) < 10:
        continue
    if KILL.search(t):
        killed += 1
        continue
    if BAD.search(t):
        killed += 1
        continue
    if x.get("wh") != "US":
        continue
    if x.get("rec") not in ("TEST", "HOLD"):
        continue
    if x.get("vero") == "HIGH" or x.get("policy") == "HIGH":
        continue
    buy = x.get("buy") or 0
    sell = x.get("sell") or 0
    if buy <= 0 or sell <= 0:
        continue
    nm = net_margin(buy, sell)
    if nm < 15:
        continue
    kept.append(x)

print(f"Kept after filters: {len(kept)} (killed: {killed})")

# Score
for x in kept:
    buy = x.get("buy") or 0
    sell = x.get("sell") or 0
    nm = net_margin(buy, sell)
    w = weight(x.get("title", ""), x.get("cluster", ""))
    rc = x.get("rcount") or 0
    rating_bonus = 1.1 if (x.get("rating") or 0) >= 4.3 else 1.0
    x["_nm"] = round(nm, 2)
    x["_w"] = round(w, 2)
    x["_score"] = round(nm * w * (1 + math.log1p(rc) * 0.05) * rating_bonus, 2)

kept.sort(key=lambda x: x["_score"], reverse=True)

# Cluster cap
cluster_count = collections.Counter()
selected = []
for x in kept:
    cl_key = (x.get("cluster") or "")[:40]
    if cluster_count[cl_key] >= CLUSTER_CAP:
        continue
    cluster_count[cl_key] += 1
    selected.append(x)
    if len(selected) >= CAND_CAP:
        break

print(f"\nSelected {len(selected)} candidates:")
for i, x in enumerate(selected):
    print(f"  {i+1:2d}. [{x['_score']:6.1f}] nm={x['_nm']:5.1f}% w={x['_w']} | "
          f"${x.get('buy',0):.2f}→${x.get('sell',0):.2f} | "
          f"{(x.get('title') or '')[:60]}")

BRAND_RE = re.compile(r"^[A-Z][A-Z0-9\'’&.\-]+$")

def seo_title(t):
    words = t.split()
    if words and BRAND_RE.match(words[0]):
        words = words[1:]
        if words and words[0] == "-":
            words = words[1:]
    s = " ".join(words).strip()
    if len(s) <= 79:
        return s
    cut = s[:79].rfind(" ")
    return s[:cut].strip() if cut > 30 else s[:79]

# Build output JSON
out = []
for x in selected:
    t = (x.get("title") or "").strip()
    out.append({
        "asin": x["id_on_site"],
        "title": t[:80],
        "seo_title": seo_title(t),
        "niche": niche_of(x.get("cluster", "")),
        "ebay_median": round(x.get("sell", 0), 2),
        "gross": round(x.get("margin", 0), 2),
        "recent30": x.get("rcount") or 0,
        "score": x["_score"],
        "cluster": x.get("cluster", ""),
        "buy": x.get("buy", 0),
        "net_margin_est": x["_nm"],
    })

json.dump(out, open(OUT_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nWritten: {OUT_FILE} ({len(out)} candidates)")

# Update attempted_asins.json
att_list = json.load(open(ATT_FILE, encoding="utf-8")) if os.path.exists(ATT_FILE) else []
att_set = set(att_list)
new_asins = [x["asin"] for x in out if x["asin"] not in att_set]
att_list.extend(new_asins)
json.dump(att_list, open(ATT_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Updated attempted_asins.json: +{len(new_asins)} → total {len(att_list)}")

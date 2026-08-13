#!/usr/bin/env python3
"""Read-only analysis of the last AutoDS catalog pull -> normalized CSV + SQLite.
No interpretation: every number is counted from the file.
"""
import json, os, re, csv, sqlite3, statistics as st
from collections import defaultdict

SRC = r"C:\AI Machine ebay-autoDS\AiDropshippingMachine\90_CACHE\fetches\deadclean_2026-07-27\products_live_2026-07-27_130800.json"
OUT = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(SRC, encoding="utf-8"))

DANGLING = {"with","for","and","the","a","an","of","in","on","to","by","or","w","x","is","are",
            "non","anti","ultra","super","multi","pro","plus","up","from","that","this","your"}

def cat_of(r):
    c = r.get("category")
    if isinstance(c, list) and c: return (c[0].get("name") or "").strip()
    if isinstance(c, dict): return (c.get("name") or "").strip()
    return ""

recs = []
for r in rows:
    t = (r.get("title") or "").strip()
    toks = t.split()
    last = re.sub(r"[^A-Za-z0-9]", "", toks[-1]).lower() if toks else ""
    vs = r.get("variation_statistics") or {}
    sell = vs.get("min_sell_price"); buy = vs.get("min_buy_price"); prof = vs.get("min_profit")
    instock = ((vs.get("in_stock") or {}).get("total") or 0)
    oos     = ((vs.get("out_of_stock") or {}).get("total") or 0)
    # truncation signals
    frag    = bool(last) and len(last) <= 2 and last.isalpha()
    dang    = last in DANGLING
    punct   = t.endswith(("-", "\u2013", ",", "&", "/", "|", "("))
    recs.append({
        "id": r.get("id"), "item_id": str(r.get("item_id_on_site")), "title": t,
        "title_len": len(t), "over80": len(t) > 80, "at_cap": 79 <= len(t) <= 80,
        "trunc": frag or dang or punct,
        "category": cat_of(r) or "(vuota)", "sold": int(r.get("total_sold_count") or 0),
        "sell_price": sell, "buy_price": buy, "profit": prof,
        "margin_pct": round(100*prof/sell, 1) if (sell and prof is not None) else None,
        "in_stock": instock, "oos": oos,
        "upload_date": (r.get("upload_date") or "")[:10],
        "url": r.get("preview_url"), "source": r.get("sell_site_url"),
    })

n = len(recs)
pct = lambda x: f"{100*x/n:.1f}%"
med = lambda v: st.median(v) if v else 0

print(f"=== CATALOGO REALE — {n} listing attivi [pull 2026-07-27 13:08] ===\n")

# 1 TITLES
lens = [x["title_len"] for x in recs]
over = [x for x in recs if x["over80"]]; cap = [x for x in recs if x["at_cap"]]
tr   = [x for x in recs if x["trunc"]]
bad  = [x for x in recs if x["trunc"] or x["over80"]]
print("1) TITOLI")
print(f"   lunghezza min {min(lens)} / mediana {int(med(lens))} / max {max(lens)}")
print(f"   >80 char, ILLEGALI su eBay      : {len(over):4d}  {pct(len(over))}")
print(f"   79-80 char (al limite)          : {len(cap):4d}  {pct(len(cap))}")
print(f"   troncati a meta' frase          : {len(tr):4d}  {pct(len(tr))}")
print(f"   >>> DA RISCRIVERE               : {len(bad):4d}  {pct(len(bad))}")
print("\n   esempi (troncati):")
for x in tr[:10]: print(f"     [{x['title_len']:>3}] {x['title']}")
print("   esempi (>80):")
for x in over[:4]: print(f"     [{x['title_len']:>3}] {x['title'][:100]}")

# 2 CATEGORIES
bc = defaultdict(lambda: {"n":0,"s":0,"u":0,"p":[],"m":[]})
for x in recs:
    b = bc[x["category"]]; b["n"]+=1; b["u"]+=x["sold"]
    if x["sold"]>0: b["s"]+=1
    if x["sell_price"]: b["p"].append(x["sell_price"])
    if x["margin_pct"] is not None: b["m"].append(x["margin_pct"])
print(f"\n2) CATEGORIE — {len(bc)} distinte / {n} listing = {n/len(bc):.1f} per categoria")
sel = sorted([(c,b) for c,b in bc.items() if b["s"]>0], key=lambda kv:(-kv[1]["u"]))
print(f"\n   LE {len(sel)} CATEGORIE CHE HANNO VENDUTO (unita' vendute):")
print(f"   {'categoria':<40}{'list':>5}{'vend':>5}{'unit':>5}{'prz.med':>9}{'marg%':>7}")
for c,b in sel:
    print(f"   {c[:40]:<40}{b['n']:>5}{b['s']:>5}{b['u']:>5}{med(b['p']):>9.2f}{med(b['m']):>7.1f}")
print(f"\n   TOP 12 PER VOLUME DI LISTING:")
print(f"   {'categoria':<40}{'list':>5}{'vend':>5}{'prz.med':>9}{'marg%':>7}")
for c,b in sorted(bc.items(), key=lambda kv:-kv[1]["n"])[:12]:
    print(f"   {c[:40]:<40}{b['n']:>5}{b['s']:>5}{med(b['p']):>9.2f}{med(b['m']):>7.1f}")

# 3 PRICE / MARGIN
sp = [x["sell_price"] for x in recs if x["sold"]>0 and x["sell_price"]]
np_= [x["sell_price"] for x in recs if x["sold"]==0 and x["sell_price"]]
mg = [x["margin_pct"] for x in recs if x["margin_pct"] is not None]
print(f"\n3) PREZZO / MARGINE")
print(f"   venditori   n={len(sp):4d}  prezzo mediano ${med(sp):.2f}")
print(f"   non-vend.   n={len(np_):4d}  prezzo mediano ${med(np_):.2f}")
print(f"   margine AutoDS dichiarato: mediana {med(mg):.1f}%  (n={len(mg)})")
print(f"   listing con >=1 vendita: {sum(1 for x in recs if x['sold']>0)} / {n}")
oosn = sum(1 for x in recs if x["oos"] > 0)
print(f"   listing con almeno 1 variante OUT OF STOCK: {oosn}  {pct(oosn)}")

# EXPORT
csvp = os.path.join(OUT, "catalog_2026-07-27.csv")
with open(csvp,"w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(recs[0].keys())); w.writeheader(); w.writerows(recs)
dbp = os.path.join(OUT,"catalog.db")
if os.path.exists(dbp): os.remove(dbp)
con=sqlite3.connect(dbp)
con.execute("""CREATE TABLE listing(id TEXT PRIMARY KEY,item_id TEXT,title TEXT,title_len INT,
 over80 INT,at_cap INT,trunc INT,category TEXT,sold INT,sell_price REAL,buy_price REAL,
 profit REAL,margin_pct REAL,in_stock INT,oos INT,upload_date TEXT,url TEXT,source TEXT)""")
con.executemany("INSERT OR REPLACE INTO listing VALUES(:id,:item_id,:title,:title_len,:over80,"
 ":at_cap,:trunc,:category,:sold,:sell_price,:buy_price,:profit,:margin_pct,:in_stock,:oos,"
 ":upload_date,:url,:source)",
 [{**r,"over80":int(r["over80"]),"at_cap":int(r["at_cap"]),"trunc":int(r["trunc"])} for r in recs])
con.commit(); con.close()
print(f"\nEXPORT  {csvp}\n        {dbp}")

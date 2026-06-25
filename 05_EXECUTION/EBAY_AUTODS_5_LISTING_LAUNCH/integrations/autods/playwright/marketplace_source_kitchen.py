#!/usr/bin/env python3
"""READ-ONLY fresh Kitchen-niche sourcing (proven account niche = real eBay-demand proxy). Cracked filter API,
US-warehouse, single-config-friendly terms. Output raw cache for extraction. Usage: [LO] [HI]"""
import os, re, sys, json
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json")
BASE="https://platform.autods.com"; API="https://gw.autods.com/marketplace/api/products/"
PAGES,LIMIT,MIN_RATING,MIN_RC=6,50,4.2,200
CLUSTERS=[("kitchen organizer","search","kitchen organizer"),("pantry organizer","search","pantry organizer"),
 ("drawer organizer kitchen","search","kitchen drawer organizer"),("dish drying rack","search","dish drying rack"),
 ("pot rack","search","pot and pan organizer"),("utensil holder","search","utensil holder"),
 ("spice organizer","search","spice organizer"),("kitchen storage","search","kitchen storage container"),
 ("knife block","search","knife block holder"),("mixing bowls","search","mixing bowls set"),
 ("measuring","search","measuring cups spoons"),("cutting board","search","cutting board set"),
 ("oil dispenser","search","oil dispenser bottle"),("kitchen shelf","search","kitchen counter shelf"),
 ("food storage","search","airtight food storage"),("colander strainer","search","colander strainer set"),
 ("baking mat","search","silicone baking mat set"),("can opener","search","can opener kitchen")]
PROJECTION={"title":{},"images":{},"supplier_name":{},"site_name":{},"id_on_site":{},"product_details":{},
 "region":{},"private_supplier":{},"is_winning_product":{},"is_free_winning_product":{},"categories":{}}
def find_root(s):
    c=os.path.abspath(s)
    while c!=os.path.dirname(c):
        if os.path.isdir(os.path.join(c,"10_OUTPUTS")): return c
        c=os.path.dirname(c)
    return s
def body(v,off,lo,hi):
    return {"projection":PROJECTION,"order_by":{"direction":"desc","name":"spv_param"},"condition":"and",
     "limit":LIMIT,"offset":off,"filters":[{"name":"rating","value":str(MIN_RATING),"value_type":"float","op":">"},
     {"name":"rating_count","value":str(MIN_RC),"value_type":"integer","op":">"},
     {"name":"variations.variation_details.price","value":"%s,%s"%(lo,hi),"value_type":"float","op":"between"},
     {"name":"search_query","value_type":"string","op":"search","value":v}]}
def main():
    lo=sys.argv[1] if len(sys.argv)>1 else "28"; hi=sys.argv[2] if len(sys.argv)>2 else "90"
    from playwright.sync_api import sync_playwright
    root=find_root(HERE); ts=datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache=os.path.join(root,"90_CACHE","fetches","autods","mkt_source_kitchen_"+ts); os.makedirs(cache,exist_ok=True)
    auth={};prods={}
    def on_req(r):
        if not auth and r.url.startswith(API) and r.method=="POST":
            for k,v in (r.headers or {}).items():
                if k.lower() in ("authorization","content-type","accept") or k.lower().startswith("x-"): auth[k]=v
    print("KITCHEN pull $%s-%s | clusters %d"%(lo,hi,len(CLUSTERS)))
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page(); pg.on("request",on_req)
        pg.goto(BASE+"/marketplace",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
        for label,kind,value in CLUSTERS:
            got=0
            for i in range(PAGES):
                try:
                    r=ctx.request.post(API,headers=auth,data=json.dumps(body(value,i*LIMIT,lo,hi)),timeout=45000)
                    if r.status!=200: break
                    items=r.json().get("results") or []
                except Exception: break
                if not items: break
                for it in items:
                    if isinstance(it,dict) and it.get("_id"): it["_cluster"]=label; prods.setdefault(it["_id"],it)
                got+=len(items)
                if len(items)<LIMIT: break
            print("  [%s] ~%d"%(label[:22],got))
        b.close()
    json.dump(list(prods.values()),open(os.path.join(cache,"_raw_products.json"),"w",encoding="utf-8"),ensure_ascii=False)
    us=sum(1 for it in prods.values() if (it.get("product_details") or {}).get("min_price_warehouse")=="US")
    print("-"*50);print("unique:",len(prods),"| US-WH:",us,"| cache:",cache)
if __name__=="__main__": sys.exit(main())

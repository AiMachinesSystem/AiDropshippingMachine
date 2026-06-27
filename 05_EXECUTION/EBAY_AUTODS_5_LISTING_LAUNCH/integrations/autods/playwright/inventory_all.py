import os,re,json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
URL="https://v2-api.autods.com/products/3713044/list/"
cap={}
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    def on_req(req):
        if "/products/" in req.url and "/list/" in req.url and req.method=="POST" and not cap:
            cap["url"]=req.url; cap["headers"]=dict(req.headers); cap["body"]=req.post_data
    pg.on("request", on_req)
    pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
    if not cap: print("NO_CAP"); b.close(); raise SystemExit
    hdr={k:v for k,v in cap["headers"].items() if k.lower() in ("authorization","content-type","accept","origin","referer")}
    body=json.loads(cap["body"]); body["limit"]=300; body["offset"]=0
    resp=pg.request.post(cap["url"], data=json.dumps(body), headers=hdr)
    print("STATUS:",resp.status)
    data=resp.json(); b.close()
items=data.get("results") or data.get("data") or []
if isinstance(items,dict): items=items.get("results",[])
print("TOTAL_RETURNED:",len(items))
clean=[]
for it in items:
    pid=str(it.get("id")); title=(it.get("title") or "")[:48]
    vs=it.get("variation_statistics") or {}
    buy=vs.get("min_buy_price"); prof=vs.get("min_profit")
    st=vs.get("in_stock"); st=(st.get("total") if isinstance(st,dict) else st)
    reg=vs.get("supplier_default_region") or vs.get("supplier_region")
    asin=""; regn=reg
    if isinstance(reg,list) and reg: asin=reg[0].get("item_id_on_site",""); regn=reg[0].get("region")
    nvar=it.get("amount_of_variations"); errs=it.get("error_list") or []
    sentinel=(buy is not None and abs(float(buy)-133.13)<0.5)
    ok=(regn==1) and (st and float(st)>0) and not sentinel
    if ok: clean.append((pid,prof,asin,title,nvar,len(errs)))
clean.sort(key=lambda x:-(float(x[1]) if x[1] else 0))
print("CLEAN_COUNT:",len(clean))
for pid,prof,asin,title,nvar,ne in clean:
    print("%-26s prof=%-7s var=%-3s err=%-2s %-12s | %s"%(pid,prof,nvar,ne,asin,title))

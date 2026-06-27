import os,json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
cap={}
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    def on_req(req):
        if "/products/" in req.url and "/list/" in req.url and req.method=="POST" and not cap:
            cap["url"]=req.url; cap["headers"]=dict(req.headers); cap["body"]=req.post_data
    pg.on("request", on_req)
    pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
    hdr={k:v for k,v in cap["headers"].items() if k.lower() in ("authorization","content-type","accept","origin","referer")}
    for ps in [None,0,1,2,3,4,5]:
        body=json.loads(cap["body"]); body["limit"]=400; body["offset"]=0
        if ps is None: body.pop("product_status",None)
        else: body["product_status"]=ps
        try:
            r=pg.request.post(cap["url"], data=json.dumps(body), headers=hdr)
            d=r.json(); items=d.get("results") or d.get("data") or []
            if isinstance(items,dict): items=items.get("results",[])
            print("product_status=%s -> count=%d"%(ps,len(items)))
        except Exception as e: print("ps",ps,"ERR",str(e)[:60])
    b.close()

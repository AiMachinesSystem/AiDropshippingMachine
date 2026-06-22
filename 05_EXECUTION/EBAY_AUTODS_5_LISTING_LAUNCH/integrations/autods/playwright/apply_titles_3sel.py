import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
TARGETS=[
 (r"cheese board|charcuterie|acacia","Acacia Cheese Board Charcuterie Platter Slate Tray Stainless Knife Tools Gift"),
 (r"booster|car seat","Dog Booster Car Seat Small Dogs Pet Travel Bed Safety Belt Tether Washable Cover"),
]
for _p,_t in TARGETS: assert len(_t)<=80,(len(_t),_t)
def expand(pg):
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    for pat,title in TARGETS:
        pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000); expand(pg)
        inputs=pg.locator("input[placeholder='Title']"); fld=None; cur=None; done=False
        for i in range(inputs.count()):
            try: v=inputs.nth(i).input_value()
            except Exception: continue
            if v==title: done=True; break
            if re.search(pat,v,re.I): fld=inputs.nth(i); cur=v; break
        if done: print("[skip] already:",title[:40]); continue
        if not fld: print("[MISS]",pat); continue
        print("[match]",(cur or "")[:50]); fld.scroll_into_view_if_needed(timeout=4000); fld.fill(title); pg.wait_for_timeout(800)
        res=pg.evaluate(r"""(nt)=>{const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value===nt); if(!inp)return 'no'; let el=inp; for(let k=0;k<14&&el.parentElement;k++){el=el.parentElement; const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||'')); if(btn){btn.scrollIntoView({block:'center'});btn.click();return 'saved';}} return 'nosave';}""",title)
        print("  save:",res,"->",title[:45]); pg.wait_for_timeout(4000)
    # verify
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000); expand(pg)
    ts=[]; inp2=pg.locator("input[placeholder='Title']")
    for i in range(inp2.count()):
        try: ts.append(inp2.nth(i).input_value())
        except Exception: pass
    for _p,t in TARGETS: print("PERSISTED=",t in ts, t[:45])
    b.close()

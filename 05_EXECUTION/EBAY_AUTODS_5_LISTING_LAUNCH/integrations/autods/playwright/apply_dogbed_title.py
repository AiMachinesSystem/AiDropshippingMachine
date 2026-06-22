import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
PAT=r"dog bed|orthopedic|bolster|pet bed"
TITLE="Orthopedic Dog Bed Bolster Memory Foam Washable Cover Calming Couch Sofa Pet Mat"
assert len(TITLE)<=80, len(TITLE)
from playwright.sync_api import sync_playwright
def expand(pg):
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000); expand(pg)
    inputs=pg.locator("input[placeholder='Title']"); fld=None; cur=None
    for i in range(inputs.count()):
        try: v=inputs.nth(i).input_value()
        except Exception: continue
        if v==TITLE: print("already applied"); fld="DONE"; break
        if re.search(PAT,v,re.I): fld=inputs.nth(i); cur=v; break
    if fld is None: print("MISS no dog bed draft"); b.close(); sys.exit(1)
    if fld!="DONE":
        print("match:",(cur or "")[:60]); fld.scroll_into_view_if_needed(timeout=4000); fld.fill(TITLE); pg.wait_for_timeout(800)
        res=pg.evaluate(r"""(nt)=>{const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value===nt); if(!inp)return 'no'; let el=inp; for(let k=0;k<14&&el.parentElement;k++){el=el.parentElement; const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||'')); if(btn){btn.scrollIntoView({block:'center'});btn.click();return 'saved';}} return 'nosave';}""",TITLE)
        print("save:",res); pg.wait_for_timeout(4000)
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000); expand(pg)
    ts=[]; inp2=pg.locator("input[placeholder='Title']")
    for i in range(inp2.count()):
        try: ts.append(inp2.nth(i).input_value())
        except Exception: pass
    print("PERSISTED:", TITLE in ts)
    b.close()

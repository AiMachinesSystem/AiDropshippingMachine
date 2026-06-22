import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
URL=BASE+"/upload/6a3374dc51511bebb0528135&1"
GUARD="orthopedic"; MARK="cozy, supportive sleep"
HTML=("<p>Orthopedic Dog Bed - Cozy, Supportive Sleep for Your Best Friend</p>"
 "<p>Give your dog a deep, restful sleep. The supportive memory-foam base relieves pressure on joints, while the raised bolster sides give a sense of security and a comfy place to rest the head.</p>"
 "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
 "<ul><li>Supportive memory-foam base cushions hips, elbows and joints</li>"
 "<li>Raised bolster walls for head and neck support and a secure, calming feel</li>"
 "<li>Removable cover zips off for easy machine washing</li>"
 "<li>Non-slip bottom keeps the bed in place on any floor</li>"
 "<li>Soft, durable fabric suitable for dogs and cats</li></ul>"
 "<p>Choose the size that fits your pet - measure your dog nose-to-tail and add a few inches for comfort.</p>"
 "<p><strong>WHAT YOU GET:</strong> 1x Orthopedic Bolster Pet Bed with removable washable cover. Color and size may vary by selection.</p>")
from playwright.sync_api import sync_playwright
def tab(pg): return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;}return false;}""")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(URL,wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    cur=pg.locator("input[placeholder='Title']").first.input_value(); print("title:",cur[:55])
    if GUARD not in cur.lower(): print("GUARD FAIL"); b.close(); sys.exit(1)
    print("desc tab:",tab(pg)); pg.wait_for_timeout(3500)
    print("setData:",pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ck';const ins=Object.values(window.CKEDITOR.instances);if(!ins.length)return 'no-inst';ins[0].setData(h);return 'set';}""",HTML)); pg.wait_for_timeout(1500)
    try: pg.get_by_role("button",name=re.compile(r"^\s*Save\s*$",re.I)).first.click(timeout=5000); print("save: ok")
    except Exception as e: print("save err",type(e).__name__)
    pg.wait_for_timeout(3500)
    pg.goto(URL,wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(6000); tab(pg); pg.wait_for_timeout(4000)
    got=pg.evaluate("""()=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return '';const ins=Object.values(window.CKEDITOR.instances);return ins.length?ins[0].getData().slice(0,400):'';}""")
    print("PERSISTED:", MARK in got.lower(), "|", got[:60])
    b.close()

import os, re
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
TARGETS=[
 {"url":BASE+"/upload/6a337ad3b5c5886f33fb4c56&1","guard":"cheese board","mark":"ready to entertain",
  "html":("<p>Acacia Cheese Board &amp; Charcuterie Set - Ready to Entertain</p>"
   "<p>Serve cheese, meats and snacks in style. This acacia wood board with a slate tray and stainless tools makes a beautiful centerpiece for parties, date nights and holidays - and a ready-to-give housewarming or wedding gift.</p>"
   "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
   "<ul><li>Solid acacia wood board with a built-in slate serving tray</li>"
   "<li>Includes stainless cheese knives and serving tools</li>"
   "<li>Great for charcuterie, fruit, crackers, tapas and desserts</li>"
   "<li>Sturdy, reusable and easy to wipe clean</li>"
   "<li>Gift-ready for housewarming, weddings and holidays</li></ul>"
   "<p>Care: hand wash and dry; season the wood occasionally with food-safe oil. Write on the slate with chalk to label cheeses.</p>"
   "<p><strong>WHAT YOU GET:</strong> 1x Acacia Cheese Board with slate tray + stainless knife/tool set. Style may vary by availability.</p>")},
 {"url":BASE+"/upload/6a337ae9886046c14124ac4d&1","guard":"booster","mark":"safe, comfy view",
  "html":("<p>Dog Car Booster Seat - A Safe, Comfy View for Small Dogs</p>"
   "<p>Let your small dog ride up high and happy. The raised booster lifts your pup so they can see out the window, while the included safety tether clips to their harness to keep them secure.</p>"
   "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
   "<ul><li>Raised design lets small dogs see out the window - less anxiety on trips</li>"
   "<li>Built-in safety tether clips to a harness to keep your dog in place</li>"
   "<li>Soft padded walls for a cozy, secure ride</li>"
   "<li>Straps anchor to the seat or center console - quick to install</li>"
   "<li>Removable cover for easy machine washing</li></ul>"
   "<p>For small dogs and puppies - check your pet's weight against the size before use. Always attach the tether to a body harness, not a collar.</p>"
   "<p><strong>WHAT YOU GET:</strong> 1x Dog Car Booster Seat with safety tether and washable cover. Color may vary by availability.</p>")},
]
def tab(pg): return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;}return false;}""")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    summ=[]
    for t in TARGETS:
        pg.goto(t["url"],wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
        cur=pg.locator("input[placeholder='Title']").first.input_value()
        print("\n==",t["guard"],"== title:",cur[:50])
        if t["guard"] not in cur.lower(): print("GUARD FAIL"); summ.append((t["guard"],"GUARD")); continue
        print("desc tab:",tab(pg)); pg.wait_for_timeout(3500)
        print("setData:",pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ck';const ins=Object.values(window.CKEDITOR.instances);if(!ins.length)return 'no-inst';ins[0].setData(h);return 'set';}""",t["html"])); pg.wait_for_timeout(1500)
        try: pg.get_by_role("button",name=re.compile(r"^\s*Save\s*$",re.I)).first.click(timeout=5000); print("save ok")
        except Exception as e: print("save err",type(e).__name__)
        pg.wait_for_timeout(3500)
        pg.goto(t["url"],wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(6000); tab(pg); pg.wait_for_timeout(4000)
        got=pg.evaluate("""()=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return '';const ins=Object.values(window.CKEDITOR.instances);return ins.length?ins[0].getData().slice(0,400):'';}""")
        ok=t["mark"] in got.lower(); print("PERSISTED:",ok); summ.append((t["guard"],"OK" if ok else "NO"))
    print("\n----"); [print(" ",n,s) for n,s in summ]
    b.close()

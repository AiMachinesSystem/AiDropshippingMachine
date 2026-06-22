#!/usr/bin/env python3
"""READ-ONLY: observe how AutoDS edits a product's price. Navigates /products, searches a Ham Maker
eBay item id, opens its edit/detail, and dumps price-related controls/inputs/buttons. NO writes."""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
TARGET="406103214230"  # Ham Maker (sold 5), current sell 41.83
from playwright.sync_api import sync_playwright

def dump(pg,label):
    info=pg.evaluate(r"""() => {
      const num=/\$?\d{1,4}\.\d{2}/;
      const inputs=[...document.querySelectorAll('input')].map(i=>({ph:i.placeholder||'',type:i.type,val:(i.value||'').slice(0,20),cls:(i.className||'').slice(0,30)})).filter(i=>num.test(i.val)||/price|profit|sell|margin|cost/i.test(i.ph+i.cls));
      const btns=[...document.querySelectorAll('button,a,span,div')].map(e=>e.childElementCount<=1?(e.innerText||'').trim():'').filter(t=>/edit|price|profit|save|bulk|update/i.test(t)&&t.length<30);
      const priceTxt=[...document.querySelectorAll('*')].map(e=>e.childElementCount===0?(e.innerText||'').trim():'').filter(t=>/^\$?\d{1,4}\.\d{2}$/.test(t)).slice(0,12);
      return {inputs:inputs.slice(0,12),btns:[...new Set(btns)].slice(0,20),priceTxt:[...new Set(priceTxt)]};
    }""")
    print(f"\n--- {label} ---")
    print("price-ish inputs:",json.dumps(info["inputs"]))
    print("edit/price buttons:",info["btns"])
    print("price texts on page:",info["priceTxt"])

with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1000})
    pg=ctx.new_page()
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks",re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000); pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(5000)
    # search the target item id
    try:
        box=pg.locator("input[placeholder]").first; box.fill(TARGET); box.press("Enter"); pg.wait_for_timeout(4500)
    except Exception as e: print("search fail",e)
    dump(pg,"after search (product row)")
    # try to open an edit affordance on the row
    for name in ["Edit","Bulk Edit","Edit Price","More"]:
        try:
            el=pg.get_by_text(re.compile(r"^\s*"+re.escape(name)+r"\s*$",re.I)).first
            if el.count()>0: el.click(timeout=3500); pg.wait_for_timeout(2500); dump(pg,f"after click '{name}'"); break
        except Exception: continue
    # try clicking a price text (inline edit?)
    try:
        pt=pg.get_by_text(re.compile(r"^\$?\d{1,3}\.\d{2}$")).first
        if pt.count()>0: pt.click(timeout=3000); pg.wait_for_timeout(1500); dump(pg,"after click price text")
    except Exception: pass
    pg.screenshot(path=os.path.join(HERE,"_price_inspect.png"))
    print("\nscreenshot: _price_inspect.png")
    b.close()

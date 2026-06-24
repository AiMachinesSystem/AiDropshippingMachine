#!/usr/bin/env python3
"""Open the Shipping Methods dropdown on the Book Light draft, SCREENSHOT it + dump the open
dropdown's full DOM, so we can read the real option labels and pick the US-domestic service. No save."""
import os, re, json
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
ID="6a36f3e934ccb3112fdcf3a2"; URL=BASE+"/upload/"+ID+"&1"
from playwright.sync_api import sync_playwright
root=HERE
while root and not os.path.isdir(os.path.join(root,"10_OUTPUTS")): root=os.path.dirname(root)
ts=datetime.now().strftime("%Y-%m-%d_%H%M%S")
shotdir=os.path.join(root,"90_CACHE","screenshots","autods"); os.makedirs(shotdir,exist_ok=True)
shot=os.path.join(shotdir,"shipping_dropdown_"+ts+".png")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1100}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    # scroll the shipping area into view + open the dropdown
    opened=pg.evaluate(r"""()=>{
      const items=[...document.querySelectorAll('.ant-select-selection-item,.ant-select-selector')];
      const it=[...document.querySelectorAll('*')].find(e=>/cheapest with tracking/i.test(e.textContent||'') && e.children.length<3);
      if(it){ it.scrollIntoView({block:'center'}); }
      const sel=document.querySelector('.ant-select-selection-item[title*="racking"], .ant-select-selection-item');
      return !!it;
    }""")
    pg.wait_for_timeout(1000)
    # click the selector that shows 'Cheapest with tracking'
    try:
        pg.get_by_text(re.compile(r"^\s*Cheapest with tracking\s*$", re.I)).first.click(timeout=5000)
    except Exception as e:
        print("click via text failed:", str(e)[:80])
    pg.wait_for_timeout(2500)
    pg.screenshot(path=shot, full_page=True)
    # dump any open dropdown / listbox content
    dom=pg.evaluate(r"""()=>{
      const out={};
      const dd=[...document.querySelectorAll('.ant-select-dropdown,[role=listbox],.rc-virtual-list')].filter(e=>!e.className.includes('hidden'));
      out.dropdowns=dd.map(d=>(d.innerText||'').replace(/\n+/g,' | ').slice(0,400));
      out.options=[...document.querySelectorAll('[role=option],.ant-select-item-option-content,.ant-select-item')].map(o=>(o.innerText||'').trim()).filter(Boolean).slice(0,30);
      return out;
    }""")
    print("opened:",opened)
    print("DROPDOWNS:", json.dumps(dom["dropdowns"], ensure_ascii=False))
    print("OPTIONS:", json.dumps(dom["options"], ensure_ascii=False))
    print("SHOT:", shot)
    b.close()

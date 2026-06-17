#!/usr/bin/env python3
"""Apply the optimized description to the duck draft (Description tab -> editor -> Save). Verifies persistence."""
import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
DESC = ("Add some fun to your ride! This cute yellow rubber duck topper turns a boring commute into a smile - "
        "pop it on your car antenna or sit it on your dashboard.\n\n"
        "WHY YOU'LL LOVE IT\n"
        "- Dual use: antenna topper AND dashboard buddy\n"
        "- Find your car fast in a crowded parking lot\n"
        "- Soft, durable rubber - holds up to sun, rain and car washes\n"
        "- Universal fit: flexible base slips onto most standard car antennas\n"
        "- Fun gift for friends, family, new drivers and duck lovers\n\n"
        "WHAT YOU GET: 1x yellow rubber duck topper with helmet + universal base.\n"
        "TIP: warm the base in warm water for a few seconds for a snug fit on thicker antennas.\n"
        "Fast US handling. 30-day returns. Buy with confidence!")
from playwright.sync_api import sync_playwright

def open_duck_desc(pg):
    """click the Description tab inside the duck draft card; return True if found."""
    return pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      if(!inp) return 'no-duck';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){
        el=el.parentElement;
        const tab=[...el.querySelectorAll('*')].find(e=>e.childElementCount<=1 && /^\s*Description\s*$/i.test(e.innerText||''));
        if(tab){ tab.scrollIntoView({block:'center'}); tab.click(); return 'clicked'; }
      }
      return 'no-tab';
    }""")

def read_duck_desc(pg):
    return pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      if(!inp) return '';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){
        el=el.parentElement;
        const ed=el.querySelector("textarea, [contenteditable='true']");
        if(ed) return (ed.value||ed.innerText||'').slice(0,200);
      }
      return '';
    }""")

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    print("open desc tab:", open_duck_desc(pg)); pg.wait_for_timeout(2500)
    # find the editor (textarea or contenteditable) within duck card via Playwright for reliable typing
    handle = pg.evaluate_handle(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      let el=inp;
      for(let k=0;k<16 && el && el.parentElement;k++){ el=el.parentElement;
        const ed=el.querySelector("textarea, [contenteditable='true']"); if(ed) return ed; }
      return null;
    }""")
    info = pg.evaluate("(e)=> e? {tag:e.tagName, ce:e.getAttribute('contenteditable')} : null", handle)
    print("editor:", info)
    if info:
        try:
            handle.as_element().click()
            pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.wait_for_timeout(300)
            pg.keyboard.insert_text(DESC)      # fast, fires input
            pg.wait_for_timeout(800)
        except Exception as e:
            print("type err:", type(e).__name__, e)
    # Save (scoped to duck card)
    res = pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){ el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'saved'; } }
      return 'no-save';
    }""")
    print("save:", res); pg.wait_for_timeout(4000)
    # verify
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2000)
    except Exception: pass
    open_duck_desc(pg); pg.wait_for_timeout(2000)
    got = read_duck_desc(pg)
    print("after reload, desc starts:", got[:80])
    print("PERSISTED:", "rubber duck topper" in got.lower() or "add some fun" in got.lower())
    b.close()

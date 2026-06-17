#!/usr/bin/env python3
"""
Publish ONLY the duck-topper draft to eBay (AutoDS draft -> 'Import' to store).

SAFETY (do not weaken):
- Acts on the DUCK draft ONLY: anchors to the Title input whose value contains 'duck', climbs to its card,
  clicks that card's exact 'Import' button. NEVER clicks 'Import All'. Aborts if the duck card isn't found.
- This is a LIVE publish to eBay store divinit-92-us. Run only under owner GO_PUBLISH.
GO scope: GO_PUBLISH (owner 2026-06-17) — publish the duck topper only.
"""
import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

def drafts_count(pg):
    try:
        m=re.search(r"Drafts\s*\((\d+)\)", pg.locator("body").inner_text(timeout=8000)); return m.group(1) if m else "?"
    except Exception: return "?"

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    before=drafts_count(pg); print("drafts before:", before)
    # confirm duck card + click ITS exact 'Import' (not 'Import All')
    res=pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      if(!inp) return 'no-duck';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){
        el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*import\s*$/i.test(b.innerText||''));  // exact 'Import', excludes 'Import All'
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'clicked:'+inp.value.slice(0,40); }
      }
      return 'no-import-btn';
    }""")
    print("import click:", res)
    if not str(res).startswith("clicked"):
        print("ABORT — duck Import button not found"); b.close(); sys.exit(1)
    pg.wait_for_timeout(2500)
    # confirm any publish dialog
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Publish|Import|Confirm|Yes|Publish to Store)\s*$", re.I))]:
        try: mk().first.click(timeout=4000); print("confirmed dialog"); break
        except Exception: pass
    pg.wait_for_timeout(20000)   # let the publish job run
    # verify
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    after=drafts_count(pg)
    still_duck = pg.evaluate(r"""() => !![...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value))""")
    try: pg.screenshot(path=os.path.join(HERE,"..","..","..","..","..","90_CACHE","screenshots","autods","publish_duck.png"), full_page=False)
    except Exception: pass
    print("drafts after:", after, "| duck still in drafts:", still_duck)
    print("RESULT:", "PUBLISHED (left drafts)" if not still_duck else "CHECK — duck still in drafts (publish may be queued/failed)")
    b.close()

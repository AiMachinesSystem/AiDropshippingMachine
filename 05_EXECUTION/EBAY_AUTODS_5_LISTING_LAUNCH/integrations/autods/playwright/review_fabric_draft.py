#!/usr/bin/env python3
"""READ-ONLY final review of the fabric-shaver draft: title, image presence+position, price/cost/profit/
shipping fields, description (brand check), return/handling, and any 'aparatoo'/brand mentions. No writes."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
URL = BASE + "/upload/6a334d2d85b691259974914b&1"
from playwright.sync_api import sync_playwright


def click_tab(pg, name):
    return pg.evaluate(r"""(nm) => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab],*')].find(x=>x.childElementCount<=1 && new RegExp('^\\s*'+nm+'\\s*$','i').test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""", name)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True); ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1100}); pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    print("URL:", URL)
    print("TITLE:", pg.locator("input[placeholder='Title']").first.input_value())

    # ---- price / cost / profit fields: dump labeled inputs + $ texts
    fields = pg.evaluate(r"""() => {
      const out=[];
      document.querySelectorAll('input').forEach(i=>{const lbl=(i.placeholder||i.getAttribute('aria-label')||i.name||'').trim();
        if(lbl && /price|cost|profit|margin|break|qty|quantity|ship|handling/i.test(lbl)) out.push({lbl, val:i.value});});
      return out;
    }""")
    print("FIELDS:", json.dumps(fields, ensure_ascii=False)[:1200])
    money = pg.evaluate(r"""() => [...new Set([...document.querySelectorAll('*')].map(e=>(e.childElementCount<=1?(e.innerText||''):'').trim()).filter(t=>t && t.length<32 && /(\$\s?\d|profit|break.?even|margin|cost|ROI|shipping|handling|return)/i.test(t)))].slice(0,40)""")
    print("MONEY/LABELS:", json.dumps(money, ensure_ascii=False)[:1400])

    # ---- images
    click_tab(pg, "Images"); pg.wait_for_timeout(3000)
    imgs = pg.evaluate(r"""() => {const a=[...document.querySelectorAll('img')].filter(i=>/autods-scraper-images|cloudfront/i.test(i.src||'')).map(i=>/cloudfront/i.test(i.src)?'MINE':'sup');
      return {order:a, total:a.length, mineIndex:a.indexOf('MINE')};}""")
    print("IMAGES:", json.dumps(imgs))

    # ---- description
    click_tab(pg, "Description"); pg.wait_for_timeout(3000)
    desc = pg.evaluate(r"""()=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return ''; const ins=Object.values(window.CKEDITOR.instances); return ins.length? ins[0].getData():''; }""")
    print("DESC_LEN:", len(desc))
    print("DESC_HEAD:", desc[:200].replace("\n", " "))
    print("DESC_brand_hits:", re.findall(r"aparatoo|brand|trademark|®|™", desc, re.I)[:8])

    # ---- whole-page brand scan
    body = pg.locator("body").inner_text(timeout=8000)
    print("PAGE aparatoo count:", len(re.findall(r"aparatoo", body, re.I)))
    print("RETURN/HANDLING text:", json.dumps([l.strip() for l in body.splitlines() if re.search(r"return|handling|policy|ship", l, re.I) and len(l) < 60][:12], ensure_ascii=False)[:800])
    b.close()

#!/usr/bin/env python3
"""Add the Higgsfield-generated main image to the fabric-shaver draft via the 'Enter Image URL' path,
then report image list + per-image controls so we can set it as main. Then click global Save.
Reversible (draft edit). NEVER publishes. GO scope: owner GO 2026-06-18 (create + replace main image)."""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
URL = BASE + "/upload/6a334d2d85b691259974914b&1"
IMG = "https://d8j0ntlcm91z4.cloudfront.net/user_3F9aGHpa4tAFWgsFLYcg4E0AcOK/hf_20260618_015233_655bf0c8-f59a-4717-bb5a-72933ba00b0f.png"
from playwright.sync_api import sync_playwright


def img_state(pg):
    return pg.evaluate(r"""(needle) => {
      const imgs=[...document.querySelectorAll("img")].filter(i=>/media-amazon|ebayimg|cloudfront|alicdn|ssl-images/i.test(i.src||''));
      return {count:imgs.length, hasNew: imgs.some(i=>(i.src||'').includes(needle)), first:(imgs[0]||{}).src ? imgs[0].src.slice(0,60):null, srcs:imgs.slice(0,8).map(i=>(i.src||'').slice(0,55))};
    }""", IMG.split("/")[-1][:20])


with sync_playwright() as p:
    b = p.chromium.launch(headless=True); ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000}); pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    print("title:", pg.locator("input[placeholder='Title']").first.input_value()[:55])
    pg.evaluate(r"""() => {const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Images\s*$/i.test(x.innerText||'')); if(e)e.click();}""")
    pg.wait_for_timeout(2500)
    print("before:", json.dumps(img_state(pg)))
    pg.evaluate(r"""() => {const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Add Image\s*$/i.test(x.innerText||'')); if(e)e.click();}""")
    pg.wait_for_timeout(1500)
    # fill the URL field
    try:
        box = pg.get_by_placeholder(re.compile(r"Enter Image URL", re.I)).first
        box.wait_for(state="visible", timeout=6000); box.fill(IMG); pg.wait_for_timeout(600)
        print("filled URL field")
    except Exception as e:
        print("URL field err:", type(e).__name__, e)
    # click the confirm/add button near the URL field (scoped, not global Save&Import)
    res = pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll('input')].find(i=>/enter image url/i.test(i.placeholder||''));
      if(!inp) return 'no-url-input';
      let el=inp;
      for(let k=0;k<8 && el.parentElement;k++){ el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*(add|add image|ok|confirm|insert|apply|upload)\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'clicked:'+btn.innerText.trim(); } }
      // fallback: press Enter
      inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true}));
      return 'pressed-enter';
    }""")
    print("add-url action:", res); pg.wait_for_timeout(6000)
    print("after add:", json.dumps(img_state(pg)))
    # report per-image controls (to find 'set as main')
    controls = pg.evaluate(r"""() => {
      const out=[];
      const imgs=[...document.querySelectorAll("img")].filter(i=>/media-amazon|cloudfront|ebayimg/i.test(i.src||''));
      for(const im of imgs.slice(0,6)){ let el=im, found=[];
        for(let k=0;k<5&&el.parentElement;k++){el=el.parentElement;
          [...el.querySelectorAll('button,[role=button],[class*=star i],[class*=main i],[title]')].forEach(x=>{const t=(x.innerText||x.title||x.className||'').trim(); if(t&&t.length<30)found.push(t);});}
        out.push({src:(im.src||'').slice(0,45),ctrls:[...new Set(found)].slice(0,6)});}
      return out;
    }""")
    print("per-image controls:", json.dumps(controls, ensure_ascii=False)[:900])
    # global Save
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); print("Save clicked")
    except Exception as e:
        print("Save err:", type(e).__name__)
    pg.wait_for_timeout(4000)
    # verify after reload
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    pg.evaluate(r"""() => {const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Images\s*$/i.test(x.innerText||'')); if(e)e.click();}""")
    pg.wait_for_timeout(3000)
    print("AFTER RELOAD:", json.dumps(img_state(pg)))
    b.close()

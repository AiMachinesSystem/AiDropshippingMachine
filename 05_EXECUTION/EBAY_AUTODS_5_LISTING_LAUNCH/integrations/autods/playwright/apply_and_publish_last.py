#!/usr/bin/env python3
"""
Optimize (title <=80 + rewritten description, VeRO-safe) the LAST draft on its dedicated page, then publish it.
Single-draft dedicated page (/upload/<id>) = no cross-draft scoping risk (avoids E-002).
Rule enforced: title <=80; description ALWAYS rewritten. Aborts BEFORE publish if either edit fails to persist.
GO scope: owner GO 2026-06-17 ("fallo nell'ultimo prodotto in draft e pubblicizzalo").
"""
import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
URL = BASE + "/upload/69445293348eac207fb05379&1"   # the last draft (mini flat iron)
TITLE = "Mini Flat Iron Hair Straightener Short Hair Bangs Pixie Travel Ceramic Pencil"
DESC = ("Style short hair, bangs and pixie cuts anywhere! This mini ceramic flat iron heats up in seconds "
        "and fits in your bag, purse or carry-on.\n\n"
        "WHY YOU'LL LOVE IT\n"
        "- Heats up fast - ready in about 5 seconds\n"
        "- Slim 0.7 inch ceramic plates - perfect for short hair, bangs, edges and pixie cuts\n"
        "- Negative-ion ceramic for smoother, shinier, frizz-free results\n"
        "- Travel-friendly compact size - fits anywhere\n"
        "- Easy one-button operation\n\n"
        "WHAT YOU GET: 1x mini flat iron hair straightener.\n"
        "TIP: use on dry hair in small sections for the smoothest finish.\n"
        "Fast US handling. 30-day returns. Buy with confidence!")
DESC_HTML = ("<p>Style short hair, bangs and pixie cuts anywhere! This mini ceramic flat iron heats up in seconds and fits in your bag, purse or carry-on.</p>"
  "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
  "<ul><li>Heats up fast - ready in about 5 seconds</li>"
  "<li>Slim 0.7 inch ceramic plates - perfect for short hair, bangs, edges and pixie cuts</li>"
  "<li>Negative-ion ceramic for smoother, shinier, frizz-free results</li>"
  "<li>Travel-friendly compact size - fits anywhere</li>"
  "<li>Easy one-button operation</li></ul>"
  "<p><strong>WHAT YOU GET:</strong> 1x mini flat iron hair straightener.</p>"
  "<p><strong>TIP:</strong> use on dry hair in small sections for the smoothest finish.</p>"
  "<p>Fast US handling. 30-day returns. Buy with confidence!</p>")
assert len(TITLE) <= 80, "TITLE exceeds 80 chars: %d" % len(TITLE)
from playwright.sync_api import sync_playwright

def click_save(pg):
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I))]:
        try: mk().first.click(timeout=5000); return True
        except Exception: pass
    return False

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    ti=pg.locator("input[placeholder='Title']").first
    cur=ti.input_value(); print("draft:", cur[:70], "| len", len(cur))
    if "flat iron" not in cur.lower():
        print("ABORT — not the flat iron draft"); b.close(); sys.exit(1)
    print("new title len:", len(TITLE), "->", TITLE)

    # 1) TITLE
    ti.fill(TITLE); pg.wait_for_timeout(700)
    print("save title:", click_save(pg)); pg.wait_for_timeout(3500)

    # 2) DESCRIPTION (CKEditor inside iframe) -> set via CKEDITOR API
    def click_desc_tab():
        return pg.evaluate(r"""() => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")
    print("desc tab:", click_desc_tab()); pg.wait_for_timeout(3500)
    setres=pg.evaluate("""(html)=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return 'no-ckeditor'; const ins=Object.values(window.CKEDITOR.instances); if(!ins.length) return 'no-instance'; ins[0].setData(html); return 'set:'+ins[0].name; }""", DESC_HTML)
    print("ckeditor setData:", setres); pg.wait_for_timeout(1500)
    print("save desc:", click_save(pg)); pg.wait_for_timeout(3500)

    # verify title persisted
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    title_ok = pg.locator("input[placeholder='Title']").first.input_value()==TITLE
    print("TITLE persisted:", title_ok)
    # verify desc persisted
    pg.evaluate(r"""() => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e)e.click();}""")
    pg.wait_for_timeout(4000)
    got=pg.evaluate("""()=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return ''; const ins=Object.values(window.CKEDITOR.instances); return ins.length? ins[0].getData().slice(0,300):''; }""")
    desc_persisted = "mini ceramic flat iron" in got.lower() or "style short hair" in got.lower()
    print("DESC persisted:", desc_persisted, "| starts:", got[:70])

    if not (title_ok and desc_persisted):
        print("ABORT PUBLISH — title or description did not persist (rule: always rewrite description). No publish.")
        b.close(); sys.exit(2)

    # 3) PUBLISH via 'Save & Import' on this single-draft page (safe: only this draft)
    pub=False
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
               lambda: pg.get_by_text(re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I))]:
        try: mk().first.click(timeout=5000); pub=True; break
        except Exception: pass
    print("Save & Import clicked:", pub); pg.wait_for_timeout(3000)
    # confirm any dialog
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Import|Publish|Confirm|Yes)\s*$", re.I))]:
        try: mk().first.click(timeout=4000); print("confirmed publish dialog"); break
        except Exception: pass
    pg.wait_for_timeout(20000)
    # verify: flat iron left drafts
    pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    still = pg.evaluate(r"""() => !![...document.querySelectorAll("input[placeholder='Title']")].find(i=>/flat iron/i.test(i.value))""")
    dm=re.search(r"Drafts\s*\((\d+)\)", pg.locator("body").inner_text(timeout=8000))
    print("drafts now:", dm.group(1) if dm else "?", "| flat iron still in drafts:", still)
    print("RESULT:", "PUBLISHED (left drafts)" if not still else "CHECK — still in drafts")
    b.close()

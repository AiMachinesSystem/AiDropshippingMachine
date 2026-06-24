#!/usr/bin/env python3
"""Apply NEW SEO title (<=79) + freshly-rewritten VeRO-safe description to the 5 AliExpress-ready drafts.
Each on its dedicated single-draft page (/upload/<id>&1) = no cross-draft scoping risk (E-002).
Title set via the Title input; description set via the CKEditor API (window.CKEDITOR). Verifies persistence.
NO publish here (publish = GO, and account is restricted). GO scope: owner 2026-06-22
'rifai il titolo max 79 + rifai la descrizione con SEO'.
"""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

def html(intro, bullets, whatyouget, closing):
    lis="".join("<li>%s</li>"%b for b in bullets)
    return ("<p>%s</p><p><strong>WHY YOU'LL LOVE IT</strong></p><ul>%s</ul>"
            "<p><strong>WHAT YOU GET:</strong> %s</p><p>%s</p>") % (intro, lis, whatyouget, closing)

DRAFTS = [
 dict(id="6a36f3e934ccb3112fdcf3a2", guard="book light",
   title="Clip On Book Light Rechargeable LED Reading Lamp Dimmable Eye Care Bookmark",
   intro="Read in bed without disturbing anyone. This clip-on book light gives a warm, flicker-free LED glow that is easy on the eyes for late-night reading, e-readers, music stands and laptops.",
   bullets=["Rechargeable USB battery - no disposable cells, hours of reading per charge",
            "3 brightness levels (dimmable) plus adjustable warm/cool tone for eye comfort",
            "Flexible gooseneck bends to aim the light exactly where you want it",
            "Strong clip grips books, e-readers, tablets, headboards and desks",
            "Slim and lightweight - folds flat to pack as a travel reading light"],
   whatyouget="1x clip-on rechargeable LED book light plus USB charging cable.",
   closing="A great gift for readers and students. Fast US handling. 30-day returns."),

 dict(id="6a36f440bdd8f0f8c4fd3f2a", guard="water bottle",
   title="Collapsible Water Bottle Silicone Foldable Leak Proof Travel Gym Sports 20oz",
   intro="Stay hydrated, then roll it up and pack it away. This collapsible silicone water bottle folds flat when empty so it fits a bag, backpack or gym pocket instead of taking up space.",
   bullets=["Food-grade silicone, BPA-free - clean taste with no plastic smell",
            "Leak-proof screw lid with a carry loop and carabiner for travel and hiking",
            "Folds and rolls down to a fraction of its size when empty",
            "Wide mouth for easy filling, drinking and cleaning",
            "Holds about 20 oz (600 ml) - ideal for gym, sports, travel and the office"],
   whatyouget="1x collapsible silicone water bottle with carabiner.",
   closing="Lightweight and reusable. Fast US handling. 30-day returns."),

 dict(id="6a36f4671ea3c3e963fd35fa", guard="squeegee",
   title="Silicone Shower Squeegee Streak Free Glass Door Window Mirror Wiper Bathroom",
   intro="Keep glass spotless in seconds. Wipe down your shower door, mirror, window or tile after each use and stop water spots, soap scum and streaks before they build up.",
   bullets=["Soft silicone blade glides smooth and leaves a streak-free, dry finish",
            "Works on glass shower doors, mirrors, windows, tile and car windshields",
            "Comfortable ergonomic handle with a hanging hole for easy storage",
            "Compact and lightweight - keeps the bathroom cleaner with less effort",
            "A few quick strokes a day means less mold and less scrubbing later"],
   whatyouget="1x silicone shower squeegee with hanging hole.",
   closing="Simple daily cleaning that protects your glass. Fast US handling. 30-day returns."),

 dict(id="6a36f48ebdd8f0f8c4fd3f30", guard="dog water bowl",
   title="No Spill Dog Water Bowl Floating Disk Anti Splash Slow Drink Travel Pet Bowl",
   intro="No more wet floors or soaked car seats. This no-spill dog water bowl uses a floating disk that lets your pet drink freely while blocking splashes and slosh when the bowl moves.",
   bullets=["Floating anti-splash plate keeps water in, even in the car or RV",
            "Helps slow fast drinkers for calmer, tidier drinking",
            "Great for home, travel, crates, road trips and patios",
            "Easy to fill and wipe clean with a sturdy, tip-resistant base",
            "Suitable for small, medium and large dogs and cats"],
   whatyouget="1x no-spill floating pet water bowl.",
   closing="Keep your pet hydrated without the mess. Fast US handling. 30-day returns."),

 dict(id="6a36f4b66b71e506fe2aabd4", guard="thermometer",
   title="Baby Bath Thermometer Floating Waterproof Water Temperature Newborn Safe Toy",
   intro="Check the bath is comfortable before baby goes in. This floating baby bath thermometer gives a clear water-temperature reading so you can avoid water that feels too hot or too cold for newborns and infants.",
   bullets=["Easy-read display floats right in the tub",
            "Waterproof design doubles as a cute floating bath toy",
            "Helps you check a comfortable, consistent temperature every bath",
            "Lightweight with smooth edges - simple to rinse and store",
            "A thoughtful baby-shower and new-parent gift"],
   whatyouget="1x floating baby bath thermometer.",
   closing="Always supervise children during bath time. Fast US handling. 30-day returns."),
]

def click_save(pg):
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception: return False

def click_desc_tab(pg):
    return pg.evaluate(r"""() => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")

def main():
    results=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000})
        for d in DRAFTS:
            assert len(d["title"])<=79, "title>79: "+d["id"]
            url=BASE+"/upload/"+d["id"]+"&1"
            pg=ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
                ti=pg.locator("input[placeholder='Title']").first
                cur=ti.input_value()
                if d["guard"] not in cur.lower():
                    results.append((d["id"], "SKIP guard-mismatch: "+cur[:40])); pg.close(); continue
                # title
                ti.fill(d["title"]); pg.wait_for_timeout(700); click_save(pg); pg.wait_for_timeout(3000)
                # description
                click_desc_tab(pg); pg.wait_for_timeout(3000)
                dh=html(d["intro"], d["bullets"], d["whatyouget"], d["closing"])
                setres=pg.evaluate("""(h)=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return 'no-ck'; const ins=Object.values(window.CKEDITOR.instances); if(!ins.length) return 'no-inst'; ins[0].setData(h); return 'set'; }""", dh)
                pg.wait_for_timeout(1200); click_save(pg); pg.wait_for_timeout(3500)
                # verify
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
                title_ok = pg.locator("input[placeholder='Title']").first.input_value()==d["title"]
                click_desc_tab(pg); pg.wait_for_timeout(3500)
                got=pg.evaluate("""()=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return ''; const ins=Object.values(window.CKEDITOR.instances); return ins.length? ins[0].getData().slice(0,400):''; }""")
                snippet=d["intro"][:25].lower()
                desc_ok = snippet in got.lower()
                results.append((d["id"], "title_ok=%s desc_ok=%s setData=%s | %s"%(title_ok,desc_ok,setres,d["title"][:40])))
            except Exception as e:
                results.append((d["id"], "ERROR "+str(e)[:80]))
            finally:
                pg.close()
        b.close()
    print("="*80)
    for pid,r in results: print("%-26s %s"%(pid,r))

if __name__=="__main__":
    main()

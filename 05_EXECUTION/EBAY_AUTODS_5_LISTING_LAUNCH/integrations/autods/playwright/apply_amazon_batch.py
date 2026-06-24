#!/usr/bin/env python3
"""Apply SEO title (<=79) + fresh VeRO-safe description to the publishable Amazon (US-origin) drafts.
No publish here. GO: owner 100% session GO 2026-06-22."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

def html(intro,bullets,wyg,close):
    lis="".join("<li>%s</li>"%b for b in bullets)
    return ("<p>%s</p><p><strong>WHY YOU'LL LOVE IT</strong></p><ul>%s</ul><p><strong>WHAT YOU GET:</strong> %s</p><p>%s</p>")%(intro,lis,wyg,close)

DRAFTS=[
 dict(id="6a377f6bb9c931bd741d1bfd", guard="trampoline",
   title="Trampoline Spring Pull Tool T Hook Spring Puller Install Removal Steel Handle",
   intro="Install or replace trampoline springs the easy way. This T-handle spring pull tool hooks the spring and gives you the leverage to stretch it onto the frame without pinched fingers.",
   bullets=["Strong T-bar handle for a secure, comfortable grip","Hardened steel hook stretches springs with far less effort","Speeds up trampoline assembly, repair and spring replacement","Works with most standard trampoline springs","Compact - stores easily in the garage or tool box"],
   wyg="1x trampoline spring pull tool.", close="Make spring swaps quick and safe. Fast US handling. 30-day returns."),
 dict(id="6a377b3eb9c931bd741d1bc9", guard="dog car seat cover",
   title="Waterproof Dog Car Seat Cover Hammock Nonslip Back Seat Protector 600D Oxford",
   intro="Protect your back seat from mud, hair and scratches. This waterproof hammock-style dog seat cover shields your upholstery while keeping your pet comfortable and secure on every ride.",
   bullets=["Waterproof 600D Oxford fabric wipes clean in seconds","Hammock design stops dogs sliding into the footwell","Nonslip backing and seat anchors hold it in place","Side flaps add full-door protection against dirt and claws","Adjustable straps fit most cars, trucks and SUVs"],
   wyg="1x waterproof dog car seat cover with straps.", close="Travel clean with your pup. Fast US handling. 30-day returns."),
 dict(id="694452f5e4e5caa0cd9277de", guard="splatter screen",
   title="Splatter Screen for Frying Pan 13 Inch Stainless Steel Grease Guard Mesh Lid",
   intro="Stop grease splatter and keep your stovetop clean. This 13-inch stainless steel splatter screen sits over your frying pan to block popping oil while letting steam escape.",
   bullets=["Fine stainless steel mesh blocks grease, not steam","13 inch fits most large frying pans and skillets","Folding handle for easy storage in a drawer","Resting feet keep the hot screen off your counter","Rinses clean fast and is dishwasher safe"],
   wyg="1x 13 inch stainless steel splatter screen.", close="Cook cleaner with less mess. Fast US handling. 30-day returns."),
 dict(id="6a377af5bdd8f0f8c4fd4523", guard="aerial dog tie out",
   title="Aerial Dog Tie Out Trolley System 60FT Overhead Cable Yard Run for Big Dogs",
   intro="Give your dog room to roam without running off. This 60 ft aerial tie-out trolley runs a cable overhead between two anchor points so your dog can move freely along the yard.",
   bullets=["60 ft overhead cable for a long, safe run","Heavy-duty cable and pulley built for big dogs","Cuts down tangling compared with a ground stake","Great for yards, camping and campsites","Quick to set up between two trees or posts"],
   wyg="1x aerial dog tie-out trolley system.", close="Let your dog roam, safely. Fast US handling. 30-day returns."),
 dict(id="694452ea54270174de9276d1", guard="magnetic microwave",
   title="Microwave Splatter Cover 12 Inch Magnetic Vented Plate Lid Food Guard Clear",
   intro="Keep your microwave clean and your food splatter-free. This 12-inch vented cover sticks to the microwave ceiling with built-in magnets, so it stays up and out of the way between uses.",
   bullets=["Magnetic top holds the cover to the microwave ceiling","12 inch fits most plates and bowls","Steam vents let moisture escape so food stays tender","Food-safe material that is easy to wipe or rinse clean","Collapsible for simple storage"],
   wyg="1x magnetic vented microwave splatter cover.", close="No more wiping the microwave after every meal. Fast US handling. 30-day returns."),
]

def click_save(pg):
    try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception: return False
def desc_tab(pg):
    return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")

def main():
    res=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000})
        for d in DRAFTS:
            assert len(d["title"])<=79, "title>79 %s len=%d"%(d["id"],len(d["title"]))
            url=BASE+"/upload/"+d["id"]+"&1"; pg=ctx.new_page()
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
                ti=pg.locator("input[placeholder='Title']").first; cur=ti.input_value()
                if d["guard"] not in cur.lower(): res.append((d["id"],"SKIP guard: "+cur[:40])); pg.close(); continue
                ti.fill(d["title"]); pg.wait_for_timeout(700); click_save(pg); pg.wait_for_timeout(3000)
                desc_tab(pg); pg.wait_for_timeout(3000)
                dh=html(d["intro"],d["bullets"],d["wyg"],d["close"])
                setr=pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ck';const i=Object.values(window.CKEDITOR.instances);if(!i.length)return 'no-inst';i[0].setData(h);return 'set';}""", dh)
                pg.wait_for_timeout(1200); click_save(pg); pg.wait_for_timeout(3500)
                pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
                tok=pg.locator("input[placeholder='Title']").first.input_value()==d["title"]
                res.append((d["id"],"title_ok=%s set=%s len=%d | %s"%(tok,setr,len(d["title"]),d["title"][:38])))
            except Exception as e: res.append((d["id"],"ERR "+str(e)[:70]))
            finally: pg.close()
        b.close()
    print("="*80)
    for i,r in res: print("%-26s %s"%(i,r))
main()

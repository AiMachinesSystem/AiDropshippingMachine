#!/usr/bin/env python3
"""Apply VeRO-safe descriptions to the 4 batch-2 drafts via dedicated page + CKEditor API. Verifies persistence.
Single-draft page = no cross-draft risk. NEVER publishes. GO scope: owner GO 2026-06-17."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

TARGETS = [
    {"url": BASE + "/upload/6a334d2d85b691259974914b&1", "title_must": "fabric shaver", "marker": "make old clothes",
     "html": ("<p>Electric Fabric Shaver - Make Old Clothes Look New</p>"
              "<p>Bring tired sweaters, blankets and upholstery back to life. The stainless steel blades lift away pills, fuzz and bobbles in seconds without snagging the fabric.</p>"
              "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
              "<ul><li>Sharp multi-blade head removes lint, pills and fuzz fast</li>"
              "<li>Rechargeable - no disposable batteries to buy</li>"
              "<li>Adjustable settings for delicate or thick fabrics</li>"
              "<li>Safe on sweaters, coats, couches, curtains, blankets and car seats</li>"
              "<li>Removable lint bin pops off for easy emptying</li></ul>"
              "<p><strong>WHAT YOU GET:</strong> 1x Electric Fabric Shaver + USB charging cable. Color may vary by availability.</p>")},
    {"url": BASE + "/upload/6a334d6234da1402d029ceeb&1", "title_must": "vacuum", "marker": "crumbs and dust gone",
     "html": ("<p>Mini Desktop Vacuum - Crumbs and Dust Gone in Seconds</p>"
              "<p>Keep your desk, keyboard and car spotless. This pocket-size vacuum sucks up crumbs, eraser shavings, hair and dust that a cloth just pushes around.</p>"
              "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
              "<ul><li>Strong compact suction for keyboards, desks, drawers and car seats</li>"
              "<li>Cordless and rechargeable via USB - grab and go</li>"
              "<li>Nozzle attachments for tight gaps and flat surfaces</li>"
              "<li>Empties in seconds - twist off, tip out, click back</li>"
              "<li>Lightweight and quiet enough for the office or home</li></ul>"
              "<p><strong>WHAT YOU GET:</strong> 1x Mini Desktop Vacuum + USB cable. Color may vary by availability.</p>")},
    {"url": BASE + "/upload/6a334d6d34da1402d029ceec&1", "title_must": "window cleaner", "marker": "wash both sides",
     "html": ("<p>Magnetic Window Cleaner - Wash Both Sides at Once</p>"
              "<p>Clean the outside of your windows from inside the room. Two magnetic halves grip each side of the glass, so you wipe both faces in a single pass - no ladders, no leaning out.</p>"
              "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
              "<ul><li>Cleans inside and outside of the glass at the same time</li>"
              "<li>Adjustable magnets hold firmly through the pane</li>"
              "<li>Safety cord prevents drops on upper floors</li>"
              "<li>Sponge pads scrub and dry without streaks</li>"
              "<li>Great for high windows, sliding doors and conservatories</li></ul>"
              "<p><strong>IMPORTANT:</strong> check your glass thickness before use - this model adjusts for single and double glazing within the stated range. Measure first for a firm grip.</p>"
              "<p><strong>WHAT YOU GET:</strong> 1x Magnetic Window Cleaner with pads and safety cord.</p>")},
    {"url": BASE + "/upload/6a334d89d0e2355068947f67&1", "title_must": "closet light", "marker": "instant light, no wiring",
     "html": ("<p>Motion Sensor Closet Light - Instant Light, No Wiring</p>"
              "<p>Light up closets, cabinets, stairs and hallways the moment you walk by. Stick it anywhere - no tools, no electrician, no batteries to replace.</p>"
              "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
              "<ul><li>Built-in motion sensor turns on automatically in the dark and off after you leave</li>"
              "<li>USB rechargeable - no disposable batteries</li>"
              "<li>Stick-on magnetic mount - peel, place, done</li>"
              "<li>Soft, even light that won't dazzle at night</li>"
              "<li>Perfect for closets, wardrobes, cabinets, stairs, hallways and pantries</li></ul>"
              "<p><strong>WHAT YOU GET:</strong> Rechargeable Motion Sensor LED light(s) + magnetic strip + USB cable. Pack size and color may vary by availability.</p>")},
]


def click_save(pg):
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception:
        return False


def click_desc_tab(pg):
    return pg.evaluate(r"""() => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")


def set_ck(pg, html):
    return pg.evaluate("""(html)=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return 'no-ckeditor'; const ins=Object.values(window.CKEDITOR.instances); if(!ins.length) return 'no-instance'; ins[0].setData(html); return 'set'; }""", html)


def get_ck(pg):
    return pg.evaluate("""()=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return ''; const ins=Object.values(window.CKEDITOR.instances); return ins.length? ins[0].getData().slice(0,400):''; }""")


def main():
    summary = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        for t in TARGETS:
            pg.goto(t["url"], wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            cur = pg.locator("input[placeholder='Title']").first.input_value()
            print("\n== %s == title: %s" % (t["title_must"], cur[:60]))
            if t["title_must"] not in cur.lower():
                print(" ABORT guard"); summary.append((t["title_must"], "GUARD-FAIL")); continue
            print(" desc tab:", click_desc_tab(pg)); pg.wait_for_timeout(3500)
            print(" setData:", set_ck(pg, t["html"])); pg.wait_for_timeout(1500)
            print(" save:", click_save(pg)); pg.wait_for_timeout(3500)
            pg.goto(t["url"], wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
            click_desc_tab(pg); pg.wait_for_timeout(4000)
            got = get_ck(pg)
            ok = t["marker"] in got.lower()
            print(" PERSISTED:", ok, "|", got[:60])
            summary.append((t["title_must"], "OK" if ok else "NOT-PERSISTED"))
        b.close()
    print("\n" + "-" * 50)
    for n, s in summary:
        print(" %-16s %s" % (n, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Apply rewritten VeRO-safe DESCRIPTIONS to the 3 new drafts via their DEDICATED page (/upload/<id>)
using the CKEditor API (window.CKEDITOR.instances[0].setData). Single-draft page = no cross-draft risk (E-002).
Verifies title (safety guard) + description persistence. NEVER publishes. GO scope: owner GO 2026-06-17."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

TARGETS = [
    {
        "url": BASE + "/upload/6a33452c55f86e413f55b55d&1",
        "title_must": "slow feeder",
        "marker": "healthier mealtimes",
        "html": ("<p>Slow Feeder Dog Bowl - Healthier Mealtimes, Less Mess</p>"
                 "<p>Help your pet eat at a calmer pace. The raised silicone maze turns fast gulping into a fun puzzle, "
                 "which can help reduce bloating, choking, and vomiting caused by eating too quickly.</p>"
                 "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
                 "<ul><li>Food-grade silicone, soft on gums and easy to clean</li>"
                 "<li>Suction cups on the base keep the bowl in place - no sliding, no spills</li>"
                 "<li>Maze design slows eating and adds light mental enrichment at every meal</li>"
                 "<li>Suitable for small to medium dogs and cats; works with dry, wet, or raw food</li>"
                 "<li>Dishwasher friendly - rinse or place on the top rack</li></ul>"
                 "<p><strong>WHAT YOU GET:</strong> 1x Slow Feeder Bowl. Color/pattern may vary by availability.</p>"),
    },
    {
        "url": BASE + "/upload/6a334546c81e314488748fef&1",
        "title_must": "coffee pod",
        "marker": "tidy counter",
        "html": ("<p>Coffee Pod Holder - Tidy Counter, Coffee Within Reach</p>"
                 "<p>Keep your coffee station neat with a compact countertop holder that stores your pods upright and "
                 "ready to grab. The sturdy metal frame and solid wood base add a clean, modern look to any kitchen, "
                 "bar, or office desk.</p>"
                 "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
                 "<ul><li>Holds standard single-serve coffee pods in an easy-access basket</li>"
                 "<li>Solid wood base + powder-coated metal frame for a stable, premium feel</li>"
                 "<li>Space-saving footprint fits on a counter, shelf, or breakroom table</li>"
                 "<li>Open design lets you see and reach every pod at a glance</li>"
                 "<li>Simple to assemble; wipe clean with a dry cloth</li></ul>"
                 "<p>Note: compatible with common single-serve pods. Pods and machine shown are not included.</p>"
                 "<p><strong>WHAT YOU GET:</strong> 1x Coffee Pod Holder.</p>"),
    },
    {
        "url": BASE + "/upload/6a334560d49bc5e7ee527b13&1",
        "title_must": "neck fan",
        "marker": "cool air wherever",
        "html": ("<p>Hands-Free Neck Fan - Cool Air Wherever You Go</p>"
                 "<p>Stay comfortable on hot days without holding anything. This wearable neck fan rests around your neck "
                 "and pushes a steady stream of air, leaving your hands completely free for work, travel, walking, or chores.</p>"
                 "<p><strong>WHY YOU'LL LOVE IT</strong></p>"
                 "<ul><li>Bladeless, hands-free design - safe around hair, comfortable for long wear</li>"
                 "<li>360 degree airflow cools the neck and face from multiple outlets</li>"
                 "<li>3 adjustable speeds to match a breeze or a stronger blast</li>"
                 "<li>Rechargeable 4000mAh battery with USB charging - no disposable batteries</li>"
                 "<li>Lightweight and quiet enough for the office, commute, or outdoors</li></ul>"
                 "<p><strong>WHAT YOU GET:</strong> 1x Portable Neck Fan + USB charging cable. Color may vary by availability.</p>"),
    },
]


def click_save(pg):
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); return True
    except Exception:
        return False


def click_desc_tab(pg):
    return pg.evaluate(r"""() => {const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;} return false;}""")


def set_ck(pg, html):
    return pg.evaluate("""(html)=>{ if(!window.CKEDITOR||!window.CKEDITOR.instances) return 'no-ckeditor'; const ins=Object.values(window.CKEDITOR.instances); if(!ins.length) return 'no-instance'; ins[0].setData(html); return 'set:'+ins[0].name; }""", html)


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
            print("\n== %s ==\n draft title: %s" % (t["title_must"], cur[:70]))
            if t["title_must"] not in cur.lower():
                print(" ABORT — title guard failed (wrong draft)"); summary.append((t["title_must"], "GUARD-FAIL")); continue
            print(" desc tab:", click_desc_tab(pg)); pg.wait_for_timeout(3500)
            print(" ckeditor setData:", set_ck(pg, t["html"])); pg.wait_for_timeout(1500)
            print(" save desc:", click_save(pg)); pg.wait_for_timeout(3500)
            # verify after reload
            pg.goto(t["url"], wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
            click_desc_tab(pg); pg.wait_for_timeout(4000)
            got = get_ck(pg)
            ok = t["marker"] in got.lower()
            print(" DESC persisted:", ok, "| starts:", got[:70])
            summary.append((t["title_must"], "OK" if ok else "NOT-PERSISTED"))
        b.close()
    print("\n" + "-" * 50)
    for name, st in summary:
        print(" %-14s %s" % (name, st))
    return 0


if __name__ == "__main__":
    sys.exit(main())

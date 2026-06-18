#!/usr/bin/env python3
"""Attempt to apply VeRO-safe DESCRIPTIONS to the 3 new drafts (Description tab -> editor -> Save).
Matches each draft by a keyword in its (already-optimized) title. Verifies persistence after reload.
Reversible (draft edit). NEVER publishes. GO scope: owner GO 2026-06-17.
Known risk: AutoDS 'Simple page' rich-editor previously resisted automation (manual paste fallback)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

TARGETS = [
    (r"slow feeder",
     "Slow Feeder Dog Bowl - Healthier Mealtimes, Less Mess\n\n"
     "Help your pet eat at a calmer pace. The raised silicone maze turns fast gulping into a fun puzzle, "
     "which can help reduce bloating, choking, and vomiting caused by eating too quickly.\n\n"
     "- Food-grade silicone, soft on gums and easy to clean\n"
     "- Suction cups on the base keep the bowl in place - no sliding, no spills\n"
     "- Maze design slows eating and adds light mental enrichment at every meal\n"
     "- Suitable for small to medium dogs and cats; works with dry, wet, or raw food\n"
     "- Dishwasher friendly - rinse or place on the top rack\n\n"
     "What you get: 1x Slow Feeder Bowl. Color/pattern may vary by availability."),
    (r"coffee pod",
     "Coffee Pod Holder - Tidy Counter, Coffee Within Reach\n\n"
     "Keep your coffee station neat with a compact countertop holder that stores your pods upright and "
     "ready to grab. The sturdy metal frame and solid wood base add a clean, modern look to any kitchen, "
     "bar, or office desk.\n\n"
     "- Holds standard single-serve coffee pods in an easy-access basket\n"
     "- Solid wood base + powder-coated metal frame for a stable, premium feel\n"
     "- Space-saving footprint fits on a counter, shelf, or breakroom table\n"
     "- Open design lets you see and reach every pod at a glance\n"
     "- Simple to assemble; wipe clean with a dry cloth\n\n"
     "Note: compatible with common single-serve pods. Pods and machine shown are not included.\n\n"
     "What you get: 1x Coffee Pod Holder."),
    (r"neck fan",
     "Hands-Free Neck Fan - Cool Air Wherever You Go\n\n"
     "Stay comfortable on hot days without holding anything. This wearable neck fan rests around your neck "
     "and pushes a steady stream of air, leaving your hands completely free for work, travel, walking, or chores.\n\n"
     "- Bladeless, hands-free design - safe around hair, comfortable for long wear\n"
     "- 360 degree airflow cools the neck and face from multiple outlets\n"
     "- 3 adjustable speeds to match a breeze or a stronger blast\n"
     "- Rechargeable 4000mAh battery with USB charging - no disposable batteries\n"
     "- Lightweight and quiet enough for the office, commute, or outdoors\n\n"
     "What you get: 1x Portable Neck Fan + USB charging cable. Color may vary by availability."),
]

JS_FIND = r"""(pat) => {
  const re=new RegExp(pat,'i');
  const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>re.test(i.value));
  if(!inp) return null;
  return inp;
}"""


def expand_all(pg):
    try:
        pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception:
        pass


def open_desc(pg, pat):
    return pg.evaluate(r"""(pat) => {
      const re=new RegExp(pat,'i');
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>re.test(i.value));
      if(!inp) return 'no-match';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){ el=el.parentElement;
        const tab=[...el.querySelectorAll('*')].find(e=>e.childElementCount<=1 && /^\s*Description\s*$/i.test(e.innerText||''));
        if(tab){ tab.scrollIntoView({block:'center'}); tab.click(); return 'clicked'; } }
      return 'no-tab';
    }""", pat)


def get_editor(pg, pat):
    return pg.evaluate_handle(r"""(pat) => {
      const re=new RegExp(pat,'i');
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>re.test(i.value));
      let el=inp;
      for(let k=0;k<16 && el && el.parentElement;k++){ el=el.parentElement;
        const ed=el.querySelector("textarea, [contenteditable='true']"); if(ed) return ed; }
      return null;
    }""", pat)


def save_scoped(pg, pat):
    return pg.evaluate(r"""(pat) => {
      const re=new RegExp(pat,'i');
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>re.test(i.value));
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){ el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'saved'; } }
      return 'no-save';
    }""", pat)


def read_desc(pg, pat):
    return pg.evaluate(r"""(pat) => {
      const re=new RegExp(pat,'i');
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>re.test(i.value));
      if(!inp) return '';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){ el=el.parentElement;
        const ed=el.querySelector("textarea, [contenteditable='true']"); if(ed) return (ed.value||ed.innerText||'').slice(0,300); }
      return '';
    }""", pat)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        for pat, desc in TARGETS:
            pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            expand_all(pg)
            print("[%s] open desc:" % pat, open_desc(pg, pat)); pg.wait_for_timeout(2500)
            handle = get_editor(pg, pat)
            info = pg.evaluate("(e)=> e? {tag:e.tagName, ce:e.getAttribute('contenteditable')} : null", handle)
            print("   editor:", info)
            if info:
                try:
                    handle.as_element().click()
                    pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.wait_for_timeout(300)
                    pg.keyboard.insert_text(desc); pg.wait_for_timeout(800)
                except Exception as e:
                    print("   type err:", type(e).__name__, e)
            print("   save:", save_scoped(pg, pat)); pg.wait_for_timeout(4000)
        # verify
        print("-" * 60); print("VERIFY after reload:")
        for pat, desc in TARGETS:
            pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            expand_all(pg)
            open_desc(pg, pat); pg.wait_for_timeout(2000)
            got = read_desc(pg, pat)
            marker = desc.split("\n")[0][:25].lower()
            ok = marker in got.lower()
            print("   PERSISTED=%s [%s] starts: %s" % (ok, pat, got[:60]))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

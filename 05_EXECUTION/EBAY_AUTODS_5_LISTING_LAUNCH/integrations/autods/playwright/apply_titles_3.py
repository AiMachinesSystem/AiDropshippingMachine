#!/usr/bin/env python3
"""Apply optimized, VeRO-safe TITLES (<=80) to the 3 newly imported DRAFTS.
Each target is matched by a distinctive keyword in its current (scraped) title, then the title input
is filled and the SAVE button scoped to that draft card is clicked. Verifies persistence after reload.
Reversible (draft edit). NEVER publishes. GO scope: owner GO 2026-06-17 to import 3 drafts with edited titles.
Usage: apply_titles_3.py            # apply + verify
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

# (match_regex on current title, new_title <=80). Order = distinctive first.
TARGETS = [
    (r"slow\s*feeder",                 "Slow Feeder Dog Bowl Silicone Puzzle Mat Anti-Choke Non-Slip Suction Cup Pet Cat"),
    (r"coffee\s*pod|k\s*cup|kcup",     "Coffee Pod Holder Organizer Countertop Storage Basket Wood Base Kitchen Display"),
    (r"neck\s*fan",                    "Portable Neck Fan Bladeless Hands Free 360 Cooling Rechargeable 4000mAh 3-Speed"),
]


def expand_all(pg):
    try:
        pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception:
        pass


def find_title_input(pg, pat, new_title):
    inputs = pg.locator("input[placeholder='Title']")
    for i in range(inputs.count()):
        try:
            v = inputs.nth(i).input_value()
        except Exception:
            continue
        if v == new_title:
            return None, "ALREADY"   # already applied
        if re.search(pat, v, re.I):
            return inputs.nth(i), v
    return None, None


def save_scoped(pg, new_title):
    return pg.evaluate(r"""(nt) => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value===nt);
      if(!inp) return 'no-input-after-fill';
      let el=inp;
      for(let k=0;k<14 && el.parentElement;k++){
        el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'saved'; }
      }
      return 'no-save-found';
    }""", new_title)


def main():
    results = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        for pat, new_title in TARGETS:
            pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            expand_all(pg)
            fld, cur = find_title_input(pg, pat, new_title)
            if cur == "ALREADY":
                print("[skip] already applied: %s" % new_title[:50]); results.append((pat, "ALREADY")); continue
            if not fld:
                print("[MISS] no draft matches /%s/" % pat); results.append((pat, "MISS")); continue
            print("[match] /%s/ current: %s" % (pat, (cur or "")[:70]))
            fld.scroll_into_view_if_needed(timeout=4000)
            fld.fill(new_title); pg.wait_for_timeout(800)
            res = save_scoped(pg, new_title)
            print("   save -> %s | new: %s" % (res, new_title[:60]))
            pg.wait_for_timeout(4000)
            results.append((pat, res))
        # verify pass
        print("-" * 60); print("VERIFY after reload:")
        pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        expand_all(pg)
        all_titles = []
        inputs = pg.locator("input[placeholder='Title']")
        for i in range(inputs.count()):
            try:
                all_titles.append(inputs.nth(i).input_value())
            except Exception:
                pass
        for pat, new_title in TARGETS:
            ok = new_title in all_titles
            print("   PERSISTED=%s  %s" % (ok, new_title[:60]))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

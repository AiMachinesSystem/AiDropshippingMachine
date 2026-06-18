#!/usr/bin/env python3
"""Apply optimized <=80 titles to the 4 batch-2 drafts, matched by a keyword in the scraped title.
Fill + scoped Save + verify persistence. Reversible. NEVER publishes. GO scope: owner GO 2026-06-17."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

TARGETS = [
    (r"fabric shaver|lint remover",          "Electric Fabric Shaver Rechargeable Lint Remover Sweater Pill Fuzz Defuzzer"),
    (r"vacuum",                              "Mini Desktop Vacuum Cleaner Cordless USB Rechargeable Keyboard Car Crumb Duster"),
    (r"window cleaner|magnetic window",      "Magnetic Window Cleaner Double Sided Glass Wiper Brush High Rise Home Squeegee"),
    (r"motion sensor|closet light",          "Motion Sensor LED Closet Light Rechargeable Wireless Under Cabinet Stick On"),
]
for _p, _t in TARGETS:
    assert len(_t) <= 80, "title too long (%d): %s" % (len(_t), _t)


def expand_all(pg):
    try:
        pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception:
        pass


def find_input(pg, pat, new_title):
    inputs = pg.locator("input[placeholder='Title']")
    for i in range(inputs.count()):
        try:
            v = inputs.nth(i).input_value()
        except Exception:
            continue
        if v == new_title:
            return None, "ALREADY"
        if re.search(pat, v, re.I):
            return inputs.nth(i), v
    return None, None


def save_scoped(pg, new_title):
    return pg.evaluate(r"""(nt) => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value===nt);
      if(!inp) return 'no-input';
      let el=inp;
      for(let k=0;k<14 && el.parentElement;k++){ el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'saved'; } }
      return 'no-save';
    }""", new_title)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        for pat, new_title in TARGETS:
            pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            expand_all(pg)
            fld, cur = find_input(pg, pat, new_title)
            if cur == "ALREADY":
                print("[skip] already:", new_title[:45]); continue
            if not fld:
                print("[MISS] /%s/" % pat); continue
            print("[match] /%s/ <- %s" % (pat, (cur or "")[:55]))
            fld.scroll_into_view_if_needed(timeout=4000); fld.fill(new_title); pg.wait_for_timeout(800)
            print("   save:", save_scoped(pg, new_title), "->", new_title[:55]); pg.wait_for_timeout(4000)
        # verify
        print("-" * 55, "\nVERIFY:")
        pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        expand_all(pg)
        titles = []
        inputs = pg.locator("input[placeholder='Title']")
        for i in range(inputs.count()):
            try:
                titles.append(inputs.nth(i).input_value())
            except Exception:
                pass
        for _pat, t in TARGETS:
            print("   PERSISTED=%s %s" % (t in titles, t[:55]))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

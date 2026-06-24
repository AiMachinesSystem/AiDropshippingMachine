#!/usr/bin/env python3
"""READ-ONLY: open Bulk Edit on ONE product, click the Price tab (and Profit tab), and dump the exact
controls inside (option labels, radio choices, numeric inputs, any 'increase by %'/percentage affordance).
NO submit, NO save — observe, screenshot, then Cancel. Determines the durable +2% mechanism under price-monitoring."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright


def dump_panel(pg, label):
    info = pg.evaluate(r"""() => {
      const dlg=document.querySelector('.ant-modal, [role=dialog]')||document.body;
      const txt=(dlg.innerText||'').replace(/\s+/g,' ');
      const labels=[...dlg.querySelectorAll('label,.ant-radio-wrapper,.ant-checkbox-wrapper,button,.ant-select-selection-item,.ant-segmented-item,option')]
          .map(e=>(e.innerText||'').trim()).filter(t=>t&&t.length<48);
      const inputs=[...dlg.querySelectorAll('input,select')].map(i=>({ph:i.placeholder||'',type:i.type||i.tagName,val:(i.value||'').slice(0,18)}));
      const pct=/%|percent|increase|decrease|markup|raise/i.test(txt);
      return {labels:[...new Set(labels)].slice(0,40), inputs:inputs.slice(0,25), pctMention:pct, text:txt.slice(0,800)};
    }""")
    print("\n--- %s ---" % label)
    print("labels:", info["labels"])
    print("inputs:", json.dumps(info["inputs"]))
    print("percentage/increase mention:", info["pctMention"])
    print("text:", info["text"][:500])


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(storage_state=STATE, viewport={"width": 1500, "height": 1000})
    pg = ctx.new_page()
    pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks", re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000); pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
    # tick the first real product row
    try:
        pg.locator("input.ant-checkbox-input").nth(1).check(timeout=4000); pg.wait_for_timeout(1000)
    except Exception as e:
        print("tick fail", type(e).__name__)
    try:
        pg.get_by_text(re.compile(r"^\s*Bulk Edit\s*$", re.I)).first.click(timeout=5000); pg.wait_for_timeout(2500)
        print("Bulk Edit opened")
    except Exception as e:
        print("bulk edit fail", type(e).__name__); b.close(); raise SystemExit(1)
    dump_panel(pg, "modal root")
    # click Price tab/option
    for name in ["Price", "Profit"]:
        try:
            el = pg.get_by_text(re.compile(r"^\s*" + name + r"\s*$", re.I)).last
            el.click(timeout=4000); pg.wait_for_timeout(1800)
            dump_panel(pg, "after click '%s'" % name)
            pg.screenshot(path=os.path.join(HERE, "_price_tab_%s.png" % name.lower()))
        except Exception as e:
            print("click %s fail:" % name, type(e).__name__)
    # SAFETY: cancel, never update
    try: pg.get_by_role("button", name=re.compile(r"^\s*Cancel\s*$", re.I)).first.click(timeout=4000)
    except Exception: pass
    print("\n[SAFETY] Cancelled — nothing written.")
    b.close()

#!/usr/bin/env python3
"""READ-ONLY: discover the dedicated-page id for each draft, mapped to its current title.
Looks for anchors/elements whose href or data contains an /upload/<id> reference, and also captures
the products API JSON to extract draft ids. Prints (id, title) pairs. No writes."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

api_bodies = []

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        pg.on("response", lambda r: api_bodies.append(r) if ("autods.com" in r.url and "product" in r.url.lower()) else None)
        pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
        try:
            pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
        except Exception:
            pass
        # 1) anchors containing /upload/
        links = pg.eval_on_selector_all("a[href*='/upload/']", "els=>els.map(e=>e.href)")
        print("ANCHORS /upload/:", json.dumps(links, indent=2)[:1500])
        # 2) any element with data attribute id near title inputs
        pairs = pg.evaluate(r"""() => {
          const out=[];
          const inputs=[...document.querySelectorAll("input[placeholder='Title']")];
          for(const inp of inputs){
            let el=inp, found=null;
            for(let k=0;k<18 && el.parentElement;k++){ el=el.parentElement;
              const a=el.querySelector("a[href*='/upload/']");
              if(a){ found=a.getAttribute('href'); break; }
              // data-* ids
              for(const at of el.attributes||[]){ if(/id/i.test(at.name) && /[0-9a-f]{16,}/i.test(at.value)){ found='data:'+at.value; break; } }
              if(found) break;
            }
            out.push({title: inp.value.slice(0,45), ref: found});
          }
          return out;
        }""")
        print("TITLE->REF map:")
        for pr in pairs:
            print("   %-46s %s" % (pr["title"], pr["ref"]))
        # 3) read products API JSON for ids
        print("-" * 50, "\nAPI product responses:", len(api_bodies))
        for r in api_bodies[-6:]:
            try:
                if "application/json" in (r.headers or {}).get("content-type", ""):
                    body = r.text()
                    ids = re.findall(r'"id"\s*:\s*"?([0-9a-f]{16,})"?', body)
                    titles = re.findall(r'"title"\s*:\s*"([^"]{5,60})"', body)
                    if ids:
                        print("  ", r.url.split("?")[0], "ids:", ids[:6], "titles:", titles[:4])
            except Exception:
                pass
        b.close()


if __name__ == "__main__":
    main()

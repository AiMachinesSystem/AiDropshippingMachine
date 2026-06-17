#!/usr/bin/env python3
"""
AutoDS LISTING AUDIT (read-only): tally the active products by status/error/OOS, and re-read the drafts
for VeRO/brand flags. Reuses storage_state.json. Paginates the products list capturing the SPA's own
products/<store>/list/ API (status + error_list + stock fields). NO writes — navigation/scroll/pagination
clicks + dismiss-upsell only (read queries; mutate nothing).
GO scope: GO_AUTODS_READ_SESSION (read-only).
"""
import os, re, sys, json, collections
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"


def find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        p = os.path.dirname(cur)
        if p == cur:
            return None
        cur = p


def main():
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE) or HERE
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "audit_" + ts)
    shots = os.path.join(root, "90_CACHE", "screenshots", "autods", "audit_" + ts)
    os.makedirs(cache, exist_ok=True)
    os.makedirs(shots, exist_ok=True)

    list_items = {}   # _id/item_id -> item (dedup)
    raw = []

    def on_response(resp):
        try:
            u = resp.url
            if "autods.com" not in u or "application/json" not in (resp.headers or {}).get("content-type", ""):
                return
            if "/products/" in u and "/list" in u:
                data = json.loads(resp.text())
                items = data.get("results") or data.get("items") or (data if isinstance(data, list) else [])
                for it in (items or []):
                    k = it.get("id") or it.get("_id") or it.get("item_id_on_site") or str(len(list_items))
                    list_items[k] = it
                raw.append({"url": u, "n": len(items or [])})
        except Exception:
            pass

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("response", on_response)

        # products list (dismiss upsell first)
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4500)
        if "offer" in page.url:
            for mk in [lambda: page.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                       lambda: page.get_by_text(re.compile(r"No Thanks", re.I))]:
                try:
                    mk().first.click(timeout=5000); break
                except Exception:
                    continue
            page.wait_for_timeout(3500)
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)

        # paginate via Ant Design "next" button until disabled (cap 18 clicks)
        for i in range(18):
            nxt = page.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
            if nxt.count() == 0:
                break
            try:
                nxt.first.scroll_into_view_if_needed(timeout=3000)
                nxt.first.click(timeout=4000)
            except Exception:
                break
            page.wait_for_timeout(2400)
            if len(list_items) >= 214:
                break
        try:
            page.screenshot(path=os.path.join(shots, "products_last_page.png"), full_page=False)
        except Exception:
            pass

        # drafts (/upload) — read all 11 for VeRO/brand flags
        page.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        try:
            for _ in range(4):
                page.mouse.wheel(0, 3000); page.wait_for_timeout(1200)
        except Exception:
            pass
        try:
            drafts_txt = page.locator("body").inner_text(timeout=8000)
        except Exception:
            drafts_txt = ""
        with open(os.path.join(cache, "drafts_full.txt"), "w", encoding="utf-8") as fh:
            fh.write(drafts_txt[:30000])
        try:
            page.screenshot(path=os.path.join(shots, "drafts.png"), full_page=True)
        except Exception:
            pass
        b.close()

    items = list(list_items.values())
    json.dump(items, open(os.path.join(cache, "_products_list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("AUDIT run:", ts)
    print("captured list pages:", len(raw), "| unique products tallied:", len(items), "(target 214)")
    if items:
        print("top-level item keys:", sorted(items[0].keys())[:50])
        status = collections.Counter(it.get("status") for it in items)
        print("status distribution:", dict(status))
        with_err = [it for it in items if it.get("error_list")]
        print("products WITH error_list:", len(with_err))
        # error type/message tally
        etypes = collections.Counter()
        for it in with_err:
            for e in (it.get("error_list") or []):
                etypes[e.get("error_type")] += 1
        print("error_type distribution:", dict(etypes))
        # look for any stock/oos-ish field
        oos_fields = [k for k in items[0].keys() if re.search(r"stock|oos|avail|quant", k, re.I)]
        print("possible stock fields:", oos_fields)
        # VeRO/brand scan in titles
        BRANDS = ["disney","nike","apple","invisalign","tuya","airtag","samsung","lululemon","adidas","vera bradley","amazon basics"]
        vero = []
        for it in items:
            t = (it.get("title") or "").lower()
            hits = [bvar for bvar in BRANDS if bvar in t]
            if hits:
                vero.append((it.get("title","")[:50], hits))
        print("active listings with brand-term in title:", len(vero))
        for t, h in vero[:15]:
            print("   ", h, t)
    # drafts VeRO scan
    if os.path.exists(os.path.join(cache, "drafts_full.txt")):
        dtxt = open(os.path.join(cache, "drafts_full.txt"), encoding="utf-8").read().lower()
        print("\nDRAFTS scan:")
        print("  'vero' mentions:", dtxt.count("vero"))
        print("  'alcohol' mentions:", dtxt.count("alcohol"))
        for b in ["disney","nike","apple","invisalign","tuya","airtag"]:
            if b in dtxt:
                print("  brand term in drafts:", b)
    print("CACHE:", cache)
    return 0


if __name__ == "__main__":
    sys.exit(main())

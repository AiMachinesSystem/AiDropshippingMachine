#!/usr/bin/env python3
"""
reprice_all_dryrun.py — READ-ONLY dry-run for the owner intent "renew all listings, +2% price".

Pulls every live listing (paginating the /products/<store>/list/ API, like audit_listings.py), reads the
current sell price (variation_statistics.min_sell_price) and computes the proposed +PCT price. Reports the
full old->new table + totals. WRITES NOTHING.

WHY DRY-RUN ONLY (and --confirm is hard-blocked): a +2% change across the whole live store is a GO-CLASS
action (live eBay prices). There is also no verified bulk price-WRITE mechanism yet (reprice_one.py only
observed the Bulk-Edit price panel and cancelled — never confirmed a write), and AutoDS price-monitoring
(`configuration.disable_price_monitoring`) may auto-overwrite a manual price. Executing live needs: (1) a
separate owner GO, (2) the write mechanism cracked + cold-tested on ONE listing, (3) a decision on
price-monitoring, and clarification of "rinnuova" (renew/relist vs reprice only).

GO scope: GO_AUTODS_READ_SESSION (read-only). Run with PYTHONIOENCODING=utf-8 on Windows.
Usage: reprice_all_dryrun.py [--pct 2] [--confirm(blocked)]
"""
import os, re, sys, json, argparse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"


def find_repo_root(start):
    cur = os.path.abspath(start)
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        cur = os.path.dirname(cur)
    return start


def pull_listings():
    from playwright.sync_api import sync_playwright
    items = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()

        def on_response(resp):
            try:
                u = resp.url
                if "autods.com" not in u or "application/json" not in (resp.headers or {}).get("content-type", ""):
                    return
                if "/products/" in u and "/list" in u:
                    data = json.loads(resp.text())
                    for it in (data.get("results") or []):
                        k = it.get("id") or it.get("_id")
                        if k:
                            items[k] = it
            except Exception:
                pass

        page.on("response", on_response)
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4500)
        if "offer" in page.url:
            for mk in [lambda: page.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                       lambda: page.get_by_text(re.compile(r"No Thanks", re.I))]:
                try:
                    mk().first.click(timeout=5000); break
                except Exception:
                    continue
            page.wait_for_timeout(3000)
            page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        for i in range(20):
            nxt = page.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
            if nxt.count() == 0:
                break
            try:
                nxt.first.scroll_into_view_if_needed(timeout=3000)
                nxt.first.click(timeout=4000)
            except Exception:
                break
            page.wait_for_timeout(2300)
        b.close()
    return list(items.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pct", type=float, default=2.0, help="percent increase (default 2)")
    ap.add_argument("--confirm", action="store_true", help="(BLOCKED) live write needs separate GO + verified mechanism")
    args = ap.parse_args()
    factor = 1 + args.pct / 100.0

    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "reprice_dryrun_" + ts)
    os.makedirs(cache, exist_ok=True)

    print("=" * 96)
    print("REPRICE DRY-RUN  +%.1f%%  | run: %s" % (args.pct, ts))
    print("=" * 96)
    listings = pull_listings()
    json.dump(listings, open(os.path.join(cache, "_listings_raw.json"), "w", encoding="utf-8"), ensure_ascii=False)

    rows = []
    monitored = 0
    for it in listings:
        vs = it.get("variation_statistics") or {}
        cur = vs.get("min_sell_price")
        if not isinstance(cur, (int, float)):
            continue
        cfg = it.get("configuration") or {}
        price_mon = not bool(cfg.get("disable_price_monitoring"))  # monitoring ON if not disabled
        if price_mon:
            monitored += 1
        new = round(cur * factor, 2)
        rows.append({"id": it.get("id"), "item": it.get("item_id_on_site"), "status": it.get("status"),
                     "title": (it.get("title") or "")[:50], "cur": round(cur, 2), "new": new,
                     "delta": round(new - cur, 2), "price_monitoring_on": price_mon})

    active = [r for r in rows if r["status"] == 2]
    json.dump(rows, open(os.path.join(cache, "_reprice_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("listings pulled:", len(listings), "| with sell price:", len(rows), "| ACTIVE(status=2):", len(active))
    print("price-monitoring ON (manual price may be auto-overwritten):", monitored, "/", len(rows))
    tot_cur = round(sum(r["cur"] for r in active), 2)
    tot_new = round(sum(r["new"] for r in active), 2)
    print("ACTIVE total current sell: $%.2f  ->  +%.1f%% = $%.2f   (Δ $%.2f across %d listings)" %
          (tot_cur, args.pct, tot_new, round(tot_new - tot_cur, 2), len(active)))
    print("-" * 96)
    print("%-13s %-7s %-7s %-7s %-4s | %s" % ("item", "cur$", "new$", "Δ$", "mon", "title"))
    print("-" * 96)
    for r in active[:40]:
        print("%-13s %-7s %-7s %-7s %-4s | %s" %
              (r["item"], r["cur"], r["new"], r["delta"], "Y" if r["price_monitoring_on"] else "n", r["title"]))
    if len(active) > 40:
        print("  ... +%d more (full plan in %s/_reprice_plan.json)" % (len(active) - 40, cache))
    print("=" * 96)
    if args.confirm:
        print("--confirm: BLOCKED. Live reprice needs (a) separate owner GO, (b) a verified bulk price-WRITE")
        print("mechanism (not yet cracked — reprice_one.py never confirmed a write), (c) a price-monitoring")
        print("decision. DRY-RUN ONLY by design.")
        return 1
    print("DRY-RUN complete. NOTHING changed. Awaiting owner GO + clarification (reprice only vs renew/relist).")
    print("CACHE:", cache)
    return 0


if __name__ == "__main__":
    sys.exit(main())

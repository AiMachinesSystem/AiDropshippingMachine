#!/usr/bin/env python3
"""
read_terapeak.py — READ-ONLY eBay demand reader via Terapeak (Seller Hub → Research).

PROBE-FIRST: reuses storage_state_ebay.json (from login_ebay_save_session.py). For each keyword it opens
Terapeak Product Research, CAPTURES every eBay XHR JSON on the page (the research API that backs the metrics),
saves them to cache, and best-effort extracts: avg sold price, sold count, sell-through %, active listings,
total sales, free-ship %. The exact Terapeak API shape is mapped on the FIRST authenticated run (like the AutoDS
marketplace crack) — until then the parser is best-effort and the raw capture is the source of truth.

SAFETY: READ-ONLY research (navigation + reading the research page). No listing edits/publish/orders. No creds.
GO scope: GO_EBAY_READ_SESSION (read-only). Run with PYTHONIOENCODING=utf-8.
Usage: read_terapeak.py "kitchen utensil set" "laundry basket" ...
"""
import os, re, sys, json
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state_ebay.json")
RESEARCH = "https://www.ebay.com/sh/research"


def find_root(s):
    c = os.path.abspath(s)
    while c != os.path.dirname(c):
        if os.path.isdir(os.path.join(c, "10_OUTPUTS")):
            return c
        c = os.path.dirname(c)
    return s


def parse_metrics(captured):
    """Best-effort extraction from captured research JSON. Returns {} if shape unknown (then raw is source of truth)."""
    out = {}
    for rec in captured:
        try:
            data = json.loads(rec["body"])
        except Exception:
            continue
        blob = json.dumps(data).lower()
        if not any(k in blob for k in ("selltrough", "sellthrough", "sell_through", "avgsoldprice",
                                       "totalsoldcount", "soldcount", "averagesoldprice")):
            continue
        # flatten search for common Terapeak metric keys (names confirmed on first live run)
        def deep_find(o, keys):
            stack = [o]
            while stack:
                x = stack.pop()
                if isinstance(x, dict):
                    for k, v in x.items():
                        if k.lower().replace("_", "") in keys and isinstance(v, (int, float, str)):
                            return v
                        stack.append(v)
                elif isinstance(x, list):
                    stack.extend(x)
            return None
        out.setdefault("avg_sold_price", deep_find(data, {"averagesoldprice", "avgsoldprice"}))
        out.setdefault("sold_count", deep_find(data, {"totalsoldcount", "soldcount", "totalsold"}))
        out.setdefault("sell_through", deep_find(data, {"sellthrough", "sellthroughrate", "selltrough"}))
        out.setdefault("active_listings", deep_find(data, {"totalactivelistings", "activelistings"}))
        out.setdefault("total_sales", deep_find(data, {"totalsalesamount", "totalsales"}))
    return {k: v for k, v in out.items() if v is not None}


def main():
    kws = sys.argv[1:] or ["kitchen utensil set"]
    if not os.path.exists(STATE):
        print("BLOCKED: storage_state_ebay.json not found. Run login_ebay_save_session.py first (owner login)."); return 2
    from playwright.sync_api import sync_playwright
    root = find_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "ebay", "terapeak_" + ts)
    os.makedirs(cache, exist_ok=True)
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        pg = ctx.new_page()
        for i, kw in enumerate(kws):
            captured = []

            def on_resp(r):
                try:
                    u = r.url
                    if "ebay.com" not in u or "application/json" not in (r.headers or {}).get("content-type", ""):
                        return
                    if any(s in u.lower() for s in ("research", "marketplace_insights", "aggregat", "metric", "sh/research")):
                        captured.append({"url": u, "body": r.text()[:300000]})
                except Exception:
                    pass

            pg.on("response", on_resp)
            url = RESEARCH + "?marketplace=EBAY-US&keywords=" + re.sub(r"\s+", "%20", kw) + "&dayRange=30&tabName=SOLD"
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(8000)
                pg.mouse.wheel(0, 2000); pg.wait_for_timeout(3000)
            except Exception as e:
                print("  [%s] nav err %s" % (kw, type(e).__name__))
            # detect a sign-in bounce
            if "signin" in pg.url.lower() or "/login" in pg.url.lower():
                print("  [%s] SESSION EXPIRED -> re-run login_ebay_save_session.py" % kw)
                pg.remove_listener("response", on_resp); break
            with open(os.path.join(cache, "kw_%02d_capture.jsonl" % i), "w", encoding="utf-8") as fh:
                for c in captured:
                    fh.write(json.dumps(c, ensure_ascii=False) + "\n")
            metrics = parse_metrics(captured)
            results[kw] = {"metrics": metrics, "n_json": len(captured),
                           "endpoints": sorted({c["url"].split("?")[0] for c in captured})}
            pg.remove_listener("response", on_resp)
            print("  [%s] json captured: %d | metrics: %s" % (kw, len(captured), metrics or "(map on first live run — see capture)"))
        b.close()
    json.dump(results, open(os.path.join(cache, "_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("-" * 60)
    print("CACHE:", cache)
    print("NOTE: if metrics are empty, open kw_*_capture.jsonl to map the real Terapeak API keys (probe step), then finalize parse_metrics().")
    return 0


if __name__ == "__main__":
    sys.exit(main())

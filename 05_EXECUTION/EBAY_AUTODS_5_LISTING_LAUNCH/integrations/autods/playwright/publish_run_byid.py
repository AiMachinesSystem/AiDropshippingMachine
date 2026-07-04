#!/usr/bin/env python3
"""
publish_run_byid.py — BLOAT-IMMUNE batch publish (fixes E-020). Everything is by draft-ID / via the products
list API, never by /upload-list DOM match (which broke on brand-prefixed titles + page-1 bloat).

Per candidate: ensure imported -> find draft by ASIN via list API -> econ+error gate -> set_title_by_id
(per-draft page) -> set-desc --id (templated, VeRO-safe) -> publish_one_draft (per-draft page) -> count.
Verifies the real result with a final list-API census (id gone from drafts == published, E-005/E-015 safe).
Stops the whole run on an eBay account restriction. GO: owner 2026-06-28 'pubblica 36 ... sei tu il boss'.

Usage: publish_run_byid.py <candidates.json> [--target 36] [--max-attempts 60]
"""
import os, re, sys, json, subprocess, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, ".venv", "Scripts", "python.exe")
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

BRANDLEAD = re.compile(r"^[A-Z0-9][A-Z0-9'’&.\-]+$")


def pull_drafts(retries=3):
    """Return {asin: ...} from the products list API. Retries on empty result: a missed
    auth-capture window returns {} which E-023 proved must be treated as an error, never
    as 'no drafts'."""
    for attempt in range(retries):
        out = _pull_drafts_once()
        if out:
            return out
        print("  pull_drafts empty (attempt %d/%d) - retrying" % (attempt + 1, retries), flush=True)
    return out


def _pull_drafts_once():
    cap = {}
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()

        def on_req(req):
            if "/products/" in req.url and "/list/" in req.url and req.method == "POST" and not cap:
                cap["url"] = req.url; cap["headers"] = dict(req.headers); cap["body"] = req.post_data
        pg.on("request", on_req)
        pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(9000)
        if not cap:
            b.close(); return out
        hdr = {k: v for k, v in cap["headers"].items()
               if k.lower() in ("authorization", "content-type", "accept", "origin", "referer")}
        body = json.loads(cap["body"]); body["limit"] = 450; body["offset"] = 0
        resp = pg.request.post(cap["url"], data=json.dumps(body), headers=hdr)
        data = resp.json(); b.close()
    items = data.get("results") or data.get("data") or []
    if isinstance(items, dict):
        items = items.get("results", [])
    for it in items:
        vs = it.get("variation_statistics") or {}
        buy = vs.get("min_buy_price")
        st = vs.get("in_stock"); st = (st.get("total") if isinstance(st, dict) else st)
        reg = vs.get("supplier_default_region") or vs.get("supplier_region")
        asin = ""; regn = reg
        if isinstance(reg, list) and reg:
            asin = reg[0].get("item_id_on_site", ""); regn = reg[0].get("region")
        if not asin:
            continue
        out[asin] = {"id": str(it.get("id")), "title": it.get("title") or "",
                     "err": len(it.get("error_list") or []), "stock": st, "region": regn, "buy": buy}
    return out


def gen_desc(title, niche):
    bl = {"kitchen": ["Durable, food-safe build for everyday cooking", "Easy to clean and store",
                      "A practical upgrade or gift"],
          "pool": ["Built for pool, patio and outdoor use", "Water-resistant, easy to rinse",
                   "Handy seasonal essential"],
          "storage": ["Maximizes space, cuts clutter", "Sturdy for closet, pantry or garage",
                      "Simple to set up and move"],
          "cleaning": ["Tackles everyday messes fast", "Reusable and easy to rinse",
                       "Low-cost way to keep things spotless"],
          "meat_food": ["Heavy-duty for grilling and food prep", "Reliable everyday performance",
                        "Easy to clean, built to last"]}.get(niche, ["Quality build for everyday use",
                                                                     "Easy to clean and store", "A practical upgrade"])
    lis = "\n".join("  <li>%s</li>" % x for x in bl)
    return ("<h3>%s</h3>\n<p>%s — a reliable choice for your home, made to make everyday tasks easier.</p>\n"
            "<ul>\n%s\n</ul>\n<p><em>Fast US dispatch with tracking. 30-day returns.</em></p>\n"
            % (title, title[:60], lis))


def run(cmd, t=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=t,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidates")
    ap.add_argument("--target", type=int, default=36)
    ap.add_argument("--max-attempts", type=int, default=60)
    args = ap.parse_args()
    cands = json.load(open(args.candidates, encoding="utf-8"))
    log = os.path.join(HERE, "_publish_run_byid_log.txt")

    def L(m):
        print(m, flush=True)
        open(log, "a", encoding="utf-8").write(m + "\n")

    open(log, "w").close()
    L("=== PUBLISH RUN BY-ID | target=%d | candidates=%d ===" % (args.target, len(cands)))
    drafts = pull_drafts()
    L("initial drafts (by asin): %d" % len(drafts))

    # Phase 1: import any candidate not already a draft
    missing = [c for c in cands if c["asin"] not in drafts]
    L("importing %d missing candidates..." % len(missing))
    for c in missing:
        out = run([PY, os.path.join(HERE, "manage_draft.py"), "import", "--url",
                   "https://www.amazon.com/dp/%s" % c["asin"]], 150)
        ok = "drafts after" in out and "Add as Draft" in out
        L("  import %s : %s" % (c["asin"], "ok" if ok else "fail/dup"))
    if missing:
        drafts = pull_drafts()
        L("drafts after imports (by asin): %d" % len(drafts))
        if not drafts:
            L("ABORT: drafts census empty after imports (E-023) - refusing to mark candidates no-draft.")
            return 2
    post_import = set(drafts.keys())

    # Phase 2: prepare + publish by id
    published = 0; attempts = 0; results = []
    for c in cands:
        if published >= args.target or attempts >= args.max_attempts:
            break
        asin = c["asin"]; rec = drafts.get(asin)
        if not rec:
            results.append((asin, "no-draft")); continue
        attempts += 1
        if rec["err"] > 0:
            results.append((asin, "skip-err%d" % rec["err"])); continue
        sent = rec["buy"] is not None and abs(float(rec["buy"]) - 133.13) < 0.5
        if not (rec["region"] == 1 and rec["stock"] and float(rec["stock"]) > 0 and not sent):
            results.append((asin, "skip-econ")); continue
        seo = (c.get("seo_title") or "").strip()
        if len(seo) < 18 or len(seo) > 80:
            results.append((asin, "skip-title-len")); continue
        did = rec["id"]
        st = run([PY, os.path.join(HERE, "set_title_by_id.py"), did, seo], 150)
        if "PERSISTED True" not in st:
            results.append((asin, "skip-title-persist")); continue
        df = os.path.join(HERE, "_run_desc_%s.html" % asin)
        open(df, "w", encoding="utf-8").write(gen_desc(seo, c.get("niche", "")))
        run([PY, os.path.join(HERE, "manage_draft.py"), "set-desc", "--id", did, "--desc-file", df], 150)
        guard = " ".join(re.findall(r"[A-Za-z0-9]+", seo.lower())[:2])
        pub = run([PY, os.path.join(HERE, "publish_one_draft.py"), did, guard], 200)
        if "BLOCKED-EBAY-RESTRICTION" in pub:
            L("  [%s] BLOCKED eBay restriction -> STOP." % asin); results.append((asin, "BLOCKED")); break
        if "RESULT: PUBLISHED" in pub:
            published += 1; results.append((asin, "PUBLISHED")); L("  [%d live] %s | %s" % (published, asin, seo[:48]))
        else:
            results.append((asin, "unconfirmed")); L("  [unconf] %s | %s" % (asin, pub.strip()[-80:]))

    # Phase 3: API census verify
    final = pull_drafts()
    verified = sum(1 for c in cands if c["asin"] in post_import and c["asin"] not in final)
    L("\n=== SUMMARY: publish-reported=%d | API-verified-left-drafts=%d | attempts=%d ===" %
      (published, verified, attempts))
    for a, r in results:
        L("  %s : %s" % (a, r))
    L("RUN_RESULT verified=%d" % verified)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
publish_backlog.py — publish from a PRE-FETCHED publishable-drafts pool (owner intent 2026-07-17
"listiamo 202 ben selezionati"). Unlike publish_run_byid.py this does NO import phase and does NOT
rely on the 450-limit census to find drafts (which is blind past 450 when the workspace holds ~2010
drafts). Draft ids come straight from _qbacklog.json. Per item: set_title_by_id -> set-desc --id ->
publish_one_draft (E-002 guarded). Stops the whole run on an eBay account restriction. Final result is
verified with a PAGINATED census (id no longer in drafts == published).

GO scope: batch-publish is owner-GO-implicit for the eBay/AutoDS routine (feedback-routine-go).
Usage: publish_backlog.py _qbacklog.json [--target 202] [--max-attempts 300]
"""
import os, re, sys, json, subprocess, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, ".venv", "Scripts", "python.exe")
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright


def gen_desc(title, niche):
    bl = {"kitchen": ["Durable, food-safe build for everyday cooking", "Easy to clean and store",
                      "A practical upgrade or gift"],
          "storage": ["Maximizes space, cuts clutter", "Sturdy for closet, pantry or garage",
                      "Simple to set up and move"],
          "cleaning": ["Tackles everyday messes fast", "Reusable and easy to rinse",
                       "Low-cost way to keep things spotless"]}.get(
              niche, ["Quality build for everyday use", "Easy to clean and store", "A practical upgrade"])
    lis = "\n".join("  <li>%s</li>" % x for x in bl)
    return ("<h3>%s</h3>\n<p>%s — a reliable choice for your home, made to make everyday tasks easier.</p>\n"
            "<ul>\n%s\n</ul>\n<p><em>Fast US dispatch with tracking. 30-day returns.</em></p>\n"
            % (title, title[:60], lis))


def run(cmd, t=180):
    try:
        # E-028: children print supplier titles that contain bytes outside cp1252; text=True would
        # decode with the Windows locale codec, kill the pipe reader thread and stall the child
        # until the timeout. Always decode as utf-8 with replacement.
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=t,
                           encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def draft_ids(retries=3):
    """Paginated census of current draft ids (bypasses the 450 blindness)."""
    for _ in range(retries):
        ids = _draft_ids_once()
        if ids:
            return ids
        print("  census empty - retry", flush=True)
    return ids


def _draft_ids_once():
    cap = {}; ids = set()
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
            b.close(); return ids
        hdr = {k: v for k, v in cap["headers"].items()
               if k.lower() in ("authorization", "content-type", "accept", "origin", "referer")}
        body = json.loads(cap["body"])
        for off in range(0, 3000, 300):
            body["limit"] = 300; body["offset"] = off
            resp = pg.request.post(cap["url"], data=json.dumps(body), headers=hdr)
            try:
                data = resp.json()
            except Exception:
                break
            items = data.get("results") or []
            if isinstance(items, dict):
                items = items.get("results", [])
            if not items:
                break
            for it in items:
                ids.add(str(it.get("id")))
            if len(items) < 300:
                break
        b.close()
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pool")
    ap.add_argument("--target", type=int, default=202)
    ap.add_argument("--max-attempts", type=int, default=300)
    args = ap.parse_args()
    pool = json.load(open(args.pool, encoding="utf-8"))
    log = os.path.join(HERE, "_publish_backlog_log.txt")

    def L(m):
        print(m, flush=True)
        open(log, "a", encoding="utf-8").write(m + "\n")

    open(log, "w").close()
    L("=== PUBLISH BACKLOG | target=%d | pool=%d ===" % (args.target, len(pool)))
    before = draft_ids()
    L("draft census before: %d ids" % len(before))

    published = 0; attempts = 0; results = []; quota_streak = 0
    for c in pool:
        if published >= args.target or attempts >= args.max_attempts:
            break
        did = str(c["id"]); asin = c.get("asin", ""); seo = (c.get("seo_title") or "").strip()
        if did not in before:
            results.append((asin, "gone-already")); continue
        if not (18 <= len(seo) <= 80):
            results.append((asin, "skip-title-len")); continue
        attempts += 1
        st = run([PY, os.path.join(HERE, "set_title_by_id.py"), did, seo], 150)
        if "PERSISTED True" not in st:
            results.append((asin, "skip-title-persist")); continue
        df = os.path.join(HERE, "_bk_desc_%s.html" % did)
        open(df, "w", encoding="utf-8").write(gen_desc(seo, c.get("niche", "storage")))
        run([PY, os.path.join(HERE, "manage_draft.py"), "set-desc", "--id", did, "--desc-file", df], 150)
        # E-029: the guard must be a literal substring of the on-page title. Alphanumeric runs
        # break on punctuation ("27.9" -> "27 9", "2026-2027" -> "2026 2027") and never match,
        # aborting good drafts. Use the first two ALPHABETIC words (>=3 chars) instead.
        words = [w for w in re.findall(r"[A-Za-z]{3,}", seo.lower())][:2]
        guard = " ".join(words) if len(words) == 2 else seo.lower()[:12]
        pub = run([PY, os.path.join(HERE, "publish_one_draft.py"), did, guard], 200)
        if "BLOCKED-EBAY-RESTRICTION" in pub:
            L("  [%s] BLOCKED eBay restriction -> STOP." % asin); results.append((asin, "BLOCKED")); break
        if "RESULT: PUBLISHED" in pub:
            published += 1; quota_streak = 0; results.append((asin, "PUBLISHED"))
            L("  [%d live] %s | %s" % (published, asin, seo[:48]))
        else:
            # E-027: the real eBay error now comes back in the RESULT line (read from error_list).
            # "usage limit" = eBay API quota of the AutoDS app: transient but pointless to hammer.
            low = pub.lower()
            if "usage limit" in low or "temporarily unavailable" in low:
                quota_streak += 1
                results.append((asin, "ebay-api-quota"))
                L("  [quota %d] %s | eBay API limit/unavailable" % (quota_streak, asin))
                if quota_streak >= 5:
                    L("  !! eBay API limit persists (5 in a row) -> STOP, resume later"); break
            else:
                quota_streak = 0
                results.append((asin, "unconfirmed")); L("  [unconf] %s | %s" % (asin, pub.strip()[-90:]))
        try:
            os.remove(df)
        except OSError:
            pass

    after = draft_ids()
    verified = sum(1 for c in pool if str(c["id"]) in before and str(c["id"]) not in after)
    L("\n=== SUMMARY: publish-reported=%d | API-verified-left-drafts=%d | attempts=%d ===" %
      (published, verified, attempts))
    from collections import Counter
    tally = Counter(r for _, r in results)
    for k, v in tally.most_common():
        L("  %s: %d" % (k, v))
    L("RUN_RESULT verified=%d" % verified)
    return 0


if __name__ == "__main__":
    sys.exit(main())

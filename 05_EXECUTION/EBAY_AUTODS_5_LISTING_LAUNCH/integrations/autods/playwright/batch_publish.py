#!/usr/bin/env python3
"""
batch_publish.py — orchestrate a TARGETED publish batch (owner GO 2026-06-24 "pubblica 25 annunci mirati").
Drives the PROVEN per-product scripts as subprocesses (each = fresh browser -> mitigates E-013 session fatigue):
  manage_draft.py full (import+title+desc, prints PERSISTED) -> read_draft_economics.py (E-012 sentinel check)
  -> publish_one_draft.py (E-002 guarded publish).
Safeguards: skip if title not set / desc not PERSISTED (E-013) / economics = sentinel 133.13&stock0 (E-012);
STOP the whole batch on an eBay account restriction (never hammer). Auto-generates a generic VeRO-safe title
(<=80) + a niche-templated description. Logs every decision; prints a machine-readable summary.

GO scope: owner GO 2026-06-24 (publish targeted batch). Run with PYTHONIOENCODING=utf-8.
Usage: batch_publish.py <candidates.json> [--target 25] [--max-attempts 30]
"""
import os, re, sys, json, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, ".venv", "Scripts", "python.exe")
LOGDIR = None

BRAND = re.compile(r"\b(akro-?mils|usa pan|honey-?can-?do|voten|iron american|holdn|u\.s\.|vtopmart|"
                   r"vremi|zulay|joseph|oxo|pyrex|lodge|camp chef|yiifeeo|nutrichef|sensarte|cuisinel|"
                   r"bruntmor|circulon|esplite|eslite|komuee|frieling|uptronic|blitzlabs|razab|italic|"
                   r"shineuri|fin fun|pardise|e-cloth|bankers|granitestone|hexclad|household essentials|"
                   r"smart design|lock ?& ?lock|zenacasa|shumaru|\bbull\b|convenience concepts|armocity|"
                   r"yaheetech|ella ?& ?emma|elifine|diveblast|neteast|hitop|fritz|bedwina|kooper|otdair|"
                   r"lightdot|banord|porch shield|vailge|arcedo|tempera|easy-going|startwo|tomcare)\b", re.I)


def gen_title(mtitle):
    t = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", mtitle or "")        # drop [..] (..)
    t = BRAND.sub(" ", t)
    t = re.sub(r"[|,–—-]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    # drop a leading coined-brand token (CamelCase / ALLCAPS)
    toks = t.split()
    while toks and (re.search(r"[a-z][A-Z]", toks[0]) or (toks[0].isupper() and len(toks[0]) >= 3 and toks[0].isalpha())):
        toks = toks[1:]
    t = " ".join(toks)
    if len(t) > 80:
        cut = t[:80].rsplit(" ", 1)[0]
        t = cut
    return t.strip()


def gen_desc(title, niche):
    bullets = {
        "kitchen": ["Durable, food-safe materials built for everyday cooking",
                    "Easy to clean and simple to store",
                    "A practical upgrade for any kitchen or gift"],
        "pool": ["Built for pool, patio, deck, and outdoor use",
                 "Water-resistant and easy to rinse clean",
                 "A handy seasonal essential for pool owners"],
        "storage": ["Maximizes space and keeps clutter under control",
                    "Sturdy build for closet, laundry, pantry, or garage",
                    "Simple to assemble and easy to move"],
        "cleaning": ["Tackles everyday messes quickly and effectively",
                     "Reusable and easy to rinse for repeated use",
                     "A low-cost way to keep your home spotless"],
        "meat_food": ["Heavy-duty build for grilling, frying, and food prep",
                      "Even heat and reliable everyday performance",
                      "Easy to clean and built to last"],
    }.get(niche, ["Quality build for everyday use", "Easy to clean and store", "A practical, useful upgrade"])
    lis = "\n".join("  <li>%s</li>" % b for b in bullets)
    short = title[:60]
    return ("<h3>%s</h3>\n<p>%s - a practical, reliable choice for your home. Designed to make everyday tasks "
            "easier, with quality you can count on.</p>\n<ul>\n%s\n</ul>\n"
            "<p><em>Fast US dispatch with tracking. 30-day returns. Buy with confidence.</em></p>\n"
            % (title, short, lis))


def run(cmd, timeout):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidates")
    ap.add_argument("--target", type=int, default=25)
    ap.add_argument("--max-attempts", type=int, default=30)
    args = ap.parse_args()
    cands = json.load(open(args.candidates, encoding="utf-8"))
    log_path = os.path.join(HERE, "_batch_publish_log.txt")
    results = []
    published = 0
    attempts = 0

    def log(m):
        print(m, flush=True)
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(m + "\n")

    log("=== BATCH PUBLISH start | target=%d | candidates=%d ===" % (args.target, len(cands)))
    for c in cands:
        if published >= args.target or attempts >= args.max_attempts:
            break
        attempts += 1
        asin = c["asin"]; niche = c.get("niche", "")
        title = gen_title(c.get("title", ""))
        if len(title) < 18:
            log("SKIP %s: generated title too short (%r)" % (asin, title)); results.append((asin, "SKIP-title")); continue
        words = re.findall(r"[A-Za-z0-9]+", title.lower())
        match = " ".join(re.findall(r"[A-Za-z0-9]+", (c.get("title", "")).lower())[:2])
        guard = " ".join(words[:2])
        descfile = os.path.join(HERE, "_batch_desc_%s.html" % asin)
        open(descfile, "w", encoding="utf-8").write(gen_desc(title, niche))
        url = "https://www.amazon.com/dp/%s" % asin
        log("\n[%d/%d attempt, %d live] %s | niche=%s | title=%r" % (attempts, args.max_attempts, published, asin, niche, title))

        out = run([PY, os.path.join(HERE, "manage_draft.py"), "full", "--url", url,
                   "--match", match, "--title", title, "--desc-file", descfile], 300)
        m_id = re.search(r"id=([0-9a-f]+)", out)
        ok_title = "title=True" in out
        ok_desc = re.search(r"desc=True", out)
        if not (m_id and ok_title):
            log("  -> SKIP import/title (match=%r). tail: %s" % (match, out.strip()[-160:])); results.append((asin, "SKIP-import")); continue
        did = m_id.group(1)
        if not ok_desc:
            # E-013 mitigation: retry set-desc once on a fresh subprocess (fresh session) before giving up
            log("  -> desc not PERSISTED, retrying set-desc once (E-013 mitigation)")
            rt = run([PY, os.path.join(HERE, "manage_draft.py"), "set-desc", "--id", did, "--desc-file", descfile], 150)
            if "PERSISTED: True" in rt:
                ok_desc = True; log("     retry OK (desc persisted)")
            else:
                log("  -> SKIP desc not PERSISTED after retry (E-013)"); results.append((asin, "SKIP-desc")); continue

        econ = run([PY, os.path.join(HERE, "read_draft_economics.py")], 150)
        row = [l for l in econ.splitlines() if did in l]
        if row and ("133.13" in row[0] and re.search(r"stock=0", row[0])):
            log("  -> SKIP E-012 sentinel economics (133.13/stock0): %s" % row[0][:80]); results.append((asin, "SKIP-E012")); continue

        pub = run([PY, os.path.join(HERE, "publish_one_draft.py"), did, guard], 200)
        if "RESULT: PUBLISHED" in pub:
            published += 1; log("  -> PUBLISHED (%d live)" % published); results.append((asin, "PUBLISHED"))
        elif "BLOCKED-EBAY-RESTRICTION" in pub:
            log("  -> BLOCKED eBay account restriction -> STOP batch."); results.append((asin, "BLOCKED")); break
        else:
            log("  -> UNCONFIRMED: %s" % pub.strip()[-160:]); results.append((asin, "UNCONFIRMED"))

    log("\n=== SUMMARY: published=%d / target=%d | attempts=%d ===" % (published, args.target, attempts))
    for a, r in results:
        log("  %s : %s" % (a, r))
    log("BATCH_RESULT published=%d" % published)
    return 0


if __name__ == "__main__":
    sys.exit(main())

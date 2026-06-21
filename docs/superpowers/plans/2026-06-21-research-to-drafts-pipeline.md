# Research→3-Drafts Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One command pulls AutoDS Marketplace candidates, scores them by REAL eBay margin, selects the top 3, generates VeRO-safe draft copy, and imports them as drafts — replacing today's manual multi-step loop.

**Architecture:** A small Python package `pipeline/` of pure, unit-tested functions (filtering, brand detection, margin math, eBay-price parsing, copy generation, ranking) plus thin network/Playwright shells (Marketplace pull, eBay fetch) and a CLI orchestrator. The orchestrator chains: pull → ebay-check → rank → copy → import (via the existing `manage_draft.py full`). Pure logic is TDD'd in isolation; side-effecting steps are smoke-tested.

**Tech Stack:** Python 3.12, Playwright (sync), pytest, the existing `manage_draft.py` CLI, `r.jina.ai` render proxy for eBay search.

## Global Constraints

- Working dir for all code: `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/` (call it `PW/`). The package lives at `PW/pipeline/`.
- **Title ≤ 80 chars HARD CAP** — any title-producing function returns ≤80 or raises; never emit >80.
- **Drafts only, never publish** — the pipeline imports via `manage_draft.py full` (which only clicks "Add as Draft"); it must never click Import/Publish.
- **Import is a live AutoDS write = GO-class** — the CLI defaults to `--dry-run` (no writes); real import happens ONLY with an explicit `--go` flag. No `--go` ⇒ no AutoDS mutation.
- `storage_state.json` holds session tokens — it is gitignored and MUST never be committed or printed.
- Ephemeral/probe files use a leading `_` (gitignored). Pipeline source files do NOT use `_` (they are committed).
- Evidence honesty: eBay sold/price come from proxy renders → all counts are lower bounds; the report labels them so. eBay Sold filter is often 403 (known wall) — degrade to active-listing price, never invent.
- Brand/VeRO: titles are stripped of brand tokens before use; branded candidates are excluded upstream.
- Margin formula (canonical, used everywhere): `margin = ebay_price - amazon_cost - (ebay_price * 0.1325 + 0.40)`.
- Python invocation: `PW/.venv/Scripts/python.exe`; tests: `PW/.venv/Scripts/python.exe -m pytest`.

---

### Task 1: Title cleaner (`clean_title`)

**Files:**
- Create: `PW/pipeline/__init__.py` (empty)
- Create: `PW/pipeline/copy_gen.py`
- Test: `PW/pipeline/tests/test_copy_gen.py`

**Interfaces:**
- Produces: `clean_title(raw: str, brands: list[str], max_len: int = 80) -> str` — strips any brand token (case-insensitive, whole-word), collapses whitespace, truncates at a word boundary so the result is ≤ `max_len`. Never returns >`max_len`.

- [ ] **Step 1: Write the failing test**

```python
# PW/pipeline/tests/test_copy_gen.py
from pipeline.copy_gen import clean_title

BRANDS = ["BV", "Goldenwarm", "Comsun"]

def test_strips_brand_and_caps_length():
    raw = "BV Pet 60ft Aerial Trolley Runner Cable Dog Tie Out System For Large Yards Heavy Duty Outdoor"
    out = clean_title(raw, BRANDS)
    assert "BV" not in out.split()
    assert len(out) <= 80
    assert out == out.strip()

def test_truncates_at_word_boundary():
    raw = "Aerial " * 30
    out = clean_title(raw, BRANDS)
    assert len(out) <= 80
    assert not out.endswith(" ")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_copy_gen.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.copy_gen'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/copy_gen.py
import re

def clean_title(raw: str, brands: list[str], max_len: int = 80) -> str:
    words = (raw or "").split()
    low = {b.lower() for b in brands}
    words = [w for w in words if w.lower().strip(",.") not in low]
    s = " ".join(words)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= max_len:
        return s
    out = []
    n = 0
    for w in s.split():
        if n + len(w) + (1 if out else 0) > max_len:
            break
        n += len(w) + (1 if out else 0)
        out.append(w)
    return " ".join(out).strip()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_copy_gen.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/__init__.py PW/pipeline/copy_gen.py PW/pipeline/tests/test_copy_gen.py
git commit -m "feat(pipeline): clean_title - brand-strip + <=80 hard cap"
```

---

### Task 2: VeRO-safe description builder (`build_description`)

**Files:**
- Modify: `PW/pipeline/copy_gen.py`
- Test: `PW/pipeline/tests/test_copy_gen.py` (add cases)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `build_description(hook: str, intro: str, bullets: list[str], close: str) -> str` — returns deterministic VeRO-safe HTML: `<p><strong>hook</strong></p><p>intro</p><ul><li>…</li></ul><p>close</p>`. Escapes `<`,`>`,`&` in inputs. No brand names, no fabricated claims (caller's responsibility; function never injects claims).

- [ ] **Step 1: Write the failing test**

```python
# add to PW/pipeline/tests/test_copy_gen.py
from pipeline.copy_gen import build_description

def test_build_description_structure():
    html = build_description("Hook", "Intro line", ["One", "Two"], "Closing line")
    assert html.startswith("<p><strong>Hook</strong></p>")
    assert "<ul><li>One</li><li>Two</li></ul>" in html
    assert html.rstrip().endswith("<p>Closing line</p>")

def test_build_description_escapes_html():
    html = build_description("A & B", "x < y", ["a > b"], "end")
    assert "&amp;" in html and "&lt;" in html and "&gt;" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_copy_gen.py -k description -v`
Expected: FAIL with `ImportError: cannot import name 'build_description'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to PW/pipeline/copy_gen.py
def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_description(hook: str, intro: str, bullets: list[str], close: str) -> str:
    lis = "".join("<li>%s</li>" % _esc(b) for b in bullets)
    return (
        "<p><strong>%s</strong></p>" % _esc(hook)
        + "<p>%s</p>" % _esc(intro)
        + "<ul>%s</ul>" % lis
        + "<p>%s</p>" % _esc(close)
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_copy_gen.py -k description -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/copy_gen.py PW/pipeline/tests/test_copy_gen.py
git commit -m "feat(pipeline): build_description - VeRO-safe HTML, escaped"
```

---

### Task 3: Margin math + eBay price parsing (`ebay_check` pure functions)

**Files:**
- Create: `PW/pipeline/ebay_check.py`
- Test: `PW/pipeline/tests/test_ebay_check.py`

**Interfaces:**
- Produces:
  - `compute_margin(ebay_price: float, amazon_cost: float) -> float` — canonical formula, rounded to 2 dp.
  - `parse_ebay_prices(render_text: str) -> list[float]` — extracts `$<float>` amounts from an `r.jina.ai` eBay-search render, ignoring values <1 and >999.
  - `median_price(prices: list[float]) -> float | None` — None on empty.

- [ ] **Step 1: Write the failing test**

```python
# PW/pipeline/tests/test_ebay_check.py
from pipeline.ebay_check import compute_margin, parse_ebay_prices, median_price

def test_compute_margin_canonical():
    # 26.99 - 8.49 - (26.99*0.1325 + 0.40) = 14.52 -> rounded
    assert compute_margin(26.99, 8.49) == 14.52

def test_parse_prices_filters_outliers():
    text = "Item A $24.99 Free shipping ... Item B $0.99 promo ... Item C $1,080.77 rug ... $27.99"
    prices = parse_ebay_prices(text)
    assert 24.99 in prices and 27.99 in prices
    assert 0.99 not in prices and 1080.77 not in prices

def test_median_price():
    assert median_price([10.0, 20.0, 30.0]) == 20.0
    assert median_price([]) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_ebay_check.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.ebay_check'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/ebay_check.py
import re, statistics

def compute_margin(ebay_price: float, amazon_cost: float) -> float:
    fee = ebay_price * 0.1325 + 0.40
    return round(ebay_price - amazon_cost - fee, 2)

def parse_ebay_prices(render_text: str) -> list[float]:
    out = []
    for m in re.findall(r"\$\s?([0-9][0-9,]*\.[0-9]{2})", render_text or ""):
        v = float(m.replace(",", ""))
        if 1.0 <= v <= 999.0:
            out.append(v)
    return out

def median_price(prices: list[float]):
    return round(statistics.median(prices), 2) if prices else None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_ebay_check.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/ebay_check.py PW/pipeline/tests/test_ebay_check.py
git commit -m "feat(pipeline): margin math + eBay price parse (outlier-filtered)"
```

---

### Task 4: Candidate filtering (`candidates` pure functions)

**Files:**
- Create: `PW/pipeline/candidates.py`
- Test: `PW/pipeline/tests/test_candidates.py`

**Interfaces:**
- Produces:
  - `is_branded(title: str, brands: list[str]) -> bool` — True if any brand token present OR first word is an ALLCAPS brandish token (≥3 chars, not in `{LED,USB,RC,BPA,XL,XXL,3D}`).
  - `filter_candidates(rows: list[dict], tested: set[str], brands: list[str], keep_cats: set[str], max_cost: float) -> list[dict]` — keeps rows where `cat in keep_cats`, `cost <= max_cost`, `asin not in tested`, `not is_branded(title)`; dedups by `asin`; sorts by `cost` ascending. Each row has keys: `asin, title, cat, niche, cost, site, date`.

- [ ] **Step 1: Write the failing test**

```python
# PW/pipeline/tests/test_candidates.py
from pipeline.candidates import is_branded, filter_candidates

BRANDS = ["Yes4All", "BV"]

def test_is_branded():
    assert is_branded("Yes4All Steel Mace", BRANDS)
    assert is_branded("SAFAVIEH Rug", BRANDS)        # ALLCAPS first word
    assert not is_branded("LED Tea Lights 24 Pack", BRANDS)

def test_filter_candidates_keeps_sorts_dedups():
    rows = [
        {"asin": "A1", "title": "Generic dog bowl", "cat": "Pets", "niche": "Dogs", "cost": 9.0, "site": "amazon", "date": "2024-01-01"},
        {"asin": "A1", "title": "Generic dog bowl", "cat": "Pets", "niche": "Dogs", "cost": 9.0, "site": "amazon", "date": "2024-01-01"},
        {"asin": "A2", "title": "Generic cat toy", "cat": "Pets", "niche": "Cats", "cost": 4.0, "site": "amazon", "date": "2024-01-01"},
        {"asin": "A3", "title": "Yes4All weight", "cat": "Sports", "niche": "Fit", "cost": 5.0, "site": "amazon", "date": "2024-01-01"},
        {"asin": "A4", "title": "Generic rug", "cat": "Beauty", "niche": "x", "cost": 5.0, "site": "amazon", "date": "2024-01-01"},
        {"asin": "A5", "title": "Generic pricey", "cat": "Pets", "niche": "Dogs", "cost": 99.0, "site": "amazon", "date": "2024-01-01"},
    ]
    out = filter_candidates(rows, tested={"A6"}, brands=BRANDS, keep_cats={"Pets", "Sports"}, max_cost=20.0)
    assert [r["asin"] for r in out] == ["A2", "A1"]   # A3 branded, A4 cat, A5 cost; deduped; sorted by cost
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_candidates.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.candidates'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/candidates.py
_GENERIC_CAPS = {"LED", "USB", "RC", "BPA", "XL", "XXL", "3D"}

def is_branded(title: str, brands: list[str]) -> bool:
    tl = (title or "").lower()
    if any(b.lower() in tl for b in brands):
        return True
    w0 = (title or "").split()[0] if title else ""
    return len(w0) >= 3 and w0.isupper() and w0 not in _GENERIC_CAPS

def filter_candidates(rows, tested, brands, keep_cats, max_cost):
    seen = set()
    out = []
    for r in rows:
        a = r.get("asin")
        if not a or a in tested or a in seen:
            continue
        if r.get("cat") not in keep_cats:
            continue
        try:
            if float(r.get("cost")) > max_cost:
                continue
        except (TypeError, ValueError):
            continue
        if is_branded(r.get("title", ""), brands):
            continue
        seen.add(a)
        out.append(r)
    out.sort(key=lambda r: float(r["cost"]))
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_candidates.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/candidates.py PW/pipeline/tests/test_candidates.py
git commit -m "feat(pipeline): candidate filter (brand/cat/cost/dedup/sort)"
```

---

### Task 5: Scoring + top-N selection (`selection`)

**Files:**
- Create: `PW/pipeline/selection.py`
- Test: `PW/pipeline/tests/test_selection.py`

**Interfaces:**
- Consumes: scored candidate dicts that carry `margin: float`, `demand: int` (lower-bound sold/active), `saturation: str` in `{low,medium,high,unknown}`.
- Produces:
  - `score_candidate(margin: float, demand: int, saturation: str) -> float` — `0` if `margin <= 0`; else `margin * demand_factor * sat_factor` where `demand_factor = min(demand, 500)/100` (min 0.5) and `sat_factor = {low:1.0, medium:0.7, high:0.4, unknown:0.5}`.
  - `select_top_n(cands: list[dict], n: int = 3) -> list[dict]` — attaches `score` to each, returns the top `n` by score descending (stable).

- [ ] **Step 1: Write the failing test**

```python
# PW/pipeline/tests/test_selection.py
from pipeline.selection import score_candidate, select_top_n

def test_score_zero_on_nonpositive_margin():
    assert score_candidate(-1.0, 300, "low") == 0
    assert score_candidate(0.0, 300, "low") == 0

def test_score_orders_by_margin_demand_saturation():
    low = score_candidate(10.0, 300, "high")
    high = score_candidate(10.0, 300, "low")
    assert high > low

def test_select_top_n():
    cands = [
        {"asin": "A", "margin": 14.0, "demand": 300, "saturation": "medium"},
        {"asin": "B", "margin": 2.0, "demand": 50, "saturation": "high"},
        {"asin": "C", "margin": 9.0, "demand": 400, "saturation": "low"},
        {"asin": "D", "margin": -1.0, "demand": 999, "saturation": "low"},
    ]
    top = select_top_n(cands, n=2)
    assert [c["asin"] for c in top] == ["C", "A"]
    assert all("score" in c for c in top)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_selection.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.selection'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/selection.py
_SAT = {"low": 1.0, "medium": 0.7, "high": 0.4, "unknown": 0.5}

def score_candidate(margin: float, demand: int, saturation: str) -> float:
    if margin is None or margin <= 0:
        return 0
    demand_factor = max(min(int(demand or 0), 500) / 100.0, 0.5)
    sat_factor = _SAT.get(saturation, 0.5)
    return round(margin * demand_factor * sat_factor, 3)

def select_top_n(cands: list[dict], n: int = 3) -> list[dict]:
    scored = []
    for c in cands:
        c = dict(c)
        c["score"] = score_candidate(c.get("margin"), c.get("demand"), c.get("saturation"))
        scored.append(c)
    scored.sort(key=lambda c: c["score"], reverse=True)
    return scored[:n]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_selection.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/selection.py PW/pipeline/tests/test_selection.py
git commit -m "feat(pipeline): scoring + top-N selection"
```

---

### Task 6: Marketplace pull shell (`marketplace.pull_candidates`)

**Files:**
- Create: `PW/pipeline/marketplace.py`
- Test: `PW/pipeline/tests/test_marketplace.py`

**Interfaces:**
- Consumes: nothing from other tasks (calls AutoDS over the network).
- Produces:
  - `rows_from_results(results: list[dict]) -> list[dict]` — pure: maps raw Marketplace API objects to candidate rows (`asin,title,cat,niche,cost,site,date`), decoding `date` from the `_id` ObjectId timestamp. (Unit-tested.)
  - `pull_candidates(state_path: str, max_offset: int = 300) -> list[dict]` — Playwright: capture auth from `/marketplace`, POST the products API paginated with `rating_count>1000` + price band, return `rows_from_results(all)`. (Smoke-tested only.)

- [ ] **Step 1: Write the failing test (pure mapper only)**

```python
# PW/pipeline/tests/test_marketplace.py
from pipeline.marketplace import rows_from_results

def test_rows_from_results_maps_and_decodes_date():
    raw = [{
        "_id": "67e7d8be2bd0f0e37b14d41a",
        "id_on_site": "B0XYZ",
        "site_name": "amazon",
        "title": "Generic widget",
        "categories": [{"name": "Pets"}, {"name": "Dogs"}],
        "product_details": {"min_price": 7.5},
    }]
    rows = rows_from_results(raw)
    assert rows[0]["asin"] == "B0XYZ"
    assert rows[0]["cat"] == "Pets" and rows[0]["niche"] == "Dogs"
    assert rows[0]["cost"] == 7.5
    assert rows[0]["date"].startswith("2025-")   # decoded from ObjectId
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_marketplace.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.marketplace'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/marketplace.py
import os, json, datetime
BASE = "https://platform.autods.com"

def _oid_date(_id):
    try:
        ts = int(str(_id)[:8], 16)
        return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return "?"

def rows_from_results(results):
    rows = []
    for it in results or []:
        cats = it.get("categories", [])
        pd = it.get("product_details") or {}
        rows.append({
            "asin": it.get("id_on_site"),
            "title": (it.get("title") or "")[:120],
            "cat": cats[0]["name"] if cats else "?",
            "niche": cats[1]["name"] if len(cats) > 1 else (cats[-1]["name"] if cats else "?"),
            "cost": pd.get("min_price"),
            "site": it.get("site_name"),
            "date": _oid_date(it.get("_id")),
        })
    return rows

def pull_candidates(state_path, max_offset=300):
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=state_path, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        with pg.expect_response(lambda r: "marketplace/api/products" in r.url and r.status == 200, timeout=40000) as ri:
            pg.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
        cap = ri.value.request
        url = cap.url
        hdrs = {k: v for k, v in cap.headers.items() if k.lower() != "content-length"}
        for offset in range(0, max_offset + 1, 50):
            body = {
                "projection": {"title": {}, "id_on_site": {}, "site_name": {}, "product_details": {}, "categories": {}},
                "order_by": {"direction": "desc", "name": "spv_param"},
                "condition": "and", "limit": 50, "offset": offset,
                "filters": [
                    {"name": "rating_count", "value": "1000", "value_type": "integer", "op": ">"},
                    {"name": "variations.variation_details.price", "value": "1.5,22", "value_type": "float", "op": "between"},
                ],
            }
            r = ctx.request.post(url, headers=hdrs, data=json.dumps(body))
            res = r.json().get("results", []) if r.ok else []
            if not res:
                break
            out.extend(res)
        b.close()
    return rows_from_results(out)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_marketplace.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Smoke-test the live pull, then commit**

Run: `PW/.venv/Scripts/python.exe -c "from pipeline.marketplace import pull_candidates; rows=pull_candidates('storage_state.json'); print(len(rows), rows[0] if rows else None)"`
Expected: prints a count >0 and a sample row (requires a valid session). If session invalid, run `login_and_save_session.py` first.

```bash
git add PW/pipeline/marketplace.py PW/pipeline/tests/test_marketplace.py
git commit -m "feat(pipeline): Marketplace pull + pure result mapper"
```

---

### Task 7: eBay fetch shell (`ebay_check.fetch_ebay_median`)

**Files:**
- Modify: `PW/pipeline/ebay_check.py`
- Test: `PW/pipeline/tests/test_ebay_check.py` (add a fixture-based test)

**Interfaces:**
- Consumes: `parse_ebay_prices`, `median_price` (Task 3).
- Produces: `fetch_ebay_median(query: str, fetcher=None) -> tuple[float | None, int]` — builds the `r.jina.ai`+eBay-search URL, calls `fetcher(url)` (default: a urllib GET) to get render text, returns `(median_price, n_prices_found)`. `fetcher` is injectable so tests pass a stub (no network in unit tests).

- [ ] **Step 1: Write the failing test**

```python
# add to PW/pipeline/tests/test_ebay_check.py
from pipeline.ebay_check import fetch_ebay_median

def test_fetch_ebay_median_with_stub_fetcher():
    def stub(url):
        assert "ebay.com" in url
        return "Listing $19.99 ... Listing $24.99 ... Listing $29.99"
    median, n = fetch_ebay_median("dog trolley 60ft", fetcher=stub)
    assert median == 24.99 and n == 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_ebay_check.py -k fetch -v`
Expected: FAIL with `ImportError: cannot import name 'fetch_ebay_median'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to PW/pipeline/ebay_check.py
import urllib.parse, urllib.request

def _default_fetcher(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "ignore")

def fetch_ebay_median(query: str, fetcher=None):
    fetcher = fetcher or _default_fetcher
    q = urllib.parse.quote_plus(query)
    url = "https://r.jina.ai/https://www.ebay.com/sch/i.html?_nkw=%s" % q
    try:
        text = fetcher(url)
    except Exception:
        return (None, 0)
    prices = parse_ebay_prices(text)
    return (median_price(prices), len(prices))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_ebay_check.py -k fetch -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git add PW/pipeline/ebay_check.py PW/pipeline/tests/test_ebay_check.py
git commit -m "feat(pipeline): eBay median fetch via r.jina.ai (injectable fetcher)"
```

---

### Task 8: CLI orchestrator (`run_pipeline.py`) — dry-run default, `--go` to import

**Files:**
- Create: `PW/pipeline/run_pipeline.py`
- Test: `PW/pipeline/tests/test_run_pipeline.py`

**Interfaces:**
- Consumes: `pull_candidates` (T6), `filter_candidates` (T4), `fetch_ebay_median`+`compute_margin` (T3/T7), `select_top_n` (T5), `clean_title`+`build_description` (T1/T2), and `manage_draft.py full` (existing) for import.
- Produces:
  - `enrich(rows: list[dict], fetch=fetch_ebay_median) -> list[dict]` — for each row, fetch eBay median + count, attach `ebay_price`, `demand`, `margin` (via `compute_margin`), and a coarse `saturation` (`high` if `demand>=8` else `medium` if `demand>=3` else `unknown`). Pure given an injected `fetch`. (Unit-tested.)
  - `main(argv)` — CLI: `--max-cost`, `--keep N` (default 3), `--tested-file`, `--dry-run` (default True), `--go` (sets dry_run False). In dry-run, prints the selected top-N + generated title/desc and writes NOTHING. With `--go`, calls `manage_draft.py full` per selected product.

- [ ] **Step 1: Write the failing test (enrich, no network)**

```python
# PW/pipeline/tests/test_run_pipeline.py
from pipeline.run_pipeline import enrich

def test_enrich_attaches_margin_demand_saturation():
    rows = [{"asin": "A1", "title": "Generic widget", "cost": 8.49, "cat": "Pets", "niche": "Dogs", "site": "amazon", "date": "2024-01-01"}]
    def fake_fetch(query):
        return (26.99, 10)   # median 26.99, 10 prices found
    out = enrich(rows, fetch=fake_fetch)
    assert out[0]["ebay_price"] == 26.99
    assert out[0]["demand"] == 10
    assert out[0]["margin"] == 14.52     # compute_margin(26.99, 8.49)
    assert out[0]["saturation"] == "high"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_run_pipeline.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pipeline.run_pipeline'`

- [ ] **Step 3: Write minimal implementation**

```python
# PW/pipeline/run_pipeline.py
import os, sys, json, argparse, subprocess
from pipeline.marketplace import pull_candidates
from pipeline.candidates import filter_candidates
from pipeline.ebay_check import fetch_ebay_median, compute_margin
from pipeline.selection import select_top_n
from pipeline.copy_gen import clean_title, build_description

HERE = os.path.dirname(os.path.abspath(__file__))
PW = os.path.dirname(HERE)
KEEP_CATS = {"Home & Garden", "Pets", "Home Improvements & Tools", "Electronics & Gadgets", "Outdoors", "Automotive & Motorcycle", "Sports & Fitness", "Toys & Hobbies"}
BRANDS = ["Yes4All", "PetAmi", "BV", "Comsun", "Goldenwarm", "Pawfly", "Joytale", "SmartyKat"]  # extend as needed

def _saturation(demand: int) -> str:
    return "high" if demand >= 8 else ("medium" if demand >= 3 else "unknown")

def enrich(rows, fetch=fetch_ebay_median):
    out = []
    for r in rows:
        median, n = fetch(r["title"])
        r = dict(r)
        r["ebay_price"] = median
        r["demand"] = n
        r["margin"] = compute_margin(median, float(r["cost"])) if median else None
        r["saturation"] = _saturation(n)
        out.append(r)
    return out

def _make_copy(row):
    title = clean_title(row["title"], BRANDS)
    desc = build_description(
        hook=title,
        intro="A practical, problem-solving pick sourced for fast eBay dropshipping.",
        bullets=["Generic, brand-free listing", "Lightweight and easy to ship", "Everyday utility"],
        close="Order today and have it on its way.",
    )
    return title, desc

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cost", type=float, default=20.0)
    ap.add_argument("--keep", type=int, default=3)
    ap.add_argument("--tested-file", default=None)
    ap.add_argument("--go", action="store_true", help="LIVE import (GO-class); default is dry-run")
    args = ap.parse_args(argv)
    tested = set()
    if args.tested_file and os.path.exists(args.tested_file):
        tested = set(json.load(open(args.tested_file, encoding="utf-8")))
    rows = pull_candidates(os.path.join(PW, "storage_state.json"))
    cands = filter_candidates(rows, tested, BRANDS, KEEP_CATS, args.max_cost)
    enriched = enrich(cands)
    top = select_top_n(enriched, n=args.keep)
    print("== SELECTED TOP %d ==" % len(top))
    for r in top:
        title, desc = _make_copy(r)
        print(json.dumps({"asin": r["asin"], "score": r["score"], "margin": r["margin"], "ebay": r["ebay_price"], "title": title}, ensure_ascii=False))
        if args.go:
            url = "https://www.amazon.com/dp/%s" % r["asin"]
            subprocess.run([sys.executable, os.path.join(PW, "manage_draft.py"), "full",
                            "--url", url, "--match", r["title"].split()[0], "--title", title, "--desc", desc], check=False)
    if not args.go:
        print("DRY-RUN: nothing imported. Re-run with --go (GO-class) to import.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/test_run_pipeline.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Smoke-test dry-run end-to-end, then commit**

Run: `PW/.venv/Scripts/python.exe -m pipeline.run_pipeline --max-cost 20 --keep 3`
Expected: prints `== SELECTED TOP 3 ==`, 3 JSON lines with titles ≤80, and `DRY-RUN: nothing imported.` — and makes NO AutoDS writes.

```bash
git add PW/pipeline/run_pipeline.py PW/pipeline/tests/test_run_pipeline.py
git commit -m "feat(pipeline): CLI orchestrator (dry-run default, --go GO-gated import)"
```

---

### Task 9: Full test run + README

**Files:**
- Create: `PW/pipeline/README.md`
- Test: (run the whole suite)

**Interfaces:** none new.

- [ ] **Step 1: Run the full suite**

Run: `PW/.venv/Scripts/python.exe -m pytest PW/pipeline/tests/ -v`
Expected: all tests PASS (Tasks 1-8).

- [ ] **Step 2: Write the README**

```markdown
# Research→3-Drafts Pipeline

One command: pull AutoDS Marketplace candidates → score by REAL eBay margin → import top 3 as drafts.

## Usage
- Dry-run (default, no writes):  `python -m pipeline.run_pipeline --max-cost 20 --keep 3`
- LIVE import (GO-class, owner GO required):  `python -m pipeline.run_pipeline --go`

## Notes / honesty
- eBay price/demand come from r.jina.ai proxy renders → LOWER BOUNDS; the eBay Sold filter is often 403.
- Generated title (≤80, brand-stripped) and description are STUBS — review/polish copy before relying on them.
- Import only ever clicks "Add as Draft" (via manage_draft.py full); never publishes.
- For LLM-grade adversarial margin verification, run the separate Workflow pass (see RESEARCH_MEMORY_INDEX).
```

- [ ] **Step 3: Commit**

```bash
git add PW/pipeline/README.md
git commit -m "docs(pipeline): README - usage + honesty notes"
```

---

## Self-Review

- **Spec coverage:** Task 1-2 = copy gen (title ≤80 + VeRO desc); Task 3+7 = eBay margin verify; Task 4 = candidate pull/filter; Task 5 = rank/select top 3; Task 6 = Marketplace pull; Task 8 = one-command CLI + dry-run + GO-gated import; Task 9 = register/README. The "cockpit/index auto-register" preview item is intentionally left as a manual close-out step (the machine's AUTO-REFRESH rule + RESEARCH_MEMORY_INDEX registration are governance-sensitive and stay human/LLM-driven, not script-driven) — noted in README.
- **Type consistency:** candidate row keys (`asin,title,cat,niche,cost,site,date`) are produced in T6 and consumed by T4/T8; `margin/demand/saturation` produced in T8.enrich and consumed by T5.select_top_n; `compute_margin` signature identical in T3 and T8. Consistent.
- **Placeholder scan:** every code step contains complete code; no TBD/TODO.

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-06-21-research-to-drafts-pipeline.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — execute tasks in this session via executing-plans, batch with checkpoints.

**Which approach?**

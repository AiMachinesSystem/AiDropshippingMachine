#!/usr/bin/env python3
"""
Playwright BROWSER CONNECTIVITY smoke test for AutoDS (Step 1 — no login, no actions).

SAFETY CONTRACT (do not weaken):
- Opens a HEADLESS browser and navigates to a single PUBLIC URL (platform.autods.com).
- NO login, NO typing of credentials, NO clicks, NO form submits, NO writes anywhere.
- NO secrets are read, printed, or stored. This is a read-only "does the browser work" probe.
- Takes ONE screenshot of whatever public page loads and saves it to the requested path.
- Exits non-zero with a clear message on any failure. Always closes the browser.

GO scope: owner explicitly requested a browser connectivity test (navigate + screenshot only).
"""
import os
import sys
import argparse


TARGET_URL = "https://platform.autods.com"
DEFAULT_OUT_RELATIVE = os.path.join("10_OUTPUTS", "playwright_test.png")


def find_repo_root(start):
    """Ascend from `start` until a directory containing 10_OUTPUTS (and CLAUDE.md) is found."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def resolve_out_path(cli_out):
    if cli_out:
        return os.path.abspath(cli_out)
    root = find_repo_root(os.path.dirname(os.path.abspath(__file__)))
    if root:
        return os.path.join(root, DEFAULT_OUT_RELATIVE)
    # last resort: write next to this script
    return os.path.abspath(DEFAULT_OUT_RELATIVE)


def main():
    parser = argparse.ArgumentParser(description="Playwright browser connectivity smoke test (no login).")
    parser.add_argument("--out", default=None, help="Absolute path for the screenshot PNG.")
    parser.add_argument("--url", default=TARGET_URL, help="URL to open (default: platform.autods.com).")
    parser.add_argument("--timeout", type=int, default=45000, help="Navigation timeout in ms (default 45000).")
    args = parser.parse_args()

    out_path = resolve_out_path(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL: the 'playwright' package is not importable in this interpreter.")
        print("      Activate the venv and run: pip install -r requirements.txt && python -m playwright install chromium")
        return 3

    print("Playwright browser connectivity smoke test (HEADLESS — no login, no actions).")
    print("  target url  :", args.url)
    print("  screenshot  :", out_path)
    print("  timeout(ms) :", args.timeout)
    print("-" * 60)

    status = None
    final_url = None
    title = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(
                    viewport={"width": 1366, "height": 900},
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                    ),
                )
                page = context.new_page()
                print("  [..] launching chromium + navigating ...")
                response = page.goto(args.url, wait_until="load", timeout=args.timeout)
                status = response.status if response else None
                # let client-side app render a bit (no interaction)
                try:
                    page.wait_for_timeout(2500)
                except Exception:
                    pass
                final_url = page.url
                try:
                    title = page.title()
                except Exception:
                    title = None
                page.screenshot(path=out_path, full_page=True)
            finally:
                browser.close()
    except Exception as e:  # noqa: BLE001
        print("  [ERR] %s: %s" % (type(e).__name__, e))
        print("-" * 60)
        print("RESULT: FAIL — browser could not complete the navigation/screenshot.")
        return 1

    size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print("  [ok] navigation complete")
    print("  http_status :", status)
    print("  final_url   :", final_url)
    print("  page_title  :", repr(title))
    print("  screenshot  : %s (%d bytes)" % (out_path, size))
    print("-" * 60)
    if size > 0:
        print("RESULT: PASS — headless browser worked, page loaded, screenshot saved.")
        return 0
    print("RESULT: FAIL — no screenshot bytes written.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

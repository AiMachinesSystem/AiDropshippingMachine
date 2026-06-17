#!/usr/bin/env python3
"""
AutoDS login + session saver (Playwright) — Step 2.

WHAT IT DOES
- Reads AUTODS_EMAIL / AUTODS_PASSWORD from a LOCAL `autods_credentials.env` (gitignored).
- Opens a VISIBLE (non-headless) Chromium so you can watch every step.
- Navigates to platform.autods.com, fills the login form, clicks "Log in".
- WAITS for login to complete (so you can finish any 2FA / captcha by hand in the window).
- On success, saves the authenticated session to `storage_state.json` (gitignored) and closes the browser.

SAFETY CONTRACT (do not weaken)
- This is the ONE script that performs a real login (account access) — it runs ONLY after the owner's explicit GO.
- Secrets are read from the local .env ONLY. The email/password VALUES are NEVER printed or logged.
- It performs login ONLY: no import, no publish, no pricing, no orders, no other writes.
- If credentials are missing (and not --manual), it fails safely without opening a browser.
- The saved storage_state.json contains session cookies/tokens — it is gitignored and must never be committed.

GO scope: GO_PLAYWRIGHT_LOGIN (login + save session only).
"""
import os
import re
import sys
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(HERE, "autods_credentials.env")
DEFAULT_STATE = os.path.join(HERE, "storage_state.json")
LOGIN_URL = "https://platform.autods.com"


def load_credentials():
    """Read AUTODS_EMAIL / AUTODS_PASSWORD from the local .env (env vars override). Values never printed."""
    creds = {}
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    for k in ("AUTODS_EMAIL", "AUTODS_PASSWORD"):
        if not creds.get(k) and os.environ.get(k):
            creds[k] = os.environ[k]
    return creds.get("AUTODS_EMAIL", ""), creds.get("AUTODS_PASSWORD", "")


def locate(page, strategies, label, timeout=12000):
    """Return the first locator (from ordered strategies) that becomes visible, else raise."""
    for make in strategies:
        try:
            loc = make().first
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except Exception:
            continue
    raise RuntimeError("Could not locate the %s element on the page." % label)


def main():
    parser = argparse.ArgumentParser(description="AutoDS login + save session (Playwright, visible browser).")
    parser.add_argument("--state", default=DEFAULT_STATE, help="Where to save storage_state.json.")
    parser.add_argument("--url", default=LOGIN_URL, help="Login URL (default platform.autods.com).")
    parser.add_argument("--manual", action="store_true",
                        help="Do NOT auto-fill; you log in by hand (Google/2FA). Script just waits + saves.")
    parser.add_argument("--login-timeout", type=int, default=180000,
                        help="Max ms to wait for login to complete (default 180000 = 3 min; covers 2FA).")
    parser.add_argument("--slowmo", type=int, default=120, help="Slow down actions by N ms so you can watch.")
    parser.add_argument("--keep-open", action="store_true", help="Leave the browser open after saving.")
    args = parser.parse_args()

    email, password = load_credentials()
    if not args.manual and (not email or not password):
        print("CREDENTIAL ACTION REQUIRED")
        print("  Fill AUTODS_EMAIL and AUTODS_PASSWORD in:")
        print("   ", CRED_FILE)
        print("  (or run with --manual to log in by hand). Nothing was opened.")
        return 2

    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("FAIL: 'playwright' not importable. Activate the venv and: pip install -r requirements.txt")
        return 3

    print("AutoDS login + save session (VISIBLE browser).")
    print("  mode        :", "MANUAL (you log in by hand)" if args.manual else "auto-fill credentials")
    print("  email       :", "present (value hidden)" if email else "(not set)")
    print("  password    :", "present (value hidden)" if password else "(not set)")
    print("  url         :", args.url)
    print("  save state  :", args.state)
    print("-" * 64)

    logged_in = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=args.slowmo)
            context = browser.new_context(
                viewport={"width": 1366, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()
            print("  [..] opening", args.url)
            page.goto(args.url, wait_until="load", timeout=60000)

            if not args.manual:
                print("  [..] filling email + password and clicking Log in")
                email_el = locate(page, [
                    lambda: page.get_by_placeholder("Enter email"),
                    lambda: page.locator("input[type='email']"),
                    lambda: page.locator("input[name='email']"),
                    lambda: page.get_by_label("Email Address"),
                ], "email")
                email_el.fill(email)

                pwd_el = locate(page, [
                    lambda: page.get_by_placeholder("Enter password"),
                    lambda: page.locator("input[type='password']"),
                    lambda: page.locator("input[name='password']"),
                    lambda: page.get_by_label("Password"),
                ], "password")
                pwd_el.fill(password)

                btn = locate(page, [
                    lambda: page.get_by_role("button", name=re.compile(r"log\s*in", re.I)),
                    lambda: page.locator("button[type='submit']"),
                ], "Log in button")
                btn.click()
            else:
                print("  [..] MANUAL mode — please log in inside the browser window now.")

            print("  [..] waiting up to %ds for login to complete" % (args.login_timeout // 1000))
            print("       (if 2FA / captcha appears, complete it in the window)")
            try:
                page.wait_for_url(lambda u: "/login" not in u, timeout=args.login_timeout)
                logged_in = True
            except PWTimeout:
                logged_in = "/login" not in page.url

            if logged_in:
                # small settle so post-login tokens/cookies are set before snapshotting
                try:
                    page.wait_for_timeout(2500)
                except Exception:
                    pass
                context.storage_state(path=args.state)
                print("  [ok] login detected — current url:", page.url)
                print("  [ok] session saved to:", args.state)
            else:
                print("  [!!] still on the login page — login did NOT complete.")
                print("       Check credentials / 2FA / captcha. Session NOT saved.")

            if args.keep_open:
                print("  [..] --keep-open set; close the browser window manually when done.")
                try:
                    page.wait_for_event("close", timeout=0)
                except Exception:
                    pass
            browser.close()
    except Exception as e:  # noqa: BLE001
        print("  [ERR] %s: %s" % (type(e).__name__, e))
        print("-" * 64)
        print("RESULT: FAIL — login flow errored. Session NOT saved.")
        return 1

    print("-" * 64)
    if logged_in and os.path.exists(args.state):
        size = os.path.getsize(args.state)
        print("RESULT: PASS — logged in and session saved (%d bytes). Reuse it via storage_state=." % size)
        return 0
    print("RESULT: FAIL — login not completed; no session saved.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

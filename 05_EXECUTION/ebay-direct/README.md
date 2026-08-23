# eBay Direct — Production listing client (Sell Inventory API)

Local Deno/TypeScript CLI that replaces the AutoDS write path for `EBAY_US`
listings. It owns OAuth, redacted API access, manifest validation, action-pack
hashing, protected idempotent writes, read-back verification, and a token-free
audit trail. It talks only to the Production endpoints — never Sandbox.

The existing Deno Deploy webhook (`05_EXECUTION/ebay-api-compliance/`) is
unchanged and keeps handling account-deletion notifications only.

## Non-negotiables

- **Production only.** `https://api.ebay.com`, `https://auth.ebay.com`,
  marketplace `EBAY_US`, seller `divinit-92`.
- **Secrets live only in gitignored files.** Client Secret, refresh token,
  OAuth state and the redirect URL go in `.env.local` or `*.local` — never on the
  command line, never in a commit. `git grep` secret scans gate every run.
- **No external write without an exact action pack + SHA-256 in the Owner GO.**
  The pack hash is recomputed deterministically, so the Owner can name the exact
  bytes being authorized. A generic or earlier GO never authorizes a new write.
- **A chat GO is never translated into `--owner-go`.** The CLI rejects
  `--token`, `--secret`, `--code` and `--owner-go` flags outright.
- **Listings are managed here, not in Seller Hub.** Inventory API items must not
  be edited through Seller Hub — that would silently diverge from the hashed
  remote state this client reads back.

## Setup

Copy `.env.example` to `.env.local` and fill only the secret fields:

| Key | Meaning |
|---|---|
| `EBAY_CLIENT_ID` | Production application client id |
| `EBAY_CLIENT_SECRET` | Production application client secret |
| `EBAY_RUNAME` | Production OAuth redirect RuName |
| `EBAY_REFRESH_TOKEN` | Written by `oauth-exchange`, not by hand |

`EBAY_API_BASE_URL` and `EBAY_AUTH_BASE_URL` default to the Production hosts and
must never be pointed at Sandbox (`loadConfig` fails closed on Sandbox).

## Command order

Each command is one stage. There is no `publish-all` shortcut — every write is
named individually and gated individually.

```
# 1. Authorization (live, inline, GO-gated)
deno task cli oauth-start                       # prints consent URL, writes .oauth-state.local
#   open the URL, verify seller divinit-92, accept; capture the redirect URL
#   write the redirect URL into .oauth-redirect.local (do not print it)
deno task cli oauth-exchange                    # exchanges code, writes EBAY_REFRESH_TOKEN, deletes transient files

# 2. Read-only seller bootstrap (live, no write)
deno task cli bootstrap                         # prints AccountBootstrap JSON (policies, locations, SKUs)

# 3. Local validation and dry-run (no network, no write to eBay)
deno task cli validate   --manifest manifests/X.json --bootstrap bootstrap.json
deno task cli dry-run    --manifest manifests/X.json --bootstrap bootstrap.json   # writes action-packs/<sku>.json

# 4. Protected writes — each requires --action-pack and --expected-sha256
deno task cli apply-inventory --action-pack action-packs/<sku>.json --expected-sha256 <64-hex> --manifest manifests/X.json
deno task cli create-offer    --action-pack action-packs/<sku>.json --expected-sha256 <64-hex> --manifest manifests/X.json
deno task cli publish-offer   --action-pack action-packs/<sku>.json --expected-sha256 <64-hex> --offer-id <id>
deno task cli verify          --action-pack action-packs/<sku>.json --expected-sha256 <64-hex> --offer-id <id> --listing-id <id> --price <val> --quantity <n>
deno task cli withdraw        --action-pack action-packs/<sku>.json --expected-sha256 <64-hex> --offer-id <id>
```

`validate` and `dry-run` are fully local and need no credentials. `bootstrap`
is read-only but live. Every write command refuses to send anything unless the
pack hash and the per-stage payload hash both match.

## Evidence labels

Manifests carry source evidence with a checked-at timestamp. The validator
refuses evidence older than 24 hours, delivery later than 10 days, and net profit
below `$5.00` or below 20% of sale price. Every numeric claim in a manifest
names its source URL and timestamp; nothing is invented.

## Expected outputs

- `dry-run` prints `{ sku, packSha256 }` and writes `action-packs/<sku>.json`.
- `apply-inventory` prints `{ sku, outcome: "created" | "unchanged" }`.
- `create-offer` prints `{ offerId, outcome: "created" | "reused" }`.
- `publish-offer` prints `{ offerId, listingId, outcome }`.
- `verify` prints `{ verified, listingId, offerId, sku, price, quantity }`.
- `withdraw` prints `{ offerId, outcome: "withdrawn" | "already_ended" }`.

Audit records are appended to `audit/<sku>.jsonl` (see `audit.ts`) and are
token-free by construction — a key matching `token|secret|authorization|buyer|
username|email|address` is rejected before it is written.

## Recovery

- **State conflict** (`REMOTE_STATE_CONFLICT`): the remote object differs from the
  intended payload and is never overwritten. Read the current remote state before
  deciding the next action.
- **Verification failure** (`VERIFY_FAILED`): a published listing does not match.
  Later batch items stay frozen; nothing is silently retried.
- **Publish timeout**: `publish-offer` reads the offer back before retrying, so a
  listing that was actually created is returned as `already_published` instead of
  being published twice.

## Checks

```
deno task check   # fmt + lint + unit tests + type-check
```

## Security scan

```
git grep -n -I -E 'v\^1\.|Bearer [A-Za-z0-9]|EBAY_CLIENT_SECRET=.+|EBAY_REFRESH_TOKEN=.+' -- ':!**/.env.local' ':!**/*.local'
```

Expected: no matches.

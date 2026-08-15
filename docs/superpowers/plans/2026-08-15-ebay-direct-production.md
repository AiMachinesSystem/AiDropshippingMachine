# eBay Direct Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and prove a local eBay Production client that replaces AutoDS and can validate, create, and publish five exact `EBAY_US` listings through the Sell Inventory API.

**Architecture:** A local Deno/TypeScript CLI owns OAuth, redacted API access, manifest validation, action-pack hashing, protected writes, and audit records. The existing Deno Deploy webhook remains unchanged and continues to handle only account-deletion notifications. OAuth and every live write run inline in the primary session; no subagent receives secrets or live-surface tools.

**Tech Stack:** Deno 2, TypeScript, Web `fetch`/Web Crypto APIs, `@std/assert`, eBay REST Sell Inventory and Account APIs.

**Spec:** `docs/superpowers/specs/2026-08-15-ebay-direct-production-design.md`

## Global Constraints

- Production only: `https://api.ebay.com`, `https://auth.ebay.com`, marketplace `EBAY_US`, seller `divinit-92`.
- Do not import, call, or update AutoDS code; historical AutoDS data is `STALE` research only.
- Minimum OAuth scopes: `sell.inventory` and `sell.account.readonly`; do not request `sell.account` in milestone one.
- Store Client Secret, refresh token, transient OAuth redirect and state only in gitignored `05_EXECUTION/ebay-direct/.env.local` or `*.local` files.
- Never print access tokens, refresh tokens, authorization codes, Client Secret, buyer data, or raw request headers.
- No external write without an exact action pack and SHA-256 identified in the Owner GO.
- Never translate a chat GO into an `--owner-go` flag or an approval-ledger command.
- Tasks 1–7 are internal/reversible. Tasks 8–10 handle credentials or live surfaces and must execute inline in the primary session.
- Do not modify `05_EXECUTION/ebay-api-compliance`; its public Deno webhook has a separate responsibility.

## File Map

- `05_EXECUTION/ebay-direct/deno.json` — tasks, imports, formatting/lint/test contract.
- `05_EXECUTION/ebay-direct/.env.example` — key names and non-secret configuration examples.
- `05_EXECUTION/ebay-direct/README.md` — operator contract and exact safe commands.
- `05_EXECUTION/ebay-direct/types.ts` — shared config, manifest, action-pack and audit types.
- `05_EXECUTION/ebay-direct/config.ts` — strict environment loading without logging values.
- `05_EXECUTION/ebay-direct/redaction.ts` — recursive credential/PII-safe error rendering.
- `05_EXECUTION/ebay-direct/oauth.ts` — state, consent URL, code exchange, refresh and introspection.
- `05_EXECUTION/ebay-direct/api_client.ts` — authenticated fetch, bounded retry and structured eBay errors.
- `05_EXECUTION/ebay-direct/account.ts` — read-only policies, privileges, locations and duplicate bootstrap.
- `05_EXECUTION/ebay-direct/manifest.ts` — manifest parser and local validation.
- `05_EXECUTION/ebay-direct/payloads.ts` — Inventory Item/Offer request builders and canonical hashes.
- `05_EXECUTION/ebay-direct/action_pack.ts` — dry-run artifact construction and verification.
- `05_EXECUTION/ebay-direct/publisher.ts` — idempotent inventory/offer/publish/withdraw stages.
- `05_EXECUTION/ebay-direct/audit.ts` — append-only redacted JSONL records.
- `05_EXECUTION/ebay-direct/cli.ts` — command routing; secrets never accepted as CLI flags.
- `05_EXECUTION/ebay-direct/*_test.ts` — focused unit and contract tests beside each component.
- `05_EXECUTION/ebay-direct/fixtures/` — fake eBay responses and invalid/valid sample manifests.
- `05_EXECUTION/ebay-direct/manifests/` — five future, non-secret listing manifests.
- `05_EXECUTION/ebay-direct/action-packs/` — generated redacted dry-run packs.
- `05_EXECUTION/ebay-direct/audit/` — redacted verification records; token-free by construction.

---

### Task 1: Package foundation, types, configuration and redaction

**Files:**
- Create: `05_EXECUTION/ebay-direct/deno.json`
- Create: `05_EXECUTION/ebay-direct/.env.example`
- Create: `05_EXECUTION/ebay-direct/types.ts`
- Create: `05_EXECUTION/ebay-direct/config.ts`
- Create: `05_EXECUTION/ebay-direct/redaction.ts`
- Test: `05_EXECUTION/ebay-direct/config_test.ts`
- Test: `05_EXECUTION/ebay-direct/redaction_test.ts`

**Interfaces:**
- Produces: `loadConfig(env): EbayConfig`, `redact(value, secrets): unknown`, `safeError(error, secrets): SafeError`.
- `EbayConfig` contains `clientId`, `clientSecret`, `ruName`, `refreshToken`, `marketplaceId: "EBAY_US"`, `locale: "en-US"`, `baseUrl`, and `authUrl`.

- [ ] **Step 1: Write failing configuration and redaction tests**

```ts
Deno.test("loadConfig rejects Sandbox endpoints", () => {
  assertThrows(() => loadConfig({
    EBAY_CLIENT_ID: "client",
    EBAY_CLIENT_SECRET: "secret",
    EBAY_RUNAME: "runame",
    EBAY_REFRESH_TOKEN: "refresh",
    EBAY_API_BASE_URL: "https://api.sandbox.ebay.com",
  }), Error, "Production");
});

Deno.test("redact removes nested credentials", () => {
  const value = { headers: { authorization: "Bearer access-value" }, refresh: "refresh-value" };
  assertEquals(JSON.stringify(redact(value, ["access-value", "refresh-value"])).includes("value"), false);
});
```

- [ ] **Step 2: Run the tests and verify failure**

Run: `deno test config_test.ts redaction_test.ts` from `05_EXECUTION/ebay-direct`  
Expected: FAIL because modules/functions do not exist.

- [ ] **Step 3: Implement strict config and recursive redaction**

```ts
export interface EbayConfig {
  clientId: string;
  clientSecret: string;
  ruName: string;
  refreshToken: string;
  marketplaceId: "EBAY_US";
  locale: "en-US";
  baseUrl: "https://api.ebay.com";
  authUrl: "https://auth.ebay.com";
}

export function redact(value: unknown, secrets: readonly string[]): unknown {
  const scrub = (text: string) => secrets.filter(Boolean)
    .reduce((out, secret) => out.split(secret).join("[REDACTED]"), text)
    .replace(/Bearer\s+[^\s"']+/gi, "Bearer [REDACTED]");
  if (typeof value === "string") return scrub(value);
  if (Array.isArray(value)) return value.map((item) => redact(item, secrets));
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) =>
      [key, /token|secret|authorization|code/i.test(key) ? "[REDACTED]" : redact(item, secrets)]
    ));
  }
  return value;
}
```

- [ ] **Step 4: Add `deno task check` and a secret-safe `.env.example`**

`deno.json` tasks:

```json
{
  "tasks": {
    "check": "deno fmt --check *.ts && deno lint *.ts && deno test --allow-read --allow-env *_test.ts && deno check cli.ts",
    "cli": "deno run --allow-net=api.ebay.com,auth.ebay.com --allow-read=.env.local,*.local,manifests,action-packs,audit --allow-write=.env.local,*.local,action-packs,audit --allow-env cli.ts"
  },
  "imports": { "@std/assert": "jsr:@std/assert@^1.0.14" }
}
```

- [ ] **Step 5: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: add eBay direct secure foundation" -- 05_EXECUTION/ebay-direct`

---

### Task 2: OAuth authorization-code flow

**Files:**
- Create: `05_EXECUTION/ebay-direct/oauth.ts`
- Test: `05_EXECUTION/ebay-direct/oauth_test.ts`
- Create: `05_EXECUTION/ebay-direct/fixtures/oauth_token.json`

**Interfaces:**
- Consumes: `EbayConfig`, `redact`, injected `fetch`.
- Produces: `createOAuthState(): string`, `buildConsentUrl(config, state): URL`, `parseRedirect(url, expectedState): string`, `exchangeCode(fetcher, config, code): Promise<TokenGrant>`, `refreshAccessToken(fetcher, config): Promise<AccessGrant>`.

- [ ] **Step 1: Write failing tests for state, scopes and redirect validation**

```ts
Deno.test("consent URL is Production and least-privilege", () => {
  const url = buildConsentUrl(testConfig, "state-123");
  assertEquals(url.origin, "https://auth.ebay.com");
  assertEquals(url.searchParams.get("response_type"), "code");
  assertEquals(url.searchParams.get("redirect_uri"), testConfig.ruName);
  assertEquals(url.searchParams.get("scope")?.split(" ").sort(), [
    "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
  ]);
});

Deno.test("redirect state mismatch fails closed", () => {
  assertThrows(() => parseRedirect(
    new URL("https://example.invalid/?state=wrong&code=single-use"),
    "expected",
  ), Error, "state");
});
```

- [ ] **Step 2: Run tests and verify failure**

Run: `deno test oauth_test.ts`  
Expected: FAIL because OAuth functions do not exist.

- [ ] **Step 3: Implement consent URL and state verification**

```ts
const OAUTH_SCOPES = [
  "https://api.ebay.com/oauth/api_scope/sell.inventory",
  "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
] as const;

export function createOAuthState(): string {
  return crypto.randomUUID() + crypto.randomUUID();
}
```

`buildConsentUrl` must set `client_id`, `redirect_uri` to the Production RuName,
`response_type=code`, `locale=en-US`, the two scopes, and state. `parseRedirect`
must reject missing/expired state, missing code, and any `error` query parameter.

- [ ] **Step 4: Implement code exchange and refresh with injected fetch**

Use `POST https://api.ebay.com/identity/v1/oauth2/token`, Basic
`base64(clientId:clientSecret)`, and form-encoded bodies. The exchange body is
`grant_type=authorization_code`, the single-use code and RuName. The refresh body
is `grant_type=refresh_token`, refresh token and the exact two scopes. Return
parsed grants; never log response bodies.

- [ ] **Step 5: Test successful and failing token responses**

Cover `200`, `400 invalid_grant`, `401 invalid_client`, malformed JSON and a test
asserting that `safeError` contains none of the fixture token strings.

- [ ] **Step 6: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: add eBay Production OAuth flow" -- 05_EXECUTION/ebay-direct`

---

### Task 3: Authenticated API client and read-only seller bootstrap

**Files:**
- Create: `05_EXECUTION/ebay-direct/api_client.ts`
- Create: `05_EXECUTION/ebay-direct/account.ts`
- Test: `05_EXECUTION/ebay-direct/api_client_test.ts`
- Test: `05_EXECUTION/ebay-direct/account_test.ts`
- Create: `05_EXECUTION/ebay-direct/fixtures/account_bootstrap.json`

**Interfaces:**
- Produces: `EbayApiClient.request<T>(request): Promise<T>`, `readBootstrap(client): Promise<AccountBootstrap>`.
- `AccountBootstrap` returns privilege metadata, payment/fulfillment/return policy IDs, enabled merchant location keys, and existing SKU/offer summaries.

- [ ] **Step 1: Write failing retry and redaction tests**

Test that `401` refreshes once, `409` never retries, `429` honors bounded retry,
`5xx` retries at most three times, and thrown `EbayApiError` exposes only status,
error IDs, domains, categories and redacted messages.

- [ ] **Step 2: Implement `EbayApiClient`**

```ts
export interface ApiRequest {
  method: "GET" | "POST" | "PUT";
  path: string;
  body?: unknown;
  write: boolean;
  idempotencyKey?: string;
}
```

Require `Authorization: Bearer`, `Content-Type: application/json`,
`Content-Language: en-US` and `X-EBAY-C-MARKETPLACE-ID: EBAY_US` where applicable.
Allow retries only for the rules above and never retry `POST .../publish` unless a
subsequent read proves that no listing was created.

- [ ] **Step 3: Write failing bootstrap aggregation tests**

Mock these exact reads:

- `GET /sell/account/v1/privilege`
- `GET /sell/account/v1/payment_policy?marketplace_id=EBAY_US`
- `GET /sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US`
- `GET /sell/account/v1/return_policy?marketplace_id=EBAY_US`
- `GET /sell/inventory/v1/location?limit=100`
- `GET /sell/inventory/v1/inventory_item?limit=100`
- `GET /sell/inventory/v1/offer?limit=100&marketplace_id=EBAY_US`

Assert that missing policy types, no enabled location, or seller restrictions
produce `ready: false` with explicit non-secret blocker codes.

- [ ] **Step 4: Implement pagination and `readBootstrap`**

Pagination must follow response `next` values only when they remain under
`https://api.ebay.com/`; reject cross-origin links. Return summaries without
buyer data or raw API response persistence.

- [ ] **Step 5: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: add eBay seller bootstrap audit" -- 05_EXECUTION/ebay-direct`

---

### Task 4: Listing manifest schema and evidence validator

**Files:**
- Create: `05_EXECUTION/ebay-direct/manifest.ts`
- Test: `05_EXECUTION/ebay-direct/manifest_test.ts`
- Create: `05_EXECUTION/ebay-direct/fixtures/manifest_valid.json`
- Create: `05_EXECUTION/ebay-direct/fixtures/manifest_invalid.json`

**Interfaces:**
- Produces: `parseManifest(value): ListingManifest`, `validateManifest(manifest, bootstrap, now): ValidationReport`.
- `ValidationReport` has `pass`, `errors`, `warnings`, `evidenceFreshAt`, and no secrets.

- [ ] **Step 1: Define and test the manifest contract**

```ts
export interface ListingManifest {
  version: 1;
  sku: string;
  marketplaceId: "EBAY_US";
  product: {
    title: string;
    description: string;
    aspects: Record<string, string[]>;
    imageUrls: string[];
  };
  condition: "NEW";
  categoryId: string;
  quantity: number;
  price: { value: string; currency: "USD" };
  merchantLocationKey: string;
  policies: { payment: string; fulfillment: string; return: string };
  evidence: {
    supplierUrl: string;
    sourceCheckedAt: string;
    stockObserved: number;
    supplierCostUsd: string;
    deliveryLatestDays: number;
    imageRights: "SUPPLIER_AUTHORIZED" | "OWNER_OWNED";
    vero: "PASS";
    estimatedEbayFeesUsd: string;
    estimatedFulfillmentUsd: string;
    estimatedNetProfitUsd: string;
  };
}
```

- [ ] **Step 2: Run tests and verify failure**

Run: `deno test manifest_test.ts`  
Expected: FAIL because parser/validator do not exist.

- [ ] **Step 3: Implement fail-closed validation**

Require SKU regex `^[A-Z0-9][A-Z0-9._-]{2,49}$`, title 1–80 characters,
description 1–4000 characters, 1–12 unique HTTPS image URLs, positive integer
quantity, two-decimal positive USD amounts, policies/location present in the
bootstrap, evidence no older than 24 hours, delivery latest ≤10 days, VeRO PASS,
and estimated net profit ≥$5.00 and ≥20% of sale price. Reject unknown fields.

- [ ] **Step 4: Add claim and duplicate guards**

Reject unsupported claim phrases unless an aspect/evidence field contains the
source fact. Initial blocked phrases: `BPA-Free`, `waterproof`, `safe`,
`streak-free`, `eye care`, trademark symbols and any brand not present in a
verified `Brand` aspect. Reject duplicate image URLs and SKUs already found in
bootstrap.

- [ ] **Step 5: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: validate direct eBay listing manifests" -- 05_EXECUTION/ebay-direct`

---

### Task 5: Canonical payloads, hashes and dry-run action packs

**Files:**
- Create: `05_EXECUTION/ebay-direct/payloads.ts`
- Create: `05_EXECUTION/ebay-direct/action_pack.ts`
- Test: `05_EXECUTION/ebay-direct/payloads_test.ts`
- Test: `05_EXECUTION/ebay-direct/action_pack_test.ts`

**Interfaces:**
- Produces: `buildInventoryPayload(manifest)`, `buildOfferPayload(manifest)`, `canonicalJson(value)`, `sha256Canonical(value)`, `buildActionPack(manifest, validation, bootstrap)`.

- [ ] **Step 1: Write failing canonicalization and payload tests**

Assert that different object key order yields the same SHA-256, array order is
preserved, numeric currency values remain strings, and the payloads contain no
supplier URL, supplier cost or audit-only evidence.

- [ ] **Step 2: Implement Inventory Item and Offer builders**

Inventory Item includes availability quantity, condition and product fields.
Offer includes SKU, marketplace, category, merchant location, quantity, price,
description and the three policy IDs. Builders must return new immutable values.

- [ ] **Step 3: Implement action-pack structure**

```ts
export interface ActionPack {
  version: 1;
  sku: string;
  manifestSha256: string;
  inventoryAction: { method: "PUT"; path: string; payloadSha256: string };
  offerAction: { method: "POST"; path: "/sell/inventory/v1/offer"; payloadSha256: string };
  publishAction: { method: "POST"; pathTemplate: "/sell/inventory/v1/offer/{offerId}/publish" };
  effect: string;
  risk: string;
  rollback: string;
  validation: { pass: true; checkedAt: string };
  packSha256: string;
}
```

Compute `packSha256` from the pack without its own hash. Refuse pack generation
unless validation PASS and bootstrap `ready: true`.

- [ ] **Step 4: Prove dry-run performs zero writes**

Use a fake client whose `request` throws if called with `write: true`; assert the
dry-run creates only a local JSON file under `action-packs/` and leaves the fake
write counter at zero.

- [ ] **Step 5: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: generate hashed eBay action packs" -- 05_EXECUTION/ebay-direct`

---

### Task 6: Idempotent protected writer, verification and rollback

**Files:**
- Create: `05_EXECUTION/ebay-direct/publisher.ts`
- Create: `05_EXECUTION/ebay-direct/audit.ts`
- Test: `05_EXECUTION/ebay-direct/publisher_test.ts`
- Test: `05_EXECUTION/ebay-direct/audit_test.ts`

**Interfaces:**
- Produces: `applyInventory`, `createOrReuseOffer`, `publishOffer`, `verifyPublished`, `withdrawOffer`, `appendAudit`.
- Every write consumes an `ActionPack` plus `expectedPackSha256` and rejects mismatch before HTTP.

- [ ] **Step 1: Write failing hash and idempotency tests**

Test mismatched hash → zero calls; existing identical inventory item → no PUT;
existing unpublished matching offer → reuse; publish timeout → read offer before
retry; existing listing ID → return verified success without a second publish.

- [ ] **Step 2: Implement inventory and offer stages**

Before PUT/POST, read current remote state and compare canonical payload hashes.
A remote mismatch blocks with `REMOTE_STATE_CONFLICT`; it never overwrites an
unknown object. Record offer ID only after a successful response parse.

- [ ] **Step 3: Implement publish and read-back**

Publish once, then read both offer and inventory item. Success requires listing
ID, `EBAY_US`, expected SKU, price and quantity. A missing/mismatched field yields
`VERIFY_FAILED` and freezes subsequent batch items.

- [ ] **Step 4: Implement separate withdrawal**

`withdrawOffer` requires its own withdrawal pack SHA-256 and reads back the offer
to confirm non-published state. It must never delete the inventory item.

- [ ] **Step 5: Implement redacted append-only audit**

Audit fields: timestamp, stage, SKU, action-pack hash, HTTP status, eBay error IDs,
offer ID, listing ID, verification result. Reject objects containing keys that
match `token|secret|authorization|buyer|username|email|address`.

- [ ] **Step 6: Run checks and commit**

Run: `deno task check`  
Expected: PASS.  
Commit: `git commit -m "feat: add protected eBay publishing stages" -- 05_EXECUTION/ebay-direct`

---

### Task 7: CLI, documentation and regression gate

**Files:**
- Create: `05_EXECUTION/ebay-direct/cli.ts`
- Create: `05_EXECUTION/ebay-direct/cli_test.ts`
- Create: `05_EXECUTION/ebay-direct/README.md`
- Modify: `05_EXECUTION/ebay-direct/deno.json`

**Interfaces:**
- Commands: `oauth-start`, `oauth-exchange`, `bootstrap`, `validate`, `dry-run`, `apply-inventory`, `create-offer`, `publish-offer`, `verify`, `withdraw`.
- Secrets come only from environment/files; commands reject `--token`, `--secret`, `--code` and `--owner-go` flags.

- [ ] **Step 1: Write failing CLI parsing tests**

Assert exact arguments, unknown-command failure, write commands requiring
`--action-pack` and `--expected-sha256`, and rejection of any secret-bearing flag.

- [ ] **Step 2: Implement command routing**

`oauth-start` writes `.oauth-state.local` with creation time and prints only the
consent URL. `oauth-exchange` reads `.oauth-redirect.local`, validates state,
exchanges the code, writes `EBAY_REFRESH_TOKEN` into `.env.local` without echo,
then deletes both transient `.local` files.

`bootstrap`, `validate`, `dry-run` are read-only. Write commands call only their
single named stage; there is no `publish-all` shortcut in milestone one.

- [ ] **Step 3: Write operator README**

Document exact command order, evidence labels, expected outputs, per-action GO
boundaries, recovery commands and the fact that Inventory API listings must be
managed through this client rather than Seller Hub.

- [ ] **Step 4: Run full checks and secret scan**

Run: `deno task check`  
Run: `git grep -n -I -E 'v\^1\.|Bearer [A-Za-z0-9]|EBAY_CLIENT_SECRET=.+|EBAY_REFRESH_TOKEN=.+' -- ':!**/.env.local' ':!**/*.local'`  
Expected: tests PASS and secret scan returns no matches.

- [ ] **Step 5: Commit**

Commit: `git commit -m "feat: complete eBay direct Production CLI" -- 05_EXECUTION/ebay-direct`

---

### Task 8: Production OAuth and read-only smoke test — inline only

**Files:**
- Create locally/gitignored: `05_EXECUTION/ebay-direct/.env.local`
- Create then delete: `05_EXECUTION/ebay-direct/.oauth-state.local`
- Create then delete: `05_EXECUTION/ebay-direct/.oauth-redirect.local`
- Create: `05_EXECUTION/ebay-direct/audit/bootstrap-production.json`

**Interfaces:**
- Consumes the Owner's existing exact authorization: `GO EBAY OAUTH PRD SELLER divinit-92`.
- Produces an active refresh token stored locally and a redacted `AccountBootstrap` audit.

- [ ] **Step 1: Load PRD Client ID/Secret without exposing values**

Read the already-authorized Production credentials from the logged-in eBay
Developer page into trusted process memory and write them to `.env.local` using a
secret-safe helper. Report only lengths and key names.

- [ ] **Step 2: Inspect or configure Production RuName**

Read the Production `Get a Token from eBay via Your Application` settings. Reuse
an existing OAuth-enabled RuName. If none exists, stop with one exact external
configuration action; do not invent the RuName or redirect URLs.

- [ ] **Step 3: Generate consent URL and obtain seller consent**

Run: `deno task cli oauth-start`  
Open the generated `auth.ebay.com` URL in the logged-in browser, verify the shown
application and seller `divinit-92`, then accept under the existing OAuth GO. If
eBay presents CAPTCHA or a different seller, stop and hand off to the Owner.

- [ ] **Step 4: Capture redirect securely and exchange once**

Write the final redirect URL into `.oauth-redirect.local` without printing it,
run `deno task cli oauth-exchange`, and verify the transient files are deleted.
Report only refresh-token presence, access-token active status, exact scopes and
introspected username.

- [ ] **Step 5: Run bootstrap smoke test**

Run: `deno task cli bootstrap --output audit/bootstrap-production.json`  
Expected: authenticated reads succeed and the audit contains no token. If
policies or locations are missing, record blockers and stop before any write.

- [ ] **Step 6: Verify security and commit only non-secret audit/docs**

Run the Task 7 secret scan. Commit the redacted audit only if it contains no
account PII beyond seller username and no secret-shaped values.

---

### Task 9: Fresh five-product selection and manifest dry-runs

**Files:**
- Create: `05_EXECUTION/ebay-direct/manifests/PILOT-20260815-01.json`
- Create: `05_EXECUTION/ebay-direct/manifests/PILOT-20260815-02.json`
- Create: `05_EXECUTION/ebay-direct/manifests/PILOT-20260815-03.json`
- Create: `05_EXECUTION/ebay-direct/manifests/PILOT-20260815-04.json`
- Create: `05_EXECUTION/ebay-direct/manifests/PILOT-20260815-05.json`
- Create: `05_EXECUTION/ebay-direct/action-packs/PILOT-20260815-01.json`
- Create: `05_EXECUTION/ebay-direct/action-packs/PILOT-20260815-02.json`
- Create: `05_EXECUTION/ebay-direct/action-packs/PILOT-20260815-03.json`
- Create: `05_EXECUTION/ebay-direct/action-packs/PILOT-20260815-04.json`
- Create: `05_EXECUTION/ebay-direct/action-packs/PILOT-20260815-05.json`
- Create: `05_EXECUTION/ebay-direct/audit/five-product-selection.json`

**Interfaces:**
- Consumes the ready Production bootstrap and current public supplier/market evidence.
- Produces five validation-PASS manifests and five action-pack hashes; no external writes.

- [ ] **Step 1: Build a fresh candidate pool**

Ignore AutoDS drafts. Evaluate at least 15 current unbranded candidates with
canonical supplier URLs, stock, delivered-US cost, ≤10-day latest delivery,
image rights, current eBay sold demand and VeRO risk. Record evidence timestamp
and source URL for every numeric claim.

- [ ] **Step 2: Apply the deterministic value gate**

Reject any candidate with stale/unknown stock, missing rights-cleared images,
unsupported claims, brand ambiguity, estimated net profit below $5 or margin
below 20%. Rank the survivors by net profit, demand evidence, delivery confidence
and category concentration; select the top five distinct SKUs.

- [ ] **Step 3: Resolve eBay metadata read-only**

For each survivor, retrieve category suggestions and required aspects from eBay
Taxonomy/Metadata reads, then populate exact category, aspects, condition,
policies and location in its manifest.

- [ ] **Step 4: Validate all five manifests**

Run `deno task cli validate --manifest manifests/PILOT-20260815-01.json` through
`PILOT-20260815-05.json`. Expected: five PASS, zero errors. A failure removes the
candidate and pulls the next ranked survivor; never weaken a gate.

- [ ] **Step 5: Generate five dry-run action packs**

Run `deno task cli dry-run --manifest manifests/PILOT-20260815-01.json` through
`PILOT-20260815-05.json`. Expected: five local packs, zero eBay writes. Re-run
bootstrap duplicate checks immediately before presenting them.

- [ ] **Step 6: Present the exact protected batch**

Show SKU, title, price, quantity, net-margin estimate, action-pack SHA-256,
effect, risk and rollback for all five. Stop for a batch GO that names all five
hashes; a generic or earlier GO cannot authorize these newly materialized writes.

---

### Task 10: Apply and verify the exact five listings — inline only

**Files:**
- Create: `05_EXECUTION/ebay-direct/audit/PILOT-20260815-01.jsonl`
- Create: `05_EXECUTION/ebay-direct/audit/PILOT-20260815-02.jsonl`
- Create: `05_EXECUTION/ebay-direct/audit/PILOT-20260815-03.jsonl`
- Create: `05_EXECUTION/ebay-direct/audit/PILOT-20260815-04.jsonl`
- Create: `05_EXECUTION/ebay-direct/audit/PILOT-20260815-05.jsonl`
- Create: `05_EXECUTION/ebay-direct/audit/five-listing-live-result.json`

**Interfaces:**
- Consumes five action packs and a current Owner GO naming their hashes.
- Produces five eBay listing IDs with read-back PASS, or a partial result with untouched later items frozen.

- [ ] **Step 1: Revalidate freshness and hashes**

Re-run bootstrap and manifest validation. Abort the whole batch if supplier
evidence is older than 24 hours, a duplicate appears, or any pack hash changes.

- [ ] **Step 2: Apply inventory stage for listing one**

Run `apply-inventory` with the exact pack and expected hash. Read back the SKU and
verify canonical payload equality before proceeding.

- [ ] **Step 3: Create/reuse offer for listing one**

Run `create-offer`, persist the returned offer ID in the audit, and confirm the
offer remains unpublished with expected price, quantity, policies and location.

- [ ] **Step 4: Publish and verify listing one**

Run `publish-offer`, then `verify`. Require returned listing ID and public listing
read PASS. On any unexplained mismatch, freeze listings two through five and
report the exact remote state.

- [ ] **Step 5: Repeat the same three stages serially for listings two–five**

Do not parallelize writes. Before each listing, confirm its pack hash still
matches and the prior listing has a complete verification record.

- [ ] **Step 6: Produce the final live result**

Record five rows: SKU, offer ID, listing ID, price, quantity, published timestamp,
verification status and pack hash. Run the secret scan and report `COMPLETE` only
when all five read-backs pass; otherwise report `PARTIAL_COMPLETE` with untouched
packs and no guessed success.

---

## Plan Self-Review

- Spec coverage: OAuth, minimum scopes, secret boundary, bootstrap, manifests,
  validation, payload hashes, per-action writes, retries, verification, rollback,
  audit, first-five pilot and non-goals are each mapped to Tasks 1–10.
- Type consistency: `EbayConfig`, `AccountBootstrap`, `ListingManifest`,
  `ValidationReport`, `ActionPack` and SHA-256 arguments retain the same names
  across producer and consumer tasks.
- Placeholder scan: no `TBD`, `TODO`, “implement later”, unspecified error
  handling or undefined function reference remains.
- Scope split: software construction is Tasks 1–7; credential/live bootstrap is
  Task 8; product/evidence work is Task 9; protected publication is Task 10.

# eBay Direct Production — design

**Status:** approved in chat by the Owner on 2026-08-15; written review pending  
**Consumer:** eBay machine operator and the local direct-listing CLI  
**Environment:** eBay US Production (`EBAY_US`), seller `divinit-92`

## Objective

Replace the retired AutoDS execution path with a local, auditable integration
against eBay Sell APIs. The first milestone is to validate and publish five
exact listings without giving a public service or a subagent access to seller
credentials.

## Decision

Use the REST Inventory API with an OAuth User token. Do not use AutoDS, browser
automation, or the legacy Trading API for the canonical write path.

The webhook deployed on Deno remains responsible only for Marketplace Account
Deletion notifications. Listing operations run locally because they handle
seller credentials and protected writes.

## Alternatives rejected

1. **Trading API / AddFixedPriceItem:** workable fallback, but legacy XML and a
   weaker fit for deterministic bulk inventory management.
2. **Seller Hub automation:** useful only as a recovery surface; it defeats the
   purpose of the Production API integration and is brittle around login and
   CAPTCHA state.
3. **Deno listing service:** rejected because a public runtime does not need the
   seller refresh token and would widen the credential attack surface.

## OAuth and secret boundary

The seller authorizes the Production application through the authorization-code
grant. Request the minimum initial scopes:

- `https://api.ebay.com/oauth/api_scope/sell.inventory`
- `https://api.ebay.com/oauth/api_scope/sell.account.readonly`

The refresh token and transient access token live only in a gitignored local
secret file. Client ID and Client Secret are consumed through the existing
protected credential flow and are never written to reports, logs, manifests, or
command output. Access tokens are refreshed in memory and redacted from errors.

Request `sell.account` later only if the existing business policies are missing
and the Owner separately authorizes creating or changing them. Order handling
and fulfillment scopes are outside this first milestone.

## Components

### 1. OAuth helper

- generates the Production consent URL with an unpredictable state value;
- verifies returned state before exchanging the authorization code;
- stores only the refresh token in the local secret file;
- can introspect the access token and report only username, active status,
  scopes, and expiry metadata.

### 2. Read-only account bootstrap

Reads and validates:

- seller identity and privileges;
- payment, fulfillment, and return policy IDs for `EBAY_US`;
- enabled inventory locations and their merchant location keys;
- existing inventory items/offers for duplicate detection.

It must not create or update policies or locations. Missing prerequisites produce
an exact gated action proposal.

### 3. Listing manifest

One versioned JSON document per candidate, containing no secrets:

- stable SKU and source/product evidence;
- title, description, category and item aspects;
- condition, quantity, price and currency;
- canonical HTTPS image URLs with rights/provenance evidence;
- package dimensions/weight when required;
- merchant location key and the three business-policy IDs;
- supplier cost, fees, estimated net margin and evidence freshness;
- VeRO/compliance result and validation timestamp.

Historical AutoDS draft IDs are not identifiers in this system. Old AutoDS
artifacts may be read as stale research only and can never satisfy a live gate.

### 4. Validator and dry-run

Before any write, validate locally and with read-only eBay metadata:

- title length and prohibited/unsupported claims;
- required and recommended category aspects;
- image count, reachability, format and minimum dimensions;
- category/condition compatibility;
- policy/location existence;
- duplicate SKU, product and active-listing detection;
- current stock, delivery estimate, supplier cost and positive margin headroom;
- payload hashes for the inventory item and offer.

The dry-run emits a redacted action pack for each listing: exact SKU, effect,
risk, rollback, payload hashes and expected fees. It never creates an inventory
item or offer.

### 5. Protected writer

Writes are separated into deterministic stages:

1. `PUT /sell/inventory/v1/inventory_item/{sku}`
2. `POST /sell/inventory/v1/offer`
3. `POST /sell/inventory/v1/offer/{offerId}/publish`

Each stage records only non-secret request hashes, HTTP status, eBay error IDs,
SKU, offer ID and listing ID. Retrying must be idempotent and first read the
current remote state.

Inventory-item creation, offer creation and publication are distinct protected
external actions. A GO is valid only for the exact listing/action pack whose
hash was shown to the Owner. A batch GO is acceptable only after all five exact
packs have passed and are identified in the batch payload.

### 6. Verification and rollback

After publication:

- read the offer and inventory item back through the API;
- confirm returned listing ID, marketplace, SKU, price and quantity;
- perform a public read of the listing without changing it;
- save the redacted verification record.

Rollback is `withdrawOffer` for the exact offer ID, followed by a read-back. It
is a separate protected action. Inventory records are retained for audit unless
their deletion receives a separate GO.

## First-five workflow

1. Complete seller OAuth.
2. Run the read-only account/bootstrap audit.
3. Select five products using fresh supplier, image, demand and margin evidence.
4. Build and validate five manifests.
5. Present five exact action packs and payload hashes.
6. Execute only the specifically authorized stages.
7. Verify every listing and stop the batch on the first unexplained mismatch.

The five historical AutoDS candidates are not preselected. They may re-enter the
shortlist only if freshly validated from their canonical sources.

## Error handling

- `401/403`: stop, refresh once when appropriate, then require OAuth recovery;
- `409`: read remote state and reconcile by SKU; never blind-retry;
- `429/5xx`: bounded exponential backoff with jitter and no duplicate publish;
- eBay business-rule error: record error ID and block that listing;
- partial batch success: freeze untouched items and report exact remote state;
- credential or token text in an exception: redact before logging or persisting.

## Tests and completion evidence

- unit tests for OAuth state, redaction, token refresh, manifest schema and hash;
- mocked contract tests for inventory item, offer, publish and withdraw calls;
- failure tests for `401`, `409`, `429`, partial success and malformed responses;
- dry-run fixture proving zero write calls;
- secret scan proving no credential outside the gitignored secret file;
- Production smoke test limited to read-only identity, policies, locations and
  duplicate checks after OAuth;
- live completion requires five returned listing IDs and five read-back PASS
  records.

## Non-goals for milestone one

- automatic supplier purchasing;
- order fulfillment, shipment tracking or refunds;
- stock/price monitoring loops;
- migration of the historical AutoDS catalog;
- automatic policy or inventory-location creation;
- bulk publication before the five-listing pilot passes.

These are later milestones because removing AutoDS also removes its operational
order and stock layer; listing publication alone must not be mistaken for a
complete dropshipping system.

## Value gate

**Hypothesis:** direct eBay control removes the AutoDS subscription dependency
and gives the machine deterministic listing operations.  
**Economics:** viable for a five-listing pilot only when each manifest shows fresh
positive net margin after eBay fees and fulfillment cost; ongoing value remains
unknown until stock/order operations are covered.  
**Falsifier:** OAuth cannot obtain the required scopes, seller prerequisites are
missing, or fewer than five products clear evidence/compliance/margin gates.


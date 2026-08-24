import type { ActionPack } from "./types.ts";
import { EbayApiClient, EbayApiError } from "./api_client.ts";
import { sha256Canonical } from "./payloads.ts";

export const REMOTE_STATE_CONFLICT = "REMOTE_STATE_CONFLICT";
export const VERIFY_FAILED = "VERIFY_FAILED";

type Obj = Record<string, unknown>;

export interface InventoryOutcome {
  sku: string;
  outcome: "created" | "unchanged";
}

export interface OfferOutcome {
  offerId: string;
  outcome: "created" | "reused";
}

export interface PublishOutcome {
  offerId: string;
  listingId: string;
  outcome: "published" | "already_published";
}

export interface VerifyExpectation {
  listingId: string;
  price: string;
  quantity: number;
}

export interface WithdrawOutcome {
  offerId: string;
  outcome: "withdrawn" | "already_ended";
}

/** Refuses any write whose pack hash does not match the Owner-named hash. */
function gatePack(
  pack: ActionPack,
  expectedPackSha256: string,
): void {
  if (pack.packSha256 !== expectedPackSha256) {
    throw new Error("action pack SHA-256 mismatch: refusing write");
  }
}

/** Refuses to send a payload that does not match the pack's recorded hash. */
async function gatePayload(
  payload: unknown,
  payloadSha256: string,
): Promise<void> {
  if (await sha256Canonical(payload) !== payloadSha256) {
    throw new Error("payload SHA-256 mismatch: refusing write");
  }
}

/** Projects `obj` onto `keys` so `sku`/`offerId` metadata does not skew equality. */
function subset(obj: Obj, keys: string[]): Obj {
  const out: Obj = {};
  for (const key of keys) {
    if (key in obj) out[key] = obj[key];
  }
  return out;
}

async function readOrNull(
  client: EbayApiClient,
  path: string,
): Promise<Obj | null> {
  try {
    return await client.request<Obj>({ method: "GET", path, write: false });
  } catch (err) {
    if (err instanceof EbayApiError && err.status === 404) return null;
    throw err;
  }
}

/**
 * Applies the inventory item idempotently: skips the PUT when the current remote
 * item already matches, refuses to overwrite a different one, and creates when
 * absent. The hash gate runs before any HTTP call.
 */
export async function applyInventory(
  client: EbayApiClient,
  pack: ActionPack,
  expectedPackSha256: string,
  payload: unknown,
): Promise<InventoryOutcome> {
  gatePack(pack, expectedPackSha256);
  await gatePayload(payload, pack.inventoryAction.payloadSha256);

  const path = pack.inventoryAction.path;
  const payloadKeys = Object.keys(payload as Obj);
  const remote = await readOrNull(client, path);

  if (remote === null) {
    await client.request<Obj>({
      method: "PUT",
      path,
      body: payload,
      write: true,
    });
    return { sku: pack.sku, outcome: "created" };
  }

  const remoteHash = await sha256Canonical(subset(remote, payloadKeys));
  if (remoteHash === pack.inventoryAction.payloadSha256) {
    return { sku: pack.sku, outcome: "unchanged" };
  }

  throw new Error(
    `remote inventory item differs from intended payload (${REMOTE_STATE_CONFLICT})`,
  );
}

/**
 * Creates the offer once, or reuses an existing unpublished offer whose listing
 * fields already match. Never mutates an unknown offer.
 */
export async function createOrReuseOffer(
  client: EbayApiClient,
  pack: ActionPack,
  expectedPackSha256: string,
  payload: unknown,
): Promise<OfferOutcome> {
  gatePack(pack, expectedPackSha256);
  await gatePayload(payload, pack.offerAction.payloadSha256);

  const payloadKeys = Object.keys(payload as Obj);
  const listPath =
    `/sell/inventory/v1/offer?sku=${encodeURIComponent(pack.sku)}` +
    `&marketplace_id=EBAY_US`;
  const list = await readOrNull(client, listPath);
  const offers = (list?.["offers"] ?? []) as Obj[];

  if (offers.length === 0) {
    const created = await client.request<Obj>({
      method: "POST",
      path: pack.offerAction.path,
      body: payload,
      write: true,
    });
    const offerId = created["offerId"];
    if (typeof offerId !== "string") {
      throw new Error("offer create response missing offerId");
    }
    return { offerId, outcome: "created" };
  }

  for (const offer of offers) {
    if (
      await sha256Canonical(subset(offer, payloadKeys)) ===
        pack.offerAction.payloadSha256
    ) {
      const offerId = offer["offerId"];
      if (typeof offerId !== "string") {
        throw new Error("offer list entry missing offerId");
      }
      return { offerId, outcome: "reused" };
    }
  }

  throw new Error(
    `an offer already exists for SKU with different fields (${REMOTE_STATE_CONFLICT})`,
  );
}

/**
 * Publishes an offer once. On an ambiguous failure it reads the offer back: if a
 * listing was actually created, it returns that listing id instead of retrying.
 */
export async function publishOffer(
  client: EbayApiClient,
  pack: ActionPack,
  expectedPackSha256: string,
  offerId: string,
): Promise<PublishOutcome> {
  gatePack(pack, expectedPackSha256);

  const path = pack.publishAction.pathTemplate.replace("{offerId}", offerId);
  try {
    const res = await client.request<Obj>({
      method: "POST",
      path,
      write: true,
    });
    const listingId = res["listingId"];
    if (typeof listingId !== "string") {
      throw new Error("publish response missing listingId");
    }
    return { offerId, listingId, outcome: "published" };
  } catch (err) {
    const offer = await readOrNull(
      client,
      `/sell/inventory/v1/offer/${offerId}`,
    );
    const listing = (offer?.["listing"] ?? {}) as Obj;
    const listingId = listing["listingId"] ?? offer?.["listingId"];
    if (typeof listingId === "string") {
      return { offerId, listingId, outcome: "already_published" };
    }
    throw err;
  }
}

/**
 * Reads back the offer and inventory item, confirming the listing id, marketplace,
 * SKU, price and quantity. Any missing or mismatched field yields VERIFY_FAILED.
 */
export async function verifyPublished(
  client: EbayApiClient,
  pack: ActionPack,
  expectedPackSha256: string,
  offerId: string,
  expected: VerifyExpectation,
): Promise<Obj> {
  gatePack(pack, expectedPackSha256);

  const offer = await readOrNull(client, `/sell/inventory/v1/offer/${offerId}`);
  const inventory = await readOrNull(client, pack.inventoryAction.path);

  // eBay nests the listing reference under `listing`; older payloads used a
  // top-level `listingId`, so accept both.
  const listing = (offer?.["listing"] ?? {}) as Obj;
  const remoteListingId = listing["listingId"] ?? offer?.["listingId"];

  const failures: string[] = [];
  if (remoteListingId !== expected.listingId) {
    failures.push("listing id mismatch");
  }
  if (offer?.["marketplaceId"] !== "EBAY_US") {
    failures.push("marketplace mismatch");
  }
  if (offer?.["sku"] !== pack.sku) failures.push("SKU mismatch");

  const pricing = (offer?.["pricingSummary"] ?? {}) as Obj;
  const price = (pricing["price"] ?? {}) as Obj;
  if (price["value"] !== expected.price) failures.push("price mismatch");

  const availability = (inventory?.["availability"] ?? {}) as Obj;
  const shipTo = (availability["shipToLocationAvailability"] ?? {}) as Obj;
  if (shipTo["quantity"] !== expected.quantity) {
    failures.push("quantity mismatch");
  }

  if (failures.length > 0) {
    throw new Error(`${VERIFY_FAILED}: ${failures.join(", ")}`);
  }

  return {
    verified: true,
    listingId: expected.listingId,
    offerId,
    sku: pack.sku,
    price: expected.price,
    quantity: expected.quantity,
  };
}

/**
 * Withdraws an offer under its own pack hash and reads it back to confirm a
 * non-published state. The inventory item is never touched.
 */
export async function withdrawOffer(
  client: EbayApiClient,
  pack: ActionPack,
  expectedPackSha256: string,
  offerId: string,
): Promise<WithdrawOutcome> {
  gatePack(pack, expectedPackSha256);

  const path = `/sell/inventory/v1/offer/${offerId}/withdraw`;
  try {
    await client.request<Obj>({ method: "POST", path, write: true });
  } catch (err) {
    const offer = await readOrNull(
      client,
      `/sell/inventory/v1/offer/${offerId}`,
    );
    const status = offer?.["status"];
    if (status === "ENDED" || status === undefined && offer !== null) {
      return { offerId, outcome: "already_ended" };
    }
    throw err;
  }

  const offer = await readOrNull(client, `/sell/inventory/v1/offer/${offerId}`);
  if (offer?.["status"] === "PUBLISHED") {
    throw new Error(
      `withdrawal failed: offer still published (${VERIFY_FAILED})`,
    );
  }
  return { offerId, outcome: "withdrawn" };
}

import type { EbayApiClient } from "./api_client.ts";
import type { AccountBootstrap } from "./types.ts";

const MARKETPLACE_ID = "EBAY_US";

function extractIds(
  page: Record<string, unknown> | null,
  listKey: string,
  idKey: string,
): string[] {
  if (!page) return [];
  const list = (page[listKey] ?? []) as Array<Record<string, unknown>>;
  return list
    .map((item) => item[idKey])
    .filter((value): value is string => typeof value === "string");
}

function safeNext(next: unknown, baseUrl: string): string | null {
  if (typeof next !== "string") return null;
  let url: URL;
  try {
    url = new URL(next);
  } catch {
    return null;
  }
  if (url.origin !== new URL(baseUrl).origin) return null;
  return url.pathname + url.search;
}

async function safeRead(
  client: EbayApiClient,
  path: string,
): Promise<Record<string, unknown> | null> {
  try {
    return await client.request<Record<string, unknown>>({
      method: "GET",
      path,
      write: false,
    });
  } catch {
    return null;
  }
}

/**
 * Follows eBay `next` pagination links, rejecting cross-origin targets, and
 * collects one identifier per item. Returns an empty list on any read failure.
 */
export async function readPaged(
  client: EbayApiClient,
  path: string,
  listKey: string,
  idKey: string,
): Promise<string[]> {
  const ids: string[] = [];
  let currentPath: string = path;
  let guard = 0;
  while (currentPath && guard < 100) {
    guard++;
    const page = await safeRead(client, currentPath);
    if (!page) break;
    ids.push(...extractIds(page, listKey, idKey));
    const next = safeNext(page["next"], client.baseUrl);
    if (!next) break;
    currentPath = next;
  }
  return ids;
}

export async function readBootstrap(
  client: EbayApiClient,
): Promise<AccountBootstrap> {
  const checkedAt = new Date().toISOString();
  const blockers: string[] = [];

  const privilegePage = await safeRead(client, "/sell/account/v1/privilege");
  const privileges = (privilegePage?.["privileges"] ?? []) as Array<
    Record<string, unknown>
  >;
  if (!Array.isArray(privileges) || privileges.length === 0) {
    blockers.push("PRIVILEGE_MISSING");
  }

  const paymentPolicyIds = await readPaged(
    client,
    "/sell/account/v1/payment_policy?marketplace_id=" + MARKETPLACE_ID,
    "paymentPolicies",
    "paymentPolicyId",
  );
  if (paymentPolicyIds.length === 0) blockers.push("PAYMENT_POLICY_MISSING");

  const fulfillmentPolicyIds = await readPaged(
    client,
    "/sell/account/v1/fulfillment_policy?marketplace_id=" + MARKETPLACE_ID,
    "fulfillmentPolicies",
    "fulfillmentPolicyId",
  );
  if (fulfillmentPolicyIds.length === 0) {
    blockers.push("FULFILLMENT_POLICY_MISSING");
  }

  const returnPolicyIds = await readPaged(
    client,
    "/sell/account/v1/return_policy?marketplace_id=" + MARKETPLACE_ID,
    "returnPolicies",
    "returnPolicyId",
  );
  if (returnPolicyIds.length === 0) blockers.push("RETURN_POLICY_MISSING");

  const merchantLocationKeys = await readPaged(
    client,
    "/sell/inventory/v1/location?limit=100",
    "locations",
    "merchantLocationKey",
  );
  if (merchantLocationKeys.length === 0) blockers.push("NO_MERCHANT_LOCATION");

  const existingSkus = await readPaged(
    client,
    "/sell/inventory/v1/inventory_item?limit=100",
    "inventoryItems",
    "sku",
  );

  const existingOfferSkus = await readPaged(
    client,
    "/sell/inventory/v1/offer?limit=100&marketplace_id=" + MARKETPLACE_ID,
    "offers",
    "sku",
  );

  return {
    ready: blockers.length === 0,
    blockers,
    sellerUsername: undefined,
    privileges,
    paymentPolicyIds,
    fulfillmentPolicyIds,
    returnPolicyIds,
    merchantLocationKeys,
    existingSkus,
    existingOfferSkus,
    checkedAt,
  };
}

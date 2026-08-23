import { assertEquals, assertRejects } from "@std/assert";
import type { ActionPack } from "./types.ts";
import type { EbayApiClient } from "./api_client.ts";
import { EbayApiError } from "./api_client.ts";
import { sha256Canonical } from "./payloads.ts";
import {
  applyInventory,
  createOrReuseOffer,
  publishOffer,
  verifyPublished,
  withdrawOffer,
} from "./publisher.ts";

const SKU = "SKU-TEST-001";
const INVENTORY_PATH = `/sell/inventory/v1/inventory_item/${SKU}`;
const OFFER_LIST_PATH =
  `/sell/inventory/v1/offer?sku=${SKU}&marketplace_id=EBAY_US`;
const OFFER_PATH = "/sell/inventory/v1/offer";

interface Call {
  method: string;
  path: string;
  write: boolean;
  body?: unknown;
}

function makeFake(routes: Record<string, unknown | Error>): {
  client: EbayApiClient;
  calls: Call[];
} {
  const calls: Call[] = [];
  const client = {
    baseUrl: "https://api.ebay.com",
    request: (req: {
      method: string;
      path: string;
      write: boolean;
      body?: unknown;
    }) => {
      calls.push({
        method: req.method,
        path: req.path,
        write: req.write,
        body: req.body,
      });
      const entry = routes[`${req.method} ${req.path}`];
      if (entry instanceof Error) return Promise.reject(entry);
      if (entry === undefined) {
        return Promise.reject(new EbayApiError("not found", 404));
      }
      return Promise.resolve(entry);
    },
  };
  return { client: client as unknown as EbayApiClient, calls };
}

async function fixture(): Promise<{
  inventoryPayload: Record<string, unknown>;
  offerPayload: Record<string, unknown>;
  pack: ActionPack;
}> {
  const inventoryPayload = {
    availability: { shipToLocationAvailability: { quantity: 5 } },
    condition: "NEW",
    product: {
      title: "Pool Chlorinator Replacement Cell",
      description: "Replacement salt cell.",
      aspects: { Brand: ["Generic"] },
      imageUrls: ["https://example.com/a.jpg"],
    },
  };
  const offerPayload = {
    sku: SKU,
    marketplaceId: "EBAY_US",
    format: "FIXED_PRICE",
    categoryId: "123456",
    merchantLocationKey: "LOC1",
    availableQuantity: 5,
    pricingSummary: { price: { value: "59.99", currency: "USD" } },
    listingDescription: "Replacement salt cell.",
    listingPolicies: {
      fulfillmentPolicyId: "FP1",
      paymentPolicyId: "PP1",
      returnPolicyId: "RP1",
    },
  };
  const pack = {
    version: 1,
    sku: SKU,
    manifestSha256: "m".repeat(64),
    inventoryAction: {
      method: "PUT",
      path: INVENTORY_PATH,
      payloadSha256: await sha256Canonical(inventoryPayload),
    },
    offerAction: {
      method: "POST",
      path: OFFER_PATH,
      payloadSha256: await sha256Canonical(offerPayload),
    },
    publishAction: {
      method: "POST",
      pathTemplate: "/sell/inventory/v1/offer/{offerId}/publish",
    },
    effect: "effect",
    risk: "risk",
    rollback: "rollback",
    validation: { pass: true, checkedAt: "2026-08-15T10:00:00Z" },
    packSha256: "PACK-HASH",
  } as ActionPack;
  return { inventoryPayload, offerPayload, pack };
}

Deno.test("applyInventory rejects pack hash mismatch with zero calls", async () => {
  const { inventoryPayload, pack } = await fixture();
  const { client, calls } = makeFake({});
  await assertRejects(
    () => applyInventory(client, pack, "WRONG", inventoryPayload),
    Error,
    "mismatch",
  );
  assertEquals(calls.length, 0);
});

Deno.test("applyInventory rejects payload hash mismatch with zero calls", async () => {
  const { pack } = await fixture();
  const { client, calls } = makeFake({});
  await assertRejects(
    () => applyInventory(client, pack, "PACK-HASH", { different: true }),
    Error,
    "payload",
  );
  assertEquals(calls.length, 0);
});

Deno.test("applyInventory skips PUT when remote item already matches", async () => {
  const { inventoryPayload, pack } = await fixture();
  const { client, calls } = makeFake({
    [`GET ${INVENTORY_PATH}`]: { sku: SKU, ...inventoryPayload },
  });
  const result = await applyInventory(
    client,
    pack,
    "PACK-HASH",
    inventoryPayload,
  );
  assertEquals(result.outcome, "unchanged");
  assertEquals(calls.filter((c) => c.write).length, 0);
});

Deno.test("applyInventory PUTs when the item is absent", async () => {
  const { inventoryPayload, pack } = await fixture();
  const { client, calls } = makeFake({
    [`PUT ${INVENTORY_PATH}`]: {},
  });
  const result = await applyInventory(
    client,
    pack,
    "PACK-HASH",
    inventoryPayload,
  );
  assertEquals(result.outcome, "created");
  assertEquals(calls.some((c) => c.method === "PUT" && c.write), true);
});

Deno.test("createOrReuseOffer reuses an existing matching offer", async () => {
  const { offerPayload, pack } = await fixture();
  const { client, calls } = makeFake({
    [`GET ${OFFER_LIST_PATH}`]: {
      offers: [{ offerId: "OFF-1", ...offerPayload }],
    },
  });
  const result = await createOrReuseOffer(
    client,
    pack,
    "PACK-HASH",
    offerPayload,
  );
  assertEquals(result.outcome, "reused");
  assertEquals(result.offerId, "OFF-1");
  assertEquals(calls.filter((c) => c.write).length, 0);
});

Deno.test("createOrReuseOffer creates when no offer exists", async () => {
  const { offerPayload, pack } = await fixture();
  const { client, calls } = makeFake({
    [`GET ${OFFER_LIST_PATH}`]: { offers: [] },
    [`POST ${OFFER_PATH}`]: { offerId: "OFF-NEW" },
  });
  const result = await createOrReuseOffer(
    client,
    pack,
    "PACK-HASH",
    offerPayload,
  );
  assertEquals(result.outcome, "created");
  assertEquals(result.offerId, "OFF-NEW");
  assertEquals(calls.filter((c) => c.write).length, 1);
});

Deno.test("publishOffer returns an existing listing id without a second publish", async () => {
  const { pack } = await fixture();
  const { client, calls } = makeFake({
    [`POST ${OFFER_PATH}/OFF-1/publish`]: new EbayApiError("timeout", 500),
    [`GET ${OFFER_PATH}/OFF-1`]: { listingId: "L123", status: "PUBLISHED" },
  });
  const result = await publishOffer(client, pack, "PACK-HASH", "OFF-1");
  assertEquals(result.outcome, "already_published");
  assertEquals(result.listingId, "L123");
  assertEquals(calls.filter((c) => c.write).length, 1);
});

Deno.test("publishOffer returns the new listing id on success", async () => {
  const { pack } = await fixture();
  const { client } = makeFake({
    [`POST ${OFFER_PATH}/OFF-1/publish`]: { listingId: "L-NEW" },
  });
  const result = await publishOffer(client, pack, "PACK-HASH", "OFF-1");
  assertEquals(result.outcome, "published");
  assertEquals(result.listingId, "L-NEW");
});

Deno.test("verifyPublished fails on a mismatched field", async () => {
  const { inventoryPayload, pack } = await fixture();
  const { client } = makeFake({
    [`GET ${OFFER_PATH}/OFF-1`]: {
      listingId: "L123",
      marketplaceId: "EBAY_US",
      sku: SKU,
      pricingSummary: { price: { value: "99.99", currency: "USD" } },
    },
    [`GET ${INVENTORY_PATH}`]: inventoryPayload,
  });
  await assertRejects(
    () =>
      verifyPublished(client, pack, "PACK-HASH", "OFF-1", {
        listingId: "L123",
        price: "59.99",
        quantity: 5,
      }),
    Error,
    "VERIFY_FAILED",
  );
});

Deno.test("verifyPublished passes when all fields match", async () => {
  const { inventoryPayload, pack } = await fixture();
  const { client } = makeFake({
    [`GET ${OFFER_PATH}/OFF-1`]: {
      listingId: "L123",
      marketplaceId: "EBAY_US",
      sku: SKU,
      pricingSummary: { price: { value: "59.99", currency: "USD" } },
    },
    [`GET ${INVENTORY_PATH}`]: inventoryPayload,
  });
  const result = await verifyPublished(client, pack, "PACK-HASH", "OFF-1", {
    listingId: "L123",
    price: "59.99",
    quantity: 5,
  });
  assertEquals(result["verified"], true);
});

Deno.test("withdrawOffer never touches the inventory item", async () => {
  const { pack } = await fixture();
  const { client, calls } = makeFake({
    [`POST ${OFFER_PATH}/OFF-1/withdraw`]: {},
    [`GET ${OFFER_PATH}/OFF-1`]: { offerId: "OFF-1", status: "ENDED" },
  });
  const result = await withdrawOffer(client, pack, "PACK-HASH", "OFF-1");
  assertEquals(result.outcome, "withdrawn");
  assertEquals(calls.some((c) => c.path === INVENTORY_PATH), false);
});

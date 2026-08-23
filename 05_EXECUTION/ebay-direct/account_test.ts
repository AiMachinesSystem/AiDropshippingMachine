import { assertEquals } from "@std/assert";
import type { EbayApiClient } from "./api_client.ts";
import { readBootstrap, readPaged } from "./account.ts";

function fakeClient(routes: Record<string, unknown>): EbayApiClient {
  const requested: string[] = [];
  const client = {
    baseUrl: "https://api.ebay.com",
    requested,
    request: (req: { path: string }) => {
      requested.push(req.path);
      const body = routes[req.path];
      if (body === undefined) {
        return Promise.reject(new Error("unmocked " + req.path));
      }
      return Promise.resolve(body);
    },
  };
  return client as unknown as EbayApiClient;
}

const FULL_BOOTSTRAP: Record<string, unknown> = {
  "/sell/account/v1/privilege": {
    privileges: [{ privilege: "sell" }],
  },
  "/sell/account/v1/payment_policy?marketplace_id=EBAY_US": {
    paymentPolicies: [{ paymentPolicyId: "PP1" }],
  },
  "/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US": {
    fulfillmentPolicies: [{ fulfillmentPolicyId: "FP1" }],
  },
  "/sell/account/v1/return_policy?marketplace_id=EBAY_US": {
    returnPolicies: [{ returnPolicyId: "RP1" }],
  },
  "/sell/inventory/v1/location?limit=100": {
    locations: [{ merchantLocationKey: "LOC1" }],
  },
  "/sell/inventory/v1/inventory_item?limit=100": {
    inventoryItems: [{ sku: "SKU-EXISTING" }],
  },
  "/sell/inventory/v1/offer?limit=100&marketplace_id=EBAY_US": {
    offers: [{ sku: "SKU-EXISTING" }],
  },
};

Deno.test("readBootstrap returns ready when all prerequisites exist", async () => {
  const bootstrap = await readBootstrap(fakeClient({ ...FULL_BOOTSTRAP }));
  assertEquals(bootstrap.ready, true);
  assertEquals(bootstrap.blockers, []);
  assertEquals(bootstrap.paymentPolicyIds, ["PP1"]);
  assertEquals(bootstrap.fulfillmentPolicyIds, ["FP1"]);
  assertEquals(bootstrap.returnPolicyIds, ["RP1"]);
  assertEquals(bootstrap.merchantLocationKeys, ["LOC1"]);
  assertEquals(bootstrap.existingSkus, ["SKU-EXISTING"]);
  assertEquals(bootstrap.existingOfferSkus, ["SKU-EXISTING"]);
});

Deno.test("readBootstrap flags missing fulfillment policy and location", async () => {
  const bootstrap = await readBootstrap(
    fakeClient({
      ...FULL_BOOTSTRAP,
      "/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US": {
        fulfillmentPolicies: [],
      },
      "/sell/inventory/v1/location?limit=100": { locations: [] },
    }),
  );
  assertEquals(bootstrap.ready, false);
  assertEquals(
    bootstrap.blockers.includes("FULFILLMENT_POLICY_MISSING"),
    true,
  );
  assertEquals(bootstrap.blockers.includes("NO_MERCHANT_LOCATION"), true);
});

Deno.test("readPaged rejects cross-origin next links", async () => {
  const client = fakeClient({
    "/sell/inventory/v1/inventory_item?limit=100": {
      inventoryItems: [{ sku: "A" }],
      next: "https://evil.example.com/next",
    },
  });
  const ids = await readPaged(
    client,
    "/sell/inventory/v1/inventory_item?limit=100",
    "inventoryItems",
    "sku",
  );
  assertEquals(ids, ["A"]);
  assertEquals(
    (client as unknown as { requested: string[] }).requested.length,
    1,
  );
});

Deno.test("readPaged follows same-origin next links", async () => {
  const client = fakeClient({
    "/sell/inventory/v1/inventory_item?limit=100": {
      inventoryItems: [{ sku: "A" }],
      next: "https://api.ebay.com/sell/inventory/v1/inventory_item?offset=100",
    },
    "/sell/inventory/v1/inventory_item?offset=100": {
      inventoryItems: [{ sku: "B" }],
    },
  });
  const ids = await readPaged(
    client,
    "/sell/inventory/v1/inventory_item?limit=100",
    "inventoryItems",
    "sku",
  );
  assertEquals(ids, ["A", "B"]);
});

import { assertEquals, assertNotEquals } from "@std/assert";
import type { ListingManifest } from "./types.ts";
import {
  buildInventoryPayload,
  buildOfferPayload,
  canonicalJson,
  sha256Canonical,
} from "./payloads.ts";

function validManifest(): ListingManifest {
  return {
    version: 1,
    sku: "SKU-TEST-001",
    marketplaceId: "EBAY_US",
    product: {
      title: "Pool Chlorinator Replacement Cell",
      description:
        "Replacement salt cell for salt water pool chlorinator systems.",
      aspects: { Brand: ["Generic"], Type: ["Salt Cell"] },
      imageUrls: ["https://example.com/a.jpg", "https://example.com/b.jpg"],
    },
    condition: "NEW",
    categoryId: "123456",
    quantity: 5,
    price: { value: "59.99", currency: "USD" },
    merchantLocationKey: "LOC1",
    policies: { payment: "PP1", fulfillment: "FP1", return: "RP1" },
    evidence: {
      supplierUrl: "https://supplier.example.com/item",
      sourceCheckedAt: "2026-08-15T10:00:00Z",
      stockObserved: 12,
      supplierCostUsd: "20.00",
      deliveryLatestDays: 5,
      imageRights: "SUPPLIER_AUTHORIZED",
      vero: "PASS",
      estimatedEbayFeesUsd: "9.00",
      estimatedFulfillmentUsd: "6.00",
      estimatedNetProfitUsd: "24.99",
    },
  };
}

Deno.test("canonicalJson sorts object keys deterministically", () => {
  const a = canonicalJson({ a: 1, b: 2, nested: { x: 1, y: 2 } });
  const b = canonicalJson({ b: 2, a: 1, nested: { y: 2, x: 1 } });
  assertEquals(a, b);
});

Deno.test("sha256Canonical is independent of key order", async () => {
  const a = await sha256Canonical({ a: 1, b: 2 });
  const b = await sha256Canonical({ b: 2, a: 1 });
  assertEquals(a, b);
});

Deno.test("sha256Canonical preserves array order", async () => {
  const a = await sha256Canonical([1, 2, 3]);
  const b = await sha256Canonical([3, 2, 1]);
  assertNotEquals(a, b);
});

Deno.test("canonicalJson keeps numeric currency strings as strings", () => {
  const json = canonicalJson({ price: { value: "59.99", currency: "USD" } });
  assertEquals(json.includes('"59.99"'), true);
});

Deno.test("buildInventoryPayload omits supplier URL and cost", () => {
  const payload = JSON.stringify(buildInventoryPayload(validManifest()));
  assertEquals(payload.includes("supplier"), false);
  assertEquals(payload.includes("supplier.example.com"), false);
  assertEquals(payload.includes("20.00"), false);
});

Deno.test("buildInventoryPayload carries quantity, condition and product", () => {
  const payload = buildInventoryPayload(validManifest()) as {
    availability: { shipToLocationAvailability: { quantity: number } };
    condition: string;
    product: { title: string };
  };
  assertEquals(payload.availability.shipToLocationAvailability.quantity, 5);
  assertEquals(payload.condition, "NEW");
  assertEquals(payload.product.title.includes("Pool Chlorinator"), true);
});

Deno.test("buildOfferPayload carries SKU, marketplace, price and policies", () => {
  const payload = buildOfferPayload(validManifest()) as {
    sku: string;
    marketplaceId: string;
    categoryId: string;
    merchantLocationKey: string;
    availableQuantity: number;
    pricingSummary: { price: { value: string; currency: string } };
    listingPolicies: {
      fulfillmentPolicyId: string;
      paymentPolicyId: string;
      returnPolicyId: string;
    };
  };
  assertEquals(payload.sku, "SKU-TEST-001");
  assertEquals(payload.marketplaceId, "EBAY_US");
  assertEquals(payload.categoryId, "123456");
  assertEquals(payload.merchantLocationKey, "LOC1");
  assertEquals(payload.availableQuantity, 5);
  assertEquals(payload.pricingSummary.price.value, "59.99");
  assertEquals(payload.pricingSummary.price.currency, "USD");
  assertEquals(payload.listingPolicies.paymentPolicyId, "PP1");
  assertEquals(payload.listingPolicies.fulfillmentPolicyId, "FP1");
  assertEquals(payload.listingPolicies.returnPolicyId, "RP1");
});

Deno.test("buildOfferPayload omits audit-only evidence", () => {
  const json = JSON.stringify(buildOfferPayload(validManifest()));
  assertEquals(json.includes("supplier"), false);
  assertEquals(json.includes("estimatedNetProfit"), false);
  assertEquals(json.includes("stockObserved"), false);
});

import { assertEquals, assertRejects } from "@std/assert";
import type {
  AccountBootstrap,
  ListingManifest,
  ValidationReport,
} from "./types.ts";
import { buildActionPack } from "./action_pack.ts";
import { sha256Canonical } from "./payloads.ts";

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

function readyBootstrap(): AccountBootstrap {
  return {
    ready: true,
    blockers: [],
    sellerUsername: undefined,
    privileges: [{ privilege: "sell" }],
    paymentPolicyIds: ["PP1"],
    fulfillmentPolicyIds: ["FP1"],
    returnPolicyIds: ["RP1"],
    merchantLocationKeys: ["LOC1"],
    existingSkus: [],
    existingOfferSkus: [],
    checkedAt: "2026-08-15T09:00:00Z",
  };
}

function passingValidation(): ValidationReport {
  return {
    pass: true,
    errors: [],
    warnings: [],
    evidenceFreshAt: "2026-08-15T10:00:00Z",
  };
}

Deno.test("buildActionPack refuses when validation did not pass", async () => {
  await assertRejects(
    () =>
      buildActionPack(validManifest(), {
        ...passingValidation(),
        pass: false,
        errors: ["net profit below $5"],
      }, readyBootstrap()),
    Error,
    "validation",
  );
});

Deno.test("buildActionPack refuses when bootstrap is not ready", async () => {
  await assertRejects(
    () =>
      buildActionPack(
        validManifest(),
        passingValidation(),
        {
          ...readyBootstrap(),
          ready: false,
          blockers: ["NO_MERCHANT_LOCATION"],
        },
      ),
    Error,
    "bootstrap",
  );
});

Deno.test("packSha256 equals the hash of the pack without its own hash", async () => {
  const pack = await buildActionPack(
    validManifest(),
    passingValidation(),
    readyBootstrap(),
  );
  const { packSha256, ...rest } = pack;
  assertEquals(await sha256Canonical(rest), packSha256);
});

Deno.test("buildActionPack is deterministic for identical input", async () => {
  const a = await buildActionPack(
    validManifest(),
    passingValidation(),
    readyBootstrap(),
  );
  const b = await buildActionPack(
    validManifest(),
    passingValidation(),
    readyBootstrap(),
  );
  assertEquals(a.packSha256, b.packSha256);
  assertEquals(a.manifestSha256, b.manifestSha256);
});

Deno.test("pack embeds inventory and offer paths and hashes", async () => {
  const pack = await buildActionPack(
    validManifest(),
    passingValidation(),
    readyBootstrap(),
  );
  assertEquals(pack.inventoryAction.method, "PUT");
  assertEquals(
    pack.inventoryAction.path,
    "/sell/inventory/v1/inventory_item/SKU-TEST-001",
  );
  assertEquals(pack.offerAction.method, "POST");
  assertEquals(pack.offerAction.path, "/sell/inventory/v1/offer");
  assertEquals(
    pack.publishAction.pathTemplate,
    "/sell/inventory/v1/offer/{offerId}/publish",
  );
  assertEquals(pack.inventoryAction.payloadSha256.length, 64);
  assertEquals(pack.offerAction.payloadSha256.length, 64);
  assertEquals(pack.validation.pass, true);
});

Deno.test("pack does not embed supplier URL or cost", async () => {
  const pack = await buildActionPack(
    validManifest(),
    passingValidation(),
    readyBootstrap(),
  );
  const serialized = JSON.stringify(pack);
  assertEquals(serialized.includes("supplier.example.com"), false);
  assertEquals(serialized.includes("20.00"), false);
});

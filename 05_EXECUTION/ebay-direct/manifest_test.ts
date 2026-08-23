import { assertEquals, assertThrows } from "@std/assert";
import type { AccountBootstrap, ListingManifest } from "./types.ts";
import { parseManifest, validateManifest } from "./manifest.ts";

const NOW = new Date("2026-08-15T12:00:00Z");
const CHECKED_AT = "2026-08-15T10:00:00Z";

function validBootstrap(
  overrides: Partial<AccountBootstrap> = {},
): AccountBootstrap {
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
    ...overrides,
  };
}

function validManifest(
  overrides: Record<string, unknown> = {},
): ListingManifest {
  const base = {
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
      sourceCheckedAt: CHECKED_AT,
      stockObserved: 12,
      supplierCostUsd: "20.00",
      deliveryLatestDays: 5,
      imageRights: "SUPPLIER_AUTHORIZED",
      vero: "PASS",
      estimatedEbayFeesUsd: "9.00",
      estimatedFulfillmentUsd: "6.00",
      estimatedNetProfitUsd: "24.99",
    },
    ...overrides,
  };
  return base as unknown as ListingManifest;
}

Deno.test("parseManifest accepts a structurally valid manifest", () => {
  const manifest = validManifest();
  const parsed = parseManifest(manifest);
  assertEquals(parsed.sku, "SKU-TEST-001");
});

Deno.test("parseManifest rejects unknown top-level fields", () => {
  assertThrows(
    () => parseManifest({ ...validManifest(), bogus: 1 }),
    Error,
    "Unknown",
  );
});

Deno.test("parseManifest rejects unknown product fields", () => {
  const manifest = validManifest();
  (manifest.product as unknown as Record<string, unknown>).extra = "x";
  assertThrows(() => parseManifest(manifest), Error, "Unknown product");
});

Deno.test("parseManifest rejects non-object", () => {
  assertThrows(() => parseManifest("nope"), Error, "object");
});

Deno.test("validateManifest passes a fully valid manifest", () => {
  const report = validateManifest(validManifest(), validBootstrap(), NOW);
  assertEquals(report.pass, true);
  assertEquals(report.errors, []);
});

Deno.test("validateManifest rejects title over 80 characters", () => {
  const manifest = validManifest({
    product: {
      ...validManifest().product,
      title: "x".repeat(81),
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("title must be 1-80 characters"), true);
});

Deno.test("validateManifest rejects price without exactly two decimals", () => {
  const manifest = validManifest({ price: { value: "59.9", currency: "USD" } });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(
    report.errors.includes("price must have exactly two decimals"),
    true,
  );
});

Deno.test("validateManifest rejects net profit below $5", () => {
  const manifest = validManifest({
    evidence: { ...validManifest().evidence, estimatedNetProfitUsd: "3.00" },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("net profit below $5"), true);
});

Deno.test("validateManifest rejects net profit below 20% of price", () => {
  const manifest = validManifest({
    price: { value: "200.00", currency: "USD" },
    evidence: { ...validManifest().evidence, estimatedNetProfitUsd: "30.00" },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(
    report.errors.includes("net profit below 20% of sale price"),
    true,
  );
});

Deno.test("validateManifest rejects duplicate image URLs", () => {
  const manifest = validManifest({
    product: {
      ...validManifest().product,
      imageUrls: ["https://example.com/a.jpg", "https://example.com/a.jpg"],
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("duplicate image URLs"), true);
});

Deno.test("validateManifest rejects a policy missing from bootstrap", () => {
  const report = validateManifest(
    validManifest(),
    validBootstrap({ paymentPolicyIds: ["OTHER"] }),
    NOW,
  );
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("payment policy not in bootstrap"), true);
});

Deno.test("validateManifest rejects evidence older than 24 hours", () => {
  const manifest = validManifest({
    evidence: {
      ...validManifest().evidence,
      sourceCheckedAt: "2026-08-14T11:59:00Z",
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("evidence is older than 24 hours"), true);
});

Deno.test("validateManifest rejects a SKU already in bootstrap", () => {
  const report = validateManifest(
    validManifest(),
    validBootstrap({ existingSkus: ["SKU-TEST-001"] }),
    NOW,
  );
  assertEquals(report.pass, false);
  assertEquals(report.errors.includes("SKU already exists in bootstrap"), true);
});

Deno.test("validateManifest rejects an unsupported claim without an aspect source", () => {
  const manifest = validManifest({
    product: {
      ...validManifest().product,
      title: "Waterproof Pool Chlorinator Cell",
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(
    report.errors.includes("unsupported claim without source: waterproof"),
    true,
  );
});

Deno.test("validateManifest allows a claim backed by an aspect source", () => {
  const manifest = validManifest({
    product: {
      ...validManifest().product,
      title: "Waterproof Pool Chlorinator Cell",
      aspects: { Brand: ["Generic"], Waterproof: ["Yes"] },
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(
    report.errors.includes("unsupported claim without source: waterproof"),
    false,
  );
});

Deno.test("validateManifest rejects trademark symbols", () => {
  const manifest = validManifest({
    product: {
      ...validManifest().product,
      title: "Pool Chlorinator™ Cell",
    },
  });
  const report = validateManifest(manifest, validBootstrap(), NOW);
  assertEquals(report.pass, false);
  assertEquals(
    report.errors.includes("trademark symbols are not allowed"),
    true,
  );
});

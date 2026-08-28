import type {
  AccountBootstrap,
  ListingManifest,
  ValidationReport,
} from "./types.ts";

const SKU_PATTERN = /^[A-Z0-9][A-Z0-9._-]{2,49}$/;
const PRICE_PATTERN = /^\d+\.\d{2}$/;
const HOURS_24_MS = 24 * 60 * 60 * 1000;

const BLOCKED_CLAIMS = [
  "bpa-free",
  "bpa free",
  "waterproof",
  "safe",
  "streak-free",
  "streak free",
  "eye care",
];

const TOP_LEVEL_KEYS = new Set([
  "version",
  "sku",
  "marketplaceId",
  "product",
  "condition",
  "categoryId",
  "quantity",
  "price",
  "merchantLocationKey",
  "policies",
  "evidence",
]);

const PRODUCT_KEYS = new Set(["title", "description", "aspects", "imageUrls"]);
const EVIDENCE_KEYS = new Set([
  "supplierUrl",
  "sourceCheckedAt",
  "stockObserved",
  "supplierCostUsd",
  "deliveryLatestDays",
  "imageRights",
  "vero",
  "estimatedEbayFeesUsd",
  "estimatedFulfillmentUsd",
  "estimatedNetProfitUsd",
]);

function asRecord(value: unknown, name: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${name} must be an object`);
  }
  return value as Record<string, unknown>;
}

function asString(value: unknown, name: string): string {
  if (typeof value !== "string") throw new Error(`${name} must be a string`);
  return value;
}

function asNumber(value: unknown, name: string): number {
  if (typeof value !== "number") throw new Error(`${name} must be a number`);
  return value;
}

function rejectUnknown(
  record: Record<string, unknown>,
  allowed: Set<string>,
  label: string,
): void {
  for (const key of Object.keys(record)) {
    if (!allowed.has(key)) throw new Error(`Unknown ${label} field: ${key}`);
  }
}

/** Parses and structurally validates a manifest, rejecting unknown fields. */
export function parseManifest(value: unknown): ListingManifest {
  const record = asRecord(value, "manifest");
  rejectUnknown(record, TOP_LEVEL_KEYS, "manifest");

  const product = asRecord(record.product, "manifest.product");
  rejectUnknown(product, PRODUCT_KEYS, "product");

  const evidence = asRecord(record.evidence, "manifest.evidence");
  rejectUnknown(evidence, EVIDENCE_KEYS, "evidence");

  const policies = asRecord(record.policies, "manifest.policies");
  const price = asRecord(record.price, "manifest.price");

  asNumber(record.version, "version");
  asString(record.sku, "sku");
  asString(record.marketplaceId, "marketplaceId");
  asString(record.condition, "condition");
  asString(record.categoryId, "categoryId");
  asNumber(record.quantity, "quantity");
  asString(record.merchantLocationKey, "merchantLocationKey");
  asString(product.title, "product.title");
  asString(product.description, "product.description");
  asRecord(product.aspects, "product.aspects");
  if (!Array.isArray(product.imageUrls)) {
    throw new Error("product.imageUrls must be an array");
  }
  asString(price.value, "price.value");
  asString(price.currency, "price.currency");
  asString(policies.payment, "policies.payment");
  asString(policies.fulfillment, "policies.fulfillment");
  asString(policies.return, "policies.return");
  asString(evidence.supplierUrl, "evidence.supplierUrl");
  asString(evidence.sourceCheckedAt, "evidence.sourceCheckedAt");
  asNumber(evidence.stockObserved, "evidence.stockObserved");
  asString(evidence.supplierCostUsd, "evidence.supplierCostUsd");
  asNumber(evidence.deliveryLatestDays, "evidence.deliveryLatestDays");
  asString(evidence.imageRights, "evidence.imageRights");
  asString(evidence.vero, "evidence.vero");
  asString(evidence.estimatedEbayFeesUsd, "evidence.estimatedEbayFeesUsd");
  asString(
    evidence.estimatedFulfillmentUsd,
    "evidence.estimatedFulfillmentUsd",
  );
  asString(evidence.estimatedNetProfitUsd, "evidence.estimatedNetProfitUsd");

  return record as unknown as ListingManifest;
}

/**
 * Local fail-closed validation: only facts present in the bootstrap, a
 * 24-hour evidence window, VeRO PASS and a positive margin gate produce PASS.
 */
export function validateManifest(
  manifest: ListingManifest,
  bootstrap: AccountBootstrap,
  now: Date = new Date(),
): ValidationReport {
  const errors: string[] = [];
  const warnings: string[] = [];
  const evidenceFreshAt = manifest.evidence.sourceCheckedAt;

  if (manifest.version !== 1) errors.push("version must be 1");
  if (!SKU_PATTERN.test(manifest.sku)) errors.push("invalid SKU format");
  if (manifest.marketplaceId !== "EBAY_US") {
    errors.push("marketplaceId must be EBAY_US");
  }

  const title = manifest.product.title.trim();
  if (title.length < 1 || title.length > 80) {
    errors.push("title must be 1-80 characters");
  }

  const description = manifest.product.description;
  if (description.length < 1 || description.length > 4000) {
    errors.push("description must be 1-4000 characters");
  }

  const images = manifest.product.imageUrls;
  if (images.length < 1 || images.length > 12) {
    errors.push("must have 1-12 image URLs");
  } else {
    if (new Set(images).size !== images.length) {
      errors.push("duplicate image URLs");
    }
    for (const img of images) {
      try {
        if (new URL(img).protocol !== "https:") {
          errors.push("image URLs must be HTTPS");
        }
      } catch {
        errors.push("invalid image URL");
      }
    }
  }

  if (manifest.condition !== "NEW") errors.push("condition must be NEW");
  if (!manifest.categoryId) errors.push("categoryId is required");

  if (!Number.isInteger(manifest.quantity) || manifest.quantity <= 0) {
    errors.push("quantity must be a positive integer");
  }

  const price = manifest.price;
  if (price.currency !== "USD") errors.push("price currency must be USD");
  if (!PRICE_PATTERN.test(price.value)) {
    errors.push("price must have exactly two decimals");
  } else if (Number(price.value) <= 0) {
    errors.push("price must be positive");
  }

  if (!bootstrap.paymentPolicyIds.includes(manifest.policies.payment)) {
    errors.push("payment policy not in bootstrap");
  }
  if (!bootstrap.fulfillmentPolicyIds.includes(manifest.policies.fulfillment)) {
    errors.push("fulfillment policy not in bootstrap");
  }
  if (!bootstrap.returnPolicyIds.includes(manifest.policies.return)) {
    errors.push("return policy not in bootstrap");
  }
  if (!bootstrap.merchantLocationKeys.includes(manifest.merchantLocationKey)) {
    errors.push("merchant location not in bootstrap");
  }

  const evidence = manifest.evidence;
  const checkedAt = new Date(evidence.sourceCheckedAt);
  if (Number.isNaN(checkedAt.getTime())) {
    errors.push("invalid evidence timestamp");
  } else {
    const ageMs = now.getTime() - checkedAt.getTime();
    if (ageMs < 0) errors.push("evidence timestamp is in the future");
    else if (ageMs > HOURS_24_MS) {
      errors.push("evidence is older than 24 hours");
    }
  }

  if (evidence.deliveryLatestDays > 10) {
    errors.push("delivery latest exceeds 10 days");
  }
  if (evidence.vero !== "PASS") errors.push("VeRO must be PASS");
  if (
    evidence.imageRights !== "SUPPLIER_AUTHORIZED" &&
    evidence.imageRights !== "OWNER_OWNED"
  ) {
    errors.push("imageRights must be SUPPLIER_AUTHORIZED or OWNER_OWNED");
  }

  const salePrice = Number(price.value);
  const netProfit = Number(evidence.estimatedNetProfitUsd);
  if (!Number.isFinite(netProfit)) {
    errors.push("estimatedNetProfitUsd must be a number");
  } else if (netProfit < 5) {
    errors.push("net profit below $5");
  } else if (salePrice > 0 && netProfit < salePrice * 0.10) {
    errors.push("net profit below 10% of sale price");
  }

  const titleDesc = (title + " " + description).toLowerCase();
  const aspectValues = Object.entries(manifest.product.aspects ?? {})
    .flatMap(([k, v]) => [k, ...v])
    .map((v) => v.toLowerCase())
    .join(" ");
  for (const claim of BLOCKED_CLAIMS) {
    if (titleDesc.includes(claim) && !aspectValues.includes(claim)) {
      errors.push(`unsupported claim without source: ${claim}`);
    }
  }

  if (/[®™]/u.test(title + description)) {
    errors.push("trademark symbols are not allowed");
  }

  if (
    bootstrap.existingSkus.includes(manifest.sku) ||
    bootstrap.existingOfferSkus.includes(manifest.sku)
  ) {
    errors.push("SKU already exists in bootstrap");
  }

  return {
    pass: errors.length === 0,
    errors,
    warnings,
    evidenceFreshAt,
  };
}

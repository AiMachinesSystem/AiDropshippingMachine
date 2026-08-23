import type { ListingManifest } from "./types.ts";

/** Recursively sorts object keys so equal values canonicalize identically. */
function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    const record = value as Record<string, unknown>;
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(record).sort()) {
      out[key] = canonicalize(record[key]);
    }
    return out;
  }
  return value;
}

/** Deterministic JSON: sorted keys, preserved array order, strings untouched. */
export function canonicalJson(value: unknown): string {
  return JSON.stringify(canonicalize(value));
}

/** Lowercase hex SHA-256 of the canonical JSON for `value`. */
export async function sha256Canonical(value: unknown): Promise<string> {
  const bytes = new TextEncoder().encode(canonicalJson(value));
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

/**
 * eBay Sell Inventory `inventory_item` body. Carries only listing facts the
 * marketplace needs; supplier URL, cost and audit-only evidence never leave this
 * machine, so they are omitted by construction.
 */
export function buildInventoryPayload(manifest: ListingManifest): unknown {
  return {
    availability: {
      shipToLocationAvailability: { quantity: manifest.quantity },
    },
    condition: manifest.condition,
    product: {
      title: manifest.product.title,
      description: manifest.product.description,
      aspects: manifest.product.aspects,
      imageUrls: manifest.product.imageUrls,
    },
  };
}

/** eBay Sell Inventory `offer` body: SKU, marketplace, category, price, policies. */
export function buildOfferPayload(manifest: ListingManifest): unknown {
  return {
    sku: manifest.sku,
    marketplaceId: manifest.marketplaceId,
    format: "FIXED_PRICE",
    categoryId: manifest.categoryId,
    merchantLocationKey: manifest.merchantLocationKey,
    availableQuantity: manifest.quantity,
    pricingSummary: {
      price: {
        value: manifest.price.value,
        currency: manifest.price.currency,
      },
    },
    listingDescription: manifest.product.description,
    listingPolicies: {
      fulfillmentPolicyId: manifest.policies.fulfillment,
      paymentPolicyId: manifest.policies.payment,
      returnPolicyId: manifest.policies.return,
    },
  };
}

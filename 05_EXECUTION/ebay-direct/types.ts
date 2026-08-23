/**
 * Shared types for the eBay direct Production client.
 *
 * Single source of truth so producer and consumer modules agree on the same
 * names. No secrets live here; credentials are typed only as opaque strings.
 */

export type MarketplaceId = "EBAY_US";
export type Locale = "en-US";
export type Currency = "USD";
export type ConditionId = "NEW";

export const PRODUCTION_BASE_URL = "https://api.ebay.com";
export const PRODUCTION_AUTH_URL = "https://auth.ebay.com";

export interface EbayConfig {
  clientId: string;
  clientSecret: string;
  ruName: string;
  refreshToken: string;
  marketplaceId: MarketplaceId;
  locale: Locale;
  baseUrl: string;
  authUrl: string;
}

export interface SafeError {
  name: string;
  message: string;
  status?: number;
  errorIds?: number[];
  domains?: string[];
  categories?: string[];
  cause?: SafeError | null;
}

export interface AccountBootstrap {
  ready: boolean;
  blockers: string[];
  sellerUsername?: string;
  privileges: Array<Record<string, unknown>>;
  paymentPolicyIds: string[];
  fulfillmentPolicyIds: string[];
  returnPolicyIds: string[];
  merchantLocationKeys: string[];
  existingSkus: string[];
  existingOfferSkus: string[];
  checkedAt: string;
}

export interface ListingEvidence {
  supplierUrl: string;
  sourceCheckedAt: string;
  stockObserved: number;
  supplierCostUsd: string;
  deliveryLatestDays: number;
  imageRights: "SUPPLIER_AUTHORIZED" | "OWNER_OWNED";
  vero: "PASS";
  estimatedEbayFeesUsd: string;
  estimatedFulfillmentUsd: string;
  estimatedNetProfitUsd: string;
}

export interface ListingManifest {
  version: 1;
  sku: string;
  marketplaceId: MarketplaceId;
  product: {
    title: string;
    description: string;
    aspects: Record<string, string[]>;
    imageUrls: string[];
  };
  condition: ConditionId;
  categoryId: string;
  quantity: number;
  price: { value: string; currency: Currency };
  merchantLocationKey: string;
  policies: { payment: string; fulfillment: string; return: string };
  evidence: ListingEvidence;
}

export interface ValidationReport {
  pass: boolean;
  errors: string[];
  warnings: string[];
  evidenceFreshAt: string;
}

export interface ActionPack {
  version: 1;
  sku: string;
  manifestSha256: string;
  inventoryAction: { method: "PUT"; path: string; payloadSha256: string };
  offerAction: { method: "POST"; path: string; payloadSha256: string };
  publishAction: { method: "POST"; pathTemplate: string };
  effect: string;
  risk: string;
  rollback: string;
  validation: { pass: true; checkedAt: string };
  packSha256: string;
}

export interface AuditRecord {
  timestamp: string;
  stage: string;
  sku: string;
  actionPackSha256: string;
  httpStatus: number;
  ebayErrorIds: string[];
  offerId?: string;
  listingId?: string;
  verificationResult?: string;
}

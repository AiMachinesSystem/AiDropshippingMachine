import type {
  AccountBootstrap,
  ActionPack,
  ListingManifest,
  ValidationReport,
} from "./types.ts";
import {
  buildInventoryPayload,
  buildOfferPayload,
  sha256Canonical,
} from "./payloads.ts";

/**
 * Builds a dry-run action pack for a validation-PASS manifest. The pack hash is
 * computed from the pack without its own hash, so the Owner can name it in a GO.
 * Refuses to produce a pack unless validation passed and the bootstrap is ready.
 */
export async function buildActionPack(
  manifest: ListingManifest,
  validation: ValidationReport,
  bootstrap: AccountBootstrap,
): Promise<ActionPack> {
  if (!validation.pass) {
    throw new Error("Cannot build action pack: validation did not PASS");
  }
  if (!bootstrap.ready) {
    throw new Error("Cannot build action pack: bootstrap is not ready");
  }

  const inventoryPayload = buildInventoryPayload(manifest);
  const offerPayload = buildOfferPayload(manifest);

  const manifestSha256 = await sha256Canonical(manifest);
  const inventoryPayloadSha256 = await sha256Canonical(inventoryPayload);
  const offerPayloadSha256 = await sha256Canonical(offerPayload);

  const packWithoutHash = {
    version: 1,
    sku: manifest.sku,
    manifestSha256,
    inventoryAction: {
      method: "PUT",
      path: `/sell/inventory/v1/inventory_item/${manifest.sku}`,
      payloadSha256: inventoryPayloadSha256,
    },
    offerAction: {
      method: "POST",
      path: "/sell/inventory/v1/offer",
      payloadSha256: offerPayloadSha256,
    },
    publishAction: {
      method: "POST",
      pathTemplate: "/sell/inventory/v1/offer/{offerId}/publish",
    },
    effect:
      `Publish inventory item ${manifest.sku} to ${manifest.marketplaceId} at ` +
      `${manifest.price.value} ${manifest.price.currency}`,
    risk:
      "Creates a live eBay listing; reversible via withdrawOffer (offer unpublished, inventory retained).",
    rollback: `withdrawOffer for ${manifest.sku}`,
    validation: {
      pass: true,
      checkedAt: validation.evidenceFreshAt,
    },
  };

  const packSha256 = await sha256Canonical(packWithoutHash);

  return { ...packWithoutHash, packSha256 } as ActionPack;
}

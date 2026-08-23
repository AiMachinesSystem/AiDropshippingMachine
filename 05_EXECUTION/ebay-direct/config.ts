import {
  type EbayConfig,
  type Locale,
  type MarketplaceId,
  PRODUCTION_AUTH_URL,
  PRODUCTION_BASE_URL,
} from "./types.ts";

const SANDBOX_MARKERS = ["sandbox", "api.sandbox.ebay.com"];

/**
 * Strict environment loading. Returns a fully populated config or throws; it
 * never logs values and never accepts Sandbox endpoints in Production.
 */
export function loadConfig(
  env: Record<string, string | undefined>,
  opts: { requireRefreshToken?: boolean } = {},
): EbayConfig {
  const clientId = env["EBAY_CLIENT_ID"] ?? "";
  const clientSecret = env["EBAY_CLIENT_SECRET"] ?? "";
  const ruName = env["EBAY_RUNAME"] ?? "";
  const refreshToken = env["EBAY_REFRESH_TOKEN"] ?? "";
  const marketplaceId = (env["EBAY_MARKETPLACE_ID"] ??
    "EBAY_US") as MarketplaceId;
  const locale = (env["EBAY_LOCALE"] ?? "en-US") as Locale;
  const baseUrl = env["EBAY_API_BASE_URL"] ?? PRODUCTION_BASE_URL;
  const authUrl = env["EBAY_AUTH_URL"] ?? PRODUCTION_AUTH_URL;

  if (marketplaceId !== "EBAY_US") {
    throw new Error("Only EBAY_US marketplace is supported in Production");
  }

  for (const [name, value] of Object.entries({ baseUrl, authUrl })) {
    const lower = value.toLowerCase();
    if (SANDBOX_MARKERS.some((marker) => lower.includes(marker))) {
      throw new Error(
        `Sandbox endpoints are not allowed in Production (${name})`,
      );
    }
  }

  const missing = [
    ["EBAY_CLIENT_ID", clientId],
    ["EBAY_CLIENT_SECRET", clientSecret],
    ["EBAY_RUNAME", ruName],
    ...(opts.requireRefreshToken === false
      ? []
      : [["EBAY_REFRESH_TOKEN", refreshToken] as const]),
  ].filter(([, value]) => value.length === 0).map(([key]) => key);

  if (missing.length > 0) {
    throw new Error(`Missing required configuration: ${missing.join(", ")}`);
  }

  return {
    clientId,
    clientSecret,
    ruName,
    refreshToken,
    marketplaceId,
    locale,
    baseUrl,
    authUrl,
  };
}

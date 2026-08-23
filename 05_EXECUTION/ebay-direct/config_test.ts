import { assertEquals, assertThrows } from "@std/assert";
import { loadConfig } from "./config.ts";

const PRODUCTION_ENV = {
  EBAY_CLIENT_ID: "client",
  EBAY_CLIENT_SECRET: "secret",
  EBAY_RUNAME: "runame",
  EBAY_REFRESH_TOKEN: "refresh",
} as const;

Deno.test("loadConfig loads Production values without echoing them", () => {
  const config = loadConfig({ ...PRODUCTION_ENV });
  assertEquals(config.clientId, "client");
  assertEquals(config.marketplaceId, "EBAY_US");
  assertEquals(config.locale, "en-US");
  assertEquals(config.baseUrl, "https://api.ebay.com");
  assertEquals(config.authUrl, "https://auth.ebay.com");
});

Deno.test("loadConfig rejects Sandbox endpoints", () => {
  assertThrows(
    () =>
      loadConfig({
        ...PRODUCTION_ENV,
        EBAY_API_BASE_URL: "https://api.sandbox.ebay.com",
      }),
    Error,
    "Production",
  );
});

Deno.test("loadConfig rejects a non-EBAY_US marketplace", () => {
  assertThrows(
    () => loadConfig({ ...PRODUCTION_ENV, EBAY_MARKETPLACE_ID: "EBAY_DE" }),
    Error,
    "EBAY_US",
  );
});

Deno.test("loadConfig names missing required secrets without their values", () => {
  assertThrows(
    () => loadConfig({ ...PRODUCTION_ENV, EBAY_CLIENT_SECRET: "" }),
    Error,
    "EBAY_CLIENT_SECRET",
  );
});

Deno.test("loadConfig tolerates an empty refresh token before oauth-exchange", () => {
  const config = loadConfig(
    { ...PRODUCTION_ENV, EBAY_REFRESH_TOKEN: "" },
    { requireRefreshToken: false },
  );
  assertEquals(config.refreshToken, "");
  assertEquals(config.clientId, "client");
});

Deno.test("loadConfig still rejects a missing client secret when refresh token is optional", () => {
  assertThrows(
    () =>
      loadConfig(
        { ...PRODUCTION_ENV, EBAY_CLIENT_SECRET: "", EBAY_REFRESH_TOKEN: "" },
        { requireRefreshToken: false },
      ),
    Error,
    "EBAY_CLIENT_SECRET",
  );
});

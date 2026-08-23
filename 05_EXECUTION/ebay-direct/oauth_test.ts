import { assertEquals, assertStringIncludes, assertThrows } from "@std/assert";
import {
  buildConsentUrl,
  createOAuthState,
  exchangeCode,
  parseRedirect,
  refreshAccessToken,
} from "./oauth.ts";
import { safeError } from "./redaction.ts";
import type { EbayConfig } from "./types.ts";

const testConfig: EbayConfig = {
  clientId: "client-id",
  clientSecret: "client-secret",
  ruName: "RU_NAME_VALUE",
  refreshToken: "refresh-token-value",
  marketplaceId: "EBAY_US",
  locale: "en-US",
  baseUrl: "https://api.ebay.com",
  authUrl: "https://auth.ebay.com",
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status });
}

Deno.test("consent URL is Production and least-privilege", () => {
  const url = buildConsentUrl(testConfig, "state-123");
  assertEquals(url.origin, "https://auth.ebay.com");
  assertEquals(url.searchParams.get("response_type"), "code");
  assertEquals(url.searchParams.get("redirect_uri"), testConfig.ruName);
  assertEquals(
    url.searchParams.get("scope")?.split(" ").sort(),
    [
      "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
      "https://api.ebay.com/oauth/api_scope/sell.inventory",
    ],
  );
  assertEquals(url.searchParams.get("state"), "state-123");
  assertEquals(url.searchParams.get("client_id"), "client-id");
});

Deno.test("createOAuthState is unpredictable and non-empty", () => {
  const a = createOAuthState();
  const b = createOAuthState();
  assertEquals(a.length > 0, true);
  assertEquals(a === b, false);
});

Deno.test("redirect state mismatch fails closed", () => {
  assertThrows(
    () =>
      parseRedirect(
        new URL("https://example.invalid/?state=wrong&code=single-use"),
        "expected",
      ),
    Error,
    "state",
  );
});

Deno.test("redirect with error param or missing code is rejected", () => {
  assertThrows(
    () =>
      parseRedirect(
        new URL("https://e.invalid/?state=s&error=access_denied"),
        "s",
      ),
    Error,
    "error",
  );
  assertThrows(
    () => parseRedirect(new URL("https://e.invalid/?state=s"), "s"),
    Error,
    "code",
  );
});

Deno.test("parseRedirect returns the single-use code on success", () => {
  const code = parseRedirect(
    new URL("https://e.invalid/?state=s&code=abc"),
    "s",
  );
  assertEquals(code, "abc");
});

Deno.test("exchangeCode posts form-encoded and returns the grant", async () => {
  const fetcher = (url: string, init: RequestInit) => {
    assertEquals(url, "https://api.ebay.com/identity/v1/oauth2/token");
    assertEquals(init.method, "POST");
    const body = init.body as string;
    assertStringIncludes(body, "grant_type=authorization_code");
    assertStringIncludes(body, "code=abc");
    assertStringIncludes(body, `redirect_uri=${testConfig.ruName}`);
    return Promise.resolve(
      jsonResponse({
        access_token: "access-value",
        expires_in: 7200,
        token_type: "Application Access Token",
        refresh_token: "refresh-value",
      }),
    );
  };
  const grant = await exchangeCode(
    fetcher as unknown as typeof fetch,
    testConfig,
    "abc",
  );
  assertEquals(grant.access_token, "access-value");
  assertEquals(grant.refresh_token, "refresh-value");
});

Deno.test("refreshAccessToken uses grant_type=refresh_token", async () => {
  const fetcher = (_url: string, init: RequestInit) => {
    const body = init.body as string;
    assertStringIncludes(body, "grant_type=refresh_token");
    assertStringIncludes(body, `refresh_token=${testConfig.refreshToken}`);
    return Promise.resolve(
      jsonResponse({
        access_token: "new-access-value",
        expires_in: 7200,
        token_type: "Application Access Token",
      }),
    );
  };
  const grant = await refreshAccessToken(
    fetcher as unknown as typeof fetch,
    testConfig,
  );
  assertEquals(grant.access_token, "new-access-value");
});

Deno.test("token failure carries status and is redacted by safeError", async () => {
  const fetcher = () =>
    Promise.resolve(
      jsonResponse({
        error: "invalid_grant",
        error_description: "the refresh-token-value is bad",
      }, 400),
    );
  let thrown: unknown;
  try {
    await refreshAccessToken(fetcher as unknown as typeof fetch, testConfig);
  } catch (err) {
    thrown = err;
  }
  const safe = safeError(thrown, ["refresh-token-value"]);
  assertEquals(safe.message.includes("refresh-token-value"), false);
  assertEquals(safe.status, 400);
});

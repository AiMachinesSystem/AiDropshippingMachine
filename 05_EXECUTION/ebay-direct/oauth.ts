import type { EbayConfig } from "./types.ts";

const OAUTH_SCOPES = [
  "https://api.ebay.com/oauth/api_scope/sell.inventory",
  "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
] as const;

const TOKEN_ENDPOINT = "/identity/v1/oauth2/token";

export interface TokenGrant {
  access_token: string;
  expires_in: number;
  token_type: string;
  refresh_token?: string;
}

export interface AccessGrant {
  access_token: string;
  expires_in: number;
  token_type: string;
}

export function createOAuthState(): string {
  return crypto.randomUUID() + crypto.randomUUID();
}

/** Builds the Production consent URL with the minimum two scopes. */
export function buildConsentUrl(config: EbayConfig, state: string): URL {
  const url = new URL(`${config.authUrl}/oauth2/authorize`);
  url.searchParams.set("client_id", config.clientId);
  url.searchParams.set("redirect_uri", config.ruName);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("locale", config.locale);
  url.searchParams.set("scope", OAUTH_SCOPES.join(" "));
  url.searchParams.set("state", state);
  return url;
}

/**
 * Validates the redirect and returns the single-use authorization code.
 * Fails closed on state mismatch, a missing code, or an `error` parameter.
 */
export function parseRedirect(url: URL, expectedState: string): string {
  if (url.searchParams.has("error")) {
    throw new Error(
      `OAuth redirect error: ${url.searchParams.get("error") ?? "unknown"}`,
    );
  }
  const state = url.searchParams.get("state") ?? "";
  if (state !== expectedState) {
    throw new Error("OAuth state mismatch");
  }
  const code = url.searchParams.get("code") ?? "";
  if (!code) {
    throw new Error("OAuth redirect missing authorization code");
  }
  return code;
}

async function requestToken(
  fetcher: typeof fetch,
  config: EbayConfig,
  body: URLSearchParams,
): Promise<TokenGrant> {
  const basic = btoa(`${config.clientId}:${config.clientSecret}`);
  const response = await fetcher(`${config.baseUrl}${TOKEN_ENDPOINT}`, {
    method: "POST",
    headers: {
      "Authorization": `Basic ${basic}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });

  const text = await response.text();
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw Object.assign(
      new Error(`Token endpoint returned non-JSON (HTTP ${response.status})`),
      { status: response.status },
    );
  }

  if (!response.ok) {
    const record = parsed as Record<string, unknown>;
    throw Object.assign(
      new Error(
        `Token request failed (HTTP ${response.status}): ${
          record.error ?? "unknown"
        }`,
      ),
      { status: response.status, error: record.error },
    );
  }

  return parsed as TokenGrant;
}

export async function exchangeCode(
  fetcher: typeof fetch,
  config: EbayConfig,
  code: string,
): Promise<TokenGrant> {
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    code,
    redirect_uri: config.ruName,
  });
  return await requestToken(fetcher, config, body);
}

export async function refreshAccessToken(
  fetcher: typeof fetch,
  config: EbayConfig,
): Promise<AccessGrant> {
  const body = new URLSearchParams({
    grant_type: "refresh_token",
    refresh_token: config.refreshToken,
    scope: OAUTH_SCOPES.join(" "),
  });
  return await requestToken(fetcher, config, body);
}

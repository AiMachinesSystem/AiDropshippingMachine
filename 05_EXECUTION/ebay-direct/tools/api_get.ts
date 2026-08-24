/**
 * Read-only helper: GETs an arbitrary Production API path with the user token
 * from .env.local and prints the JSON. No writes to eBay.
 *
 * Usage:
 *   deno run --allow-net=api.ebay.com,auth.ebay.com --allow-read=.env.local \
 *     --allow-env tools/api_get.ts "/sell/inventory/v1/offer/244469781011"
 */
import { loadConfig } from "../config.ts";
import { refreshAccessToken } from "../oauth.ts";

async function loadEnvLocal(): Promise<Record<string, string | undefined>> {
  const env: Record<string, string | undefined> = { ...Deno.env.toObject() };
  try {
    const text = await Deno.readTextFile(".env.local");
    for (const line of text.split("\n")) {
      const match = line.match(/^([A-Z0-9_]+)=(.*)$/);
      if (match) env[match[1]] = match[2];
    }
  } catch {
    // config loader will surface missing secrets
  }
  return env;
}

const path = Deno.args[0];
if (!path || !path.startsWith("/")) {
  console.error("usage: api_get.ts /<api-path>");
  Deno.exit(1);
}

const config = loadConfig(await loadEnvLocal());
const grant = await refreshAccessToken(fetch, config);
const res = await fetch(`${config.baseUrl}${path}`, {
  headers: {
    "Authorization": `Bearer ${grant.access_token}`,
    "X-EBAY-C-MARKETPLACE-ID": config.marketplaceId,
    "Content-Language": config.locale,
    "Accept-Language": config.locale,
  },
});
const text = await res.text();
console.log(`HTTP ${res.status}`);
try {
  console.log(JSON.stringify(JSON.parse(text), null, 2));
} catch {
  console.log(text);
}

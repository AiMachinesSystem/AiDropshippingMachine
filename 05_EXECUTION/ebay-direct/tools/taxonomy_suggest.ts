/**
 * Read-only helper: asks the eBay Taxonomy API (Production) for category
 * suggestions for a product query. Uses the existing OAuth refresh token from
 * .env.local. No writes to eBay, no secrets echoed.
 *
 * Usage:
 *   deno run --allow-net=api.ebay.com,auth.ebay.com --allow-read=.env.local \
 *     --allow-env tools/taxonomy_suggest.ts "salt cell pool chlorinator"
 */
import { loadConfig } from "../config.ts";

/** Application access token via client-credentials grant (read-only scope). */
async function applicationToken(
  config: { clientId: string; clientSecret: string; baseUrl: string },
): Promise<string> {
  const res = await fetch(`${config.baseUrl}/identity/v1/oauth2/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": `Basic ${btoa(`${config.clientId}:${config.clientSecret}`)}`,
    },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      scope: "https://api.ebay.com/oauth/api_scope",
    }),
  });
  if (!res.ok) throw new Error(`token grant failed HTTP ${res.status}`);
  const data = await res.json();
  return data.access_token as string;
}

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

const query = Deno.args[0];
if (!query) {
  console.error("usage: taxonomy_suggest.ts <query>");
  Deno.exit(1);
}

const config = loadConfig(await loadEnvLocal(), { requireRefreshToken: false });
const accessToken = await applicationToken(config);

const url = `${config.baseUrl}/commerce/taxonomy/v1/category_tree/0/` +
  `get_category_suggestions?q=${encodeURIComponent(query)}`;
const res = await fetch(url, {
  headers: {
    "Authorization": `Bearer ${accessToken}`,
    "X-EBAY-C-MARKETPLACE-ID": config.marketplaceId,
    "Accept-Language": config.locale,
  },
});
if (!res.ok) {
  console.error(`taxonomy API error HTTP ${res.status}`);
  Deno.exit(1);
}
const data = await res.json();
const suggestions = (data.categorySuggestions ?? []).map((s: unknown) => {
  const rec = s as {
    category: { categoryId: string; categoryName: string };
    categoryTreeNodeAncestors?: Array<{ categoryName: string }>;
  };
  const path = (rec.categoryTreeNodeAncestors ?? [])
    .map((a) => a.categoryName).join(" > ");
  return {
    categoryId: rec.category.categoryId,
    categoryName: rec.category.categoryName,
    path,
  };
});
console.log(JSON.stringify({ query, suggestions }, null, 2));

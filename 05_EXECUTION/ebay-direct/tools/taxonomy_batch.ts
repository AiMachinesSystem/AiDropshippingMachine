/**
 * Read-only helper: batch category suggestions. Reads a JSON file of
 * [{ sku, query }] and prints [{ sku, query, top }]. No writes to eBay.
 *
 * Usage:
 *   deno run --allow-net=api.ebay.com --allow-read=.env.local,<input.json> \
 *     --allow-env tools/taxonomy_batch.ts <input.json>
 */
import { loadConfig } from "../config.ts";

async function appToken(config: {
  clientId: string;
  clientSecret: string;
  baseUrl: string;
}): Promise<string> {
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
  return (await res.json()).access_token as string;
}

async function loadEnvLocal(): Promise<Record<string, string | undefined>> {
  const env: Record<string, string | undefined> = { ...Deno.env.toObject() };
  const text = await Deno.readTextFile(".env.local");
  for (const line of text.split("\n")) {
    const match = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (match) env[match[1]] = match[2];
  }
  return env;
}

const inputPath = Deno.args[0];
const queries = JSON.parse(await Deno.readTextFile(inputPath)) as Array<{
  sku: string;
  query: string;
}>;

const config = loadConfig(await loadEnvLocal(), { requireRefreshToken: false });
const token = await appToken(config);

const out = [];
for (const { sku, query } of queries) {
  const url = `${config.baseUrl}/commerce/taxonomy/v1/category_tree/0/` +
    `get_category_suggestions?q=${encodeURIComponent(query)}`;
  const res = await fetch(url, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    },
  });
  if (!res.ok) {
    out.push({ sku, query, error: res.status });
    continue;
  }
  const data = await res.json();
  const first = (data.categorySuggestions ?? [])[0];
  out.push({
    sku,
    query,
    top: first
      ? {
        categoryId: first.category.categoryId,
        categoryName: first.category.categoryName,
        path: (first.categoryTreeNodeAncestors ?? [])
          .map((a: { categoryName: string }) => a.categoryName).join(" > "),
      }
      : null,
  });
}
console.log(JSON.stringify(out, null, 2));

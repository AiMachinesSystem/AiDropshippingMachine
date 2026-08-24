// probe: list seller's live items via eBay Browse API (client-credentials)
const env = (await Deno.readTextFile("05_EXECUTION/ebay-direct/.env.local"))
  .split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"))
  .reduce((m: Record<string,string>, l) => { const i = l.indexOf("="); if (i>0) m[l.slice(0,i)] = l.slice(i+1); return m; }, {});

const id = env.EBAY_CLIENT_ID!;
const sec = env.EBAY_CLIENT_SECRET!;

const basic = btoa(`${id}:${sec}`);
const tokRes = await fetch("https://api.ebay.com/identity/v1/oauth2/token", {
  method: "POST",
  headers: {
    "Authorization": `Basic ${basic}`,
    "Content-Type": "application/x-www-form-urlencoded",
  },
  body: new URLSearchParams({
    grant_type: "client_credentials",
    scope: "https://api.ebay.com/oauth/api_scope",
  }),
});
const tokJson = await tokRes.json();
if (!tokRes.ok) { console.log("TOKEN ERR", tokRes.status, JSON.stringify(tokJson)); Deno.exit(1); }
const token = tokJson.access_token;

const q = new URLSearchParams({
  filter: "sellers:{divinit-92}",
  limit: "50",
});
const itemsRes = await fetch(`https://api.ebay.com/buy/browse/v1/item_summary/search?${q}`, {
  headers: { "Authorization": `Bearer ${token}`, "X-EBAY-C-MARKETPLACE-ID": "EBAY_US" },
});
const itemsJson = await itemsRes.json();
if (!itemsRes.ok) { console.log("SEARCH ERR", itemsRes.status, JSON.stringify(itemsJson).slice(0,500)); Deno.exit(1); }
console.log("TOTAL", itemsJson.total);
for (const it of (itemsJson.itemSummaries ?? [])) {
  console.log("---");
  console.log("title:", it.title);
  console.log("price:", it.price?.value, it.price?.currency);
  console.log("categoryId:", it.categories?.[0]?.categoryId, it.categories?.[0]?.categoryName);
  console.log("image:", it.image?.imageUrl);
  console.log("itemId:", it.itemId);
}

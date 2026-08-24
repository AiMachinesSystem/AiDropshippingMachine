const env = (await Deno.readTextFile("05_EXECUTION/ebay-direct/.env.local"))
  .split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"))
  .reduce((m: Record<string,string>, l) => { const i = l.indexOf("="); if (i>0) m[l.slice(0,i)] = l.slice(i+1); return m; }, {});
const basic = btoa(`${env.EBAY_CLIENT_ID}:${env.EBAY_CLIENT_SECRET}`);
const t = await (await fetch("https://api.ebay.com/identity/v1/oauth2/token", {
  method: "POST", headers: { "Authorization": `Basic ${basic}`, "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ grant_type: "client_credentials", scope: "https://api.ebay.com/oauth/api_scope" }),
})).json();
const token = t.access_token;
// try filter=sellers combined with broad q
for (const q of ["pool", "feeder", "pump"]) {
  const qs = new URLSearchParams({ q, filter: "sellers:{divinit-92}", limit: "30" });
  const r = await fetch(`https://api.ebay.com/buy/browse/v1/item_summary/search?${qs}`, {
    headers: { "Authorization": `Bearer ${token}`, "X-EBAY-C-MARKETPLACE-ID": "EBAY_US" },
  });
  const j = await r.json();
  console.log(`=== q="${q}" filter=sellers total=${j.total} status=${r.status} ===`);
  if (!r.ok) { console.log(JSON.stringify(j).slice(0,200)); continue; }
  for (const it of (j.itemSummaries ?? [])) {
    console.log(`${it.itemId} | ${it.title?.slice(0,55)} | ${it.price?.value} | cat=${it.categories?.[0]?.categoryId} | img=${it.image?.imageUrl?.slice(0,45)}`);
  }
}

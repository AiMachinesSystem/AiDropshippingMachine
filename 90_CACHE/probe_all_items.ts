const env = (await Deno.readTextFile("05_EXECUTION/ebay-direct/.env.local"))
  .split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"))
  .reduce((m: Record<string,string>, l) => { const i = l.indexOf("="); if (i>0) m[l.slice(0,i)] = l.slice(i+1); return m; }, {});
const basic = btoa(`${env.EBAY_CLIENT_ID}:${env.EBAY_CLIENT_SECRET}`);
const t = await (await fetch("https://api.ebay.com/identity/v1/oauth2/token", {
  method: "POST", headers: { "Authorization": `Basic ${basic}`, "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ grant_type: "client_credentials", scope: "https://api.ebay.com/oauth/api_scope" }),
})).json();
const token = t.access_token;
const seen = new Map<string,string>();
const kws = ["pool","feeder","pump","bowl","holder","cover","brush","float","light","organizer","filter","spa","garden","pet","dog","cat"];
for (const q of kws) {
  const qs = new URLSearchParams({ q, filter: "sellers:{divinit-92}", limit: "50" });
  const r = await fetch(`https://api.ebay.com/buy/browse/v1/item_summary/search?${qs}`, {
    headers: { "Authorization": `Bearer ${token}`, "X-EBAY-C-MARKETPLACE-ID": "EBAY_US" },
  });
  if (!r.ok) continue;
  const j = await r.json();
  for (const it of (j.itemSummaries ?? [])) {
    const id = it.itemId?.split("|")[1];
    if (id && !seen.has(id)) seen.set(id, `${it.title?.slice(0,52)} | $${it.price?.value} | cat=${it.categories?.[0]?.categoryId}`);
  }
}
console.log("TOTAL UNIQUE:", seen.size);
let n = 0;
for (const [id, info] of seen) { console.log(`${id} | ${info}`); n++; if (n >= 40) break; }

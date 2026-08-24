const env = (await Deno.readTextFile("05_EXECUTION/ebay-direct/.env.local"))
  .split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"))
  .reduce((m: Record<string,string>, l) => { const i = l.indexOf("="); if (i>0) m[l.slice(0,i)] = l.slice(i+1); return m; }, {});
const basic = btoa(`${env.EBAY_CLIENT_ID}:${env.EBAY_CLIENT_SECRET}`);
const t = await (await fetch("https://api.ebay.com/identity/v1/oauth2/token", {
  method: "POST", headers: { "Authorization": `Basic ${basic}`, "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ grant_type: "client_credentials", scope: "https://api.ebay.com/oauth/api_scope" }),
})).json();
const token = t.access_token;
for (const id of ["v1%7C407113382755%7C0", "407113382755"]) {
  const r = await fetch(`https://api.ebay.com/buy/browse/v1/item/${id}`, {
    headers: { "Authorization": `Bearer ${token}`, "X-EBAY-C-MARKETPLACE-ID": "EBAY_US" },
  });
  console.log(`=== item ${id} status=${r.status} ===`);
  if (r.ok) {
    const j = await r.json();
    console.log("title:", j.title);
    console.log("price:", JSON.stringify(j.price));
    console.log("category:", JSON.stringify(j.categories));
    console.log("images:", JSON.stringify((j.image?.imageUrl ? [j.image.imageUrl, ...(j.additionalImages?.map((x:any)=>x.imageUrl)??[])] : []).slice(0,8)));
    console.log("aspects:", JSON.stringify((j.localizedAspects ?? []).slice(0,12)));
    console.log("condition:", j.condition, "| qty:", j.estimatedAvailabilities?.[0]?.estimatedAvailableQuantity, "| sku:", j.sku);
  } else {
    console.log("err:", (await r.text()).slice(0,200));
  }
}

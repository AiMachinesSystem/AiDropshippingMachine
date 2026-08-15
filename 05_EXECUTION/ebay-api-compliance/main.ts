/**
 * eBay Marketplace Account Deletion / Closure notification endpoint.
 *
 * Spec source: https://developer.ebay.com/develop/guides-v2/marketplace-user-account-deletion
 * Read live 2026-08-14. Two behaviours are mandatory:
 *
 *   GET  ?challenge_code=<code>  -> 200 + application/json
 *                                   {"challengeResponse": sha256hex(code + token + endpoint)}
 *                                   The three parts MUST be hashed in that exact order.
 *   POST <notification payload>  -> 200 / 201 / 202 / 204, acknowledged immediately.
 *
 * ENDPOINT_URL must be byte-identical to the URL registered in the eBay developer
 * portal, otherwise the hash differs and eBay rejects the subscription.
 *
 * Run locally:  deno run --allow-net --allow-env --env-file=.env.local main.ts
 */

const VERIFICATION_TOKEN = Deno.env.get("EBAY_VERIFICATION_TOKEN") ?? "";
const ENDPOINT_URL = Deno.env.get("EBAY_ENDPOINT_URL") ?? "";
// Deno Deploy ignores this and supplies its own port; locally 8000 is often
// already taken (Docker Desktop binds it on this machine).
const PORT = Number(Deno.env.get("PORT") ?? "8000");

async function sha256Hex(...parts: string[]): Promise<string> {
  const bytes = new TextEncoder().encode(parts.join(""));
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

/**
 * Erase every trace of an eBay user from this machine's storage.
 *
 * NOT IMPLEMENTED. eBay's requirement is not "return 204" — it is to delete the
 * user's personal data so that not even the highest system privilege can restore
 * it. Until the machine's order/buyer storage is wired in here, this endpoint
 * satisfies eBay's mechanical check and NOT the legal obligation behind it.
 */
async function deleteUserData(userId: string, username: string, eiasToken: string) {
  console.warn(
    `[ACTION REQUIRED] deletion requested for userId=${userId} ` +
      `username=${username} eiasToken=${eiasToken} — no storage wired in yet`,
  );
}

Deno.serve({ port: PORT }, async (req: Request) => {
  const url = new URL(req.url);

  if (req.method === "GET") {
    const challengeCode = url.searchParams.get("challenge_code");

    // Plain GET without a challenge: health check.
    if (!challengeCode) {
      return new Response("ok", { status: 200 });
    }

    if (!VERIFICATION_TOKEN) {
      console.error("EBAY_VERIFICATION_TOKEN not set");
      return new Response("endpoint not configured", { status: 500 });
    }

    // The hash must use the endpoint URL exactly as registered with eBay.
    // EBAY_ENDPOINT_URL wins when set; otherwise derive it from the request eBay
    // actually made (origin + path, query string stripped). The fallback breaks
    // the chicken-and-egg at first deploy — the public URL is not known until
    // the service exists — and removes a whole class of copy-paste mismatches.
    const effectiveEndpoint = ENDPOINT_URL || `${url.origin}${url.pathname}`;

    const challengeResponse = await sha256Hex(
      challengeCode,
      VERIFICATION_TOKEN,
      effectiveEndpoint,
    );

    console.log(
      `challenge ok · endpoint used for hash: ${effectiveEndpoint} ` +
        `(${ENDPOINT_URL ? "from env" : "derived from request"})`,
    );

    // JSON.stringify, never hand-built string: a BOM makes the body invalid JSON
    // and eBay's subscription attempt fails.
    return new Response(JSON.stringify({ challengeResponse }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  }

  if (req.method === "POST") {
    let payload: any = null;
    try {
      payload = await req.json();
    } catch {
      // Acknowledge anyway: an unparseable body must not cause eBay to retry
      // this notification forever.
    }

    console.log("MARKETPLACE_ACCOUNT_DELETION", JSON.stringify(payload));

    const data = payload?.notification?.data;
    if (data?.userId) {
      await deleteUserData(data.userId, data.username ?? "", data.eiasToken ?? "");
    }

    return new Response(null, { status: 204 });
  }

  return new Response("method not allowed", { status: 405 });
});

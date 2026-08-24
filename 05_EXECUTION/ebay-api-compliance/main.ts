/**
 * eBay Marketplace Account Deletion / Closure notification endpoint.
 *
 * The public webhook acknowledges eBay immediately and stores only the fields
 * required to locate the affected user. The private queue is intentionally
 * separate from destructive local deletion: machine policy requires an Owner GO
 * for each purge. No buyer identifiers are written to application logs.
 */

import {
  createHandler,
  type DeletionRequest,
  type DeletionStore,
  type SignatureVerifier,
} from "./app.ts";
import {
  createEbaySignatureVerifier,
  type EbaySdkSignatureValidator,
} from "./signature.ts";

const VERIFICATION_TOKEN = Deno.env.get("EBAY_VERIFICATION_TOKEN_SECRET") ??
  Deno.env.get("EBAY_VERIFICATION_TOKEN") ?? "";
const ENDPOINT_URL = Deno.env.get("EBAY_ENDPOINT_URL") ?? "";
const PURGE_API_TOKEN = Deno.env.get("EBAY_PURGE_API_TOKEN_SECRET") ??
  Deno.env.get("EBAY_PURGE_API_TOKEN") ?? "";
const REQUIRE_SIGNATURE =
  (Deno.env.get("EBAY_REQUIRE_SIGNATURE") ?? "true").toLowerCase() !== "false";
const PORT = Number(Deno.env.get("PORT") ?? "8000");
const KV_PATH = Deno.env.get("EBAY_KV_PATH") ?? undefined;

class DenoKvDeletionStore implements DeletionStore {
  constructor(private readonly kv: Deno.Kv) {}

  async enqueue(request: DeletionRequest): Promise<"created" | "duplicate"> {
    const key: Deno.KvKey = ["ebay-deletion", request.notificationId];
    const current = await this.kv.get<DeletionRequest>(key);
    if (current.value) return "duplicate";
    const committed = await this.kv.atomic()
      .check({ key, versionstamp: null })
      .set(key, request)
      .commit();
    return committed.ok ? "created" : "duplicate";
  }

  async list(limit: number): Promise<DeletionRequest[]> {
    const requests: DeletionRequest[] = [];
    for await (
      const entry of this.kv.list<DeletionRequest>({
        prefix: ["ebay-deletion"],
      }, { limit })
    ) {
      requests.push(entry.value);
    }
    return requests.sort((left, right) =>
      left.receivedAt.localeCompare(right.receivedAt)
    );
  }

  async complete(notificationId: string): Promise<boolean> {
    const key: Deno.KvKey = ["ebay-deletion", notificationId];
    const current = await this.kv.get<DeletionRequest>(key);
    if (!current.value) return false;
    const result = await this.kv.atomic()
      .check(current)
      .delete(key)
      .set(["ebay-deletion-audit", notificationId], {
        notificationId,
        completedAt: new Date().toISOString(),
      })
      .commit();
    return result.ok;
  }
}

async function buildSignatureVerifier(): Promise<
  SignatureVerifier | undefined
> {
  const clientId = Deno.env.get("EBAY_CLIENT_ID") ?? "";
  const clientSecret = Deno.env.get("EBAY_CLIENT_SECRET") ?? "";
  if (!clientId || !clientSecret) return undefined;

  const imported = await import("event-notification-validator");
  const sdk = (imported.default ?? imported) as {
    validateSignature: EbaySdkSignatureValidator;
  };
  return createEbaySignatureVerifier(
    clientId,
    clientSecret,
    sdk.validateSignature,
  );
}

if (!VERIFICATION_TOKEN || !PURGE_API_TOKEN) {
  throw new Error(
    "EBAY_VERIFICATION_TOKEN and EBAY_PURGE_API_TOKEN must be configured",
  );
}

const kv = await Deno.openKv(KV_PATH);
const signatureVerifier = await buildSignatureVerifier();
if (REQUIRE_SIGNATURE && !signatureVerifier) {
  throw new Error(
    "Signature verification is required but Production credentials are missing",
  );
}

const handler = createHandler({
  verificationToken: VERIFICATION_TOKEN,
  endpointUrl: ENDPOINT_URL,
  purgeApiToken: PURGE_API_TOKEN,
  requireSignature: REQUIRE_SIGNATURE,
  signatureVerifier,
}, new DenoKvDeletionStore(kv));

Deno.serve({ port: PORT }, handler);

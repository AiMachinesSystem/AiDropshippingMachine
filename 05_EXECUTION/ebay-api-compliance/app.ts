export type DeletionRequest = {
  notificationId: string;
  receivedAt: string;
  eventDate: string;
  publishDate: string;
  publishAttemptCount: number;
  signatureVerified: boolean;
  data: {
    username: string;
    userId: string;
    eiasToken: string;
  };
};

export interface DeletionStore {
  enqueue(request: DeletionRequest): Promise<"created" | "duplicate">;
  list(limit: number): Promise<DeletionRequest[]>;
  complete(notificationId: string): Promise<boolean>;
}

export type SignatureVerifier = (
  payload: unknown,
  signature: string,
) => Promise<boolean>;

export type HandlerConfig = {
  verificationToken: string;
  endpointUrl: string;
  purgeApiToken: string;
  requireSignature: boolean;
  signatureVerifier?: SignatureVerifier;
  now?: () => Date;
};

const MAX_BODY_BYTES = 64 * 1024;
const MAX_IDENTIFIER_LENGTH = 2048;

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function noContent(status = 204): Response {
  return new Response(null, {
    status,
    headers: { "cache-control": "no-store" },
  });
}

async function sha256Hex(value: string): Promise<string> {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(value),
  );
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function safeString(value: unknown): string {
  return typeof value === "string" && value.length <= MAX_IDENTIFIER_LENGTH
    ? value
    : "";
}

function isAuthorized(req: Request, expectedToken: string): boolean {
  if (!expectedToken) return false;
  const presented = req.headers.get("authorization") ?? "";
  const prefix = "Bearer ";
  if (!presented.startsWith(prefix)) return false;
  const candidate = presented.slice(prefix.length);
  const expectedBytes = new TextEncoder().encode(expectedToken);
  const candidateBytes = new TextEncoder().encode(candidate);
  const length = Math.max(expectedBytes.length, candidateBytes.length);
  let difference = expectedBytes.length ^ candidateBytes.length;
  for (let index = 0; index < length; index += 1) {
    difference |= (expectedBytes[index] ?? 0) ^ (candidateBytes[index] ?? 0);
  }
  return difference === 0;
}

function parseDeletionRequest(
  payload: unknown,
  receivedAt: string,
  signatureVerified: boolean,
): DeletionRequest | null {
  if (!payload || typeof payload !== "object") return null;
  const record = payload as Record<string, unknown>;
  const metadata = record.metadata as Record<string, unknown> | undefined;
  const notification = record.notification as
    | Record<string, unknown>
    | undefined;
  const data = notification?.data as Record<string, unknown> | undefined;
  if (
    metadata?.topic !== "MARKETPLACE_ACCOUNT_DELETION" ||
    !notification ||
    !data
  ) return null;

  const notificationId = safeString(notification.notificationId);
  const userId = safeString(data.userId);
  if (!notificationId || !userId) return null;

  return {
    notificationId,
    receivedAt,
    eventDate: safeString(notification.eventDate),
    publishDate: safeString(notification.publishDate),
    publishAttemptCount: Number.isSafeInteger(notification.publishAttemptCount)
      ? Number(notification.publishAttemptCount)
      : 0,
    signatureVerified,
    data: {
      username: safeString(data.username),
      userId,
      eiasToken: safeString(data.eiasToken),
    },
  };
}

export function createHandler(
  config: HandlerConfig,
  store: DeletionStore,
): (req: Request) => Promise<Response> {
  const now = config.now ?? (() => new Date());

  return async (req: Request): Promise<Response> => {
    const url = new URL(req.url);

    if (req.method === "GET" && url.pathname === "/health") {
      return json({ ok: true });
    }

    if (req.method === "GET" && url.pathname === "/") {
      const challengeCode = url.searchParams.get("challenge_code");
      if (!challengeCode) return json({ ok: true });
      if (!config.verificationToken) {
        return json({ error: "endpoint not configured" }, 503);
      }
      const effectiveEndpoint = config.endpointUrl ||
        `${url.origin}${url.pathname}`;
      const challengeResponse = await sha256Hex(
        challengeCode + config.verificationToken + effectiveEndpoint,
      );
      return json({ challengeResponse });
    }

    if (req.method === "GET" && url.pathname === "/internal/deletions") {
      if (!isAuthorized(req, config.purgeApiToken)) {
        return json({ error: "unauthorized" }, 401);
      }
      const requestedLimit = Number(url.searchParams.get("limit") ?? "100");
      const limit = Number.isSafeInteger(requestedLimit)
        ? Math.min(Math.max(requestedLimit, 1), 500)
        : 100;
      return json({ requests: await store.list(limit) });
    }

    const completion = url.pathname.match(
      /^\/internal\/deletions\/([^/]+)\/complete$/,
    );
    if (req.method === "POST" && completion) {
      if (!isAuthorized(req, config.purgeApiToken)) {
        return json({ error: "unauthorized" }, 401);
      }
      const notificationId = decodeURIComponent(completion[1]);
      return (await store.complete(notificationId))
        ? noContent()
        : json({ error: "not found" }, 404);
    }

    if (req.method === "POST" && url.pathname === "/") {
      const declaredLength = Number(req.headers.get("content-length") ?? "0");
      if (declaredLength > MAX_BODY_BYTES) {
        return json({ error: "payload too large" }, 413);
      }

      const rawBody = await req.text();
      if (new TextEncoder().encode(rawBody).byteLength > MAX_BODY_BYTES) {
        return json({ error: "payload too large" }, 413);
      }

      let payload: unknown;
      try {
        payload = JSON.parse(rawBody);
      } catch {
        return json({ error: "invalid JSON" }, 400);
      }

      const signature = req.headers.get("x-ebay-signature") ?? "";
      let signatureVerified = false;
      if (config.signatureVerifier && signature) {
        try {
          signatureVerified = await config.signatureVerifier(
            payload,
            signature,
          );
        } catch {
          return json({ error: "signature verification unavailable" }, 503);
        }
      }
      if (config.requireSignature && !signatureVerified) {
        return json({ error: "signature verification failed" }, 412);
      }

      const request = parseDeletionRequest(
        payload,
        now().toISOString(),
        signatureVerified,
      );
      if (!request) return json({ error: "invalid notification" }, 400);

      const result = await store.enqueue(request);
      console.log(
        `MARKETPLACE_ACCOUNT_DELETION ${request.notificationId} ${result}`,
      );
      return noContent();
    }

    return json({ error: "not found" }, 404);
  };
}

export class MemoryDeletionStore implements DeletionStore {
  #requests = new Map<string, DeletionRequest>();

  enqueue(request: DeletionRequest): Promise<"created" | "duplicate"> {
    if (this.#requests.has(request.notificationId)) {
      return Promise.resolve("duplicate");
    }
    this.#requests.set(request.notificationId, structuredClone(request));
    return Promise.resolve("created");
  }

  list(limit: number): Promise<DeletionRequest[]> {
    return Promise.resolve(
      Array.from(this.#requests.values())
        .sort((left, right) => left.receivedAt.localeCompare(right.receivedAt))
        .slice(0, limit)
        .map((request) => structuredClone(request)),
    );
  }

  complete(notificationId: string): Promise<boolean> {
    return Promise.resolve(this.#requests.delete(notificationId));
  }
}

import {
  createHandler,
  MemoryDeletionStore,
  type SignatureVerifier,
} from "./app.ts";
import { assertEquals } from "@std/assert";

const notification = {
  metadata: {
    topic: "MARKETPLACE_ACCOUNT_DELETION",
    schemaVersion: "1.0",
    deprecated: false,
  },
  notification: {
    notificationId: "notification-1",
    eventDate: "2026-08-15T10:00:00.000Z",
    publishDate: "2026-08-15T10:00:01.000Z",
    publishAttemptCount: 1,
    data: {
      username: "buyer-1",
      userId: "user-1",
      eiasToken: "eias-1",
    },
  },
};

function testHandler(options: {
  requireSignature?: boolean;
  signatureVerifier?: SignatureVerifier;
} = {}) {
  const store = new MemoryDeletionStore();
  const handler = createHandler({
    verificationToken: "verification-token-1234567890123456",
    endpointUrl: "https://example.deno.net/",
    purgeApiToken: "purge-token",
    requireSignature: options.requireSignature ?? false,
    signatureVerifier: options.signatureVerifier,
    now: () => new Date("2026-08-15T10:00:02.000Z"),
  }, store);
  return { handler, store };
}

Deno.test("returns the exact eBay challenge hash", async () => {
  const { handler } = testHandler();
  const response = await handler(
    new Request("https://example.deno.net/?challenge_code=abc123"),
  );
  assertEquals(response.status, 200);
  assertEquals(await response.json(), {
    challengeResponse:
      "6d2f649ebebd7fd93c89eb931e028bd2940c0f05427350ac885d75774422032d",
  });
});

Deno.test("queues a structurally valid bootstrap notification idempotently", async () => {
  const { handler, store } = testHandler();
  const request = () =>
    new Request("https://example.deno.net/", {
      method: "POST",
      body: JSON.stringify(notification),
      headers: { "content-type": "application/json" },
    });
  assertEquals((await handler(request())).status, 204);
  assertEquals((await handler(request())).status, 204);
  const queued = await store.list(10);
  assertEquals(queued.length, 1);
  assertEquals(queued[0].notificationId, "notification-1");
  assertEquals(queued[0].signatureVerified, false);
});

Deno.test("requires a valid signature after bootstrap", async () => {
  const invalid = testHandler({
    requireSignature: true,
    signatureVerifier: () => Promise.resolve(false),
  });
  const invalidResponse = await invalid.handler(
    new Request("https://example.deno.net/", {
      method: "POST",
      body: JSON.stringify(notification),
      headers: { "x-ebay-signature": "invalid" },
    }),
  );
  assertEquals(invalidResponse.status, 412);

  const valid = testHandler({
    requireSignature: true,
    signatureVerifier: () => Promise.resolve(true),
  });
  const validResponse = await valid.handler(
    new Request("https://example.deno.net/", {
      method: "POST",
      body: JSON.stringify(notification),
      headers: { "x-ebay-signature": "valid" },
    }),
  );
  assertEquals(validResponse.status, 204);
  assertEquals((await valid.store.list(10))[0].signatureVerified, true);
});

Deno.test("protects queue reads and removes completed PII", async () => {
  const { handler, store } = testHandler();
  await store.enqueue({
    notificationId: "notification-1",
    receivedAt: "2026-08-15T10:00:02.000Z",
    eventDate: "",
    publishDate: "",
    publishAttemptCount: 1,
    signatureVerified: true,
    data: { username: "buyer-1", userId: "user-1", eiasToken: "eias-1" },
  });

  assertEquals(
    (await handler(new Request("https://example.deno.net/internal/deletions")))
      .status,
    401,
  );
  const authorized = new Request(
    "https://example.deno.net/internal/deletions",
    {
      headers: { authorization: "Bearer purge-token" },
    },
  );
  const listed = await handler(authorized);
  assertEquals(listed.status, 200);
  assertEquals((await listed.json()).requests.length, 1);

  const completed = await handler(
    new Request(
      "https://example.deno.net/internal/deletions/notification-1/complete",
      {
        method: "POST",
        headers: { authorization: "Bearer purge-token" },
      },
    ),
  );
  assertEquals(completed.status, 204);
  assertEquals((await store.list(10)).length, 0);
});

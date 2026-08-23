import { assertEquals, assertInstanceOf, assertRejects } from "@std/assert";
import {
  EbayApiClient,
  type EbayApiClientOptions,
  EbayApiError,
  type TokenProvider,
} from "./api_client.ts";

function tokenProvider(initial = "tok-0"): TokenProvider {
  let current = initial;
  return {
    get: () => Promise.resolve(current),
    refresh: () => {
      current = "tok-refreshed";
      return Promise.resolve(current);
    },
  };
}

function ok(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status });
}

function makeClient(
  fetcher: typeof fetch,
  overrides: Partial<EbayApiClientOptions> = {},
): EbayApiClient {
  return new EbayApiClient({
    baseUrl: "https://api.ebay.com",
    marketplaceId: "EBAY_US",
    locale: "en-US",
    tokenProvider: tokenProvider(),
    fetcher,
    delay: async () => {},
    ...overrides,
  } as EbayApiClientOptions);
}

Deno.test("401 refreshes once and retries", async () => {
  let calls = 0;
  const fetcher = (() => {
    calls++;
    if (calls === 1) return Promise.resolve(new Response("", { status: 401 }));
    return Promise.resolve(ok({ ok: true }));
  }) as unknown as typeof fetch;
  const client = makeClient(fetcher);
  const res = await client.request<{ ok: boolean }>({
    method: "GET",
    path: "/x",
    write: false,
  });
  assertEquals(res.ok, true);
  assertEquals(calls, 2);
});

Deno.test("409 never retries", async () => {
  let calls = 0;
  const fetcher = (() => {
    calls++;
    return Promise.resolve(new Response("", { status: 409 }));
  }) as unknown as typeof fetch;
  const client = makeClient(fetcher);
  await assertRejects(
    () => client.request({ method: "GET", path: "/x", write: false }),
    EbayApiError,
  );
  assertEquals(calls, 1);
});

Deno.test("5xx retries at most three times", async () => {
  let calls = 0;
  const fetcher = (() => {
    calls++;
    return Promise.resolve(new Response("", { status: 500 }));
  }) as unknown as typeof fetch;
  const client = makeClient(fetcher, { max5xxRetries: 3 });
  await assertRejects(
    () => client.request({ method: "GET", path: "/x", write: false }),
    EbayApiError,
  );
  assertEquals(calls, 4);
});

Deno.test("429 honors bounded retry then throws", async () => {
  let calls = 0;
  const fetcher = (() => {
    calls++;
    return Promise.resolve(
      new Response("", { status: 429, headers: { "retry-after": "0" } }),
    );
  }) as unknown as typeof fetch;
  const client = makeClient(fetcher, { max429Retries: 2 });
  await assertRejects(
    () => client.request({ method: "GET", path: "/x", write: false }),
    EbayApiError,
  );
  assertEquals(calls, 3);
});

Deno.test("publish is never auto-retried on 5xx", async () => {
  let calls = 0;
  const fetcher = (() => {
    calls++;
    return Promise.resolve(new Response("", { status: 500 }));
  }) as unknown as typeof fetch;
  const client = makeClient(fetcher);
  await assertRejects(
    () =>
      client.request({
        method: "POST",
        path: "/sell/inventory/v1/offer/1/publish",
        write: true,
      }),
    EbayApiError,
  );
  assertEquals(calls, 1);
});

Deno.test("EbayApiError exposes status, ids, domains and categories", async () => {
  const fetcher = (() =>
    Promise.resolve(
      new Response(
        JSON.stringify({
          errors: [{
            errorId: 25001,
            domain: "API_INVENTORY",
            category: "APPLICATION",
            message: "conflict",
            longMessage: "SKU already exists",
          }],
        }),
        { status: 409 },
      ),
    )) as unknown as typeof fetch;
  const client = makeClient(fetcher);
  let caught: unknown;
  try {
    await client.request({ method: "GET", path: "/x", write: false });
  } catch (e) {
    caught = e;
  }
  assertInstanceOf(caught, EbayApiError);
  const err = caught as EbayApiError;
  assertEquals(err.status, 409);
  assertEquals(err.errorIds, [25001]);
  assertEquals(err.domains, ["API_INVENTORY"]);
  assertEquals(err.categories, ["APPLICATION"]);
  assertEquals(err.message, "SKU already exists");
});

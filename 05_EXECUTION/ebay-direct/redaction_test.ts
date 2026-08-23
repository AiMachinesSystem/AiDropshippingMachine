import { assertEquals } from "@std/assert";
import { redact, safeError } from "./redaction.ts";

Deno.test("redact removes nested credentials", () => {
  const value = {
    headers: { authorization: "Bearer access-value" },
    refresh: "refresh-value",
  };
  const out = JSON.stringify(redact(value, ["access-value", "refresh-value"]));
  assertEquals(out.includes("value"), false);
  assertEquals(out.includes("access"), false);
});

Deno.test("redact scrubs a bearer token even when the key is not secret-shaped", () => {
  const out = redact({ text: "send Bearer abc123 now" }, []) as {
    text: string;
  };
  assertEquals(out.text, "send Bearer [REDACTED] now");
});

Deno.test("redact preserves array order and non-secret scalars", () => {
  const out = redact(
    { tags: ["b", "a", "c"], count: 3, price: "12.99" },
    [],
  ) as { tags: string[]; count: number; price: string };
  assertEquals(out.tags, ["b", "a", "c"]);
  assertEquals(out.count, 3);
  assertEquals(out.price, "12.99");
});

Deno.test("safeError redacts a secret inside an Error message", () => {
  const err = new Error("token refresh-value was rejected");
  const safe = safeError(err, ["refresh-value"]);
  assertEquals(safe.message.includes("refresh-value"), false);
  assertEquals(safe.name, "Error");
});

Deno.test("safeError preserves eBay status and error ids without secrets", () => {
  const safe = safeError(
    { message: "bad client-secret-value", status: 409, errorIds: [25001] },
    ["client-secret-value"],
  );
  assertEquals(safe.status, 409);
  assertEquals(safe.errorIds, [25001]);
  assertEquals(safe.message.includes("client-secret-value"), false);
});

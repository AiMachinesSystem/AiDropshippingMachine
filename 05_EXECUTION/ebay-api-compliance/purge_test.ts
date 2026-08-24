import { assertEquals, assertStringIncludes } from "@std/assert";
import { join } from "@std/path";
import { purgeTree, sanitizeFileContent } from "./purge.ts";

const identifiers = {
  username: "buyer-alpha",
  userId: "user-alpha",
  eiasToken: "eias-alpha",
};

Deno.test("removes the matching order while retaining unrelated JSON data", () => {
  const input = JSON.stringify({
    results: [
      { id: 1, buyer_username: "buyer-alpha", first_name: "Private" },
      { id: 2, buyer_username: "buyer-beta", first_name: "Keep" },
    ],
  });
  const result = sanitizeFileContent(input, ".json", identifiers);
  const parsed = JSON.parse(result.content);
  assertEquals(parsed.results, [
    { id: 2, buyer_username: "buyer-beta", first_name: "Keep" },
  ]);
  assertEquals(result.removedRecords, 1);
});

Deno.test("purges a buyer from a JSON body embedded in JSONL", () => {
  const body = JSON.stringify({
    results: [
      { id: 1, buyer_username: "buyer-alpha", address_1: "Private" },
      { id: 2, buyer_username: "buyer-beta", address_1: "Keep" },
    ],
  });
  const input = JSON.stringify({ method: "GET", url: "/orders/list", body }) +
    "\n";
  const result = sanitizeFileContent(input, ".jsonl", identifiers);
  const outer = JSON.parse(result.content.trim());
  const parsedBody = JSON.parse(outer.body);
  assertEquals(parsedBody.results.length, 1);
  assertEquals(parsedBody.results[0].id, 2);
  assertEquals(result.removedRecords, 1);
});

Deno.test("preview is read-only and execute removes all matching content", async () => {
  const root = await Deno.makeTempDir({ prefix: "ebay-purge-test-" });
  try {
    const jsonPath = join(root, "orders.json");
    const textPath = join(root, "notes.txt");
    await Deno.writeTextFile(
      jsonPath,
      JSON.stringify({ orders: [{ buyer_username: "buyer-alpha" }] }),
    );
    await Deno.writeTextFile(
      textPath,
      "retain this line\nprivate buyer-alpha line\n",
    );

    const preview = await purgeTree({ root, identifiers, execute: false });
    assertEquals(preview.filesChanged, 2);
    assertStringIncludes(await Deno.readTextFile(jsonPath), "buyer-alpha");
    assertStringIncludes(await Deno.readTextFile(textPath), "buyer-alpha");

    const executed = await purgeTree({ root, identifiers, execute: true });
    assertEquals(executed.filesChanged, 2);
    assertEquals(
      (await purgeTree({ root, identifiers, execute: false })).filesChanged,
      0,
    );
    assertEquals(
      (await Deno.readTextFile(jsonPath)).includes("buyer-alpha"),
      false,
    );
    assertEquals(
      (await Deno.readTextFile(textPath)).includes("buyer-alpha"),
      false,
    );
  } finally {
    await Deno.remove(root, { recursive: true });
  }
});

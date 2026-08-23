import { assertEquals, assertThrows } from "@std/assert";
import { parseArgs } from "./cli.ts";

Deno.test("parseArgs accepts a read command with no options", () => {
  const inv = parseArgs(["bootstrap"]);
  assertEquals(inv.command, "bootstrap");
  assertEquals(inv.options, {});
});

Deno.test("parseArgs collects key/value options", () => {
  const inv = parseArgs([
    "validate",
    "--manifest",
    "m.json",
    "--bootstrap",
    "b.json",
  ]);
  assertEquals(inv.command, "validate");
  assertEquals(inv.options, {
    manifest: "m.json",
    bootstrap: "b.json",
  });
});

Deno.test("parseArgs rejects a missing command", () => {
  assertThrows(() => parseArgs([]), Error, "missing command");
});

Deno.test("parseArgs rejects an unknown command", () => {
  assertThrows(() => parseArgs(["ship-it"]), Error, "unknown command");
});

Deno.test("parseArgs rejects a positional argument", () => {
  assertThrows(
    () => parseArgs(["validate", "m.json"]),
    Error,
    "positional",
  );
});

Deno.test("parseArgs rejects a flag without a value", () => {
  assertThrows(
    () => parseArgs(["validate", "--manifest"]),
    Error,
    "requires a value",
  );
});

Deno.test("parseArgs rejects every secret-bearing flag", () => {
  for (const flag of ["--token", "--secret", "--code", "--owner-go"]) {
    assertThrows(
      () => parseArgs(["oauth-start", flag, "x"]),
      Error,
      "secret-bearing",
    );
  }
});

Deno.test("parseArgs requires the pack gate on write commands", () => {
  for (
    const command of [
      "apply-inventory",
      "create-offer",
      "publish-offer",
      "verify",
      "withdraw",
    ]
  ) {
    assertThrows(
      () => parseArgs([command]),
      Error,
      "--action-pack",
    );
    assertThrows(
      () => parseArgs([command, "--action-pack", "pack.json"]),
      Error,
      "--expected-sha256",
    );
  }
});

Deno.test("parseArgs accepts a write command with the full pack gate", () => {
  const inv = parseArgs([
    "publish-offer",
    "--action-pack",
    "pack.json",
    "--expected-sha256",
    "a".repeat(64),
    "--offer-id",
    "OFF-1",
  ]);
  assertEquals(inv.command, "publish-offer");
  assertEquals(inv.options["action-pack"], "pack.json");
  assertEquals(inv.options["expected-sha256"], "a".repeat(64));
});

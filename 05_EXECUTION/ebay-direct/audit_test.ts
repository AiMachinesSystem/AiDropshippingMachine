import { assertEquals, assertThrows } from "@std/assert";
import type { AuditRecord } from "./types.ts";
import { auditLine, validateAuditRecord } from "./audit.ts";

function record(overrides: Record<string, unknown> = {}): AuditRecord {
  return {
    timestamp: "2026-08-15T12:00:00Z",
    stage: "apply-inventory",
    sku: "SKU-TEST-001",
    actionPackSha256: "p".repeat(64),
    httpStatus: 200,
    ebayErrorIds: [],
    ...overrides,
  } as AuditRecord;
}

Deno.test("validateAuditRecord accepts a clean record", () => {
  validateAuditRecord(record());
});

Deno.test("validateAuditRecord rejects a token key", () => {
  assertThrows(
    () => validateAuditRecord(record({ accessToken: "x" })),
    Error,
    "forbidden",
  );
});

Deno.test("validateAuditRecord rejects a username key", () => {
  assertThrows(
    () => validateAuditRecord(record({ username: "x" })),
    Error,
    "username",
  );
});

Deno.test("validateAuditRecord rejects an email key", () => {
  assertThrows(
    () => validateAuditRecord(record({ buyerEmail: "x" })),
    Error,
    "forbidden",
  );
});

Deno.test("auditLine serializes a single JSON object", () => {
  const line = auditLine(record());
  assertEquals(JSON.parse(line)["sku"], "SKU-TEST-001");
  assertEquals(line.includes("\n"), false);
});

Deno.test("auditLine rejects secret-shaped keys before writing", () => {
  assertThrows(
    () => auditLine(record({ authorization: "Bearer x" })),
    Error,
    "authorization",
  );
});

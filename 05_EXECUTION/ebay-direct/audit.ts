import type { AuditRecord } from "./types.ts";

const FORBIDDEN_KEY =
  /token|secret|authorization|buyer|username|email|address/i;

/**
 * Rejects audit records carrying secret- or PII-shaped keys before they are ever
 * written. Enforced at the field-name level so a broader object cannot leak.
 */
export function validateAuditRecord(record: object): void {
  for (const key of Object.keys(record)) {
    if (FORBIDDEN_KEY.test(key)) {
      throw new Error(`audit record contains forbidden key: ${key}`);
    }
  }
}

/** Serializes a validated audit record to a single JSONL line. */
export function auditLine(record: AuditRecord): string {
  validateAuditRecord(record);
  return JSON.stringify(record);
}

/** Appends one redacted record to an append-only JSONL file. */
export async function appendAudit(
  record: AuditRecord,
  filePath: string,
): Promise<void> {
  const line = auditLine(record);
  await Deno.writeTextFile(filePath, line + "\n", { append: true });
}

import type { SafeError } from "./types.ts";

const SECRET_KEY_PATTERN =
  /token|secret|authorization|code|client_secret|client_id|refresh/i;

/**
 * Recursively scrubs known secret strings and secret-shaped keys. Used before
 * any value reaches a log, report, audit record or error message.
 */
export function redact(value: unknown, secrets: readonly string[]): unknown {
  const scrub = (text: string): string => {
    let out = text;
    for (const secret of secrets.filter((s) => s.length > 0)) {
      out = out.split(secret).join("[REDACTED]");
    }
    return out.replace(/Bearer\s+[^\s"']+/gi, "Bearer [REDACTED]");
  };

  if (typeof value === "string") return scrub(value);
  if (Array.isArray(value)) return value.map((item) => redact(item, secrets));
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>).map(([key, item]) => [
        key,
        SECRET_KEY_PATTERN.test(key) ? "[REDACTED]" : redact(item, secrets),
      ]),
    );
  }
  return value;
}

/**
 * Renders an error without leaking secrets, preserving only status and eBay
 * error metadata needed to diagnose a failed API call.
 */
export function safeError(
  error: unknown,
  secrets: readonly string[],
): SafeError {
  if (error instanceof Error) {
    const record = error as Error & Record<string, unknown>;
    return {
      name: error.name,
      message: redact(error.message, secrets) as string,
      status: typeof record.status === "number" ? record.status : undefined,
      errorIds: Array.isArray(record.errorIds)
        ? (record.errorIds as number[])
        : undefined,
      domains: Array.isArray(record.domains)
        ? (record.domains as string[])
        : undefined,
      categories: Array.isArray(record.categories)
        ? (record.categories as string[])
        : undefined,
      cause: error.cause ? safeError(error.cause, secrets) : null,
    };
  }
  if (error && typeof error === "object") {
    const record = error as Record<string, unknown>;
    const rawMessage = String(
      record.message ?? record.error ?? "Unknown error",
    );
    return {
      name: "Error",
      message: redact(rawMessage, secrets) as string,
      status: typeof record.status === "number" ? record.status : undefined,
      errorIds: Array.isArray(record.errorIds)
        ? (record.errorIds as number[])
        : undefined,
      domains: Array.isArray(record.domains)
        ? (record.domains as string[])
        : undefined,
      categories: Array.isArray(record.categories)
        ? (record.categories as string[])
        : undefined,
      cause: null,
    };
  }
  return {
    name: "Error",
    message: redact(String(error), secrets) as string,
    cause: null,
  };
}

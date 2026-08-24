import { dirname, fromFileUrl, resolve } from "@std/path";
import { type PurgeIdentifiers, purgeTree } from "./purge.ts";

type QueueRequest = {
  notificationId: string;
  data: PurgeIdentifiers;
};

function argument(name: string): string {
  const index = Deno.args.indexOf(name);
  return index >= 0 ? Deno.args[index + 1] ?? "" : "";
}

function hasArgument(name: string): boolean {
  return Deno.args.includes(name);
}

function queueBaseUrl(): string {
  const value = Deno.env.get("EBAY_QUEUE_URL") ?? "";
  if (!value.startsWith("https://")) {
    throw new Error("EBAY_QUEUE_URL must be an HTTPS URL");
  }
  return value.replace(/\/$/, "");
}

function queueHeaders(): Headers {
  const token = Deno.env.get("EBAY_PURGE_API_TOKEN_SECRET") ??
    Deno.env.get("EBAY_PURGE_API_TOKEN") ?? "";
  if (!token) throw new Error("EBAY_PURGE_API_TOKEN is required");
  return new Headers({ authorization: `Bearer ${token}` });
}

async function fetchJob(notificationId: string): Promise<QueueRequest> {
  const response = await fetch(
    `${queueBaseUrl()}/internal/deletions?limit=500`,
    {
      headers: queueHeaders(),
    },
  );
  if (!response.ok) {
    throw new Error(`Queue read failed with HTTP ${response.status}`);
  }
  const payload = await response.json() as { requests?: QueueRequest[] };
  const request = payload.requests?.find((entry) =>
    entry.notificationId === notificationId
  );
  if (!request) {
    throw new Error(`Notification ${notificationId} is not pending`);
  }
  return request;
}

async function acknowledge(notificationId: string): Promise<void> {
  const encoded = encodeURIComponent(notificationId);
  const response = await fetch(
    `${queueBaseUrl()}/internal/deletions/${encoded}/complete`,
    { method: "POST", headers: queueHeaders() },
  );
  if (!response.ok) {
    throw new Error(`Queue completion failed with HTTP ${response.status}`);
  }
}

const notificationId = argument("--notification-id");
if (!notificationId) throw new Error("--notification-id is required");

const execute = hasArgument("--execute");
const acknowledgeQueue = hasArgument("--ack");
const ownerGo = argument("--owner-go");
if (execute && ownerGo !== notificationId) {
  throw new Error(
    "Execution requires --owner-go with the exact notification ID from the Owner GO",
  );
}
if (acknowledgeQueue && !execute) {
  throw new Error("--ack requires --execute");
}

const packageDirectory = dirname(fromFileUrl(import.meta.url));
const defaultRoot = resolve(packageDirectory, "..", "..");
const root = argument("--root") || defaultRoot;
const job = await fetchJob(notificationId);
const result = await purgeTree({ root, identifiers: job.data, execute });

if (execute) {
  const verification = await purgeTree({
    root,
    identifiers: job.data,
    execute: false,
  });
  if (verification.filesChanged !== 0) {
    throw new Error(
      `Purge verification failed: ${verification.filesChanged} files still match`,
    );
  }
  if (acknowledgeQueue) await acknowledge(notificationId);
}

console.log(JSON.stringify(
  {
    notificationId,
    executed: execute,
    acknowledged: execute && acknowledgeQueue,
    filesScanned: result.filesScanned,
    filesChanged: result.filesChanged,
    removedRecords: result.removedRecords,
    redactedStrings: result.redactedStrings,
    changes: result.changes.map((change) => ({
      path: change.path,
      removedRecords: change.removedRecords,
      redactedStrings: change.redactedStrings,
      bytesBefore: change.bytesBefore,
      bytesAfter: change.bytesAfter,
    })),
  },
  null,
  2,
));

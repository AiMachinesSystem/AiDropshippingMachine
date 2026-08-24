import { extname, relative, resolve } from "@std/path";

export type PurgeIdentifiers = {
  username: string;
  userId: string;
  eiasToken: string;
};

export type PurgeFileResult = {
  path: string;
  removedRecords: number;
  redactedStrings: number;
  bytesBefore: number;
  bytesAfter: number;
};

export type PurgeResult = {
  root: string;
  execute: boolean;
  filesScanned: number;
  filesChanged: number;
  removedRecords: number;
  redactedStrings: number;
  changes: PurgeFileResult[];
};

const STRUCTURED_EXTENSIONS = new Set([".json", ".jsonl"]);
const LINE_EXTENSIONS = new Set([".csv", ".tsv", ".txt", ".md", ".log"]);
const EXCLUDED_DIRECTORIES = new Set([
  ".git",
  ".venv",
  "node_modules",
  "__pycache__",
]);
const REDACTION = "[DELETED_EBAY_USER]";
const REMOVED = Symbol("removed");

type Sanitized = {
  value: unknown | typeof REMOVED;
  changed: boolean;
  removedRecords: number;
  redactedStrings: number;
};

function identifierValues(identifiers: PurgeIdentifiers): string[] {
  return [identifiers.username, identifiers.userId, identifiers.eiasToken]
    .filter((value) => value.length > 0);
}

function equalsIdentifier(value: string, identifiers: string[]): boolean {
  return identifiers.some((identifier) => value === identifier);
}

function containsIdentifier(value: string, identifiers: string[]): boolean {
  return identifiers.some((identifier) => value.includes(identifier));
}

function redactString(value: string, identifiers: string[]): string {
  let result = value;
  for (const identifier of identifiers) {
    result = result.split(identifier).join(REDACTION);
  }
  return result;
}

function sanitizeValue(value: unknown, identifiers: string[]): Sanitized {
  if (typeof value === "string") {
    if (equalsIdentifier(value, identifiers)) {
      return {
        value: REMOVED,
        changed: true,
        removedRecords: 0,
        redactedStrings: 1,
      };
    }

    const trimmed = value.trim();
    if (
      containsIdentifier(value, identifiers) &&
      ((trimmed.startsWith("{") && trimmed.endsWith("}")) ||
        (trimmed.startsWith("[") && trimmed.endsWith("]")))
    ) {
      try {
        const nested = sanitizeValue(JSON.parse(value), identifiers);
        if (nested.value === REMOVED) {
          return {
            value: REDACTION,
            changed: true,
            removedRecords: nested.removedRecords + 1,
            redactedStrings: nested.redactedStrings,
          };
        }
        return {
          value: JSON.stringify(nested.value),
          changed: nested.changed,
          removedRecords: nested.removedRecords,
          redactedStrings: nested.redactedStrings,
        };
      } catch {
        // Fall through to exact string redaction.
      }
    }

    if (containsIdentifier(value, identifiers)) {
      return {
        value: redactString(value, identifiers),
        changed: true,
        removedRecords: 0,
        redactedStrings: 1,
      };
    }
    return { value, changed: false, removedRecords: 0, redactedStrings: 0 };
  }

  if (Array.isArray(value)) {
    const output: unknown[] = [];
    let changed = false;
    let removedRecords = 0;
    let redactedStrings = 0;
    for (const entry of value) {
      const sanitized = sanitizeValue(entry, identifiers);
      changed ||= sanitized.changed;
      removedRecords += sanitized.removedRecords;
      redactedStrings += sanitized.redactedStrings;
      if (sanitized.value === REMOVED) {
        changed = true;
        removedRecords += 1;
      } else {
        output.push(sanitized.value);
      }
    }
    return { value: output, changed, removedRecords, redactedStrings };
  }

  if (value && typeof value === "object") {
    const record = value as Record<string, unknown>;
    if (
      Object.values(record).some((entry) =>
        typeof entry === "string" && equalsIdentifier(entry, identifiers)
      )
    ) {
      return {
        value: REMOVED,
        changed: true,
        removedRecords: 0,
        redactedStrings: 0,
      };
    }

    const output: Record<string, unknown> = {};
    let changed = false;
    let removedRecords = 0;
    let redactedStrings = 0;
    for (const [key, entry] of Object.entries(record)) {
      const sanitized = sanitizeValue(entry, identifiers);
      changed ||= sanitized.changed;
      removedRecords += sanitized.removedRecords;
      redactedStrings += sanitized.redactedStrings;
      if (sanitized.value === REMOVED) {
        changed = true;
        removedRecords += 1;
      } else {
        output[key] = sanitized.value;
      }
    }
    return { value: output, changed, removedRecords, redactedStrings };
  }

  return { value, changed: false, removedRecords: 0, redactedStrings: 0 };
}

export function sanitizeFileContent(
  content: string,
  extension: string,
  identifiers: PurgeIdentifiers,
): { content: string; removedRecords: number; redactedStrings: number } {
  const values = identifierValues(identifiers);
  if (values.length === 0 || !containsIdentifier(content, values)) {
    return { content, removedRecords: 0, redactedStrings: 0 };
  }

  const normalizedExtension = extension.toLowerCase();
  if (normalizedExtension === ".json") {
    const sanitized = sanitizeValue(JSON.parse(content), values);
    const output = sanitized.value === REMOVED ? null : sanitized.value;
    return {
      content: JSON.stringify(output, null, 2) + "\n",
      removedRecords: sanitized.removedRecords +
        (sanitized.value === REMOVED ? 1 : 0),
      redactedStrings: sanitized.redactedStrings,
    };
  }

  if (normalizedExtension === ".jsonl") {
    const trailingNewline = content.endsWith("\n");
    const output: string[] = [];
    let removedRecords = 0;
    let redactedStrings = 0;
    for (const line of content.split(/\r?\n/)) {
      if (!line) continue;
      if (!containsIdentifier(line, values)) {
        output.push(line);
        continue;
      }
      const sanitized = sanitizeValue(JSON.parse(line), values);
      removedRecords += sanitized.removedRecords;
      redactedStrings += sanitized.redactedStrings;
      if (sanitized.value === REMOVED) {
        removedRecords += 1;
      } else {
        output.push(JSON.stringify(sanitized.value));
      }
    }
    return {
      content: output.join("\n") + (trailingNewline ? "\n" : ""),
      removedRecords,
      redactedStrings,
    };
  }

  const trailingNewline = content.endsWith("\n");
  const lines = content.split(/\r?\n/);
  const retained = lines.filter((line) => !containsIdentifier(line, values));
  const removedRecords = lines.length - retained.length;
  return {
    content: retained.join("\n") + (trailingNewline ? "\n" : ""),
    removedRecords,
    redactedStrings: 0,
  };
}

async function* walkFiles(root: string): AsyncGenerator<string> {
  const entries = [];
  for await (const entry of Deno.readDir(root)) entries.push(entry);
  entries.sort((left, right) => left.name.localeCompare(right.name));
  for (const entry of entries) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory) {
      if (!EXCLUDED_DIRECTORIES.has(entry.name)) yield* walkFiles(path);
    } else if (entry.isFile) {
      yield path;
    }
  }
}

function assertWithinRoot(root: string, path: string): void {
  const pathRelativeToRoot = relative(root, path);
  if (
    pathRelativeToRoot === "" ||
    pathRelativeToRoot.startsWith("..") ||
    resolve(root, pathRelativeToRoot) !== resolve(path)
  ) {
    throw new Error(`Refusing path outside purge root: ${path}`);
  }
}

async function replaceFile(path: string, content: string): Promise<void> {
  const temporary = `${path}.ebay-purge-${crypto.randomUUID()}.tmp`;
  await Deno.writeTextFile(temporary, content, { createNew: true });
  try {
    await Deno.rename(temporary, path);
  } catch (error) {
    await Deno.remove(temporary).catch(() => undefined);
    throw error;
  }
}

export async function purgeTree(options: {
  root: string;
  identifiers: PurgeIdentifiers;
  execute: boolean;
}): Promise<PurgeResult> {
  const root = await Deno.realPath(options.root);
  const identifiers = identifierValues(options.identifiers);
  if (identifiers.length === 0) {
    throw new Error("No deletion identifiers supplied");
  }

  const result: PurgeResult = {
    root,
    execute: options.execute,
    filesScanned: 0,
    filesChanged: 0,
    removedRecords: 0,
    redactedStrings: 0,
    changes: [],
  };

  for await (const path of walkFiles(root)) {
    assertWithinRoot(root, path);
    const extension = extname(path).toLowerCase();
    if (
      !STRUCTURED_EXTENSIONS.has(extension) && !LINE_EXTENSIONS.has(extension)
    ) {
      continue;
    }
    result.filesScanned += 1;
    const content = await Deno.readTextFile(path);
    if (!containsIdentifier(content, identifiers)) continue;
    const sanitized = sanitizeFileContent(
      content,
      extension,
      options.identifiers,
    );
    if (sanitized.content === content) continue;

    const change: PurgeFileResult = {
      path,
      removedRecords: sanitized.removedRecords,
      redactedStrings: sanitized.redactedStrings,
      bytesBefore: new TextEncoder().encode(content).byteLength,
      bytesAfter: new TextEncoder().encode(sanitized.content).byteLength,
    };
    result.filesChanged += 1;
    result.removedRecords += change.removedRecords;
    result.redactedStrings += change.redactedStrings;
    result.changes.push(change);

    if (options.execute) await replaceFile(path, sanitized.content);
  }

  return result;
}

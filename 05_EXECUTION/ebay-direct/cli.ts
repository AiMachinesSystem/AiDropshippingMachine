import type {
  AccountBootstrap,
  ActionPack,
  EbayConfig,
  ListingManifest,
} from "./types.ts";
import { loadConfig } from "./config.ts";
import {
  buildConsentUrl,
  createOAuthState,
  exchangeCode,
  parseRedirect,
  refreshAccessToken,
} from "./oauth.ts";
import { EbayApiClient } from "./api_client.ts";
import { readBootstrap } from "./account.ts";
import { parseManifest, validateManifest } from "./manifest.ts";
import { buildInventoryPayload, buildOfferPayload } from "./payloads.ts";
import { buildActionPack } from "./action_pack.ts";
import {
  applyInventory,
  createOrReuseOffer,
  publishOffer,
  verifyPublished,
  withdrawOffer,
} from "./publisher.ts";

const SECRET_FLAGS = new Set(["--token", "--secret", "--code", "--owner-go"]);
const COMMANDS = new Set([
  "oauth-start",
  "oauth-exchange",
  "bootstrap",
  "validate",
  "dry-run",
  "apply-inventory",
  "create-offer",
  "publish-offer",
  "verify",
  "withdraw",
]);
const WRITE_COMMANDS = new Set([
  "apply-inventory",
  "create-offer",
  "publish-offer",
  "verify",
  "withdraw",
]);

export interface CliInvocation {
  command: string;
  options: Record<string, string>;
}

/**
 * Parses `argv` (everything after the script path). Rejects unknown commands,
 * secret-bearing flags, and write commands missing their pack gate.
 */
export function parseArgs(argv: string[]): CliInvocation {
  if (argv.length === 0) throw new Error("missing command");

  const command = argv[0];
  if (!COMMANDS.has(command)) throw new Error(`unknown command: ${command}`);

  const options: Record<string, string> = {};
  const rest = argv.slice(1);
  for (let i = 0; i < rest.length; i++) {
    const arg = rest[i];
    if (!arg.startsWith("--")) {
      throw new Error(`unexpected positional argument: ${arg}`);
    }
    if (SECRET_FLAGS.has(arg)) {
      throw new Error(`refusing secret-bearing flag: ${arg}`);
    }
    const name = arg.slice(2);
    const value = rest[i + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`flag ${arg} requires a value`);
    }
    options[name] = value;
    i++;
  }

  if (WRITE_COMMANDS.has(command)) {
    for (const required of ["action-pack", "expected-sha256"]) {
      if (!options[required]) {
        throw new Error(`command ${command} requires --${required}`);
      }
    }
  }

  return { command, options };
}

function requireOption(
  options: Record<string, string>,
  name: string,
  command: string,
): string {
  const value = options[name];
  if (!value) throw new Error(`command ${command} requires --${name}`);
  return value;
}

async function readJsonFile<T>(path: string): Promise<T> {
  const text = await Deno.readTextFile(path);
  return JSON.parse(text) as T;
}

/** Loads `.env.local` (KEY=VALUE) over the process environment, never echoing. */
async function loadEnvLocal(): Promise<Record<string, string | undefined>> {
  const env: Record<string, string | undefined> = { ...Deno.env.toObject() };
  try {
    const text = await Deno.readTextFile(".env.local");
    for (const line of text.split("\n")) {
      const match = line.match(/^([A-Z0-9_]+)=(.*)$/);
      if (match) env[match[1]] = match[2];
    }
  } catch {
    // No .env.local yet; config loading will surface the missing secrets.
  }
  return env;
}

function tokenProvider(config: EbayConfig) {
  let accessToken = "";
  const refresh = async () => {
    const grant = await refreshAccessToken(fetch, config);
    accessToken = grant.access_token;
    return accessToken;
  };
  return {
    get: async () => accessToken || (await refresh()),
    refresh,
  };
}

function buildClient(config: EbayConfig): EbayApiClient {
  return new EbayApiClient({
    baseUrl: config.baseUrl,
    marketplaceId: config.marketplaceId,
    locale: config.locale,
    tokenProvider: tokenProvider(config),
  });
}

async function loadPack(path: string): Promise<ActionPack> {
  return await readJsonFile<ActionPack>(path);
}

export async function main(argv: string[]): Promise<void> {
  const { command, options } = parseArgs(argv);

  switch (command) {
    case "oauth-start": {
      const config = loadConfig(await loadEnvLocal(), {
        requireRefreshToken: false,
      });
      const state = createOAuthState();
      const url = buildConsentUrl(config, state);
      await Deno.writeTextFile(
        ".oauth-state.local",
        JSON.stringify({ state, createdAt: new Date().toISOString() }),
      );
      console.log(url.toString());
      return;
    }

    case "oauth-exchange": {
      const config = loadConfig(await loadEnvLocal(), {
        requireRefreshToken: false,
      });
      const stateJson = JSON.parse(
        await Deno.readTextFile(".oauth-state.local"),
      );
      const redirectJson = JSON.parse(
        await Deno.readTextFile(".oauth-redirect.local"),
      );
      const code = parseRedirect(
        new URL(redirectJson.url),
        stateJson.state as string,
      );
      const grant = await exchangeCode(fetch, config, code);
      if (!grant.refresh_token) {
        throw new Error("token grant did not include a refresh token");
      }
      await Deno.writeTextFile(
        ".env.local",
        `EBAY_REFRESH_TOKEN=${grant.refresh_token}\n`,
        { append: true },
      );
      await Deno.remove(".oauth-state.local");
      await Deno.remove(".oauth-redirect.local");
      console.log("refresh token stored (not echoed)");
      return;
    }

    case "bootstrap": {
      const config = loadConfig(await loadEnvLocal());
      const bootstrap = await readBootstrap(buildClient(config));
      console.log(JSON.stringify(bootstrap, null, 2));
      return;
    }

    case "validate":
    case "dry-run": {
      const manifest = await readJsonFile<ListingManifest>(
        requireOption(options, "manifest", command),
      );
      const bootstrap = await readJsonFile<AccountBootstrap>(
        requireOption(options, "bootstrap", command),
      );
      const parsed = parseManifest(manifest);
      const report = validateManifest(parsed, bootstrap);

      if (command === "validate") {
        console.log(JSON.stringify(report, null, 2));
        if (!report.pass) Deno.exit(1);
        return;
      }

      const pack = await buildActionPack(parsed, report, bootstrap);
      await Deno.writeTextFile(
        `action-packs/${pack.sku}.json`,
        JSON.stringify(pack, null, 2),
      );
      console.log(
        JSON.stringify({ sku: pack.sku, packSha256: pack.packSha256 }),
      );
      return;
    }

    case "apply-inventory":
    case "create-offer": {
      const config = loadConfig(await loadEnvLocal());
      const client = buildClient(config);
      const pack = await loadPack(
        requireOption(options, "action-pack", command),
      );
      const expected = requireOption(options, "expected-sha256", command);
      const manifest = await readJsonFile<ListingManifest>(
        requireOption(options, "manifest", command),
      );
      const parsed = parseManifest(manifest);
      const payload = command === "apply-inventory"
        ? buildInventoryPayload(parsed)
        : buildOfferPayload(parsed);
      const outcome = command === "apply-inventory"
        ? await applyInventory(client, pack, expected, payload)
        : await createOrReuseOffer(client, pack, expected, payload);
      console.log(JSON.stringify(outcome));
      return;
    }

    case "publish-offer": {
      const config = loadConfig(await loadEnvLocal());
      const client = buildClient(config);
      const pack = await loadPack(
        requireOption(options, "action-pack", command),
      );
      const expected = requireOption(options, "expected-sha256", command);
      const offerId = requireOption(options, "offer-id", command);
      const outcome = await publishOffer(client, pack, expected, offerId);
      console.log(JSON.stringify(outcome));
      return;
    }

    case "verify": {
      const config = loadConfig(await loadEnvLocal());
      const client = buildClient(config);
      const pack = await loadPack(
        requireOption(options, "action-pack", command),
      );
      const expected = requireOption(options, "expected-sha256", command);
      const offerId = requireOption(options, "offer-id", command);
      const result = await verifyPublished(client, pack, expected, offerId, {
        listingId: requireOption(options, "listing-id", command),
        price: requireOption(options, "price", command),
        quantity: Number(requireOption(options, "quantity", command)),
      });
      console.log(JSON.stringify(result));
      return;
    }

    case "withdraw": {
      const config = loadConfig(await loadEnvLocal());
      const client = buildClient(config);
      const pack = await loadPack(
        requireOption(options, "action-pack", command),
      );
      const expected = requireOption(options, "expected-sha256", command);
      const offerId = requireOption(options, "offer-id", command);
      const outcome = await withdrawOffer(client, pack, expected, offerId);
      console.log(JSON.stringify(outcome));
      return;
    }

    default:
      throw new Error(`unhandled command: ${command}`);
  }
}

if (import.meta.main) {
  try {
    await main(Deno.args);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(message);
    Deno.exit(1);
  }
}

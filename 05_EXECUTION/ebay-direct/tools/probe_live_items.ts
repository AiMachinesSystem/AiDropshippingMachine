/**
 * Read-only helper: enumerates the currently LIVE eBay items of seller
 * divinit-92 via the Browse API (seller filter, keyword fan-out, pagination).
 * Writes the unique item ids + titles to stdout as JSON. No writes to eBay.
 *
 * Usage:
 *   deno run --allow-net=api.ebay.com --allow-read=.env.local --allow-env \
 *     tools/probe_live_items.ts
 */
import { loadConfig } from "../config.ts";

const KEYWORDS = [
  "pool", "feeder", "chlorinator", "pump", "spa", "filter", "float", "solar",
  "pet", "dog", "cat", "bed", "bowl", "leash", "grooming", "toy",
  "kitchen", "pan", "knife", "utensil", "cutting", "storage", "container",
  "organizer", "box", "basket", "bag", "rack", "holder", "hook", "hanger",
  "shelf", "drawer", "closet", "laundry", "bath", "shower", "towel", "mat",
  "candle", "pillow", "blanket", "throw", "cover", "cushion", "frame",
  "poster", "print", "lamp", "light", "led", "solar", "garden", "outdoor",
  "patio", "chair", "table", "desk", "mouse", "pad", "stand", "mount",
  "car", "seat", "trunk", "phone", "cable", "charger", "usb", "speaker",
  "headphone", "watch", "jewelry", "bracelet", "necklace", "ring",
  "baby", "kids", "toy", "game", "puzzle", "book", "pen", "notebook",
  "fitness", "yoga", "resistance", "band", "massage", "camping", "tent",
  "fishing", "bike", "tool", "drill", "screwdriver", "wrench", "tape",
  "cleaning", "brush", "mop", "vacuum", "duster", "sponge", "gloves",
  "hat", "cap", "scarf", "sock", "shoe", "slipper", "sandal", "belt",
  "wallet", "backpack", "luggage", "umbrella", "sunglasses", "mirror",
  "clock", "vase", "plant", "pot", "planter", "watering", "hose", "nozzle",
  "grill", "bbq", "smoker", "ham", "coffee", "tea", "mug", "bottle",
  "wine", "glass", "plate", "bowl", "fork", "spoon", "spatula", "tong",
  "ice", "tray", "mold", "baking", "cake", "cookie", "sheet", "liner",
  "curtain", "rug", "carpet", "doormat", "pill", "first", "aid", "mask",
];

async function appToken(config: {
  clientId: string;
  clientSecret: string;
  baseUrl: string;
}): Promise<string> {
  const res = await fetch(`${config.baseUrl}/identity/v1/oauth2/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": `Basic ${btoa(`${config.clientId}:${config.clientSecret}`)}`,
    },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      scope: "https://api.ebay.com/oauth/api_scope",
    }),
  });
  if (!res.ok) throw new Error(`token grant failed HTTP ${res.status}`);
  return (await res.json()).access_token as string;
}

async function loadEnvLocal(): Promise<Record<string, string | undefined>> {
  const env: Record<string, string | undefined> = { ...Deno.env.toObject() };
  const text = await Deno.readTextFile(".env.local");
  for (const line of text.split("\n")) {
    const match = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (match) env[match[1]] = match[2];
  }
  return env;
}

const config = loadConfig(await loadEnvLocal(), { requireRefreshToken: false });
const token = await appToken(config);

const seen = new Map<string, { title: string; price: string }>();
for (const q of KEYWORDS) {
  for (let offset = 0; offset < 1000; offset += 200) {
    const qs = new URLSearchParams({
      q,
      filter: "sellers:{divinit-92}",
      limit: "200",
      offset: String(offset),
    });
    const res = await fetch(
      `${config.baseUrl}/buy/browse/v1/item_summary/search?${qs}`,
      {
        headers: {
          "Authorization": `Bearer ${token}`,
          "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        },
      },
    );
    if (!res.ok) break;
    const data = await res.json();
    const items = data.itemSummaries ?? [];
    for (const it of items) {
      const id = String(it.itemId ?? "").split("|")[1];
      if (id && !seen.has(id)) {
        seen.set(id, {
          title: String(it.title ?? ""),
          price: String(it.price?.value ?? ""),
        });
      }
    }
    if (items.length < 200) break;
  }
}

const out = [...seen.entries()].map(([itemId, v]) => ({
  itemId,
  title: v.title,
  price: v.price,
}));
console.log(JSON.stringify({ total: out.length, items: out }, null, 2));

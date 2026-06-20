#!/usr/bin/env node
/* Update the Amazon links in the shopping lists via the Amazon Creators API.
 *
 * Runs LOCALLY ONLY (needs the secret in .env) - never in public CI.
 * The static GitHub Pages site can't hold a secret, so the workflow is:
 *   1. run this locally   ->  rewrites the markdown (prices, validated ASINs)
 *   2. commit the markdown ->  deploy ships the refreshed, plain links
 *
 * Modes:
 *   --audit   parse the files and list every Amazon link found (NO API call)
 *   --check   verify credentials + one sample product call
 *   --write   query the API and rewrite prices / flag dead ASINs in the files
 *   --resolve-search  (with --write) also turn /s?k= search links into the
 *                     top concrete /dp/ASIN product link
 *
 * Usage:  node tools/amazon-creators/update-links.mjs --check
 */
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { CreatorsApi } from "./creators-api.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, "../..");
const FILES = ["Materials/Einkaufsliste-Links.md", "Materials/ShoppingList.md"];
const args = new Set(process.argv.slice(2));
const mode = args.has("--write") ? "write" : args.has("--check") ? "check" : "audit";

function loadEnv() {
  try {
    for (const line of readFileSync(resolve(HERE, ".env"), "utf8").split("\n")) {
      const m = line.match(/^\s*([A-Z_]+)=(.*)$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
    }
  } catch { /* rely on real env */ }
}

function apiFromEnv() {
  loadEnv();
  const { CREATORS_CLIENT_ID, CREATORS_CLIENT_SECRET } = process.env;
  if (!CREATORS_CLIENT_ID || !CREATORS_CLIENT_SECRET) {
    console.error("Missing CREATORS_CLIENT_ID / CREATORS_CLIENT_SECRET (see .env.example).");
    process.exit(1);
  }
  return new CreatorsApi({
    clientId: CREATORS_CLIENT_ID,
    clientSecret: CREATORS_CLIENT_SECRET,
    version: process.env.CREATORS_VERSION || "3.2",
    marketplace: process.env.CREATORS_MARKETPLACE || "www.amazon.de",
    partnerTag: process.env.CREATORS_PARTNER_TAG || "huskynarr-21",
  });
}

// ---- markdown link extraction ----
const ASIN_RE = /amazon\.[a-z.]+\/(?:[^\s)]*?\/)?dp\/([A-Z0-9]{10})/i;
const SEARCH_RE = /amazon\.[a-z.]+\/(?:[^\s)]*?)\/?s\?[^\s)]*?\bk=([^&\s)]+)/i;

function scanFile(rel) {
  const text = readFileSync(resolve(REPO, rel), "utf8");
  const out = [];
  text.split("\n").forEach((line, i) => {
    if (!/amazon\./i.test(line)) return;
    const asin = line.match(ASIN_RE);
    const search = line.match(SEARCH_RE);
    if (asin) out.push({ file: rel, line: i + 1, type: "dp", key: asin[1] });
    else if (search) out.push({ file: rel, line: i + 1, type: "search", key: decodeURIComponent(search[1].replace(/\+/g, " ")) });
  });
  return out;
}

function priceOf(item) {
  // tolerant dig for a display price across possible response shapes
  const j = item || {};
  const lp = j.offersV2?.listings?.[0]?.price || j.offers?.listings?.[0]?.price || j.price;
  return lp?.money?.displayAmount || lp?.displayAmount || lp?.amount || null;
}

async function runAudit() {
  let n = 0;
  for (const f of FILES) {
    const links = scanFile(f);
    n += links.length;
    console.log(`\n# ${f}  (${links.length} Amazon links)`);
    for (const l of links) console.log(`  L${String(l.line).padStart(3)}  ${l.type === "dp" ? "ASIN  " : "SEARCH"}  ${l.key}`);
  }
  console.log(`\nTotal: ${n} Amazon links across ${FILES.length} files.`);
  console.log("Parser OK. Run with --write (account must be Creators-API eligible) to refresh.");
}

async function runCheck() {
  const api = apiFromEnv();
  process.stdout.write("Token exchange ... ");
  await api._auth();
  console.log("OK");
  const sample = scanFile(FILES[0]).find((l) => l.type === "dp");
  if (!sample) return console.log("No ASIN sample found to test.");
  process.stdout.write(`getItems(${sample.key}) ... `);
  const r = await api.getItems([sample.key]);
  if (r.ok) console.log(`OK - price: ${priceOf(r.json?.itemsResult?.items?.[0] ?? r.json?.items?.[0]) || "(parse)"}`);
  else console.log(`HTTP ${r.status}: ${r.json?.reason || r.json?.message || r.raw?.slice(0, 160)}`);
}

async function runWrite() {
  const api = apiFromEnv();
  await api._auth();
  const resolveSearch = args.has("--resolve-search");
  let changed = 0, dead = 0, skipped = 0;
  for (const f of FILES) {
    let text = readFileSync(resolve(REPO, f), "utf8");
    const lines = text.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const asin = lines[i].match(ASIN_RE);
      if (asin) {
        const r = await api.getItems([asin[1]]);
        if (!r.ok) { skipped++; if (r.status === 403) { console.error("Account not eligible (403) - aborting writes."); return; } continue; }
        const item = r.json?.itemsResult?.items?.[0] ?? r.json?.items?.[0];
        if (!item) { console.warn(`! dead/invalid ASIN ${asin[1]} (L${i + 1} ${f})`); dead++; continue; }
        const price = priceOf(item);
        if (price) { lines[i] = refreshPriceCell(lines[i], price); changed++; }
      } else if (resolveSearch) {
        const s = lines[i].match(SEARCH_RE);
        if (!s) continue;
        const term = decodeURIComponent(s[1].replace(/\+/g, " "));
        const r = await api.searchItems(term, { itemCount: 1 });
        if (!r.ok) { skipped++; continue; }
        const item = r.json?.searchResult?.items?.[0] ?? r.json?.items?.[0];
        if (item?.asin || item?.itemId) {
          const id = item.asin || item.itemId;
          lines[i] = lines[i].replace(SEARCH_RE, `amazon.de/dp/${id}`);
          const price = priceOf(item);
          if (price) lines[i] = refreshPriceCell(lines[i], price);
          changed++;
        }
      }
    }
    writeFileSync(resolve(REPO, f), lines.join("\n"));
  }
  console.log(`Done. ${changed} updated, ${dead} dead ASINs flagged, ${skipped} skipped.`);
}

// table row: | Posten | Produkt | Shop | Preis ca. | Link |  -> rewrite 4th cell
function refreshPriceCell(line, price) {
  const cells = line.split("|");
  if (cells.length >= 6) { cells[4] = ` ${price} `; return cells.join("|"); }
  return line;
}

const run = mode === "write" ? runWrite : mode === "check" ? runCheck : runAudit;
run().catch((e) => { console.error("ERROR: " + e.message); process.exit(1); });

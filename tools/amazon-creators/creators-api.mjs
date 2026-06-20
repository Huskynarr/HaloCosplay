/* Minimal Amazon Creators API (v3.x LWA) client - no dependencies, Node 18+ global fetch.
 *
 * The Creators API replaced the old Product Advertising API (PA-API). It uses
 * Login-with-Amazon OAuth2 client_credentials. Credentials are REGION-based:
 *   v3.1 -> NA  (api.amazon.com)
 *   v3.2 -> EU  (api.amazon.co.uk)   <- amazon.de lives here
 *   v3.3 -> FE  (api.amazon.co.jp)
 * Spec reverse-engineered from the official docs + the apaapi reference lib.
 *
 * SECURITY: never hard-code the secret. Read it from the environment / .env.
 */

const TOKEN_ENDPOINTS = {
  "3.1": "https://api.amazon.com/auth/o2/token",
  "3.2": "https://api.amazon.co.uk/auth/o2/token",
  "3.3": "https://api.amazon.co.jp/auth/o2/token",
};
const API_HOST = "https://creatorsapi.amazon";
const API_PATH = "/catalog/v1";

export class CreatorsApi {
  constructor({ clientId, clientSecret, version = "3.2", marketplace = "www.amazon.de", partnerTag }) {
    if (!clientId || !clientSecret) throw new Error("clientId and clientSecret are required");
    if (!TOKEN_ENDPOINTS[version]) throw new Error(`Unsupported version ${version} (use 3.1/3.2/3.3)`);
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.version = version;
    this.marketplace = marketplace;
    this.partnerTag = partnerTag;
    this._token = null;
    this._exp = 0;
  }

  async _auth() {
    if (this._token && Date.now() < this._exp) return this._token;
    const res = await fetch(TOKEN_ENDPOINTS[this.version], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        grant_type: "client_credentials",
        client_id: this.clientId,
        client_secret: this.clientSecret,
        scope: "creatorsapi::default",
      }),
    });
    const text = await res.text();
    if (!res.ok) throw new Error(`Token HTTP ${res.status}: ${text.slice(0, 300)}`);
    const data = JSON.parse(text);
    if (!data.access_token) throw new Error(`No access_token in response: ${text.slice(0, 300)}`);
    this._token = data.access_token;
    this._exp = Date.now() + ((data.expires_in || 3600) - 60) * 1000;
    return this._token;
  }

  async _call(operation, body) {
    const token = await this._auth();
    const res = await fetch(`${API_HOST}${API_PATH}/${operation}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json; charset=utf-8",
        "x-marketplace": this.marketplace,
        "User-Agent": "halocosplay-link-updater/1.0",
      },
      body: JSON.stringify({ partnerTag: this.partnerTag, partnerType: "Associates", marketplace: this.marketplace, ...body }),
    });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* keep raw */ }
    return { ok: res.ok, status: res.status, json, raw: text };
  }

  /** Validate ASINs and fetch title/price/image/url. ids: string[] (max 10 per call). */
  getItems(itemIds, resources) {
    return this._call("getItems", {
      itemIds,
      resources: resources || ["itemInfo.title", "offersV2.listings.price", "images.primary.medium"],
    });
  }

  /** Resolve a search term to products. */
  searchItems(keywords, { itemCount = 3, searchIndex = "All", resources } = {}) {
    return this._call("searchItems", {
      keywords, itemCount, searchIndex,
      resources: resources || ["itemInfo.title", "offersV2.listings.price", "images.primary.medium"],
    });
  }
}

/** Just verify credentials work (token exchange only). */
export async function checkAuth(cfg) {
  const api = new CreatorsApi(cfg);
  await api._auth();
  return true;
}

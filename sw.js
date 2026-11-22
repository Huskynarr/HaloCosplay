/* Offline support for the guide site (scope: repository root on GitHub Pages).
 * Network first, so online visitors always get the current files; the cache is
 * only the fallback when the network fails or stalls. Nothing here is hardware
 * or build evidence - it only keeps already published pages readable offline. */
'use strict';

const CACHE = 'halo-guide-v1';
const NETWORK_TIMEOUT_MS = 4000;
const REFRESH_MS = 24 * 60 * 60 * 1000;
const STAMP = new URL('__offline-guides-stamp', self.registration.scope).href;
// App shell, relative to this file. Tests/Automation/guide.test.cjs checks that every entry exists.
const SHELL = [
  'web/', 'web/index.html', 'web/app.js', 'web/content.js', 'web/guide.js', 'web/monitoring.js', 'web/favicon.svg',
  'web/vendor/tailwind.css', 'web/vendor/marked-12.0.2.min.js', 'web/vendor/purify-3.4.17.min.js',
  'web/fonts/fonts.css', 'web/fonts/barlow-400.woff2', 'web/fonts/barlow-500.woff2', 'web/fonts/barlow-600.woff2',
  'web/fonts/chakra-petch-500.woff2', 'web/fonts/chakra-petch-600.woff2', 'web/fonts/chakra-petch-700.woff2',
  'web/fonts/jetbrains-mono-var.woff2',
  'web/products/', 'web/products/index.html', 'web/products/style.css', 'web/products/catalog.js',
  'web/products/products.js', 'web/products/app.js',
  'web/configurator/', 'web/configurator/index.html', 'web/configurator/style.css', 'web/configurator/profile.js',
  'web/configurator/app.js',
  'web/budget/', 'web/budget/index.html', 'web/budget/style.css', 'web/budget/budget.js', 'web/budget/app.js',
];
// Large downloads stay network only: they would fill the cache without helping at a convention.
const SKIP = /\.(pdf|stl|blend|zip|3mf|scad)$/i;

function cacheable(url) {
  return url.origin === self.location.origin && url.pathname.startsWith(new URL(self.registration.scope).pathname) &&
    !SKIP.test(url.pathname);
}

async function store(request, response) {
  if (response && response.status === 200 && response.type === 'basic') {
    const cache = await caches.open(CACHE);
    await cache.put(request, response.clone());
  }
  return response;
}

async function addAll(paths) {
  const cache = await caches.open(CACHE);
  let stored = 0;
  for (const path of paths) {
    const url = new URL(path, self.registration.scope);
    if (!cacheable(url)) continue;
    try {
      const response = await fetch(url, {cache: 'no-cache'});
      if (response.status === 200) { await cache.put(url, response); stored++; }
    } catch (error) { /* offline or missing: keep whatever is cached already */ }
  }
  return stored;
}

self.addEventListener('install', event => {
  event.waitUntil(addAll(SHELL).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(key => key.startsWith('halo-guide-') && key !== CACHE).map(key => caches.delete(key))))
    .then(() => self.clients.claim()));
});

// The page sends the guide list from content.js once; answer with the number stored.
self.addEventListener('message', event => {
  const data = event.data || {};
  if (data.type !== 'precache' || !Array.isArray(data.files)) return;
  const files = data.files.filter(file => typeof file === 'string' && /^[A-Za-z0-9_./-]+\.md$/.test(file) && !file.includes('..'));
  event.waitUntil((async () => {
    // Refresh the whole guide set at most once a day; opened guides are refreshed on every online visit anyway.
    const cache = await caches.open(CACHE);
    const stamp = await cache.match(STAMP);
    const previous = stamp ? await stamp.json() : null;
    let stored = previous ? previous.stored : 0;
    if (!previous || Date.now() - previous.time > REFRESH_MS || previous.requested !== files.length) {
      stored = await addAll(files.slice(0, 400));
      await cache.put(STAMP, new Response(JSON.stringify({time: Date.now(), stored: stored, requested: files.length}),
        {headers: {'Content-Type': 'application/json'}}));
    }
    if (event.source) event.source.postMessage({type: 'precached', stored: stored, requested: files.length});
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET' || request.headers.has('range')) return;
  const url = new URL(request.url);
  if (!cacheable(url)) return;
  event.respondWith((async () => {
    const cached = await caches.match(request, {ignoreSearch: request.mode === 'navigate'});
    const network = fetch(request).then(response => store(request, response));
    if (!cached) return network;
    // A dead-but-connected network (crowded hall) must not block a page that is already cached.
    const timeout = new Promise(resolve => setTimeout(() => resolve(cached), NETWORK_TIMEOUT_MS));
    return Promise.race([network.catch(() => cached), timeout]);
  })());
});

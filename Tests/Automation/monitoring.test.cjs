'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '../..');
const source = fs.readFileSync(path.join(root, 'web/monitoring.js'), 'utf8');

function browser(url = 'https://huskynarr.github.io/HaloCosplay/web/', options) {
  const listeners = new Map(), scripts = [], captured = [];
  let config;
  const sentry = {
    init(value) { config = value; },
    captureException(error, hint) { captured.push({error, hint}); return 'event-id'; }
  };
  for (const name of ['globalHandlers', 'browserApiErrors', 'eventFilters', 'dedupe']) {
    sentry[name + 'Integration'] = () => ({name});
  }
  const window = {
    HaloMonitoringOptions: options,
    addEventListener(type, fn) { listeners.set(type, fn); },
    removeEventListener(type, fn) { if (listeners.get(type) === fn) listeners.delete(type); }
  };
  const sandbox = {
    window, location: new URL(url), URL,
    document: {createElement: () => ({}), head: {appendChild: script => scripts.push(script)}}
  };
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox);
  return {
    window, scripts, captured, listeners,
    config: () => config,
    dispatch(type, event) { listeners.get(type)?.(event); },
    load() { window.Sentry = sentry; scripts[0].onload(); },
    rerun() { vm.runInContext(source, sandbox); }
  };
}

test('local HTTP, file URLs and HTTPS loopback do not load or send telemetry by default', () => {
  for (const url of ['http://localhost:8000/web/', 'http://127.0.0.1/web/', 'file:///tmp/web/index.html', 'https://localhost/web/', 'https://[::1]/web/']) {
    const b = browser(url);
    assert.equal(b.scripts.length, 0, url);
    assert.equal(b.listeners.size, 0);
    assert.doesNotThrow(() => b.window.HaloMonitoring.captureException(new Error('offline')));
    assert.equal(b.captured.length, 0);
  }
});

test('production uses a version-pinned, integrity-checked, non-blocking SDK with no CDN referrer', () => {
  const b = browser();
  assert.equal(b.scripts.length, 1);
  const script = b.scripts[0];
  assert.match(script.src, /^https:\/\/browser\.sentry-cdn\.com\/\d+\.\d+\.\d+\/bundle\.min\.js$/);
  assert.match(script.integrity, /^sha384-[A-Za-z0-9+/]{64}$/);
  assert.equal(script.crossOrigin, 'anonymous');
  assert.equal(script.referrerPolicy, 'no-referrer');
  assert.equal(script.async, true);
  assert.equal(script.fetchPriority, 'low');
  b.rerun();
  assert.equal(b.scripts.length, 1, 'duplicate inclusion must not register a second client');
});

test('local development requires explicit opt-in and production can explicitly opt out', () => {
  const b = browser('http://localhost:8000/web/', {enabled: true});
  b.load();
  assert.equal(b.config().environment, 'development');
  assert.equal(browser(undefined, {enabled: false}).scripts.length, 0);
});

test('early exceptions and promise rejections are buffered once with unhandled mechanisms', () => {
  const b = browser();
  const early = new Error('early failure'), rejection = new Error('promise failure');
  b.dispatch('error', {message: early.message, error: early});
  b.dispatch('unhandledrejection', {reason: rejection});
  b.dispatch('error', {target: {src: 'missing-image.png'}});
  b.load();
  assert.equal(b.captured.length, 2);
  assert.equal(b.captured[0].error, early);
  assert.equal(b.captured[0].hint.mechanism.handled, false);
  assert.equal(b.captured[0].hint.mechanism.type, 'onerror');
  assert.equal(b.captured[1].error, rejection);
  assert.equal(b.captured[1].hint.mechanism.type, 'onunhandledrejection');
  assert.equal(b.listeners.size, 0, 'buffer listeners must be removed after SDK takeover');
  assert.equal(b.window.HaloMonitoring.captureException(new Error('load failed'), 'guide-load'), 'event-id');
  assert.equal(b.captured[2].hint.captureContext.tags.operation, 'guide-load');
});

test('early buffer is bounded and a blocked or broken SDK does not break the app', () => {
  const b = browser();
  for (let i = 0; i < 30; i++) b.dispatch('unhandledrejection', {reason: new Error('failure ' + i)});
  b.load();
  assert.equal(b.captured.length, 20);
  const blocked = browser();
  blocked.dispatch('unhandledrejection', {reason: 'pending'});
  blocked.scripts[0].onerror();
  assert.equal(blocked.listeners.size, 0);
  assert.doesNotThrow(() => blocked.window.HaloMonitoring.captureException(new Error('later')));
  assert.equal(blocked.captured.length, 0);
  const broken = browser();
  assert.doesNotThrow(() => broken.scripts[0].onload());
  assert.equal(broken.listeners.size, 0);
});

test('error-only settings do not install replay, tracing, sessions, logs or breadcrumbs', () => {
  const b = browser(); b.load();
  const c = b.config();
  assert.equal(new URL(c.dsn).hostname, 'logging.gardenpiratez.de');
  assert.equal(new URL(c.dsn).pathname, '/57');
  assert.equal(c.environment, 'production');
  assert.equal(c.defaultIntegrations, false);
  assert.deepEqual(Array.from(c.integrations, i => i.name), ['globalHandlers', 'browserApiErrors', 'eventFilters', 'dedupe']);
  assert.equal(c.maxBreadcrumbs, 0);
  assert.equal(c.sendClientReports, false);
  for (const key of ['userInfo', 'cookies', 'httpHeaders', 'urlQueryParams', 'stackFrameVariables']) assert.equal(c.dataCollection[key], false);
  assert.equal(c.dataCollection.httpBodies.length, 0);
});

test('beforeSend removes private scope data and query/hash parts while retaining useful stack locations', () => {
  const b = browser('https://huskynarr.github.io/HaloCosplay/web/configurator/?profile=PRIVATE#PRIVATE');
  b.load();
  const event = {
    user: {email: 'PRIVATE'}, extra: {measurements_mm: {height: 1740}},
    breadcrumbs: [{message: 'PRIVATE'}], contexts: {profile: {name: 'PRIVATE'}},
    request: {url: 'PRIVATE', headers: {Cookie: 'PRIVATE'}, data: 'PRIVATE'},
    exception: {values: [{type: 'Error', value: 'schema failed', stacktrace: {frames: [
      {filename: 'https://huskynarr.github.io/HaloCosplay/web/app.js?token=PRIVATE#PRIVATE', lineno: 12, colno: 8, vars: {profile: 'PRIVATE'}},
      {filename: 'blob:https://example.invalid/PRIVATE'}
    ]}}]}, tags: {app: 'halocosplay-frontend'}
  };
  const sent = b.config().beforeSend(event);
  assert.doesNotMatch(JSON.stringify(sent), /PRIVATE|measurements_mm/);
  assert.equal(sent.request.url, 'https://huskynarr.github.io/HaloCosplay/web/configurator/');
  const frame = sent.exception.values[0].stacktrace.frames[0];
  assert.equal(frame.filename, 'https://huskynarr.github.io/HaloCosplay/web/app.js');
  assert.equal(frame.lineno, 12);
  assert.equal(frame.colno, 8);
  assert.equal(sent.exception.values[0].value, 'schema failed');
  assert.doesNotThrow(() => b.config().beforeSend({}));
});

test('all five public frontend entrypoints load monitoring before application scripts', () => {
  for (const page of ['index.html', 'configurator/index.html', 'budget/index.html', 'products/index.html', 'cortana/index.html']) {
    const html = fs.readFileSync(path.join(root, 'web', page), 'utf8');
    const scripts = Array.from(html.matchAll(/<script\b[^>]*>/g), m => m[0]);
    assert.match(scripts[0], /src="(?:\.\.\/)?monitoring\.js"/, page);
  }
  const exhibition = fs.readFileSync(path.join(root, 'Code/Exhibition/index.html'), 'utf8');
  assert.doesNotMatch(exhibition, /monitoring\.js|sentry/i, 'offline exhibition stays self-contained');
});

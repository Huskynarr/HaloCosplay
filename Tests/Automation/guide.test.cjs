const {test} = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const guide = require('../../web/guide.js');
const web = path.resolve(__dirname, '../../web');
const read = file => fs.readFileSync(path.join(web, file), 'utf8');
const TOP = ['Documentation/', 'Materials/'];

test('guide paths stay inside the repository and end in .md', () => {
  for (const ok of ['README.md', 'Documentation/Guides/Exoskelett.md', 'Design/HardwareKit/README.MD']) assert.equal(guide.safeDocPath(ok), ok);
  for (const bad of ['', '../x.md', 'a/../../x.md', '/etc/x.md', '//host/x.md', 'https://host/x.md', 'javascript:x.md',
    'a\\b.md', 'a/./b.md', 'a//b.md', 'a.md?x=1', 'a%2e%2e/b.md', 'a.html', 'a.md/', 'x\u0000.md', 'a'.repeat(400) + '.md', null, 7]) {
    assert.equal(guide.safeDocPath(bad), null, String(bad));
  }
});

test('route parsing never throws and separates guide from section', () => {
  assert.deepEqual(guide.parseRoute(''), {file: '', anchor: ''});
  assert.deepEqual(guide.parseRoute('#'), {file: '', anchor: ''});
  assert.equal(guide.parseRoute('#%').error, 'encoding');
  assert.equal(guide.parseRoute('#%E0%A4%A').error, 'encoding');
  assert.equal(guide.parseRoute('#../../Other/x.md').error, 'path');
  assert.equal(guide.parseRoute('#..%2F..%2FOther%2Fx.md').error, 'path');
  assert.equal(guide.parseRoute('#https://example.org/x.md').error, 'path');
  assert.equal(guide.parseRoute('#Documentation/Guides/x.html').error, 'path');
  assert.deepEqual(guide.parseRoute('#Documentation/Guides/Exoskelett.md'), {file: 'Documentation/Guides/Exoskelett.md', anchor: ''});
  assert.deepEqual(guide.parseRoute('#Documentation/Guides/Exoskelett.md#3a-Neues Ziel'), {file: 'Documentation/Guides/Exoskelett.md', anchor: '3a-neues-ziel'});
  assert.deepEqual(guide.parseRoute('#Materials%2FShoppingList.md'), {file: 'Materials/ShoppingList.md', anchor: ''});
  assert.deepEqual(guide.parseRoute('#3d-viewer'), {file: '3d-viewer', anchor: '', sentinel: true});
});

test('heading ids follow GitHub slugs and stay unique', () => {
  assert.equal(guide.slug('3a. Neues Entwicklungsziel: Ruestungslast zum Boden'), '3a-neues-entwicklungsziel-ruestungslast-zum-boden');
  assert.equal(guide.slug('  Laufzeit (Wh statt mAh rechnen!) '), 'laufzeit-wh-statt-mah-rechnen');
  assert.equal(guide.slug('<img src=x onerror=alert(1)>'), 'img-srcx-onerroralert1');
  assert.deepEqual(guide.headingIds(['Teile', 'Teile', 'Hinweis', 'Teile', 'constructor']), ['teile', 'teile-1', 'hinweis', 'teile-2', 'constructor']);
});

test('links are rewritten to in-app routes, assets or blocked', () => {
  const from = 'Documentation/Guides/Exoskelett.md';
  assert.deepEqual(guide.rewriteLink('https://example.org/a', from, TOP), {kind: 'external', href: 'https://example.org/a'});
  assert.equal(guide.rewriteLink('mailto:a@example.org', from, TOP).kind, 'external');
  assert.deepEqual(guide.rewriteLink('#3a-neues-ziel', from, TOP), {kind: 'anchor', anchor: '3a-neues-ziel', href: '#' + from + '#3a-neues-ziel'});
  assert.deepEqual(guide.rewriteLink('Sicherheit.md#hitze', from, TOP), {kind: 'doc', file: 'Documentation/Guides/Sicherheit.md', anchor: 'hitze', href: '#Documentation/Guides/Sicherheit.md#hitze'});
  assert.equal(guide.rewriteLink('../../Materials/ShoppingList.md', from, TOP).href, '#Materials/ShoppingList.md');
  assert.equal(guide.rewriteLink('Materials/ShoppingList.md', from, TOP).href, '#Materials/ShoppingList.md');
  assert.deepEqual(guide.rewriteLink('../../Design/HardwareKit/Preview.png', from, TOP), {kind: 'asset', path: 'Design/HardwareKit/Preview.png'});
  // Leaving the repository is impossible: surplus ".." segments are dropped.
  assert.equal(guide.rewriteLink('../../../../../Other/x.md', from, TOP).href, '#Other/x.md');
  for (const bad of ['javascript:alert(1)', ' JaVaScRiPt:alert(1)', 'data:text/html,x', 'vbscript:x', '//evil.example/x.md', 'file:///etc/passwd', '']) {
    assert.equal(guide.rewriteLink(bad, from, TOP).kind, 'blocked', bad);
  }
});

test('sanitizer wrapper fails closed and keeps only checkbox inputs', () => {
  assert.throws(() => guide.sanitize(undefined, '<p>x</p>'), /sanitizer missing/);
  const hooks = {};
  const fake = {addHook: (name, fn) => { hooks[name] = (hooks[name] || 0) + 1; fake.hook = fn; }, sanitize: (html, config) => ({html, config})};
  const first = guide.sanitize(fake, '<p>x</p>');
  guide.sanitize(fake, '<p>y</p>');
  assert.equal(hooks.afterSanitizeAttributes, 1, 'hook registered once');
  assert.equal(first.config, guide.purifyConfig);
  for (const attr of ['style', 'id', 'class', 'srcset']) assert.ok(guide.purifyConfig.FORBID_ATTR.includes(attr));
  for (const tag of ['style', 'form', 'button', 'textarea']) assert.ok(guide.purifyConfig.FORBID_TAGS.includes(tag));
  const removed = [];
  const node = type => ({nodeName: 'INPUT', getAttribute: () => type, parentNode: {removeChild: n => removed.push(n)}});
  fake.hook(node('checkbox')); fake.hook(node('CHECKBOX'));
  assert.equal(removed.length, 0);
  fake.hook(node('text')); fake.hook(node(null));
  assert.equal(removed.length, 2);
});

test('main page loads pinned local libraries and has no inline script handlers', () => {
  const html = read('index.html'), app = read('app.js');
  assert.doesNotMatch(html, /cdn\.jsdelivr\.net/);
  assert.match(html, /<script src="vendor\/marked-12\.0\.2\.min\.js" defer><\/script>\s*<script src="vendor\/purify-3\.4\.17\.min\.js" defer><\/script>/);
  assert.ok(html.indexOf('guide.js') < html.indexOf('"app.js"'));
  // Deferred scripts run in document order; a mix of deferred and blocking scripts would break that order.
  const scripts = [...html.matchAll(/<script src="([^"]+)"( defer)?><\/script>/g)];
  assert.deepEqual(scripts.filter(match => !match[2]).map(match => match[1]), ['monitoring.js']);
  for (const source of [html, app, read('configurator/index.html'), read('budget/index.html'), read('products/index.html')]) {
    assert.doesNotMatch(source, /\son(click|error|load|change|input|submit)\s*=\s*["']/i);
  }
  assert.doesNotMatch(app, /innerHTML\s*=\s*marked\.parse/);
  assert.doesNotMatch(app, /decodeURIComponent\(location\.hash/);
});

test('vendored libraries match the documented hashes', () => {
  const table = read('vendor/README.md');
  for (const file of ['marked-12.0.2.min.js', 'purify-3.4.17.min.js']) {
    const digest = crypto.createHash('sha256').update(fs.readFileSync(path.join(web, 'vendor', file))).digest('hex');
    assert.ok(table.includes(digest), file + ' differs from web/vendor/README.md');
  }
});

test('every page ships a CSP before its first script and without script unsafe-inline', () => {
  for (const page of ['index.html', 'configurator/index.html', 'budget/index.html', 'products/index.html', 'cortana/index.html']) {
    const html = read(page);
    const match = html.match(/<meta http-equiv="Content-Security-Policy" content="([^"]+)">/);
    assert.ok(match, page + ' has no CSP');
    assert.ok(html.indexOf(match[0]) < html.indexOf('<script'), page + ': CSP must precede scripts');
    const script = match[1].split(';').map(part => part.trim()).find(part => part.startsWith('script-src'));
    assert.ok(script, page);
    assert.doesNotMatch(script, /unsafe-inline|unsafe-eval|\*|data:|https:(?!\/\/)/, page);
    assert.match(match[1], /base-uri '(none|self)'/);
  }
});

test('Cortana viewer CSP hash matches its inline script', () => {
  const html = read('cortana/index.html');
  const inline = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1]);
  assert.equal(inline.length, 1);
  const digest = crypto.createHash('sha256').update(inline[0]).digest('base64');
  assert.ok(html.includes("'sha256-" + digest + "'"), 'Update the sha256 in the CSP meta after editing the inline script: sha256-' + digest);
  assert.match(inline[0], /try \{ data = JSON\.parse/);
  assert.match(inline[0], /typeof data\.id === "string"/);
});

test('service worker shell lists only files that exist and skips large downloads', () => {
  const repo = path.resolve(__dirname, '../..');
  const source = fs.readFileSync(path.join(repo, 'sw.js'), 'utf8');
  const shell = source.match(/const SHELL = \[([\s\S]*?)\];/)[1].match(/'[^']+'/g).map(item => item.slice(1, -1));
  assert.ok(shell.length > 20);
  for (const entry of shell) {
    const file = path.join(repo, entry.endsWith('/') ? entry + 'index.html' : entry);
    assert.ok(fs.existsSync(file), 'missing shell file: ' + entry);
  }
  // Every local asset the main page references directly must be in the shell.
  const html = fs.readFileSync(path.join(repo, 'web/index.html'), 'utf8');
  for (const match of html.matchAll(/<(?:script|link)[^>]+(?:src|href)="([^"#:]+\.(?:js|css))"/g)) {
    assert.ok(shell.includes('web/' + match[1]), 'not cached for offline use: ' + match[1]);
  }
  const skip = new RegExp(source.match(/const SKIP = \/(.*)\/i;/)[1], 'i');
  assert.ok(skip.test('Resources/CosplayGuides/MK7_CosplayGuide_Full.pdf'));
  assert.ok(!skip.test('Documentation/Guides/Sicherheit.md'));
});

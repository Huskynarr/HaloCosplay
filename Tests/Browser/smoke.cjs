/* Real DOM, imports, downloads and profile isolation. Run with Playwright installed. */
'use strict';
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../..');
const output = path.join(root, 'build/browser-results');
const mime = {'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml'};
const server = http.createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    let file = path.resolve(root, '.' + pathname);
    if (!file.startsWith(root + path.sep)) throw new Error('Outside root');
    if ((await fs.stat(file)).isDirectory()) file = path.join(file, 'index.html');
    const content = await fs.readFile(file);
    response.writeHead(200, {'Content-Type': mime[path.extname(file)] || 'application/octet-stream'});
    response.end(content);
  } catch { response.writeHead(404); response.end('Not found'); }
});

async function downloadJSON(page, button) {
  const downloaded = page.waitForEvent('download');
  await page.locator(button).click();
  const download = await downloaded;
  return JSON.parse(await fs.readFile(await download.path(), 'utf8'));
}

(async () => {
  await fs.mkdir(output, {recursive: true});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({headless: true});
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}, acceptDownloads: true});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    // A CSP that blocks something the pages need must fail the run, not pass silently.
    page.on('console', entry => { if (/Content Security Policy/i.test(entry.text())) errors.push('CSP: ' + entry.text().slice(0, 300)); });
    page.on('dialog', dialog => dialog.accept());
    const base = 'http://127.0.0.1:' + server.address().port;

    await page.goto(base + '/web/configurator/');
    await page.locator('#workspace').waitFor({state: 'visible'});
    assert.equal(await page.locator('#count').textContent(), '0 / 32');
    assert.equal(await page.locator('#measurements_mm-height').inputValue(), '');
    await page.locator('#name').fill('Suit-A');
    await page.locator('#measurements_mm-height').fill('1740');
    await page.locator('#build-material').selectOption('foam');
    await page.locator('#build-fog_system').selectOption('pmi-cloud');
    const firstId = await page.locator('#profiles').inputValue();
    await page.locator('#new').click();
    assert.equal(await page.locator('#measurements_mm-height').inputValue(), '');
    await page.locator('#name').fill('Suit-B');
    await page.locator('#measurements_mm-height').fill('1880');
    await page.locator('#profiles').selectOption(firstId);
    assert.equal(await page.locator('#name').inputValue(), 'Suit-A');
    assert.equal(await page.locator('#measurements_mm-height').inputValue(), '1740');
    assert.equal(await page.locator('#build-material').inputValue(), 'foam');
    assert.equal(await page.evaluate(() => localStorage.length), 0);
    const profile = await downloadJSON(page, '#export');
    assert.equal(profile.profile, 'Suit-A');
    assert.equal(profile.build.fog_system, 'pmi-cloud');
    assert.equal(profile.measurements_mm.height, 1740);
    assert.equal(profile.measurements_mm.boot_width_l, null);
    assert.equal(profile.status, 'measurements_pending');
    await page.locator('#persist').check();
    await page.reload();
    await page.locator('#workspace').waitFor({state: 'visible'});
    assert.equal(await page.locator('#profiles option').count(), 2);
    assert.equal(await page.locator('#name').inputValue(), 'Suit-A');
    await page.locator('#persist').uncheck();
    assert.equal(await page.evaluate(() => localStorage.length), 0);
    await page.locator('#demo').click();
    await page.waitForFunction(() => document.querySelector('#kind').textContent === 'SYNTHETISCHE DEMO');
    assert.equal(await page.locator('#confirm').isDisabled(), true);
    await page.locator('#file').setInputFiles({name: 'Suit-A.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(profile))});
    await page.waitForFunction(() => document.querySelector('#profiles').options.length === 4);
    assert.equal(await page.locator('#name').inputValue(), 'Suit-A');
    await page.screenshot({path: path.join(output, 'configurator-desktop.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true, 'Configurator must fit mobile width');
    await page.screenshot({path: path.join(output, 'configurator-mobile.png'), fullPage: true});

    // Browser copies survive schema changes; unreadable copies are kept, never replaced silently.
    const DATA = 'mjolnir:configurator:profiles:v1', CONSENT = 'mjolnir:configurator:consent:v1', BACKUP = DATA + ':backup';
    const stored = key => page.evaluate(name => localStorage.getItem(name), key);
    const seed = async raw => {
      await page.evaluate(([data, consent, value]) => { localStorage.clear(); localStorage.setItem(data, value); localStorage.setItem(consent, 'yes'); }, [DATA, CONSENT, raw]);
      await page.reload();
      await page.locator('#workspace').waitFor({state: 'visible'});
    };
    const older = JSON.parse(JSON.stringify(profile));
    delete older.measurements_mm.boot_width_l;
    older.measurements_mm.retired_measurement = 12;
    const olderRaw = JSON.stringify({schema_version: 1, active: 'old-1', profiles: [{id: 'old-1', data: older}]});
    await seed(olderRaw);
    assert.equal(await page.locator('#name').inputValue(), 'Suit-A', 'Older browser copy is still loaded');
    assert.equal(await page.locator('#measurements_mm-height').inputValue(), '1740');
    assert.equal(await page.locator('#measurements_mm-boot_width_l').inputValue(), '');
    assert.match(await page.locator('#message').textContent(), /angepasst: 1 Felder leer ergaenzt, 1 unbekannte Felder entfernt/);
    assert.equal(await stored(BACKUP), olderRaw, 'Unchanged earlier copy is kept');
    assert.equal(await page.locator('#persist').isChecked(), true);
    const backupDownload = page.waitForEvent('download');
    await page.locator('#backup-download').click();
    assert.equal(await fs.readFile(await (await backupDownload).path(), 'utf8'), olderRaw);
    await page.locator('#persist').uncheck();
    assert.equal(await page.evaluate(() => localStorage.length), 0, 'Turning storage off also removes the backup');
    assert.equal(await page.locator('#backup-download').count(), 0);

    await seed('{"schema_version":1,"profiles":[{"id":"x","data":{"profile":"Kaputt"');
    assert.match(await page.locator('#message').textContent(), /konnte nicht geladen werden\. Sie bleibt als Sicherung/);
    assert.equal(await page.locator('#persist').isChecked(), false);
    assert.equal(await page.locator('#profiles option').count(), 1);
    await page.locator('#persist').check();
    assert.equal(JSON.parse(await stored(DATA)).profiles.length, 1, 'Re-enabling storage writes the new session');
    assert.match(await stored(BACKUP), /Kaputt/, 'The unreadable copy is still available');

    // "Profil entfernt" must not claim more than happened.
    await page.locator('#name').fill('Bleibt');
    await page.locator('#new').click();
    await page.locator('#name').fill('Fehlerhaft');
    await page.locator('#measurements_mm-height').fill('1');
    const keepId = (await page.locator('#profiles option').first().getAttribute('value'));
    await page.locator('#profiles').selectOption(keepId);
    assert.equal(await page.locator('#name').inputValue(), 'Bleibt');
    await page.locator('#delete').click();
    assert.match(await page.locator('#message').textContent(), /Die Browserkopie enthaelt es noch/);
    assert.ok(JSON.parse(await stored(DATA)).profiles.some(record => record.data.profile === 'Bleibt'));
    await page.locator('#measurements_mm-height').fill('1750');
    await page.locator('#new').click();
    await page.locator('#delete').click();
    assert.equal(await page.locator('#message').textContent(), 'Profil aus Sitzung und Browserkopie entfernt.');
    assert.equal(JSON.parse(await stored(DATA)).profiles.length, 1);
    await page.locator('#persist').uncheck();
    assert.equal(await page.evaluate(() => localStorage.length), 0);

    await page.goto(base + '/web/budget/');
    await page.locator('#add').click();
    const row = page.locator('fieldset.item').first();
    await row.getByLabel('Bezeichnung', {exact: true}).fill('Test fan');
    await row.getByLabel('Anzahl', {exact: true}).fill('2');
    await row.getByLabel('EUR je Einheit: bis', {exact: true}).fill('15');
    await row.getByLabel('EUR je Einheit: von', {exact: true}).fill('10');
    assert.match(await page.locator('#unknown').textContent(), /unvollstaendig/);
    await row.getByLabel('Planmasse g je Einheit', {exact: true}).fill('100');
    assert.equal(await page.locator('#base').textContent(), '20,00 - 30,00 EUR');
    assert.equal(await page.locator('#reserved').textContent(), '24,00 - 36,00 EUR');
    assert.equal(await page.locator('#mass').textContent(), '0,2 kg');
    await row.getByLabel('Wird getragen', {exact: true}).uncheck();
    assert.equal(await page.locator('#mass').textContent(), '0 kg');
    const bom = await downloadJSON(page, '#export');
    assert.equal(bom.items[0].qty, 2);
    assert.equal(bom.items[0].worn, false);
    await page.locator('#new').click();
    assert.equal(await page.locator('fieldset.item').count(), 0);
    await page.locator('#file').setInputFiles({name: 'Test-BOM.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(bom))});
    await page.locator('fieldset.item').waitFor();
    assert.equal(await page.locator('#base').textContent(), '20,00 - 30,00 EUR');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true, 'Budget must fit mobile width');
    await page.locator('#fog-add').click();
    await page.waitForFunction(() => document.querySelectorAll('fieldset.item').length === 7);
    assert.equal(await page.locator('#base').textContent(), '350,00 - 535,00 EUR');
    await page.locator('#fog-add').click();
    await page.waitForFunction(() => document.querySelector('#message').textContent.includes('bereits vorhanden'));
    assert.equal(await page.locator('fieldset.item').count(), 7);
    await page.screenshot({path: path.join(output, 'budget-mobile.png'), fullPage: true});

    await page.goto(base + '/web/products/');
    await page.locator('.card').first().waitFor();
    assert.equal(await page.locator('.card').count(), 52);
    await page.locator('#category').selectOption('fog');
    assert.equal(await page.locator('.card').count(), 7);
    await page.locator('#search').fill('PMI');
    assert.equal(await page.locator('.card').count(), 6);
    await page.locator('#reset').click();
    await page.locator('#search').fill('Noctua');
    assert.equal(await page.locator('.card').count(), 1);
    assert.match(await page.locator('.links a').last().getAttribute('rel'), /sponsored/);
    await page.locator('[data-add="fan"]').click();
    await page.locator('[data-qty="fan"]').fill('2');
    await page.locator('[data-qty="fan"]').blur();
    const selection = await downloadJSON(page, '#export-json');
    assert.equal(selection.items[0].qty, 2);
    assert.equal(selection.items[0].price_eur, null);
    await page.locator('#clear').click();
    await page.locator('#file').setInputFiles({name:'Merklist.json', mimeType:'application/json', buffer:Buffer.from(JSON.stringify(selection))});
    await page.waitForFunction(() => document.querySelector('[data-qty="fan"]')?.value === '2');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true, 'Catalog must fit mobile width');
    await page.screenshot({path:path.join(output, 'products-mobile.png'), fullPage:true});
    await page.setViewportSize({width:1440, height:1000});
    await page.locator('#reset').click();
    await page.locator('#category').selectOption('helmet');
    await page.screenshot({path:path.join(output, 'products-desktop.png'), fullPage:true});
    await page.goto(base + '/web/products/?guide=Documentation%2FGuides%2FMjolnir-Nebeltechnik.md');
    assert.equal(await page.locator('.card').count(), 6);
    assert.equal(await page.locator('.selected-item').count(), 0, 'Catalog does not silently persist selection');
    await page.locator('#search').fill('does-not-exist');
    assert.equal(await page.locator('#empty').isVisible(), true);
    await page.locator('#reset').click();
    assert.equal(await page.locator('.card').count(), 52);

    // Main page: markdown parser and sanitizer are served from web/vendor, the other CDNs are stubbed.
    await page.route('https://cdn.tailwindcss.com**', route => route.fulfill({body:'', contentType:'application/javascript'}));
    await page.route('https://fonts.googleapis.com/**', route => route.fulfill({body:'', contentType:'text/css'}));
    await page.goto(base + '/web/index.html#Documentation/Guides/Mjolnir-Nebeltechnik.md');
    await page.locator('.catalog-context').waitFor();
    assert.equal(await page.locator('.catalog-context li').count(), 6);
    await page.locator('.catalog-context a.btn').click();
    await page.locator('.card').first().waitFor();
    assert.equal(await page.locator('.card').count(), 6);
    await page.goto(base + '/web/index.html#Materials/Einkaufsliste-Links.md');
    await page.locator('#doc a[rel~="sponsored"]').first().waitFor();
    assert.match(await page.locator('#doc a[rel~="sponsored"]').first().textContent(), /Affiliate/);
    assert.equal(await page.locator('#doc a[href*="pololu.com"]').getAttribute('rel'), 'noopener noreferrer');
    await page.route('https://unpkg.com/**', route => route.abort());
    await page.goto(base + '/web/index.html#3d-viewer');
    await page.waitForFunction(() => document.querySelector('#mv-banner')?.textContent.includes('konnte nicht geladen'));
    await page.locator('.part-row[data-id="hud"]').click();
    assert.match(await page.locator('#part-panel').textContent(), /XREAL One Pro/);
    await page.locator('#part-panel a[href="products/?part=hud"]').click();
    await page.locator('.card').first().waitFor();
    assert.equal(await page.locator('.card').count(), 3);
    await page.goto(base + '/web/index.html#product-catalog');
    await page.waitForURL('**/web/products/');

    // Rendered Markdown is untrusted: nothing in a guide may execute or restyle the page.
    const hostile = ['# Titel', '## Abschnitt Zwei', '<img src="x" onerror="window.__xss=1">', '<script>window.__xss=2</script>',
      '[klick](javascript:window.__xss=3)', '<a href="https://example.org/" onclick="window.__xss=4" id="search" style="position:fixed">extern</a>',
      '<iframe src="https://example.org/"></iframe>', '<form action="https://example.org/"><input type="text" name="q"><button>go</button></form>',
      '<svg><script>window.__xss=5</script></svg>', '<style>#doc{display:none}</style>', '- [ ] Aufgabe', '| A | B |\n| --- | --- |\n| 1 | 2 |',
      '[nach unten](#ziel-ganz-unten)', '[anderer Guide](Mjolnir-Nebeltechnik.md#grenzen)', '[raus](../../../../etc/passwd)',
      ...Array.from({length: 80}, (_, index) => 'Zeile ' + index), '## Ziel ganz unten', 'Ende'].join('\n\n');
    await page.route('**/Documentation/Guides/Xss-Fixture.md', route => route.fulfill({body: hostile, contentType: 'text/markdown'}));
    await page.setViewportSize({width: 1440, height: 700});
    await page.goto(base + '/web/index.html#Documentation/Guides/Xss-Fixture.md');
    await page.locator('#doc h1').waitFor();
    await page.waitForTimeout(300);
    assert.equal(await page.evaluate(() => window.__xss), undefined, 'No script from a guide runs');
    assert.equal(await page.locator('#doc script, #doc iframe, #doc form, #doc style, #doc button, #doc input:not([type="checkbox"])').count(), 0);
    assert.equal(await page.locator('#doc [onerror], #doc [onclick], #doc [style]').count(), 0);
    assert.equal(await page.locator('#search').evaluate(node => node.tagName), 'INPUT', 'Guide content cannot take over page ids');
    assert.equal(await page.locator('#doc').isVisible(), true);
    assert.equal(await page.locator('#doc a', {hasText: 'klick'}).getAttribute('href'), null);
    assert.equal(await page.locator('#doc a', {hasText: 'extern'}).getAttribute('rel'), 'noopener noreferrer');
    assert.equal(await page.locator('#doc input[type="checkbox"]').isEnabled(), true);
    assert.equal(await page.locator('#doc table td').count(), 2);
    assert.equal(await page.locator('#doc a', {hasText: 'anderer Guide'}).getAttribute('href'), '#Documentation/Guides/Mjolnir-Nebeltechnik.md#grenzen');
    assert.doesNotMatch(await page.locator('#doc a', {hasText: 'raus'}).getAttribute('href'), /\.\.\/\.\.\/\.\./);
    // Section links scroll inside the guide instead of routing to a missing document.
    assert.equal(await page.evaluate(() => scrollY), 0);
    await page.locator('#doc a', {hasText: 'nach unten'}).click();
    await page.waitForFunction(() => scrollY > 500);
    assert.equal(await page.locator('#doc h1').textContent(), 'Titel');
    assert.equal(await page.evaluate(() => location.hash), '#Documentation/Guides/Xss-Fixture.md#ziel-ganz-unten');
    await page.goto(base + '/web/index.html#README.md');
    await page.locator('#doc a[href$="#3a-neues-entwicklungsziel-ruestungslast-zum-boden"]').first().click();
    await page.waitForFunction(() => /Exoskelett/.test(document.querySelector('#doc h1')?.textContent || '') && scrollY > 500);
    // Malformed or escaping hashes show the not-found view instead of a blank page.
    for (const hash of ['#%', '#../../Other/x.md', '#https://example.org/x.md', '#unbekannte-ansicht']) {
      await page.goto(base + '/web/index.html');
      await page.evaluate(value => { location.hash = value; }, hash);
      await page.waitForFunction(() => document.querySelector('#doc h1')?.textContent === 'Nicht gefunden');
    }
    await page.setViewportSize({width: 390, height: 844});
    await page.goto(base + '/web/index.html#Documentation/Guides/Start-Hier.md');
    await page.locator('#doc h1').waitFor();
    assert.equal(await page.locator('#backdrop').evaluate(node => node.hasAttribute('onclick')), false);

    await page.goto(base + '/Code/Exhibition/');
    await page.locator('#demo').click();
    await page.locator('#project-file').setInputFiles({name: 'Suit-A.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(profile))});
    await page.waitForFunction(() => document.querySelector('#project-title').textContent === 'Suit-A');
    assert.equal(await page.locator('#status').textContent(), 'KEINE DATEN');
    await page.locator('#project-clear').click();
    assert.doesNotMatch(await page.locator('#project-title').textContent(), /Suit-A/);
    assert.deepEqual(errors, [], 'No uncaught browser errors');
    console.log('Browser smoke passed: profile isolation, persistence consent, schema-upgrade backup, JSON round trips, sanitized guides, section links, route validation, CSP, budget totals, mobile width, product filters/affiliate/selection export-import, exhibition reset.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });

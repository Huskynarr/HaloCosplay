'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const lib = require('../../web/products/products.js');
const data = require('../../web/products/catalog.js');

test('affiliate classification rejects spoofed hosts, credentials and duplicate tags', () => {
  const good = 'https://www.amazon.de/s?k=RGB&tag=huskynarr-21';
  assert.equal(lib.affiliate(good, 'huskynarr-21'), true);
  for (const url of [good.replace('amazon.de', 'amazon.de.evil.example'), good.replace('https:', 'http:'), good + '&tag=other-21', good.replace('www.', 'user:pass@www.'), good.replace('huskynarr', 'other'), 'javascript:alert(1)']) assert.equal(lib.affiliate(url, 'huskynarr-21'), false, url);
});
test('only affiliate links get sponsored and visible affiliate labels', () => {
  const p = data.products.find(p => p.id === 'fan');
  assert.match(lib.linkHTML(p.links[1], 'huskynarr-21'), /sponsored nofollow/);
  assert.match(lib.linkHTML(p.links[1], 'huskynarr-21'), /Affiliate/);
  assert.doesNotMatch(lib.linkHTML(p.links[0], 'huskynarr-21'), /sponsored|Affiliate/);
  assert.equal(lib.linkHTML({url:'javascript:alert(1)'}, 'huskynarr-21'), '');
});
test('search combines category, source, guides and normalized German queries', () => {
  assert(lib.filter(data, {q:'Lüfter', category:'comfort'}).some(p => p.id === 'fan'));
  assert.deepEqual(lib.filter(data, {product:'fan'}).map(p => p.id), ['fan']);
  assert.equal(lib.filter(data, {q:'impossible-not-a-product'}).length, 0);
  assert(lib.filter(data, {guide:'Documentation/Guides/Mjolnir-Nebeltechnik.md'}).every(p => p.category === 'fog'));
  assert(lib.filter(data, {source:'direct'}).every(p => p.links.some(l => l.kind !== 'search')));
});
test('selection export retains unknown prices and distinct product quantities', () => {
  const list = lib.selection(data, {fan:2, 'pmi-vest':1});
  assert.equal(list.items[0].qty, 2);
  assert.equal(list.items[0].price_eur, null);
  assert.equal(list.items[1].status, 'alternative');
  assert.equal(list.prices, 'unknown_not_quotes');
  assert.match(lib.csv(list), /"fan";"Noctua NF-A4x10 5V PWM";"2";""/);
  assert.throws(() => lib.selection(data, {fan:0}));
  assert.throws(() => lib.selection(data, {fan:1.5}));
  assert.throws(() => lib.selection(data, {missing:1}));
});
test('import is atomic and uses current catalog instead of imported URLs or prices', () => {
  const list = lib.selection(data, {fan:2});
  list.items[0].links = [{url:'javascript:alert(1)'}]; list.items[0].price_eur = 0;
  const imported = lib.importSelection(data, list);
  assert.equal(imported.fan, 2);
  const roundTrip = lib.selection(data, imported);
  assert.equal(roundTrip.items[0].price_eur, null);
  assert(roundTrip.items[0].links[0].url.startsWith('https:'));
  list.items.push(list.items[0]); assert.throws(() => lib.importSelection(data, list));
  assert.throws(() => lib.importSelection(data, {schema_version:1, kind:'budget',items:[]}));
});

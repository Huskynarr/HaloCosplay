/* Shared catalog logic: no network requests, no storage, no automatic purchases. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SuitProducts = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const status = {candidate: 'Kandidat', alternative: 'Option / Alternative', specification: 'Produktspezifikation offen'};
  function normalize(s) {
    return String(s).toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
  function escape(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c])); }
  function affiliate(url, tag) {
    try { const u = new URL(url); return u.protocol === 'https:' && !u.username && !u.password && !u.port && ['amazon.de', 'www.amazon.de'].includes(u.hostname) && u.searchParams.getAll('tag').length === 1 && u.searchParams.get('tag') === tag; } catch { return false; }
  }
  function linkHTML(link, tag) {
    let u;
    try { u = new URL(link.url); } catch { return ''; }
    if (u.protocol !== 'https:' || u.username || u.password) return '';
    const ad = affiliate(u.href, tag);
    const label = link.kind === 'search' ? (ad ? 'Amazon-Suche · Affiliate' : 'Shop-Suche') : link.label;
    return '<a href="' + escape(u.href) + '" target="_blank" rel="noopener noreferrer' + (ad ? ' sponsored nofollow' : '') + '">' + escape(label) + ' ↗</a>';
  }
  function filter(data, options = {}) {
    const terms = normalize(options.q || '').trim().split(/\s+/).filter(Boolean);
    return data.products.filter(p => (!options.category || p.category === options.category) &&
      (!options.status || p.status === options.status) && (!options.guide || p.guides.includes(options.guide)) &&
      (!options.part || p.parts.includes(options.part)) && (!options.product || p.id === options.product) &&
      (!options.source || p.links.some(l => options.source === 'direct' ? l.kind !== 'search' : l.kind === 'search')) &&
      terms.every(t => normalize([p.name, p.compatibility, p.category, data.categories.find(c => c.id === p.category)?.label || '', ...p.guides].join(' ')).includes(t)));
  }
  function selection(data, quantities) {
    const items = [];
    for (const [id, qty] of Object.entries(quantities)) {
      const p = data.products.find(p => p.id === id);
      if (!p || !Number.isSafeInteger(qty) || qty < 1 || qty > 999) throw new Error('Unbekanntes Produkt oder Menge ausserhalb 1 bis 999.');
      items.push({id, name: p.name, qty, price_eur: null, status: p.status, compatibility: p.compatibility, links: p.links});
    }
    return {schema_version: 1, kind: 'halo_product_selection', catalog_date: data.updated_on, currency: 'EUR', prices: 'unknown_not_quotes', items};
  }
  function importSelection(data, input) {
    if (!input || input.schema_version !== 1 || input.kind !== 'halo_product_selection' || !Array.isArray(input.items) || input.items.length > data.products.length) throw new Error('Keine gueltige Katalog-Merkliste.');
    const quantities = Object.create(null);
    for (const item of input.items) {
      if (!item || typeof item.id !== 'string' || Object.hasOwn(quantities, item.id)) throw new Error('Ungueltige oder doppelte Produktkennung.');
      quantities[item.id] = item.qty;
    }
    selection(data, quantities); // Ignore imported URLs/text/prices; use only trusted catalog data.
    return quantities;
  }
  function csv(list) {
    const cell = v => '"' + String(v ?? '').replace(/^[=+@-]/, "'$&").replace(/"/g, '""') + '"';
    const rows = [['ID', 'Produkt', 'Menge', 'Preis EUR (offen)', 'Status', 'Kompatibilitaet', 'Quellen']];
    list.items.forEach(p => rows.push([p.id, p.name, p.qty, '', status[p.status], p.compatibility, p.links.map(l => l.url).join(' | ')]));
    return '\uFEFF' + rows.map(row => row.map(cell).join(';')).join('\r\n') + '\r\n';
  }
  return {status, normalize, escape, affiliate, linkHTML, filter, selection, importSelection, csv};
});

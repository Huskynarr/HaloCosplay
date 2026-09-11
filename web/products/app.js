(function () {
  'use strict';
  const $ = s => document.querySelector(s);
  const data = window.SuitProductData, lib = window.SuitProducts;
  if (!data || !lib) { $('#count').textContent = 'Katalog konnte nicht geladen werden. Einkaufsliste im Bauhandbuch verwenden.'; return; }
  const esc = lib.escape;
  let quantities = Object.create(null);
  let params = new URLSearchParams(location.search);
  const tag = data.affiliate.amazon_de_tag;
  $('#total').textContent = data.products.length;
  $('#catalog-date').textContent = 'Katalogstand ' + data.updated_on;
  $('#disclosure').textContent = 'Werbung / Affiliate: ' + data.affiliate.disclosure;
  data.categories.forEach(c => { const o = document.createElement('option'); o.value = c.id; o.textContent = c.label; $('#category').append(o); });
  function restoreFilters() {
    $('#search').value = params.get('q') || '';
    ['category', 'status', 'source'].forEach(key => { const select = $('#' + key); select.value = params.get(key) || ''; if (select.selectedIndex < 0) select.value = ''; });
  }
  function options() {
    return {q: $('#search').value, category: $('#category').value, status: $('#status').value, source: $('#source').value, guide: params.get('guide'), part: params.get('part'), product: params.get('product')};
  }
  function render() {
    const opts = options(), matches = lib.filter(data, opts);
    $('#count').textContent = matches.length + ' von ' + data.products.length + ' Eintraegen';
    $('#empty').hidden = matches.length !== 0;
    const context = [opts.guide && 'Anleitung: ' + opts.guide, opts.part && 'Ruestungsteil: ' + opts.part, opts.product && 'Produktauswahl: ' + opts.product].filter(Boolean);
    $('#context').hidden = !context.length;
    $('#context').textContent = context.join(' / ') + (context.length ? ' — Alle Eintraege ueber „Filter zuruecksetzen“.' : '');
    $('#cards').innerHTML = matches.map(p => '<article class="card' + (quantities[p.id] ? ' chosen' : '') + '" id="product-' + p.id + '"><span class="badge ' + p.status + '">' + esc(lib.status[p.status]) + '</span><h2>' + esc(p.name) + '</h2><p>' + esc(p.compatibility) + '</p><p class="quantity-note">Planungsmenge: ' + esc(p.quantity_note) + '</p><div class="links">' + p.links.map(l => lib.linkHTML(l, tag)).join('') + '</div><p class="verified">' + esc(p.links.filter(l => l.checked_on).map(l => 'Quelle geprueft: ' + l.checked_on).join(' / ') || (p.links.every(l => l.kind === 'search') ? 'Shop-Suche: konkretes Produkt noch auszuwaehlen.' : 'Quelle hinterlegt; erneute Quellenpruefung offen.')) + '</p><div class="guides">' + p.guides.map(g => '<a href="../index.html#' + esc(g) + '">' + esc(g.split('/').pop().replace('.md', '')) + '</a>').join('') + '</div><button class="add" type="button" data-add="' + p.id + '" aria-pressed="' + Boolean(quantities[p.id]) + '">' + (quantities[p.id] ? 'Aus Merkliste entfernen' : 'Zur Merkliste hinzufuegen') + '</button></article>').join('');
  }
  function renderSelection() {
    const entries = Object.entries(quantities);
    $('#selection-count').textContent = entries.length + ' Positionen · Preise offen';
    $('#selection-jump').textContent = 'Zur Merkliste · ' + entries.length;
    $('#selected').innerHTML = entries.map(([id, qty]) => { const p = data.products.find(p => p.id === id); return '<div class="selected-item"><strong>' + esc(p.name) + '</strong><div class="selected-row"><label>Menge<input type="number" min="1" max="999" step="1" value="' + qty + '" data-qty="' + id + '" aria-label="Menge ' + esc(p.name) + '"></label><button type="button" data-remove="' + id + '" aria-label="' + esc(p.name) + ' entfernen">Entfernen</button></div></div>'; }).join('');
    ['export-json', 'export-csv', 'clear'].forEach(id => { $('#' + id).disabled = !entries.length; });
  }
  function syncURL() {
    const opts = options();
    ['q', 'category', 'status', 'source'].forEach(key => opts[key] ? params.set(key, opts[key]) : params.delete(key));
    history.replaceState(null, '', location.pathname + (params.size ? '?' + params.toString() : ''));
    render();
  }
  $('#search').addEventListener('input', syncURL);
  ['category', 'status', 'source'].forEach(id => $('#' + id).addEventListener('change', syncURL));
  $('#reset').onclick = () => { params = new URLSearchParams(); restoreFilters(); syncURL(); };
  window.addEventListener('popstate', () => { params = new URLSearchParams(location.search); restoreFilters(); render(); });
  $('#cards').addEventListener('click', event => {
    const button = event.target.closest('[data-add]'); if (!button) return;
    const id = button.dataset.add;
    if (quantities[id]) delete quantities[id]; else quantities[id] = 1;
    render(); renderSelection();
    document.querySelector('[data-add="' + id + '"]').focus({preventScroll: true});
  });
  $('#selected').addEventListener('click', event => { const button = event.target.closest('[data-remove]'); if (button) { delete quantities[button.dataset.remove]; renderSelection(); render(); $('#selection-title').setAttribute('tabindex', '-1'); $('#selection-title').focus({preventScroll:true}); } });
  $('#selected').addEventListener('change', event => {
    const input = event.target.closest('[data-qty]'); if (!input) return;
    const value = Number(input.value);
    if (!Number.isInteger(value) || value < 1 || value > 999) { input.value = quantities[input.dataset.qty]; $('#message').textContent = 'Menge muss eine ganze Zahl von 1 bis 999 sein.'; return; }
    quantities[input.dataset.qty] = value; $('#message').textContent = '';
  });
  function download(name, content, type) {
    const url = URL.createObjectURL(new Blob([content], {type}));
    const a = document.createElement('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('#export-json').onclick = () => download('HaloCosplay-Einkaufsmerkliste.json', JSON.stringify(lib.selection(data, quantities), null, 2) + '\n', 'application/json');
  $('#export-csv').onclick = () => download('HaloCosplay-Einkaufsmerkliste.csv', lib.csv(lib.selection(data, quantities)), 'text/csv;charset=utf-8');
  $('#clear').onclick = () => { quantities = Object.create(null); render(); renderSelection(); $('#message').textContent = 'Auswahl geleert.'; };
  $('#import').onclick = () => $('#file').click();
  $('#file').onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      if (file.size > 1000000) throw new Error('Datei zu gross (maximal 1 MB).');
      const imported = JSON.parse(await file.text());
      const next = lib.importSelection(data, imported);
      quantities = next; render(); renderSelection();
      $('#message').textContent = 'Merkliste importiert. Produktinformationen stammen aus dem aktuellen Katalog.';
    } catch (error) { $('#message').textContent = 'Import fehlgeschlagen: ' + error.message; }
    finally { event.target.value = ''; }
  };
  restoreFilters(); render(); renderSelection();
})();

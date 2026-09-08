/* No persistence or external services; explicit JSON import/export only. */
(function () {
  'use strict';
  const api = window.SuitBudget;
  const element = id => document.getElementById(id);
  const money = new Intl.NumberFormat('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  const number = new Intl.NumberFormat('de-DE', {maximumFractionDigits: 3});
  let data = api.empty();
  let dirty = false;
  let revision = 0;
  let loadToken = 0;
  const numericInput = input => input.value.trim() === '' ? NaN : Number(input.value);

  function changed() { dirty = true; revision++; }

  function stillCurrent(start, token) {
    if (token !== loadToken) return false;
    if (start !== revision) {
      message('Ladevorgang verworfen: Die Liste wurde inzwischen bearbeitet. Die aktuellen Eingaben bleiben erhalten.');
      return false;
    }
    return true;
  }

  function message(text, error = false) {
    element('message').textContent = text;
    element('message').classList.toggle('error', error);
  }

  function recalculate() {
    try {
      const totals = api.calculate(data);
      const range = values => values.map(value => money.format(value)).join(' - ') + ' EUR';
      element('base').textContent = range(totals.base_eur);
      element('reserved').textContent = range(totals.with_reserve_eur);
      element('mass').textContent = number.format(totals.planned_worn_g / 1000) + ' kg';
      const difference = totals.planned_worn_g - data.wearable_target_g;
      element('comparison').textContent = data.items.length === 0 ? 'Noch keine Positionen.' : difference === 0 ?
        'Bekannte Planmasse entspricht dem Plan-Massenziel (' + number.format(data.wearable_target_g) + ' g).' :
        'Bekannte Planmasse: ' + number.format(Math.abs(difference)) + ' g ' + (difference > 0 ? 'ueber dem' : 'unter dem') + ' Plan-Massenziel (' + number.format(data.wearable_target_g) + ' g).';
      element('unknown').textContent = totals.unknown_worn_mass_ids.length ?
        'Getragene Planmasse unvollstaendig. Ohne Masseneintrag: ' + totals.unknown_worn_mass_ids.join(', ') + '. Diese Positionen sind nicht in der Massensumme enthalten.' : '';
      element('errors').textContent = '';
      element('export').disabled = false;
    } catch (error) {
      element('errors').textContent = error.message;
      ['base', 'reserved', 'mass'].forEach(id => {element(id).textContent = 'Eingaben pruefen';});
      element('comparison').textContent = '';
      element('unknown').textContent = '';
      element('export').disabled = true;
    }
  }

  function field(title, value, onChange, options = {}) {
    const label = document.createElement('label');
    label.textContent = title;
    const input = document.createElement('input');
    Object.assign(input, {type: options.type || 'text', value: value === null ? '' : value});
    if (options.key) input.dataset.field = options.key;
    if (options.type === 'number') {input.min = options.min || '0'; input.step = options.step || 'any';}
    if (options.placeholder) input.placeholder = options.placeholder;
    input.addEventListener('input', () => {onChange(input); changed(); recalculate();});
    label.appendChild(input);
    return label;
  }

  function render() {
    element('reserve').value = data.contingency_fraction * 100;
    element('target').value = data.wearable_target_g;
    element('excluded').value = data.excluded.join('\n');
    const container = element('items');
    container.replaceChildren();
    data.items.forEach((item, index) => {
      const row = document.createElement('fieldset');
      row.className = 'item';
      const legend = document.createElement('legend');
      legend.textContent = 'Position ' + (index + 1);
      row.appendChild(legend);
      const fields = document.createElement('div'); fields.className = 'fields';
      fields.append(field('ID', item.id, input => {item.id = input.value;}, {key: 'id'}),
        field('Bezeichnung', item.name, input => {item.name = input.value;}, {key: 'name'}),
        field('Anzahl', item.qty, input => {item.qty = numericInput(input);}, {type: 'number', min: '1', step: '1', key: 'qty'}));
      const costs = document.createElement('div'); costs.className = 'costs';
      costs.append(field('EUR je Einheit: von', item.unit_budget_eur[0], input => {item.unit_budget_eur[0] = numericInput(input);}, {type: 'number', key: 'price-low'}),
        field('EUR je Einheit: bis', item.unit_budget_eur[1], input => {item.unit_budget_eur[1] = numericInput(input);}, {type: 'number', key: 'price-high'}),
        field('Planmasse g je Einheit', item.unit_mass_target_g, input => {item.unit_mass_target_g = input.value.trim() === '' ? null : numericInput(input);}, {type: 'number', placeholder: 'unbekannt', key: 'mass'}));
      const actions = document.createElement('div'); actions.className = 'item-actions';
      const check = document.createElement('label'); check.className = 'check';
      const checkbox = document.createElement('input'); checkbox.type = 'checkbox'; checkbox.checked = item.worn;
      checkbox.dataset.field = 'worn';
      checkbox.addEventListener('change', () => {item.worn = checkbox.checked; changed(); recalculate();});
      check.append(checkbox, document.createTextNode('Wird getragen'));
      const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'remove'; remove.textContent = 'Entfernen';
      remove.setAttribute('aria-label', 'Position ' + (index + 1) + ' entfernen');
      remove.addEventListener('click', () => {data.items.splice(index, 1); changed(); render(); element('add').focus();});
      actions.append(check, remove);
      row.append(fields, costs, actions);
      container.appendChild(row);
    });
    element('empty').hidden = data.items.length > 0;
    recalculate();
  }

  function replace(next, origin) {
    data = next; dirty = false; revision++;
    element('origin').textContent = origin;
    render();
  }

  function mayReplace() {
    return !dirty || window.confirm('Nicht exportierte Aenderungen verwerfen und die Liste ersetzen?');
  }

  element('reserve').addEventListener('input', event => {data.contingency_fraction = numericInput(event.target) / 100; changed(); recalculate();});
  element('target').addEventListener('input', event => {data.wearable_target_g = numericInput(event.target); changed(); recalculate();});
  element('excluded').addEventListener('input', event => {data.excluded = event.target.value.split('\n').map(line => line.trim()).filter(Boolean); changed(); recalculate();});
  element('add').addEventListener('click', () => {
    data.items.push({id: api.nextId(data.items), name: 'Neue Position', qty: 1, unit_budget_eur: [0, 0], unit_mass_target_g: null, worn: true});
    changed(); render();
    element('items').lastElementChild.querySelectorAll('input')[1].focus();
  });
  element('new').addEventListener('click', () => {if (mayReplace()) {replace(api.empty(), 'Neue Stueckliste'); message('Leere Liste angelegt. Plan-Massenziel und Positionen festlegen.');}});
  element('sample').addEventListener('click', async () => {
    if (!mayReplace()) return;
    const start = revision, token = ++loadToken;
    element('sample').disabled = true;
    try {
      const response = await fetch('../../Materials/Mjolnir-BOM.json');
      if (!response.ok) throw new Error('Beispieldatei nicht erreichbar.');
      const next = api.parse(await response.text());
      if (!stillCurrent(start, token)) return;
      replace(next, 'KONZEPTBEISPIEL / eigene Budgetansaetze');
      message('Konzeptbeispiel geladen. Mengen, Planmassen und Budgetansaetze sind unbestaetigte Beispielwerte; sie sind fuer das eigene Projekt anzupassen.');
    } catch (error) {if (stillCurrent(start, token)) message(error.message + ' Alternativ die vorhandene JSON-Datei importieren. Fuer das Laden der Beispieldatei die Seite ueber einen lokalen HTTP-Server oeffnen.', true);}
    finally {element('sample').disabled = false;}
  });
  element('import').addEventListener('click', () => {element('file').click();});
  element('file').addEventListener('change', async event => {
    const file = event.target.files[0];
    if (!file) return;
    const start = revision, token = ++loadToken;
    try {
      if (file.size > 2 * 1024 * 1024) throw new Error('Datei ist groesser als 2 MiB.');
      const next = api.parse(await file.text());
      if (!stillCurrent(start, token)) return;
      if (!mayReplace()) return;
      replace(next, 'Import: ' + file.name);
      message('Stueckliste importiert. Preise und Massen werden weiterhin als Planwerte behandelt.');
    } catch (error) {if (stillCurrent(start, token)) message('Import abgebrochen: ' + error.message, true);}
    finally {event.target.value = '';}
  });
  element('export').addEventListener('click', () => {
    try {
      const url = URL.createObjectURL(new Blob([api.serialize(data)], {type: 'application/json'}));
      const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'Cosplay-BOM.local.json';
      document.body.appendChild(anchor); anchor.click(); anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      dirty = false;
      message('JSON-Download gestartet. Die Datei enthaelt Planwerte und kann wieder importiert werden.');
    } catch (error) {message(error.message, true);}
  });
  window.addEventListener('beforeunload', event => {if (dirty) {event.preventDefault(); event.returnValue = '';}});
  render();
}());

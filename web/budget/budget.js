/* Browser/Node module: planning allowances, never load or hardware approval. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.SuitBudget = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const numeric = value => typeof value === 'number' && Number.isFinite(value) && value >= 0;
  const text = value => typeof value === 'string' && value.trim().length > 0;

  function empty() {
    return {schema_version: 1, currency: 'EUR', status: 'planning_allowances_not_supplier_quotes',
      contingency_fraction: 0.2, wearable_target_g: 0, excluded: [], items: []};
  }

  function validate(data) {
    if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('Eine JSON-Stueckliste wird benoetigt.');
    if (data.schema_version !== 1 || data.currency !== 'EUR') throw new Error('Unterstuetzt werden Schema 1 und EUR.');
    if (!numeric(data.contingency_fraction) || data.contingency_fraction > 1) throw new Error('Reserve: 0 bis 100 Prozent eintragen.');
    if (!numeric(data.wearable_target_g)) throw new Error('Plan-Massenziel: eine Zahl ab 0 g eintragen.');
    if (!Array.isArray(data.excluded) || !data.excluded.every(text)) throw new Error('Ausschluesse muessen eine Liste nicht leerer Texte sein.');
    if (!Array.isArray(data.items)) throw new Error('Positionen muessen als Liste vorliegen.');
    const ids = new Set();
    data.items.forEach((item, index) => {
      const label = 'Position ' + (index + 1) + ': ';
      if (!item || typeof item !== 'object' || Array.isArray(item)) throw new Error(label + 'ungueltiges Format.');
      if (!text(item.id) || item.id !== item.id.trim() || ids.has(item.id)) throw new Error(label + 'eine eindeutige ID ohne aeussere Leerzeichen eintragen.');
      ids.add(item.id);
      if (!text(item.name)) throw new Error(label + 'Bezeichnung fehlt.');
      if (!Number.isSafeInteger(item.qty) || item.qty < 1) throw new Error(label + 'Anzahl muss eine positive ganze Zahl sein.');
      if (!Array.isArray(item.unit_budget_eur) || item.unit_budget_eur.length !== 2 || !item.unit_budget_eur.every(numeric) || item.unit_budget_eur[0] > item.unit_budget_eur[1]) throw new Error(label + 'Preisbereich muss aus zwei aufsteigenden Zahlen ab 0 bestehen.');
      if (typeof item.worn !== 'boolean') throw new Error(label + 'Getragen muss true oder false sein.');
      if (item.unit_mass_target_g !== null && !numeric(item.unit_mass_target_g)) throw new Error(label + 'Planmasse muss eine Zahl ab 0 oder null sein.');
    });
    return data;
  }

  function calculate(data) {
    validate(data);
    let low = 0, high = 0, mass = 0;
    const unknown = [];
    data.items.forEach(item => {
      low += item.qty * item.unit_budget_eur[0];
      high += item.qty * item.unit_budget_eur[1];
      if (item.worn) {
        if (item.unit_mass_target_g === null) unknown.push(item.id);
        else mass += item.qty * item.unit_mass_target_g;
      }
    });
    const reserved = [low, high].map(value => Math.round((value * (1 + data.contingency_fraction) + Number.EPSILON) * 100) / 100);
    if (![low, high, mass, ...reserved].every(Number.isFinite)) throw new Error('Summen sind zu gross; Eingaben reduzieren.');
    return {base_eur: [low, high], with_reserve_eur: reserved, planned_worn_g: mass,
      unknown_worn_mass_ids: unknown,
      mass_target_met_in_plan: unknown.length === 0 && mass <= data.wearable_target_g};
  }

  function parse(source) {
    let data;
    try { data = JSON.parse(source); } catch (_) { throw new Error('Die Datei enthaelt kein gueltiges JSON.'); }
    calculate(data);
    return data;
  }

  function serialize(data) {
    calculate(data);
    return JSON.stringify(data, null, 2) + '\n';
  }

  function nextId(items) {
    const ids = new Set(items.map(item => item.id));
    let number = 1;
    while (ids.has('P' + String(number).padStart(3, '0'))) number++;
    return 'P' + String(number).padStart(3, '0');
  }

  function appendModule(base, extra) {
    calculate(base); calculate(extra);
    const ids = new Set(base.items.map(item => item.id));
    if (extra.items.some(item => ids.has(item.id))) throw new Error('Modulposition bereits vorhanden. Bestehende Positionen bearbeiten.');
    const merged = JSON.parse(JSON.stringify(base));
    merged.items.push(...JSON.parse(JSON.stringify(extra.items)));
    // Base exclusions describe the full project; module-only exclusions do not.
    calculate(merged);
    return merged;
  }

  return {empty, validate, calculate, parse, serialize, nextId, appendModule};
}));

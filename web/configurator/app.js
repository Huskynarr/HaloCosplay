(function () {
  'use strict';
  const CORE = window.SuitProfile;
  const DATA_KEY = 'mjolnir:configurator:profiles:v1';
  const CONSENT_KEY = 'mjolnir:configurator:consent:v1';
  const MAX_BYTES = 1024 * 1024;
  const $ = id => document.getElementById(id);
  const LABELS = {
    none: 'Kein Nebel / Licht allein', 'pmi-cloud': 'PMI-Nebelmodul mit Originalfluid',
    external: 'Externe Nebelquelle am Stand', 'water-mist': 'Ultraschall-Wassernebel (Versuch)',
    'chief-infinite': 'Master Chief / Infinite / Mark VI GEN3',
    'mark-vii': 'Spartan / Mark VII GEN3', custom: 'Eigene Referenz',
    hybrid: 'Hybrid: Schaumstoff und Druck', foam: 'Schaumstoff', printed: '3D-Druck',
    wearable: 'Tragbares Cosplay', exhibition: 'Ausstellungsobjekt', both: 'Tragen und Ausstellen'
  };
  let schema, records = [], active = '', persistent = false;
  let fields = new Map();

  function current() { return records.find(record => record.id === active); }
  function message(text = '', error = false) {
    $('message').textContent = text;
    $('message').classList.toggle('error', error);
  }
  function id() {
    return typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2);
  }
  function dirty() { return records.some(record => record.dirty); }
  function add(profile) {
    if (records.length >= 100) throw new Error('Maximal 100 Profile pro Browser-Sitzung. Vorhandene Profile exportieren und entfernen.');
    const record = {id: id(), data: profile, dirty: false};
    records.push(record); active = record.id;
    render(); save();
  }
  function save() {
    if (!persistent) return;
    if (records.some(record => CORE.inspect(record.data, schema).errors.length)) {
      $('privacy').textContent = 'Mindestens ein Profil enthaelt Eingabefehler. Die letzte gueltige Browserkopie bleibt bestehen; aktuelle Aenderungen sind noch nicht gespeichert.';
      return;
    }
    try {
      const data = JSON.stringify({schema_version: 1, active, profiles: records.map(({id: key, data: profile}) => ({id: key, data: profile}))});
      if (data.length > MAX_BYTES) throw new Error('Profilsammlung zu gross.');
      localStorage.setItem(DATA_KEY, data);
      localStorage.setItem(CONSENT_KEY, 'yes');
      records.forEach(record => { record.dirty = false; });
      $('privacy').textContent = 'Aktuelle gueltige Profile werden nur in diesem Browser gespeichert. JSON-Export bleibt die portable Sicherung.';
    } catch (error) {
      $('privacy').textContent = 'Browser-Speicherung fehlgeschlagen. Aktuelle Eingaben bleiben nur im Arbeitsspeicher. JSON-Export verwenden.';
      message('Speichern nicht moeglich: ' + error.message, true);
    }
  }
  function restore() {
    try {
      if (localStorage.getItem(CONSENT_KEY) !== 'yes') return;
      const raw = localStorage.getItem(DATA_KEY);
      if (!raw || raw.length > MAX_BYTES) throw new Error('Browserkopie fehlt oder ist zu gross.');
      const saved = JSON.parse(raw);
      if (saved.schema_version !== 1 || !Array.isArray(saved.profiles) || !saved.profiles.length || saved.profiles.length > 100) throw new Error('Unbekanntes Speicherformat.');
      const ids = new Set();
      const restored = saved.profiles.map(record => {
        if (!record || typeof record.id !== 'string' || !/^[A-Za-z0-9-]{1,80}$/.test(record.id) || ids.has(record.id)) throw new Error('Ungueltige Profil-ID.');
        ids.add(record.id);
        return {id: record.id, data: CORE.imported(record.data, schema), dirty: false};
      });
      records = restored;
      active = ids.has(saved.active) ? saved.active : records[0].id;
      persistent = true; $('persist').checked = true;
      $('privacy').textContent = 'Zuvor aktivierte Browser-Speicherung ist eingeschaltet. Gespeicherte Profile wurden geladen.';
    } catch (error) {
      message('Browserkopie konnte nicht geladen werden; sie wurde nicht ueberschrieben. ' + error.message, true);
    }
  }
  function options(select, values, selected) {
    select.replaceChildren();
    values.forEach(([value, label]) => {
      const option = document.createElement('option'); option.value = value; option.textContent = label;
      select.appendChild(option);
    });
    select.value = selected;
  }
  function profileList() {
    options($('profiles'), records.map(record => [record.id, record.data.profile || '(Name fehlt)']), active);
  }
  function changed() {
    current().dirty = true;
    profileList(); summary(); save();
  }
  function numberField(container, key, definition, section) {
    const wrap = document.createElement('div'), label = document.createElement('label');
    const input = document.createElement('input'), hint = document.createElement('small'), error = document.createElement('small');
    const path = section + '.' + key, fieldId = section + '-' + key;
    label.htmlFor = fieldId; label.textContent = definition.label + ' (mm)';
    input.id = fieldId; input.type = 'number'; input.inputMode = 'decimal'; input.step = 'any';
    input.min = definition.min; input.max = definition.max; input.autocomplete = 'off';
    input.value = current().data[section][key] === null ? '' : current().data[section][key];
    hint.id = fieldId + '-hint'; hint.textContent = definition.min + '-' + definition.max + ' mm';
    error.id = fieldId + '-error'; error.className = 'field-error';
    input.setAttribute('aria-describedby', hint.id + ' ' + error.id);
    input.addEventListener('input', () => {
      const value = input.validity.badInput ? NaN : input.value === '' ? null : Number(input.value);
      if (section === 'measurements_mm') current().data = CORE.updateMeasurement(current().data, key, value, schema);
      else current().data[section][key] = value;
      changed();
    });
    wrap.append(label, input, hint, error); container.appendChild(wrap);
    fields.set(path, {input, error});
  }
  function render() {
    profileList(); fields = new Map();
    const profile = current().data;
    $('name').value = profile.profile;
    $('build').replaceChildren(); $('features').replaceChildren(); $('measurements').replaceChildren(); $('allowances').replaceChildren();
    Object.entries(schema.build_fields).forEach(([key, definition]) => {
      const label = document.createElement('label'), select = document.createElement('select');
      label.textContent = definition.label; select.id = 'build-' + key; label.htmlFor = select.id;
      options(select, definition.options.map(value => [value, LABELS[value] || value]), profile.build[key]);
      select.addEventListener('change', () => { current().data.build[key] = select.value; changed(); });
      label.appendChild(select); $('build').appendChild(label);
    });
    Object.entries(schema.feature_fields).forEach(([key, definition]) => {
      const label = document.createElement('label'), input = document.createElement('input'), span = document.createElement('span');
      label.className = 'check'; input.type = 'checkbox'; input.checked = profile.build.features[key]; input.id = 'feature-' + key;
      span.textContent = definition.label;
      input.addEventListener('change', () => { current().data.build.features[key] = input.checked; changed(); });
      label.append(input, span); $('features').appendChild(label);
    });
    const groups = new Map();
    Object.entries(schema.measurements).forEach(([key, definition]) => {
      if (!groups.has(definition.group)) {
        const fieldset = document.createElement('fieldset'), legend = document.createElement('legend'), grid = document.createElement('div');
        fieldset.className = 'measurement-group'; legend.textContent = definition.group; grid.className = 'fields';
        fieldset.append(legend, grid); $('measurements').appendChild(fieldset); groups.set(definition.group, grid);
      }
      numberField(groups.get(definition.group), key, definition, 'measurements_mm');
    });
    Object.entries(schema.allowances).forEach(([key, definition]) => numberField($('allowances'), key, definition, 'allowances_mm'));
    summary();
  }
  function guide(title, file) {
    const item = document.createElement('li'), link = document.createElement('a');
    link.textContent = title; link.href = '../index.html#' + file;
    item.appendChild(link); $('guides').appendChild(item);
  }
  function summary() {
    const profile = current().data, report = CORE.inspect(profile, schema), total = Object.keys(schema.measurements).length;
    const valid = Object.entries(schema.measurements).filter(([key, range]) => {
      const value = profile.measurements_mm[key];
      return typeof value === 'number' && Number.isFinite(value) && value >= range.min && value <= range.max;
    }).length;
    $('count').textContent = valid + ' / ' + total;
    $('progress').max = total; $('progress').value = valid;
    $('kind').textContent = profile.status === 'synthetic' ? 'SYNTHETISCHE DEMO' : profile.status === 'measured' ? 'SELBSTAUSKUNFT' : 'MESSWERTE OFFEN';
    $('status-label').textContent = profile.status === 'synthetic' ? 'Demo: keine realen Koerpermasse.' : profile.status === 'measured' ? 'Messwerte als selbst gemessen gekennzeichnet.' : 'Messwerte noch nicht als vollstaendig gemessen gekennzeichnet.';
    $('missing-summary').textContent = report.missing.length + ' offene Messwerte; ' + report.errors.length + ' Eingabefehler.';
    $('missing').replaceChildren();
    report.missing.forEach(key => { const item = document.createElement('li'); item.textContent = schema.measurements[key].label; $('missing').appendChild(item); });
    if (!report.missing.length) { const item = document.createElement('li'); item.textContent = 'Keine leeren Messfelder. Eingabefehler und Messherkunft gesondert beachten.'; $('missing').appendChild(item); }
    fields.forEach(({input, error}) => { input.setAttribute('aria-invalid', 'false'); error.textContent = ''; });
    $('name').setAttribute('aria-invalid', 'false'); $('errors').replaceChildren();
    report.errors.forEach(issue => {
      if (fields.has(issue.field)) { const field = fields.get(issue.field); field.input.setAttribute('aria-invalid', 'true'); field.error.textContent = issue.message; }
      if (issue.field === 'profile') $('name').setAttribute('aria-invalid', 'true');
      const p = document.createElement('p'); p.textContent = issue.message; $('errors').appendChild(p);
    });
    $('export').disabled = report.errors.length > 0;
    $('confirm').disabled = report.errors.length > 0 || report.missing.length > 0 || profile.status === 'synthetic' || profile.status === 'measured';
    $('guides').replaceChildren();
    guide('Messung und Passprobe', 'Documentation/Guides/Mjolnir-Massanpassung.md');
    guide(profile.build.material === 'foam' ? 'Schaumstoff konstruieren' : 'Schalen und Verbindungen ausarbeiten', profile.build.material === 'foam' ? 'Documentation/Guides/Foam-Bau.md' : 'Documentation/Guides/Mjolnir-Fertigung.md');
    guide('Konzept-CAD mit diesem Profil', 'Design/Parametric/README.md');
    if (profile.build.operating_mode !== 'exhibition') guide('Tragesystem und Einstieg', 'Documentation/Guides/Mjolnir-Einstieg.md');
    if (profile.build.operating_mode !== 'wearable') guide('Ausstellung und Vorfuehrbetrieb', 'Documentation/Guides/Mjolnir-Messebetrieb.md');
    if (profile.build.features.exoskeleton) guide('Exoskelett separat anpassen', 'Documentation/Guides/Exoskelett.md');
    if (profile.build.features.hud) guide('HUD und Sichtfeld planen', 'Documentation/Guides/Elektronik-HUD.md');
    if (profile.build.fog_system !== 'none') guide('Nebelmodul, Einkauf und Pruefung', 'Documentation/Guides/Elektronik-Schubduesen.md');
    if (profile.build.features.lighting || profile.build.features.audio) guide('Elektronik und Strombudget', 'Documentation/Guides/Mjolnir-Elektronik.md');
  }
  async function json(url) {
    const response = await fetch(url, {credentials: 'omit'});
    if (!response.ok) throw new Error('Datei nicht erreichbar: ' + url + ' (HTTP ' + response.status + ')');
    return response.json();
  }
  function events() {
    $('profiles').addEventListener('change', () => { active = $('profiles').value; render(); save(); });
    $('name').addEventListener('input', () => { current().data.profile = $('name').value; changed(); });
    $('new').addEventListener('click', () => {
      try { add(CORE.create(schema, 'Profil-' + (records.length + 1))); message('Leeres Profil angelegt. Alle Koerpermasse sind unbekannt.'); }
      catch (error) { message(error.message, true); }
    });
    $('demo').addEventListener('click', async () => {
      $('demo').disabled = true;
      try {
        const profile = CORE.imported(await json('../../Design/Parametric/Profiles/Demo.json'), schema);
        if (profile.status !== 'synthetic') throw new Error('Die Demoquelle ist nicht als synthetisch gekennzeichnet.');
        add(profile); message('Synthetisches Demoprofil geladen. Fuer reale Messwerte ein leeres Profil anlegen.');
      } catch (error) { message(error.message, true); }
      finally { $('demo').disabled = false; }
    });
    $('import').addEventListener('click', () => $('file').click());
    $('file').addEventListener('change', async () => {
      const file = $('file').files[0];
      if (!file) return;
      try {
        if (file.size > MAX_BYTES) throw new Error('JSON-Datei ist groesser als 1 MiB.');
        add(CORE.imported(JSON.parse(await file.text()), schema)); message('Profil importiert. Vorhandene Profile bleiben erhalten.');
      } catch (error) { message('Import abgebrochen: ' + error.message, true); }
      finally { $('file').value = ''; }
    });
    $('export').addEventListener('click', () => {
      try {
        const profile = CORE.imported(current().data, schema);
        const blob = new Blob([JSON.stringify(profile, null, 2) + '\n'], {type: 'application/json'});
        const url = URL.createObjectURL(blob), link = document.createElement('a');
        link.href = url; link.download = profile.profile.replace(/ /g, '-') + '.local.json';
        document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
        current().dirty = false; message('Download gestartet: ' + link.download + '. Das Profil enthaelt die eingetragenen Koerpermasse.');
      } catch (error) { message(error.message, true); }
    });
    $('confirm').addEventListener('click', () => {
      try { current().data = CORE.confirmMeasurements(current().data, schema); changed(); message('Messherkunft gekennzeichnet. Eine Aenderung an den Messwerten setzt diese Kennzeichnung zurueck.'); }
      catch (error) { message(error.message, true); }
    });
    $('delete').addEventListener('click', () => {
      if (!window.confirm('Aktives Profil aus dieser Sitzung und gegebenenfalls der Browserkopie entfernen? Exportierte Dateien bleiben erhalten.')) return;
      records = records.filter(record => record.id !== active);
      if (!records.length) add(CORE.create(schema));
      else { active = records[0].id; render(); save(); }
      message('Profil entfernt.');
    });
    $('persist').addEventListener('change', () => {
      persistent = $('persist').checked;
      if (persistent) save();
      else {
        try { localStorage.removeItem(DATA_KEY); localStorage.removeItem(CONSENT_KEY); message('Browserkopie entfernt. Aktuelle Profile bleiben bis zum Neuladen im Arbeitsspeicher.'); }
        catch (error) { message('Browserkopie konnte nicht entfernt werden. Website-Daten in den Browser-Einstellungen loeschen.', true); }
        records.forEach(record => { record.dirty = true; });
        $('privacy').textContent = 'Nur Arbeitsspeicher: Eingaben gehen beim Neuladen verloren. JSON-Export sichert das aktive Profil.';
      }
    });
    window.addEventListener('beforeunload', event => { if (dirty()) { event.preventDefault(); event.returnValue = ''; } });
  }
  async function start() {
    try {
      schema = await json('../../Design/Parametric/ProfileSchema.json');
      message(''); restore();
      if (!records.length) records.push({id: id(), data: CORE.create(schema), dirty: false});
      if (!active) active = records[0].id;
      events(); render(); $('workspace').hidden = false;
    } catch (error) {
      message('Konfigurator konnte nicht starten. Das Repository ueber einen lokalen HTTP-Server oder GitHub Pages oeffnen; file:// unterstuetzt das Nachladen des Schemas nicht. ' + error.message, true);
    }
  }
  start();
}());

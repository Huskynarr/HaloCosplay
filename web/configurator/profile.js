/* Shared by the browser and Node tests. No storage, DOM or network access. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SuitProfile = factory();
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const NAME = /^[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}$/;
  const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  // Preserve invalid numeric drafts until validation; JSON cloning would turn
  // NaN into null and silently convert an input error into an unknown value.
  const clone = value => Array.isArray(value) ? value.map(clone) : object(value) ? Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, clone(entry)])) : value;

  function create(schema, name = 'Neues-Profil') {
    const measurements = {}, allowances = {}, build = {features: {}};
    Object.keys(schema.measurements).forEach(key => { measurements[key] = null; });
    Object.entries(schema.allowances).forEach(([key, field]) => { allowances[key] = field.default; });
    Object.entries(schema.build_fields).forEach(([key, field]) => { build[key] = field.default; });
    Object.entries(schema.feature_fields).forEach(([key, field]) => { build.features[key] = field.default; });
    return {schema_version: 1, profile: name, status: 'measurements_pending', measurements_mm: measurements, allowances_mm: allowances, build};
  }

  function inspect(profile, schema) {
    const errors = [], missing = [];
    const issue = (field, message) => errors.push({field, message});
    if (!object(profile)) return {errors: [{field: 'profile', message: 'Das Profil muss ein JSON-Objekt sein.'}], missing};
    if (profile.schema_version !== 1) issue('schema_version', 'Unterstuetzt wird schema_version 1.');
    if (typeof profile.profile !== 'string' || !NAME.test(profile.profile) || profile.profile.trim() !== profile.profile) {
      issue('profile', 'Profilname: 1-64 ASCII-Zeichen, Beginn mit Buchstabe oder Zahl; danach auch Leerzeichen, Punkt, Unterstrich und Bindestrich.');
    }
    if (!['measurements_pending', 'synthetic', 'measured'].includes(profile.status)) issue('status', 'Unbekannter Messstatus.');
    function values(key, fields, nullable) {
      const source = profile[key];
      if (!object(source)) { issue(key, key + ' fehlt oder ist kein Objekt.'); return; }
      Object.keys(source).forEach(field => { if (!own(fields, field)) issue(key + '.' + field, 'Unbekanntes Feld: ' + field); });
      Object.entries(fields).forEach(([field, definition]) => {
        const path = key + '.' + field;
        if (!own(source, field)) { issue(path, definition.label + ': Feld fehlt im Profil.'); return; }
        const value = source[field];
        if (nullable && value === null) { missing.push(field); return; }
        if (typeof value !== 'number' || !Number.isFinite(value) || value < definition.min || value > definition.max) {
          issue(path, definition.label + ': Zahl zwischen ' + definition.min + ' und ' + definition.max + ' mm erforderlich.');
        }
      });
    }
    values('measurements_mm', schema.measurements, true);
    values('allowances_mm', schema.allowances, false);
    if (object(profile.measurements_mm)) {
      const measurements = profile.measurements_mm;
      const numeric = value => typeof value === 'number' && Number.isFinite(value);
      Object.entries(measurements).forEach(([key, value]) => {
        if (key !== 'height' && numeric(value) && numeric(measurements.height) && value >= measurements.height) issue('measurements_mm.' + key, 'Messwert muss kleiner als die Koerpergroesse sein.');
      });
      if (numeric(measurements.chest_width) && numeric(measurements.shoulder_width) && measurements.chest_width > measurements.shoulder_width + 120) issue('measurements_mm.chest_width', 'Brust-/Schulterbreite: Messdefinition pruefen.');
      const edge = object(profile.allowances_mm) ? profile.allowances_mm.edge_clearance : null;
      if (numeric(edge)) {
        Object.entries(measurements).forEach(([key, value]) => {
          if ((key === 'torso_length' || /^(upperarm|forearm|thigh|shin)_length_[lr]$/.test(key)) && numeric(value) && value <= 2 * edge) issue('measurements_mm.' + key, 'Laenge muss groesser als der doppelte Randabstand sein.');
        });
      }
    }
    if (profile.status === 'measured' && missing.length) issue('status', 'Als gemessen markierte Profile benoetigen alle Messwerte.');
    if (own(profile, 'build')) {
      if (!object(profile.build)) issue('build', 'Baukonfiguration muss ein Objekt sein.');
      else {
        Object.keys(profile.build).forEach(key => {
          if (key !== 'features' && !own(schema.build_fields, key)) issue('build.' + key, 'Unbekannte Bauoption: ' + key);
        });
        Object.entries(schema.build_fields).forEach(([key, field]) => {
          if (own(profile.build, key) && !field.options.includes(profile.build[key])) issue('build.' + key, field.label + ': unbekannte Auswahl.');
        });
        if (own(profile.build, 'features')) {
          if (!object(profile.build.features)) issue('build.features', 'Ausstattung muss ein Objekt sein.');
          else Object.keys(profile.build.features).forEach(key => {
            if (!own(schema.feature_fields, key) || typeof profile.build.features[key] !== 'boolean') issue('build.features.' + key, 'Ausstattung muss bekannte Optionen mit true oder false enthalten.');
          });
        }
      }
    }
    return {errors, missing};
  }

  function imported(value, schema) {
    const checked = inspect(value, schema);
    if (checked.errors.length) throw new Error(checked.errors.map(error => error.message).join('\n'));
    const profile = clone(value), defaults = create(schema);
    profile.build = {...defaults.build, ...profile.build, features: {...defaults.build.features, ...(profile.build && profile.build.features)}};
    return profile;
  }

  function updateMeasurement(profile, key, value, schema) {
    if (!own(schema.measurements, key)) throw new Error('Unbekanntes Messfeld.');
    const next = clone(profile);
    next.measurements_mm[key] = value;
    if (next.status === 'measured' && value !== profile.measurements_mm[key]) next.status = 'measurements_pending';
    return next;
  }

  function confirmMeasurements(profile, schema) {
    const report = inspect(profile, schema);
    if (profile.status === 'synthetic') throw new Error('Ein Demoprofil bleibt synthetisch. Fuer echte Messwerte ein leeres Profil anlegen.');
    if (report.errors.length || report.missing.length) throw new Error('Zuerst alle Messwerte vollstaendig und gueltig eintragen.');
    return {...clone(profile), status: 'measured'};
  }

  return {create, inspect, imported, updateMeasurement, confirmMeasurements};
}));

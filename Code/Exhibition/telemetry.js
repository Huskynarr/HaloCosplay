/* Pure validation shared by the offline display and Node tests. */
(function (root) {
  'use strict';
  function validate(data, now) {
    if (!data || data.schema_version !== 1 || !['measured', 'demo'].includes(data.source)) throw Error('Format oder Datenquelle ungueltig');
    if (typeof data.timestamp !== 'string' || !/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(data.timestamp)) throw Error('Zeitstempel mit Zeitzone erforderlich');
    const time = Date.parse(data.timestamp);
    if (!Number.isFinite(time) || time > now) throw Error('Zeitstempel ungueltig oder zukuenftig');
    if (typeof data.device !== 'string' || !data.device.trim() || data.device.length > 100) throw Error('Geraet fehlt');
    const fields = {battery_pct: [0, 100], temperature_c: [-40, 125], fan_rpm: [0, 50000]};
    const values = {};
    for (const [key, range] of Object.entries(fields)) {
      const v = data[key];
      if (v !== null && (typeof v !== 'number' || !Number.isFinite(v) || v < range[0] || v > range[1])) throw Error('Ungueltiger Messwert: ' + key);
      values[key] = v;
    }
    return {source: data.source, device: data.device, time, values};
  }
  function state(sample, now) {
    if (!sample) return {label: 'KEINE DATEN', values: null};
    if (sample.source === 'demo') return {label: 'BEISPIELDATEN - SIMULATION', values: sample.values};
    if (now < sample.time || now - sample.time > 10000) return {label: 'MESS-SNAPSHOT VERALTET', values: null};
    return {label: 'MESS-SNAPSHOT - NICHT LIVE', values: sample.values};
  }
  const api = {validate, state};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.HaloTelemetry = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);

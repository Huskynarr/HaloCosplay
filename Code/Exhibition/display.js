'use strict';
let sample = null;
let generation = 0;
const el = id => document.getElementById(id);
function paint() {
  const view = HaloTelemetry.state(sample, Date.now());
  el('status').textContent = view.label;
  el('origin').textContent = sample ? sample.device + ' | ' + new Date(sample.time).toISOString() : 'Keine Sensorverbindung eingerichtet.';
  for (const [id, key, unit] of [['battery','battery_pct',' %'],['temperature','temperature_c',' C'],['fan','fan_rpm',' rpm']]) {
    el(id).textContent = view.values && view.values[key] !== null ? view.values[key] + unit : '--';
  }
}
el('clear').onclick = () => { generation++; sample = null; el('error').textContent = ''; el('file').value = ''; paint(); };
el('demo').onclick = () => {
  generation++;
  sample = HaloTelemetry.validate({schema_version:1,source:'demo',device:'Synthetischer Beispieldatensatz',timestamp:new Date().toISOString(),battery_pct:72,temperature_c:28,fan_rpm:1800}, Date.now());
  el('error').textContent = ''; paint();
};
el('file').onchange = async event => {
  const token = ++generation;
  sample = null; el('error').textContent = ''; paint();
  try {
    const file = event.target.files[0];
    if (!file) return;
    if (file.size > 16384) throw Error('Datei groesser als 16 KiB');
    const text = await file.text();
    if (token !== generation) return;
    sample = HaloTelemetry.validate(JSON.parse(text), Date.now());
  } catch (error) {
    if (token !== generation) return;
    sample = null; el('error').textContent = error.message;
  }
  paint();
};
setInterval(paint, 1000);
paint();

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
function clearTelemetry() {
  generation++; sample = null; el('error').textContent = ''; el('file').value = ''; paint();
}
el('clear').onclick = clearTelemetry;
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

let projectGeneration = 0;
function clearProject() {
  el('project-title').textContent = 'MJOLNIR - Mechanik zum Anziehen.';
  el('project-summary').textContent = 'Konfigurierbare Ruestungsreferenz und Module. Ein Projektprofil kann fuer die Beschriftung geladen werden.';
}
el('project-clear').onclick = () => {
  projectGeneration++; clearProject(); el('project-file').value = ''; el('project-error').textContent = '';
  clearTelemetry();
};
el('project-file').onchange = async event => {
  const token = ++projectGeneration;
  clearProject(); el('project-error').textContent = '';
  clearTelemetry();
  try {
    const file = event.target.files[0];
    if (!file) return;
    if (file.size > 65536) throw Error('Projektprofil groesser als 64 KiB');
    const text = await file.text();
    if (token !== projectGeneration) return;
    const project = HaloProject.metadata(JSON.parse(text));
    el('project-title').textContent = project.title;
    el('project-summary').textContent = project.summary;
  } catch (error) {
    if (token !== projectGeneration) return;
    clearProject(); el('project-error').textContent = error.message;
  } finally {
    // Snapshots started during this import cannot be assigned to the new title.
    // An obsolete import must not clear data belonging to a later project.
    if (token === projectGeneration) clearTelemetry();
  }
};

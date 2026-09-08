const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const HaloTelemetry = require('../../Code/Exhibition/telemetry.js');
const HaloProject = require('../../Code/Exhibition/project.js');

function fixture() {
  const elements = new Map();
  const el = id => {
    if (!elements.has(id)) elements.set(id, {textContent:'', value:''});
    return elements.get(id);
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../../Code/Exhibition/display.js'), 'utf8'), {
    document:{getElementById:el}, HaloTelemetry, HaloProject, Date, JSON, setInterval:()=>{}
  });
  const event = text => ({target:{files:[{size:100, text:async()=>text}]}});
  const project = title => JSON.stringify({schema_version:1,profile:title,
    build:{armor_reference:'custom',material:'foam',operating_mode:'wearable'}});
  const snapshot = device => JSON.stringify({schema_version:1,source:'measured',device,
    timestamp:new Date().toISOString(),battery_pct:50,temperature_c:25,fan_rpm:1000});
  return {el, event, project, snapshot};
}
function deferred() {
  let resolve;
  const promise = new Promise(done => { resolve = done; });
  return {promise, resolve};
}

test('project import completion clears snapshots imported while the profile was loading', async () => {
  for (const valid of [true, false]) {
    const {el,event,project,snapshot} = fixture(), pending = deferred();
    const loading = el('project-file').onchange(event(pending.promise));
    await el('file').onchange(event(snapshot('Device-of-A')));
    assert.equal(el('battery').textContent, '50 %');
    pending.resolve(valid ? project('Project-B') : '{invalid');
    await loading;
    assert.equal(el('battery').textContent, '--');
    assert.equal(el('status').textContent, 'KEINE DATEN');
    assert.doesNotMatch(el('origin').textContent, /Device-of-A/);
    if (valid) assert.equal(el('project-title').textContent, 'Project-B');
    else assert.notEqual(el('project-error').textContent, '');
  }
});

test('snapshot still loading when a project completes cannot repopulate telemetry', async () => {
  const {el,event,project,snapshot} = fixture(), pendingProject = deferred(), pendingSample = deferred();
  const loadingProject = el('project-file').onchange(event(pendingProject.promise));
  const loadingSample = el('file').onchange(event(pendingSample.promise));
  pendingProject.resolve(project('Project-B'));
  await loadingProject;
  pendingSample.resolve(snapshot('Device-of-A'));
  await loadingSample;
  assert.equal(el('project-title').textContent, 'Project-B');
  assert.equal(el('status').textContent, 'KEINE DATEN');
});

test('obsolete project import cannot remove snapshots loaded for a newer project', async () => {
  const {el,event,project,snapshot} = fixture(), pendingOld = deferred();
  const oldImport = el('project-file').onchange(event(pendingOld.promise));
  await el('project-file').onchange(event(project('Project-C')));
  await el('file').onchange(event(snapshot('Device-of-C')));
  pendingOld.resolve(project('Project-B'));
  await oldImport;
  assert.equal(el('project-title').textContent, 'Project-C');
  assert.match(el('origin').textContent, /Device-of-C/);
  assert.equal(el('battery').textContent, '50 %');
});

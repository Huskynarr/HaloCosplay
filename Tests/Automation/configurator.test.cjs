const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const core = require('../../web/configurator/profile.js');
const schema = require('../../Design/Parametric/ProfileSchema.json');
const template = require('../../Design/Parametric/Profiles/Template.json');
const demo = require('../../Design/Parametric/Profiles/Demo.json');
const copy = value => JSON.parse(JSON.stringify(value));

test('new profiles start with every measurement unknown, including height', () => {
  const profile = core.create(schema, 'Test-01');
  assert.equal(Object.keys(profile.measurements_mm).length, 32);
  assert.ok(Object.values(profile.measurements_mm).every(value => value === null));
  assert.deepEqual(profile.measurements_mm, template.measurements_mm);
  assert.deepEqual(profile.allowances_mm, template.allowances_mm);
  assert.deepEqual(profile.build, template.build);
  assert.equal(core.inspect(profile, schema).missing.length, 32);
  assert.equal(core.inspect(profile, schema).errors.length, 0);
});

test('profile edits are isolated, side-specific and preserve synthetic provenance', () => {
  const edited = core.updateMeasurement(demo, 'boot_width_l', 160, schema);
  assert.equal(edited.measurements_mm.boot_width_l, 160);
  assert.equal(edited.measurements_mm.boot_width_r, demo.measurements_mm.boot_width_r);
  assert.equal(edited.status, 'synthetic');
  assert.notEqual(demo.measurements_mm.boot_width_l, 160);
  assert.throws(() => core.confirmMeasurements(edited, schema), /Demoprofil/);
});

test('real measurement status requires explicit confirmation and resets after changed measurement', () => {
  const profile = {...copy(demo), status: 'measurements_pending'};
  assert.equal(core.imported(profile, schema).status, 'measurements_pending');
  const measured = core.confirmMeasurements(profile, schema);
  assert.equal(measured.status, 'measured');
  assert.equal(core.updateMeasurement(measured, 'height', measured.measurements_mm.height, schema).status, 'measured');
  assert.equal(core.updateMeasurement(measured, 'height', 1850, schema).status, 'measurements_pending');
  assert.throws(() => core.confirmMeasurements(core.create(schema), schema), /vollstaendig/);
});

test('strict import rejects wrong types, invalid bounds, unknown fields and false measurement status', () => {
  for (const value of [false, '1700', Infinity, NaN, 0, 2300]) {
    const profile = copy(demo); profile.measurements_mm.height = value;
    assert.throws(() => core.imported(profile, schema));
  }
  const unknown = copy(demo); unknown.measurements_mm.weight = 80;
  assert.throws(() => core.imported(unknown, schema), /Unbekanntes Feld/);
  const missing = copy(demo); delete missing.measurements_mm.height;
  assert.throws(() => core.imported(missing, schema), /Feld fehlt/);
  assert.throws(() => core.imported({...core.create(schema), status: 'measured'}, schema), /alle Messwerte/);
  for (const profile of [null, [], 'bad', {...demo, schema_version: true}, {...demo, status: 'approved'}]) assert.throws(() => core.imported(profile, schema));
});

test('cross-field validation catches impossible geometry before export', () => {
  const shoulder = copy(demo); shoulder.measurements_mm.shoulder_width = 200; shoulder.measurements_mm.chest_width = 650;
  assert.throws(() => core.imported(shoulder, schema), /Brust-/);
  const edge = copy(demo); edge.measurements_mm.upperarm_length_l = 100; edge.allowances_mm.edge_clearance = 60;
  assert.throws(() => core.imported(edge, schema), /Randabstand/);
});

test('editing another field preserves invalid numeric drafts instead of replacing them by null', () => {
  const broken = core.updateMeasurement(demo, 'height', NaN, schema);
  const next = core.updateMeasurement(broken, 'boot_width_l', 145, schema);
  assert.ok(Number.isNaN(next.measurements_mm.height));
  assert.ok(core.inspect(next, schema).errors.length);
});

test('legacy build defaults are normalized; unknown source metadata stays unchanged', () => {
  const legacy = copy(demo); delete legacy.build;
  legacy.reference_notes = {source: 'own measurement sheet', calibrated: false};
  const imported = core.imported(legacy, schema);
  assert.deepEqual(imported.build, template.build);
  assert.deepEqual(imported.reference_notes, legacy.reference_notes);
  imported.reference_notes.calibrated = true;
  assert.equal(legacy.reference_notes.calibrated, false);
});

test('build settings accept schema choices and reject malformed feature flags', () => {
  for (const [key, field] of Object.entries(schema.build_fields)) {
    for (const value of field.options) {
      const profile = copy(demo); profile.build[key] = value;
      assert.equal(core.imported(profile, schema).build[key], value);
    }
  }
  for (const build of [false, {material: 'carbon'}, {features: {hud: 'true'}}, {features: {motorized: true}}, {size: 'XL'}]) {
    assert.throws(() => core.imported({...copy(demo), build}, schema));
  }
});

test('profile names remain safe portable filenames', () => {
  for (const name of ['../secret', '<script>', '', ' leading', 'trailing ', 'x'.repeat(65), '\u00e4']) {
    assert.throws(() => core.imported({...demo, profile: name}, schema));
  }
  assert.equal(core.imported({...demo, profile: 'Spartan 04-A_2.0'}, schema).profile, 'Spartan 04-A_2.0');
});

test('browser export contract is accepted by Python with preserved provenance and configuration', () => {
  const profile = core.imported(demo, schema);
  profile.build = {...profile.build, armor_reference: 'mark-vii', material: 'foam', operating_mode: 'both', features: {exoskeleton: true, hud: false, lighting: true, audio: true}};
  const python = spawnSync('python3', ['-c', 'import json,sys; from tools.suit_fit import derive; p=json.load(sys.stdin); r=derive(p); print(json.dumps({"build": r["build"], "input_status": r["input_status"]}))'], {cwd: path.resolve(__dirname, '../..'), input: JSON.stringify(profile), encoding: 'utf8'});
  assert.equal(python.status, 0, python.stderr);
  const result = JSON.parse(python.stdout);
  assert.deepEqual(result.build, profile.build);
  assert.equal(result.input_status, 'synthetic');
});

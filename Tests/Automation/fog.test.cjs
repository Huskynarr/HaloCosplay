'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const path = require('node:path');
const budget = require('../../web/budget/budget.js');
const profile = require('../../web/configurator/profile.js');
const schema = require('../../Design/Parametric/ProfileSchema.json');
const fog = require('../../Materials/Mjolnir-Nebel-BOM.json');
const base = require('../../Materials/Mjolnir-BOM.json');
const clone = value => JSON.parse(JSON.stringify(value));

test('fog addon preserves base costs, settings and source objects without inventing mass', () => {
  const previous = clone(base);
  const merged = budget.appendModule(base, fog);
  assert.deepEqual(base, previous);
  assert.equal(merged.contingency_fraction, base.contingency_fraction);
  assert.equal(merged.wearable_target_g, base.wearable_target_g);
  assert.deepEqual(merged.excluded, base.excluded);
  assert.deepEqual(budget.calculate(fog).base_eur, [330, 505]);
  assert.deepEqual(budget.calculate(fog).with_reserve_eur, [396, 606]);
  assert.equal(budget.calculate(merged).unknown_worn_mass_ids.length, 6);
  assert.equal(budget.calculate(merged).mass_target_met_in_plan, false);
  assert.deepEqual(budget.calculate(merged).base_eur, [1993, 4045]);
  merged.items[0].name = 'changed';
  assert.deepEqual(base, previous);
});

test('adding the same module twice fails without changing the project', () => {
  const once = budget.appendModule(base, fog), previous = clone(once);
  assert.throws(() => budget.appendModule(once, fog), /bereits vorhanden/);
  assert.deepEqual(once, previous);
});

test('legacy profiles default to no fog; valid fog choices survive Python export', () => {
  const legacy = profile.create(schema); delete legacy.build.fog_system;
  assert.equal(profile.imported(legacy, schema).build.fog_system, 'none');
  for (const choice of schema.build_fields.fog_system.options) {
    const selected = profile.imported(legacy, schema);
    selected.build.fog_system = choice;
    const result = spawnSync('python3', ['-c', 'import json,sys; from tools.suit_fit import derive; print(derive(json.load(sys.stdin),concept=True)["build"]["fog_system"])'], {cwd:path.resolve(__dirname,'../..'),input:JSON.stringify(profile.imported(selected,schema)),encoding:'utf8'});
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout.trim(), choice);
  }
  const invalid = profile.create(schema); invalid.build.fog_system = 'DIY-heater';
  assert.throws(() => profile.imported(invalid, schema));
});

test('fog budget has the same totals through the Python calculator', () => {
  const result = spawnSync('python3', ['-c', 'import json,sys; from tools.suit_budget import calculate; print(json.dumps(calculate(json.load(sys.stdin))))'], {cwd:path.resolve(__dirname,'../..'),input:JSON.stringify(fog),encoding:'utf8'});
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), budget.calculate(fog));
});

const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {empty, calculate, parse, serialize, nextId} = require('../../web/budget/budget.js');
const sample = () => JSON.parse(fs.readFileSync(path.join(__dirname, '../../Materials/Mjolnir-BOM.json'), 'utf8'));
const item = (patch = {}) => ({id:'P001', name:'Testteil', qty:2, unit_budget_eur:[10,20], unit_mass_target_g:100, worn:true, ...patch});
const fixture = () => ({...empty(), wearable_target_g:500, items:[item()]});

test('existing concept BOM has expected totals and round-trips', () => {
  const data = sample();
  const totals = calculate(data);
  assert.deepEqual(totals.base_eur, [1663,3540]);
  assert.deepEqual(totals.with_reserve_eur, [2161.9,4602]);
  assert.equal(totals.planned_worn_g, 11460);
  assert.deepEqual(parse(serialize(data)), data);
});
test('costs include unworn items and reserve does not increase mass', () => {
  const data = fixture();
  data.items.push(item({id:'P002',qty:1,unit_mass_target_g:8000,worn:false}));
  assert.deepEqual(calculate(data).base_eur, [30,60]);
  assert.deepEqual(calculate(data).with_reserve_eur, [36,72]);
  assert.equal(calculate(data).planned_worn_g, 200);
});
test('unknown worn masses cannot meet a planning target', () => {
  const data = fixture();
  data.items.push(item({id:'P002',unit_mass_target_g:null}));
  const result = calculate(data);
  assert.equal(result.planned_worn_g,200);
  assert.deepEqual(result.unknown_worn_mass_ids,['P002']);
  assert.equal(result.mass_target_met_in_plan,false);
  data.items[1].worn = false;
  assert.deepEqual(calculate(data).unknown_worn_mass_ids,[]);
});
test('empty BOM has zero totals and no implied wearer defaults', () => {
  const data = empty();
  assert.deepEqual(data.items, []);
  assert.equal(data.wearable_target_g, 0);
  assert.deepEqual(calculate(data).base_eur, [0,0]);
});
test('IDs are unique and the generated ID fills the first available slot', () => {
  assert.equal(nextId([item(),item({id:'P003'})]),'P002');
  const data = fixture(); data.items.push(item());
  assert.throws(()=>calculate(data),/eindeutige ID/);
});
test('invalid quantities, price ranges, mass types and worn flags fail validation', () => {
  const patches = [{qty:0},{qty:1.5},{qty:true},{qty:Number.MAX_SAFE_INTEGER+1},
    {unit_budget_eur:[20,10]},{unit_budget_eur:[-1,2]},{unit_budget_eur:[1,Infinity]},
    {unit_budget_eur:['1',2]},{unit_budget_eur:[1]}, {unit_mass_target_g:undefined},
    {unit_mass_target_g:NaN},{unit_mass_target_g:-1},{unit_mass_target_g:'10'},{worn:'true'},
    {id:''},{id:' P1'},{name:' '}];
  patches.forEach(patch => assert.throws(()=>calculate({...fixture(),items:[item(patch)]})));
});
test('unsupported schema, currency, reserve, target and exclusions fail validation', () => {
  [null, [], {}, {...fixture(),schema_version:2}, {...fixture(),currency:'USD'},
    {...fixture(),contingency_fraction:1.01}, {...fixture(),contingency_fraction:true},
    {...fixture(),wearable_target_g:null}, {...fixture(),excluded:'Werkzeug'},
    {...fixture(),excluded:['']}, {...fixture(),items:null}].forEach(data => assert.throws(()=>calculate(data)));
});
test('invalid JSON and overflowing totals are rejected, optional metadata is retained', () => {
  assert.throws(()=>parse('{'),/JSON/);
  const data = fixture(); data.items[0].unit_budget_eur = [1e308,1e308];
  assert.throws(()=>calculate(data),/gross/);
  const extended = {...fixture(),project_note:'Eigene Konfiguration'};
  assert.equal(parse(serialize(extended)).project_note,'Eigene Konfiguration');
});

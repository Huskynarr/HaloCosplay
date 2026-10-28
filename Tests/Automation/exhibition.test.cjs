const {test} = require('node:test');
const assert = require('node:assert/strict');
const {validate, state} = require('../../Code/Exhibition/telemetry.js');
const now = Date.parse('2026-09-08T12:00:00Z');
const base = {schema_version:1,source:'measured',device:'Fixture',timestamp:new Date(now).toISOString(),battery_pct:50,temperature_c:null,fan_rpm:1800};
test('starts without assumed sensor values', () => assert.equal(state(null, now).values, null));
test('stale snapshot hides values at expiry', () => {
 const sample = validate(base, now);
 assert.equal(state(sample, now + 10000).values.battery_pct, 50);
 assert.equal(state(sample, now + 10001).values, null);
});
test('demo is always clearly marked', () => assert.match(state(validate({...base,source:'demo'},now),now+999999).label,/SIMULATION/));
test('rejects invalid types, bounds and missing fields', () => {
 for (const battery_pct of [true, '50', NaN, Infinity, -1, 101, undefined]) assert.throws(()=>validate({...base,battery_pct},now));
});
test('rejects unsupported source and ambiguous/future timestamps', () => {
 assert.throws(()=>validate({...base,source:'live'},now));
 for (const timestamp of ['bad','2026-09-08T12:00:00','2026-09-08T12:00:01Z']) assert.throws(()=>validate({...base,timestamp},now));
});
test('clock reversal hides measurements; unknown fields stay unknown', () => {
 const sample=validate(base,now);
 assert.equal(sample.values.temperature_c,null);
 assert.equal(state(sample,now-1).values,null);
});
const {metadata} = require('../../Code/Exhibition/project.js');
test('project display selects only metadata, never measurements',()=>{
 const result=metadata({schema_version:1,profile:'Suit A',build:{armor_reference:'custom',material:'foam',operating_mode:'wearable'},measurements_mm:{height:1910}});
 assert.equal(result.title,'Suit A');
 assert.doesNotMatch(JSON.stringify(result),/1910|height/);
 assert.match(result.summary,/custom/);
});
test('invalid project metadata is rejected',()=>{
 for (const data of [null,{}, {schema_version:1,profile:'',build:{}}, {schema_version:1,profile:'A',build:{material:12}}]) assert.throws(()=>metadata(data));
});

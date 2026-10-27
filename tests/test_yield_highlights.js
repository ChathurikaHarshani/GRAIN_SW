const assert = require('node:assert/strict');
const {yieldDeviations} = require('../static/yield_highlights.js');
const field = (acres, bushels, irrigation = 'Dryland', hybrid = 'DK59-82') => ({acres, bushels, irrigation, hybrid});

let result = yieldDeviations([field(1, 100), field(1, 200)], 'irrigation', 15, 30);
assert.equal(result[0].severity, 'extreme');
assert.ok(result[0].deviation < 0 && result[1].deviation > 0);
assert.equal(result[0].average, 150);

result = yieldDeviations([field(1, 100), field(9, 1800)], 'irrigation', 15, 30);
assert.equal(result[0].average, 190); // Acreage-weighted, not an average of yields.
assert.equal(result[1].severity, null);

result = yieldDeviations([field(1, 120), field(1, 180)], 'irrigation', 15, 30);
assert.equal(result[0].severity, 'moderate');
assert.equal(result[1].severity, 'moderate');

assert.deepEqual(yieldDeviations([field(1, 100), field(1, 200, 'Irrigated')], 'irrigation', 15, 30), [null, null]);
assert.deepEqual(yieldDeviations([field(1, 100), field(1, 200, 'Dryland', 'Other')], 'hybrid', 15, 30), [null, null]);
assert.deepEqual(yieldDeviations([field(0, 100), field(1, 200), field(1, 20, ''), field(1, NaN)], 'irrigation', 15, 30), [null, null, null, null]);
assert.deepEqual(yieldDeviations([field(1, 0), field(1, 0)], 'irrigation', 15, 30), [null, null]);
assert.deepEqual(yieldDeviations([field(1, 100, 'Dryland', ''), field(1, 200, 'Dryland', '')], 'hybrid', 15, 30), [null, null]);
console.log('Yield highlight checks passed.');

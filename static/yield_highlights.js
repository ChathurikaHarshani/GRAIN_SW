// Pure calculation also exercised by the Node regression checks.
function yieldDeviations(fields, mode, moderate, extreme) {
  const groups = new Map();
  const normalized = fields.map(field => {
    const irrigation = field.irrigation.trim().toLowerCase();
    const type = irrigation.startsWith('i') ? 'I' : irrigation.startsWith('d') ? 'D' : null;
    const hybrid = field.hybrid.trim().toLowerCase();
    if (!Number.isFinite(field.acres) || field.acres <= 0 ||
        !Number.isFinite(field.bushels) || field.bushels < 0 || !type ||
        (mode === 'hybrid' && (!hybrid || hybrid === '-' || hybrid === 'unspecified'))) return null;
    const key = JSON.stringify([type, mode === 'hybrid' ? hybrid : '']);
    const group = groups.get(key) || {acres: 0, bushels: 0, count: 0};
    group.acres += field.acres;
    group.bushels += field.bushels;
    group.count += 1;
    groups.set(key, group);
    return {...field, key};
  });
  return normalized.map(field => {
    if (!field) return null;
    const group = groups.get(field.key);
    const average = group.bushels / group.acres;
    if (group.count < 2 || average <= 0) return null;
    const deviation = ((field.bushels / field.acres) / average - 1) * 100;
    const distance = Math.abs(deviation);
    return {average, deviation, severity: distance >= extreme ? 'extreme' : distance >= moderate ? 'moderate' : null};
  });
}

if (typeof module !== 'undefined') module.exports = {yieldDeviations};
if (typeof document !== 'undefined') (() => {
  const toggle = document.getElementById('highlight-yields');
  if (!toggle) return;
  const comparison = document.getElementById('yield-comparison');
  const moderateInput = document.getElementById('yield-moderate');
  const extremeInput = document.getElementById('yield-extreme');
  function update() {
    const moderate = Number(moderateInput.value);
    const extreme = Number(extremeInput.value);
    const valid = moderateInput.validity.valid && extremeInput.validity.valid &&
      Number.isFinite(moderate) && Number.isFinite(extreme) && moderate > 0 && extreme > moderate;
    document.getElementById('yield-highlight-error').textContent = toggle.checked && !valid
      ? 'Enter positive thresholds; extreme must be greater than moderate.' : '';
    document.getElementById('yield-highlight-legend').hidden = !toggle.checked || !valid;
    document.querySelectorAll('.yield-field-table').forEach(table => {
      const rows = Array.from(table.querySelectorAll('[data-yield-field]'));
      const results = toggle.checked && valid ? yieldDeviations(rows.map(row => ({
        acres: row.dataset.acres === '' ? NaN : Number(row.dataset.acres),
        bushels: row.dataset.bushels === '' ? NaN : Number(row.dataset.bushels),
        irrigation: row.dataset.irrigation, hybrid: row.dataset.hybrid
      })), comparison.value, moderate, extreme) : [];
      rows.forEach((row, index) => {
        row.classList.remove('yield-unusual-moderate', 'yield-unusual-extreme');
        row.removeAttribute('title');
        const label = row.querySelector('.yield-deviation');
        label.textContent = '';
        const result = results[index];
        if (!result) return;
        row.title = `Group average: ${result.average.toFixed(1)} bu/ac; ${result.deviation.toFixed(1)}% difference`;
        if (!result.severity) return;
        row.classList.add(`yield-unusual-${result.severity}`);
        label.textContent = `${result.deviation >= 0 ? 'High' : 'Low'} ${Math.abs(result.deviation).toFixed(1)}%`;
      });
    });
  }
  [toggle, comparison, moderateInput, extremeInput].forEach(control => control.addEventListener('input', update));
  update();
})();

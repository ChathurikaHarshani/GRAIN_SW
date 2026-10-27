// Float app table headers during page scrolling, preserving horizontal scrolling.
(() => {
  const report = document.querySelector('main');
  if (!report) return;
  const headers = Array.from(report.querySelectorAll('table')).map(table => {
    if (!table?.tHead) return null;
    const wrapper = table.closest('.table-responsive') || table.parentElement;
    const floating = document.createElement('div');
    floating.className = 'report-floating-header no-print';
    floating.setAttribute('aria-hidden', 'true');
    floating.hidden = true;
    const copy = table.cloneNode(false);
    copy.removeAttribute('id');
    const head = table.tHead.cloneNode(true);
    head.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
    head.querySelectorAll('a, button, input, select, textarea, [tabindex]').forEach(node => {
      node.setAttribute('tabindex', '-1');
    });
    copy.append(head);
    floating.append(copy);
    document.body.append(floating);
    return {wrapper, table, floating, copy, head};
  }).filter(Boolean);
  let pending = false;
  function update() {
    pending = false;
    const nav = document.querySelector('.navbar');
    const top = Math.max(0, nav?.getBoundingClientRect().bottom || 0);
    headers.forEach(({wrapper, table, floating, copy, head}) => {
      const bounds = table.getBoundingClientRect();
      const viewport = wrapper.getBoundingClientRect();
      const height = table.tHead.getBoundingClientRect().height;
      const visible = bounds.width > 0 && height > 0 && bounds.top < top && bounds.bottom > top && viewport.right > 0 && viewport.left < innerWidth;
      floating.hidden = !visible;
      if (!visible) return;
      floating.style.top = `${Math.min(top, bounds.bottom - height)}px`;
      const wrapped = wrapper.classList.contains('table-responsive');
      floating.style.left = `${wrapped ? viewport.left + wrapper.clientLeft : bounds.left}px`;
      floating.style.width = `${wrapped ? wrapper.clientWidth : bounds.width}px`;
      copy.style.width = `${bounds.width}px`;
      copy.style.transform = `translateX(${wrapped ? -wrapper.scrollLeft : 0}px)`;
      copy.style.fontSize = getComputedStyle(table).fontSize;
      const originals = table.tHead.querySelectorAll('th, td');
      head.querySelectorAll('th, td').forEach((cell, index) => {
        const rect = originals[index].getBoundingClientRect();
        const style = getComputedStyle(originals[index]);
        for (const property of ['fontFamily', 'fontSize', 'fontWeight', 'lineHeight',
                                'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                                'textAlign', 'verticalAlign', 'backgroundColor', 'color']) {
          cell.style[property] = style[property];
        }
        cell.style.width = `${rect.width}px`;
        cell.style.minWidth = `${rect.width}px`;
        cell.style.height = `${rect.height}px`;
      });
    });
  }
  function schedule() {
    if (!pending) { pending = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', schedule, {passive: true});
  window.addEventListener('resize', schedule);
  headers.forEach(({wrapper}) => wrapper.addEventListener('scroll', schedule, {passive: true}));
  const observer = new ResizeObserver(schedule);
  observer.observe(report);
  headers.forEach(({table}) => observer.observe(table));
  const nav = document.querySelector('.navbar');
  if (nav) observer.observe(nav);
  schedule();
})();

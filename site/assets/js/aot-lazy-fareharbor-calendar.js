(function () {
  'use strict';

  var loaded = new WeakSet();
  var selector = '.aot-lazy-fh-calendar[data-src]';

  function loadCalendar(holder) {
    if (!holder || loaded.has(holder)) return;
    loaded.add(holder);
    var src = holder.getAttribute('data-src');
    holder.innerHTML = '<div class="fh-label">Loading booking calendar...</div>';
    var script = document.createElement('script');
    script.src = src;
    script.async = true;
    holder.appendChild(script);
  }

  function init() {
    var holders = Array.prototype.slice.call(document.querySelectorAll(selector));
    holders.forEach(function (holder) {
      holder.addEventListener('click', function () { loadCalendar(holder); }, { once: true });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();

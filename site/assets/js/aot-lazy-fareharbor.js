(function () {
  'use strict';

  var apiSrc = 'https://fareharbor.com/embeds/api/v1/?autolightframe=yes';
  var loading = null;

  function showSpinner() {
    var overlay = document.getElementById('fh-loading-overlay');
    if (overlay) overlay.classList.add('active');
  }

  function parseConfig(anchor) {
    var cfg = { shortname: 'activeoahutours', fallback: 'simple' };
    var inline = anchor.getAttribute('onclick') || '';
    var itemMatch = inline.match(/['"]item['"]\s*:\s*['"]([^'"]+)['"]/) || anchor.href.match(/\/items\/(\d+)\//);
    if (itemMatch && itemMatch[1]) cfg.view = { item: itemMatch[1] };
    return cfg;
  }

  function loadFareHarbor() {
    if (window.FH && typeof window.FH.open === 'function' && !window.FH._aotLazyStub) {
      return Promise.resolve();
    }
    if (loading) return loading;
    loading = new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[src^="' + apiSrc + '"]');
      if (existing) {
        existing.addEventListener('load', resolve, { once: true });
        existing.addEventListener('error', reject, { once: true });
        return;
      }
      var script = document.createElement('script');
      script.src = apiSrc;
      script.async = true;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
    return loading;
  }

  function openBooking(anchor) {
    var cfg = parseConfig(anchor);
    showSpinner();
    loadFareHarbor().then(function () {
      window.setTimeout(function () {
        if (window.FH && typeof window.FH.open === 'function') {
          window.FH.open(cfg);
        } else {
          window.location.href = anchor.href;
        }
      }, 650);
    }).catch(function () {
      window.location.href = anchor.href;
    });
  }

  document.addEventListener('click', function (event) {
    var anchor = event.target && event.target.closest ? event.target.closest('a[href*="fareharbor.com/embeds/book"]') : null;
    if (!anchor) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    openBooking(anchor);
  }, true);
})();

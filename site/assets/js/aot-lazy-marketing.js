(function () {
  'use strict';

  var loaded = false;
  var GTAG_ID = 'G-PRRRLMBR8Z';
  var GTM_ID = 'GTM-P55TSP';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  function appendScript(src) {
    if (document.querySelector('script[src="' + src + '"]')) return;
    var script = document.createElement('script');
    script.async = true;
    script.src = src;
    document.head.appendChild(script);
  }

  function loadMarketing() {
    if (loaded) return;
    loaded = true;
    window.gtag('set', 'linker', { domains: ['activeoahutours.com'] });
    window.gtag('js', new Date());
    window.gtag('set', 'developer_id.dZTNiMT', true);
    window.gtag('config', GTAG_ID);
    window.dataLayer.push({ event: 'aot_marketing_loaded_after_interaction' });
    appendScript('https://www.googletagmanager.com/gtag/js?id=' + GTAG_ID);
    appendScript('https://www.googletagmanager.com/gtm.js?id=' + GTM_ID);
  }

  ['pointerdown', 'keydown'].forEach(function (eventName) {
    window.addEventListener(eventName, loadMarketing, { once: true, passive: true });
  });
})();

(function () {
  'use strict';

  var loaded = false;
  var selector = 'script[type="text/plain"][data-aot-lazy-tripadvisor][data-src]';

  function loadTripAdvisorWidgets() {
    if (loaded) return;
    var placeholders = Array.prototype.slice.call(document.querySelectorAll(selector));
    if (!placeholders.length) return;
    loaded = true;

    placeholders.forEach(function (placeholder) {
      var script = document.createElement('script');
      script.async = true;
      script.src = placeholder.getAttribute('data-src');
      script.setAttribute('data-loadtrk', '');
      script.onload = function () { script.loadtrk = true; };
      placeholder.parentNode.insertBefore(script, placeholder.nextSibling);
    });
  }

  function observeWidgets() {
    var placeholders = Array.prototype.slice.call(document.querySelectorAll(selector));
    if (!placeholders.length) return;
    if (!('IntersectionObserver' in window)) {
      window.setTimeout(loadTripAdvisorWidgets, 5000);
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i += 1) {
        if (entries[i].isIntersecting) {
          observer.disconnect();
          loadTripAdvisorWidgets();
          break;
        }
      }
    }, { rootMargin: '600px 0px' });

    placeholders.forEach(function (placeholder) {
      var card = placeholder.closest('.review-item') || placeholder.parentElement || placeholder;
      observer.observe(card);
    });
  }

  ['scroll'].forEach(function (eventName) {
    window.addEventListener(eventName, loadTripAdvisorWidgets, { once: true, passive: true });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observeWidgets, { once: true });
  } else {
    observeWidgets();
  }
})();

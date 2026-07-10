(function() {
  'use strict';
  if (window.__aotBookingAnalyticsInit) { return; }
  window.__aotBookingAnalyticsInit = true;

  var bookingInProgress = false;
  var lastClickTarget = null;
  var lastBookingClickSignature = '';
  var lastBookingClickAt = 0;

  function closestContext(el) {
    var node = el;
    for (var i = 0; i < 10 && node; i++) {
      var cls = ((node.className || '') + ' ' + (node.id || '')).toLowerCase();
      if (cls.indexOf('listing-book-button') > -1 || cls.indexOf('card-cta') > -1) { return 'card'; }
      if (cls.indexOf('site-header') > -1 || cls.indexOf('header-cta') > -1 || cls.indexOf('nav') > -1) { return 'header'; }
      if (cls.indexOf('footer') > -1) { return 'footer'; }
      if (cls.indexOf('calendar') > -1 || cls.indexOf('fareharbor-calendar') > -1) { return 'calendar'; }
      if (cls.indexOf('hero') > -1 || cls.indexOf('banner') > -1) { return 'hero'; }
      node = node.parentElement;
    }
    if (el && el.tagName === 'A' && el.href && el.href.indexOf('fareharbor.com/embeds/book') > -1) { return 'link'; }
    return 'unknown';
  }

  function parseItemFromHref(href) {
    var match = String(href || '').match(/\/items\/(\d+)\//);
    return match ? match[1] : '';
  }

  function parseShortnameFromHref(href) {
    var match = String(href || '').match(/fareharbor\.com\/embeds\/book\/([^/?#]+)/);
    return match ? match[1] : 'activeoahutours';
  }

  function shouldEmitBookingClick(payload) {
    var now = Date.now();
    var signature = [
      payload.fareharbor_shortname || '',
      payload.fareharbor_item || '',
      payload.cta_type || '',
      payload.cta_source || ''
    ].join('|');
    if (signature === lastBookingClickSignature && now - lastBookingClickAt < 1000) {
      return false;
    }
    lastBookingClickSignature = signature;
    lastBookingClickAt = now;
    return true;
  }

  document.addEventListener('click', function(evt) {
    var target = evt.target;
    var link = target && target.closest ? target.closest('a[href*="fareharbor.com/embeds/book"]') : null;
    if (link) {
      lastClickTarget = link;
      emitBookingClick({
        shortname: parseShortnameFromHref(link.href),
        view: { item: parseItemFromHref(link.href) },
        source: 'fareharbor_link'
      });
    }
  }, true);

  function emitBookingClick(options) {
    var item = (options && options.view && options.view.item) || '';
    if (!item && lastClickTarget) { item = parseItemFromHref(lastClickTarget.href); }
    var ctaType = 'unknown';
    if (options && options.source === 'fareharbor_link') {
      ctaType = 'link';
    } else if (options && options.view) {
      ctaType = options.view.item ? 'calendar' : (options.view.category ? 'category' : 'view');
    } else if (lastClickTarget) {
      ctaType = 'link';
    }
    var payload = {
      fareharbor_shortname: (options && options.shortname) || 'activeoahutours',
      fareharbor_item: item,
      cta_type: ctaType,
      cta_source: closestContext(lastClickTarget)
    };
    if (typeof window.gtag === 'function' && shouldEmitBookingClick(payload)) {
      window.gtag('event', 'booking_click', payload);
    }
  }

  function wrapFHOpen() {
    if (!window.FH || typeof window.FH.open !== 'function') {
      window.setTimeout(wrapFHOpen, 500);
      return;
    }
    if (window.FH.__aotBookingAnalyticsWrapped) { return; }
    var originalOpen = window.FH.open;
    window.FH.open = function(options) {
      emitBookingClick(options || {});
      bookingInProgress = true;
      return originalOpen.apply(this, arguments);
    };
    window.FH.__aotBookingAnalyticsWrapped = true;
  }

  function checkLightboxDismissed() {
    if (!bookingInProgress) { return; }
    var overlay = document.querySelector('.fh-modal, .fareharbor-iframe, [data-fh-modal], iframe[src*="fareharbor"]');
    if (!overlay) {
      bookingInProgress = false;
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'booking_complete', { source: 'fh_lightbox_dismiss' });
      }
    }
  }

  wrapFHOpen();
  window.setInterval(checkLightboxDismissed, 2000);
})();

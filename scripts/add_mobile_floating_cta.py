#!/usr/bin/env python3
"""Add GRO-1931 mobile floating CTA component to target static HTML pages.

Idempotent: skips files that already contain the AOT_MOBILE_CTA_START marker.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / 'site/oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/index.html',
    ROOT / 'site/oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/index.html',
    ROOT / 'site/sharks-cove-snorkeling/index.html',
    ROOT / 'site/oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/index.html',
]
MARKER = 'AOT_MOBILE_CTA_START'
SNIPPET = r'''
<!-- AOT_MOBILE_CTA_START: GRO-1931 mobile floating CTA -->
<style id="aot-mobile-cta-styles">
  .aot-mobile-cta {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9998;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 14px max(12px, env(safe-area-inset-bottom));
    background: #ffffff;
    color: #17324d;
    border-top: 1px solid rgba(23, 50, 77, 0.16);
    box-shadow: 0 -8px 24px rgba(23, 50, 77, 0.18);
    transform: translateY(110%);
    opacity: 0;
    transition: transform 180ms ease, opacity 180ms ease;
  }
  .aot-mobile-cta.is-visible { transform: translateY(0); opacity: 1; }
  .aot-mobile-cta.is-suppressed,
  .aot-mobile-cta[hidden] { display: none !important; }
  .aot-mobile-cta__copy { min-width: 0; line-height: 1.15; }
  .aot-mobile-cta__price { display: block; font-weight: 800; font-size: 0.98rem; }
  .aot-mobile-cta__trust { display: block; font-size: 0.78rem; color: #425466; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .aot-mobile-cta__button { min-height: 44px; min-width: 132px; border: 0; border-radius: 999px; padding: 0 16px; font-weight: 800; background: #0b6f88; color: #fff; }
  .aot-mobile-cta__button:focus-visible { outline: 3px solid #ffbf47; outline-offset: 2px; }
  body.aot-mobile-cta-active { padding-bottom: 76px; }
  @media (min-width: 768px) { .aot-mobile-cta { display: none !important; } body.aot-mobile-cta-active { padding-bottom: 0; } }
  @media (max-width: 359px) { .aot-mobile-cta { gap: 8px; padding-left: 10px; padding-right: 10px; } .aot-mobile-cta__button { min-width: 118px; padding: 0 12px; } }
  @media (prefers-reduced-motion: reduce) { .aot-mobile-cta { transition: none; } }
</style>
<div class="aot-mobile-cta" data-aot-mobile-cta hidden aria-live="polite">
  <div class="aot-mobile-cta__copy">
    <span class="aot-mobile-cta__price" data-aot-mobile-cta-price></span>
    <span class="aot-mobile-cta__trust" data-aot-mobile-cta-trust></span>
  </div>
  <button class="aot-mobile-cta__button" type="button" data-aot-mobile-cta-button></button>
</div>
<script id="aot-mobile-cta-script">
(function () {
  'use strict';
  var routes = {
    '/oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/': {
      item: 402403,
      label: 'Book Mokoliʻi Kayak',
      price: 'From $69 / 4 hrs',
      trust: 'Gear + launch guidance • check wind first',
      fallbackGlobal: true
    },
    '/oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/': {
      item: 491345,
      label: 'Book Kailua Kayak',
      price: 'From $69 / 4 hrs',
      trust: 'Permit handled when landing • route briefing included',
      fallbackGlobal: true
    },
    '/sharks-cove-snorkeling/': {
      item: 7872,
      label: 'Book Snorkel Gear',
      price: 'From $18 / full day',
      trust: 'Summer-calm conditions only • respect the reef'
    },
    '/oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/': {
      item: null,
      label: 'Book Kahana Kayak',
      price: 'Check availability',
      trust: 'Rainforest paddle • conditions can change',
      fallbackGlobal: true
    }
  };
  var path = window.location.pathname;
  if (path.slice(-1) !== '/') { path += '/'; }
  var cfg = routes[path];
  var mql = window.matchMedia ? window.matchMedia('(min-width: 768px)') : { matches: false };
  if (!cfg || mql.matches) { return; }

  var bar = document.querySelector('[data-aot-mobile-cta]');
  var price = document.querySelector('[data-aot-mobile-cta-price]');
  var trust = document.querySelector('[data-aot-mobile-cta-trust]');
  var button = document.querySelector('[data-aot-mobile-cta-button]');
  if (!bar || !price || !trust || !button) { return; }
  price.textContent = cfg.price;
  trust.textContent = cfg.trust;
  button.textContent = cfg.label;
  button.setAttribute('aria-label', cfg.label);

  var impressionSent = false;
  var lastClickAt = 0;
  function pushEvent(name, params) {
    params = params || {};
    params.page_path = path;
    params.cta_label = cfg.label;
    params.fareharbor_item = cfg.item || 'global';
    params.price_text = cfg.price;
    if (window.dataLayer && Array.isArray(window.dataLayer)) {
      window.dataLayer.push(Object.assign({ event: name }, params));
    }
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    }
  }
  function isVisibleOverlay(el) {
    if (!el) { return false; }
    var cs = window.getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') { return false; }
    var rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }
  function hasFareHarborOverlay() {
    var nodes = document.querySelectorAll('iframe[src*="fareharbor"], .fh-modal, .fareharbor-iframe, [data-fh-modal], [class*="lightframe"], [id*="lightframe"]');
    for (var i = 0; i < nodes.length; i += 1) {
      if (isVisibleOverlay(nodes[i])) { return true; }
    }
    return false;
  }
  function overlapRisk() {
    if (hasFareHarborOverlay()) { return 'fareharbor_open'; }
    var footer = document.querySelector('footer');
    if (footer) {
      var rect = footer.getBoundingClientRect();
      if (rect.top < window.innerHeight - 84) { return 'footer_overlap'; }
    }
    return '';
  }
  function setVisible(visible, reason) {
    if (visible) {
      bar.hidden = false;
      bar.classList.remove('is-suppressed');
      bar.classList.add('is-visible');
      document.body.classList.add('aot-mobile-cta-active');
      if (!impressionSent) {
        impressionSent = true;
        pushEvent('mobile_cta_impression', { viewport_width: window.innerWidth });
      }
    } else {
      bar.classList.remove('is-visible');
      document.body.classList.remove('aot-mobile-cta-active');
      if (reason) {
        bar.classList.add('is-suppressed');
        pushEvent('mobile_cta_suppressed', { reason: reason });
      }
    }
  }
  function updateVisibility() {
    if (mql.matches) { setVisible(false, 'desktop'); return; }
    var risk = overlapRisk();
    if (risk) { setVisible(false, risk); return; }
    setVisible(window.scrollY >= 320, '');
  }
  function openFareHarbor() {
    var started = Date.now();
    lastClickAt = started;
    var scrollDepth = Math.round((window.scrollY / Math.max(1, document.documentElement.scrollHeight - window.innerHeight)) * 100);
    pushEvent('mobile_cta_click', { scroll_depth_pct: scrollDepth });
    if (window.FH && typeof window.FH.open === 'function') {
      if (cfg.item) {
        window.FH.open({ shortname: 'activeoahutours', view: { item: cfg.item }, fallback: 'simple' });
      } else {
        window.FH.open({ shortname: 'activeoahutours', fallback: 'simple' });
      }
    } else {
      window.location.href = cfg.item ? 'https://fareharbor.com/embeds/book/activeoahutours/items/' + cfg.item + '/' : 'https://fareharbor.com/embeds/book/activeoahutours/';
      return;
    }
    var interval = window.setInterval(function () {
      if (Date.now() - started > 4000) { window.clearInterval(interval); return; }
      if (hasFareHarborOverlay()) {
        window.clearInterval(interval);
        setVisible(false, 'fareharbor_open');
        pushEvent('mobile_cta_fareharbor_launch', { launch_latency_ms: Date.now() - lastClickAt });
      }
    }, 200);
  }
  button.addEventListener('click', openFareHarbor);
  window.addEventListener('scroll', updateVisibility, { passive: true });
  window.addEventListener('resize', updateVisibility);
  if (mql.addEventListener) { mql.addEventListener('change', updateVisibility); }
  window.setTimeout(updateVisibility, 250);
}());
</script>
<!-- AOT_MOBILE_CTA_END -->
'''


def add_snippet(path: Path) -> bool:
    text = path.read_text(encoding='utf-8', errors='ignore')
    if MARKER in text:
        return False
    idx = text.lower().rfind('</body>')
    if idx == -1:
        raise ValueError(f'Missing </body>: {path}')
    text = text[:idx] + SNIPPET + '\n' + text[idx:]
    path.write_text(text, encoding='utf-8')
    return True


def main() -> int:
    changed = []
    for target in TARGETS:
        if not target.exists():
            raise FileNotFoundError(target)
        if add_snippet(target):
            changed.append(str(target.relative_to(ROOT)))
    print('changed_count=', len(changed), sep='')
    for item in changed:
        print('changed=', item, sep='')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

# FareHarbor CTA Friction & Performance Audit — GRO-1711

**Auditor:** Kai-JS & AGY (dual audit)  
**Date:** June 15, 2026  
**Subject Site:** activeoahutours.com (`~/work/active-oahu-static`)

---

## Executive Summary
This audit investigates the performance overhead of the FareHarbor booking widget on mobile widths, above-the-fold visibility of Call-To-Action (CTA) elements on key tour pages, and user experience friction points. 

We discovered that the current configuration introduces **significant performance bottlenecks** on mobile devices due to a heavy 2.0 MB synchronous prewarm mechanism. Additionally, key tour page CTAs are placed deep below the fold, causing visual friction. 

Finally, a **critical maintenance risk** was identified where previous mobile layout adjustments were committed directly to generated static files rather than their respective source templates, leaving them vulnerable to regression upon any site rebuild.

---

## 1. Widget Load Times Investigation & Network Overhead

### Synchronous Script Bottleneck
The current layout in `site/_templates/body_bottom.html` includes the FareHarbor API script synchronously:
```html
<script src="https://fareharbor.com/embeds/api/v1/?autolightframe=yes"></script>
```
* **Redirection Overhead:** This URL returns a `302 Found` redirecting to `https://fareharbor.com/embeds/api/integration-kit-with-ssr/v1/?autolightframe=yes`, adding an extra network roundtrip.
* **Parser Blocking:** Although positioned near the end of the body, parsing and fetching this script synchronously blocks the complete execution of subsequent scripts and delays the window's final `load` event.

### Heavy Prewarm Iframe on `DOMContentLoaded`
The current scripts trigger a `prewarmFH()` function immediately when the DOM is ready:
```javascript
function prewarmFH() {
  var pw = document.createElement('iframe');
  pw.src = 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes';
  pw.style.cssText = 'display:none!important;width:0!important;height:0!important';
  ...
  document.body.appendChild(pw);
  setTimeout(function() {
    if (pw.parentNode) pw.parentNode.removeChild(pw);
  }, 4000);
}
```
* **Payload Overhead:** The prewarm page transfers **~2.0 MB** of raw resources. Inside this hidden iframe, the browser must fetch and compile large libraries (React, Redux), payment processor APIs (Stripe, Adyen, PayPal), and tracking scripts (Google Tag Manager, GA4, Facebook Pixel, Mixpanel, Hotjar).
* **Connection Pools & CPU Competition:** Mobile browsers limit concurrent TCP connections per domain (typically 6). Sating this pool with 2MB of FareHarbor assets during early page load competes with local tour images and stylesheets, directly inflating **First Contentful Paint (FCP)** and **Largest Contentful Paint (LCP)**.
* **Data Waste:** Users browsing the page who leave without clicking a CTA are forced to download 2MB of redundant code, which is highly inefficient for mobile cellular connections.
* **Premature Destruction:** The prewarm iframe is removed from the DOM after exactly 4 seconds. Because typical reading times exceed 4 seconds, the iframe is destroyed before the user clicks a booking button, forcing the browser to reconstruct the iframe and repay compilation penalties when they finally trigger the checkout.

---

## 2. Above-the-Fold Mobile CTA Visibility

### Primary Body CTAs Pushed Below the Fold
On a standard mobile viewport (e.g. 375x812px), the layout flow of key tour pages (such as `activities/oahu-sunset-kayak-tour/index.html`) is structured as follows:
1. **Announcement Banner (sticky):** ~60px
2. **Branding Header (logo, phone, book link):** ~100px
3. **Menu Toggle Bar:** ~50px
4. **Hero Image:** ~188px
5. **H1 Title & Subtitle:** ~100px
6. **Detailed Body Copy (4–5 long paragraphs):** ~500px+
7. **Tour Details Icons (stars, time, location):** ~60px
8. **Pricing Table List:** ~100px
9. **Primary "Book Now" CTA Button:** ~50px

This forces the user to scroll **1,000px to 1,200px** down the page to see the primary action. On mobile, this requires multiple swipes and isolates the booking trigger from the initial emotional impact of the page.

### Header CTA Constraints
The header contains a generic "Book Online" CTA:
* **Generic Routing:** The button points to the main booking folder (`https://fareharbor.com/embeds/book/activeoahutours/`) instead of initiating checkout for the specific tour being viewed (e.g. using the tour's specific `flow` parameter).
* **Lack of Persistence:** The header is static on mobile widths and scrolls out of view immediately, leaving no persistent purchase path.

---

## 3. CTA Friction Analysis

* **Context Loss:** When users click the header "Book Online" CTA, they are redirected to a comprehensive list of all activities, forcing them to find the tour again.
* **AdBlocker Fragility:** If a content blocker (e.g. Brave, Safari Extensions) blocks the FareHarbor script, the inline `onclick="FH.open(...)"` throws a JavaScript exception. If propagation/default logic fails, the button becomes inert, failing to fall back gracefully to the simple link.
* **Interactive Lag:** When "Book Now" is clicked, there is a noticeable delay (spinner state) while the iframe loads. This lag reduces trust and interrupts the booking momentum.

---

## 4. JS-Level Performance & Conversion Recommendations

We recommend implementing the following JS-level optimizations within `site/_templates/body_bottom.html` to eliminate friction and improve performance:

### A. Dynamic Script & Intent-Based Prewarming
Remove the synchronous `<script>` tag and load FareHarbor asynchronously based on user intent (hover or touch) or a 3-second idle delay. This keeps the initial page rendering path clean.

```javascript
// Example Dynamic Loader & Interceptor
(function() {
  'use strict';
  
  var fhScriptLoaded = false;
  var fhScriptLoading = false;
  var loadingCallbacks = [];

  function loadFareHarborScript(callback) {
    if (fhScriptLoaded) {
      if (callback) callback();
      return;
    }
    if (callback) loadingCallbacks.push(callback);
    if (fhScriptLoading) return;
    fhScriptLoading = true;

    var script = document.createElement('script');
    script.src = 'https://fareharbor.com/embeds/api/v1/?autolightframe=yes';
    script.async = true;
    script.onload = function() {
      fhScriptLoaded = true;
      fhScriptLoading = false;
      wrapFH();
      while (loadingCallbacks.length > 0) {
        var cb = loadingCallbacks.shift();
        try { cb(); } catch(e) { console.error(e); }
      }
    };
    script.onerror = function() {
      fhScriptLoading = false;
      console.error('Failed to load FareHarbor script');
    };
    document.head.appendChild(script);
  }

  // Bind prewarm to hover/touch of CTAs (gives 150-400ms head start)
  var prewarmed = false;
  function prewarmOnIntent() {
    if (prewarmed) return;
    prewarmed = true;
    loadFareHarborScript(function() {
      // Execute the heavy prewarm iframe only when the user expresses purchase interest
      prewarmFH();
    });
  }

  function bindIntentListeners() {
    var ctas = document.querySelectorAll('a[href*="fareharbor.com"], [onclick*="FH.open"], .btn-primary');
    ctas.forEach(function(cta) {
      cta.addEventListener('mouseenter', prewarmOnIntent, { once: true });
      cta.addEventListener('touchstart', prewarmOnIntent, { once: true });
      cta.addEventListener('focus', prewarmOnIntent, { once: true });
    });
  }

  // Intercept inline onclick attributes in the capture phase to avoid JS exceptions
  document.addEventListener('click', function(e) {
    var anchor = e.target.closest('a');
    if (!anchor) return;

    var onclickStr = anchor.getAttribute('onclick') || '';
    if (onclickStr.indexOf('FH.open') !== -1) {
      if (typeof FH !== 'undefined' && FH.open) return; // Script already loaded, let inline onclick execute

      e.preventDefault();
      e.stopPropagation(); // Stop inline onclick from executing and throwing 'FH is not defined'

      showSpinner();

      var config = null;
      var match = onclickStr.match(/FH\.open\(([^)]+)\)/);
      if (match && match[1]) {
        try {
          config = new Function('return ' + match[1])();
        } catch(err) {
          console.error('Failed to parse FH config', err);
        }
      }

      loadFareHarborScript(function() {
        if (typeof FH !== 'undefined' && FH.open && config) {
          FH.open(config);
        } else {
          window.location.href = anchor.href; // Fallback
        }
      });
    }
  }, true); // capturing phase intercept

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      bindIntentListeners();
      setTimeout(loadFareHarborScript, 3000); // Backfill load after 3s
    });
  } else {
    bindIntentListeners();
    setTimeout(loadFareHarborScript, 3000);
  }
})();
```

### B. Sticky Mobile CTA Bar
Introduce a fixed bottom CTA bar on mobile screens (viewport < 768px) containing two prominent taps:
1. **Call/Text Button:** Triggers `tel:+180****1894` to capture high-intent inquiries.
2. **Book Now Button:** Triggers the specific booking flow for the active page.

**Dynamic Configuration Binding:**  
Instead of hardcoding booking configurations in templates, we can scrape the primary page CTA dynamically at runtime:
```javascript
document.addEventListener('DOMContentLoaded', function() {
  var pageCta = document.querySelector('.content a[onclick*="FH.open"]');
  var stickyBookBtn = document.querySelector('.aot-cta-btn-book');
  if (pageCta && stickyBookBtn) {
    var ctaOnClick = pageCta.getAttribute('onclick');
    stickyBookBtn.setAttribute('onclick', ctaOnClick);
  }
});
```

---

## 5. Critical Rebuild Regression Warning (Template Maintenance)

During this audit, we reviewed the git logs to trace previous mobile layout optimization attempts (specifically **GRO-1197**: *Optimize mobile header — logo/phone/CTA on single line*).

We discovered that commit `e57f6475` added inline style blocks (containing `.social-header` media queries) **directly to individual HTML files** inside the generated `site/` folder (such as `site/tours/index.html` and other generated views). 

* **The Issue:** These layout overrides were **never backported** to the source templates (`site/_templates/body_top.html` or `site/_templates/head.html`).
* **The Risk:** If the site pages are rebuilt or regenerated using the compilation scripts (like `generate_pages.py`), these manual layout improvements will be **completely overwritten and lost**.
* **Remediation:** All mobile header styles, brand style guides, and CTA layout fixes must be maintained within the unified CSS files (e.g. `brand-overrides.css`) or directly in the layout templates, rather than modifying HTML files in the compiled output directory.

---

## Kai's Prioritized Fix List (from Kai-JS audit)

| Priority | Issue | Location | Risk | Fix Type |
|---|---|---|---|---|
| **P1** | Header "Book Online" bypasses FH.open | body_top.html:42 | HIGH | Replace direct URL with FH.open call |
| **P2** | No sticky mobile CTA — first button is below the fold | All activity pages | MEDIUM | Add fixed-bottom CTA bar on mobile |
| **P3** | Zero booking analytics events | body_bottom.js | MEDIUM | Inject gtag events into FH.open wrapper |
| **P4** | FareHarbor API script loads without defer | body_bottom.html:841 | LOW | Add `defer` to script tag |
| **P5** | Calendar widget uses document.write() | 32 activity pages | MEDIUM | Investigate iframe embed alternative |

---

## Status

- **Kai-JS Audit:** ✅ Complete (posted as Linear comment Jun 15 15:12 UTC)
- **AGY Audit:** ✅ Complete (saved to disk, comprehensive JS optimization recommendations)
- **Linear Issue:** GRO-1711, parent GRO-1680
- **Next:** Needs state update to Done (rate-limited at time of processing)

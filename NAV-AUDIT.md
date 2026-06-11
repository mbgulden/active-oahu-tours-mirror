# Navigation and Header Audit Report

This document presents the audit findings comparing the header and navigation elements of the Active Oahu Tours websites across different environments:
1. **Flywheel (Source of Truth)**: `https://activeoahutours2.flywheelstaging.com`
2. **Production**: `https://activeoahutours.com/?v=5`
3. **Staging**: `https://staging.active-oahu-tours-mirror.pages.dev/?v=5`
4. **Local File**: `/home/ubuntu/work/active-oahu-tours-mirror/site/index.html`

---

## Executive Summary

1. **Mobile Menu (Hamburger) is Broken on Static Builds**: Both Production and Staging have a JavaScript event conflict. They load the original WordPress `navigation.js` *and* a custom `Nav dropdown + mobile menu toggle` script. Both scripts listen to the click event on the hamburger button (`.menu-toggle`) and toggle the `.toggled` class on the `#site-navigation` container. This double-triggering cancels itself out, leaving the mobile menu completely non-functional. It works correctly only on Flywheel.
2. **Language Switcher Bugs**: 
   - **Flywheel** uses a dynamic Weglot translation dropdown.
   - **Staging** uses a static "English | 日本語" inline switcher that works correctly in both directions.
   - **Production** uses a static inline "日本語" link. However, on the Japanese sub-pages, the switcher still links to `/ja/` (itself) instead of pointing back to the English homepage (`/` or `/index.html`), meaning users cannot switch back to English.
3. **Link Structure Differences**: Flywheel links contain absolute staging domains or relative WordPress directories (with trailing slashes). Production and Local File map these to `.html` extensions (e.g., `/activities.html`), while Staging maps them to relative clean directories or `index.html` files (e.g., `/activities/`).
4. **CSS Classes**: Navigation CSS classes are 100% identical across all environments.

---

## Environment Comparison Table

| Feature / Element | Flywheel (Source of Truth) | Production | Staging | Local File (`site/index.html`) |
| :--- | :--- | :--- | :--- | :--- |
| **Header Wrapper** | `<header class="clearfix">` | `<header class="clearfix">` | `<header class="clearfix">` | `<header class="clearfix">` |
| **Site Navigation** | `<nav id="site-navigation" class="main-navigation" ...>` | `<nav id="site-navigation" class="main-navigation" ...>` | `<nav id="site-navigation" class="main-navigation" ...>` | `<nav id="site-navigation" class="main-navigation" ...>` |
| **Hamburger Button** | `.menu-toggle` (Click works) | `.menu-toggle` (**BROKEN** due to script conflict) | `.menu-toggle` (**BROKEN** due to script conflict) | `.menu-toggle` (**BROKEN** due to script conflict) |
| **Language Switcher** | Weglot Dropdown (Dynamic) | Inline "日本語" link (Broken on Japanese page) | Inline "English \| 日本語" (Working) | Inline "日本語" link (Broken on Japanese page) |
| **Branding Section Layout** | Logo block + Social Header (Phone/Book Online) + Social Header (Weglot) | Logo block + Social Header (Phone/Book Online/Japanese Link) | Logo block + Social Header (Phone/Book Online) + Social Header (Custom Switcher) | Logo block + Social Header (Phone/Book Online/Japanese Link) |
| **Primary Menu Hrefs** | Staging absolute domain + WP relative directories | Root-relative static `.html` files (e.g., `/activities.html`) | Root-relative clean directories / index files | Root-relative static `.html` files (e.g., `/activities.html`) |
| **Footer Navigation** | Relative directory links | Relative `.html` files | Relative `.html` files | Relative `.html` files |

---

## Detailed Findings

### 1. Mobile Menu Hamburger Toggle Behavior
* **Flywheel (OK)**: Uses only the standard `navigation.js` script to toggle `.toggled` class on the `#site-navigation` container. Clicking works correctly.
* **Production, Staging, & Local (BROKEN)**:
  - Both `navigation.js` and a custom script (`// Nav dropdown + mobile menu toggle...`) are registered on the `.menu-toggle` button.
  - The custom script uses `toggleBtn.addEventListener('click', ...)` and the other assigns `button.onclick = function() { ... }`.
  - When a user clicks the hamburger menu, both scripts execute sequentially in the same event tick. The first script adds/removes the class `.toggled`, and the second immediately removes/adds it back.
  - Due to this double-toggling, the class state remains unchanged, preventing the mobile menu from ever opening.

### 2. Language Switcher Behavior & Rendering
* **Flywheel**: Renders Weglot plugin markup (aside wrapper, inputs, labels, and language choice `<ul>` list). It styles this as a dropdown.
* **Staging**: Replaces Weglot with a custom static HTML block:
  ```html
  <span class="lang-switcher" style="font-size:14px;color:#006699;margin:0 0 0 15px;vertical-align:middle;display:inline-block;line-height:1;">
    <a href="/" style="color:#006699;text-decoration:none;padding:0 4px;">English</a>
    <span style="color:#ccc;padding:0 2px;">|</span>
    <a href="/ja/" style="color:#006699;text-decoration:none;padding:0 4px;">日本語</a>
  </span>
  ```
  This renders two clean, styled text links. It is fully functional.
* **Production & Local**: Nest a single hardcoded link inside `.social-links`:
  ```html
  <a href="/ja/" style="color:#006699;text-decoration:none;padding:0 4px;">日本語</a>
  ```
  - **Critical Bug**: On the Japanese translation page (`/ja/index.html`), the header contains this exact same link pointing to `/ja/`. There is no link back to the English site, trapping users in the Japanese version of the page.

### 3. CSS Class Comparison
All navigation CSS classes match exactly across all sites:
* Main Navigation element: `['main-navigation']`
* Mobile toggle button: `['menu-toggle']`
* Primary Menu `<ul>`: `['menu']`
* Individual `<li>` classes inside the navigation:
  `['menu-item', 'menu-item-has-children', 'menu-item-type-custom', 'menu-item-object-custom', 'menu-item-object-page', ...]` are 100% consistent.

### 4. Layout & DOM Structure Differences
* **Branding Area**:
  - **Flywheel & Staging** have 3 child elements in `<section id="branding">`:
    1. `<div class="aot-logo">`
    2. `<div class="social-header">` (phone, online booking)
    3. `<div class="social-header">` (language switcher markup)
  - **Production & Local File** have only 2 child elements in `<section id="branding">`:
    1. `<div class="aot-logo">`
    2. `<div class="social-header">` (phone, online booking, and inline "日本語" link)
* **Logo Link**:
  - **Flywheel**: points to staging URL `https://activeoahutours2.flywheelstaging.com/` and the image has no loading attribute.
  - **Staging**: points to `/` and the image has `loading="lazy"`.
  - **Production & Local**: point to `/index.html` and the image has `loading="lazy"`.

---

## Comparison of Local File (`site/index.html`) vs Live Flywheel Site

When comparing the local static template `/home/ubuntu/work/active-oahu-tours-mirror/site/index.html` to the live Flywheel site, the following primary HTML and structural differences in navigation were identified:

```diff
--- Flywheel Nav (Live)
+++ Local File Nav (site/index.html)
@@ -1,3 +1,3 @@
 <nav class="main-navigation" data-instant="" id="site-navigation" role="navigation">
 <button aria-controls="primary-menu" aria-expanded="false" class="menu-toggle">Main Menu</button>
-<div class="menu-menu-1-container"><ul class="menu" id="primary-menu"><li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-75" id="menu-item-75"><a href="/activities/">Activities &amp; Tours</a>
+<div class="menu-menu-1-container"><ul class="menu" id="primary-menu"><li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-75" id="menu-item-75"><a href="/activities.html">Activities &amp; Tours</a>
 <ul class="sub-menu">
-  <li id="menu-item-4484"><a href="/activities/">All Tours</a></li>
-  <li id="menu-item-4482"><a href="/activities/#Chinaman's%20Hat%20Kayak%20&amp;%20Hike">Self Guided Tours</a></li>
-  <li id="menu-item-4483"><a href="/activities/#Guided%20Mokulua%20Islands%20Kayak%20Tour%20and%20E-Bike%20Adventure">Guided Tours</a></li>
+  <li id="menu-item-4484"><a href="/activities.html">All Tours</a></li>
+  <li id="menu-item-4482"><a href="/activities.html#Chinaman's%20Hat%20Kayak%20&amp;%20Hike">Self Guided Tours</a></li>
+  <li id="menu-item-4483"><a href="/activities.html#Guided%20Mokulua%20Islands%20Kayak%20Tour%20and%20E-Bike%20Adventure">Guided Tours</a></li>
 </ul>
 </li>
-<li id="menu-item-144"><a href="https://activeoahutours2.flywheelstaging.com/oahu-equipment-rentals/">Rentals</a>
+<li id="menu-item-144"><a href="/rentals/index.html">Rentals</a>
 <ul class="sub-menu">
-  <li id="menu-item-4470"><a href="/oahu-equipment-rentals/">All Rentals</a></li>
-  <li id="menu-item-1375"><a href="https://activeoahutours2.flywheelstaging.com/rentals/oahu-tandem-kayak-rentals/">Kayak Rentals</a>
+  <li id="menu-item-4470"><a href="/rentals/index.html">All Rentals</a></li>
+  <li id="menu-item-1375"><a href="/rentals/oahu-tandem-kayak-rentals/index.html">Kayak Rentals</a>
   <ul class="sub-menu">
-    <li id="menu-item-2857"><a href="https://activeoahutours2.flywheelstaging.com/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/">Mokolii Kayak Rentals</a></li>
-    <li id="menu-item-3036"><a href="https://activeoahutours2.flywheelstaging.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/">Kailua Kayak Rentals</a></li>
+    <li id="menu-item-2857"><a href="/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html">Mokolii Kayak Rentals</a></li>
+    <li id="menu-item-3036"><a href="/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html">Kailua Kayak Rentals</a></li>
   </ul>
 </li>
-  <li id="menu-item-2676"><a href="https://activeoahutours2.flywheelstaging.com/multi-day-kayak-and-beach-gear-rentals/">Multi-Day Rentals</a>
+  <li id="menu-item-2676"><a href="/multi-day-kayak-and-beach-gear-rentals/index.html">Multi-Day Rentals</a>
   <ul class="sub-menu">
-    <li id="menu-item-2678"><a href="https://activeoahutours2.flywheelstaging.com/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/">Rental Partners</a></li>
+    <li id="menu-item-2678"><a href="/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/index.html">Rental Partners</a></li>
   </ul>
 </li>
-  <li id="menu-item-3256"><a href="https://activeoahutours2.flywheelstaging.com/rentals/kailua-beach-bike-rentals/">Electric Bike Rentals</a></li>
+  <li id="menu-item-3256"><a href="/rentals/kailua-beach-bike-rentals/index.html">Electric Bike Rentals</a></li>
 </ul>
 </li>
-<li id="menu-item-4473"><a href="https://activeoahutours2.flywheelstaging.com/oahu-kayaking-and-beach-adventures/">Adventure Guide</a>
+<li id="menu-item-4473"><a href="/oahu-kayaking-and-beach-adventures/index.html">Adventure Guide</a>
 <ul class="sub-menu">
-  <li id="menu-item-4480"><a href="/oahu-kayaking-and-beach-adventures/">All Adventure Guides</a></li>
-  <li id="menu-item-4477"><a href="https://activeoahutours2.flywheelstaging.com/oahu-equipment-rentals/kayak-rental-near-chinamans-hat/">Get Your Kayak Rental for Chinaman’s Hat</a></li>
-  <li id="menu-item-4478"><a href="https://activeoahutours2.flywheelstaging.com/oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/">Lanikai Beach Guide</a></li>
-  <li id="menu-item-4476"><a href="https://activeoahutours2.flywheelstaging.com/oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/">Kailua Beach Guide</a></li>
-  <li id="menu-item-4475"><a href="https://activeoahutours2.flywheelstaging.com/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/">How to Transport Kayaks</a></li>
+  <li id="menu-item-4480"><a href="/oahu-kayaking-and-beach-adventures/index.html">All Adventure Guides</a></li>
+  <li id="menu-item-4477"><a href="/oahu-equipment-rentals/kayak-rental-near-chinamans-hat/index.html">Get Your Kayak Rental for Chinaman’s Hat</a></li>
+  <li id="menu-item-4478"><a href="/oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/index.html">Lanikai Beach Guide</a></li>
+  <li id="menu-item-4476"><a href="/oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/index.html">Kailua Beach Guide</a></li>
+  <li id="menu-item-4475"><a href="/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/index.html">How to Transport Kayaks</a></li>
 </ul>
 </li>
-<li id="menu-item-17"><a href="https://activeoahutours2.flywheelstaging.com/contact-us/">Contact Us</a>
+<li id="menu-item-17"><a href="/contact-us.html">Contact Us</a>
 <ul class="sub-menu">
-  <li id="menu-item-76"><a href="https://activeoahutours2.flywheelstaging.com/about-active-oahu-tours/">About</a>
+  <li id="menu-item-76"><a href="/about-active-oahu-tours/index.html">About</a>
   <ul class="sub-menu">
-    <li id="menu-item-3080"><a href="https://activeoahutours2.flywheelstaging.com/kailua-oahu-storefront/">Our Kailua Storefront</a></li>
-    <li id="menu-item-2421"><a href="https://activeoahutours2.flywheelstaging.com/about-active-oahu-tours/awards/">Awards</a></li>
-    <li id="menu-item-101"><a href="/guides/">Guides</a></li>
-    <li id="menu-item-470"><a href="/reviews/">Reviews</a></li>
+    <li id="menu-item-3080"><a href="/kailua-oahu-storefront/index.html">Our Kailua Storefront</a></li>
+    <li id="menu-item-2421"><a href="/about-active-oahu-tours/awards/index.html">Awards</a></li>
+    <li id="menu-item-101"><a href="/guides/index.html">Guides</a></li>
+    <li id="menu-item-470"><a href="/reviews/index.html">Reviews</a></li>
   </ul>
 </li>
-  <li id="menu-item-225"><a href="https://activeoahutours2.flywheelstaging.com/active-oahu-photo-gallery/">Gallery</a></li>
-  <li id="menu-item-697"><a href="https://activeoahutours2.flywheelstaging.com/faq/">FAQ</a></li>
+  <li id="menu-item-225"><a href="/active-oahu-photo-gallery/index.html">Gallery</a></li>
+  <li id="menu-item-697"><a href="/faq/index.html">FAQ</a></li>
 </ul>
 </li>
 </ul></div> </nav>
```

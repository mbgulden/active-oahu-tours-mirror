# Mobile Experience Report

**Date:** 2026-06-12  
**Source Data:** GA4 Device report (Property `289642224`, last 30 days)  

---

## 1. Device Traffic Distribution

Mobile devices represent the majority of search traffic for Active Oahu Tours. Our GA4 data shows:

* **Mobile**: **1,986 sessions (52.6% share)**
* **Desktop**: **1,780 sessions (47.1% share)**
* **Tablet**: **12 sessions (0.3% share)**
* **Total**: **3,778 sessions**

Because more than half of our potential bookings start on mobile devices, mobile UX is our primary driver for conversion optimization.

---

## 2. Mobile CTA Visibility & Layout Issues

During our mobile audit of `activeoahutours.com`, we identified several layout and visual issues:

1. **Header Crowding**:
   * The logo image (`Active-Oahu-Logo.jpg`) is hardcoded to `width="232"` and `height="65"`. On standard mobile viewports (360px–390px wide), this leaves less than 130px of horizontal space.
   * As a result, the phone number `(808) 498-1894` and the "Book Online" header CTA wrap and stack vertically. This consumes **120px of vertical space** at the top of every page, pushing main hero content and headings below the fold.
2. **Deep-Scroll CTAs**:
   * On rental pages, the "Book" buttons are nested within product description rows. On mobile, these rows stack vertically. A user must scroll through **2 to 3 full screens of text** before reaching the booking button for a specific kayak or paddleboard.
3. **Language Switcher Placement**:
   * The Weglot language switcher ("English | 日本語") is placed in the header next to the booking button. On mobile, it overlaps with the button, leading to accidental clicks and frustrating navigation loops.

---

## 3. Mobile Page Speed & Performance

According to our audit of script integrations:

* **Third-Party Script Weight**:
  * **Weglot** (translation engine) and **FareHarbor** (booking engine) scripts load asynchronously.
  * While this prevents blocking initial paint, it causes a noticeable **Layout Shift (CLS)** on mobile devices about 1.5 seconds after load, as the widgets and translated text render.
* **Image Sizes**:
  * High-resolution JPEG hero images (e.g. `Oahu-Snorkeling_Header2-3x1-1.jpg`, 2000px wide) are served to mobile users without optimized scaling, increasing mobile load times on cellular connections.

---

## 4. Mobile-Specific Recommendations

1. **Responsive Header Logo**:
   * Reduce the logo size to `width="160"` on mobile devices via CSS media queries, freeing up horizontal space so that the logo, phone number, and "Book Online" CTA can sit neatly on a single line.
2. **Sticky Mobile Bottom CTA**:
   * Implement a floating bottom bar on mobile screens. When a user scrolls past the hero section, a sticky button slides up from the bottom: **"Book Tandem Kayak - $49"**. This keeps the primary transaction path accessible at all times without cluttering the screen.
3. **FareHarbor Checkout Form Simplification**:
   * Minimize the traveler fields in FareHarbor for mobile viewports. Postpone participant sizing questions (shoe size, height, weight) to a post-booking confirmation portal or automated email.
4. **Lazy-Load Weglot**:
   * Defer the Weglot language widget script so it only initializes after the primary page elements have fully rendered, reducing layout shifts and improving Mobile Speed Index scores.

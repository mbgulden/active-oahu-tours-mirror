# Mobile CTA & Trust Block Visibility Audit

**GRO-1713** — Sub-task of GRO-1680
**Auditor:** Kai-CSS
**Date:** June 15, 2026
**Device width target:** 375px (iPhone SE / small mobile)

---

## 1. CTA Button Hierarchy (375px width)

### Findings

**Header "Book Online" button** ✅ — Well-positioned as `.btn-primary` in the `.social-header` column. On mobile (≤767px), it scales down to 12px font, 5px/10px padding. Visible without scrolling.

**Activity listing FareHarbor CTAs** ⚠️ — Three booking CTAs on the homepage (lines 757, 812, 867) use the `.listing-book-button` class with `float:right`. On mobile ≤480px, this float causes collapsed layout issues — the button may overlap or be pushed off the edge of its container.

**Carousel CTA (`.carousel-caption .btn`)** ⚠️ — At ≤400px, the `p` inside the caption is hidden (`display:none`), but the CTA link remains. However, the text "Book Online" in the carousel may be hard to read against hero images at 375px.

**Kadence block CTAs (homepage activity cards)** ✅ — These use `.kb-button` with good responsive sizing. At ≤767px they use `font-size: 14px` with adequate padding.

### Issues
1. `.listing-book-button` uses `float:right` which breaks at mobile widths → CTA is invisible or collapsed
2. No sticky/always-visible CTA on mobile — user must scroll back up to find "Book Online"
3. Multiple competing CTAs on homepage (header book button + 3 listing CTAs + carousel CTA + Kadence block buttons)

### Suggested Improvements
- **Add sticky mobile CTA bar** at bottom of viewport (phone + book buttons)
- **Fix `.listing-book-button` on mobile** — change from `float:right` to `display:block; width:100%`
- **Ensure min 44x44pt tap targets** on all mobile CTAs

---

## 2. Trust Signals Visible Without Scrolling

### Findings

**Review section position** ❌ — The `.review-container` starts at ~line 1041 of the homepage HTML, well below the fold. On a 375px device, this is 3+ scrolls down, past the hero, activity listings, and newsletter signup.

**Review item layout** ⚠️ — At ≤460px, `.review-item` goes to `width:100%` (correct), but the 4 reviews stack vertically, consuming significant vertical space. The first review isn't visible until the user scrolls down past the tour listings.

**TripAdvisor widget** ⚠️ — The `TA_cdsratingsonlynarrow` widget loads dynamically. Its position in the HTML (after the reviews section at line 1068) means it's far below the fold on mobile.

**No trust badges/guarantees** ❌ — There are no visible "Best Price Guarantee," "Secure Booking," or "100% Satisfaction" badges anywhere on the homepage that would appear above the fold.

**Phone number visibility** ✅ — The "Call or Text (808)498-1894" is visible in the header immediately. The hero section also has a phone link at line 679.

### Issues
1. Review section is 3+ scrolls below the fold on mobile
2. No trust badges, guarantees, or ratings visible in the initial viewport
3. TripAdvisor rating widget loads but is positioned too low

### Suggested Improvements
- **Show a featured review excerpt** in the hero or near the top content
- **Add trust badges row** (guarantee, secure booking, local expert) near the CTA area
- **Move first review higher** or display star ratings summary near page top

---

## 3. Sticky Mobile Header Does Not Obscure CTAs

### Findings

**No sticky nav on mobile** ✅ — The `.sticky` class (position:fixed, z-index:100) exists in `style.css` but is NOT applied to the nav on mobile breakpoints. The `.main-navigation` scrolls naturally with content. The `activity-nav-container` (position:sticky) is set to `position:static` at ≤630px.

**Header area** ✅ — `#branding` and `.social-header` scroll with the page on mobile. They are not position:fixed or position:sticky. No element at z-index > 100 sits over content.

**Conclusion:** No sticky element obscures CTAs on mobile. This is good — but it also means there's no persistent CTA access. The user has to scroll back up to find "Book Online" or the phone number after scrolling down.

### Issues
1. No sticky header means CTAs are not persistently accessible
2. If a sticky bottom CTA bar is added (§1 recommendation), it must not overlap FareHarbor modal widgets

---

## 4. Mobile Tap Target Compliance

### Checked against WCAG 2.1 AA (44x44pt minimum)

| Element | Tap Target Size | Pass/Fail |
|---|---|---|
| Header "Book Online" `.btn-primary` | ~30x20pt (12px font, 5px padding) | ⚠️ BORDERLINE |
| Activity listing `.listing-book-button .btn` | Float-dependent, varies | ❌ FAIL |
| Kadence block `.kb-button` | Variable, ~40pt height | ✅ PASS (barely) |
| Carousel `.carousel-caption .btn` | ~40pt with padding | ✅ PASS |
| Phone number link | Inline, no padding | ❌ FAIL |
| Menu toggle (hamburger) | 44pt+ (12px padding, full width) | ✅ PASS |

---

## 5. Summary of Implementation Recommendations

### Priority A — Sticky bottom CTA bar (highest conversion impact)
```css
/* Fixed at bottom on mobile, two buttons: Call + Book Now */
.aot-mobile-cta-bar { position: fixed; bottom: 0; ... }
```
- Follows common local business conversion pattern
- Gives persistent access to primary actions
- Must be gated behind mobile-only media query
- Add `body { padding-bottom: 64px }` to prevent content occlusion

### Priority B — Fix mobile booking button layout
```css
@media (max-width: 480px) {
  .listing-book-button { float: none; width: 100%; display: block; }
}
```

### Priority C — Surface trust signals
```css
/* Featured review with star rating near top of content */
.aot-featured-review { border-left: 3px solid #FF6600; ... }
```

### Priority D — Tap target sizing
```css
@media (max-width: 767px) {
  .kb-button.kt-btn-size-standard { min-height: 44px; }
}
```

---

## CSS Files Touched

| File | Action | Reason |
|---|---|---|
| `site/wp-content/themes/activeoahu/css/aot-mobile-cta-audit.css` | **NEW** | All mobile CTA/trust improvements in a standalone `aot-` prefixed file |

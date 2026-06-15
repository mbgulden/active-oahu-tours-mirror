# GRO-1682: AOT Mobile Conversion Audit — Header, CTA Visibility, Trust Blocks

**Date**: 2026-06-15
**Auditor**: Kai-CSS
**Pages Scanned**: Homepage, Chinaman's Hat Self-Guided Kayak Tour (tour page), site-wide CSS

---

## Executive Summary

The mobile site has had significant optimization work (GRO-1302 sticky CTA, GRO-1298 mobile header, GRO-1197 single-line header, GRO-1650 768px breakpoint). The foundation is solid. Below are 8 actionable findings ordered by conversion impact.

---

## 1. 🔴 HIGH — Sticky Header Not Fully Sticky on Mobile

**Observation**: The `position: sticky` is applied to `#navbar-scroll` (the nav bar), NOT to `#branding` (the header row containing logo, phone, and Book Online button). On mobile, when the user scrolls down, the header scrolls away and only the nav/hamburger stays sticky.

**Files**: `site/wp-content/themes/activeoahu/css/nav-fix.css` (lines 106-119, no `sticky` on `#branding`)

**Impact**: The phone number and Book Online button disappear on scroll. Mobile users must scroll back to top to call or book.

**Recommendation**: Make the full `#branding` row sticky at `top: 0` on mobile so the phone + book button persist. Add `z-index: 101` to stay above content.

**Selectors to modify**:
```css
#branding {
  position: sticky !important;
  top: 0 !important;
  z-index: 101 !important;
  background: #fff !important;
}
```

---

## 2. 🔴 HIGH — CTA Button Tap Target Too Small

**Observation**: The primary Book Online button in the header uses `.btn-small` with `padding: 6px 14px; font-size: 13px`. This creates a tap target of approximately 25px × 90px — well under the 44px × 44px minimum for touch targets (WCAG 2.5.5).

**Files**: `nav-fix.css` lines 73-78 (`.social-header .btn-primary`)

**Impact**: Users may miss the button on small screens, especially on bumpy boat rides or with larger fingers.

**Recommendation**: Increase tap target to min 44px height:
```css
@media (max-width: 767px) {
  .social-header .btn-primary {
    padding: 11px 16px !important;
    font-size: 14px !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
  }
}
```

---

## 3. 🟠 MEDIUM — Duplicate Mobile Nav Breakpoint Rules (Conflicting CSS)

**Observation**: Two CSS files govern the mobile nav breakpoint at 767px:
- `nav-fix.css` line 228 — `@media (max-width: 767px)` — derived from GRO-1650
- `brand-overrides.css` line 230 — `@media (max-width: 767px)` — from GRO-751

Both are loaded, and `nav-fix.css` loads AFTER `style.css` (as documented), but `brand-overrides.css` loads after `nav-fix.css` in the HTML. Since both use `!important` on many identical rules, the last-loaded wins — making the nav behavior dependent on load order.

**Files**: Both CSS files noted above

**Impact**: Fragile. Any change to the stylesheet load order or a future breakpoint change requires updating both files simultaneously (as documented in the pitfall). If one file is updated and the other isn't, the nav breaks at specific widths.

**Recommendation**: Consolidate all mobile nav rules into a single CSS file (`nav-fix.css`) and remove the mobile nav section from `brand-overrides.css`. Brand overrides should only define `:root` variables and desktop styling.

---

## 4. 🟠 MEDIUM — Inline Booking CTAs Not Styled as Buttons

**Observation**: Per the GRO-1539 audit, multiple guide pages still have inline text links for booking ("Book your kayak rental here", "→ Book the Sharks Cove Snorkel Experience") that should be styled as visible `.btn` buttons. This was flagged in the earlier audit but remains unresolved on live pages.

**Files**: Various guide pages in `site/guides/*/index.html`

**Impact**: Inline text links blend into content and are missed by scanning users. Visual buttons have 3-5x higher click-through rates per industry benchmarks.

**Recommendation**: Create an `.aot-inline-cta-btn` CSS class:
```css
.aot-inline-cta-btn {
  display: inline-block;
  padding: 12px 24px;
  background: var(--color-accent-orange);
  color: #fff;
  border-radius: var(--border-radius-md);
  font-weight: bold;
  text-decoration: none;
  min-height: 44px;
}
```
Then apply to each inline booking link identified in GRO-1539.

---

## 5. 🟠 MEDIUM — Review/Trust Signals Below Fold on Mobile

**Observation**: On the Chinaman's Hat tour page, review stars and "356 Reviews" appear in the right sidebar. On mobile (<768px), sidebars collapse to full-width below the main content. This means review signals appear after the user scrolls past the entire article (about 2-3 screens).

**Files**: `site/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html` — review block in sidebar

**Impact**: First-time visitors don't see social proof until after the fold. This reduces conversion because trust is a primary purchase driver.

**Recommendation**: Move a review excerpt + star rating into the tour page hero area (between the title and the first CTA button) on mobile. The desktop sidebar can stay as-is. Use a `@media (max-width: 767px)` rule to show a mobile-specific trust banner.

---

## 6. 🟡 LOW — Hero Billboard Background Size on Very Small Screens

**Observation**: The hero billboard uses `background-size: 250%` at `max-width: 480px` and `350%` at `max-width: 380px`. This crops the image heavily on small phones.

**Files**: `style.css` lines (media queries at 480px and 380px for `.bilboard-item:first-child`)

**Impact**: The hero image is heavily zoomed-in on small screens, reducing visual quality and making it harder for users to identify what they're seeing.

**Recommendation**: Use `background-size: cover` at all sizes and set `background-position: center 40%` to keep the focal point visible. Remove the percentage scaling at 480px and 380px.

---

## 7. 🟡 LOW — Guide Items Go Full Width at 460px (Gap from 767px to 461px)

**Observation**: The guide grid breakpoints are:
- `460px` — items go full-width
- `767px` — nav collapses to mobile
- `991px` — tablet layout

There's a gap from 461px to 767px where mobile CSS is partially applied but guide items may not have optimized spacing.

**Files**: `style.css` line (guide-item at max-width: 460px)

**Impact**: Minor — on tablets in portrait (768px width), the nav just switched to mobile but the guide items still show 2-column layout. The 460px breakpoint means phones in landscape (480-736px) show single-column guides.

**Recommendation**: Consider consolidating breakpoints to align with the nav breakpoint (768px). Change guide-item to `@media (max-width: 767px)` to match the mobile nav breakpoint.

---

## 8. 🟡 LOW — No Mobile-Specific Phone Tappable Link

**Observation**: The phone number `(808)498-1894` is displayed as plain text inside `<h3 class="social-header-h3"><span class="feature">`. There is no `<a href="tel:+18084981894">` wrapper to make it a tappable call link on mobile.

**Files**: `site/_templates/body_top.html` (or equivalent header template)

**Impact**: Mobile users must manually copy or remember the number to call. A `tel:` link opens the dialer with one tap.

**Recommendation**: Wrap the phone number in an `<a href="tel:+18084981894">` tag. This is a one-line HTML change, not CSS:
```html
<a href="tel:+18084981894" style="color:#ff7f00;text-decoration:none;">
  <span class="feature">(808)498-1894</span>
</a>
```

---

## Implementation Priority

| # | Finding | Effort | Impact | Quick Win? |
|---|---------|--------|--------|------------|
| 1 | Make header sticky on mobile | Low | High | ✅ Yes |
| 2 | Increase CTA tap target | Low | High | ✅ Yes |
| 8 | Add tel: link to phone | Trivial | Medium | ✅ Yes |
| 3 | Consolidate nav CSS | Medium | Medium | No |
| 4 | Style inline CTAs as buttons | Medium | High | No |
| 5 | Mobile trust banner above fold | Low | High | ✅ Yes |
| 6 | Fix hero image zoom | Low | Low | ✅ Yes |
| 7 | Consolidate guide breakpoints | Low | Low | ✅ Yes |

## Files Touched (Audit Only)

No files were modified. This is a read-only audit. All CSS file references use production branch (`main`) paths under `site/wp-content/themes/activeoahu/css/`.

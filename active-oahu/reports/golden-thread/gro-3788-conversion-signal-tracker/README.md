# GRO-3788 — AOT conversion signal tracker

Generated: 2026-07-11T15:18:26Z

## Scan summary

- HTML files scanned: 310
- `fareharbor_embed_url`: 302
- `fh_open`: 293
- `booking_analytics_loader`: 80
- `gtag_ga4`: 238
- `formsubmit`: 7
- `contact_us_link`: 295
- `partner_path_or_copy`: 292

## Tracker schema

Required fields: `signal`, `source_page`, `event_name`, `collection_method`, `evidence`, `owner`, `threshold`.

## Signals

### booking CTA click
- **signal:** booking CTA click
- **source_page:** Global header/site booking surfaces and product listing cards across static HTML pages
- **event_name:** booking_click
- **collection_method:** Existing /assets/js/aot-booking-analytics.js wraps window.FH.open and emits gtag event with fareharbor_shortname, fareharbor_item, cta_type, cta_source. Static scan found FareHarbor embed URLs on 302 HTML files and FH.open calls on 293 HTML files.
- **evidence:** site/assets/js/aot-booking-analytics.js:35-52; site/assets/js/aot-booking-analytics.js:54-67; scan: fareharbor_embed_url=302, fh_open=293
- **owner:** Kai / Active Oahu analytics
- **threshold:** Weekly: alert when booking_click count drops >20% week-over-week on high-intent pages or fareharbor_item is blank for >25% of item-card clicks.
- **status:** collectable_with_existing_hook
- **missing_hook:** The loader appears on 80/310 HTML files; expand loader coverage or template injection before relying on all booking surfaces.

### FareHarbor lightbox open
- **signal:** FareHarbor lightbox open
- **source_page:** All pages that launch FareHarbor via FH.open
- **event_name:** booking_click plus optional future fareharbor_lightbox_open
- **collection_method:** Current implementation records the click immediately before invoking FH.open; overlay presence is polled only for dismissal/completion proxy. Use booking_click as baseline until a dedicated visible-overlay event is added.
- **evidence:** site/assets/js/aot-booking-analytics.js:61-64; site/assets/js/aot-booking-analytics.js:69-81; scan: fh_open=293
- **owner:** Kai / Active Oahu analytics
- **threshold:** Weekly: investigate if booking_click exists but no FareHarbor sessions/conversions are visible in FareHarbor/GA4 for the same pages.
- **status:** partially_collectable
- **missing_hook:** Add a dedicated fareharbor_lightbox_open event when a visible FareHarbor iframe/modal is detected after FH.open.

### contact form open/submit
- **signal:** contact form open/submit
- **source_page:** Contact/package/partner forms that submit to FormSubmit.co
- **event_name:** contact_form_view, contact_form_submit
- **collection_method:** Static HTML exposes FormSubmit forms on 7 pages. No site-wide JS listener for form view/submit was found in this pass; baseline can currently be inferred from page views plus FormSubmit inbox outcomes only.
- **evidence:** site/contact-us/index.html:510-515; site/contact-us.html:524-529; scan: formsubmit=7
- **owner:** Kai / Active Oahu lead-gen
- **threshold:** Weekly: alert if contact page views rise but inbox leads do not; after hook is added, alert on submit rate <2% for contact pages.
- **status:** missing_site_hook
- **missing_hook:** Add delegated submit listener for form[action*="formsubmit.co"] and optional form impression/view event.

### partner CTA click
- **signal:** partner CTA click
- **source_page:** Become-a-partner pages and any partner-program CTA/link
- **event_name:** partner_cta_click
- **collection_method:** Partner pages/forms are present; static text/path scan found partner language/paths on 292 HTML files, but this broad match includes navigation/footer text and needs a specific CTA selector/data attribute.
- **evidence:** site/become-a-partner/index.html:514-518; site/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/become-a-partner/index.html:520-524; scan: partner_path_or_copy=292
- **owner:** Kai / Active Oahu partnerships
- **threshold:** Weekly: review partner_cta_click to partner form submit ratio; flag if clicks occur with zero submits.
- **status:** missing_specific_hook
- **missing_hook:** Add data-aot-signal="partner_cta" to true partner CTAs and record click events.

### high-intent guide page booking click
- **signal:** high-intent guide page booking click
- **source_page:** Guide pages with booking cards/headers, e.g. tide/launch/safety/logistics pages
- **event_name:** booking_click with page_path and page_type=guide
- **collection_method:** Existing booking_click hook captures CTA source and item, but not page_path/page_type. GA4 page context can be joined in reports; a first-party page_path param would make weekly CRO review cleaner.
- **evidence:** site/kaneohe-bay-sandbar-tide-guide/index.html:193-196; site/oahu-launch-guide/index.html:593-596; site/assets/js/aot-booking-analytics.js:44-50
- **owner:** Kai / Active Oahu content + CRO
- **threshold:** Weekly: prioritize CRO fixes for guide pages with >50 organic sessions and booking_click CTR below 1.5%.
- **status:** collectable_with_reporting_join
- **missing_hook:** Add page_path/page_type params to booking_click; classify guide pages using URL/content taxonomy.

## Weekly review checklist

- [ ] Export GA4 events for booking_click, booking_complete, future contact_form_submit, future partner_cta_click by page_path and source/medium.
- [ ] Compare FareHarbor bookings/revenue against booking_click trend; flag tracking breaks before judging CRO.
- [ ] Review high-intent guide pages by organic sessions, booking_click CTR, and item-card attribution.
- [ ] Inspect missing-hook list and promote one instrumentation fix per sprint until all five signals are first-party measurable.
- [ ] Annotate content/CRO changes so weekly deltas are tied to shipped work, not vibes.

## Fact-check gates

- Verified AOT/FareHarbor booking surfaces by scanning local canonical site HTML for `fareharbor.com/embeds/book` and `FH.open`.
- Verified GA4/GTM evidence from local site snippets containing `G-PRRRLMBR8Z`, `gtag`, and `GTM-P55TSP`.
- Verified FormSubmit contact/partner forms from local HTML `form[action="https://formsubmit.co/team%40activeoahutours.com"]`.
- No prices, durations, safety claims, routes, permits, or new customer-facing product claims were introduced.

## Image/GPS verification

- Not applicable: no imagery selected, edited, placed, or described.

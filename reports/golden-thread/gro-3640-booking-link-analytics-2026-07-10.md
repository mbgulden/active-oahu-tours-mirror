# GRO-3640 booking link analytics hardening — 2026-07-10

## Scope

Closed one remaining Booking & Mobile Conversion gap: booking-surface pages that use plain FareHarbor embed links now emit the same `booking_click` signal as `FH.open` lightbox launches before the visitor leaves for FareHarbor.

## Change

- Updated `site/assets/js/aot-booking-analytics.js` so direct `a[href*="fareharbor.com/embeds/book"]` clicks call `gtag('event', 'booking_click', ...)`.
- Preserved existing `FH.open` instrumentation for lightbox/calendar launches.
- Added a one-second duplicate guard keyed by FareHarbor shortname, item, CTA type, and CTA source so a link-driven lightbox cannot double-count the same click.
- Parsed FareHarbor shortname and item ID from direct embed URLs for better analytics payloads.

## Acceptance evidence to rerun

```bash
python3 -m py_compile scripts/inject_booking_analytics.py
python3 scripts/inject_booking_analytics.py
git diff --exit-code -- scripts/inject_booking_analytics.py site/**/*.html
node /tmp/hermes-verify-gro3640-booking-analytics.js
```

Expected results:

- `inject_booking_analytics.py` reports `Injected booking analytics loader into 0 pages` on the current tree.
- All FareHarbor booking-surface HTML files are covered by either the shared analytics loader or existing inline `booking_click` instrumentation.
- The Node harness observes exactly one `booking_click` for a direct FareHarbor link click and exactly one `booking_click` for two rapid duplicate `FH.open` calls.

## Remaining parent scope

This is a focused implementation unit for the parent. GRO-3640 still needs preview/production verification after merge and the focused Lighthouse pass/follow-up remediation loop tracked under the Golden Path 03 lane.

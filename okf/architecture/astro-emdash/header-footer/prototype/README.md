# Astro/emdash shell prototype — typed data slice

Generated: 2026-07-11T23:42:58Z  
Source commit: `6686a0340a961401c2415e614558f6e622259681`

This prototype is intentionally **non-public** and does not change rendered site output. It proves the current Active Oahu header/footer can be represented as typed data before real Astro adoption.

## Files

- `src/content/nav/aot-shell-data.json` — canonical shell data source.
- `src/content/nav/aot-nav.json` — primary nav + utility links.
- `src/content/nav/aot-footer.json` — footer groups + business/contact data.
- `src/content/nav/aot-booking.json` — FareHarbor booking config.
- `src/types/shell.ts` — TypeScript data interfaces.
- `src/components/shell/*.astro` — non-public component prototype.
- `rendered/aot-shell-prototype.html` — static proof render generated from the same JSON.

## What is preserved

- Primary nav labels and hrefs from the current homepage header.
- Footer hrefs from the current homepage footer, including contact, social, gallery, company, and policy links.
- FareHarbor shortname: `activeoahutours`.
- Booking CTA label: `Book Online`.
- Phone and email contact paths.
- Intent tags for users/search/AI/booking: `tour`, `rental`, `guide`, `support`, `booking`, `language`, `contact`, `social`, `trust`.

## Why this matters

Astro should not inherit the current static export’s hundreds of header/footer variants. This data slice becomes the single source for:

1. rendered navigation,
2. `SiteNavigationElement`/LocalBusiness schema,
3. `/llms.txt` and AI navigation summaries,
4. booking CTA behavior.

## Verification target

This slice must pass exact label/href parity against `current-header-footer-inventory.json` before visual styling or page adoption starts.

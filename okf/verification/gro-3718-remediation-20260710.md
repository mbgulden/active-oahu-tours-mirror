# GRO-3718 — Lighthouse Best Practices remediation

## Scope

Resolve the remaining Best Practices blockers that were still visible after the safe CSP/font pass:

- third-party cookies from TripAdvisor/FareHarbor/Google/Stripe
- Cloudflare challenge-platform deprecation noise
- page-level `TypeError: Line: 2, column: 1, Syntax error`

## Changes made

1. Removed stale static Cloudflare challenge snippets from the exported site.
   - Before: static files contained `285` references to `/cdn-cgi/challenge-platform/scripts/jsd/main.js` and `window.__CF$cv`.
   - After: `0` references remain in `.html`, `.php`, or `.js` files.

2. Deferred TripAdvisor widgets.
   - Replaced direct `https://www.jscache.com/wejs...` widget scripts with inert `data-aot-lazy-tripadvisor` placeholders.
   - Added `/assets/js/aot-lazy-tripadvisor.js` to load the widget only when the review widget nears the viewport or the visitor scrolls.
   - Booking clicks do not trigger TripAdvisor loading.

3. Removed hidden FareHarbor checkout prewarm.
   - The hidden `fareharbor-prewarm` iframe created third-party booking cookies before a visitor asked to book.
   - FareHarbor API/lightbox remains active for visible booking CTAs.

4. Removed empty `speculationrules` script tags.
   - These were the source of Chromium's `While parsing speculation rules: Line: 2, column: 1, Syntax error` warning and the matching page-level Playwright/Lighthouse TypeError.
   - Non-empty valid speculation rules were preserved.

## Verification

Focused static verification:

```text
prewarmFH: 0
fareharbor-prewarm: 0
__CF$cv: 0
/cdn-cgi/challenge-platform/scripts/jsd/main.js: 0
lazy TA placeholders: 79
lazy loader includes: 77
```

Syntax / diff hygiene:

```text
git diff --check: pass
python3 -m py_compile scripts/remediate_lighthouse_best_practices.py: pass
node --check site/assets/js/aot-lazy-tripadvisor.js: pass
```

Rendered console trace on `/kayak-rentals/`:

| Run | TripAdvisor initial request | FareHarbor prewarm request | Static CF challenge request | Page errors |
|---|---:|---:|---:|---:|
| Baseline | yes | yes | yes | `TypeError: Line: 2, column: 1, Syntax error` |
| After | no | no | no | none |

Booking CTA smoke test on `/kayak-rentals/` after remediation:

```json
{
  "before": {
    "fhReady": true,
    "tripAdvisorLoaded": 0,
    "prewarmIframes": 0
  },
  "after": {
    "overlays": 4,
    "spinnerPresent": true,
    "tripAdvisorLoaded": 0
  },
  "fareHarborRequestCount": 27
}
```

Focused local Lighthouse Best Practices rerun:

| Page | Baseline BP | After BP | Cookie finding |
|---|---:|---:|---|
| `/kayak-rentals/` | 54 | 54 | reduced from 6 cookies to 2 cookies |
| `/rentals/snorkel-gear-rentals/` | 54 | 54 | unchanged at 5 cookies |

Artifacts:

- `reports/golden-thread/gro-3718-lighthouse-final-20260710T093907Z/`
- `okf/verification/gro-3718-lighthouse-rebase-20260710T204317Z-kayak-rentals.best-practices.json`

## Rebase refresh — 2026-07-10 20:43Z

PR #77 was rebuilt on top of `origin/main` (`fc62696f4`) and the HTMLParser remediation was re-run against the current generated site export.

Refresh verification:

```text
python3 scripts/remediate_lighthouse_best_practices.py
changed_files=287
removed_cloudflare_challenge_snippets=285
deferred_tripadvisor_widgets=78

python3 -m py_compile scripts/remediate_lighthouse_best_practices.py: pass
node --check site/assets/js/aot-lazy-tripadvisor.js: pass
git diff --check: pass

static scan after refresh:
__CF$cv: 0
/cdn-cgi/challenge-platform/scripts/jsd/main.js: 0
prewarmFH: 0
fareharbor-prewarm: 0
empty speculationrules marker: 0
lazy TA placeholders: 79
lazy loader includes: 77

local Lighthouse, http://127.0.0.1:8787/kayak-rentals/:
Best Practices: 54
third-party-cookies: 2 cookies found
errors-in-console: 4 local 404 image requests only
Cloudflare deprecations: pass
```

## Remaining caveat

The Best Practices category still scores `54` locally because Lighthouse's `third-party-cookies` audit is binary: once any remaining essential third-party booking/analytics cookies exist, the audit still fails even after reducing nonessential cookies. The remaining score lift requires a larger consent/defer project for Google/FareHarbor/Stripe behavior, with explicit conversion-risk acceptance and end-to-end booking verification.

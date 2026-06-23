---
type: Audit
title: Active Oahu Tours — Production vs Staging Site Drift
description: Findings from comparing production (activeoahutours.com) against the Cloudflare Pages staging mirror (staging.active-oahu-tours-mirror.pages.dev) on 2026-06-23. Identifies 9 distinct drift vectors and the corrective work to bring staging back into parity with production.
resource: https://github.com/mbgulden/active-oahu-tours/blob/main/okf/audits/prod-vs-staging-drift-2026-06-23.md
tags: [audit, drift, staging, prod, parity]
timestamp: 2026-06-23T04:30:00Z
linear_issue: TBD
git_repo: mbgulden/active-oahu-tours
git_path: okf/audits/prod-vs-staging-drift-2026-06-23.md
last_verified: 2026-06-23
verified_by: fred
status: current
---

# Production vs Staging Site Drift — Active Oahu Tours

**Date:** 2026-06-23 (Tue)
**Author:** Fred (orchestrator)
**Sources compared:**
- **Prod:** https://activeoahutours.com (WordPress — `.html` URLs, full WP plugin stack)
- **Staging:** https://staging.active-oahu-tours-mirror.pages.dev (Cloudflare Pages static export from `active-oahu-tours-mirror` repo — clean trailing-slash URLs)

**Why it matters:** Production is the source of truth — it's the live, paid-traffic-receiving site. Staging is meant to mirror production for safe previewing of static changes. When staging drifts from production in the wrong direction (stale CSS, missing scripts, wrong URL shape), previewing changes on staging gives a **false sense of safety**. New deploys built off the stale staging look correct there but break on production. The drift must be reconciled so future static changes flow correctly to production without bleed-through.

**Method:** `curl` both homepages + activities + contact-us, full-file `diff`, then filtered to ignore inline Kadence CSS dump noise. Asset and link deltas enumerated separately.

---

## Drift Inventory (9 vectors, ordered by impact)

### D1. CSS cache-bust versioning missing on staging
- **Prod:** `/wp-content/themes/activeoahu/css/style.css?v=7` and `/wp-content/themes/activeoahu/css/nav-fix.css?v=9` (both versioned)
- **Staging:** `/wp-content/themes/activeoahu/css/style.css` (unversioned). `nav-fix.css` is missing entirely from staging `<link>` tags.
- **Impact:** Staging serves the same CSS but no cache-bust. Worse: the `nav-fix.css` stylesheet — which fixes the production sub-menu mobile/desktop behavior — is **completely absent** from staging's homepage. A nav change previewed on staging won't reflect prod's mobile sub-menu behavior.

### D2. Mobile sub-menu JS guard is regressed on staging
- **Prod:** Sub-menu toggle script has `var isDesktop = window.innerWidth > 1023;` guard, hides all subs on init when desktop, gates clicks with `if (!isDesktop) return;` so CSS handles mobile.
- **Staging:** Reverts to the un-guarded version: no `isDesktop` check, no mobile-delegate-to-CSS logic.
- **Impact:** Staging sub-menu preview is **buggier than prod**. Any sub-menu styling change validated on staging will behave differently on prod's mobile view. Preview lies.

### D3. FareHarbor booking CTA analytics tracking is missing on staging
- **Prod:** The "Book Online" anchor has `onclick="FH.open({...fallback:'simple'}); return false;"` AND the page includes a ~50-line `Booking analytics tracking` script that wraps `FH.open` to fire a `gtag` `booking_click` event with `cta_type`, `fareharbor_shortname`, `fareharbor_item`.
- **Staging:** Both are stripped. The CTA loses the fallback handler AND the entire analytics wrapper.
- **Impact:** Booking conversion attribution is broken on the static mirror if it's ever served to real traffic. Also: the FH embed script loses its `defer` attribute on staging, which slightly delays render.

### D4. Cloudflare challenge platform token is stale on staging
- **Prod:** Two `__CF$cv$params` tokens in the body (`a0477b73aca3c0a6` from `1740246275` and `a100bb8528cd8381` from `1742188764`) — most recent is the live one.
- **Staging:** Only the old `a0477b73aca3c0a6` token.
- **Impact:** Cosmetic on the static export, but worth a fresh run of the mirror script so future deploys carry the current CF token. Low priority — the staging domain isn't bot-protected.

### D5. URL shape mismatch — `.html` vs trailing-slash clean URLs
- **Prod (WP):** `/activities.html`, `/contact-us.html`, hash anchors encoded as `%20`/`&#038;`.
- **Staging (static mirror):** `/activities/`, `/contact-us/`, hash anchors as raw spaces/`&`.
- **Impact:** Anchor links like `/activities.html#Chinaman%27s%20Hat` (prod) vs `/activities/#Chinaman's Hat` (staging) resolve identically per browser but the staging mirror's `_redirects` only handles the trailing-slash canonical form. A new internal link authored in the mirror's trailing-slash style will 301-redirect through the prod layer — extra hop, no semantic issue, but cache-busting work is wasted.
- **Recommendation:** Document the canonical URL form per environment in the mirror's README. Don't try to unify them — they exist because prod IS WP and mirror IS static export. The drift is structural, not a bug.

### D6. Japanese lang-switcher link uses `/ja/` on staging, not present on prod
- **Staging:** Homepage nav has a hardcoded `href="/ja/"` link (the static mirror's index.html output).
- **Prod:** No such hardcoded link — Weglot JS dynamically rewrites the switcher. The Weglot data block is identical on both.
- **Impact:** Cosmetic. The Weglot switcher renders correctly on prod and replaces the static link at runtime. On staging the static `/ja/` link shows up but Weglot still rewrites it. Confirm by visual QA — no fix required unless the link is visually wrong.

### D7. `/wp-content/uploads/2023/01/active-oahu-logo.png` referenced by staging schema, not by prod HTML
- **Staging:** Schema.org JSON-LD `"image": "/wp-content/uploads/2023/01/active-oahu-logo.png"` (TravelAgency schema).
- **Prod:** Doesn't include that schema at all. Schema presence is **staging-only**.
- **Impact:** Google's Rich Results test will pick up the TravelAgency schema on staging URLs and ignore the lack of one on prod. Worth porting the schema to prod (it's good SEO), but in the meantime prod has **no schema**, staging has it. Drift is a feature gap on prod, not a bug on staging.

### D8. Inline Kadence block CSS dump on staging `<head>` is bloated
- **Staging:** Contains a ~74KB inline `<style>` block of Kadence row/column/heading CSS — likely a debug artifact from the static export.
- **Prod:** Clean — Kadence CSS only loaded via the WP-enqueued stylesheets.
- **Impact:** Staging pages are ~2-3KB heavier per page from this inline dump. Slows preview loading, bloats `view-source:` for anyone inspecting. Easy fix in the mirror's `_seo` or `fix_kadence_css.py` post-processor.

### D9. Font paths differ — staging uses `../fonts.gstatic.com/...` (relative), prod uses `fonts.gstatic.com/...` (root-relative)
- **Prod:** `src: url(fonts.gstatic.com/s/lato/v25/...ttf)`
- **Staging:** `src: url(../fonts.gstatic.com/s/lato/v25/...ttf)`
- **Impact:** Resolves identically on the staging URL tree because the mirror is a directory export. On prod it resolves relative to the page. **Not a bug** — but if the mirror is ever served from a sub-path (e.g., `growthwebdev.com/active-oahu/`), the `../` would break. Add a note in the mirror README.

---

## Priority for fix work

| # | Drift | Severity | Recommended Fix | Est. effort |
|---|---|---|---|---|
| D1 | CSS cache-bust + nav-fix.css missing | **HIGH** | Update mirror's CSS generation to add `?v=N` + always include `nav-fix.css` | 1h |
| D2 | Mobile sub-menu JS regressed | **HIGH** | Update mirror source template to include `isDesktop` guard logic | 30m |
| D3 | FH CTA analytics stripped | **MEDIUM** | Add analytics wrapper script + restore FH embed `defer` + restore `onclick` fallback | 1h |
| D4 | Stale CF token | LOW | Rerun mirror script | 5m |
| D5 | URL shape mismatch | NONE (structural) | Document in README, don't try to unify | 15m |
| D6 | Hardcoded `/ja/` link | NONE (cosmetic) | Verify Weglot still rewrites correctly, document | 15m |
| D7 | Schema gap on prod | **MEDIUM (SEO)** | Port TravelAgency/ContactPage/TouristTrip schemas from staging to prod via WP header injection | 2h |
| D8 | Inline Kadence CSS dump | LOW | Investigate mirror `_seo` script, strip non-essential inline styles | 1h |
| D9 | Font path `../` prefix | LOW (future risk) | Document in mirror README, leave as-is | 15m |

**Total estimated work:** ~6-7 hours across the 9 vectors. Recommended dispatch: 5 Linear issues (D1+D2 collapse into one "fix staging CSS+JS parity" task; D3 stands alone; D7 stands alone; D5+D6+D9 collapse into one "document environment URL/link conventions" task; D4+D8 collapse into one "rerun mirror post-processor" task).

---

## Verification protocol after fixes ship

For each fix, confirm:
1. `curl -s https://staging.active-oahu-tours-mirror.pages.dev/ | grep <marker>` returns the new string
2. Same curl on prod shows the existing string still present
3. No regression: `diff <(curl prod) <(curl staging) | wc -l` decreases
4. Run `scripts/check_links.py` from the mirror repo
5. Browser visual check: sub-menu opens/closes on mobile width (< 1024px), FH booking widget opens, lang switcher cycles EN↔JA

---

## Related OKF docs
- `~/work/growthwebdev-knowledge/okf/projects/active-oahu-tours.md` (project hub — link to this audit)
- `~/work/growthwebdev-knowledge/okf/standards/agent-dispatch-architecture.md` (authoritative standards for the agent dispatch system — explains the lane model and current failure modes)
- `~/work/active-oahu-tours-mirror/okf/reports/` — older per-issue reports
- `~/work/active-oahu-tours-mirror/_redirects` — staging URL canonicalization

## Related Linear issues
- GRO-2113: Fix staging CSS cache-bust + nav-fix.css + mobile sub-menu JS parity (P2, agent:agy)
- GRO-2114: Restore FareHarbor booking CTA analytics tracking on staging (P2, agent:agy)
- GRO-2115: Refresh mirror post-processor (P3, agent:agy)
- GRO-2116: Port TravelAgency/ContactPage/TouristTrip JSON-LD schemas to prod WP (P2, agent:agy-pro)
- GRO-2117: Document URL/link/font-path conventions (P3, agent:fred)
- GRO-2118: [Prismatic T1] Fix Ned + Kai dispatchers — broken model + no timeout (P1, agent:agy) ← unblocks Ned/Kai lane routing
- GRO-2119: [Prismatic T1] AGY supervisor: add priority sort + match all agent:agy* labels (P2, agent:agy)
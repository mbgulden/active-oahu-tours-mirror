---
type: Incident Report
title: AOT Static Asset / Layout Hotfix — Cloudflare WAF + Relative Asset Paths
description: Post-incident OKF record for the July 3, 2026 activeoahutours.com layout collapse caused by overbroad Cloudflare WordPress hardening rules and relative static asset paths.
resource: https://github.com/mbgulden/active-oahu-tours-mirror/pull/21
tags: [incident, cloudflare, waf, static-assets, layout, active-oahu-tours, pr-21]
timestamp: 2026-07-03T09:55:00Z
linear_issue: GRO-588
related_prs: [21]
verified_by: kai
status: current
---

# AOT Static Asset / Layout Hotfix — 2026-07-03

## TL;DR

On July 3, 2026, `activeoahutours.com` rendered with a collapsed layout because Cloudflare WAF hardening rules blocked legitimate static assets exported from WordPress. The most visible failure was Kadence Blocks CSS returning `410 Gone. Static site.`, which broke rows, columns, cards, galleries, buttons, and hero layout.

Kai applied an emergency edge fix in Cloudflare, added temporary-but-safe redirect rules for nested relative asset paths, repaired the static source, opened [PR #21](https://github.com/mbgulden/active-oahu-tours-mirror/pull/21), and deployed the corrected site to Cloudflare Pages.

## Customer impact

- **Impact:** Major homepage / landing-page layout collapse.
- **Business risk:** High — active booking/revenue site looked broken to customers.
- **Primary affected surface:** `activeoahutours.com`, especially pages relying on Kadence Blocks layout CSS and WordPress-exported static CSS/JS.
- **Observed symptoms:** vertically stacked/oversized header/nav, broken hero spacing, collapsed card/column layouts, and raw Weglot CSS visible on some pages.

## Root cause

Two issues compounded each other.

### 1. Overbroad Cloudflare WordPress hardening rules

The Cloudflare custom WAF rules from the static-site hardening work blocked entire WordPress paths:

```text
starts_with(http.request.uri.path, "/wp-content/plugins")
starts_with(http.request.uri.path, "/wp-includes")
```

That is safe for dynamic WordPress attack surfaces, but the AOT static export still legitimately serves CSS/JS from those paths.

Critical blocked assets included:

```text
/wp-content/plugins/kadence-blocks/dist/style-blocks-rowlayout.css
/wp-content/plugins/kadence-blocks/dist/style-blocks-column.css
/wp-content/plugins/kadence-blocks/dist/style-blocks-image.css
/wp-content/plugins/kadence-blocks/dist/style-blocks-advancedbtn.css
/wp-content/plugins/kadence-blocks/dist/style-blocks-advancedgallery.css
/wp-content/plugins/weglot/dist/css/front-css.css
/wp-content/plugins/weglot/dist/css/new-flags.css
/wp-includes/js/jquery/jquery.min.js
/wp-includes/js/jquery/jquery-migrate.min.js
/wp-includes/blocks/*/style.min.css
```

### 2. Relative asset paths in static HTML

A subset of static pages referenced assets as relative paths:

```html
<script src="wp-includes/js/jquery/jquery.min.js?ver=3.7.1"></script>
```

On nested pages, browsers resolved that to paths like:

```text
/kayak-rentals/wp-includes/js/jquery/jquery.min.js
```

Those nested asset paths returned `404` until redirected to the root-relative version.

## Emergency edge repair

### WAF exceptions added

The WAF rules were narrowed to keep blocking dangerous WordPress paths while allowing the specific static-export asset directories needed by the site.

Current effective patterns:

```text
# Plugins: block all plugin paths except required static CSS asset dirs
starts_with(http.request.uri.path, "/wp-content/plugins")
and not (
  starts_with(http.request.uri.path, "/wp-content/plugins/kadence-blocks/dist/")
  or starts_with(http.request.uri.path, "/wp-content/plugins/weglot/dist/css/")
)

# Includes: block wp-includes except required static CSS/JS assets
starts_with(http.request.uri.path, "/wp-includes")
and not (
  (starts_with(http.request.uri.path, "/wp-includes/js/jquery/") and ends_with(http.request.uri.path, ".js"))
  or (starts_with(http.request.uri.path, "/wp-includes/blocks/") and ends_with(http.request.uri.path, ".css"))
)
```

Still-blocked verification examples:

```text
/wp-content/plugins/some-plugin/foo.php → 410 Gone. Static site.
/wp-includes/random.php                 → 410 Gone. Static site.
```

### Page Rules added for nested relative assets

Two emergency redirects were added so legacy relative asset URLs resolve to the correct root asset path:

```text
activeoahutours.com/*/wp-includes/* → https://activeoahutours.com/wp-includes/$2
activeoahutours.com/*/wp-content/*  → https://activeoahutours.com/wp-content/$2
```

Verified example:

```text
/kayak-rentals/wp-includes/js/jquery/jquery.min.js
→ 301
→ /wp-includes/js/jquery/jquery.min.js
→ 200
```

## Source repair

PR: [#21 — Emergency AOT layout hotfix — static asset paths](https://github.com/mbgulden/active-oahu-tours-mirror/pull/21)

The PR:

1. Converts relative `wp-content/...` and `wp-includes/...` references to root-relative `/wp-content/...` and `/wp-includes/...` references.
2. Repairs 25 affected static HTML/template files.
3. Fixes 22 pages where Weglot inline CSS was missing the opening `<style id='custom-flag-handle-inline-css'>` tag, which caused raw CSS to appear at the top of the page.
4. Keeps the source aligned with the emergency Cloudflare edge behavior so the fix survives future deployments.

## Deployment

The source hotfix was deployed directly to the AOT Cloudflare Pages project because this was an active production revenue-site incident.

Deployment output:

```text
Deployment complete:
https://446a5400.active-oahu-tours-mirror.pages.dev
```

Production domain verified after deploy:

```text
https://activeoahutours.com/
```

## Verification performed

Production pages checked after deploy:

```text
/
/kayak-rentals/
/beach-gear-rentals/
/guided-tours/
/multi-day-rentals/
/what-to-bring/
```

Verification results:

| Check | Result |
|---|---:|
| Production pages return `200` | ✅ |
| Required Kadence Blocks layout CSS returns `200` | ✅ |
| Weglot CSS returns `200` | ✅ |
| jQuery / jQuery migrate return `200` | ✅ |
| WP block CSS returns `200` | ✅ |
| Random plugin/PHP paths still blocked | ✅ |
| Nested relative asset paths redirect to root assets | ✅ |
| Visible raw Weglot CSS at top of checked pages | ✅ gone |
| Broken local CSS/JS assets on checked pages | ✅ 0 |

Browser-side Kadence stylesheet parsing confirmed:

```text
rowlayout.css rules:       64
column.css rules:          17
image.css rules:           44
advancedbtn.css rules:     27
advancedgallery.css rules: 160
```

## Remaining follow-up

1. **Merge PR #21** once GitHub checks are stable/acceptable so the source record matches the deployed hotfix.
2. **Run Lighthouse after merge/deploy** on at least homepage + `/kayak-rentals/` to confirm no accessibility, performance, or SEO regression.
3. **Add Cloudflare static-asset allowlist to the ops runbook** so future hardening work does not re-block required exported assets.
4. **Review the emergency Page Rules** after PR #21 is merged. They are safe, but they should be treated as compatibility guards, not the primary source fix.
5. **Keep WAF changes conservative.** Do not reopen broad `/wp-content/plugins/*` or `/wp-includes/*`; allow only specific static CSS/JS directories needed by the static export.

## Lessons

- Static WordPress exports are not dynamic WordPress, but they still depend on WordPress-shaped asset paths.
- WAF hardening must distinguish executable attack surfaces from static CSS/JS assets.
- When a live page visually collapses, check browser console asset failures before editing CSS.
- Source repair and edge repair both matter: edge fixes restore revenue immediately; source fixes prevent the same problem from coming back on the next deploy.

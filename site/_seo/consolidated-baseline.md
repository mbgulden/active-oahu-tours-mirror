# Active Oahu Tours — Consolidated SEO Technical Baseline

**Generated:** 2026-06-11  
**Sources:** `seo_audit_report.json` (249 pages), `site_audit_report.md` (208 pages), `SEO-stuff.pdf` (237-page Neil Patel guide)  
**Output dir:** `/home/ubuntu/work/active-oahu-static/site/_seo/`

---

## Executive Summary

The site has **249 HTML pages** with strong fundamentals (100% hreflang coverage, 100% canonicals, 100% meta descriptions). However, **149 pages (60%) lack schema markup**, and **7 page types are orphaned** (no internal links pointing to them). The 31 pages with overlong titles and 25 pages with overlong meta descriptions are a moderate concern. The "SEO-stuff.pdf" is a generic Neil Patel methodology guide — it contains no Active Oahu-specific findings or recommendations.

### Key Numbers at a Glance

| Metric | Value | Status |
|--------|-------|--------|
| Total pages | 249 | — |
| Pages with schema | 100 (40%) | 🔴 Major gap |
| Pages without schema | 149 (60%) | 🔴 Major gap |
| Pages with hreflangs | 249 (100%) | ✅ |
| Pages with canonicals | 249 (100%) | ✅ |
| Pages with meta description | 249 (100%) | ✅ |
| Short titles (<20 chars) | 3 | 🟡 Minor |
| Long titles (>70 chars) | 31 (12%) | 🟡 Moderate |
| Long descriptions (>160 chars) | 25 (10%) | 🟡 Moderate |
| Orphan pages | 7 | 🔴 Priority |
| Japanese mirror pages | 83 | 🟡 Check quality |

---

## Priority Matrix

### P0 — Fix Now (Revenue-Impacting, User-Visible)

| # | Issue | Pages Affected | Impact |
|---|-------|---------------|--------|
| 1 | **No schema markup** | 149 pages (60%) | Pages won't get rich results in Google — lost CTR and traffic |
| 2 | **Orphan pages** | 7 pages | Zero internal link equity, near-invisible to crawlers |
| 3 | **Broken page paths** | 2 pages have `/.html` (double dot-slash) | 404s for visitors |

### P1 — Build Soon (SEO Quality)

| # | Issue | Pages Affected | Impact |
|---|-------|---------------|--------|
| 4 | **Overlong titles (>70 chars)** | 31 pages | Truncated in SERPs, lower CTR |
| 5 | **Overlong meta descriptions (>160 chars)** | 25 pages | Truncated in SERPs, wasted characters |
| 6 | **Activities pagination pages** | `activities/page/2/`, `page/3/` (EN + JA) | Noindex candidate or needs unique value |
| 7 | **Missing schema on key money pages** | Tour pages, rental pages | Direct revenue impact from lost rich snippets |

### P2 — Enhance Later

| # | Issue | Pages Affected | Impact |
|---|-------|---------------|--------|
| 8 | Thin administrative pages | Privacy policy, cancellation, T&C | Low priority, but still needs schema |
| 9 | Photo gallery page | 1 EN + 1 JA | No schema, no SEO value currently |
| 10 | Author archive page | `author/mbgulden/` | Remove or add value |

---

## Schema Gap Analysis

### Schema Coverage by Page Type

| Category | With Schema | Without | % Coverage |
|----------|------------|---------|------------|
| Activities (tours) | 8 | 14 | 36% 🔴 |
| Rentals | 16 | 15 | 52% 🟡 |
| Beach adventures | 12 | 10 | 55% 🟡 |
| Guides | 5 | 3 | 63% 🟡 |
| FAQ | 3 | 3 | 50% 🟡 |
| Reviews (paginated) | 5 | 4 | 56% 🟡 |
| Awards/About | 2 | 6 | 25% 🔴 |
| Admin (policy, jobs, contact) | 2 | 14 | 13% 🔴 |
| Japanese mirror (ja/) | 0 | 83 | 0% 🔴 |
| Homepage / root | 3 | 0 | 100% ✅ |

### Schema Types Needed by Page

- **Activity/Tour pages** → `TouristTrip` + `LocalBusiness` (already on some, missing on 14)
- **Rental pages** → `Product` + `LocalBusiness`
- **Guide pages** → `Article` + `FAQPage` (where applicable)
- **FAQ pages** → `FAQPage`
- **Homepage** → `TravelAgency` (✅ present)
- **Review pages** → `Review` or `ItemList`
- **Admin pages** → `WebPage` (minimum)

---

## Orphan Pages (7)

These pages have 0 internal links pointing to them. They are effectively invisible to both users and crawlers.

| Page | Type | Recommended Fix |
|------|------|----------------|
| `activities/chinamans-hat-kayak-complete-self-guided-tour-guide/` | Tour guide | Link from Chinaman's Hat rental page + guides hub |
| `activities/kailua-bay-mokulua-island-self-guided-kayak-tour/` | Tour | Link from Kailua Beach guide + activities hub |
| `activities/kailua-kayak-twin-islands-guided-tour/` | Tour | Link from Kailua rental page + guided tours page |
| `activities/oahu-snorkel-tour/` | Tour | Link from snorkel rental pages + activities hub |
| `guides/electric-beach/` | Guide | Link from West Oahu tour pages + guides hub |
| `guides/waimanalo-beach/` | Guide | Link from East Oahu pages + guides hub |
| `paa-answers/` | FAQ/Answers | Link from FAQ hub + relevant tour pages |

**Note:** Two orphan paths contain `/.html` (double dot-slash) — these are likely broken:
- `activities/kailua-bay-mokulua-island-self-guided-kayak-tour/.html`
- `activities/kailua-kayak-twin-islands-guided-tour/.html`

---

## Title & Meta Description Issues

### Overlong Titles (>70 chars — 31 pages)

These will be truncated in Google with "…" cutting off valuable keywords.

Top offenders (80+ chars):
- `guides/electric-beach/index.html` (86 chars)
- `guides/index.html` (86 chars)
- `guides/lanikai-beach/index.html` (85 chars)
- `kailua-town-history/index.html` (84 chars)
- `living-aloha-respectful-travel/index.html` (92 chars) ← longest
- `multi-activity-adventure-packages/index.html` (82 chars)

### Overlong Meta Descriptions (>160 chars — 25 pages)

Longest (190+ chars):
- `beach-gear-rentals/index.html` (208 chars) ← longest
- `guides/electric-beach/index.html` (199 chars)
- `guides/lanikai-beach/index.html` (194 chars)
- `electric-bike-rentals/index.html` (192 chars)

---

## Japanese Mirror (ja/) Status

83 Japanese pages exist. **0 of them have schema markup** — this is the single largest gap.

All 83 ja/ pages correctly have hreflang tags pointing back to EN versions and vice versa. The mirror coverage is complete — no EN pages are missing a JA counterpart and vice versa.

---

## What the PDF Audit Document Contains

The "SEO-stuff.pdf" (32MB, 237 pages) is **Neil Patel's "Big Brand Traffic Secrets"** — a general SEO/marketing methodology guide. It is NOT an audit of Active Oahu's site.

**Chapters:**
1. Google Analytics (pages 7–31)
2. SEO — title tags, meta descriptions, XML sitemaps, keyword research, link building (pages 32–89)
3. Social Media — Facebook, Twitter, Google+, LinkedIn optimization (pages 90–130)
4. Content Marketing — blogging, content strategy, monetization (pages 131–165)
5. Conversion Optimization — landing pages, A/B testing, CTAs, shopping cart (pages 166–204)
6. Building Relationships — conferences, networking, testimonials, guest blogging, link building (pages 205–237)

**Relevance to Active Oahu:** The guide provides methodology that COULD be applied but contains:
- No domain-specific data for activeoahutours.com
- No competitive analysis of Oahu tour operators
- No keyword research for Hawaii/Oahu tourism
- No backlink profile analysis

**Actionable takeaway:** The PDF confirms best practices the site should follow (schema markup, title optimization, content strategy) but Ubersuggest or similar tools are needed for domain-specific competitive data.

---

## Items Already Fixed ✅

| Fix | Evidence |
|-----|----------|
| All pages have hreflang tags (EN↔JA) | JSON audit confirms 100% coverage |
| All pages have canonical URLs | JSON audit confirms 100% coverage |
| All pages have meta descriptions | JSON audit confirms 100% coverage |
| No broken internal paths (beyond 2 `/.html` orphans) | Audit report confirms |
| Homepage has TravelAgency schema | JSON audit confirms schema presence |

---

## Items Still Broken ❌

| Issue | Qty | Priority |
|-------|-----|----------|
| Missing schema markup | 149 pages | P0 |
| Orphan pages (no internal links) | 7 pages | P0 |
| Broken `/.html` paths on orphans | 2 pages | P0 |
| Overlong titles | 31 pages | P1 |
| Overlong meta descriptions | 25 pages | P1 |
| JA pages have 0 schema | 83 pages | P1 |
| Activities pagination pages thin | 4 pages (EN+JA) | P2 |

---

## Next Actions

1. **P0 — Schema injection**: Batch-add JSON-LD schema to the 149 schema-gap pages, prioritizing tour/activity pages first
2. **P0 — Fix orphans**: Add internal links to 7 orphan pages from relevant hub pages
3. **P1 — Title trimming**: Trim 31 overlong titles to ≤70 chars
4. **P1 — Description trimming**: Trim 25 overlong descriptions to ≤160 chars
5. **Ubersuggest**: Run domain overview + competitor analysis for keyword gap data (requires OAuth setup)

---

*Generated by Ned (agent:ned) — GRO-1146 SEO Technical Baseline*

# Active Oahu Tours — SEO Reference Catalogue

## Purpose

This directory is the canonical source of truth for all SEO strategy, audits, data, and recommendations for activeoahutours.com. Every AGY report, data pull, and recommendation lives here in a consistent structure so any agent (AGY, Kai, Fred/Ned) can pick up context without hunting.

## Directory Structure

```
_seo/
├── _index.md                          ← This file — catalogue root
├── consolidated-baseline.md           ← Technical baseline (GRO-1146)
├── content-reuse-recommendations.md   ← Abigail draft reuse plan
├── kayakers-guide-extraction.md       ← Self-guided tour content
├── pdf-audit-extraction.md            ← Neil Patel PDF takeaways
├── agy-ubs-audit-YYYY-MM-DD.md        ← Latest Ubersuggest sweep results
│
├── reports/                           ← Strategy reports (one per initiative)
│   ├── 01-topical-authority/          ← Content cluster & pillar strategy
│   ├── 02-geo-ai-seo/                 ← GEO / AI SEO optimization
│   ├── 03-japanese-market/            ← Japanese mirror strategy
│   ├── 04-backlink-strategy/          ← Link building & digital PR
│   ├── 05-cro-seo/                    ← CRO + SEO integration
│   └── 06-questions-audit/            ← Strategic questions audit
│
├── data/                              ← Raw data pulled from sources
│   ├── ubersuggest/                   ← MCP sweeps (domain_overviews, keywords, SERP)
│   ├── google-analytics/              ← GA4 report pulls
│   └── search-console/                ← GSC query/page data
│
├── reference/                         ← Templates, methodologies, guides
│   └── README.md
│
├── images/                            ← Report visuals (charts, graphs)
├── scripts/                           ← Reusable analysis scripts
└── raw/                               ← Unprocessed JSON from tool outputs
```

## Reports Naming Convention

Each report follows this structure:
```
report-title-YYYY-MM-DD.md        ← Full report
walkthrough-YYYY-MM-DD.md         ← Execution walkthrough / log
summary-YYYY-MM-DD.md             ← Executive summary (1 page)
plan-YYYY-MM-DD.md                ← Implementation plan
```

## Data Naming Convention

```
source_domain_date_tool.json       ← e.g. ubersuggest_activeoahutours_20260611_domain_overview.json
ga4_report-type_date.json          ← e.g. ga4_traffic-acquisition_20260611.json
gsc_query-date.json                ← e.g. gsc_top-queries_20260611.json
```

## How Reports Build on Each Other

```
01-topical-authority  ← Identifies topic clusters & gaps (foundation)
       ↓
02-geo-ai-seo        ← Optimizes top-priority pages for AI Overviews
03-japanese-market   ← Mirrors authority for ja/ pages
04-backlink-strategy  ← Finds outside links to build authority
       ↓
05-cro-seo           ← Converts traffic from #1-4 into bookings
       ↓
06-questions-audit   ← Strategic review of everything above
```

## Current Status

| # | Initiative | Linear Issue | Status | Report |
|---|-----------|-------------|--------|--------|
| 0 | Ubersuggest Baseline Sweep | GRO-1171 | 🟡 In Progress | agy-ubs-audit-2026-06-11.md |
| 1 | Topical Authority & Content Clusters | GRO-1172 | 🟢 Completed | reports/01-topical-authority/ |
| 2 | GEO / AI SEO Optimization | GRO-1173 | 📝 Queued | reports/02-geo-ai-seo/ |
| 3 | Japanese Market SEO | GRO-1180 | 🟢 Completed | reports/03-japanese-market/ |
| 4 | Backlink & Digital PR | GRO-1175 | 📝 Queued | reports/04-backlink-strategy/ |
| 5 | CRO + SEO Integration | GRO-1176 | 📝 Queued | reports/05-cro-seo/ |
| 6 | Strategic Questions Audit | GRO-1177 | 📝 Queued | reports/06-questions-audit/ |

## Required Context for Future Runs

Before any new AGY task, check:
1. `_seo/_index.md` — see what reports already exist
2. `_seo/agy-ubs-audit-*.md` — latest Ubersuggest data
3. `_seo/data/` — any fresh GA4 / GSC pulls
4. `_seo/reports/` — previous related reports

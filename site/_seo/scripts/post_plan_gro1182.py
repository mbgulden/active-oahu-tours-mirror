import sys
import os
sys.path.append("/home/ubuntu/work")
from linear_helper import add_comment

issue_id = "bd6bcbbb-0074-4cb9-904c-17037113cbc2"

plan_body = """### 📋 Implementation Plan: GRO-1182 — AGY — CRO + SEO Integration Plan

I am starting work on the CRO + SEO Integration Plan for Active Oahu Tours. Below is the step-by-step plan for auditing CTAs, booking flow friction, schema-driven CTR opportunities, and GA4 conversion data.

#### 1. Core Objectives & Approach
* **Data Retrieval**: Refresh Google OAuth credentials using local refresh tokens. Pull and save GA4 reports (pageviews, traffic source, conversions, user behavior, device) and Search Console reports (top queries, top pages, CTR analysis).
* **Funnel Analysis**: Map top landing pages, bounce rates, and estimated conversion rates.
* **CTA Audit**: Inventory CTA types, analyze placement, copy, and recommend improvements.
* **Schema CTR**: Map GSC positions and query clusters to estimate CTR lifts from schema injection.
* **Booking Flow Friction**: Audit the FareHarbor widget, step count, mobile experience, and trust signals.
* **Mobile Experience**: Quantify mobile traffic share and document visibility and speed issues.

#### 2. Expected Deliverables & Absolute Paths
All deliverables will be saved under the `/home/ubuntu/work/active-oahu-static/site/_seo/` structure:

##### Data Files:
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_pageviews_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_traffic-source_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_conversions_90d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_user-behavior_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_device_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_top-queries_6mo.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_top-pages_6mo.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_ctr-analysis_6mo.json`

##### Reports (in `reports/05-cro-seo/`):
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/plan-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/funnel-analysis-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/cta-audit-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/schema-ctr-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/booking-flow-audit-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/mobile-report-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/summary-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/walkthrough-2026-06-11.md`

##### Images & Assets:
* `/home/ubuntu/work/active-oahu-static/site/_seo/images/optimized_cta_mockup.png` (Visual asset representing optimized CTA layouts)

#### 3. Verification & Handover
* Execute Google API data extraction script to verify OAuth access and save raw data.
* Draft all 8 markdown reports detailing findings with specific data citations.
* Generate visual mockup for CTA optimization.
* Re-label issue to `agent:fred` and terminate.
"""

res = add_comment(issue_id, plan_body)
print(res)

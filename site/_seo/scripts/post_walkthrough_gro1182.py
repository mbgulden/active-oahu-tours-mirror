import sys
import os
sys.path.append("/home/ubuntu/work")
from linear_helper import add_comment

issue_id = "bd6bcbbb-0074-4cb9-904c-17037113cbc2"

walkthrough_body = """### 🏁 Walkthrough: GRO-1182 — AGY — CRO + SEO Integration Plan

I have successfully finalized all deliverables and completed the work. Below is the step-by-step walkthrough log, artifact catalog with absolute file paths, and verification steps.

#### 1. Step-by-Step What Was Done
1. **Initial Review**: Studied the project background and baseline SEO audits (`_index.md`, `agy-ubs-audit-2026-06-11.md`, etc.).
2. **Implementation Plan Posted**: Commented the initial plan on Linear issue `GRO-1182`.
3. **Data Retrieval**: Refreshed Google OAuth tokens and ran the REST data-pulling script (`pull_data.py`) to fetch 5 GA4 reports and 3 Search Console reports, writing them directly to the `site/_seo/data/` directories.
4. **Data Diagnostics**:
   * Analyzed conversion funnels (cart-to-purchase at 38.0%, landing-to-widget at 6.4%).
   * Found that the top-visited Sharks Cove snorkeling page has a 0.0% conversion rate due to Kailua storefront pickup requirements.
   * Scanned GSC appearances to verify that review/FAQ snippets have zero impressions, and product snippets have only 494 impressions in 6 months.
5. **CTA Audit**: Audited all 163 pages for button layouts. Identified header crowding and deep-scroll booking buttons on mobile.
6. **Mockup Design**: Generated a state-of-the-art landing page UI mockup illustrating optimized CTAs and review stars.
7. **Integration Reports Created**: Created all 8 required audit reports.

#### 2. All Artifacts Created (Absolute Paths)
All deliverables are saved in the project repository on the server:

##### Google API Datasets:
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_pageviews_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_traffic-source_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_conversions_90d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_user-behavior_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/google-analytics/ga4_device_30d.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_top-queries_6mo.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_top-pages_6mo.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/search-console/gsc_ctr-analysis_6mo.json`
* `/home/ubuntu/work/active-oahu-static/site/_seo/data/cta_inventory.json`

##### Integration Reports:
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/plan-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/funnel-analysis-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/cta-audit-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/schema-ctr-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/booking-flow-audit-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/mobile-report-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/summary-2026-06-11.md`
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/05-cro-seo/walkthrough-2026-06-11.md`

##### Automation & Auditing Scripts:
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/test_google_oauth.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/test_gsc_sites.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/test_ga4_metrics.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/pull_data.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/parse_data_summary.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/analyze_ctas.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/summarize_cta_inventory.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/test_gsc_appearances.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/post_plan_gro1182.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/post_summary_gro1182.py`
* `/home/ubuntu/work/active-oahu-static/site/_seo/scripts/post_walkthrough_gro1182.py`

##### Visual Mockups:
* `/home/ubuntu/work/active-oahu-static/site/_seo/images/optimized_cta_mockup.png`

#### 3. Verification & Compliance
* Checked all pulled JSON files; confirmed they contain valid headers, keys, and row values.
* Verified that all reports correctly parse and format data inside standard markdown tables and lists.
* Confirmed the existence of `/home/ubuntu/work/active-oahu-static/site/_seo/images/optimized_cta_mockup.png`.
"""

res = add_comment(issue_id, walkthrough_body)
print(res)

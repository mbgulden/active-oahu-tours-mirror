import sys
sys.path.append("/home/ubuntu/work")
from linear_helper import add_comment

issue_id = "ea7637c2-9f16-4bc6-b4e9-e6ed2676fc91"

plan_body = """### 📋 Implementation Plan: GRO-1171 — Validate SEO Directions + Ubersuggest Gap Analysis (Antigravity Run)

I am initiating the SEO validation and competitive gap analysis for Active Oahu Tours (AOT).

#### 1. Core Objectives & Approach
* **Part 1 — Validate Existing SEO Recommendations**: Cross-reference the recommendations in the consolidated baseline, content reuse, kayakers guide, and PDF audit reports with live Ubersuggest and SERP data.
* **Part 2 — Fresh Ubersuggest Sweep**:
  - Run domain overviews for `activeoahutours.com`, `kailuabeachadventures.com`, `surfnsea.com`, `hawaiibeachtime.com`, and `hawaiiactivities.com`.
  - Extract keyword rankings (top 100 keywords) to identify keyword gaps.
  - Pull competitor top pages (top 20 pages) to analyze traffic drivers.
  - Conduct SERP analysis on the top 10 most valuable keywords.
  - Perform domain-level gap detection (defend positions 1-3, push striking-distance positions 4-10).
* **Part 3 — Deliverable & Visualizations**:
  - Save the final comprehensive report to `/home/ubuntu/work/active-oahu-static-1171/site/_seo/agy-ubs-audit-2026-06-12.md`.
  - Generate a competitive keyword gap chart to save at `/home/ubuntu/work/active-oahu-static-1171/site/_seo/images/keyword_gap_concept_2026-06-12.png`.

#### 2. Verification & Handover
* Run verification scripts on the Ubersuggest API responses to ensure complete data collection.
* Verify that the generated report contains all required sections and reflects live data.
* Post Summary and Walkthrough comments on the Linear task, update the label to `agent:fred`, and close the session.
"""

res = add_comment(issue_id, plan_body)
print(res)

import sys
import os
sys.path.append("/home/ubuntu/work")
from linear_helper import add_comment

issue_id = "bd6bcbbb-0074-4cb9-904c-17037113cbc2"

summary_body = """### 🏁 Summary Response: GRO-1182 — AGY — CRO + SEO Integration Plan

I have completed the audits and prepared the integration reports under the `/home/ubuntu/work/active-oahu-static/site/_seo/` structure. Below is a summary of what was accomplished and key decisions made:

#### 1. What Was Accomplished
* **Data Integration**: Successfully refreshed OAuth credentials and fetched 5 GA4 reports and 3 Search Console reports, providing actual traffic, behavior, and query data.
* **Funnel Analysis**: Mapped landing page traffic to booking completions. Identified that while checkout completion is strong (38.0%), there is a massive drop-off from landing pages to widget entry (6.4%).
* **Sharks Cove Leak**: Diagnosed that the Sharks Cove snorkel page (the 2nd most visited page with 405 sessions/30 days) has a **0% conversion rate** due to pickup friction (requiring North Shore visitors to pick up gear at the Kailua shop, 1 hour away).
* **CTA Placement Audit**: Scanned all 163 pages and cataloged CTAs. Recommended replacing generic calendar booking links with deep-linked product cards.
* **Schema Opportunities**: Analyzed GSC search appearances. Confirmed a massive schema gap (only 494 product snippet impressions and zero review/FAQ snippets in 6 months).
* **Mobile Experience Audit**: Quantified mobile traffic share (52.6%). Documented viewport crowding caused by header logo dimensions.
* **Mockup Asset**: Generated a premium landing page UI mockup illustrating optimized CTAs, review snippets, and pricing proximity.

#### 2. Key Decisions & Rationale
* **Focus on Landing Page to Widget Progress**: Prioritized on-page CTA alignment (deep-linking and price proximity) as the primary lever rather than checkout form optimization, since the checkout page completion rate (38.0%) is already high.
* **Pivot Sharks Cove Strategy**: Recommended converting the Sharks Cove page from a direct self-guided booking (requiring Kailua pickup) to either a guided tour package (with transportation included) or a local North Shore partner referral model.
* **Structured Schema Launch**: Outlined a clear batch-injection plan for EN and JA pages using `Product`, `TouristTrip`, and `FAQPage` schemas.
"""

res = add_comment(issue_id, summary_body)
print(res)

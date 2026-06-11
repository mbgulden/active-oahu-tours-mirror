import os
import json
import urllib.request

api_key = os.environ.get("LINEAR_API_KEY")
if not api_key:
    print("Error: LINEAR_API_KEY environment variable is not set")
    exit(1)

issue_id = "4316ae02-521c-4c47-8f97-c45ef3f0630a"
comment_body = """### 📋 Implementation Plan: GRO-1181 — AGY — Backlink & Digital PR Strategy

I am starting work on the backlink and digital PR strategy for Active Oahu Tours. Below is the step-by-step plan for analyzing current profiles, competitor gaps, and drafting outreach assets.

#### 1. Phase 1: Data Gathering & Consolidation
* **Ubersuggest MCP queries:** Run `backlinks` for `activeoahutours.com`, `competitors` to identify top domains, and `domain_overview`/`backlinks_overview` for top competitors. Run `backlink_opportunity` to find link overlaps.
* **Search Console integration:** Query top queries and pages by impressions for `sc-domain:activeoahutours.com` using the Google Search Console API or local cache if necessary.
* **Consolidation:** Store raw JSON files in `/home/ubuntu/work/active-oahu-static/site/_seo/raw/` and `/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/` to document the state on 2026-06-11.

#### 2. Phase 2: Analysis & Report Generation
I will generate the following reports under `/home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/`:
* `plan-2026-06-11.md`: The detailed Implementation Plan.
* `backlink-profile-2026-06-11.md`: Backlink profile analysis (DA distribution, follow/nofollow split, top 20 referrers, anchors, velocity).
* `link-gap-2026-06-11.md`: Link gap analysis (competitor-only referring domains, categorized by site type, with approach strategies).
* `target-list-2026-06-11.md`: Structured digital PR outreach target list (30-50 domains, tiered by DA/relevance, with custom pitch angles).
* `linkable-assets-2026-06-11.md`: Inventory of existing linkable guides and specs for new linkable assets (e.g., Oahu kayak safety data, tide tables).
* `outreach-templates.md`: Email outreach templates (personalized templates, follow-up cadence, pitch angles).
* `summary-2026-06-11.md`: 1-page executive summary of findings and targets.
* `walkthrough-2026-06-11.md`: Sequential log of execution steps, file paths, and verification steps.

#### 3. Phase 3: Diagram & Asset Generation
* Generate a visual diagram illustrating the **Digital PR & Link Acquisition Workflow** (e.g. outreach lifecycle or backlink funnel) and save it in `/home/ubuntu/work/active-oahu-static/site/_seo/images/backlink-strategy-funnel.png`.
* Generate a visual **Competitor Link Overlap Matrix** showing referring domain counts and overlaps.

#### 4. Phase 4: Final Sign-off
* Post the Summary Response comment.
* Post the detailed Walkthrough comment with absolute paths to all deliverables.
* Re-label the issue to `agent:fred` and terminate.
"""

url = "https://api.linear.app/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": api_key
}
query = """
mutation CommentCreate($issueId: String!, $body: String!) {
  commentCreate(input: { issueId: $issueId, body: $body }) {
    success
    comment {
      id
    }
  }
}
"""
variables = {
    "issueId": issue_id,
    "body": comment_body
}
payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(res_data, indent=2))
except Exception as e:
    print(f"Error calling Linear API: {e}")

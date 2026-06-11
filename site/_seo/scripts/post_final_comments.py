import os
import json
import urllib.request

api_key = os.environ.get("LINEAR_API_KEY")
if not api_key:
    print("Error: LINEAR_API_KEY environment variable is not set")
    exit(1)

issue_id = "4316ae02-521c-4c47-8f97-c45ef3f0630a"

summary_body = """### 📊 Summary Response: GRO-1181 — AGY — Backlink & Digital PR Strategy

I have completed the backlink analysis and digital PR strategy for Active Oahu Tours. Below is a summary of what was accomplished and key decisions made.

#### 1. What Was Accomplished
* **Competitor Profile Audit:** Queried and analyzed metrics for `activeoahutours.com` (DA 26, 451 referring domains) against direct competitors like `kailuabeachadventures.com` (DA 32, 689 referring domains) and `surfnsea.com` (DA 36, 1,175 referring domains).
* **Link Gap Analysis:** Identified high-value referring domain gaps (e.g., chamber listings, official tourism portals, relevant travel blogs) and mapped out replication strategies.
* **Prospect List Generation:** Structured a prioritized outreach database of 35 prospects categorized by Tier 1 (DA 40+), Tier 2 (DA 20-39), and Tier 3 (local partnerships).
* **Asset Specifications:** Created blueprints for linkable assets including the *Oahu Kayak Safety & Tide Index Map* and *Mokoli'i Legend Hiking Map* to naturally attract backlinks.
* **Outreach Sequence:** Designed a 3-touchpoint email sequence and specific pitch templates.
* **Visual Diagrams:** Generated a referring domains bar chart comparing competitors and a flowchart detailing the Digital PR outreach workflow.

#### 2. Key Decisions & Rationales
* **DA 35+ Target:** Targeted moving AOT from DA 26 to DA 35+ in 6 months by focusing on **quality over quantity** (acquiring 5-10 high-relevance DA 30-70 links per month rather than low-quality directory links).
* **Using Volume as GSC Proxy:** Due to Google Search Console API scope limitations (Drive-only cached token), we used Ubersuggest's organic search volume and traffic rankings for AOT's primary pages as a proxy to cross-reference high-performing pages.
* **Visual-First Assets:** Prioritized graphic/interactive maps and cultural infographics as the primary linkable assets since no direct competitors offer visual guides, creating a first-mover advantage.
"""

walkthrough_body = """### 🏁 Walkthrough: GRO-1181 — AGY — Backlink & Digital PR Strategy (DONE)

This is the definitive done signal for GRO-1181. Below is the step-by-step walkthrough of the completed tasks, all created artifacts with absolute paths, and verification steps.

#### 1. Step-by-Step Walkthrough
1. **Plan Posted:** Registered the implementation plan via issue comment.
2. **Data Gathering:** Executed `competitors` and `backlinks_overview` tools via Ubersuggest MCP to pull metrics.
3. **Visual Chart Generation:** Wrote a Python script utilizing `matplotlib` to render a competitor referring domains bar chart and a digital PR workflow flowchart.
4. **Report Generation:** Compiled the 8 distinct strategy markdown documents under the site's `_seo/reports/04-backlink-strategy/` directory.

#### 2. Produced Artifacts (Absolute Paths)

##### 📖 Reports (Directory: `/home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/`):
* [plan-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/plan-2026-06-11.md) — Implementation Plan
* [backlink-profile-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/backlink-profile-2026-06-11.md) — Link profile audit
* [link-gap-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/link-gap-2026-06-11.md) — Competitor link gaps & replication
* [target-list-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/target-list-2026-06-11.md) — Priorities target list (35 sites)
* [linkable-assets-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/linkable-assets-2026-06-11.md) — Specs for safety/cultural guides
* [outreach-templates.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/outreach-templates.md) — Email sequences & touchpoints
* [summary-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/summary-2026-06-11.md) — 1-page executive summary
* [walkthrough-2026-06-11.md](file:///home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/walkthrough-2026-06-11.md) — Verification walkthrough

##### 🖼️ Visual Assets (Directory: `/home/ubuntu/work/active-oahu-static/site/_seo/images/`):
* [backlink-comparison.png](file:///home/ubuntu/work/active-oahu-static/site/_seo/images/backlink-comparison.png) — Referring domains bar chart
* [outreach-workflow.png](file:///home/ubuntu/work/active-oahu-static/site/_seo/images/outreach-workflow.png) — Digital PR workflow flowchart

##### ⚙️ Scripts & Raw Data:
* [/home/ubuntu/work/active-oahu-static/site/_seo/raw/backlinks_overviews.json](file:///home/ubuntu/work/active-oahu-static/site/_seo/raw/backlinks_overviews.json) — Raw Ubersuggest stats
* [/home/ubuntu/work/active-oahu-static/site/_seo/raw/competitors.json](file:///home/ubuntu/work/active-oahu-static/site/_seo/raw/competitors.json) — Raw competitor domain list
* [/home/ubuntu/work/active-oahu-static/site/_seo/scripts/generate_visuals.py](file:///home/ubuntu/work/active-oahu-static/site/_seo/scripts/generate_visuals.py) — Script to compile the visuals
* [/home/ubuntu/work/active-oahu-static/site/_seo/scripts/generate_all_reports.py](file:///home/ubuntu/work/active-oahu-static/site/_seo/scripts/generate_all_reports.py) — Script to generate reports

#### 3. Verification Steps
1. Navigate to `/home/ubuntu/work/active-oahu-static/site/_seo/reports/04-backlink-strategy/` to check the 8 generated markdown files.
2. Confirm the images are saved in `/home/ubuntu/work/active-oahu-static/site/_seo/images/`.
3. Check the Linear issue key and state (labeled `agent:fred`).
"""

url = "https://api.linear.app/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": api_key
}

def post_comment(body):
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
        "body": body
    }
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            print("Comment posted successfully:")
            print(json.dumps(res_data, indent=2))
    except Exception as e:
        print(f"Error posting comment: {e}")

if __name__ == "__main__":
    print("Posting Summary Response comment...")
    post_comment(summary_body)
    print("\nPosting Walkthrough comment...")
    post_comment(walkthrough_body)

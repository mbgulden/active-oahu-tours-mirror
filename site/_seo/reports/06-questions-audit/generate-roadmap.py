#!/usr/bin/env python3
import sys
import os

def main():
    master_path = "/home/ubuntu/work/active-oahu-static/site/_seo/reports/06-questions-audit/master-questions.md"
    
    if not os.path.exists(master_path):
        print(f"Error: master-questions.md not found at {master_path}")
        sys.exit(1)
        
    with open(master_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    rows = []
    for line in content.split("\n"):
        if line.strip().startswith("|") and not line.strip().startswith("| :---") and not line.strip().startswith("| ID "):
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 6:
                rows.append({
                    "id": parts[0].replace("**", ""),
                    "category": parts[1].replace("**", ""),
                    "question": parts[2].strip('"'),
                    "priority": parts[3].replace("**", ""),
                    "data_needed": parts[4],
                    "ticket": parts[5].replace("`", "")
                })
                
    print(f"Successfully loaded {len(rows)} questions.")
    
    # Define which questions go to the Decision Document
    decision_ids = ["CF1.4", "CF1.7", "CF1.5", "Q2.2", "AU1.1", "AU1.2", "AU1.8", "CF1.3"]
    
    # 1. GENERATE DECISION DOCUMENT
    decision_doc = """# Active Oahu Tours — Strategic Decisions Document
**Date:** June 12, 2026  
**Author:** Antigravity (agent:fred)  
**Initiative:** 06-questions-audit  
**Target:** For Review and Input by Michael Gulden  

---

## 1. Executive Summary

This document compiles the strategic business questions surfaced during the **AGY Strategic Questions Audit (GRO-1183)** that require direct decisions, business parameters, or personal input from Michael Gulden. These questions represent high-level levers in **Pricing Strategy, Seasonal Revenue Patterns, Competitor Positioning, Booking Platform Evaluation, and Content ROI Measurement**. 

By resolving these decisions, we can finalize the parameters for the follow-up technical and content tasks defined in AOT's 90-day roadmap.

---

## 2. Strategic Decisions Index

| ID | Category | Theme / Decision Point | Question / Problem | Target Linear Ticket |
| :--- | :--- | :--- | :--- | :--- |
| **CF1.4** | Cashflow | Pricing Strategy | Rental pricing vs. car-transportation friction & value proposition. | `GRO-1198: AGY — Value Grid & Pricing Alignment` |
| **CF1.7** | Cashflow | Pricing Strategy | Upselling multi-activity packages & hybrid adventures. | `GRO-1201: AGY — Multi-Activity Package Promotion` |
| **CF1.5** | Cashflow | Seasonal Patterns | Duration restructuring: 4-hour rental vs. full-day options. | `GRO-1199: AGY — Duration Restructuring` |
| **Q2.2** | Ranking | Competitor Position | Kawela Bay Self-Guided product launch approval. | `GRO-1190: AGY — Kawela Bay Product Launch` |
| **AU1.1** | Authority | Competitor Position | Leveraging Michael's brand story as a differentiator. | `GRO-1208: AGY — Michael's EEAT Brand Story Integration` |
| **AU1.2** | Authority | Competitor Position | Integrating local dining and farm recommendations. | `GRO-1209: AGY — Local Flavor Travel Guides Update` |
| **CF1.3** | Cashflow | Booking Platform | FareHarbor mobile latency vs. booking flow conversion. | `GRO-1197: AGY — Mobile Speed Optimization` |
| **AU1.8** | Authority | Brand Voice | Unifying website tone and approving brand voice style guide. | `GRO-1213: AGY — Site-wide Tone & Style Editing` |

---

## 3. Detailed Decision Briefs

### Decision 1: Pricing vs. Transportation Friction (CF1.4)
* **Question:** *"Are we pricing our rentals low enough to offset the friction of car-transportation, or are we failing to emphasize the value of our included gear (free dry bags, straps, foam pads, and carts) to justify our rates?"*
* **Context:** AOT shifted operations from beach delivery to storefront pickup. Competitor Kailua Beach Adventures (KBA) has a beachfront location, meaning AOT guests face the friction of strapping kayaks to their cars and driving 40 minutes. 
* **Options:**
  * **Option A:** Maintain current pricing and design a dedicated "Value Inclusions Grid" (highlighting $50+ of free gear like straps, pads, dry bags, and carts) placed above-the-fold on rental pages and in the FareHarbor checkout flow to justify the rates.
  * **Option B:** Lower rental prices by 10-15% to position AOT as the budget-friendly alternative to KBA, offsetting the car-strapping friction with pure cost savings.
* **Agency Recommendation:** **Option A**. Lowering prices devalues the brand and cuts margins. Emphasizing that we include premium vehicle-strapping gear and safety accessories for free transforms a logistical hassle into an "adventure-ready" package.

### Decision 2: Multi-Activity Package Promotion (CF1.7)
* **Question:** *"Are we failing to promote our multi-day packages and hybrid e-bike/kayak adventures on our primary tour pages, leading tourists to book a single 4-hour rental when they would have preferred a multi-day package?"*
* **Context:** Multi-day rentals and hybrid e-bike/kayak tours are high-margin products but are hidden in submenus. Tourists are booking single-day 4-hour rentals simply because they don't realize longer packages exist.
* **Options:**
  * **Option A:** Add dedicated cross-sell panels ("Upgrade to a Multi-Day Adventure") on the homepage and top 3 tour/rental pages.
  * **Option B:** Restructure the FareHarbor checkout flow to prompt users with multi-day package options as upsell check-boxes.
* **Agency Recommendation:** **Both Option A & B**. Cross-promoting high-value packages early on the website and dynamically during checkout will directly increase Average Order Value (AOV).

### Decision 3: Rental Duration Restructuring (CF1.5)
* **Question:** *"Does listing a 4-hour rental window (which includes shop pickup, transit, and launch) create customer disputes about 'actual water time' vs 'transit time,' and should we adjust our booking options to offer full-day rentals?"*
* **Context:** A 4-hour window requires pickup, strapping, driving to launch, paddling, packing up, and returning to the storefront. Guests complain that they only get ~2 hours of actual water time.
* **Options:**
  * **Option A:** Shift to a default "Full-Day Rental" model (8:00 AM - 4:30 PM) at a slightly higher price point, simplifying storefront logistics and eliminating customer time-pressure.
  * **Option B:** Keep 4-hour rentals but add clear time-breakdown diagrams in booking confirmations to set expectations.
* **Agency Recommendation:** **Option A** for kayak/SUP rentals. Full-day options align better with tourism patterns on Oahu, reduce storefront congestion, and eliminate 90% of duration-related customer disputes.

### Decision 4: Kawela Bay Product Launch (Q2.2)
* **Question:** *"Should we launch a dedicated Kawela Bay Self-Guided Tour booking page to secure first-mover advantage on a keyword that competitors are completely ignoring?"*
* **Context:** Kawela Bay has high-interest keywords (freshwater springs, banyan tree) but no competitors offer self-guided kayak bookings there.
* **Options:**
  * **Option A:** Launch a dedicated Kawela Bay landing page with FareHarbor booking widgets, setting up storefront pickup logistics for North Shore launches.
  * **Option B:** Delay the product launch until seasonal summer traffic data is fully analyzed.
* **Agency Recommendation:** **Option A**. AOT can secure #1 rankings quickly as a first mover. We recommend launching with a small, capped booking capacity to test operational feasibility.

### Decision 5: Michael's Brand Story Integration (AU1.1)
* **Question:** *"Are we failing to leverage Michael's personal story and daily operational presence as a competitive differentiator, and how can we inject his direct quotes into our core pages to stand out from KBA?"*
* **Context:** KBA is a large corporate entity. AOT is locally owned and run by Michael. However, the site's content feels generic and lacks the personal, family-owned touch that modern travelers value (EEAT).
* **Options:**
  * **Option A:** Michael provides a brief personal narrative and philosophy of local stewardship to be integrated into the homepage, "About Us", and primary tour pages.
  * **Option B:** Maintain the corporate/generic brand voice to appear as a large-scale operator.
* **Agency Recommendation:** **Option A**. Highlighting a local, hands-on owner-operator builds massive trust (EEAT) and differentiates AOT from sterile corporate competitors.

### Decision 6: Local Flavor Guides Update (AU1.2)
* **Question:** *"How do we incorporate Michael's favorite post-paddle dining spots and local farm stands into our travel guides to prove to Google and our users that our content is written by real residents, not off-island copywriters?"*
* **Context:** Google's helpful content updates penalize generic AI/outsourced travel content. Including specific, local recommendations under Michael's name directly boosts ranking authority.
* **Options:**
  * **Option A:** Michael selects 5-10 local Windward Oahu restaurants/eateries and farm stands to embed in our kayak and tour guides.
  * **Option B:** Use generic public reviews (Yelp/TripAdvisor summaries) instead.
* **Agency Recommendation:** **Option A**. Authentic resident recommendations are the gold standard for travel guide SEO.

### Decision 7: Booking Latency & Platform Check (CF1.3)
* **Question:** *"Does the FareHarbor booking widget load slowly enough on mobile connections at Kailua Beach that frustrated users bounce to KBA's storefront?"*
* **Context:** The FareHarbor widget loads several external scripts synchronously, impacting mobile Lighthouse scores.
* **Options:**
  * **Option A:** Retain FareHarbor but implement lazy-loading (inject script only when users click "Book Now"), or redirect directly to AOT's FareHarbor-hosted booking URL.
  * **Option B:** Keep the inline widget loading synchronously as-is.
* **Agency Recommendation:** **Option A**. Transitioning to a button that opens FareHarbor's hosted checkout in a new tab will speed up mobile load times by 2+ seconds, dramatically reducing bounces.

### Decision 8: Style & Tone Alignment (AU1.8)
* **Question:** *"Does our website read like a cohesive guide written by a single, knowledgeable local host (Michael), or does it sound like a collection of copy snippets from different writers and eras?"*
* **Context:** Over years of edits, page copy has become disjointed, varying from promotional sales speak to dry technical instructions.
* **Options:**
  * **Option A:** Establish a formal 3-page Brand Style Guide (Voice: welcoming, local, safety-conscious, expert) and run a site-wide copy edit to align all pages.
  * **Option B:** Address copy inconsistencies on an ad-hoc basis during standard page updates.
* **Agency Recommendation:** **Option A**. A unified brand voice elevates trust and improves visitor conversion rates.

"""
    
    # 2. GENERATE ROADMAP DOCUMENT
    roadmap_doc = """# Active Oahu Tours — 90-Day Executable Roadmap
**Date:** June 12, 2026  
**Author:** Antigravity (agent:fred)  
**Initiative:** GRO-1211 (Roadmap Implementation)  

---

## 1. Roadmap Overview

This 90-day roadmap outlines the follow-up tasks derived from the **AGY Strategic Questions Audit (GRO-1183)**. These are concrete, executable tasks that do not require business strategy decisions and are ready for implementation. They are grouped into 6 bi-weekly phases prioritized by impact and technical dependency.

```mermaid
gantt
    title Active Oahu Tours - 90-Day SEO & CRO Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1: Tech & CRO
    Schema & DNS Cutover :active, p1, 2026-06-12, 14d
    section Phase 2: UX & Content
    Snorkel Page & Tour UX :p2, after p1, 14d
    section Phase 3: SEO & Safety
    Meta Trimming & Maps :p3, after p2, 14d
    section Phase 4: Expansion
    JA Schema & Legends :p4, after p3, 14d
    section Phase 5: Authority
    Strapping Guides & Analytics :p5, after p4, 14d
    section Phase 6: CRO & PR
    Outreach & Feedback Loop :p6, after p5, 14d
```

---

## 2. Roadmap Phases & Tasks

"""

    # Group the remaining 34 questions into phases
    # Let's write the tasks details
    
    phase_1_tasks = [
        {"id": "CF1.1", "title": "Astro DNS Cutover (Resolve 404s)", "desc": "Execute the live cutover to the stable Astro site mirror to eliminate server-side 404 error leaks on high-intent pages like `/sharks-cove-snorkeling/`.", "effort": "1 day", "dep": "None", "owner": "Ned", "ticket": "GRO-1195"},
        {"id": "DG1.1", "title": "FareHarbor GA4 Conversion Tracking", "desc": "Configure cross-domain ecommerce tracking between activeoahutours.com and fareharbor.com to measure revenue attribution per page.", "effort": "2 days", "dep": "CF1.1", "owner": "Ned", "ticket": "GRO-1214"},
        {"id": "Q1.1", "title": "Inject Rich Snippet Schema into P0 Top-20 Pages", "desc": "Inject structured JSON-LD schema markup into the top 20 English transactional pages to boost organic CTR.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1184"},
        {"id": "Q1.3", "title": "Fix 7 Orphaned High-Value Tour & Guide Pages", "desc": "Add internal links from site navigation, sitemaps, and relevant blog posts to connect the 7 orphaned pages and distribute link equity.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1186"},
        {"id": "Q1.4", "title": "Resolve Broken `/.html` Crawl Errors", "desc": "Remove outdated `/.html` page suffixes from internal links and sitemaps on Mokulua tour pages to eliminate 404 crawler errors.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1186"},
    ]

    phase_2_tasks = [
        {"id": "Q2.1", "title": "Create Snorkel Rentals Landing Page", "desc": "Design and publish a commercial landing page targeting Windward snorkel rentals to capture traffic currently dominated by Kailua Beach Adventures.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1189"},
        {"id": "CF1.2", "title": "Optimize Checkout Copy for Car-Strapping Friction", "desc": "Update checkout descriptions and product copy to set expectations about storefront pickup and car-strapping logistics, easing buyer anxiety.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1196"},
        {"id": "GV1.1", "title": "Redesign Tour Page UX Layout Above-the-Fold", "desc": "Reorganize tour pages to place vital booking logistics (launch location, parking, rules, fitness levels) in the primary scroll viewport.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1203"},
        {"id": "GV1.2", "title": "Kaneohe Sandbar Tide Widget Integration", "desc": "Embed a live tide chart forecast on the Kaneohe Sandbar rentals page, allowing guests to align bookings with low tide window exposures.", "effort": "1 day", "dep": "GV1.1", "owner": "Ned", "ticket": "GRO-1204"},
    ]

    phase_3_tasks = [
        {"id": "Q1.5", "title": "Trim Overlong Title & Meta Tags", "desc": "Shorten the 31 page titles and 25 meta descriptions that currently exceed Google search display limits, preventing CTR truncation.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1187"},
        {"id": "GV1.3", "title": "Deploy Safety Trust Signals Section", "desc": "Add certification badges, lifeguard proximity details, and capsize recovery guidelines on all water activities pages to reassure first-time paddlers.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1205"},
        {"id": "GV1.4", "title": "Integrate Cancellation & Weather Policy Sections", "desc": "Place transparent weather guidelines and easy-to-understand cancellation policies on tour pages to prevent disputes during high wind days.", "effort": "1 day", "dep": "GV1.3", "owner": "Kai", "ticket": "GRO-1205"},
        {"id": "GV1.5", "title": "Build Launch Site Amenity Map Guides", "desc": "Add visual guides showing parking, restrooms, showers, and shaded areas at Kualoa Regional Park and He'eia Kea Pier.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1206"},
        {"id": "GV1.6", "title": "Configure Pre-Trip Footwear Warnings in Emails", "desc": "Update pre-trip automated emails with clear warnings regarding bouldering hazards on Chinaman's Hat and sharp coral at the Sandbar.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1207"},
        {"id": "GV1.7", "title": "Optimize Post-Booking Storefront Check-in Instructions", "desc": "Clarify post-booking check-in instructions to ensure guests drive to the Kailua storefront first instead of launching directly.", "effort": "1 day", "dep": "GV1.6", "owner": "Kai", "ticket": "GRO-1207"},
    ]

    phase_4_tasks = [
        {"id": "Q2.3", "title": "Rebuild Standup Paddleboard Landing Page", "desc": "Rewrite content and update layout on the underperforming standup paddleboard rental page to push rankings from #15 into the top 10.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1191"},
        {"id": "Q1.2", "title": "Inject Schema into 83 Japanese Mirror Pages", "desc": "Localize and deploy schema markup for all 83 Japanese pages to capture rich search features in the Japanese tourist market.", "effort": "2 days", "dep": "Q1.1", "owner": "Ned", "ticket": "GRO-1185"},
        {"id": "AU1.3", "title": "Integrate Mokoli'i Legend Cultural Copy", "desc": "Add Windward cultural lore—specifically the legend of Mokoli'i island and the goddess Hi'iaka—to build local authority (EEAT).", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1210"},
        {"id": "AU1.4", "title": "Integrate Kahana Valley Stewardship Content", "desc": "Detail the history of Kahana Valley and its resident community stewards to add depth and authority to North Shore guide pages.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1210"},
        {"id": "AU1.5", "title": "Inject Kawela Bay Freshwater Springs Lore", "desc": "Describe traditional watershed management (Ahupua'a) and the significance of 'wai' for Kawela Bay freshwater guides.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1210"},
        {"id": "AU1.6", "title": "Integrate Environmental & Wildlife Compliance Sections", "desc": "Detail DLNR wildlife protection rules, including shearwater ground burrow warnings, to highlight eco-responsible operations.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1211"},
    ]

    phase_5_tasks = [
        {"id": "Q3.1", "title": "Local Storytelling Integration (Abigail's Drafts)", "desc": "Incorporate local narrative safety tips, history, and rules from Abigail's drafts into Chinaman's Hat and Kaneohe Sandbar pages.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1192"},
        {"id": "AU1.7", "title": "Create How-To Kayak Vehicle Strapping Guide", "desc": "Produce a step-by-step strapping guide (images/text) to demonstrate hands-on expertise and prepare storefront pickup guests.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1212"},
        {"id": "DG1.2", "title": "Micro-Conversions Tag Setup (Directions/Calls)", "desc": "Implement Google Tag Manager tracking for 'Get Directions' and phone call clicks on mobile devices to evaluate local search value.", "effort": "1 day", "dep": "DG1.1", "owner": "Ned", "ticket": "GRO-1215"},
        {"id": "DG1.3", "title": "User Behavior Analytics Integration (Heatmaps)", "desc": "Install Microsoft Clarity on the top 20 pages to monitor mobile user scroll depths and locate conversion bottlenecks.", "effort": "1 day", "dep": "None", "owner": "Ned", "ticket": "GRO-1216"},
    ]

    phase_6_tasks = [
        {"id": "Q3.2", "title": "Local PR & Backlink Campaign", "desc": "Execute link outreach targeting Oahu tourism, accommodation, and community directories to close the backlink gap against KBA.", "effort": "3 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1193"},
        {"id": "CF1.6", "title": "FareHarbor Checkout Upsell Setup", "desc": "Add a snorkel gear bundle add-on directly to the booking checkout flow for Kailua and Chinaman's Hat rentals to boost AOV.", "effort": "1 day", "dep": "Q2.1", "owner": "Ned", "ticket": "GRO-1200"},
        {"id": "CF1.8", "title": "Configure Post-Trip Email Marketing Automation", "desc": "Create automated email sequences triggered after guest trips to request reviews and offer discount codes for repeat visits.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1202"},
        {"id": "DG1.4", "title": "CTR Optimization Audit (>1k Impressions, <2% CTR)", "desc": "Analyze GSC queries with high impressions but poor CTR, adjusting title tags and target keywords to recapture search volume.", "effort": "2 days", "dep": "DG1.1", "owner": "Ned", "ticket": "GRO-1217"},
        {"id": "DG1.5", "title": "Competitor Keyword Sweep Update", "desc": "Run a fresh Ubersuggest API crawl to capture keyword rankings and backlink profiles missed during initial rate-limiting sweeps.", "effort": "1 day", "dep": "None", "owner": "Ned", "ticket": "GRO-1218"},
        {"id": "DG1.6", "title": "Competitive Price Scraping Setup", "desc": "Build a light price-monitoring script to track competitor rental adjustments during peak summer and winter seasons.", "effort": "2 days", "dep": "None", "owner": "Ned", "ticket": "GRO-1219"},
        {"id": "DG1.7", "title": "Establish Customer Feedback & Survey Loops", "desc": "Set up a feedback loop aggregating post-trip reviews and customer support logs to feed directly into content updates.", "effort": "1 day", "dep": "CF1.8", "owner": "Kai", "ticket": "GRO-1220"},
        {"id": "Q4.1", "title": "On-Page SEO Tuning (Striking Distance Keywords)", "desc": "Tune content, schema, and linking on pages ranking in positions #4-10 (e.g. 'kayak tour oahu') to push them into the top 3.", "effort": "2 days", "dep": "None", "owner": "Kai", "ticket": "GRO-1194"},
        {"id": "Q1.6", "title": "Thin Content Indexation Cleanup (Paginated Archives)", "desc": "Deploy `noindex` tags across paginated blog and activity archive pages to prevent search engine thin-content penalties.", "effort": "1 day", "dep": "None", "owner": "Kai", "ticket": "GRO-1188"},
    ]

    phases = [
        ("Phase 1: Weeks 1-2 — Immediate Technical & Conversion Fixes (P0)", phase_1_tasks),
        ("Phase 2: Weeks 3-4 — Immediate Content & UX Optimizations (P0/P1)", phase_2_tasks),
        ("Phase 3: Weeks 5-6 — Technical SEO & Safety Enhancements (P1)", phase_3_tasks),
        ("Phase 4: Weeks 7-8 — Secondary Content & Schema (P1/P2)", phase_4_tasks),
        ("Phase 5: Weeks 9-10 — Authority & How-To Guides (P1/P2)", phase_5_tasks),
        ("Phase 6: Weeks 11-12 — CRO, PR & Analytics Automation (P2)", phase_6_tasks),
    ]

    for title, tasks in phases:
        roadmap_doc += f"### {title}\n\n"
        roadmap_doc += "| ID | Task | Description | Effort | Depends On | Owner | Target Ticket |\n"
        roadmap_doc += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for t in tasks:
            roadmap_doc += f"| **{t['id']}** | {t['title']} | {t['desc']} | {t['effort']} | {t['dep']} | {t['owner']} | `{t['ticket']}` |\n"
        roadmap_doc += "\n"

    roadmap_doc += """---

## 3. Immediate Next Actions (This Week)
1. **[Michael decision]** Review the **Strategic Decisions Document** (`decision-document-2026-06-12.md`), specifically Pricing Strategy and duration restructuring.
2. **[Ned execute]** Complete Astro DNS Cutover (`CF1.1`) to resolve 404 leakage immediately.
3. **[Kai execute]** Begin P0 schema injection on the top 20 English pages (`Q1.1`).
4. **[Fred audit]** Verify tracking setups once GA4 FareHarbor integration goes live.

"""

    with open("/home/ubuntu/work/active-oahu-static/site/_seo/reports/06-questions-audit/decision-document-2026-06-12.md", "w", encoding="utf-8") as f:
        f.write(decision_doc)
    print("Created decision-document-2026-06-12.md")
        
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/aot-90-day-roadmap-2026-06-12.md", "w", encoding="utf-8") as f:
        f.write(roadmap_doc)
    print("Created aot-90-day-roadmap-2026-06-12.md")

if __name__ == "__main__":
    main()

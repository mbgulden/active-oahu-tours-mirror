# Strategic Questions Audit: Data Gaps (Analytics & Tracking)

**Date:** 2026-06-11  
**Author:** Antigravity (agent:agy (redispatched via agent:fred))  
**Initiative:** 06-questions-audit  

This document surfaces the key strategic questions Michael should ask about the data and analytics we *do not* currently have, covering conversion tracking, user behavior, competitive intelligence, and customer feedback loop gaps.

---

## 1. Conversion Tracking Gaps
*Understanding how traffic translates into bookings.*

*   **Q5.1: FareHarbor GA4 E-Commerce Integration**
    *   *Context:* AOT uses FareHarbor for booking activities. FareHarbor checkouts load in an iframe or redirect to their domain, which can disrupt Google Analytics tracking if not configured properly.
    *   *Strategic Question:* "Are we accurately tracking FareHarbor booking transactions, revenue, and product IDs inside Google Analytics (GA4), or are we flying blind on which blog posts and guide pages drive the most bookings?"
    *   *Future Work:* Verify cross-domain tracking between `activeoahutours.com` and `fareharbor.com` and configure GA4 purchase events.

*   **Q5.2: Micro-Conversion Tracking**
    *   *Context:* Micro-conversions include clicking the phone number, copy-pasting the address (134B Hamakua Dr), clicking "Get Directions," or downloading safety checklists.
    *   *Strategic Question:* "How many mobile users are visiting our site to get directions or call the shop rather than booking online, and are we tracking these micro-conversions as indicators of business value?"
    *   *Future Work:* Implement Google Tag Manager (GTM) event triggers for phone clicks, email clicks, and directions clicks.

---

## 2. User Behavior Gaps
*Monitoring how visitors interact with our content.*

*   **Q5.3: Heatmaps & Scroll Depth Analysis**
    *   *Context:* Some guide pages (e.g. the Chinaman's Hat ultimate guide) are very long. We do not know if users are reading our safety guidelines and legends or bouncing because the page looks too long.
    *   *Strategic Question:* "Are users scrolling far enough down our tour pages to see the safety and logistics sections, or do we need to move these elements higher to reduce bounces?"
    *   *Future Work:* Set up Microsoft Clarity or Hotjar to track scroll depth, clicks, and session recordings on high-traffic landing pages.

*   **Q5.4: Search Console Click-Through Rate Gaps**
    *   *Context:* Search Console data shows high-impression keywords with CTR below 2%. We don't have a clear analysis of why these queries fail to convert searchers.
    *   *Strategic Question:* "For search queries where we have >1,000 impressions but <2% CTR, is the problem poor keyword matching, uncompelling SERP titles, or the lack of rich snippets compared to competitors?"
    *   *Future Work:* Audit queries with high impressions and low CTRs to match search intent with updated titles and schema markup.

---

## 3. Competitive Intelligence Gaps
*Tracking competitor moves and market pricing.*

*   **Q5.5: Ubersuggest Rate Limit Gaps**
    *   *Context:* During Ned's Ubersuggest sweep, several key reports were blocked by daily limits (such as `domain_overview`, `domain_keywords`, and `keyword_overview`), preventing us from getting full competitor traffic data.
    *   *Strategic Question:* "What competitor keywords and backlink profiles did we miss during the Ubersuggest API rate-limiting, and how can we scheduled-run another sweep to complete the competitive picture?"
    *   *Future Work:* Run a fresh, unrestricted Ubersuggest API sweep for competitor domains and keywords.

*   **Q5.6: Competitor Pricing and Capacity Adjustments**
    *   *Context:* KBA adjusts pricing and capacity based on seasons. We lack automated tracking of their pricing or booking calendars.
    *   *Strategic Question:* "Are competitors dynamically adjusting their rental pricing during peak summer months, and how does our pricing compare during the winter off-season?"
    *   *Future Work:* Conduct quarterly competitive pricing audits of KBA and other operators on Oahu.

---

## 4. Customer Feedback & Satisfaction Gaps
*Leveraging customer reviews and complaints to optimize the site.*

*   **Q5.7: Storefront Logistics Post-Trip Survey**
    *   *Context:* AOT transitioned to storefront pickup. We do not have systematic data on how hard customers found it to secure kayaks to their vehicles or find the storefront.
    *   *Strategic Question:* "What is the most common operational complaint in our post-trip customer feedback (e.g., vehicle strapping difficulties or location confusion), and how do we address these issues directly in our pre-trip website content?"
    *   *Future Work:* Implement a short post-trip email survey and use the responses to improve the website's FAQ and logistics guides.

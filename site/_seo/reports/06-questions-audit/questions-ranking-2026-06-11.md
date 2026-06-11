# Strategic Questions Audit: Ranking Gaps (SEO)

**Date:** 2026-06-11  
**Author:** Antigravity (agent:agy)  
**Initiative:** 06-questions-audit  

This document surfaces the key strategic questions Michael should ask to improve the organic Google rankings, CTR, and search visibility of Active Oahu Tours. It is divided into technical, content, authority, and competitive gaps.

---

## 1. Technical SEO Gaps
*Improving crawlability, indexation, and search engine presentation.*

*   **Q1.1: Schema Markup Deficit**
    *   *Context:* 149 out of 249 pages (60%) lack schema markup. Most critically, 14 out of 22 activity pages (63%) and 15 out of 31 rentals pages (48%) lack `Product`, `TouristTrip`, or `LocalBusiness` JSON-LD schema, preventing rich snippets.
    *   *Strategic Question:* "How much organic CTR and booking revenue are we losing to Kailua Beach Adventures on local SERPs because 60% of our transactional pages lack rich snippet schema markup?"
    *   *Future Work:* Inject batch JSON-LD schema (e.g., `TouristTrip`, `Product`, `FAQPage`) to key money pages.

*   **Q1.2: Japanese Mirror Schema Gap**
    *   *Context:* Active Oahu Tours has 83 Japanese (`ja/`) mirror pages, but **0%** of them have schema markup. Japanese tourists represent high-value, high-intent traffic, and KBA currently has minimal Japanese SEO presence.
    *   *Strategic Question:* "Are we failing to capture the high-intent Japanese tourist market by leaving our 83 Japanese mirror pages with zero schema markup, making them invisible in rich search results?"
    *   *Future Work:* Translate and inject corresponding schema markup for all `ja/` mirror pages.

*   **Q1.3: Structural Orphan Pages**
    *   *Context:* 7 pages have 0 internal links pointing to them. Crucially, this includes high-value pages like the Chinaman's Hat self-guided guide (`/activities/chinamans-hat-kayak-complete-self-guided-tour-guide/`) and the Kailua Bay self-guided kayak tour (`/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/`).
    *   *Strategic Question:* "Why are we spending crawl budget on high-value tour guides and activity pages if they are completely orphaned with zero internal links, preventing search engines from distributing link equity to them?"
    *   *Future Work:* Audit site structure and inject internal links to the 7 orphaned pages from top-level category pages or the homepage.

*   **Q1.4: Broken Orphan Paths**
    *   *Context:* Two orphan pages contain a double dot-slash `/.html` extension in the codebase:
        *   `activities/kailua-bay-mokulua-island-self-guided-kayak-tour/.html`
        *   `activities/kailua-kayak-twin-islands-guided-tour/.html`
    *   *Strategic Question:* "Are the broken `/.html` extensions on our Mokulua self-guided and guided tour pages triggering crawl errors (404s) and destroying their ability to rank for high-volume Kailua search queries?"
    *   *Future Work:* Fix link paths and rewrite rules to resolve the `/.html` extension error.

*   **Q1.5: SERP Title and Meta Description Truncation**
    *   *Context:* 31 pages have titles >70 characters (longest is 92 characters on `living-aloha-respectful-travel`), and 25 pages have descriptions >160 characters (longest is 208 characters on `beach-gear-rentals`). This leads to truncation (the "..." ellipsis) in SERPs.
    *   *Strategic Question:* "Is our search click-through rate (CTR) on key terms being suppressed because 31 page titles and 25 meta descriptions are too long and get truncated by Google's display limits?"
    *   *Future Work:* Batch-run a script to trim titles and descriptions to recommended lengths (≤70 characters for titles, ≤160 characters for descriptions).

*   **Q1.6: Indexation of Thin Pagination Pages**
    *   *Context:* Pagination pages such as `activities/page/2/` and `page/3/` in both English and Japanese are thin and currently indexable.
    *   *Strategic Question:* "Should we add `noindex` tags to our paginated activity archives to prevent Google from flag-marking them as thin content and dilute our domain quality?"
    *   *Future Work:* Apply `noindex` or proper canonicals to paginated archive pages.

---

## 2. Content Gaps
*Identifying missing pages and opportunities to capture unranked keywords.*

*   **Q2.1: Snorkel Rental Revenue Leak**
    *   *Context:* AOT has **no rankings** in the top 20 for "snorkel rental oahu", while KBA ranks #6. This represents a direct product and keyword gap. AOT has snorkeling gear but no dedicated commercial landing page.
    *   *Strategic Question:* "Why does Active Oahu Tours completely lack a commercial landing page for snorkel rentals, allowing KBA to capture 100% of the Windward snorkel search traffic?"
    *   *Future Work:* Build a dedicated page `/rentals/snorkel-gear-rentals/` featuring `Product` schema.

*   **Q2.2: Kawela Bay Transactional Opportunity**
    *   *Context:* Kawela Bay on the North Shore has a blog post but no transactional product page on `activeoahutours.com`. Abigail's drafts (Docs 6 and 7) provide ready-made product copy, safety guidelines, and local features. No competitor currently ranks for "kawela bay kayak".
    *   *Strategic Question:* "Should we launch a dedicated Kawela Bay Self-Guided Tour booking page to secure first-mover advantage on a keyword that competitors are completely ignoring?"
    *   *Future Work:* Create `/activities/kawela-bay-self-guided-kayak-tour/` with booking widgets and local/historical context.

*   **Q2.3: Rebuilding the Underperforming Paddleboard Page**
    *   *Context:* For the keyword "paddleboard rental oahu", AOT ranks at #15, whereas KBA ranks at #6. The paddleboard page currently lacks rich content, schema, and internal link volume.
    *   *Strategic Question:* "What specific content and internal linking structure does our standup paddleboard page lack that keeps us sitting at #15 while KBA ranks in the top 10?"
    *   *Future Work:* Rewrite the paddleboard page using local navigation, weather limits, and schema.

---

## 3. Authority Gaps
*Strengthening site authority and topical expertise (E-E-A-T).*

*   **Q3.1: Topical Authority Defense**
    *   *Context:* AOT ranks #1 for "chinamans hat kayak" and "kaneohe sandbar kayak" but trails in Domain Authority (26 vs. KBA's 32). Competitors are actively creating content to target these spots.
    *   *Strategic Question:* "How do we integrate the rich historical stories, safety tips, and local navigation rules from Abigail's drafts to build a 'content moat' around our #1 rankings for Chinaman's Hat and Kaneohe Sandbar?"
    *   *Future Work:* Inject localized information (legends, tide guides, safety warnings) into existing high-ranking pages.

*   **Q3.2: Domain Authority Backlink Gap**
    *   *Context:* KBA has 2,225 backlinks from 689 referring domains, while AOT has 1,374 backlinks from 451 referring domains (a gap of +238 referring domains).
    *   *Strategic Question:* "Which high-authority tourism, accommodation, and community domains are linking to KBA but ignoring AOT, and how do we close this 238 referring domain gap?"
    *   *Future Work:* Perform a link intersect analysis to find tourism directories, partner accommodations, and Oahu travel blogs linking to competitors.

---

## 4. Competitive Gaps
*Closing the gap on close-run search terms.*

*   **Q4.1: Striking Distance Keywords (Positions 4-10)**
    *   *Context:* AOT ranks at #6 for "kayak tour oahu" (KBA is #4), #7 for "mokulua islands kayak" (KBA is #3), and #6 for "lanikai beach kayak" (KBA is #8).
    *   *Strategic Question:* "What optimizations (schema, keyword alignment, title adjustments) are required to push our striking-distance keywords (e.g., 'kayak tour oahu') into the top 3 positions to capture high-intent click volume?"
    *   *Future Work:* Perform on-page optimization, add FAQ schema, and trim meta descriptions for pages currently ranking in positions 4-10.

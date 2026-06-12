# Executive Summary: Strategic Questions Audit (Meta-Audit)

**Date:** 2026-06-11  
**Author:** Antigravity (agent:agy (redispatched via agent:fred))  
**Initiative:** 06-questions-audit  

---

## 1. Context & Purpose

Active Oahu Tours (AOT) operates in a highly competitive local tourism market on Oahu. While the business has solid fundamentals and holds #1 rankings for high-intent niche queries (e.g., "chinamans hat kayak"), it faces significant pressure from established competitors like Kailua Beach Adventures (KBA), which boasts a higher Domain Authority (32 vs. 26) and substantially more organic traffic.

This **Strategic Questions Audit** is a meta-audit designed to surface the deep, structural questions Michael Gulden should ask about AOT's digital footprint. The purpose is not to answer the questions today, but to identify the critical levers—in rankings, revenue/cashflow, guest experience, and brand authenticity—that future tickets must resolve.

---

## 2. High-Level Findings

The meta-audit analyzed data from the technical baseline, Ubersuggest sweeps, content-reuse guides, and interview frameworks. The analysis highlighted three core strategic challenges:

1.  **The Rich Snippet Deficit (Ranking Gaps):** 60% of AOT's English pages and 100% of its 83 Japanese mirror pages lack schema markup. Because local search is increasingly dominated by rich snippets and local map packs, this technical omission directly translates into lost clicks.
2.  **Storefront Logistics Friction (Cashflow Gaps):** AOT's transition from beach delivery to storefront pickup (Hamakua Dr) requires guests to strap heavy kayaks to their personal rental cars. While operationally necessary, this creates a major customer conversion barrier that the website does not yet address.
3.  **Topical Moat Vulnerability (Authority Gaps):** AOT holds top organic spots for Windward tours, but KBA is expanding aggressively. AOT lacks local, narrative storytelling and cultural stewardship indicators (such as Hawaiian lore, taro farming, and wildlife education) that could form a defensible "content moat."

---

## 3. Core Question Breakdown

The meta-audit produced **37 specific, actionable questions** organized into five outcome-driven categories:

*   **Ranking (12 questions):** Focusing on schema markup gaps (EN & JA), structure fixes for 7 orphaned pages, broken `/.html` extensions, title/description truncation, and high-value product page gaps (like standup paddleboards and snorkel rentals).
*   **Cashflow (8 questions):** Addressing critical server 404 leaks, storefront pickup copy friction, mobile check-out latency, add-on upsell flows, and email marketing automation.
*   **Guest Value (7 questions):** Targeting information completeness above the fold, live tide charts for Kaneohe Sandbar, safety trust indicators, launch site restroom/shower maps, and post-booking logistical prep.
*   **Authority & Authenticity (8 questions):** Leveraging Michael's story and daily presence, local post-paddle eats guides, Hawaiian cultural storytelling (the legend of Mokoliʻi, Kahana Valley stewardship, and the concept of *wai*), and bird sanctuary conservation guidelines.
*   **Data Gaps (7 questions):** Targeting FareHarbor GA4 integration, micro-conversion button tracking, mobile heatmaps, and systematic customer feedback loops.

---

## 4. Next Actions & Priority Road Map

The 37 questions have been prioritized into a road map matching specific future tickets:

1.  **P0 - Immediate Fixes (Revenue & Tech Gaps):**
    *   Resolve server-side 404 errors by completing the Astro staging-to-live Cutover (`CF1.1` $\rightarrow$ `GRO-1195`).
    *   Configure dynamic FareHarbor GA4 conversion tracking to measure marketing performance (`DG1.1` $\rightarrow$ `GRO-1214`).
    *   Deploy schema markup across all 149 English pages and 83 Japanese mirror pages to secure rich search results (`Q1.1/Q1.2` $\rightarrow$ `GRO-1184/GRO-1185`).
    *   Fix the 7 orphaned pages and broken `/.html` extensions to restore internal link equity (`Q1.3/Q1.4` $\rightarrow$ `GRO-1186`).
2.  **P1 - Build Soon (UX & Content Moat):**
    *   Address car-strapping friction on rental landing pages and pre-trip email confirmations (`CF1.2/GV1.7` $\rightarrow$ `GRO-1196/GRO-1207`).
    *   Launch the Kawela Bay Self-Guided product page and build a dedicated Snorkel Rentals page (`Q2.1/Q2.2` $\rightarrow$ `GRO-1189/GRO-1190`).
    *   Inject Michael's brand voice, local eats recommendations, and Hawaiian cultural history into existing pages (`AU1.1-AU1.7` $\rightarrow$ `GRO-1208/GRO-1210`).
3.  **P2 - Long-Term Polish (Cleanup & Automation):**
    *   Implement post-trip feedback loops and repeat guest email marketing (`CF1.8/DG1.7` $\rightarrow$ `GRO-1202/GRO-1220`).
    *   Perform thin page indexation cleanups (`Q1.6` $\rightarrow$ `GRO-1188`).

# Executive Summary: CRO + SEO Integration Plan

**Date:** 2026-06-11  
**Project:** Active Oahu Tours (GRO-1233)  
**Objective:** Leverage existing organic search traffic (~4K monthly sessions) to drive more bookings through conversion rate optimization (CRO) and schema enhancements.

---

## 1. Core Findings & Data Diagnostics

1. **The Traffic-to-Booking Gap**:
   * The site gets strong traffic (~3,778 sessions/30 days), driven primarily by **google / organic** (2,086 sessions, 55.2%).
   * However, the overall session-to-booking conversion rate is **0.93%** (35 purchases/30 days).
   * Once users reach the checkout cart, conversions are healthy (**38.0% cart completion rate**), indicating that the primary leak is between the landing page and the booking widget.
2. **The Sharks Cove Snoorkeling Leak**:
   * The self-guided Sharks Cove Snorkeling page is the 2nd most visited page (405 sessions/30 days), but generated **0 purchases** in 90 days.
   * **The Cause**: The page requires customers to pick up rental gear at our storefront in Kailua (an hour's drive away) to use it at Sharks Cove (North Shore). Users realize this geographical mismatch and bounce.
3. **The Schema Gap**:
   * GSC search appearance data shows **zero review snippets** and **zero FAQ dropdowns** in search results. 
   * AOT had only **494 impressions for product snippets** in 6 months. Competitors like Kailua Beach Adventures (KBA) capture the majority of clicks by displaying 5-star ratings and pricing in search results.
4. **Mobile UX Constraints**:
   * Mobile drives **52.6% of traffic** (1,986 sessions). 
   * The hardcoded header logo size causes the phone number and CTAs to stack vertically, consuming **120px of vertical space** and pushing core product headlines below the fold.

---

## 2. Priority Recommendation Matrix

We have organized recommendations into high-impact, immediate actions (P0) and secondary improvements (P1):

| Priority | Initiative | Targeted Page/Section | Action Item | Expected Impact |
|---|---|---|---|---|
| **P0** | **Deep-Link CTAs** | Homepage & Category pages | Replace generic catalog booking widgets with direct links to specific item codes. | **+15% Bookings** (Reduces catalog drop-offs). |
| **P0** | **Address Sharks Cove Mismatch** | `/activities/sharks-cove...` | Revise copy to promote North Shore delivery partners or shift to a guided snorkel tour structure. | **Eliminates 100% leak** on our 2nd highest traffic page. |
| **P0** | **Batch Schema Injection** | All 149 EN & 83 JA pages | Inject JSON-LD schema (`Product`, `TouristTrip`, `FAQPage`) to enable rich snippets in search results. | **+20% to +50% CTR lift** on ranking pages. |
| **P1** | **Optimize Mobile Header** | Site Header | Adjust CSS to render the logo, phone, and CTA on a single line on mobile viewports. | **+10% mobile conversions** (Restores above-the-fold real estate). |
| **P1** | **Form Field Simplification** | FareHarbor checkout | Postpone participant Height/Weight/Shoe Size fields until *after* checkout is completed. | **Decreases checkout abandonment**. |

---

## 3. Visual Reference

An optimized desktop landing page layout featuring a clear pricing structure, adjacent CTAs, and integrated trust badges is available in the workspace:
* [optimized_cta_mockup.png](file:///home/ubuntu/work/active-oahu-static/site/_seo/images/optimized_cta_mockup.png)

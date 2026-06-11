# Strategic Questions Audit: Cashflow Gaps (Revenue & Conversions)

**Date:** 2026-06-11  
**Author:** Antigravity (agent:agy)  
**Initiative:** 06-questions-audit  

This document surfaces the key strategic questions Michael should ask to improve the conversion rate, average order value (AOV), and customer lifetime value (LTV) for Active Oahu Tours. It focuses on funnel leaks, pricing/positioning, upselling, and customer retention.

---

## 1. Funnel Leaks & Conversion Gaps
*Identifying where potential bookers drop out of the purchasing process.*

*   **Q2.1: The Flywheel 404 Revenue Drain**
    *   *Context:* A recent technical audit revealed that 4 high-value pages were returning 404 errors on the live Flywheel site despite being 200 OK on the staging/mirror site. This includes the high-traffic `/sharks-cove-snorkeling/` page (which received 555 clicks over 90 days) and `/kayak-kailua/`.
    *   *Strategic Question:* "How much booking revenue did we lose over the last 90 days due to high-intent pages like `/sharks-cove-snorkeling/` throwing 404 errors on our live server, and how quickly can we cut over to our stable Astro mirror to stop this leak?"
    *   *Future Work:* Complete the Cutover Runbook to point DNS to the fully functional Astro mirror.

*   **Q2.2: Storefront Pickup Friction vs. Competitor Beach Proximity**
    *   *Context:* KBA is located within walking distance of Kailua Beach, allowing customers to easily walk their rentals to the water. Active Oahu Tours has transitioned from a direct-beach-delivery model to a storefront pickup model (134B Hamakua Dr). Customers must check in, load the kayaks onto their own vehicle using provided foam pads and straps, and drive 35-45 minutes to the launch site.
    *   *Strategic Question:* "How does the requirement for guests to self-strap kayaks to their personal 4-door rental cars and drive 40 minutes to launch locations affect our cart abandonment rate, and how can we address this friction in our checkout copy?"
    *   *Future Work:* A/B test booking flow copy that frames vehicle strapping as an "easy, 5-minute setup" with video tutorials, or highlight the included foam pads and straps.

*   **Q2.3: Mobile FareHarbor Checkout Speed**
    *   *Context:* The majority of activity bookings on Oahu are made via mobile devices, often by travelers already on the island. The FareHarbor widget loads external scripts that can slow down mobile page load speeds.
    *   *Strategic Question:* "Does the FareHarbor booking widget load slowly enough on mobile connections at Kailua Beach that frustrated users bounce to KBA's storefront?"
    *   *Future Work:* Optimize site scripts, implement lazy-loading for non-critical assets, and measure the performance of the FareHarbor embed on slow mobile networks.

---

## 2. Pricing & Positioning Gaps
*Maximizing margins and perceived value.*

*   **Q2.4: Pricing for the Car Transport Model**
    *   *Context:* AOT's 4-hour rentals start at $49 for a single kayak and $69 for a tandem kayak. Because the customer handles transportation, AOT's pricing should reflect either a cost-savings advantage or an added-value advantage (e.g., providing longer durations, free dry bags, or beach carts).
    *   *Strategic Question:* "Are we pricing our rentals low enough to offset the friction of car-transportation, or are we failing to emphasize the value of our included gear (free dry bags, straps, foam pads, and carts) to justify our rates?"
    *   *Future Work:* Add a clear comparison grid showing what AOT includes (dry bags, vehicle mounting kit) vs. what competitors charge extra for.

*   **Q2.5: The 4-Hour vs. 3-Hour Duration Pricing Discrepancy**
    *   *Context:* Older Abigail drafts and FareHarbor notes refer to a "3-hour experience" for Chinaman's Hat, while the current live page lists it as a "4-hour rental."
    *   *Strategic Question:* "Does listing a 4-hour rental window (which includes shop pickup, transit, and launch) create customer disputes about 'actual water time' vs. 'transit time,' and should we adjust our booking options to offer full-day rentals?"
    *   *Future Work:* Restructure the rental options to emphasize that the 4-hour block is generous enough for a relaxed trip, or offer a "Full Day (8-hour) Explorer Package" for a small price increase.

---

## 3. Upsell Gaps
*Increasing average order value at the point of purchase.*

*   **Q2.6: Snorkel Gear Bundle Attach Rate**
    *   *Context:* Snorkeling gear is currently offered as a $15 add-on to kayak rentals. AOT has no dedicated snorkel landing page, and snorkeling is often treated as an afterthought in the booking flow.
    *   *Strategic Question:* "Are we missing out on high-margin revenue by failing to proactively upsell snorkel gear bundles during the booking checkout flow for Kailua and Chinaman's Hat rentals?"
    *   *Future Work:* Redesign the booking flow to show a "Kayak + Snorkel Bundle" option with a clear checkbox in FareHarbor.

*   **Q2.7: Multi-Activity and Multi-Day Package Adoption**
    *   *Context:* AOT offers multi-day rentals (e.g., 2 days at $99 for a single) and e-bike packages (like the Lanikai E-Bike & Snorkel adventure).
    *   *Strategic Question:* "Are we failing to promote our multi-day packages and hybrid e-bike/kayak adventures on our primary tour pages, leading tourists to book a single 4-hour rental when they would have preferred a multi-day package?"
    *   *Future Work:* Add a "Upgrade to Multi-Day" callout block on all high-traffic rental pages.

---

## 4. Customer Retention & LTV Gaps
*Building a list of returning customers and generating referrals.*

*   **Q2.8: Post-Booking Email Capture & Repeat Bookings**
    *   *Context:* Oahu visitors often return to the island every 2-3 years, or recommend activities to friends. 
    *   *Strategic Question:* "What post-trip marketing automation do we have in place to turn one-time kayakers into brand advocates who refer friends and book again on their next trip to Hawaii?"
    *   *Future Work:* Implement a post-booking email sequence offering a "15% return guest discount" and a request for a TripAdvisor review.

# Pillar & Cluster Recommendations — Active Oahu Tours

**Date:** 2026-06-11  
**Initiative:** 01 — Topical Authority & Content Clusters (GRO-1178)

This report details AOT's Pillar-Spoke (Hub-and-Spoke) promotion strategy, internal linking architecture, and URL consolidation recommendations.

---

## 1. Designated Pillar Pages

We designate the following pages as the high-equity "Hubs" for their respective topic clusters:

1.  **Kayak Rentals Hub (Windward Oahu):** `/kayak-rentals/index.html`
    - *Strategic Purpose:* Capture broad search intent for "oahu kayak rentals" and distribute link equity to specific product pages.
2.  **Chinaman's Hat Tour Hub:** `/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
    - *Strategic Purpose:* Defend AOT's #1 position for "chinamans hat kayak" against KBA.
3.  **Kaneohe Sandbar Hub:** `/activities/kaneohe-sandbar-kayak-rentals/index.html`
    - *Strategic Purpose:* Maintain #1 spot for "kaneohe sandbar kayak rental".
4.  **Kahana River Tour Hub:** `/activities/kahana-rainforest-river-oahu-kayak-tour/index.html`
    - *Strategic Purpose:* Establish authority in family-friendly flat-water kayaking.
5.  **Beach Gear & Snorkeling Hub:** `/beach-gear-rentals/index.html`
    - *Strategic Purpose:* Promote high-margin rental packages (chairs, umbrellas, coolers) and support the new snorkel rentals page.
6.  **E-Bike rentals Hub:** `/electric-bike-rentals/index.html`
    - *Strategic Purpose:* Drive rentals and multi-activity combination bookings.

---

## 2. Internal Linking Rules & Architecture

To pass link equity efficiently and resolve the orphan pages issue, implement these linking rules:

### Rule 1: The Spoke-to-Hub Flow
Every supporting page (spoke) must link back to its designated category Pillar page using exact or partial keyword anchor texts.
- Example: `/guides/lanikai-beach/` must link back to `/kayak-rentals/` with the text "[Kailua kayak rentals](file:///kayak-rentals/)".

### Rule 2: The Hub-to-Product Flow
Pillar hub pages must display featured links to key money pages (transactional spokes).
- Example: `/beach-gear-rentals/` must have a prominent CTA pointing to `/rentals/oahu-snorkel-mask-and-fin-rentals/` and the new `/rentals/snorkel-gear-rentals/` page.

### Rule 3: The Cross-Cluster Context Flow
Link relevant guides across clusters to increase session depth and crawler accessibility.
- Example: Link from `/activities/chinamans-hat-self-guided-oahu-kayak-tour/` to the safety safety guide `/guides/chinamans-hat-tide-guide/`.

---

## 3. URL Structure & Cannibalization Cleanup

### Duplicate Landing Pages (Kailua Kayaking)
The audit identified multiple landing pages competing for "kailua kayak rental":
- `/kailua-kayak/`
- `/kayak-kailua/`
- `/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` (Primary Money Page)

**Recommendation:**
1.  Add canonical tags on `/kailua-kayak/index.html` and `/kayak-kailua/index.html` pointing to `https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/`.
2.  After 30 days, set up permanent 301 redirects in `_redirects`:
    ```
    /kailua-kayak/*  /rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/ 301
    /kayak-kailua/*  /rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/ 301
    ```

### Broken Orphan Paths
Two orphaned paths contain double extensions (`/.html`) representing 404 targets:
- `activities/kailua-bay-mokulua-island-self-guided-kayak-tour/.html`
- `activities/kailua-kayak-twin-islands-guided-tour/.html`

**Recommendation:** Remove these directories from the server or 301 redirect them to the correct, extension-free URLs.

---

*Prepared by Antigravity (agent:antigravity) — GRO-1178 Strategy*

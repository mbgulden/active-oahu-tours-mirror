# Schema-Driven CTR Opportunities

**Date:** 2026-06-12  
**Source Data:** Google Search Console (`sc-domain:activeoahutours.com`, last 6 months)  

---

## 1. GSC Search Appearances Analysis

A query for search appearances over the last 6 months shows that Active Oahu Tours is completely failing to capture rich results in Google:

* **`PRODUCT_SNIPPETS`**: Only **494 impressions** (generating a mere **28 clicks**, 5.6% CTR) in 6 months.
* **`REVIEW_SNIPPETS`**: **0 impressions** (no star ratings are showing in organic SERPs).
* **`FAQ` Rich Results**: **0 impressions** (no dropdown questions are showing).

This confirms a massive schema gap. While organic positions are strong (e.g., AOT holds #1-3 positions for high-intent terms like "chinamans hat kayak rental" and "kaneohe sandbar kayak"), our listings appear as plain text, while competitors like Kailua Beach Adventures (KBA) capture larger SERP real estate using review stars, pricing, and availability.

---

## 2. Key Target Keywords & Competitor Snippets

| Keyword | AOT Position | GSC Impressions (6mo) | Competitor Rich Results | AOT Schema Status | Estimated CTR Lift |
|---|---|---|---|---|---|
| **kaneohe sandbar kayak rental** | 3.3 | 601 | KBA shows 5-star ratings, price ($79+), stock | 🔴 Missing | **+25%** (CTR from 14.6% → 18.2%) |
| **sharks cove snorkeling** | 6.6 | 3,374 | TripAdvisor, Viator show star ratings + review count | 🔴 Missing | **+50%** (CTR from 4.0% → 6.0%) |
| **kayaking oahu** | 9.4 | 2,131 | KBA and Hawaii Activities show price, rating stars | 🔴 Missing | **+80%** (CTR from 2.1% → 3.8%) |
| **kailua kayak rental** | 6.7 | 825 | KBA shows 4.8 stars (220+ reviews), price ($49+) | 🔴 Missing | **+40%** (CTR from 3.5% → 4.9%) |
| **electric beach** | 5.6 | 6,544 | Guide sites show FAQ dropdowns, review ratings | 🔴 Missing | **+100%** (CTR from 0.5% → 1.0%) |

---

## 3. Schema Architecture by Page Type

To resolve this gap, we recommend batch-injecting JSON-LD schema across the 149 English pages and 83 Japanese mirror pages using the following schemas:

### 1. Rental Pages (`/rentals/` or `/oahu-equipment-rentals/`)
* **Schema Type**: `Product` + `Offer` + `AggregateRating`
* **Properties to Inject**:
  * `name`: Product title (e.g. "Chinaman's Hat Kayak Rental")
  * `offers`: `price` ($49.00), `priceCurrency` ("USD"), `availability` ("https://schema.org/InStock")
  * `aggregateRating`: `ratingValue` (4.9), `reviewCount` (1240)
* **Expected Result**: Prices and star ratings appear directly in Google Shopping and organic search.

### 2. Tour & Activity Pages (`/activities/`)
* **Schema Type**: `TouristTrip` + `Offer` + `AggregateRating`
* **Properties to Inject**:
  * `name`: Tour name (e.g. "Kaneohe Sandbar Kayak Tour")
  * `touristType`: "Outdoor / Adventure"
  * `offers`: `price` ($79.00), `priceCurrency` ("USD")
  * `aggregateRating`: `ratingValue` (4.8), `reviewCount` (180)
* **Expected Result**: Tour duration, pricing, and reviews display in search results.

### 3. Informational Guides (`/guides/`)
* **Schema Type**: `Article` + `FAQPage`
* **Properties to Inject**:
  * `mainEntity`: List of `Question` and `Answer` items (derived from FAQs on pages like `lanikai-beach/index.html` or `chinamans-hat-tide-guide/index.html`).
* **Expected Result**: FAQ rich snippets (expandable question boxes in search results) to push competitors down the page.

---

## 4. Japanese Mirror Opportunity

The **83 Japanese mirror pages** have **0% schema coverage**. The Japanese tourism market has high booking intent, and local competitors (such as KBA) have minimal Japanese-language optimization. Injecting Japanese-translated `Product` and `TouristTrip` schema will give AOT an immediate first-mover advantage in Japanese search engines (Google Japan and Yahoo! Japan).

# AOT Link Audit — 2026-06-13

## Summary
- Old staging URLs: 153
- New mirror pages: 260
- Matched (same path on both): 99
- Missing (old→no new): 54
- New-only (new→no old): 161

## Priority 1 — High-Traffic Missing Pages
Only include pages with measurable GSC clicks.

1. **`/reviews/3-person-kayak-rental-alyssa`**
   - **GSC Clicks:** 3
   - **GA Sessions:** 6.0
   - **GA Conversions:** 0.0
   - **Description:** Staging review page for a 3-person kayak rental.

2. **`/reviews/3-person-kayak-rental-remy`**
   - **GSC Clicks:** 3
   - **GA Sessions:** 4.0
   - **GA Conversions:** 0.0
   - **Description:** Staging review page for a 3-person kayak rental.

3. **`/reviews/rental-deliveries-3`**
   - **GSC Clicks:** 1
   - **GA Sessions:** 0.0
   - **GA Conversions:** 0.0
   - **Description:** Staging review page discussing beach rental deliveries.

## Priority 2 — Medium-Traffic Missing Pages
Pages that have zero GSC clicks but generated measurable user engagement sessions or impressions.

1. **`/category/kayaking-experiences`**
   - **GA Sessions:** 12.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

2. **`/reviews/kayak-rental-review-google-jessica`**
   - **GA Sessions:** 10.0
   - **GSC Impressions:** 26
   - **GA Conversions:** 0.0

3. **`/reviews/kayak-rental-mokolii-kasie-c`**
   - **GA Sessions:** 10.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

4. **`/reviews/kayak-rental-review-google-c-bland`**
   - **GA Sessions:** 10.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

5. **`/reviews/kayak-rental-review-reef-google-jessica`**
   - **GA Sessions:** 10.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

6. **`/reviews/kayak-rental-trip-advisor-mokolii-nancy-b`**
   - **GA Sessions:** 9.0
   - **GSC Impressions:** 7
   - **GA Conversions:** 0.0

7. **`/reviews/kayak-rental-tripadvisor-sandbar-n9295pbmayas`**
   - **GA Sessions:** 8.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

8. **`/reviews/kayak-rental-mokolii-alyssa-m`**
   - **GA Sessions:** 7.0
   - **GSC Impressions:** 0
   - **GA Conversions:** 0.0

## Priority 3 — Zero-Traffic Missing Pages
Mostly /reviews/* and /category/* — note these.

There are **43 missing pages** that recorded zero GSC clicks and zero GA sessions. The vast majority of these are individual testimonial/review pages (40 paths) and administrative/system paths:
- **Testimonial/Review Pages (40 paths):** E.g. `/reviews/e-bike-snorkel-review-2` (47 impressions), `/reviews/chinamans-hat-review-3` (35 impressions), `/reviews/single-kayak-rental-robin` (31 impressions), `/reviews/popoia-island-review` (20 impressions). These can safely be ignored for individual redirects or grouped under product-level redirects.
- **Administrative & Utility Pages (3 paths):**
  - `/locations.kml` (0 traffic)
  - `/job-edit` (0 traffic)
  - `/job-submit` (0 traffic)

## New Pages Without Old Equivalent
Key pages worth monitoring.

The new mirror introduces **161 new-only paths**. These fall into two primary groups:
1. **Japanese Translation Pages (`/ja/...` - 90 paths):** A substantial amount of search volume and traffic is already migrating to these Japanese equivalents. The top pages performing in search should be closely monitored:
   - **`/ja/activities/sharks-cove-self-guided-snorkel`** — 49 Clicks | 87.0 Sessions | 1,328 Impressions
   - **`/ja/rentals/oahu-beach-umbrella-rentals`** — 38 Clicks | 54.0 Sessions | 557 Impressions
   - **`/ja/rentals/oahu-snorkel-mask-and-fin-rentals`** — 29 Clicks | 57.0 Sessions | 436 Impressions
   - **`/ja/rentals/oahu-boogie-board-rentals`** — 21 Clicks | 38.0 Sessions | 408 Impressions
   - **`/ja/rentals/oahu-life-vest-rentals`** — 17 Clicks | 27.0 Sessions | 258 Impressions
   - **`/ja/rentals/oahu-beginner-surf-board-rentals`** — 15 Clicks | 16.0 Sessions | 231 Impressions
   - **`/ja/oahu-equipment-rentals`** — 14 Clicks | 43.0 Sessions | 497 Impressions
   - **`/ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire`** — 14 Clicks | 29.0 Sessions | 215 Impressions

2. **New English Content & Structuring (71 paths):** Key structural pages introduced that are starting to show traffic:
   - **`/rentals`** — 0 Clicks | 35.0 Sessions | 0 Impressions
   - **`/guides`** — 0 Clicks | 10.0 Sessions | 122 Impressions
   - **`/activities/rainforest-oahu-kayak-tour`** — 0 Clicks | 9.0 Sessions | 8 Impressions
   - **`/about-active-oahu`** — 0 Clicks | 4.0 Sessions | 32 Impressions
   - **`/beach-gear-rentals`** — 0 Clicks | 4.0 Sessions | 0 Impressions
   - **`/electric-bike-rentals`** — 0 Clicks | 4.0 Sessions | 0 Impressions

## Keyword Gaps (Ubersuggest)
Keywords people search that we lack dedicated pages for.

Based on keyword suggestions extracted from Neil Patel's Ubersuggest MCP for "oahu tours", the website has significant content/commercial gaps for highly searched attractions and tour types on Oahu. 

| Seed / Gap Keyword | Search Volume | CPC (USD) | Paid Difficulty (PD) | Opportunity / Action Plan |
| :--- | :--- | :--- | :--- | :--- |
| **`dole plantation oahu`** | 165,000 | $1.85 | 63 | Create a dedicated blog guide or tour package including Dole Plantation transportation. |
| **`diamond head crater hike oahu`** | 90,500 | $0.90 | 37 | Create a self-guided hiking + shuttle combo page. |
| **`uss missouri oahu`** | 90,500 | $1.48 | 87 | Pearl Harbor tour guide/booking packages. |
| **`pearl harbor tickets oahu`** | 22,200 | $2.08 | 100 | High conversion intent. A detailed ticketing/access guide could capture valuable traffic. |
| **`luaus in hawaii oahu`** / **`best luau oahu`** | 12,100 / 9,900 | $3.77 / $2.92 | 100 / 90 | Partner with local luaus to resell bookings or publish a comparative guide review. |
| **`climbworks oahu`** / **`keana farms zipline oahu`** | 8,100 | $1.91 | 30 | Low Paid Difficulty. High opportunity for an adventure guide page or booking referral. |
| **`oahu arizona memorial tours`** | 8,100 | $2.71 | 100 | Pearl Harbor Arizona Memorial tour page. |
| **`pearl harbor tours oahu`** | 6,600 | $3.73 | 69 | Highly transactional tours landing page. |
| **`snorkel oahu`** / **`snorkeling in hawaii oahu`** | 6,600 | $2.77 | 100 | Target broader snorkeling terms beyond hyper-local spots like Sharks Cove. |
| **`jurassic park tour oahu hawaii`** | 6,600 | $1.10 | 66 | Kualoa Ranch tours and filming locations guide. |

## Redirect Map
Old URL → New URL for any high-traffic missing pages.

To preserve the ranking equity of high-traffic missing pages, implement the following 301 redirects to the closest relevant destination on the new site:

* **`/reviews/3-person-kayak-rental-alyssa`**  
  → `/rentals/oahu-tandem-kayak-rentals`  
  *(Redirect to the core tandem kayak rental category as 3-person specific review pages do not exist on the mirror)*

* **`/reviews/3-person-kayak-rental-remy`**  
  → `/rentals/oahu-tandem-kayak-rentals`  
  *(Redirect to the core tandem kayak rental category)*

* **`/reviews/rental-deliveries-3`**  
  → `/oahu-kayaking-and-beach-adventures/kayak-deliveries-on-oahu`  
  *(Redirect to the dedicated guide page explaining kayak and beach gear delivery logistics on Oahu)*

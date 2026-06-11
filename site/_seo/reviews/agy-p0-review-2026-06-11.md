# AGY Review — Phase 1: Review all P0 changes by Kai (GRO-1238)
**Review Date:** 2026-06-11
**Reviewer:** AGY (Design & SEO Specialist)
**Status:** Complete

---

## Overview
This report documents the Phase 1 review of the P0 changes implemented by Kai. The audit covers 4 main groups of changes: Orphan Page Links, the new Snorkel Gear Rentals page, Kailua Kayak duplicate page fixes, and Japanese Schema cleanups. We checked for content correctness, visual layout integration, HTML structural integrity, and proper SEO attributes (canonical, alternates, and Hawaiian diacritical marks).

---

## Detailed File-by-File Review

### 1. GRO-1224 — Orphan Page Links

#### File 1: `site/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html`
* **✅ What's done well:** Successfully added a highly contextual, helpful link to the Chinaman's Hat self-guided tour guide.
* **⚠️ What could be improved:** The added paragraph and original text use straight apostrophes/quotes (`Mokoli'i`, `Ko'olau`) instead of proper Hawaiian okinas (`Mokoliʻi`, `Koʻolau`). Also, `Mokolii island` is missing the okina on `Mokoliʻi` and capital `I` on `Island`.
* **❌ What needs fixing:** None.
* **🛠️ Specific fix recommendation:**
  Update the paragraph to use correct diacriticals and proper name capitalization:
  ```html
  <p>Rent a kayak and paddle to Mokoliʻi Island (also known as Chinaman's Hat) on the east shore of Oʻahu and experience both an ocean and mountain adventure. Ocean kayak over sheltered waters, hike on the trails of Mokoliʻi, and take in the magnificent views of the Koʻolau Mountain range. We will help you load the equipment and instruct you where to launch for your adventure. The kayak rental includes everything you need to have a safe and enjoyable experience. The Tandem Kayaks fit one or two people and include life vests, seat backs, and paddles. Book now to experience kayaking to Mokoliʻi, explore the tide pools and trails, and enjoy scenic views of the East shore of Oʻahu. </p>
  <p>👀 Check out our <a href="/activities/chinamans-hat-kayak-complete-self-guided-tour-guide/">Complete self-guided tour guide for Chinaman's Hat</a> for detailed tips, launch directions, and hiking route information.</p>
  ```

#### File 2: `site/guides/kailua-beach-park/index.html`
* **✅ What's done well:** Well-placed contextual link to the self-guided kayak tour of Kailua Bay & the Mokulua Islands.
* **⚠️ What could be improved:** In the preceding paragraph: `"Kailua Beach is the premier kayaking launch point on Windward Oahu."` -> should use proper okina: `"Windward Oʻahu"`.
* **❌ What needs fixing:** None.
* **🛠️ Specific fix recommendation:**
  Change "Windward Oahu" to "Windward Oʻahu".

#### File 3: `site/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html`
* **✅ What's done well:** Added a clean guided tour alternative link (`/activities/kailua-kayak-twin-islands-guided-tour/`) for customers wanting a guided experience.
* **⚠️ What could be improved:** None.
* **❌ What needs fixing:** None.
* **🛠️ Specific fix recommendation:** None.

#### File 4: `site/oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/index.html`
* **✅ What's done well:** Successfully added the cross-link to the Electric Beach guide.
* **⚠️ What could be improved:** Missing the okina on "Oahu".
* **❌ What needs fixing (P0):** **Factually Incorrect Content.** The added link description states: `"👀 Also check out our Electric Beach guide for another great Windward Oahu beach day..."` Electric Beach (Kahe Point Beach Park) is located on the **Leeward** (West) side of Oʻahu, not the **Windward** (East) side. Stating that it's another "Windward Oahu beach day" is misleading.
* **🛠️ Specific fix recommendation:**
  Update the text to specify Leeward coast and correct diacriticals:
  ```html
  <p>👀 Also check out our <a href="/guides/electric-beach/">Electric Beach guide</a> for another great Leeward Oʻahu beach day — warm waters, snorkeling, and sea turtles!</p>
  ```

#### File 5: `site/guides/index.html`
* **✅ What's done well:** Added Waimanalo Beach, Kailua Beach Park, and Electric Beach guides under a new section `Popular Beach & Adventure Guides`.
* **⚠️ What could be improved:** Missing Hawaiian macrons (kahakō) and okinas. "Waimanalo" should be "Waimānalo" (macron on the first `a`), and "Oahu's" should be "Oʻahu's".
* **❌ What needs fixing:** None.
* **🛠️ Specific fix recommendation:**
  ```html
  <li><a href="/guides/waimanalo-beach/">Waimānalo Beach Guide</a> — Oʻahu's longest stretch of white sand</li>
  ```

#### File 6: `site/activities/sharks-cove-self-guided-snorkel/index.html`
* **✅ What's done well:** Added a helpful FAQ/PAA cross-link to the Oahu snorkeling FAQ page.
* **⚠️ What could be improved:** "Oahu" is missing the okina ("Oʻahu").
* **❌ What needs fixing:** None (the placement was correct and validated inside the `<body>` element).
* **🛠️ Specific fix recommendation:**
  Change "Oahu snorkeling" to "Oʻahu snorkeling".

---

### 2. GRO-1225 — New Snorkel Gear Rentals Page

#### File 7: `site/rentals/snorkel-gear-rentals/index.html`
* **✅ What's done well:** Page is set up with good Yoast meta-tags, canonical link, English/Japanese alternates, and uses the responsive theme grid styling nicely.
* **⚠️ What could be improved:** Meta description and page title use "Oahu" instead of "Oʻahu" (missing okina).
* **❌ What needs fixing (P0):**
  1. **Incorrect Pricing Structure & Wrong FareHarbor Code:** Kai copied the pricing table and code integration from the **Lanikai Self-Guided Snorkel** activity page (item code `400783`). It lists "2 Hours" ($38) and "4 Hours" ($49) prices. But this is a **Rental** page, and the description explicitly states it is a "full-day rental." The pricing table conflicts with the description.
  2. **Wrong Product Booking calendar:** The page integrates the FareHarbor calendar for item `400783` (Lanikai Snorkel activity) instead of the actual snorkel rentals. The correct prices from the old page `oahu-snorkel-mask-and-fin-rentals` are:
     * **1 Day:** $18 (Item `7872`)
     * **2 Days:** $30 (Multi-day rental item `371661`)
     * **3 Days:** $36
     * **4 Days:** $44
     * **5 Days:** $50
     * **6 Days:** $54
     * **7 Days:** $56
     * **8+ Days:** $7/day
  3. **Broken HTML Links due to Escaped Quotes:** On line 465, the links to Sharks Cove and Windward to North Shore guides have backslashes escaping their double quotes (`href=\"...\"`), which breaks rendering in static HTML.
* **🛠️ Specific fix recommendation:**
  * Clean up line 465 to remove the backslashes from the quotes:
    ```html
    <p>Check out our <a href="/activities/sharks-cove-self-guided-snorkel/">Sharks Cove Self-Guided Snorkel guide</a> for tips on the best spots, and fuel up along the way with our <a href="/guides/eating-your-way-windward-to-north-shore/">Eating Your Way Windward to North Shore guide</a> — because snorkeling works up an appetite.</p>
    ```
  * Replace the main pricing table with the correct Single Day ($18) pricing and the correct FareHarbor button (`item: 7872`).
  * Verify that the multi-day table and FareHarbor button use item `371661`.

---

### 3. GRO-1226 — Kailua Kayak Duplicate Fix

#### File 8: `site/kailua-kayak/index.html`
* **✅ What's done well:** Canonical and English alternate tags successfully updated to point to the canonical URL `/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/`.
* **⚠️ What could be improved:** The `og:url` property is still pointing to the old URL `https://activeoahutours.com/kailua-kayak/`. It should be updated to point to the canonical URL for consistency.
* **❌ What needs fixing:** None.
* **🛠️ Specific fix recommendation:**
  ```html
  <meta content="https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" property="og:url"/>
  ```

#### File 9: `site/kayak-kailua/index.html`
* **✅ What's done well:** Canonical and English alternate tags updated.
* **⚠️ What could be improved:** `og:url` is still pointing to the old URL.
* **❌ What needs fixing (P0):** The Japanese alternate link (`hreflang="ja"`) was entirely removed from the head section. Instead of being deleted, it should have been updated to point to the canonical Japanese version `/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` to preserve correct multilingual mapping.
* **🛠️ Specific fix recommendation:**
  Restore the Japanese alternate tag and update it to the canonical Japanese URL, and update `og:url`:
  ```html
  <link href="https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" rel="canonical"/><link href="https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" hreflang="en" rel="alternate"/><link href="https://activeoahutours.com/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" hreflang="ja" rel="alternate"/>
  <meta content="https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" property="og:url"/>
  ```

#### File 10: `site/_redirects`
* **✅ What's done well:** English duplicate pages redirect to the canonical page with a proper 301 status.
* **❌ What needs fixing (P0):** Missing redirect for the Japanese duplicate page. Since `/ja/kayak-kailua/` exists as a duplicate file, it must also be redirected.
* **🛠️ Specific fix recommendation:**
  Add the following line to `site/_redirects`:
  ```text
  /ja/kayak-kailua/ /ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/ 301
  ```

#### Omitted File: `site/ja/kayak-kailua/index.html`
* **❌ What needs fixing (P0):** This file was completely missed during the duplicate cleanup. It must be updated to have its canonical and alternates point to `/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` (canonical) and `/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` (English alternate).
* **🛠️ Specific fix recommendation:**
  Update the canonical and alternate hreflang tags:
  ```html
  <link href="https://activeoahutours.com/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" rel="canonical"/><link href="https://activeoahutours.com/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" hreflang="en" rel="alternate"/><link href="https://activeoahutours.com/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/" hreflang="ja" rel="alternate"/>
  ```

---

### 4. GRO-1229 — Japanese Schema Cleanup

#### File 11: `site/ja/activities/sharks-cove-self-guided-snorkel/index.html`
* **✅ What's done well:** Translated schema fields naturally. Replaced machine-translated description with correct Japanese phrasing. Translated `touristType` array elements to native Japanese. Translated the Three Tables header and body text references to native Japanese "スリー・テーブルズ（Three Tables）".
* **⚠️ What could be improved:** None.
* **❌ What needs fixing:** None.

#### File 12: `site/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
* **✅ What's done well:** Corrected page description and schema trip description. Translated `touristType` variables and included correct okina in `Mokoliʻi Island`.
* **⚠️ What could be improved:** None.
* **❌ What needs fixing:** None.

#### File 13: `site/ja/rentals/oahu-beach-chair-rentals/index.html`
* **✅ What's done well:** Replaced unnatural description in Yoast meta headers and JSON-LD schema with professional Japanese translation.
* **⚠️ What could be improved:** None.
* **❌ What needs fixing:** None.

---

## Consolidated Action Plan

### P0 (Critical — Must Fix Immediately)
1. **Snorkel Rental Pricing & FareHarbor IDs:**
   * Replace the "2 Hours" ($38) and "4 Hours" ($49) table with a "1 Day" ($18) option.
   * Update FareHarbor calendar embed script and button link elements in `/rentals/snorkel-gear-rentals/index.html` to point to item `7872` (for 1 day) and verify multi-day uses `371661`.
2. **Snorkel Rental Escaped Links:**
   * Remove backslashes from the `href` attributes on line 465 of `site/rentals/snorkel-gear-rentals/index.html`.
3. **Electric Beach Coastline Correction:**
   * Correct "Windward Oahu" to "Leeward Oʻahu" in `site/oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/index.html`.
4. **Hreflang Alternate Restore:**
   * Restore the Japanese alternate tag pointing to the Japanese canonical page in `site/kayak-kailua/index.html`.
5. **Japanese Duplicate Page Canonical:**
   * Update canonical, alternates, and `og:url` tags in the Japanese duplicate file `site/ja/kayak-kailua/index.html`.
6. **Japanese Redirect rule:**
   * Add a 301 redirect for `/ja/kayak-kailua/` to `/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` in `site/_redirects`.

### P1 (High Priority — Hawaiian Orthography & Diacriticals)
1. **Mokoliʻi & Koʻolau Okinas:**
   * Change straight apostrophes (`Mokoli'i`, `Ko'olau`) to correct modifier letter turned commas (`Mokoliʻi`, `Koʻolau`) in `site/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html`.
   * Standardize `Mokolii island` to `Mokoliʻi Island`.
2. **Oʻahu Okinas:**
   * Replace instances of `Oahu` with `Oʻahu` in all updated content paragraphs (mokolii rentals, kailua beach park, guides list, sharks cove FAQ link).
3. **Waimānalo Macron:**
   * Change `Waimanalo` to `Waimānalo` in the guides list in `site/guides/index.html`.
4. **Open Graph og:url updates:**
   * Update `og:url` to match the new canonical paths in `site/kailua-kayak/index.html` and `site/kayak-kailua/index.html`.

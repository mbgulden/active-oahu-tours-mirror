# AGY SEO & Design Review Report (Phase 3)
**Linear Issue:** [GRO-1251](https://linear.app/growthwebdev/issue/GRO-1251)
**Date:** 2026-06-12
**Reviewer:** AGY

---

## 1. Executive Summary

This report covers Phase 3 of the three-phase audit and review cycle (P0 ✓ → P1 ✓ → P2). We have audited all P2 changes and content modifications introduced by Kai. Key changes were reviewed across visual design integration, multilingual content cohesion, Hawaiian orthography, schema logic, factual accuracy, and FareHarbor integration parameters.

All identified design gaps, placeholder values, unlocalized English blocks on Japanese pages, and broken redirect stubs rendering 404 templates have been resolved directly in the codebase on the feature branch `audit/agy-GRO-1251`.

---

## 2. Detailed File Audits

### 2.1 GRO-1237: Stand-Up Paddleboard (SUP) Rentals Rebuild (English & Japanese)
* **File Paths:**
  - `site/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html` (English)
  - `site/ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html` (Japanese)
  - `site/ja/stand-up-paddleboard-rental/index.html` (Japanese stub redirect)
* **Status:** ✅ Audited & Fixed

#### Evaluation:
* ✅ **What's good:** The English page has excellent content depth, describing trade wind conditions, beginner tips, spots, and return policies. It also includes comprehensive Product, FAQPage, and HowTo schemas.
* ⚠️ **Improvements:**
  - Standardized Hawaiian orthography (macrons/okinas) across user-facing text and metadata.
* ❌ **Needs fixing:**
  - **FareHarbor Copy-Paste Error (English & Japanese):** The single-day and multi-day booking buttons, as well as the calendar lazy-load script, pointed to snorkel gear item IDs (`7872` and `371661`) instead of actual SUP rental items.
  - **Japanese Content Gaps:** The Japanese page `/ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/` was missing translated equivalents of the new English sections ("SUP Tips", "Best SUP Spots", "SUP for Beginners", and "After-Hours returns").
  - **Missing Japanese Schemas:** The FAQPage and HowTo schemas were absent on the Japanese page.
  - **404 Redirect Stub Failure:** The Japanese redirect stub `/ja/stand-up-paddleboard-rental/` rendered a 404 page template instead of redirecting to the canonical Japanese SUP page.
* 🔧 **Specific fixes:**
  - Corrected FareHarbor item IDs in English and Japanese files: Single-day updated to `368417`, Multi-day updated to `371689`, and scriptSrc updated to `368417,371689`.
  - Translated and injected the expanded sections ("SUP Tips", "Best SUP Spots", "SUP for Beginners", and "After-Hours returns") into the Japanese rentals page.
  - Localized and added FAQPage, HowTo, and expanded Product schemas to the Japanese page.
  - Replaced the 1050-line 404 error template in `/ja/stand-up-paddleboard-rental/index.html` with a clean, fast-redirect stub.

---

### 2.2 GRO-1235: Japanese Page Content Expansion
* **File Paths:**
  - `site/ja/activities/sharks-cove-self-guided-snorkel/index.html` (Sharks Cove)
  - `site/ja/rentals/oahu-beach-chair-rentals/index.html` (Beach Chairs)
  - `site/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html` (Kailua Kayak Rentals)
  - `site/ja/kaneohe-bay-sandbar-kayak/index.html` (Kaneohe Sandbar stub)
  - `site/ja/kayak-kailua/index.html` (Kailua Kayak stub)
  - `site/ja/chinamans-hat-kayak-tour/index.html` (Chinaman's Hat stub)
  - `site/ja/sharks-cove-snorkeling/index.html` (Sharks Cove stub)
* **Status:** ✅ Audited & Fixed

#### Evaluation:
* ✅ **What's good:** The Japanese pages have been expanded with local routes, maps, and specific gear details.
* ❌ **Needs fixing:**
  - **Untranslated English Blocks:** Several paragraphs were left entirely in English on the Japanese versions (wildlife sanctuary guidelines on Mokulua, Kaneohe Bay Sandbar overview, and Sharks Cove entry/parking info).
  - **404 Redirect Stub Failures:** Several Japanese stub URLs that correspond to English redirect pages (e.g. `/ja/kayak-kailua/`, `/ja/sharks-cove-snorkeling/`) rendered full 404 templates rather than executing `http-equiv="refresh"` redirects.
* 🔧 **Specific fixes:**
  - Translated and replaced all remaining English paragraphs with high-quality, natural Japanese descriptions across the three priority pages.
  - Replaced the 404 templates at `/ja/kaneohe-bay-sandbar-kayak/`, `/ja/kayak-kailua/`, `/ja/chinamans-hat-kayak-tour/`, and `/ja/sharks-cove-snorkeling/` with optimized redirect stubs pointing to their respective canonical Japanese counterparts.

---

## 3. Summary of Code Changes

| File Path | Description of Changes |
|---|---|
| `site/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html` | Updated FareHarbor booking button item IDs and lazy-load script to point to SUP item IDs (`368417`, `371689`) instead of snorkel items. |
| `site/ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html` | Injected SUP Tips, Spots, Beginner, and Return sections in Japanese. Localized Product, FAQPage, and HowTo schemas. Corrected FareHarbor IDs to `368417`/`371689`. |
| `site/ja/stand-up-paddleboard-rental/index.html` | Replaced 404 page template with redirect stub to `/ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/`. |
| `site/ja/activities/sharks-cove-self-guided-snorkel/index.html` | Translated remaining English paragraphs (entry guidelines and parking instructions) to Japanese. |
| `site/ja/rentals/oahu-beach-chair-rentals/index.html` | Translated remaining English overview paragraph to Japanese. |
| `site/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html` | Translated remaining English paragraphs (wedge-tail shearwater nesting and Kaneohe Sandbar description) and links to Japanese. |
| `site/ja/kaneohe-bay-sandbar-kayak/index.html` | Replaced 404 page template with redirect stub to `/ja/kaneohe-sandbar/`. |
| `site/ja/kayak-kailua/index.html` | Replaced 404 page template with redirect stub to `/ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/`. |
| `site/ja/chinamans-hat-kayak-tour/index.html` | Replaced 404 page template with redirect stub to `/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/`. |
| `site/ja/sharks-cove-snorkeling/index.html` | Replaced 404 page template with redirect stub to `/ja/activities/sharks-cove-self-guided-snorkel/`. |

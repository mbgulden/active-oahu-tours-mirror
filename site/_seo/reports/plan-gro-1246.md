### 📋 Implementation Plan: GRO-1246 — Phase 2: Review all P1 changes by Kai

Below is the planned approach to execute the second review cycle of all P1 pages and content changes introduced by Kai.

#### 1. What I Will Do
* **Audit Kawela Bay Page (GRO-1239):** Inspect `/home/ubuntu/work/active-oahu-static/site/activities/kawela-bay-self-guided-kayak-tour/index.html` for layout structure, price descriptions, FareHarbor integration, correct image alt attributes, and canonical/hreflang tags.
* **Audit Abigail's Local Narratives (GRO-1240):** Inspect the newly added "Legend of Mokoliʻi" on Chinaman's Hat page (`site/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`) and the "History of Kahana Valley" narrative on Kahana Rainforest River page (`site/activities/kahana-rainforest-river-oahu-kayak-tour/index.html`). Validate multilingual alignment (ensure Japanese translation files also contain these narratives).
* **Audit Oahu Kayak Safety & Tide Guide (GRO-1241):** Inspect `site/guides/oahu-kayak-safety-tide-guide/index.html`. Verify that it is fully styled with theme templates, headers/footers, and lists correct links to tours instead of placeholder `/tours/` links. Ensure it is integrated into the guides catalog `site/guides/index.html` (resolving orphan status).
* **Hawaiian Orthography Validation:** Audit all target pages to ensure proper use of the okina (`ʻ`) and kahakō (macrons) in place of plain/straight spellings.
* **Schema Validation:** Verify that the organization schema has the active shop phone number (`+1-808-498-1894`) instead of placeholder values.
* **Check Link Integrity:** Run link checker script to ensure no new broken links are introduced.
* **Review Report Deliverable:** Verify and finalize `/home/ubuntu/work/active-oahu-static/site/_seo/reviews/agy-p1-review-2026-06-12.md`.

#### 2. Artifacts to Be Audited/Created
* **Review Report:** `/home/ubuntu/work/active-oahu-static/site/_seo/reviews/agy-p1-review-2026-06-12.md`
* **Target Pages Audited:**
  - `site/activities/kawela-bay-self-guided-kayak-tour/index.html`
  - `site/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
  - `site/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
  - `site/activities/kahana-rainforest-river-oahu-kayak-tour/index.html`
  - `site/ja/activities/kahana-rainforest-river-oahu-kayak-tour/index.html`
  - `site/guides/oahu-kayak-safety-tide-guide/index.html`
  - `site/guides/index.html`

#### 3. Verification Steps
* Run `python3 check_links.py` to confirm link integrity.
* Perform manual/grep sweeps on the target pages for plain text spelling.
* Confirm successful generation and git status of the report.

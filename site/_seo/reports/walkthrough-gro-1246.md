### 🏁 Walkthrough: GRO-1246 — Phase 2: Review all P1 changes by Kai (DONE)

This is the definitive done signal for GRO-1246. Below is the step-by-step walkthrough of the completed tasks, all created/modified artifacts with absolute paths, and verification steps.

#### 1. Step-by-Step Walkthrough
1. **Plan Posted:** Registered the implementation plan via issue comment.
2. **Audit & Review:** Audited Kawela Bay, Chinaman's Hat, Kahana Valley, and safety guide pages for diacriticals, layout, multilingual alignment, and schema accuracy.
3. **Design & Code Fixes:** Rebuilt the unstyled safety guide page into a standard theme page, translated legends/stories into Japanese, corrected phone schemas, and applied Hawaiian orthography corrections.
4. **Link Integrity Check:** Ran `check_links.py` to verify all links are correct.
5. **Git Sync:** Synchronized all modifications to both local repositories, committed and pushed branch `audit/agy-GRO-1246`.
6. **Issue Relabeled:** Re-labeled the issue to `agent:fred` on Linear.

#### 2. Produced/Modified Artifacts (Absolute Paths)

##### 📖 Reports & Planning:
* `/home/ubuntu/work/active-oahu-static/site/_seo/reviews/agy-p1-review-2026-06-12.md` — Main review report containing positives, improvements, bugs, and fixes.
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/plan-gro-1246.md` — Implementation plan comment source.
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/summary-gro-1246.md` — Summary comment source.
* `/home/ubuntu/work/active-oahu-static/site/_seo/reports/walkthrough-gro-1246.md` — Walkthrough comment source.

##### 💻 Code & HTML Files Modified:
* `/home/ubuntu/work/active-oahu-static/site/activities/kawela-bay-self-guided-kayak-tour/index.html` — Alt tag addition, Hawaiian orthography standardization.
* `/home/ubuntu/work/active-oahu-static/site/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html` — Schema telephone correction, Hawaiian orthography.
* `/home/ubuntu/work/active-oahu-static/site/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html` — Schema telephone correction, Japanese translation of Mokoliʻi legend.
* `/home/ubuntu/work/active-oahu-static/site/activities/kahana-rainforest-river-oahu-kayak-tour/index.html` — Schema telephone correction, Hawaiian orthography.
* `/home/ubuntu/work/active-oahu-static/site/ja/activities/kahana-rainforest-river-oahu-kayak-tour/index.html` — Schema telephone correction, Japanese translation of Kahana Valley history.
* `/home/ubuntu/work/active-oahu-static/site/guides/oahu-kayak-safety-tide-guide/index.html` — Redesigned theme wrapper layout, resolved /tours/ links, schema telephone correction.
* `/home/ubuntu/work/active-oahu-static/site/guides/index.html` — Added safety guide link to resolve orphan page status.

#### 3. Verification Steps
1. **Link Verification:** Run `python3 check_links.py` to confirm that no links on these pages are broken.
2. **Visual Inspection:** Verify the safety guide has standard styling and elements by opening `site/guides/oahu-kayak-safety-tide-guide/index.html`.
3. **Japanese Content Verification:** Inspect `site/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html` (lines 650-665) and `site/ja/activities/kahana-rainforest-river-oahu-kayak-tour/index.html` (lines 640-650) to confirm the translated narratives.
4. **Orthography Verification:** Run grep on any target page for plain spelling of `Oahu` or straight quote `O'ahu` to verify that only correct character forms like `Oʻahu` exist in user-facing content.

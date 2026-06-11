# Schema Validation Checklist

This checklist is designed to verify that the schema has been injected correctly and will be recognized by search engines without warnings or errors.

## Google Rich Results Testing Links

For each template category, use the following test query URLs on the [Google Rich Results Test](https://search.google.com/test/rich-results) tool to preview and validate the markup.

* **Homepage (TravelAgency / LocalBusiness):**
  - Live URL to Test: `https://activeoahutours.com/`
  - Validation: Verify that both a `LocalBusiness` and `TravelAgency` item are detected with zero errors.
* **Tours (TouristTrip):**
  - Live URL to Test: `https://activeoahutours.com/activities/chinamans-hat-self-guided-oahu-kayak-tour/`
  - Validation: Verify that `TouristTrip` is detected and its provider matches AOT.
* **Rentals (Product):**
  - Live URL to Test: `https://activeoahutours.com/rentals/oahu-beach-chair-rentals/`
  - Validation: Verify that a `Product` item is detected, containing an `Offer` with a price and `availability: InStock`.
* **Hub Pages (ItemList + TouristAttraction):**
  - Live URL to Test: `https://activeoahutours.com/activities/`
  - Validation: Verify `ItemList` is detected and lists the respective sub-activities.
* **FAQs (FAQPage):**
  - Live URL to Test: `https://activeoahutours.com/faq/`
  - Validation: Verify that all questions and answers are correctly paired under `FAQPage`.
* **Blog Guides (Article):**
  - Live URL to Test: `https://activeoahutours.com/guides/lanikai-beach/`
  - Validation: Verify `Article` is detected and publisher details are populated.

---

## Common Schema Errors to Avoid

1. **Unescaped Quotes in JSON-LD:**
   - *Issue:* Standard quotes (`"`) inside text fields (like descriptions) break the JSON syntax.
   - *Fix:* Ensure all text quotes inside schema strings are escaped as `\"` or replaced with single quotes.
2. **Missing Offer Price or Currency:**
   - *Issue:* Product schema requires a valid price and currency (e.g. `USD`). Without these, search engines trigger warnings.
   - *Fix:* Ensure `price` (e.g., `45.00` as string or number) and `priceCurrency` (e.g., `USD`) are set.
3. **Invalid Locale / Text Encoding:**
   - *Issue:* Japanese characters in JA schema templates must be saved in UTF-8 encoding without being escaped as unicode entities (like `\u30a2`).
   - *Fix:* Keep `ensure_ascii=False` when serializing JSON files to write raw characters.
4. **GeoCoordinates Format:**
   - *Issue:* Latitude and longitude must be numbers, not strings.
   - *Fix:* Set `"latitude": 21.3985` (no quotes around numbers).

---

## Verification Steps (Kai / Fred)

1. **Verify head element presence:**
   - Run a terminal command on the site root:
     ```bash
     grep -c "</head>" site/rentals/oahu-beach-chair-rentals/index.html
     ```
     Should return exactly `1`.
2. **Verify schema script presence:**
   - Run:
     ```bash
     grep -c "application/ld+json" site/rentals/oahu-beach-chair-rentals/index.html
     ```
     Should return at least `1`.
3. **Verify Japanese locales:**
   - Ensure the Japanese schema templates contain `"inLanguage": "ja-JP"` or use Japanese text.

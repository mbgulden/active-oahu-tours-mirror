# GRO-1539: Inline Text Booking Link Audit

**Date**: 2026-06-13  
**Scanned**: 13 guide pages (entry-content areas)  
**Parent**: GRO-1300 — Replace weak inline text booking links with visible buttons

---

## HIGH PRIORITY — Clear inline CTAs that should be styled buttons

| # | Page | Link Text | URL | Notes |
|---|------|-----------|-----|-------|
| 1 | `guides/oahu-wildlife-seabird-sanctuaries-guide/` | **"Book your kayak rental here"** | `/rentals/oahu-tandem-kayak-rentals/` | Genuine inline CTA in paragraph content. Should be a styled button. |
| 2 | `guides/eating-your-way-windward-to-north-shore/` | **"→ Book the Sharks Cove Snorkel Experience"** | `/activities/sharks-cove-self-guided-snorkel/` | CTA-style text with arrow. Inline paragraph link. |
| 3 | `guides/lanikai-pillbox-hike/` | **"electric bike rentals"** | `/electric-bike-rentals/` | Plain text link for rentals within content. |
| 4 | `guides/waimanalo-beach/` | **"rent beach gear in Kailua"** | `/rentals/` | Inline text link for rentals within content. |
| 5 | `guides/oahu-kayak-safety-tide-guide/` | **"→ Kailua Beach Kayak Rentals"** | `/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/` | CTA-style text with arrow. Should be a button. |
| 6 | `guides/oahu-kayak-safety-tide-guide/` | **"→ Kāneʻohe Sandbar Kayak Experience"** | `/kaneohe-bay-sandbar-kayak/` | CTA-style text with arrow. |
| 7 | `guides/oahu-kayak-safety-tide-guide/` | **"→ Chinaman's Hat (Mokoliʻi) Kayak Tour"** | `/activities/chinamans-hat-self-guided-oahu-kayak-tour/` | CTA-style text with arrow. |
| 8 | `guides/oahu-kayak-safety-tide-guide/` | **"→ Kahana River Kayak Tour"** | `/activities/kahana-rainforest-river-oahu-kayak-tour/` | CTA-style text with arrow. |

## MEDIUM PRIORITY — Contextual content links (could be improved)

| # | Page | Link Text | Notes |
|---|------|-----------|-------|
| 9 | `guides/ocean-kayaking-beginners-oahu/` | "kayak and beach gear rental delivery service" | Contextual content paragraph link to rentals |
| 10 | `guides/lanikai-beach/` | "Learn more about our Mokulua Islands Kayak Adventure." | Contextual link in content body |
| 11 | `guides/kailua-beach-park/` | "self-guided kayak tour of Kailua Bay & the Mokulua Islands" | Contextual link in content body |

## Pages Already Equipped

These pages already have properly styled booking buttons (btn-primary, inline styling):
- All 13 guide pages have FareHarbor booking buttons in the post-content CTA area
- `ocean-kayaking-beginners-oahu/` has a styled "Book a Kayak Tour or Rental" button
- `lanikai-beach/` has a styled "Reserve Your Kayak Rental" button
- `eating-your-way-windward-to-north-shore/` has styled "Book Your Adventure Now" button
- `oahu-kayak-safety-tide-guide/` has styled "Book Your Adventure Now" button

## Recommendation

Replace the 8 HIGH PRIORITY inline text links with styled CTA buttons matching the existing button design (background: #006699, white text, 12px padding, border-radius: 4px). These are all in content areas where a CTA button would improve conversion rates.

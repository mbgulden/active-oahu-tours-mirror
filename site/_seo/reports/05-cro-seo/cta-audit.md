# Call-to-Action (CTA) Audit

**Date:** 2026-06-12  
**Source Data:** Automated CTA scan of 163 pages in `active-oahu-static/site`  

---

## 1. CTA Typology & Inventory

The site uses a mix of global header CTAs, generic calendar links, and item-specific buttons. Below is the inventory of CTA types found across the 163 audited pages:

| CTA Type | Text / Copy | Target URL / Action | Placement | Frequency | Copy Effectiveness |
|---|---|---|---|---|---|
| **Global Header CTA** | "Book Online" (with calendar icon) | `/embeds/book/activeoahutours/?u=f9b48...` | Top-right header, sticky | 163 pages | 🟡 **Moderate**: Visible, but opens the entire catalog instead of the current page's item. |
| **Catalog Booking CTA** | "Rent Kayaks & Beach Gear" | `/embeds/book/activeoahutours/?u=091a2...` | Homepage, category pages | ~10 pages | 🟡 **Moderate**: Directs to calendar, but lacks specific product focus. |
| **Item Booking Button** | "Book" or "Book Now" | `FH.open({'item':'XXXXXX'})` | Individual tour/rental pages | ~35 pages | 🟢 **Strong**: Directly opens the specific product widget, minimizing choices. |
| **Inline Text Booking** | "online booking calendar" or similar | `/embeds/book/activeoahutours/...` | Blog posts, guide descriptions | ~25 pages | 🔴 **Weak**: Text links are easily missed, low visual prominence. |
| **Guides Booking Button** | "Book" (linking to rental items) | `FH.open({'item':'115595'})` | Snorkeling, hiking, or tide guides | 11 pages | 🔴 **Weak**: Links to generic kayak rentals instead of snorkeling/hiking items. |

---

## 2. Placement & UX Analysis

### Desktop vs. Mobile Layouts:
1. **Above-the-Fold (ATF) Visibility**:
   * **Homepage**: The hero contains the title "Oahu Kayak Rentals & Tours" but the CTA button "Book Online" is placed far to the right in the navigation area. The center-left text section has a secondary "Book Online" button, but it competes with a transparent TripAdvisor logo.
   * **Product Pages (Tours/Rentals)**: On desktop, the primary CTA button is located next to the prices. On mobile, this requires scrolling down 1.5 to 2 full screens to find the "Book" button.
2. **Sticky Navigation**:
   * The header "Book Online" button is sticky, which keeps a purchase path always available. However, because it opens the *global* catalog rather than the item the user is reading about, it causes user confusion and drop-offs.
3. **Price/Button Proximity**:
   * Pricing details (e.g. "$49 per day") are often separated from the "Book" button by images or paragraphs, breaking the decision-making flow.

---

## 3. Copy Effectiveness & Recommendations

The current copy relies on generic words like "Book" or "Book Online". We recommend moving to more active, value-oriented copy:

* **Generic**: "Book Online"  
  * **Optimized**: "Check Availability & Prices" (Reduces purchase friction; feels exploratory).
* **Generic**: "Book"  
  * **Optimized**: "Book Chinaman's Hat Rental" or "Reserve Tandem Kayak" (Locks in specific intent).
* **Generic**: "Rent Kayaks & Beach Gear"  
  * **Optimized**: "Rent Kayaks from $49" (Features value/pricing upfront).

---

## 4. Page-Type Recommendations

### 1. Homepage (`index.html`)
* **Current state**: Generic buttons loading the global widget.
* **Recommendation**: Replace generic links with a 3-column product grid featuring:
  1. *Chinaman's Hat Kayak Rentals* ($49/day) -> CTA: "Reserve Kayak"
  2. *Kaneohe Sandbar Kayak Experience* ($79/day) -> CTA: "Book Experience"
  3. *Kailua Guided Kayak Tour* ($129) -> CTA: "Book Tour"
  * **Visual Target**: Implement the design from the generated [optimized_cta_mockup.png](file:///home/ubuntu/work/active-oahu-static/site/_seo/images/optimized_cta_mockup.png) featuring a clear pricing structure and trust signals directly adjacent to the CTAs.

### 2. Tour & Rental Pages (e.g., `/rentals/oahu-tandem-kayak-rentals/`)
* **Current state**: "Book" button located below the fold.
* **Recommendation**: Implement a floating mobile bottom bar that anchors a "Book Now from $49" button to the bottom of the screen as the user scrolls.

### 3. Informational Guides (e.g., `/guides/lanikai-beach/`)
* **Current state**: Linking to generic kayak/bike calendars.
* **Recommendation**: Insert a high-contrast "Recommended Gear for Lanikai Snorkeling" banner with a direct booking button for snorkeling sets, rather than linking to the generic home calendar.

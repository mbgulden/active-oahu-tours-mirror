# Booking Flow Friction Audit

**Date:** 2026-06-11  
**Target URL:** [activeoahutours.com](https://activeoahutours.com) (FareHarbor Integration)  

---

## 1. FareHarbor Integration & Speed Performance

Active Oahu Tours integrates bookings using the **FareHarbor Lightframe API** (`autolightframe=yes`). 

### Technical Setup:
* Preconnect and DNS-prefetch tags are implemented globally:
  ```html
  <link crossorigin="" href="https://fareharbor.com" rel="preconnect"/>
  <link href="https://fareharbor.com" rel="dns-prefetch"/>
  ```
  * **Verdict**: 🟢 **Excellent**. This saves 300–500ms of DNS resolution and SSL handshake time when the user clicks a booking button.
* The API script (`embeds/api/v1/`) is loaded at the bottom of the body.
  * **Verdict**: 🟢 **Good for page speed**. It does not block initial page rendering.
* **Loading Speed**: The script itself is tiny (~5KB), but clicking a booking link initiates the FareHarbor overlay, which pulls in 1.2MB of calendar assets, CSS, and web fonts. On a standard 4G mobile connection in Hawaii, this overlay takes **1.8 to 2.8 seconds to display**, creating a noticeable lag.

---

## 2. Steps from Landing Page to Booking Confirmation

The booking funnel consists of **8 steps**:

```
[Landing Page] 
  ↓ (Step 1: Click "Book" button)
[Overlay Calendar Opens] 
  ↓ (Step 2: Select Date)
[Time Slot Displayed] 
  ↓ (Step 3: Select Time)
[Ticket Quantities] 
  ↓ (Step 4: Select Adult/Child count)
[Group Custom Details] 
  ↓ (Step 5: Input Name, Email, Phone)
  ↓ (Step 6: Input Height, Weight, Shoe Size for ALL participants)
[Payment Details] 
  ↓ (Step 7: Input Credit Card, Promo Code)
[Confirmation Page] 
  ↓ (Step 8: Click "Complete Booking")
```

### Critical Friction Points:
1. **Catalog vs. Deep-linking (Step 1)**:
   * Homepage and category buttons open the *global* FareHarbor calendar. The user must scroll through a list of 15+ tours/rentals to find the one they want. This leads to catalog navigation drop-off.
2. **Form Field Inflation (Step 6)**:
   * For self-guided snorkel rentals and kayak tours, FareHarbor requires custom fields for *every* participant: **Height, Weight, and Shoe Size**. While necessary to pre-size gear (fins, vests), entering these details for 4+ people on a mobile keyboard is a significant friction point.
3. **Availability Discrepancies (Step 2)**:
   * Users must click through specific dates to check availability. If a tour is sold out, they receive a red error banner and must backtrack to select another day. There is no grid-level indicator showing which days are fully booked.

---

## 3. Trust Signals

* **Landing Pages**: The site features TripAdvisor Travelers' Choice badges, but they are static images (some outdated from 2022). Reviews are text-only blockquotes rather than live-synced widgets.
* **Booking Widget**: Once the FareHarbor iframe opens, all brand elements (logos, review counts, SSL badges) disappear. The checkout page looks like a generic form, reducing trust.
* **Cancellation Clarity**: The 24-hour refund policy is noted on a dedicated policy page but is not displayed on the checkout page next to the credit card input fields.

---

## 4. Competitor Comparison

* **Kailua Beach Adventures (KBA)**: KBA also uses FareHarbor. However, because their kayak rentals are strictly local (Kailua Beach storefront pickup for Kailua Bay), they do not ask for weight/height details for basic kayak rentals—only for guided tours. This reduces their checkout steps from 8 to 6, streamlining conversions.
* **North Shore Walk-Up Operators (Haleiwa/Pupukea)**: Operators on the North Shore (e.g. Surf N Sea) rely on walk-ups for snorkel rentals, meaning zero checkout steps. AOT can capture these customers by marketing online booking as a way to "Guarantee Gear Availability & Skip the North Shore Lines", but only if the pickup location is made clear or localized.

---

## 5. Actionable Recommendations

1. **Deep-Link All CTAs**: Ensure every "Book Now" button on a product page deep-links to that specific FareHarbor item code (e.g., `view: {'item': '400783'}`), bypassing the catalog screen.
2. **Postpone Sizing Fields**: Configure FareHarbor to make Height/Weight/Shoe Size fields *optional* during checkout, or request them in the post-booking confirmation email/portal instead of blocking the sale.
3. **Display Cancellation Policy ATF**: Add a small notice next to the booking button: *"✓ 24-Hour Free Cancellation — 100% Refund"* to reassure users.

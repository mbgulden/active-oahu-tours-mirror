# GRO-1198: FareHarbor Checkout — Postpone Height/Weight/Shoe Fields

## Issue
FareHarbor requires Height, Weight, and Shoe Size for ALL participants during checkout (Step 6 of 8). This creates significant mobile friction, especially for group bookings (4+ people).

## Recommendation
Make these fields **optional** during checkout or move them to a post-booking confirmation flow:

### Option A: FareHarbor Dashboard (Recommended)
1. Log into FareHarbor Dashboard → Items → [Each Tour/Rental Item]
2. Under "Custom Fields" or "Participant Questions":
   - Set Height/Weight/Shoe Size fields to **"Optional"** (not required)
3. Add an automated post-booking email asking participants to provide sizing details
4. This reduces checkout steps from 8 to 6, matching competitor KBA's flow

### Option B: JavaScript Workaround (Fallback)
If FareHarbor doesn't support optional fields, a client-side script can pre-fill default values
and hide the fields from view. This is less ideal but works as a stopgap.

### Competitor Comparison
- **Kailua Beach Adventures (KBA)**: Only asks for height/weight on guided tours (not basic rentals) → 6-step checkout
- **Active Oahu currently**: 8-step checkout with sizing for every participant on every booking

## Action Required
Michael: Log into FareHarbor Dashboard and set participant sizing fields to optional for self-guided tours and basic rentals.

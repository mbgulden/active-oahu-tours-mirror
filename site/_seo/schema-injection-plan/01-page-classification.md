# Page Type Classification Plan

This document contains the schema classification for every page on the Active Oahu Tours (AOT) website, covering English (EN) and Japanese (JA) locales. 

## Summary Counts

| Page Type | Locale | Schema Type | Page Count |
| :--- | :--- | :--- | :--- |
| Blog/Guide | EN | Article | 45 |
| Blog/Guide | JA | Article | 11 |
| Contact | EN | ContactPage | 2 |
| Contact | JA | ContactPage | 1 |
| FAQ | EN | FAQPage | 5 |
| FAQ | JA | FAQPage | 4 |
| Homepage | EN | TravelAgency + LocalBusiness + Travel | 1 |
| Homepage | JA | TravelAgency + LocalBusiness + Travel | 1 |
| Location/Hub | EN | ItemList + TouristAttraction | 15 |
| Location/Hub | JA | ItemList + TouristAttraction | 9 |
| Other | EN | WebPage | 60 |
| Other | JA | WebPage | 26 |
| Rental | EN | Product | 30 |
| Rental | JA | Product | 21 |
| Tour | EN | TouristTrip | 24 |
| Tour | JA | TouristTrip | 16 |

## Detailed Page Mapping

### Blog/Guide Pages (Schema: `Article`)

#### English Pages (EN)
- `chinamans-hat-tide-guide/index.html`
- `guides/chinamans-hat-tide-guide/index.html`
- `guides/eating-your-way-windward-to-north-shore/index.html`
- `guides/electric-beach/index.html`
- `guides/kailua-beach-park/index.html`
- `guides/lanikai-beach/index.html`
- `guides/ocean-kayaking-beginners-oahu/index.html`
- `guides/sea-turtles-oahu/index.html`
- `guides/waimanalo-beach/index.html`
- `kaneohe-sandbar-tide-guide/index.html`
- `kayak-safety-guide/index.html`
- `kualoa-bay-guide/index.html`
- `lanikai-vs-hanauma-bay-snorkeling/index.html`
- `oahu-hawaii-kayaking-guide/index.html`
- `oahu-hawaii-kayaking-guide/renting-a-kayak-and-paddling-to-mokolii-island-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/best-places-to-kayak-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/discover-oahus-best-snorkel-spot-at-electric-beach/index.html`
- `oahu-kayaking-and-beach-adventures/e-bike-rentals-in-kailua/index.html`
- `oahu-kayaking-and-beach-adventures/guide-to-towing-kayaks-with-e-bikes-in-kailua/index.html`
- `oahu-kayaking-and-beach-adventures/hidden-hawaiian-paradise-explore-kawela-bay-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/honolulu-the-best-food-activities-and-social-scene-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/kailua-e-bike-kau-kau-guided-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/kalama-beach-bodyboarding-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/kaneohe-sandbar-kayak-experience/index.html`
- `oahu-kayaking-and-beach-adventures/kaneohe-sandbar-self-guided-kayak-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/kayak-deliveries-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/lanikai-e-bike-and-snorkel-self-guided-tour/index.html`
- `oahu-kayaking-and-beach-adventures/lanikai-e-bike-snorkel-and-pillbox-hike-self-guided-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/lanikai-pillbox-hike-adventure-guide/index.html`
- `oahu-kayaking-and-beach-adventures/mokulua-islands-self-guided-kayak-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/index.html`
- `oahu-kayaking-and-beach-adventures/rent-beach-gear-for-multiple-days-with-active-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/store-your-bags-explore-kailua-bounce-luggage-storage-service-available-at-active-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/the-ultimate-guide-for-the-north-shore-of-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/the-ultimate-guide-to-exploring-windward-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/top-5-things-to-do-on-oahu/index.html`
- `oahu-kayaking-and-beach-adventures/top-things-to-do-near-ko-olina-resort/index.html`
- `oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/index.html`
- `oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/index.html`
- `oahu-kayaking-and-beach-adventures/what-to-do-in-kailua-hidden-gems-and-must-sees/index.html`
- `oahu-launch-guide/index.html`
- `sharks-cove-snorkeling-guide/index.html`
- `sharks-cove-vs-lanikai-snorkeling/index.html`

#### Japanese Pages (JA)
- `ja/oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/kalama-beach-bodyboarding-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/kaneohe-sandbar-self-guided-kayak-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/lanikai-e-bike-and-snorkel-self-guided-tour/index.html`
- `ja/oahu-kayaking-and-beach-adventures/lanikai-e-bike-snorkel-and-pillbox-hike-self-guided-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/lanikai-pillbox-hike-adventure-guide/index.html`
- `ja/oahu-kayaking-and-beach-adventures/mokulua-islands-self-guided-kayak-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/index.html`
- `ja/oahu-kayaking-and-beach-adventures/ultimate-guide-for-kailua-beach-park-experience-windward-oahus-safest-and-most-adventurous-beach/index.html`
- `ja/oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/index.html`

### Contact Pages (Schema: `ContactPage`)

#### English Pages (EN)
- `contact-us.html`
- `contact-us/index.html`

#### Japanese Pages (JA)
- `ja/contact-us/index.html`

### FAQ Pages (Schema: `FAQPage`)

#### English Pages (EN)
- `faq-oahu-beach-gear-rentals/index.html`
- `faq/faq-chinamans-hat-kayak-hike/index.html`
- `faq/faq-oahu-beach-gear-rentals/index.html`
- `faq/index.html`
- `paa-answers/index.html`

#### Japanese Pages (JA)
- `ja/faq-oahu-beach-gear-rentals/index.html`
- `ja/faq/faq-chinamans-hat-kayak-hike/index.html`
- `ja/faq/faq-oahu-beach-gear-rentals/index.html`
- `ja/faq/index.html`

### Homepage Pages (Schema: `TravelAgency + LocalBusiness + Travel`)

#### English Pages (EN)
- `index.html`

#### Japanese Pages (JA)
- `ja/index.html`

### Location/Hub Pages (Schema: `ItemList + TouristAttraction`)

#### English Pages (EN)
- `about-active-oahu-tours/awards/index.html`
- `activities.html`
- `activities/index.html`
- `activities/page/2/index.html`
- `activities/page/3/index.html`
- `guided-tours/index.html`
- `guides/index.html`
- `multi-day-kayak-and-beach-gear-rentals/index.html`
- `multi-day-rentals/index.html`
- `oahu-equipment-rentals/index.html`
- `oahu-equipment-rentals/page/2/index.html`
- `oahu-kayaking-and-beach-adventures/index.html`
- `rentals/index.html`
- `self-guided/index.html`
- `tours/index.html`

#### Japanese Pages (JA)
- `ja/about-active-oahu-tours/awards/index.html`
- `ja/activities/index.html`
- `ja/activities/page/2/index.html`
- `ja/activities/page/3/index.html`
- `ja/guides/index.html`
- `ja/multi-day-kayak-and-beach-gear-rentals/index.html`
- `ja/oahu-equipment-rentals/index.html`
- `ja/oahu-equipment-rentals/page/2/index.html`
- `ja/oahu-kayaking-and-beach-adventures/index.html`

### Other Pages (Schema: `WebPage`)

#### English Pages (EN)
- `404.html`
- `_includes/tide-chart-template.html`
- `_templates/body_bottom.html`
- `_templates/body_top.html`
- `_templates/head.html`
- `about-active-oahu-tours/awards/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/index.html`
- `about-active-oahu-tours/awards/active-oahu-recognized-one-top-10-hospitality-businesses-world/index.html`
- `about-active-oahu-tours/index.html`
- `about-active-oahu/index.html`
- `active-aloha-ambassador/index.html`
- `active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/index.html`
- `active-oahu-photo-gallery/index.html`
- `ariyoshis-summer-vacation-rainforest-kayak-tour-oahu-hawaii-2017/index.html`
- `author/mbgulden/index.html`
- `become-a-partner/index.html`
- `cancellation-policy/index.html`
- `chinamans-hat/index.html`
- `job-dashboard/index.html`
- `job/hiring-kayak-delivery-driver-jobs-in-laie/index.html`
- `join-the-team/index.html`
- `kailua-ebike-route/index.html`
- `kailua-kayak/index.html`
- `kailua-oahu-storefront/index.html`
- `kailua-town-history/index.html`
- `kaneohe-sandbar/index.html`
- `kayak-kailua/index.html`
- `laie-bay-goat-island-kayaking/index.html`
- `living-aloha-respectful-travel/index.html`
- `mokolii/index.html`
- `multi-activity-adventure-packages/index.html`
- `oahu-tour-packages/index.html`
- `oahus-best-kayaking-trips/index.html`
- `privacy-policy/index.html`
- `reviews/index.html`
- `reviews/page/2/index.html`
- `reviews/page/3/index.html`
- `reviews/page/4/index.html`
- `reviews/page/5/index.html`
- `sharks-cove-snorkeling/index.html`
- `tides/hauula.html`
- `tides/kaaawa.html`
- `tides/kahana.html`
- `tides/kahuku.html`
- `tides/kailua.html`
- `tides/kaneohe-bay.html`
- `tides/kaneohe.html`
- `tides/kualoa.html`
- `tides/laie.html`
- `tides/lanikai.html`
- `tides/mokolii.html`
- `tides/mokulua-islands.html`
- `tides/punaluu.html`
- `tides/turtle-bay.html`
- `tides/waihole.html`
- `tides/waikane.html`
- `tides/waimanalo.html`
- `trip-cancellation-insurance-terms-and-conditions.html`
- `trip-cancellation-insurance-terms-and-conditions/index.html`
- `what-to-bring/index.html`
- `why-choose-active-oahu/index.html`

#### Japanese Pages (JA)
- `ja/404.html`
- `ja/about-active-oahu-tours/awards/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/index.html`
- `ja/about-active-oahu-tours/awards/active-oahu-recognized-one-top-10-hospitality-businesses-world/index.html`
- `ja/about-active-oahu-tours/index.html`
- `ja/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/index.html`
- `ja/active-oahu-photo-gallery/index.html`
- `ja/ariyoshis-summer-vacation-rainforest-kayak-tour-oahu-hawaii-2017/index.html`
- `ja/author/mbgulden/index.html`
- `ja/become-a-partner/index.html`
- `ja/cancellation-policy/index.html`
- `ja/chinamans-hat-kayak-tour/index.html`
- `ja/job-dashboard/index.html`
- `ja/job/hiring-kayak-delivery-driver-jobs-in-laie/index.html`
- `ja/join-the-team/index.html`
- `ja/kailua-oahu-storefront/index.html`
- `ja/kaneohe-bay-sandbar-kayak/index.html`
- `ja/kayak-kailua/index.html`
- `ja/privacy-policy/index.html`
- `ja/reviews/index.html`
- `ja/reviews/page/2/index.html`
- `ja/reviews/page/3/index.html`
- `ja/reviews/page/4/index.html`
- `ja/reviews/page/5/index.html`
- `ja/sharks-cove-snorkeling/index.html`
- `ja/stand-up-paddleboard-rental/index.html`
- `ja/trip-cancellation-insurance-terms-and-conditions/index.html`

### Rental Pages (Schema: `Product`)

#### English Pages (EN)
- `activities/chinamans-hat-kayak-rentals/index.html`
- `activities/kaneohe-sandbar-kayak-rentals/index.html`
- `beach-gear-rentals/index.html`
- `electric-bike-rentals/index.html`
- `kayak-rentals/index.html`
- `multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/become-a-partner/index.html`
- `multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/index.html`
- `oahu-equipment-rentals/chinamans-hat-kayak-rentals/index.html`
- `oahu-equipment-rentals/extend-the-aloha-donate-your-beach-gear-before-you-fly/index.html`
- `oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/index.html`
- `oahu-equipment-rentals/kayak-rental-delivery-locations/index.html`
- `oahu-equipment-rentals/kayak-rental-near-chinamans-hat/index.html`
- `oahu-equipment-rentals/standard-meeting-location-info/index.html`
- `rentals/cruiser-oahu-beach-equipment-rental-package/index.html`
- `rentals/explorer-oahu-kayak-rental-package/index.html`
- `rentals/kailua-beach-bike-rentals/index.html`
- `rentals/kayak-sup-trolley/index.html`
- `rentals/oahu-beach-chair-rentals/index.html`
- `rentals/oahu-beach-umbrella-rentals/index.html`
- `rentals/oahu-beginner-surf-board-rentals/index.html`
- `rentals/oahu-boogie-board-rentals/index.html`
- `rentals/oahu-cooler-rentals/index.html`
- `rentals/oahu-dry-bag-rentals/index.html`
- `rentals/oahu-kayak-anchor-rentals/index.html`
- `rentals/oahu-life-vest-rentals/index.html`
- `rentals/oahu-snorkel-mask-and-fin-rentals/index.html`
- `rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html`
- `rentals/oahu-tandem-kayak-rentals/index.html`
- `rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html`
- `rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html`

#### Japanese Pages (JA)
- `ja/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/become-a-partner/index.html`
- `ja/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/index.html`
- `ja/oahu-equipment-rentals/chinamans-hat-kayak-rentals/index.html`
- `ja/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/index.html`
- `ja/oahu-equipment-rentals/kayak-rental-delivery-locations/index.html`
- `ja/oahu-equipment-rentals/kayak-rental-near-chinamans-hat/index.html`
- `ja/rentals/kailua-beach-bike-rentals/index.html`
- `ja/rentals/kayak-sup-trolley/index.html`
- `ja/rentals/oahu-beach-chair-rentals/index.html`
- `ja/rentals/oahu-beach-umbrella-rentals/index.html`
- `ja/rentals/oahu-beginner-surf-board-rentals/index.html`
- `ja/rentals/oahu-boogie-board-rentals/index.html`
- `ja/rentals/oahu-cooler-rentals/index.html`
- `ja/rentals/oahu-dry-bag-rentals/index.html`
- `ja/rentals/oahu-kayak-anchor-rentals/index.html`
- `ja/rentals/oahu-life-vest-rentals/index.html`
- `ja/rentals/oahu-snorkel-mask-and-fin-rentals/index.html`
- `ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html`
- `ja/rentals/oahu-tandem-kayak-rentals/index.html`
- `ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html`
- `ja/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html`

### Tour Pages (Schema: `TouristTrip`)

#### English Pages (EN)
- `activities/aloha-aina-e-bike-adventure/index.html`
- `activities/chinamans-hat-kayak-complete-self-guided-tour-guide/index.html`
- `activities/chinamans-hat-oahu-kayak-tours/index.html`
- `activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
- `activities/destination-yoga/index.html`
- `activities/east-oahu-self-guided-kayaking-experience/index.html`
- `activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/index.html`
- `activities/haleiwa-paddleboarding/index.html`
- `activities/kahana-rainforest-river-oahu-kayak-tour/index.html`
- `activities/kailua-bay-mokulua-island-self-guided-kayak-tour/index.html`
- `activities/kailua-e-bike-kau-kau-guided-adventure/index.html`
- `activities/kailua-flat-island-popoia-island-guided-kayak-e-bike-adventure/index.html`
- `activities/kailua-kayak-twin-islands-guided-tour/index.html`
- `activities/kaneohe-sandbar-kayak-ultimate-guide/index.html`
- `activities/lanikai-beach-self-guided-e-bike-snorkel-adventure/index.html`
- `activities/lanikai-beach-self-guided-snorkel/index.html`
- `activities/oahu-snorkel-tour/index.html`
- `activities/oahu-surf-lessons/index.html`
- `activities/popoia-island-and-kailua-bay-guided-kayak-tour/index.html`
- `activities/rainforest-guided-hike/index.html`
- `activities/rainforest-oahu-kayak-tour.html`
- `activities/rainforest-oahu-stand-up-paddle-boarding/index.html`
- `activities/sharks-cove-self-guided-snorkel/index.html`
- `activities/west-oahu-guided-snorkel-tour/index.html`

#### Japanese Pages (JA)
- `ja/activities/aloha-aina-e-bike-adventure/index.html`
- `ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html`
- `ja/activities/east-oahu-self-guided-kayaking-experience/index.html`
- `ja/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/index.html`
- `ja/activities/haleiwa-paddleboarding/index.html`
- `ja/activities/kahana-rainforest-river-oahu-kayak-tour/index.html`
- `ja/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/index.html`
- `ja/activities/kailua-e-bike-kau-kau-guided-adventure/index.html`
- `ja/activities/kailua-flat-island-popoia-island-guided-kayak-e-bike-adventure/index.html`
- `ja/activities/kailua-kayak-twin-islands-guided-tour/index.html`
- `ja/activities/lanikai-beach-self-guided-e-bike-snorkel-adventure/index.html`
- `ja/activities/oahu-surf-lessons/index.html`
- `ja/activities/popoia-island-and-kailua-bay-guided-kayak-tour/index.html`
- `ja/activities/rainforest-oahu-stand-up-paddle-boarding/index.html`
- `ja/activities/sharks-cove-self-guided-snorkel/index.html`
- `ja/activities/west-oahu-guided-snorkel-tour/index.html`

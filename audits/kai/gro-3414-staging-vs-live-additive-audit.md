# GRO-3414 — Staging vs Live Additive-Only Audit
- Generated: 2026-07-07 21:18:24 UTC
- Production: `https://activeoahutours.com`
- Staging baseline: `https://activeoahutours2.flywheelstaging.com`
- User agent: `Kai-AOT-Staging-Live-Audit/1.0`
- Scope: route/status, title/H1, schema counts, nav-link counts, FareHarbor markers, sitemap presence, and DNS/custom-domain serving evidence from the current run.

## Executive summary
- No destructive route-level delta found in the sampled critical paths: production returns 200 for the pages checked and preserves booking/schema markers where detected.
- Sitemap URL overlap: prod=266 URLs, staging=8 URLs, stage-only sample=8, prod-only sample=80.
- `www.activeoahutours.com` was fixed in the DNS step immediately before this audit; it now redirects to apex with HTTP 301 and returns 200 after one redirect.

## Route comparison
| Path | Prod status/final | Stage status/final | Prod title / H1 | Stage title / H1 | Schema prod/stage | FH markers prod/stage |
|---|---|---|---|---:|---:|---:|
| `/` | `200` prod/ | `200` stage/ | Oahu Kayak Rentals in Kailua, Kayak to Mokulua Islands & Chi / Oahu Kayak Rentals & Tours | Oahu Kayak Rentals in Kailua, Kayak to Mokulua Islands & Chi / Oahu Kayak Rentals & Tours | 2/2 | 12/11 |
| `/contact-us/` | `200` prod/contact-us/ | `200` stage/contact-us/ | Contact Us For Questions or if you have Large Groups or Even / Contact Us | Contact Us For Questions or if you have Large Groups or Even / Contact Us | 1/0 | 2/3 |
| `/rentals/` | `200` prod/rentals/ | `200` stage/oahu-equipment-rentals/ | Oahu Kayak Rentals, SUP & Beach Gear Delivery Near Kailua / Oahu Beach Gear Rentals & Deliveries | Oahu Kayak Rentals, SUP & Beach Gear Delivery Near Kailua / Oahu Beach Gear Rentals & Deliveries | 1/0 | 7/6 |
| `/tours/` | `200` prod/tours/ | `404` stage/tours/ | Oahu Kayak Tours & Activities — Guided & Self-Guided | Activ / Oahu Kayak Tours & Activities | This Page is on an Adventure, Sorry / This page left on an adventure... | 4/0 | 10/3 |
| `/guided-tours/` | `200` prod/guided-tours/ | `404` stage/guided-tours/ | Guided Oahu Kayak Tours — Expert-Led Adventures | Active Oah / Guided Oahu Kayak Tours — Expert-Led Adv | This Page is on an Adventure, Sorry / This page left on an adventure... | 3/0 | 10/3 |
| `/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/` | `200` prod/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/ | `200` stage/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/ | Guided Mokulua Islands Kayak Tour and E-Bike Adventure in Ka / Guided Mokulua Islands Kayak Tour and E- | Guided Mokulua Islands Kayak Tour and E-Bike Adventure in Ka / Guided Mokulua Islands Kayak Tour and E- | 2/0 | 12/11 |
| `/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/` | `200` prod/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/ | `200` stage/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/ | Kailua Self-guided Kayak Tour - Kayak to Flat Island & the M / Kailua Bay & Mokulua Islands Self-Guided | Kailua Self-guided Kayak Tour - Kayak to Flat Island & the M / Kailua Bay & Mokulua Islands Self-Guided | 2/0 | 12/12 |
| `/sharks-cove-snorkeling/` | `200` prod/sharks-cove-snorkeling/ | `404` stage/sharks-cove-snorkeling/ | Sharks Cove Snorkeling — Self-Guided Oahu Snorkel Tour | Act / Sharks Cove Snorkeling — Self-Guided Oah | This Page is on an Adventure, Sorry / This page left on an adventure... | 4/0 | 12/3 |
| `/faq/` | `200` prod/faq/ | `200` stage/faq/ | Oahu Kayak & Beach Gear Rental FAQ | Active Oahu / Oahu Kayak & Beach Gear Rental FAQ | Frequently Asked Questions – Active Oahu / Frequently Asked Questions | 1/0 | 4/3 |
| `/404.html` | `200` prod/404 | `404` stage/404.html | Page Not Found — Active Oahu Tours / Active Oahu Tours & Activities | This Page is on an Adventure, Sorry / This page left on an adventure... | 0/0 | 2/3 |
| `/robots.txt` | `200` prod/robots.txt | `200` stage/?robots=1 | text/plain; charset=utf-8 /  | text/plain; charset=utf-8 /  | -/- | 0/0 |
| `/sitemap.xml` | `200` prod/sitemap.xml | `200` stage/sitemap_index.xml | application/xml /  | text/xml; charset=UTF-8 /  | -/- | 0/0 |

## Sitemap comparison
- Production sitemap URL count: `266`
- Staging sitemap URL count: `8`
- Stage-only URLs in first 80 sample: `8`
  - `http://activeoahutours2.flywheelstaging.com/activities-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/category-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/geo-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/job-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/kayakguide-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/page-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/rentals-sitemap.xml`
  - `http://activeoahutours2.flywheelstaging.com/reviews-sitemap.xml`
- Prod-only URLs in first 80 sample: `80`
  - `https://activeoahutours.com/`
  - `https://activeoahutours.com/404.html`
  - `https://activeoahutours.com/about-active-oahu-tours/`
  - `https://activeoahutours.com/about-active-oahu-tours/awards/`
  - `https://activeoahutours.com/about-active-oahu-tours/awards/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/`
  - `https://activeoahutours.com/about-active-oahu-tours/awards/active-oahu-recognized-one-top-10-hospitality-businesses-world/`
  - `https://activeoahutours.com/about-active-oahu/`
  - `https://activeoahutours.com/active-aloha-ambassador/`
  - `https://activeoahutours.com/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/`
  - `https://activeoahutours.com/active-oahu-photo-gallery/`
  - `https://activeoahutours.com/activities.html`
  - `https://activeoahutours.com/activities/`
  - `https://activeoahutours.com/activities/aloha-aina-e-bike-adventure/`
  - `https://activeoahutours.com/activities/chinamans-hat-kayak-complete-self-guided-tour-guide/`
  - `https://activeoahutours.com/activities/chinamans-hat-kayak-rentals/`
  - `https://activeoahutours.com/activities/chinamans-hat-oahu-kayak-tours/`
  - `https://activeoahutours.com/activities/chinamans-hat-self-guided-oahu-kayak-tour/`
  - `https://activeoahutours.com/activities/destination-yoga/`
  - `https://activeoahutours.com/activities/east-oahu-self-guided-kayaking-experience/`
  - `https://activeoahutours.com/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/`
  - `https://activeoahutours.com/activities/haleiwa-paddleboarding/`
  - `https://activeoahutours.com/activities/kahana-rainforest-river-oahu-kayak-tour/`
  - `https://activeoahutours.com/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/`
  - `https://activeoahutours.com/activities/kailua-e-bike-kau-kau-guided-adventure/`
  - `https://activeoahutours.com/activities/kailua-flat-island-popoia-island-guided-kayak-e-bike-adventure/`

## Booking / FareHarbor spot checks
- `/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=091a25cd-93e6-4bf0-bad5-d305c6dbb1ea&from-ssl=yes&ga4t=AW-11496137384%2Cundefined__undefined%3B&g4=yes&cp=no&csp=no&back=https%3A%2F%2Factiveoahutours.com%2F&language=en-us', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?u=091a25cd-93e6-4bf0-bad5-d305c6dbb1ea&from-ssl=yes&ga4t=AW-11496137384%2Cundefined__undefined%3B&g4=yes&cp=no&csp=no&back=https%3A%2F%2Factiveoahutours.com%2F&language=en-us', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=091a25cd-93e6-4bf0-bad5-d305c6dbb1ea&from-ssl=yes&ga4t=AW-11496137384%2Cundefined__undefined%3B&g4=yes&cp=no&csp=no&back=https%3A%2F%2Factiveoahutours2.flywheelstaging.com%2F&language=en-us', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?u=091a25cd-93e6-4bf0-bad5-d305c6dbb1ea&from-ssl=yes&ga4t=AW-11496137384%2Cundefined__undefined%3B&g4=yes&cp=no&csp=no&back=https%3A%2F%2Factiveoahutours2.flywheelstaging.com%2F&language=en-us', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/contact-us/`
  - prod: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/rentals/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?flow=728039', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=728039', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes', 'src=https://fareharbor.com/embeds/script/calendar/activeoahutours/?fallback=simple&flow=728039']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?flow=728039', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=728039', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes', 'src=https://fareharbor.com/embeds/script/calendar/activeoahutours/?fallback=simple&flow=728039']`
- `/tours/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/guided-tours/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1128101', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/526154/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1128101', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/526154/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1128101', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/526154/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1128101', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/526154/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'href=https://fareharbor.com/embeds/book/activeoahutours/?selected-items=491544%2C491545', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/516089/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'https://fareharbor.com/embeds/book/activeoahutours/?selected-items=491544%2C491545', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/516089/calendar/']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'href=https://fareharbor.com/embeds/book/activeoahutours/?selected-items=491544%2C491545', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/516089/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?flow=1038571', 'https://fareharbor.com/embeds/book/activeoahutours/?selected-items=491544%2C491545', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/516089/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/']`
- `/sharks-cove-snorkeling/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/7872/', 'href=https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/items/115595/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/521252/calendar/', 'https://fareharbor.com/embeds/book/activeoahutours/items/7872/', 'https://fareharbor.com/embeds/book/activeoahutours/items/8522/calendar/', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/faq/`
  - prod: `['href=https://fareharbor.com', 'href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`
- `/404.html`
  - prod: `['href=https://fareharbor.com/embeds/book/activeoahutours/', 'https://fareharbor.com/embeds/book/activeoahutours/']`
  - stage: `['href=https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes', 'src=https://fareharbor.com/embeds/api/v1/?autolightframe=yes']`

## Fact-check gates
- This audit did not change visitor-facing content, prices, durations, safety claims, route advice, or Hawaiian-language copy.
- Named facts checked are operational/site facts only: production/staging URLs, HTTP statuses, sitemap counts, schema counts, and FareHarbor marker presence from live fetches.

## Image/GPS verification
- Not applicable: no imagery was selected, copied, edited, placed, or described as factual page imagery.

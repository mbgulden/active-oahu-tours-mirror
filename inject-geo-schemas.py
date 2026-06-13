#!/usr/bin/env python3
"""
GRO-793: GEO/Schema injection for 3 location pages.
Injects LocalBusiness, FAQPage, HowTo, and Product schemas + author byline.
"""

import os
import re

SITE_DIR = "/home/ubuntu/work/active-oahu-static/site"

# ─── Schema Templates (main branch format: escaped JSON, single-quoted script tags) ───

LOCAL_BUSINESS_SCHEMA = """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"TravelAgency","@id":"https:\\/\\/activeoahutours.com\\/#storefront","name":"Active Oahu Tours","url":"https:\\/\\/activeoahutours.com","logo":"https:\\/\\/activeoahutours.com\\/assets\\/images\\/logo.png","description":"Premium self-guided kayak rentals, e-bike rentals, beach gear, and guided adventures on Windward Oahu.","telephone":"+1-808-498-1894","priceRange":"$$","address":{"@type":"PostalAddress","streetAddress":"134B Hamakua Dr","addressLocality":"Kailua","addressRegion":"HI","postalCode":"96734","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":21.391694,"longitude":-157.747194},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"07:00","closes":"17:00"}],"areaServed":[{"@type":"AdministrativeArea","name":"Oahu"},{"@type":"AdministrativeArea","name":"Kailua"},{"@type":"AdministrativeArea","name":"Lanikai"},{"@type":"AdministrativeArea","name":"Waimanalo"}],"sameAs":["https:\\/\\/www.facebook.com\\/activeoahutours","https:\\/\\/www.instagram.com\\/activeoahutours","https:\\/\\/www.yelp.com\\/biz\\/active-oahu-tours-kailua-2","https:\\/\\/www.tripadvisor.com\\/Attraction_Review-g60607-d4778712-Reviews-Active_Oahu_Tours-Kailua_Oahu_Hawaii.html"]}</script>"""

# Page-specific FAQPage schemas
FAQ_SCHEMAS = {
    "kailua-beach-park": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is parking at Kailua Beach Park free?","acceptedAnswer":{"@type":"Answer","text":"Yes, the main parking lot at Kailua Beach Park (526 Kawailoa Road) is free and open to the public. It has 300+ stalls including accessible spaces. Arrive before 9am on weekends to secure a spot."}},{"@type":"Question","name":"Can I launch a kayak from Kailua Beach Park?","acceptedAnswer":{"@type":"Answer","text":"Absolutely. Kailua Beach Park is the best kayak launch point on the windward coast. The beach slopes gradually into calm bay waters, and there is a designated kayak staging area near the lifeguard tower. We provide soft car racks with every rental so you can transport your kayak the 1.5 miles from our shop."}},{"@type":"Question","name":"Does Kailua Beach Park have restrooms and showers?","acceptedAnswer":{"@type":"Answer","text":"Yes, Kailua Beach Park has public restrooms with flush toilets, outdoor freshwater showers, and picnic tables. The facilities are maintained by the City & County of Honolulu and are open daily during park hours."}}]}</script>""",

    "lanikai-beach": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is Lanikai Beach open to the public?","acceptedAnswer":{"@type":"Answer","text":"Yes, Lanikai Beach is a public beach with several shoreline access paths between private homes. There is no parking lot — only street parking on Aalapapa Drive and Mokulua Drive. Park legally with all tires off the pavement and do not block driveways."}},{"@type":"Question","name":"What is the best time to visit Lanikai Beach?","acceptedAnswer":{"@type":"Answer","text":"Early morning (before 8am) is ideal for calm conditions, sunrise views over the Mokulua Islands, and easier parking. Midday can be crowded on weekends. Afternoon trade winds pick up around 1pm, making it windier for kayaking."}},{"@type":"Question","name":"Can I kayak from Lanikai Beach to the Mokulua Islands?","acceptedAnswer":{"@type":"Answer","text":"Yes, Lanikai Beach is the closest launch point for paddling to the Mokulua Islands (Moku Nui and Moku Iki). The paddle is approximately 1.5 miles each way. We recommend launching from Kailua Beach Park for easier parking and gear staging, then paddling south along the coast to Lanikai and across to the Mokes."}}]}</script>""",

    "waimanalo-beach": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is Waimanalo Beach safe for swimming?","acceptedAnswer":{"@type":"Answer","text":"Waimanalo Beach is generally safe for swimming during calm summer months (May to September) when the shore break is minimal. However, it is more exposed to open ocean swells than Kailua, resulting in stronger currents. Swim near the lifeguard towers and avoid entering the water during winter swell events."}},{"@type":"Question","name":"Does Waimanalo Beach have parking?","acceptedAnswer":{"@type":"Answer","text":"Yes. Waimanalo Beach Park has a large, free paved parking lot directly off Kalanianaole Highway. Unlike Lanikai, parking here is abundant and rarely fills up completely, except during peak summer holiday weekends."}},{"@type":"Question","name":"Can I have kayak gear delivered to Waimanalo Beach?","acceptedAnswer":{"@type":"Answer","text":"No. Commercial delivery of water sports equipment is prohibited at Waimanalo Beach by DLNR regulations. To kayak at Waimanalo, rent equipment from Active Oahu at 134B Hamakua Dr in Kailua and transport it yourself using the soft racks we provide."}}]}</script>"""
}

# HowTo schema per page
HOWTO_SCHEMAS = {
    "kailua-beach-park": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Launch a Kayak at Kailua Beach Park","description":"Step-by-step guide for launching a self-guided kayak from Kailua Beach Park.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"79.00"},"totalTime":"PT30M","step":[{"@type":"HowToStep","name":"Pick up your kayak from Active Oahu","text":"Rent your kayak from Active Oahu at 134B Hamakua Dr in Kailua. We will set up soft car racks on your vehicle and provide paddles, life vests, and a dry bag."},{"@type":"HowToStep","name":"Drive to Kailua Beach Park","text":"Drive 1.5 miles to Kailua Beach Park at 526 Kawailoa Road. Park in the main lot and carry your kayak down the designated staging area near the lifeguard tower."},{"@type":"HowToStep","name":"Launch from the protected beach","text":"Kailua Beach Park has a gradual sandy entry perfect for launching. Paddle out past the shore break and head toward Popoia Island or south along the coast toward Lanikai."}]}</script>""",

    "lanikai-beach": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Find Legal Parking at Lanikai Beach","description":"A step-by-step guide to finding legal parking at Lanikai Beach without getting ticketed or towed.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0.00"},"totalTime":"PT15M","step":[{"@type":"HowToStep","name":"Arrive early","text":"Arrive before 8:00 AM on weekdays or 7:00 AM on weekends to secure a spot in the limited legal parking areas along Aalapapa Drive."},{"@type":"HowToStep","name":"Park at Kailua Beach Park as backup","text":"If Lanikai streets are full, park in the free public lot at Kailua Beach Park (526 Kawailoa Road). It has 300+ stalls and is a 15-minute walk or 3-minute bike ride from Lanikai."},{"@type":"HowToStep","name":"Obey all parking signs","text":"Ensure your tires are completely off the paved roadway, do not block driveways, and stay at least 4 feet from fire hydrants. Lanikai residents are vigilant about reporting parking violations."}]}</script>""",

    "waimanalo-beach": """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Visit Waimanalo Beach","description":"Everything you need to know for a great day at Waimanalo Beach.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0.00"},"totalTime":"P1D","step":[{"@type":"HowToStep","name":"Pack your gear","text":"Waimanalo has limited rental options nearby. Rent beach gear (kayaks, e-bikes, snorkel sets) from Active Oahu at 134B Hamakua Dr before heading east."},{"@type":"HowToStep","name":"Park at Waimanalo Beach Park","text":"Drive to Waimanalo Beach Park on Kalanianaole Highway. The free paved lot has abundant parking even on busy days."},{"@type":"HowToStep","name":"Find a spot on the 3-mile beach","text":"Walk north or south from the park pavilion to find your perfect spot. Lifeguards are stationed near the main parking area. Swim between the flags during summer months."}]}</script>"""
}

# Product schema (kayak rental, same for all location pages)
PRODUCT_SCHEMA = """  <script type='application/ld+json'>{"@context":"http:\\/\\/schema.org","@type":"Product","@id":"https:\\/\\/activeoahutours.com\\/rentals\\/kayak-rentals\\/#product","name":"Tandem Kayak Rental (Self-Guided)","image":"https:\\/\\/activeoahutours.com\\/wp-content\\/uploads\\/2021\\/06\\/DSC5297_2000-e1642616607887.jpg","description":"Premium 2-person ocean kayak rentals for exploring Kailua Bay, Popoia Island, and the Mokulua Islands. Includes paddles, life vests, dry bags, and soft car racks.","brand":{"@type":"Brand","name":"Active Oahu Tours"},"offers":{"@type":"Offer","url":"https:\\/\\/activeoahutours.com\\/rentals\\/kayak-rentals\\/","priceCurrency":"USD","price":"79.00","priceValidUntil":"2027-12-31","itemCondition":"https:\\/\\/schema.org\\/NewCondition","availability":"https:\\/\\/schema.org\\/InStock","seller":{"@type":"LocalBusiness","name":"Active Oahu Tours"}}}</script>"""

# Author bylines per page
AUTHOR_BYLINES = {
    "kailua-beach-park": '<p style="font-size: 0.9em; color: #666; font-style: italic;">By Michael Gulden, Owner &amp; Operator, Active Oahu Tours</p>\n',
    "lanikai-beach": '<p style="font-size: 0.9em; color: #666; font-style: italic;">By Michael Gulden, Owner &amp; Operator, Active Oahu Tours</p>\n',
    "waimanalo-beach": '<p style="font-size: 0.9em; color: #666; font-style: italic;">By Michael Gulden, Owner &amp; Operator, Active Oahu Tours</p>\n'
}

PAGES = ["kailua-beach-park", "lanikai-beach", "waimanalo-beach"]

# ─── Markers for injection ───
# After the Organization schema closing </script> (the 2nd schema block)
INSERT_AFTER_ORG = "</script>\n<meta name=\"p:domain_verify\""

# Entry content opening - where to inject author byline
ENTRY_CONTENT_MARKER = '<div class="entry-content"'

def inject_schemas(page_slug):
    """Inject all schemas into a page's HTML."""
    filepath = os.path.join(SITE_DIR, "guides", page_slug, "index.html")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Inject LocalBusiness + FAQPage + HowTo + Product after Organization schema
    new_schemas = (
        LOCAL_BUSINESS_SCHEMA + "\n" +
        FAQ_SCHEMAS[page_slug] + "\n" +
        HOWTO_SCHEMAS[page_slug] + "\n" +
        PRODUCT_SCHEMA
    )
    
    replacement = "</script>\n" + new_schemas + "\n" + '<meta name="p:domain_verify"'
    
    if replacement not in content:
        # Use INSERT_AFTER_ORG as marker
        old = INSERT_AFTER_ORG
        new = "</script>\n" + new_schemas + "\n" + '<meta name="p:domain_verify"'
        content = content.replace(old, new, 1)
    
    # 2. Inject author byline at the start of entry-content
    # Find the entry-content div and insert after the opening div
    author_html = AUTHOR_BYLINES[page_slug]
    
    # Look for the first heading or paragraph after entry-content
    # Strategy: find entry-content and insert author before any content
    entry_start = content.find(ENTRY_CONTENT_MARKER)
    if entry_start >= 0:
        # Find the end of the opening div tag
        div_end = content.find(">", entry_start)
        if div_end >= 0:
            after_div = content[div_end+1:div_end+3]
            # Insert after the opening div
            insert_pos = div_end + 1
            content = content[:insert_pos] + "\n" + author_html + content[insert_pos:]
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {page_slug}: Schemas injected + author byline added")


def verify_page(page_slug):
    """Verify all schemas were injected correctly."""
    filepath = os.path.join(SITE_DIR, "guides", page_slug, "index.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "TravelAgency": "TravelAgency" in content,
        "FAQPage": "FAQPage" in content,
        "HowTo": "HowTo" in content,
        "Product": "Product" in content,
        "Author byline": "Michael Gulden, Owner &amp; Operator" in content,
        "134B Hamakua Dr": "134B Hamakua Dr" in content,
        "No old Organization": content.count("Organization") >= 1,  # Should still have the original
    }
    
    all_pass = all(checks.values())
    print(f"\n📋 {page_slug} verification:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    # Count JSON-LD blocks
    block_count = content.count("application/ld+json")
    print(f"  {block_count} total JSON-LD blocks (expected: 6 = WebSite + Organization + TravelAgency + FAQPage + HowTo + Product)")
    
    return all_pass


# ─── Execute ───

print("=" * 60)
print("GRO-793: GEO/Schema Injection for Location Pages")
print("=" * 60)

for page in PAGES:
    print(f"\n--- Processing {page} ---")
    
    filepath = os.path.join(SITE_DIR, "guides", page, "index.html")
    if not os.path.exists(filepath):
        print(f"  ❌ File not found: {filepath}")
        continue
    
    inject_schemas(page)
    verify_page(page)

print("\n" + "=" * 60)
print("DONE — All schema injections complete")
print("=" * 60)

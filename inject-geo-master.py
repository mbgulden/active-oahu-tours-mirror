#!/usr/bin/env python3
"""
GRO-793: Master branch-specific schema injection.
Master uses content-first meta format, double-quoted script types.
"""
import os, re

SITE_DIR = "/home/ubuntu/work/active-oahu-static/site"
PAGES = ["kailua-beach-park", "lanikai-beach", "waimanalo-beach"]

# Master branch format: double-quoted script type, content-first meta
LOCAL_BUSINESS = """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"TravelAgency","@id":"https:\\/\\/activeoahutours.com\\/#storefront","name":"Active Oahu Tours","url":"https:\\/\\/activeoahutours.com","logo":"https:\\/\\/activeoahutours.com\\/assets\\/images\\/logo.png","description":"Premium self-guided kayak rentals and guided adventures on Windward Oahu.","telephone":"+1-808-498-1894","priceRange":"$$","address":{"@type":"PostalAddress","streetAddress":"134B Hamakua Dr","addressLocality":"Kailua","addressRegion":"HI","postalCode":"96734","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":21.391694,"longitude":-157.747194},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"07:00","closes":"17:00"}],"areaServed":[{"@type":"AdministrativeArea","name":"Oahu"},{"@type":"AdministrativeArea","name":"Kailua"},{"@type":"AdministrativeArea","name":"Lanikai"},{"@type":"AdministrativeArea","name":"Waimanalo"}],"sameAs":["https:\\/\\/www.facebook.com\\/activeoahutours","https:\\/\\/www.instagram.com\\/activeoahutours","https:\\/\\/www.yelp.com\\/biz\\/active-oahu-tours-kailua-2","https:\\/\\/www.tripadvisor.com\\/Attraction_Review-g60607-d4778712-Reviews-Active_Oahu_Tours-Kailua_Oahu_Hawaii.html"]}</script>"""

FAQ_SCHEMAS = {
    "kailua-beach-park": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is parking at Kailua Beach Park free?","acceptedAnswer":{"@type":"Answer","text":"Yes, the main parking lot at Kailua Beach Park (526 Kawailoa Road) is free and open to the public. It has 300+ stalls including accessible spaces."}},{"@type":"Question","name":"Can I launch a kayak from Kailua Beach Park?","acceptedAnswer":{"@type":"Answer","text":"Absolutely. Kailua Beach Park has a gradual sandy entry perfect for launching kayaks. We provide soft car racks with every rental so you can transport your kayak 1.5 miles from our shop."}},{"@type":"Question","name":"Does Kailua Beach Park have restrooms?","acceptedAnswer":{"@type":"Answer","text":"Yes, Kailua Beach Park has public restrooms with flush toilets, outdoor freshwater showers, and picnic tables. Open daily during park hours."}}]}</script>""",
    "lanikai-beach": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is Lanikai Beach open to the public?","acceptedAnswer":{"@type":"Answer","text":"Yes, Lanikai Beach is a public beach with shoreline access paths between private homes. There is no parking lot — only street parking. Park legally with all tires off the pavement."}},{"@type":"Question","name":"What is the best time to visit Lanikai Beach?","acceptedAnswer":{"@type":"Answer","text":"Early morning (before 8am) is ideal for calm conditions, sunrise over the Mokulua Islands, and easier parking. Afternoon trade winds pick up around 1pm."}},{"@type":"Question","name":"Can I kayak from Lanikai Beach?","acceptedAnswer":{"@type":"Answer","text":"Yes, Lanikai Beach is the closest launch point for paddling to the Mokulua Islands, approximately 1.5 miles each way."}}]}</script>""",
    "waimanalo-beach": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is Waimanalo Beach safe for swimming?","acceptedAnswer":{"@type":"Answer","text":"Waimanalo Beach is generally safe during calm summer months (May to September). It is more exposed to open ocean swells than Kailua. Swim near the lifeguard towers."}},{"@type":"Question","name":"Does Waimanalo Beach have parking?","acceptedAnswer":{"@type":"Answer","text":"Yes, Waimanalo Beach Park has a large, free paved parking lot directly off Kalanianaole Highway. Parking is abundant and rarely fills up."}},{"@type":"Question","name":"Can I get kayak delivery to Waimanalo Beach?","acceptedAnswer":{"@type":"Answer","text":"No. Commercial delivery is prohibited at Waimanalo Beach by DLNR regulations. Rent equipment from Active Oahu at 134B Hamakua Dr in Kailua and transport it yourself."}}]}</script>"""
}

HOWTO_SCHEMAS = {
    "kailua-beach-park": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Launch a Kayak at Kailua Beach Park","description":"Step-by-step guide for self-guided kayak launch.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"79.00"},"totalTime":"PT30M","step":[{"@type":"HowToStep","name":"Pick up your kayak from Active Oahu","text":"Rent from Active Oahu at 134B Hamakua Dr. We set up soft car racks on your vehicle."},{"@type":"HowToStep","name":"Drive to Kailua Beach Park","text":"Drive 1.5 miles to 526 Kawailoa Road. Park in the main lot by the lifeguard tower."},{"@type":"HowToStep","name":"Launch from the protected beach","text":"Kailua Beach Park has a gradual sandy entry. Paddle out toward Popoia Island or south along the coast."}]}</script>""",
    "lanikai-beach": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Find Legal Parking at Lanikai Beach","description":"Avoid tickets and towing with this guide.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0.00"},"totalTime":"PT15M","step":[{"@type":"HowToStep","name":"Arrive early","text":"Arrive before 8am on weekdays or 7am on weekends for the limited street parking."},{"@type":"HowToStep","name":"Use Kailua Beach Park as backup","text":"If Lanikai streets are full, park at Kailua Beach Park (526 Kawailoa Road) — 300+ stalls, 15-min walk away."},{"@type":"HowToStep","name":"Obey all parking signs","text":"Keep tires off pavement, do not block driveways, stay 4ft from hydrants."}]}</script>""",
    "waimanalo-beach": """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"HowTo","name":"How to Visit Waimanalo Beach","description":"Everything you need for a great beach day.","estimatedCost":{"@type":"MonetaryAmount","currency":"USD","value":"0.00"},"totalTime":"P1D","step":[{"@type":"HowToStep","name":"Pack your gear","text":"Rent gear from Active Oahu at 134B Hamakua Dr before heading east."},{"@type":"HowToStep","name":"Park at Waimanalo Beach Park","text":"Drive to Waimanalo Beach Park on Kalanianaole Highway. Free paved lot."},{"@type":"HowToStep","name":"Find your spot","text":"Walk north or south from the park pavilion. Lifeguards near main area."}]}</script>"""
}

PRODUCT = """  <script type="application/ld+json">{"@context":"http:\\/\\/schema.org","@type":"Product","@id":"https:\\/\\/activeoahutours.com\\/rentals\\/kayak-rentals\\/#product","name":"Tandem Kayak Rental (Self-Guided)","description":"Premium 2-person ocean kayak rentals. Includes paddles, life vests, dry bags, soft car racks.","brand":{"@type":"Brand","name":"Active Oahu Tours"},"offers":{"@type":"Offer","url":"https:\\/\\/activeoahutours.com\\/rentals\\/kayak-rentals\\/","priceCurrency":"USD","price":"79.00","priceValidUntil":"2027-12-31","itemCondition":"https:\\/\\/schema.org\\/NewCondition","availability":"https:\\/\\/schema.org\\/InStock","seller":{"@type":"LocalBusiness","name":"Active Oahu Tours"}}}</script>"""

AUTHOR = '<p style="font-size:0.9em;color:#666;font-style:italic;">By Michael Gulden, Owner &amp; Operator, Active Oahu Tours</p>\n'

# Master branch marker: content-first meta format
INSERT_MARKER = '</script>\n<meta content="93780a0eca896a61df488e87781da6c8"'

for page in PAGES:
    fp = os.path.join(SITE_DIR, "guides", page, "index.html")
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject 4 schema blocks after Organization
    new_blocks = LOCAL_BUSINESS + "\n" + FAQ_SCHEMAS[page] + "\n" + HOWTO_SCHEMAS[page] + "\n" + PRODUCT
    old = '</script>\n<meta content="93780a0eca896a61df488e87781da6c8"'
    new = '</script>\n' + new_blocks + '\n<meta content="93780a0eca896a61df488e87781da6c8"'
    content = content.replace(old, new, 1)
    
    # Inject author byline
    entry = '<div class="entry-content"'
    idx = content.find(entry)
    if idx >= 0:
        close = content.find(">", idx)
        content = content[:close+1] + "\n" + AUTHOR + content[close+1:]
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Verify
    blocks = content.count("application/ld+json")
    has_agency = "TravelAgency" in content
    has_faq = "FAQPage" in content
    has_howto = "HowTo" in content
    has_product = "Product" in content
    has_author = "Michael Gulden, Owner &amp; Operator" in content
    
    print(f"{page}: {blocks} blocks, Agency={has_agency}, FAQ={has_faq}, HowTo={has_howto}, Product={has_product}, Author={has_author}")
    
print("Master branch: Complete")

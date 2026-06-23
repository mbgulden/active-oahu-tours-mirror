#!/usr/bin/env python3
"""Generate 8 unified tour pages with WordPress template + TouristTrip schema."""
import os, json, re

SITE = "/home/ubuntu/work/active-oahu-tours-mirror/site"

# Read templates
with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()

# 8 pages
pages = [
    {
        "slug": "sharks-cove-snorkeling",
        "title": "Sharks Cove Snorkeling \u2014 Self-Guided Oahu Snorkel Tour | Active Oahu",
        "description": "Snorkel Sharks Cove on Oahu\u2019s North Shore \u2014 world-class snorkeling with rental gear delivery. Self-guided tour with directions, tips, and FAQ.",
        "h1": "Sharks Cove Snorkeling \u2014 Self-Guided Oahu Adventure",
        "tourist_type": "Self-Guided",
        "body": '<h2>Why Sharks Cove Is Oahu\u2019s Best Snorkeling</h2>\n<p>Sharks Cove, on Oahu\u2019s legendary North Shore, is consistently rated one of the <strong>top 12 shore dives in the world</strong> by Scuba Diving Magazine. During summer (May\u2013October), the water flattens to glass, revealing a protected marine ecosystem with over 100 species of tropical fish, sea turtles, and vibrant coral.</p>\n<p>Active Oahu provides everything you need: premium snorkel gear delivered to the cove, parking directions, tide charts, and a self-guided route map.</p>\n\n<h2>What You\u2019ll See</h2>\n<ul>\n<li><strong>Honu (Green Sea Turtles):</strong> Frequent visitors feeding on algae along the rocky edges</li>\n<li><strong>Humuhumunukunuku\u0101pua\u02bba:</strong> Hawaii\u2019s state fish, common in the shallows</li>\n<li><strong>Parrotfish, Butterflyfish, Tangs:</strong> The cove is an aquarium in summer</li>\n</ul>\n\n<h2>Self-Guided Sharks Cove Itinerary</h2>\n<p><strong>Best time:</strong> 8:00 AM \u2013 11:00 AM (arrive early for parking and calmest water)</p>\n<p><strong>Duration:</strong> 2\u20133 hours in the water</p>\n<p><strong>Skill level:</strong> Beginner to intermediate (summer only \u2014 winter brings 20+ ft waves)</p>\n\n<p><strong>Did you know?</strong> Sharks Cove got its name from its shape \u2014 not from shark sightings. When viewed from above, the cove\u2019s outline resembles a shark.</p>'
    },
    {
        "slug": "kayak-kailua",
        "title": "Kailua Kayak Rentals \u2014 Self-Guided Mokulua Islands Tour | Active Oahu",
        "description": "Kayak to the Mokulua Islands from Kailua Beach. Self-guided tour with rental gear, route map, and tips from Oahu\u2019s top-rated kayak outfitter.",
        "h1": "Kailua Kayaking \u2014 Self-Guided Mokulua Islands Tour",
        "tourist_type": "Self-Guided",
        "body": '<h2>Paddle to the Mokulua Islands \u2014 Oahu\u2019s Iconic Kayak Trip</h2>\n<p>The <strong>Mokulua Islands</strong> (\u201cThe Mokes\u201d) are the twin islets visible from Kailua Beach \u2014 paddling to them is the most iconic kayak experience on Oahu. Active Oahu provides everything: kayak, life vest, paddle, dry bag, and a detailed route map.</p>\n<p>This is a <strong>self-guided tour</strong> \u2014 you set the pace. The paddle is ~1 mile each way across protected Kailua Bay.</p>\n\n<h2>The Route</h2>\n<ul>\n<li><strong>Launch:</strong> Kailua Beach Park boat ramp (closest to the Mokes)</li>\n<li><strong>Paddle out:</strong> 30\u201345 minutes depending on wind</li>\n<li><strong>Landing:</strong> Moku Nui\u2019s protected south-facing beach</li>\n<li><strong>Explore:</strong> Tide pools, Queens Bath natural pool, seabird sanctuary views</li>\n</ul>\n\n<h2>What\u2019s Included</h2>\n<ul>\n<li>Sit-on-top ocean kayak (single or tandem)</li>\n<li>Life vest (USCG approved)</li>\n<li>Paddle with leash</li>\n<li>Dry bag for phone/keys</li>\n<li><strong>Bonus:</strong> Snorkel gear add-on available</li>\n</ul>\n\n<p><strong>Pro tip:</strong> Go early (7\u20138 AM launch). The tradewinds pick up by 11 AM. About 65,000 people kayak to the Mokes annually \u2014 the earlier you go, the more you\u2019ll have it to yourself.</p>'
    },
    {
        "slug": "chinamans-hat",
        "title": "Chinaman\u2019s Hat Kayak \u2014 Self-Guided Mokoli\u02bbi Island Tour | Active Oahu",
        "description": "Kayak to Mokoli\u02bbi Island (Chinaman\u2019s Hat) from Kualoa Regional Park. Self-guided tour with kayak rental delivery, tide guide, and hiking tips.",
        "h1": "Chinaman\u2019s Hat Kayak \u2014 Self-Guided Mokoli\u02bbi Island Tour",
        "tourist_type": "Self-Guided",
        "body": '<h2>Kayak to Oahu\u2019s Most Recognizable Island \u2014 Mokoli\u02bbi</h2>\n<p><strong>Mokoli\u02bbi</strong> (Chinaman\u2019s Hat) is the iconic cone-shaped island off Kualoa Regional Park. The paddle is one of Oahu\u2019s <strong>shortest and most rewarding kayak trips</strong> \u2014 just 500 yards across a shallow reef shelf.</p>\n<p>Active Oahu delivers your kayak to Kualoa Beach Park. Land on the island\u2019s small beach, then hike to the summit for <strong>360\u00b0 views of K\u0101ne\u02bbohe Bay, the Ko\u02bbolau Mountains, and Kualoa Ranch</strong>.</p>\n\n<h2>Quick Facts</h2>\n<ul>\n<li><strong>Paddle distance:</strong> ~500 yards one way</li>\n<li><strong>Time:</strong> 10\u201320 minutes each way</li>\n<li><strong>Best launch:</strong> Kualoa Regional Park (near the palm trees)</li>\n<li><strong>Hike to summit:</strong> ~15 minutes, steep and rocky \u2014 wear shoes!</li>\n</ul>\n\n<p><strong>Safety note:</strong> The water between Kualoa and Mokoli\u02bbi is shallow reef \u2014 never deeper than waist-deep at high tide. One of the safest ocean kayak trips on Oahu.</p>'
    },
    {
        "slug": "kaneohe-sandbar",
        "title": "Kaneohe Sandbar Kayak \u2014 Self-Guided Adventure | Active Oahu",
        "description": "Kayak to the famous Kaneohe Sandbar (Ahu o Laka). Self-guided tour with kayak rental delivery, tide chart, and tips for Oahu\u2019s floating beach party.",
        "h1": "Kaneohe Sandbar \u2014 Self-Guided Kayak Adventure",
        "tourist_type": "Self-Guided",
        "body": '<h2>Paddle to Oahu\u2019s Floating Beach \u2014 The Kaneohe Sandbar</h2>\n<p>The <strong>Kaneohe Sandbar</strong> (Ahu o Laka) is a sunken reef that emerges at low tide to create a <strong>beach in the middle of Kaneohe Bay</strong>. At high tide, the water is waist-deep; at low tide, the sand is fully exposed, surrounded by turquoise water.</p>\n<p>Active Oahu delivers your kayak to He\u02bbeia Kea Pier \u2014 the closest launch point. It\u2019s a <strong>1.5-mile paddle</strong> across protected Kaneohe Bay.</p>\n\n<h2>The Experience</h2>\n<ul>\n<li><strong>Paddle out:</strong> ~45 minutes across calm, protected bay water</li>\n<li><strong>Anchor up:</strong> Kayak anchor included</li>\n<li><strong>Hang out:</strong> Wading, snorkeling, volleyball \u2014 Hawaii\u2019s natural water park</li>\n</ul>\n\n<h2>Tide Tips</h2>\n<ul>\n<li><strong>Low tide:</strong> Full sand exposure \u2014 walk around, set up chairs</li>\n<li><strong>Mid tide:</strong> Waist-deep water \u2014 perfect for wading and floating</li>\n<li><strong>High tide:</strong> Sandbar submerges \u2014 plan for low-to-mid tide window</li>\n</ul>\n\n<p><strong>Did you know?</strong> Kaneohe Bay is the largest sheltered body of water in Hawaii, protected by Oahu\u2019s only barrier reef.</p>'
    },
    {
        "slug": "self-guided",
        "title": "Self-Guided Oahu Kayak Tours \u2014 Rentals & Route Maps | Active Oahu",
        "description": "Explore Oahu at your own pace with self-guided kayak tours. Kayak rental delivery, route maps, and support from Oahu\u2019s top-rated outfitter.",
        "h1": "Self-Guided Oahu Kayak & Snorkel Tours",
        "tourist_type": "Self-Guided",
        "body": '<h2>Explore Oahu on Your Terms</h2>\n<p>Active Oahu\u2019s <strong>self-guided tours</strong> give you the freedom to explore Hawaii\u2019s best water destinations at your own pace. We deliver premium gear, provide detailed route maps and tide guides, and handle logistics \u2014 you just show up and paddle.</p>\n\n<h2>Available Self-Guided Tours</h2>\n\n<h3>Mokulua Islands (Kailua)</h3>\n<p>Paddle 1 mile across Kailua Bay to the twin Mokes. Land on Moku Nui, explore tide pools, hike to Queens Bath. <strong>2\u20134 hours.</strong></p>\n\n<h3>Chinaman\u2019s Hat (Mokoli\u02bbi)</h3>\n<p>500 yards to Oahu\u2019s most photographed islet. Hike to the summit for 360\u00b0 views. <strong>1\u20132 hours.</strong></p>\n\n<h3>Kaneohe Sandbar</h3>\n<p>Paddle 1.5 miles to Oahu\u2019s floating beach. <strong>3\u20134 hours.</strong></p>\n\n<h3>Sharks Cove Snorkeling</h3>\n<p>World-class snorkeling on the North Shore. <strong>2\u20133 hours.</strong></p>\n\n<h2>Why Self-Guided?</h2>\n<ul>\n<li><strong>Your schedule:</strong> No group to wait for \u2014 launch when you want</li>\n<li><strong>Your pace:</strong> Linger at the good spots</li>\n<li><strong>Lower cost:</strong> Self-guided is ~40% less than guided tours</li>\n<li><strong>Full support:</strong> Route maps, tide charts, emergency contact included</li>\n</ul>\n\n<p>Every self-guided rental includes a <strong>waterproof route map</strong> with GPS coordinates, landing tips, hazard zones, and our direct phone number. You\u2019re independent \u2014 not alone.</p>'
    },
    {
        "slug": "guided-tours",
        "title": "Guided Oahu Kayak Tours \u2014 Expert-Led Adventures | Active Oahu",
        "description": "Join an expert-guided kayak tour on Oahu. Professional guides lead small groups to the Mokulua Islands, Kaneohe Sandbar, and Kailua Bay.",
        "h1": "Guided Oahu Kayak Tours \u2014 Expert-Led Adventures",
        "tourist_type": "Guided",
        "body": '<h2>Go Deeper with a Local Guide</h2>\n<p>Active Oahu\u2019s <strong>guided kayak tours</strong> pair you with a professional, local guide who knows these waters intimately. Learn about Hawaiian history, marine ecology, and island legends while exploring Oahu\u2019s most stunning coastlines.</p>\n\n<h2>Guided Tour Options</h2>\n\n<h3>Mokulua Islands Kayak &amp; E-Bike Adventure</h3>\n<p>A full-day experience: e-bike through Kailua to the marsh trail, then kayak to the Mokes with a guide. <strong>4\u20135 hours.</strong></p>\n\n<h3>Popoia Island (Flat Island) Guided Tour</h3>\n<p>Paddle to Kailua\u2019s \u201cother\u201d island \u2014 Popoia \u2014 a seabird sanctuary just offshore. <strong>2\u20133 hours.</strong></p>\n\n<h3>Kahana Rainforest River Kayak Tour</h3>\n<p>Paddle up the Kahana River through a lush rainforest valley. <strong>2\u20133 hours.</strong></p>\n\n<h2>What Makes Our Guides Different</h2>\n<ul>\n<li>All guides are <strong>CPR and First Aid certified</strong></li>\n<li><strong>Small groups only</strong> \u2014 8 paddlers max per guide</li>\n<li>Guides share <strong>Hawaiian cultural context and ecology</strong></li>\n<li>Each guide carries a marine radio and first aid kit</li>\n</ul>\n\n<p><strong>Who should book guided?</strong> First-time kayakers, families with kids under 12, anyone wanting deeper cultural and ecological context.</p>'
    },
    {
        "slug": "mokolii",
        "title": "Mokoli\u02bbi Island Kayak \u2014 Chinaman\u2019s Hat Self-Guided Tour | Active Oahu",
        "description": "Kayak to Mokoli\u02bbi Island (Chinaman\u2019s Hat) from Kualoa Park. Shortest kayak trip on Oahu \u2014 self-guided with rental delivery and hiking tips.",
        "h1": "Mokoli\u02bbi Island \u2014 Kayak to Chinaman\u2019s Hat",
        "tourist_type": "Self-Guided",
        "body": '<h2>Mokoli\u02bbi \u2014 Oahu\u2019s Most Photographed Island</h2>\n<p><strong>Mokoli\u02bbi</strong> (meaning \u201clittle lizard\u201d in Hawaiian) is the iconic cone-shaped island 500 yards off Kualoa Regional Park \u2014 the <strong>shortest and easiest kayak trip</strong> on Oahu.</p>\n\n<h2>Quick Facts</h2>\n<ul>\n<li><strong>Paddle distance:</strong> ~500 yards</li>\n<li><strong>Paddle time:</strong> 10\u201315 minutes each way</li>\n<li><strong>Water depth:</strong> Waist-deep at high tide, knee-deep at low</li>\n<li><strong>Summit hike:</strong> 15 minutes, steep/rocky \u2014 closed-toe shoes required</li>\n</ul>\n\n<h2>The Legend</h2>\n<p>Hawaiian legend says the goddess Hi\u02bbiaka (sister of Pele) slew a great mo\u02bbo (dragon). She threw its tail into the ocean, where it became Mokoli\u02bbi. The nickname \u201cChinaman\u2019s Hat\u201d comes from its resemblance to a Chinese peasant\u2019s conical straw hat.</p>'
    },
    {
        "slug": "kailua-kayak",
        "title": "Kailua Kayak Tours & Rentals \u2014 Paddle Oahu\u2019s Best Bay | Active Oahu",
        "description": "Kayak Kailua Bay to the Mokulua Islands, Popoia Island, or along Oahu\u2019s most beautiful coastline. Self-guided and guided tours from Active Oahu.",
        "h1": "Kailua Kayak Tours & Rentals",
        "tourist_type": "Self-Guided",
        "body": '<h2>Kailua Bay \u2014 Oahu\u2019s Premier Kayaking Destination</h2>\n<p><strong>Kailua Bay</strong> on Oahu\u2019s windward coast is the epicenter of kayaking in Hawaii. With turquoise water, protected conditions, and three offshore islands, it\u2019s consistently rated one of the <strong>best beaches in the United States</strong>.</p>\n\n<h2>Kayaking Options from Kailua</h2>\n\n<h3>Mokulua Islands (The Mokes)</h3>\n<p>The classic: paddle 1 mile to the twin islands, land on Moku Nui, explore tide pools and Queens Bath. <strong>2\u20134 hours.</strong></p>\n\n<h3>Popoia Island (Flat Island)</h3>\n<p>A shorter paddle (0.4 miles) to a flat seabird sanctuary island. Great for beginners. <strong>1\u20132 hours.</strong></p>\n\n<h3>Kailua Bay Coastal Paddle</h3>\n<p>Paddle along the Kailua-Lanikai coastline with views of the Mokes and Ko\u02bbolau Range. <strong>1\u20133 hours.</strong></p>\n\n<h2>Why Kailua?</h2>\n<ul>\n<li>Protected by <strong>Oahu\u2019s largest barrier reef</strong> \u2014 calm water year-round</li>\n<li><strong>Two offshore islands</strong> accessible by kayak</li>\n<li><strong>3 miles of white sand beach</strong> \u2014 consistently rated top 5 in the US</li>\n<li>Active Oahu\u2019s check-in station is <strong>2 minutes from the beach</strong></li>\n</ul>\n\n<p>Kailua receives approximately <strong>2.5 million visitors annually</strong>. Go early and you\u2019ll often have the water to yourself.</p>'
    }
]

print(f"Generating {len(pages)} pages...\n")

for p in pages:
    page_dir = f"{SITE}/{p['slug']}"
    os.makedirs(page_dir, exist_ok=True)
    
    # Customize head with page-specific meta
    head = head_template
    head = re.sub(r'<title>[^<]+</title>', f"<title>{p['title']}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{p["description"]}"', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{p["description"]}"', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://activeoahutours.com/{p["slug"]}/"', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{p["description"]}"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://activeoahutours.com/{p["slug"]}/"', head)
    
    # TouristTrip JSON-LD schema right before </head>
    schema = {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": p['title'].split(' | ')[0],
        "description": p['description'],
        "touristType": p['tourist_type'],
        "provider": {
            "@type": "TravelAgency",
            "name": "Active Oahu, LLC",
            "url": "https://activeoahutours.com/"
        }
    }
    schema_ld = f"<script type='application/ld+json'>{json.dumps(schema)}</script>"
    head = head.replace('</head>', f'{schema_ld}\n</head>')
    
    # Assemble page
    content_block = f"""    <div id="content" class="site-content">
        <div class="entry-content">
            <h1>{p['h1']}</h1>
            {p['body']}
        </div><!-- .entry-content -->
    </div>"""
    
    page = head + '\n' + body_top + '\n' + content_block + '\n' + body_bottom + '\n</body>\n</html>'
    
    page_path = f"{page_dir}/index.html"
    with open(page_path, 'w') as f:
        f.write(page)
    
    print(f"  OK {p['slug']}/index.html ({len(page):,} chars) [{p['tourist_type']}]")

print(f"\nAll {len(pages)} pages created with TouristTrip schema.")

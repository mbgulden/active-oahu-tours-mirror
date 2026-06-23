#!/usr/bin/env python3
"""Generate snorkeling comparison pages."""
import os, json, re

SITE = "/home/ubuntu/work/active-oahu-tours-mirror/site"

with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()

pages = [
    {
        "slug": "lanikai-vs-hanauma-bay-snorkeling",
        "title": "Lanikai vs Hanauma Bay Snorkeling — Honest Comparison | Active Oahu",
        "desc": "Honest comparison: Lanikai Beach vs Hanauma Bay for snorkeling on Oahu. Crowds, parking, reef quality, beginner-friendliness, and cost — from a local operator.",
        "h1": "Lanikai vs Hanauma Bay Snorkeling — An Honest Comparison",
        "body": """<h2>Two Very Different Snorkeling Experiences</h2>
<p>Lanikai Beach and Hanauma Bay are both famous Oahu snorkeling spots — but they couldn't be more different. One is a regulated nature preserve with entry fees, crowds, and infrastructure. The other is a wild, free, neighborhood beach with zero facilities and a live reef right off the sand. Here's the honest breakdown from someone who operates near both.</p>

<h2>Quick Comparison</h2>
<ul>
<li><strong>Hanauma Bay:</strong> Regulated nature preserve, $25 entry fee, 1,500+ daily visitors, facilities, lifeguards, limited parking, closed Mon-Tue</li>
<li><strong>Lanikai Beach:</strong> Free public beach, no facilities, no lifeguards, no parking lot, live reef 50-100 yards offshore, open 24/7</li>
</ul>

<h2>Reef Quality & Marine Life</h2>

<h3>Hanauma Bay</h3>
<p>Hanauma Bay is a protected marine life conservation district. The reef has had decades to recover from overuse. You'll see large parrotfish, tangs, butterflyfish, moray eels, and occasionally turtles. The reef is extensive but deep in places — beginners tend to stay in the sandy shallows.</p>

<h3>Lanikai Beach</h3>
<p>Lanikai has a <strong>live reef system right off the sandy shore</strong> — 50 to 100 yards out. No boat ride, no long swim. Just walk into the water and paddle toward the Mokulua Islands. The reef here is active with smaller tropical fish, coral formations, and regular turtle sightings. Because fewer people snorkel here (most come for the beach), the reef sees less daily pressure.</p>
<p><strong>Winner:</strong> Lanikai for accessibility and beginner-friendliness. Hanauma for volume and variety of marine life.</p>

<h2>Crowds & Experience</h2>

<h3>Hanauma Bay</h3>
<p>1,500 visitors per day (capped). Mandatory 9-minute educational video before entry. Timed reservations required. Lines form by 6:30 AM. Once inside, the beach is large enough to spread out but the best snorkeling areas near the reef can get crowded. Closed Monday and Tuesday.</p>

<h3>Lanikai Beach</h3>
<p>No cap. No reservations. No entry fee. The beach is a narrow strip of sand fronting a residential neighborhood. Weekends get busy with locals and visitors. Weekday mornings are quiet. The snorkeling area off the beach is rarely crowded because most people stay on the sand.</p>
<p><strong>Winner:</strong> Lanikai for freedom and spontaneity. Hanauma is more controlled — which is either a pro or con depending on your preference.</p>

<h2>Parking & Access — The Big Difference</h2>

<h3>Hanauma Bay</h3>
<p>Large parking lot ($3). Fills by 7:30-8:00 AM. Once full, they turn cars away. Your alternative is parking at Koko Marina and taking a shuttle or rideshare. At least there IS parking.</p>

<h3>Lanikai Beach</h3>
<p><strong>There is NO parking at Lanikai Beach.</strong> None. Zero. The entire neighborhood is residential with strict no-parking enforcement. Your options:</p>
<ul>
<li><strong>Park at Kailua Beach Park</strong> (1 mile walk along the coast)</li>
<li><strong>Ride an e-bike from Kailua</strong> — 10-minute ride, bike lockup stations at Lanikai Park near the beach access</li>
<li>Get dropped off by rideshare (but pickup can be hard with no cell service in spots)</li>
</ul>
<p><strong>This is Lanikai's biggest drawback.</strong> But there's a solution: <a href="/electric-bike-rentals/">Active Oahu rents e-bikes</a> from our Kailua shop. Ride 10 minutes to Lanikai Park, lock up at the official bike station, and walk 100 yards to the sand. <strong>Zero parking stress.</strong></p>

<h2>Facilities</h2>

<h3>Hanauma Bay</h3>
<p>Restrooms, showers, snack bar, gift shop, snorkel gear rentals, lifeguards, educational center. Full-service experience.</p>

<h3>Lanikai Beach</h3>
<p><strong>No restrooms. No showers. No lifeguards. No vendors.</strong> Nothing. Bring everything you need and take everything with you. The nearest restroom is at Kailua Beach Park — a 1-mile walk.</p>
<p><strong>Winner:</strong> Hanauma Bay, obviously. Lanikai is for people who value freedom over facilities.</p>

<h2>Cost</h2>

<h3>Hanauma Bay</h3>
<p>$25 entry fee per person (non-resident). $3 parking. Snorkel gear rental: $20-25 on-site. Total for two people: ~$75-100.</p>

<h3>Lanikai Beach</h3>
<p>Free entry. Free beach. <a href="/beach-gear-rentals/">Snorkel gear rental from our Kailua shop:</a> $15/day. <a href="/electric-bike-rentals/">E-bike rental:</a> $55-95/day (solves parking). Total for two people: $30-125 depending on gear.</p>
<p><strong>Winner:</strong> Lanikai for budget. Hanauma's fee supports conservation — worth it if you value the infrastructure.</p>

<h2>Who Should Choose Which</h2>

<h3>Choose Hanauma Bay if:</h3>
<ul>
<li>You want a curated, educational experience</li>
<li>You need facilities (restrooms, showers, food)</li>
<li>You want maximum marine life variety</li>
<li>You're okay with crowds and planning ahead</li>
<li>You're visiting Tuesday-Saturday (closed Mon-Tue)</li>
</ul>

<h3>Choose Lanikai if:</h3>
<ul>
<li>You want a natural, unstructured experience</li>
<li>You're a beginner who wants easy reef access from the sand</li>
<li>You hate crowds and reservations</li>
<li>You're combining snorkeling with a beach day or kayaking</li>
<li>You have an e-bike (solves the parking problem)</li>
<li>You're going any day of the week — Lanikai is always open</li>
</ul>

<h2>Our Recommendation</h2>
<p>If you're staying on the Windward side (Kailua, Lanikai, Kaneohe), <strong>snorkel Lanikai.</strong> Rent gear from our shop, grab an e-bike, and ride to the beach in 10 minutes. The reef is right there, the crowds are minimal, and you'll have the rest of your day free.</p>
<p>If you're staying in Waikiki or Honolulu, Hanauma Bay is closer and the full-service experience is worth the fee — just book your reservation weeks in advance.</p>"""
    },
    {
        "slug": "sharks-cove-vs-lanikai-snorkeling",
        "title": "Sharks Cove vs Lanikai Snorkeling — Which Is Better? | Active Oahu",
        "desc": "Sharks Cove vs Lanikai Beach snorkeling comparison. Marine life, difficulty, parking, seasonality, and honest advice from a local Kailua operator.",
        "h1": "Sharks Cove vs Lanikai Snorkeling — Which Should You Choose?",
        "body": """<h2>North Shore vs Windward Side — Two Worlds</h2>
<p>Sharks Cove (North Shore) and Lanikai Beach (Windward Coast) represent two completely different Oahu snorkeling experiences. One is a world-famous rocky cove with 100+ fish species. The other is a quiet sandy beach with a live reef just offshore. They're only 45 minutes apart by car — but they're worlds apart in experience.</p>

<h2>Quick Comparison</h2>
<ul>
<li><strong>Sharks Cove:</strong> Rocky volcanic cove, summer only (May-Oct), 100+ species, intermediate skill, limited parking, world-class reputation</li>
<li><strong>Lanikai Beach:</strong> Sandy beach, year-round, reef 50-100 yards out, beginner-friendly, no parking, no facilities, local secret</li>
</ul>

<h2>Marine Life</h2>

<h3>Sharks Cove</h3>
<p>Consistently rated a top-12 shore dive <strong>in the world</strong>. The volcanic rock formations create protected pockets where fish concentrate. You'll see: parrotfish, butterflyfish, tangs, wrasse, moray eels, octopus, and frequent honu (green sea turtles). The variety and density is unmatched on Oahu. <strong>Over 100 species</strong> documented in the cove.</p>

<h3>Lanikai Beach</h3>
<p>The reef at Lanikai is smaller but <strong>accessible and alive.</strong> Walk 50-100 yards offshore and you're over coral heads with tropical fish, sea urchins, and occasional turtles. Because fewer people specifically come to Lanikai to snorkel (most come for the beach), the reef feels more like your own discovery. <strong>Beginner-friendly</strong> — no rocky entry, no surge, no deep water to navigate.</p>
<p><strong>Winner:</strong> Sharks Cove for marine life density. Lanikai for ease and personal experience.</p>

<h2>Skill Level & Entry</h2>

<h3>Sharks Cove</h3>
<p><strong>Intermediate.</strong> The entry is rocky — you need water shoes and sure footing. The outer reef drops quickly to deeper water. There can be surge near the channel on the north side. Winter brings 20+ foot waves — <strong>summer only.</strong> Not recommended for first-time snorkelers or young children.</p>

<h3>Lanikai Beach</h3>
<p><strong>Beginner-friendly.</strong> Walk into the water from soft sand. The reef is in calm, protected water inside the Mokulua Islands' wind shadow. No surge, no rocks, no drop-offs. Perfect for first-time snorkelers, kids, and anyone who wants a relaxed experience. <strong>Year-round.</strong></p>
<p><strong>Winner:</strong> Lanikai. It's hard to find an easier snorkeling entry on Oahu.</p>

<h2>Seasonality</h2>

<h3>Sharks Cove</h3>
<p><strong>Summer only (May — October).</strong> Winter North Shore surf makes the cove unapproachable and dangerous — waves can exceed 20 feet. This is a hard seasonal limitation. If you're visiting Oahu between November and April, Sharks Cove is likely closed to snorkeling.</p>

<h3>Lanikai Beach</h3>
<p><strong>Year-round.</strong> The offshore islands (Mokulua) and barrier reef protect Lanikai from big swell. Water is calm and clear in all seasons. Summer is glassy; winter might have some wind chop but remains snorkelable.</p>
<p><strong>Winner:</strong> Lanikai. It's always available. Sharks Cove has a 5-month window.</p>

<h2>Parking & Access</h2>

<h3>Sharks Cove</h3>
<p>Tiny lot — maybe 20 spaces. Fills by 8 AM. Overflow parking at Pupukea Beach Park (5-minute walk). The North Shore has one road in and out — traffic can be brutal on weekends.</p>

<h3>Lanikai Beach</h3>
<p><strong>Zero parking.</strong> Residential neighborhood with strict enforcement. <strong>Solution:</strong> <a href="/electric-bike-rentals/">Rent an e-bike</a> from our Kailua shop. 10-minute ride. Lock up at Lanikai Park's official bike station. Walk 100 yards to the sand. No traffic, no tickets, no stress.</p>
<p><strong>Winner:</strong> Sharks Cove has actual parking. Lanikai requires a strategy — but the e-bike solution makes it painless.</p>

<h2>Facilities</h2>

<h3>Sharks Cove</h3>
<p>Portable restrooms across the street at Pupukea Beach Park. Food trucks often nearby on weekends. No showers, no lifeguards, no rentals on-site.</p>

<h3>Lanikai Beach</h3>
<p><strong>Nothing.</strong> No restrooms, no showers, no lifeguards, no vendors. Bring everything. Pack out everything.</p>
<p><strong>Winner:</strong> Sharks Cove, barely. Neither is a resort beach.</p>

<h2>Who Should Choose Which</h2>

<h3>Choose Sharks Cove if:</h3>
<ul>
<li>You're an intermediate or experienced snorkeler</li>
<li>You're visiting in summer (May — October)</li>
<li>You want maximum marine life density and variety</li>
<li>You can arrive by 8 AM for parking</li>
<li>You're okay with a rocky entry and deeper water</li>
</ul>

<h3>Choose Lanikai if:</h3>
<ul>
<li>You're a beginner or snorkeling with kids</li>
<li>You're visiting ANY time of year</li>
<li>You want a soft sand entry and calm water</li>
<li>You want to combine snorkeling with a beach day</li>
<li>You have (or rent) an e-bike — solves parking completely</li>
<li>You value a natural, uncrowded experience</li>
</ul>

<h2>Can You Do Both?</h2>
<p>Absolutely. They're 45 minutes apart. Morning at Sharks Cove (arrive 8 AM, snorkel 2 hours), then drive the coast to Lanikai for an afternoon beach-and-snorkel session. Rent gear once from our Kailua shop and you're equipped for both. <a href="/beach-gear-rentals/">Browse snorkel gear rentals →</a></p>

<h2>Our Recommendation</h2>
<p>If you're staying on the Windward side and want a low-stress, beautiful snorkeling experience you can do any day without planning — <strong>Lanikai wins.</strong> The live reef, the soft sand entry, and the year-round availability make it the most accessible good snorkeling on Oahu.</p>
<p>If you're a dedicated snorkeler visiting in summer who wants to see what a world-class reef looks like — <strong>Sharks Cove is a bucket-list experience.</strong> Just plan ahead, arrive early, and check the swell report.</p>"""
    }
]

print(f"Generating {len(pages)} comparison pages...\n")

for p in pages:
    page_dir = f"{SITE}/{p['slug']}"
    os.makedirs(page_dir, exist_ok=True)
    
    head = head_template
    head = re.sub(r'<title>[^<]+</title>', f"<title>{p['title']}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{p["desc"]}"', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{p["desc"]}"', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://activeoahutours.com/{p["slug"]}/"', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{p["desc"]}"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://activeoahutours.com/{p["slug"]}/"', head)
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p['title'].split(' | ')[0],
        "description": p['desc'],
        "author": {"@type": "Person", "name": "Michael Gulden", "jobTitle": "Owner & Operator, Active Oahu"},
        "publisher": {"@type": "Organization", "name": "Active Oahu, LLC"}
    }
    schema_ld = f"<script type='application/ld+json'>{json.dumps(schema)}</script>"
    head = head.replace('</head>', f'{schema_ld}\n</head>')
    
    content_block = f"""    <div id="content" class="site-content">
        <div class="entry-content">
            <h1>{p['h1']}</h1>
            {p['body']}
        </div><!-- .entry-content -->
    </div>"""
    
    page = head + '\n' + body_top + '\n' + content_block + '\n' + body_bottom + '\n</body>\n</html>'
    
    with open(f"{page_dir}/index.html", 'w') as f:
        f.write(page)
    
    print(f"  ✅ {p['slug']}/ ({len(page):,} chars)")

print(f"\nDone. Both comparison pages created with e-bike parking solution featured.")

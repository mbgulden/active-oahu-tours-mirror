#!/usr/bin/env python3
"""Generate content cluster guide pages for Active Oahu Tours."""
import os, json, re

SITE = "/home/ubuntu/work/active-oahu-static/site"

with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()

pages = [
    {
        "slug": "kualoa-bay-guide",
        "title": "Kualoa Regional Park: Parking, Launch & Kayak Guide | Active Oahu",
        "desc": "Complete guide to Kualoa Regional Park: parking, facilities, kayak launch points, and paddling to Chinaman's Hat from Kualoa Beach Park on Oahu.",
        "h1": "Kualoa Regional Park: Parking, Launch & Kayak Guide",
        "body": """<h2>Why Kualoa Regional Park?</h2>
<p>Kualoa Regional Park sits at the base of the legendary Koʻolau Mountains on Oahu's windward coast. This is the launching point for paddling to <strong>Mokoliʻi (Chinaman's Hat)</strong> — one of Oahu's shortest and most rewarding kayak trips at just 500 yards across a shallow reef shelf.</p>
<p>The park offers stunning views of <strong>Kualoa Ranch</strong> (where Jurassic Park, Lost, and Kong: Skull Island were filmed), making this one of the most scenic launch points in Hawaii.</p>

<h2>Parking at Kualoa Regional Park</h2>
<ul>
<li><strong>Parking lot:</strong> Large, free, public parking lot</li>
<li><strong>Capacity:</strong> 50+ spaces — fills by 9:00 AM on weekends and holidays</li>
<li><strong>Best arrival time:</strong> Before 8:30 AM for guaranteed parking</li>
<li><strong>Alternative:</strong> Overflow parking along Kamehameha Highway (watch for no-parking signs)</li>
<li><strong>Note:</strong> Do not leave valuables visible in your vehicle</li>
</ul>

<h2>Facilities</h2>
<ul>
<li>Restrooms with showers</li>
<li>Picnic tables and grassy areas</li>
<li>Palm tree shade</li>
<li>Drinking water fountains</li>
<li>No lifeguard on duty — swim and paddle at your own risk</li>
</ul>

<h2>Kayak Launch at Kualoa</h2>
<p>The launch is a sandy beach with protected, calm water inside the reef. The paddle to Chinaman's Hat is approximately <strong>500 yards</strong> across a shallow reef shelf — rarely deeper than waist-deep at high tide.</p>
<ul>
<li><strong>Best conditions:</strong> Morning, low-to-mid tide, trade winds under 15 mph</li>
<li><strong>Difficulty:</strong> Beginner-friendly</li>
<li><strong>Paddle time:</strong> 10-20 minutes each way</li>
<li><strong>Water depth:</strong> Knee to waist-deep depending on tide</li>
</ul>

<h2>Getting Here from Active Oahu</h2>
<p>Our Kailua shop (134B Hamakua Dr) is about a <strong>35-minute drive</strong> from Kualoa Regional Park. We provide <a href="/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/">foam pads and straps</a> so you can transport your rental kayak on any 4-door vehicle.</p>
<p><strong>Directions:</strong> Take Kalanianaʻole Highway north through Kaneohe, continue on Kahekili Highway, then Kamehameha Highway to the park entrance on your right.</p>

<h2>What to Paddle To</h2>
<ul>
<li><strong><a href="/chinamans-hat/">Chinaman's Hat (Mokoliʻi)</a></strong> — 500 yards, 10-20 min. Hike to the summit for 360° views</li>
<li><strong>Kualoa coastline</strong> — Paddle north along the dramatic Koʻolau cliffs</li>
<li><strong>Secret Island</strong> — Small sandbar south of the park (accessible at low tide)</li>
</ul>

<p><strong>Need a kayak?</strong> <a href="/kayak-rentals/">Rent from our Kailua shop</a> with soft racks included — pick up, drive to Kualoa, and launch as a private boater.</p>"""
    },
    {
        "slug": "chinamans-hat-tide-guide",
        "title": "Chinaman's Hat Tide Guide — Best Times to Paddle Mokoliʻi | Active Oahu",
        "desc": "Tide guide for paddling to Chinaman's Hat (Mokoliʻi). Best tide levels, water depth, safety tips, and when to go for the easiest landing.",
        "h1": "Chinaman's Hat (Mokoliʻi) Tide Guide — Best Times to Paddle",
        "body": """<h2>Understanding Tides at Chinaman's Hat</h2>
<p>The paddle to Mokoliʻi (Chinaman's Hat) from Kualoa Beach Park crosses a <strong>shallow reef shelf</strong> — water depth changes dramatically with the tide. Knowing the tide schedule is the difference between an easy paddle and a frustrating one.</p>

<h2>Best Tide for Chinaman's Hat</h2>
<ul>
<li><strong>Ideal:</strong> Mid-to-low tide</li>
<li><strong>Why:</strong> The reef is exposed or just covered — you can see where you're paddling, avoid coral heads, and land easily on the island's small beach</li>
<li><strong>Water depth at low tide:</strong> Knee-deep in most areas</li>
<li><strong>Water depth at high tide:</strong> Waist-to-chest deep</li>
</ul>

<h2>Tide Levels — What to Expect</h2>

<h3>Low Tide (0.0 ft — 0.5 ft)</h3>
<p><strong>Best conditions.</strong> The reef shelf is mostly exposed or just barely covered. You can walk portions of the route if needed. The island's beach is fully exposed for easy landing. Coral heads are visible and avoidable. <strong>Recommended for beginners.</strong></p>

<h3>Mid Tide (0.5 ft — 1.5 ft)</h3>
<p><strong>Good conditions.</strong> Water covers the reef but remains shallow. Easy paddling with good visibility. The island beach is still accessible. <strong>Fine for all skill levels.</strong></p>

<h3>High Tide (1.5 ft — 2.5+ ft)</h3>
<p><strong>Still doable but less ideal.</strong> Water is deeper — you're paddling over submerged reef. Harder to see coral heads. The island's beach may be partially submerged, making landing trickier. <strong>Best for intermediate paddlers.</strong></p>

<h2>How to Check the Tide</h2>
<p>Use <strong>NOAA Tide Predictions for Moku o Loʻe (Coconut Island), Kaneohe Bay</strong> — this is the nearest tide station to Kualoa. Check the tide chart for the day you plan to go and aim to launch when the tide is falling toward low or at low tide.</p>

<h2>Safety Tips</h2>
<ul>
<li><strong>Wear water shoes</strong> — the reef is sharp. Do not paddle barefoot</li>
<li><strong>Avoid outgoing tide + strong wind</strong> — wind against tide creates chop</li>
<li><strong>Summer mornings are best</strong> — calmest water, lowest crowds</li>
<li><strong>Winter swells</strong> — north and east swells can make the paddle challenging even at low tide. Check conditions before going</li>
<li><strong>Never paddle alone</strong> — always go with a buddy</li>
</ul>

<p><strong>Planning a trip?</strong> <a href="/kayak-rentals/">Rent a kayak from our Kailua shop</a> — we include a printed tide chart with every rental.</p>"""
    },
    {
        "slug": "kaneohe-sandbar-tide-guide",
        "title": "Kaneohe Sandbar Tide Calendar — Best Times to Visit | Active Oahu",
        "desc": "Tide guide for the Kaneohe Sandbar (Ahu o Laka). Best tide levels, when the sandbar is exposed, and how to time your visit perfectly.",
        "h1": "Kaneohe Sandbar (Ahu o Laka) — Tide Guide & Best Times to Visit",
        "body": """<h2>Understanding the Kaneohe Sandbar Tides</h2>
<p>The Kaneohe Sandbar (Ahu o Laka) is a sunken reef that transforms dramatically with the tide. At low tide, a <strong>beach appears in the middle of Kaneohe Bay</strong> — surrounded by turquoise water stretching to the horizon. At high tide, the sandbar submerges completely.</p>
<p>Timing your visit around the tide is everything. This guide helps you pick the perfect window.</p>

<h2>Tide Levels — What to Expect</h2>

<h3>Low Tide (Below 0.0 ft) — The Sweet Spot</h3>
<p><strong>Full sand exposure.</strong> The sandbar emerges as a proper beach — you can walk around, set up chairs, play volleyball, and wade in ankle-deep water. This is the classic Kaneohe Sandbar experience. Sand exposure typically lasts 2-4 hours around low tide. <strong>Perfect for families, groups, and social paddles.</strong></p>

<h3>Rising Tide (0.0 ft — 1.0 ft) — Still Great</h3>
<p>Water gradually rises over the sandbar. Waist-deep at most. You're still standing on sand, just in water. <strong>Ideal for wading, floating, and snorkeling</strong> around the sandbar edges.</p>

<h3>High Tide (Above 1.5 ft) — Submerged</h3>
<p>The sandbar is completely underwater. You can still paddle over it but there's no exposed sand and nowhere to stand. <strong>Not recommended</strong> unless you're just passing through on a longer paddle.</p>

<h2>How to Check the Tide</h2>
<p>Use <strong>NOAA Tide Predictions for Moku o Loʻe (Coconut Island), Kaneohe Bay</strong>. Look for days when low tide falls during daylight hours (ideally 8 AM — 2 PM). Plan to arrive at the sandbar <strong>30-60 minutes before low tide</strong> for maximum sand time.</p>

<h2>Best Months for the Sandbar</h2>
<ul>
<li><strong>May — September:</strong> Calmest water, most consistent low tides during daylight. Summer = sandbar season</li>
<li><strong>October — April:</strong> More wind and swell. Check conditions — the paddle from Heʻeia Kea Pier can be choppy</li>
</ul>

<h2>Safety Notes</h2>
<ul>
<li><strong>Sun exposure:</strong> Zero shade on the sandbar. Bring sunscreen, hats, and rash guards</li>
<li><strong>Hydration:</strong> Bring water — there's nowhere to buy any</li>
<li><strong>Anchor your kayak:</strong> The current can drift your boat away. We rent kayak anchors</li>
<li><strong>Check the wind:</strong> Afternoon trade winds (15-20 mph) create chop in Kaneohe Bay. Morning paddles are calmer</li>
<li><strong>This is a Marine Life Conservation District:</strong> No fishing, no collecting. Protect the reef — don't walk on coral heads</li>
</ul>

<p><strong>This guide is for private recreational boaters.</strong> Hawaii State Law prohibits commercial tours and deliveries in Kaneohe Bay. <a href="/kaneohe-sandbar/">Learn how to kayak the sandbar legally →</a></p>"""
    },
    {
        "slug": "sharks-cove-snorkeling-guide",
        "title": "Sharks Cove Snorkeling Guide — Marine Life, Conditions & Tips | Active Oahu",
        "desc": "Complete guide to snorkeling Sharks Cove on Oahu's North Shore. Marine life, best conditions, gear tips, and what to expect at this world-class snorkel spot.",
        "h1": "Sharks Cove Snorkeling: Marine Life, Conditions & Tips",
        "body": """<h2>Why Sharks Cove Is World-Class</h2>
<p>Sharks Cove, on Oahu's legendary North Shore, is consistently rated one of the <strong>top 12 shore dives in the world</strong> by Scuba Diving Magazine. During summer months (May through October), the North Shore goes flat, revealing a protected marine ecosystem with over 100 species of tropical fish, green sea turtles (honu), and vibrant coral formations.</p>
<p><strong>Despite its name, sharks are extremely rare here</strong> — the cove got its name from its outline shape when viewed from above, which resembles a shark.</p>

<h2>When to Go</h2>
<ul>
<li><strong>Season:</strong> May — October (summer only)</li>
<li><strong>Winter (November — April):</strong> The North Shore receives massive surf — waves can exceed 20 feet. Sharks Cove is <strong>not safe for snorkeling</strong> during winter months</li>
<li><strong>Best time of day:</strong> 8:00 AM — 11:00 AM. Arrive early for parking and the calmest water</li>
<li><strong>Duration:</strong> 2-3 hours in the water</li>
<li><strong>Skill level:</strong> Beginner to intermediate (summer conditions)</li>
</ul>

<h2>Marine Life You'll See</h2>
<ul>
<li><strong>Honu (Green Sea Turtles):</strong> Frequent visitors feeding on algae along the rocky edges</li>
<li><strong>Humuhumunukunukuāpuaʻa:</strong> Hawaii's state fish — the reef triggerfish — common in the shallows</li>
<li><strong>Parrotfish (Uhu):</strong> Large, colorful fish that feed on coral. You'll hear them crunching underwater</li>
<li><strong>Butterflyfish & Tangs:</strong> Dozens of species in the shallows. Look for the bright yellow tang</li>
<li><strong>Moray Eels:</strong> Spotted in crevices along the outer reef edge</li>
<li><strong>Octopus (Heʻe):</strong> Masters of camouflage in the rocky sections</li>
<li><strong>Spinner Dolphins:</strong> Occasionally pass by the outer reef in the early morning</li>
</ul>

<h2>Gear You'll Need</h2>
<ul>
<li>Mask (silicone skirt, tempered glass lens)</li>
<li>Snorkel (dry-top valve recommended for beginners)</li>
<li>Fins (full-foot for warm water)</li>
<li>Rash guard or wetsuit top (sun protection + warmth)</li>
<li>Reef-safe sunscreen (zinc-based — Hawaii law prohibits chemical sunscreens)</li>
<li>Water shoes (rocky entry in some areas)</li>
<li>Waterproof phone case (for photos)</li>
</ul>

<p><strong>Need gear?</strong> <a href="/beach-gear-rentals/">Rent snorkel sets, rash guards, and beach gear</a> from our Kailua shop and drive to the North Shore (~45 min).</p>

<h2>Conditions to Watch</h2>
<ul>
<li><strong>North swell:</strong> Any north swell over 2-3 feet makes the cove unsafe. Check <a href="https://www.surfnewsnetwork.com" target="_blank">Surf News Network</a> before going</li>
<li><strong>Tide:</strong> Mid-to-high tide provides the best water coverage over the reef</li>
<li><strong>Visibility:</strong> Typically 30-50 feet in summer. Best after several days of calm weather</li>
<li><strong>Entry:</strong> Rocky in places. Enter from the sandy section on the south side of the cove</li>
</ul>

<h2>Safety Tips</h2>
<ul>
<li>Never snorkel alone — always bring a buddy</li>
<li>Don't touch the turtles — it's illegal under Hawaii state law</li>
<li>Watch your fins — avoid kicking coral</li>
<li>The outer reef drops off quickly. Stay within your comfort zone</li>
<li>Rip currents can form near the channel on the north side — avoid that area</li>
<li>There are no lifeguards at Sharks Cove</li>
</ul>

<p><strong>Important:</strong> Parking at Sharks Cove is extremely limited — arrive by 8 AM or plan to park at Pupukea Beach Park and walk 5 minutes.</p>"""
    }
]

print(f"Generating {len(pages)} content guide pages...\n")

for p in pages:
    page_dir = f"{SITE}/{p['slug']}"
    os.makedirs(page_dir, exist_ok=True)
    
    # Customize head
    head = head_template
    head = re.sub(r'<title>[^<]+</title>', f"<title>{p['title']}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{p["desc"]}"', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{p["desc"]}"', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://activeoahutours.com/{p["slug"]}/"', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{p["title"]}"', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{p["desc"]}"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://activeoahutours.com/{p["slug"]}/"', head)
    
    # Article schema
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
    
    # Assemble page
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

print(f"\nAll {len(pages)} guide pages created.")

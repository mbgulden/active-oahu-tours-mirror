#!/usr/bin/env python3
"""Generate 4 informational/operational pages for Active Oahu Tours static mirror."""
import os, json, re

SITE = "/home/ubuntu/work/active-oahu-static/site"

# Read templates
with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()

pages = [
    # PAGE 1: What to Bring
    {
        "slug": "what-to-bring",
        "title": "Oahu Kayak Trip Packing List \u2014 What to Bring | Active Oahu",
        "description": "Comprehensive packing checklist for your Oahu kayak trip. See what Active Oahu provides with every rental and what you should bring for a safe, comfortable paddle.",
        "h1": "Oahu Kayak Trip Packing List \u2014 What to Bring",
        "body": """<h2>Rental Includes \u2014 We Provide</h2>
<p>Every Active Oahu rental comes fully equipped so you can hit the water with confidence. Here's what's included in your booking:</p>
<ul>
<li><strong>Kayak:</strong> Sit-on-top ocean kayak (single or tandem options available)</li>
<li><strong>PFD (Life Vest):</strong> USCG-approved personal flotation device, sized to fit</li>
<li><strong>Paddle:</strong> Lightweight paddle with leash</li>
<li><strong>Soft Racks:</strong> Foam blocks and tie-down straps for roof transport (fits most 4-door vehicles)</li>
<li><strong>Dry Bag:</strong> Waterproof dry bag for your phone, keys, and small valuables</li>
</ul>

<h2>You Bring \u2014 Essential Items</h2>
<p>These items are not included with your rental but are essential for a safe and enjoyable day on the water:</p>
<ul>
<li><strong>Water:</strong> At least 1 liter per person \u2014 more for longer trips. Hawaii's sun is intense and dehydration happens fast on the water.</li>
<li><strong>Sunscreen:</strong> Reef-safe sunscreen (mineral-based, SPF 30+). Hawaii banned oxybenzone and octinoxate sunscreens to protect coral reefs \u2014 please use reef-safe only.</li>
<li><strong>Snacks:</strong> Energy bars, fruit, sandwiches \u2014 you'll burn calories paddling.</li>
<li><strong>Water Shoes:</strong> Closed-toe water shoes or secure sandals. Lava rock and reef cuts are common \u2014 bare feet are not recommended.</li>
<li><strong>Phone:</strong> Fully charged for navigation, photos, and emergency contact. Store in the dry bag when not in use.</li>
</ul>

<h2>Optional Add-Ons</h2>
<p>Enhance your adventure with these optional add-ons available at checkout:</p>
<ul>
<li><strong>Snorkel Gear:</strong> Mask, snorkel, and fins \u2014 perfect for combining kayaking with underwater exploration at Kailua Bay, Sharks Cove, or the Kaneohe Sandbar.</li>
<li><strong>Anchor:</strong> A small kayak anchor lets you hold position at the Kaneohe Sandbar or over snorkel spots without drifting.</li>
<li><strong>Cooler:</strong> Keep drinks and lunch cold on the water. Fits in the rear tank well of our tandem kayaks.</li>
<li><strong>Rash Guard:</strong> UPF 50+ long-sleeve rash guard available for rent. Protects from sun and prevents chafing during longer paddles.</li>
</ul>

<h2>What to Wear</h2>
<ul>
<li><strong>Swimwear:</strong> Quick-dry board shorts or swimsuit as your base layer.</li>
<li><strong>Rash Guard or Lightweight Long Sleeve:</strong> The equatorial sun is intense \u2014 cover up.</li>
<li><strong>Hat:</strong> Wide-brim hat with a chin strap (the tradewinds will take it otherwise).</li>
<li><strong>Sunglasses:</strong> Polarized sunglasses with a strap \u2014 the glare off the water is significant.</li>
<li><strong>Water Shoes or Secure Sandals:</strong> Not flip-flops \u2014 they slip off in the water.</li>
</ul>

<h2>Pro Tips</h2>
<ul>
<li><strong>Pack light:</strong> Storage space on a kayak is limited. One small backpack per person is plenty.</li>
<li><strong>Double-bag electronics:</strong> Put your phone in a ziplock bag inside the dry bag for extra protection.</li>
<li><strong>Freeze your water bottles:</strong> They'll melt slowly and stay cold for hours on the water.</li>
<li><strong>Leave valuables at home:</strong> Car break-ins can happen at beach parking lots \u2014 only bring what you need.</li>
</ul>

<p><strong>Need gear?</strong> Visit our <a href="../rentals/">rentals page</a> to add snorkel gear, anchors, coolers, or rash guards to your booking.</p>"""
    },
    # PAGE 2: Oahu Launch Guide
    {
        "slug": "oahu-launch-guide",
        "title": "Oahu Kayak Launch Guide \u2014 Legal Public Access Points | Active Oahu",
        "description": "Complete guide to legal kayak launch points on Oahu with parking info, facilities, skill levels, and drive times from our Kailua shop. Private recreational access only.",
        "h1": "Oahu Kayak Launch Guide \u2014 Legal Public Access Points",
        "body": """<h2>Know Where to Launch</h2>
<p>Finding a legal, safe launch point is the first step to a great kayak trip. Below are the public access points we recommend for recreational kayakers renting from Active Oahu. <strong>Important:</strong> per <a href="https://www.capitol.hawaii.gov/hrscurrent/Vol04_Ch0201-0257/HRS0200/HRS_0200-0039.htm" target="_blank" rel="noopener">HRS &sect; 200-39</a>, these launch sites are for <strong>private boaters only</strong> &mdash; no commercial drop-offs or guided tour launches are permitted at these locations.</p>

<div style="background:#f0f8ff;border:1px solid #b8d4e8;border-radius:6px;padding:15px;margin:20px 0;">
<p style="margin:0;"><strong>&#9888; Important:</strong> This guide is for <em>private recreational boaters</em> who have rented equipment from Active Oahu. Commercial guided operations launch from separate permitted locations.</p>
</div>

<h2>Kailua Beach Park</h2>
<ul>
<li><strong>Address:</strong> 526 Kawailoa Rd, Kailua, HI 96734</li>
<li><strong>Drive Time from Shop:</strong> 5 minutes</li>
<li><strong>Parking:</strong> Large lot (fills by 9 AM on weekends). Overflow parking at Kailua Town Center. <a href="https://www.honolulu.gov/parks/beachparks/kailua-beach-park.html" target="_blank" rel="noopener">Official site</a></li>
<li><strong>Facilities:</strong> Restrooms, outdoor showers, picnic tables, lifeguard (daytime hours)</li>
<li><strong>Best For:</strong> <strong>Beginner to Intermediate</strong> &mdash; Protected by barrier reef, calm conditions year-round</li>
<li><strong>Launch Notes:</strong> Use the boat ramp near the middle of the beach. Paddle out to the Mokulua Islands (1 mile) or Flat Island (0.4 miles)</li>
</ul>

<h2>Kualoa Beach Park</h2>
<ul>
<li><strong>Address:</strong> 49-479 Kamehameha Hwy, Kaneohe, HI 96744</li>
<li><strong>Drive Time from Shop:</strong> 25 minutes</li>
<li><strong>Parking:</strong> Medium lot, usually available weekdays. Weekends can fill. Street parking on Kamehameha Hwy with care.</li>
<li><strong>Facilities:</strong> Restrooms, picnic tables, grassy area, views of Mokoli&#699;i and the Ko&#699;olau Range</li>
<li><strong>Best For:</strong> <strong>Beginner</strong> &mdash; Shortest paddle on Oahu (500 yards to Mokoli&#699;i). Shallow reef shelf, rarely deeper than waist-deep at high tide</li>
<li><strong>Launch Notes:</strong> Launch near the palm tree grove at the northern end of the park. Paddle toward the cone-shaped island directly offshore.</li>
</ul>

<h2>He&#699;eia Kea Pier</h2>
<ul>
<li><strong>Address:</strong> 46-499 Kamehameha Hwy, Kaneohe, HI 96744</li>
<li><strong>Drive Time from Shop:</strong> 20 minutes</li>
<li><strong>Parking:</strong> Small lot at the pier. Additional parking at He&#699;eia State Park (small fee). Arrive early on weekends.</li>
<li><strong>Facilities:</strong> Restrooms at pier, He&#699;eia State Park has full facilities. Food options at nearby He&#699;eia Pier General Store &amp; Deli.</li>
<li><strong>Best For:</strong> <strong>Intermediate</strong> &mdash; 1.5-mile paddle to the Kaneohe Sandbar across protected but open bay water</li>
<li><strong>Launch Notes:</strong> Best launch for the Kaneohe Sandbar. Check tide charts before going &mdash; low-to-mid tide gives the best sandbar experience.</li>
</ul>

<h2>Hale&#699;iwa Beach Park (North Shore)</h2>
<ul>
<li><strong>Address:</strong> 62-449 Kamehameha Hwy, Hale&#699;iwa, HI 96712</li>
<li><strong>Drive Time from Shop:</strong> 50 minutes</li>
<li><strong>Parking:</strong> Medium lot. Hale&#699;iwa town is busy &mdash; arrive early or park in town and walk.</li>
<li><strong>Facilities:</strong> Restrooms, showers, lifeguard, picnic tables. Close to Hale&#699;iwa town restaurants and shops.</li>
<li><strong>Best For:</strong> <strong>Intermediate to Advanced</strong> &mdash; North Shore conditions require experience. <strong>Summer only</strong> (May&ndash;October). Winter brings massive surf unsuitable for kayaking.</li>
<li><strong>Launch Notes:</strong> Launch from the beach area south of the harbor. Paddle up the Anahulu River for a calm experience, or along the coast on calm summer days.</li>
</ul>

<h2>Kahana Bay Beach Park</h2>
<ul>
<li><strong>Address:</strong> 52-222 Kamehameha Hwy, Hau&#699;ula, HI 96717</li>
<li><strong>Drive Time from Shop:</strong> 40 minutes</li>
<li><strong>Parking:</strong> Small lot, rarely full. Additional parking along Kamehameha Hwy shoulder.</li>
<li><strong>Facilities:</strong> Restrooms, picnic tables, shaded areas under ironwood trees</li>
<li><strong>Best For:</strong> <strong>All skill levels</strong> &mdash; The Kahana River is calm and protected. The bay itself can have surf &mdash; stay in the river if ocean conditions are rough.</li>
<li><strong>Launch Notes:</strong> Launch from the beach at the river mouth and paddle upstream into the Kahana rainforest valley. Our <a href="../activities/rainforest-oahu-kayak-tour.html">Kahana Rainforest River self-guided tour</a> uses this launch.</li>
</ul>

<h2>Drive Time Summary</h2>
<ul>
<li><strong>Kailua Beach Park:</strong> 5 min</li>
<li><strong>He&#699;eia Kea Pier:</strong> 20 min</li>
<li><strong>Kualoa Beach Park:</strong> 25 min</li>
<li><strong>Kahana Bay:</strong> 40 min</li>
<li><strong>Hale&#699;iwa:</strong> 50 min</li>
</ul>

<p><strong>Need equipment?</strong> <a href="../rentals/">Browse our kayak rentals</a> or <a href="../contact-us.html">contact us</a> for recommendations based on your skill level and preferred launch point.</p>"""
    },
    # PAGE 3: Kayak Safety Guide
    {
        "slug": "kayak-safety-guide",
        "title": "Oahu Kayak Safety Guide \u2014 Conditions, Tides & Emergency Info | Active Oahu",
        "description": "Essential safety information for kayaking on Oahu. Wind conditions, tide charts, what to do if you capsize, emergency contacts, and when NOT to go out.",
        "h1": "Oahu Kayak Safety Guide \u2014 Conditions, Tides &amp; Emergency Info",
        "body": """<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:6px;padding:15px;margin:20px 0;">
<p style="margin:0;"><strong>&#9888; Disclaimer:</strong> This information is for <em>private recreational boaters</em>. Always assess conditions at the launch site. Conditions can change rapidly. If in doubt, don't go out.</p>
</div>

<h2>Wind Conditions on Oahu</h2>
<p>Oahu's tradewinds blow from the northeast <strong>15&ndash;25 mph</strong> most days, strongest between 11 AM and 4 PM. Understanding wind patterns is the single most important factor for a safe paddle.</p>

<h3>Windward Side (Kailua, Kaneohe, Kualoa)</h3>
<ul>
<li><strong>Morning (6&ndash;10 AM):</strong> Light winds, 5&ndash;10 mph &mdash; ideal for paddling</li>
<li><strong>Midday (11 AM&ndash;3 PM):</strong> Tradewinds build to 15&ndash;25 mph with gusts to 30+ mph &mdash; can create challenging chop and make return paddles difficult</li>
<li><strong>Late Afternoon (3 PM&ndash;sunset):</strong> Winds gradually ease</li>
</ul>

<h3>North Shore (Hale&#699;iwa, Sharks Cove)</h3>
<ul>
<li><strong>Summer (May&ndash;October):</strong> Flat to 2&ndash;3 ft waves &mdash; generally safe for kayaking and snorkeling</li>
<li><strong>Winter (November&ndash;April):</strong> 10&ndash;30+ ft waves &mdash; <strong>DO NOT kayak the North Shore in winter</strong></li>
</ul>

<h2>Tide Charts &amp; Why They Matter</h2>
<p>Tides on Oahu are semi-diurnal (two high and two low tides daily). The range is typically 1&ndash;2 feet.</p>

<ul>
<li><strong>Kaneohe Sandbar:</strong> Best at low-to-mid tide when sand is exposed. At high tide the sandbar is underwater. Check <a href="https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=1612480" target="_blank" rel="noopener">NOAA tide predictions for Kaneohe Bay</a>.</li>
<li><strong>Kailua Bay:</strong> Less tide-dependent. The barrier reef protects the bay regardless of tide level.</li>
<li><strong>Mokoli&#699;i (Chinaman's Hat):</strong> Best at mid-to-high tide for deeper water over the reef shelf. At extreme low tide you may scrape bottom.</li>
</ul>

<p>Check <a href="https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=1612340" target="_blank" rel="noopener">NOAA tide predictions for the main Hawaiian Islands</a> before your trip.</p>

<h2>What to Do If You Capsize</h2>
<p>Capsizing in a sit-on-top kayak is rare but possible, especially in windy conditions or crossing boat wakes. Here's what to do:</p>

<ol>
<li><strong>Stay calm.</strong> Your PFD will keep you afloat. Take a breath and assess the situation.</li>
<li><strong>Stay with your kayak.</strong> Never abandon your kayak to swim to shore. A capsized kayak is visible and provides flotation.</li>
<li><strong>Flip the kayak right-side up.</strong> Reach across the hull and pull the far edge toward you.</li>
<li><strong>Re-enter from the side.</strong> Kick your legs to propel yourself up onto the kayak, then swing your legs back on. Practice this at the shop before launching.</li>
<li><strong>Retrieve your paddle.</strong> Your paddle has a leash &mdash; reel it in. If it drifts away, paddle with your hands back to the kayak.</li>
<li><strong>Secure loose items.</strong> Check that your dry bag is still attached. Retrieve floating items if safe to do so.</li>
</ol>

<h2>Emergency Contacts</h2>
<p>Save these numbers before your paddle:</p>

<ul>
<li><strong>Emergency (Police, Fire, Ambulance):</strong> <a href="tel:911">911</a></li>
<li><strong>Honolulu Fire Department Ocean Safety:</strong> <a href="tel:808-723-7867">(808) 723-7867</a></li>
<li><strong>U.S. Coast Guard Sector Honolulu:</strong> <a href="tel:808-842-2600">(808) 842-2600</a> or VHF Channel 16</li>
<li><strong>Active Oahu Shop:</strong> <a href="tel:808-498-1894">(808) 498-1894</a></li>
<li><strong>DLNR Division of Conservation and Resources Enforcement (DOCARE):</strong> <a href="tel:808-587-0077">(808) 587-0077</a> &mdash; for marine wildlife emergencies</li>
</ul>

<h2>When NOT to Go Out</h2>
<p>Do not launch if any of these conditions are present:</p>

<ul>
<li><strong>Wind advisory or small craft advisory</strong> in effect &mdash; check <a href="https://www.weather.gov/hfo/" target="_blank" rel="noopener">NWS Honolulu</a></li>
<li><strong>North Shore winter swell</strong> (November&ndash;April) &mdash; waves exceed safe limits for recreational kayaking</li>
<li><strong>Thunderstorms or lightning</strong> visible or forecast</li>
<li><strong>Brown water advisories</strong> after heavy rain &mdash; runoff carries bacteria and debris</li>
<li><strong>High surf advisory</strong> for the coast you're launching from</li>
<li><strong>Jellyfish warnings</strong> &mdash; box jellyfish appear 8&ndash;10 days after a full moon on south and leeward shores</li>
<li><strong>You are alone</strong> &mdash; always paddle with a partner</li>
<li><strong>You feel unsure</strong> &mdash; if conditions don't feel right, trust your instincts. There's always another day.</li>
</ul>

<h2>Additional Safety Tips</h2>
<ul>
<li><strong>Tell someone your plan:</strong> Let a friend or family member know your launch point, destination, and expected return time.</li>
<li><strong>Wear your PFD:</strong> It's not enough to have it in the kayak &mdash; wear it at all times on the water. It's required by law for anyone under 13 and strongly recommended for everyone.</li>
<li><strong>Paddle into the wind first:</strong> Start your trip heading into the wind. You'll have the wind at your back on the return when you're tired.</li>
<li><strong>Stay close to shore:</strong> In Kailua Bay, stay inside the reef line. In open water, stay within 0.5 miles of shore.</li>
<li><strong>Hydrate:</strong> Bring more water than you think you need. The combination of sun, salt, and exertion accelerates dehydration.</li>
<li><strong>Watch for boats:</strong> Kaneohe Bay has significant boat traffic, especially on weekends. Stay visible and yield to larger vessels.</li>
</ul>

<p><strong>Questions about conditions?</strong> <a href="../contact-us.html">Contact us</a> before your rental &mdash; we monitor conditions daily and can advise on the best launch point and time for your trip.</p>"""
    },
    # PAGE 4: About Active Oahu
    {
        "slug": "about-active-oahu",
        "title": "About Active Oahu \u2014 Kailua's Local Kayak & Beach Gear Shop | Active Oahu",
        "description": "Meet Michael Gulden, owner of Active Oahu since 2023. Kailua's community-focused kayak and beach gear shop at 134B Hamakua Dr. TripAdvisor award winner.",
        "h1": "About Active Oahu \u2014 Kailua's Local Kayak &amp; Beach Gear Shop",
        "body": """<h2>Welcome to Active Oahu</h2>
<p>Active Oahu is Kailua's local, community-focused kayak and beach gear outfitter. We're not a big tour conglomerate &mdash; we're a small, owner-operated shop that lives and breathes Oahu's windward coast. Our mission is simple: <strong>get you on the water with the right gear, the right information, and zero hassle.</strong></p>

<h2>Meet the Owner</h2>
<p><strong>Michael Gulden</strong> has been the owner of Active Oahu since 2023. A longtime windward Oahu resident and avid waterman, Michael took over the shop with a vision to create a <strong>self-serve, community-first rental experience</strong> that puts the adventure back in your hands. Under his leadership, Active Oahu has expanded its rental fleet, earned a TripAdvisor Travelers' Choice Award, and become the go-to outfitter for kayakers exploring Kailua Bay, Kaneohe Bay, and beyond.</p>

<p>Michael and his team believe that the best Hawaii experiences aren't the ones you're shuttled through on a bus &mdash; they're the ones you discover on your own, at your own pace, with the right equipment and local knowledge to back you up.</p>

<h2>Our Shop</h2>
<p>Visit us at our Kailua storefront:</p>
<p><strong>134B Hamakua Drive<br>Kailua, HI 96734</strong></p>
<p>We're located in the heart of Kailua, just minutes from Kailua Beach Park and Lanikai Beach. Our shop is your activity hub &mdash; stop by to pick up your rental gear, get local tips from our team, and start your adventure.</p>

<h2>The Self-Serve Model</h2>
<p>What sets Active Oahu apart is our <strong>self-serve approach</strong>. Here's how it works:</p>
<ol>
<li><strong>Book online:</strong> Reserve your kayak, snorkel gear, or beach equipment through our website.</li>
<li><strong>Pick up at our shop:</strong> Come to 134B Hamakua Dr. We'll have everything ready. Our team provides on-site instruction, route recommendations, and safety briefings.</li>
<li><strong>Transport your gear:</strong> We provide soft racks and tie-down straps that fit most 4-door vehicles. Load up and drive to your chosen launch point.</li>
<li><strong>Explore on your terms:</strong> Paddle, snorkel, and discover at your own pace. No guide, no schedule, no group to wait for.</li>
<li><strong>Return:</strong> Bring the gear back to the shop by your return time. Easy.</li>
</ol>
<p>This model keeps costs down and flexibility up. You get the freedom of a rental with the support of a knowledgeable local team.</p>

<h2>Community Focus</h2>
<p>Active Oahu is deeply rooted in the Kailua and windward Oahu community. We:</p>
<ul>
<li>Support local beach clean-up efforts and conservation initiatives</li>
<li>Promote reef-safe practices and responsible tourism</li>
<li>Partner with local businesses for multi-day rental logistics</li>
<li>Provide equipment and advice for community paddling events</li>
<li>Employ local guides and staff who know these waters intimately</li>
</ul>

<h2>Award-Winning Service</h2>
<p>Active Oahu is a proud <strong>TripAdvisor Travelers' Choice Award winner</strong>, placing us in the top 10% of attractions worldwide. This award is based entirely on guest reviews &mdash; people like you who paddled to the Mokulua Islands, snorkeled Sharks Cove, or explored the Kaneohe Sandbar and shared their experience.</p>
<p><a href="../ja/active-oahu-llc-wins-2022-tripadvisor-travelers-choice-award-for-tours-and-activities/index.html">Read our TripAdvisor Travelers' Choice Award press release</a></p>

<h2>What We Offer</h2>
<ul>
<li><strong>Kayak Rentals:</strong> Single and tandem sit-on-top ocean kayaks for daily and multi-day rentals</li>
<li><strong>Self-Guided Tours:</strong> Pre-planned routes to Mokoli&#699;i, the Mokulua Islands, Kaneohe Sandbar, Kahana Rainforest River, and Sharks Cove</li>
<li><strong>Guided Tours:</strong> Expert-led adventures including the Mokulua Islands Kayak &amp; E-Bike tour</li>
<li><strong>Beach Gear:</strong> Snorkel sets, stand-up paddleboards, coolers, anchors, rash guards, and more</li>
<li><strong>Multi-Day Rentals:</strong> Discounted rates for extended adventures</li>
</ul>

<p><a href="../rentals/">Browse all rentals</a> | <a href="../activities.html">View our tours</a></p>

<h2>Photo Gallery</h2>
<p>See our adventures in action! Browse photos from our guests and team on the water, on the islands, and exploring Oahu's best coastlines.</p>
<p><a href="../active-oahu-photo-gallery/index.html">Visit our photo gallery &rarr;</a></p>

<h2>Get in Touch</h2>
<ul>
<li><strong>Phone:</strong> <a href="tel:808-498-1894">(808) 498-1894</a></li>
<li><strong>Address:</strong> 134B Hamakua Dr., Kailua, HI 96734</li>
<li><strong>Online:</strong> <a href="../contact-us.html">Contact form</a></li>
</ul>

<p>Follow us on social media for daily conditions updates, adventure photos, and special offers:</p>
<ul>
<li><a href="https://www.facebook.com/activeoahutours/" target="_blank" rel="noopener">Facebook</a></li>
<li><a href="https://www.instagram.com/activeoahu/" target="_blank" rel="noopener">Instagram</a></li>
<li><a href="https://www.yelp.com/biz/active-oahu-tours-kailua" target="_blank" rel="noopener">Yelp</a></li>
<li><a href="https://www.tripadvisor.com/Attraction_Review-g60656-d5079465-Reviews-Active_Oahu_Tours-Laie_Oahu_Hawaii.html" target="_blank" rel="noopener">TripAdvisor</a></li>
</ul>"""
    }
]

print(f"Generating {len(pages)} informational pages...\n")

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
    
    # Add schema based on page type
    if p['slug'] == 'about-active-oahu':
        # Organization schema for the About page
        schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Active Oahu, LLC",
            "alternateName": "Active Oahu",
            "url": "https://activeoahutours.com/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "134B Hamakua Drive",
                "addressLocality": "Kailua",
                "addressRegion": "HI",
                "postalCode": "96734",
                "addressCountry": "US"
            },
            "telephone": "+1-808-498-1894",
            "description": "Kailua's local, community-focused kayak and beach gear outfitter. Owner-operated since 2023 by Michael Gulden. Self-serve rental model for Oahu kayaking adventures.",
            "sameAs": [
                "https://www.facebook.com/activeoahutours/",
                "https://www.instagram.com/activeoahu/",
                "https://twitter.com/activeoahutours",
                "https://www.yelp.com/biz/active-oahu-tours-kailua",
                "https://www.tripadvisor.com/Attraction_Review-g60656-d5079465-Reviews-Active_Oahu_Tours-Laie_Oahu_Hawaii.html"
            ],
            "award": "TripAdvisor Travelers' Choice Award"
        }
    else:
        # Article schema for the informational pages
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": p['title'].split(' | ')[0],
            "description": p['description'],
            "author": {
                "@type": "Organization",
                "name": "Active Oahu, LLC"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Active Oahu, LLC",
                "url": "https://activeoahutours.com/"
            }
        }
    
    schema_ld = f"<script type='application/ld+json'>{json.dumps(schema)}</script>"
    head = head.replace('</head>', f'{schema_ld}\n</head>')
    
    # Assemble page content
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
    
    print(f"  OK {p['slug']}/index.html ({len(page):,} chars)")

print(f"\nAll {len(pages)} informational pages created.")

#!/usr/bin/env python3
"""Generate 4 rental hub pages with Product schema + self-transport language."""
import os, json, re

SITE = "/home/ubuntu/work/active-oahu-tours-mirror/site"

# Read templates
with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()

# --- KBA-style check-in instructions block (reusable) ---
KBA_CHECKIN = """<div class="checkin-instructions" style="background:#f0f7fa;border-left:4px solid #069;padding:20px;margin:25px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#069;">&#128205; KBA-Style Self-Serve Check-In Instructions</h3>
<p><strong>Step 1 — Book Online:</strong> Reserve your gear through our <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes" target="_blank" rel="noopener">online booking system</a>. You'll receive a confirmation email with your pickup time slot.</p>
<p><strong>Step 2 — Arrive at Our Shop:</strong> Come to <strong>134B Hamakua Dr, Kailua, HI 96734</strong> at your scheduled time. Look for the Active Oahu signs — we're in the Kailua Beach Center complex, just 2 minutes from Kailua Beach Park.</p>
<p><strong>Step 3 — Check In & Sign Waiver:</strong> Our staff will greet you, verify your reservation, and have you sign a digital waiver. Bring a valid ID and the credit card used for booking.</p>
<p><strong>Step 4 — Gear Fitting & Instruction:</strong> We'll fit you with properly sized life vests, paddles, and seat backs. You'll receive a <strong>5-10 minute orientation</strong> covering: route tips, safety zones, tide conditions, and how to secure gear to your vehicle.</p>
<p><strong>Step 5 — Load Up & Go:</strong> We provide <strong>foam pads and heavy-duty straps</strong> that fit any 4-door vehicle. Our team helps you load and secure the kayaks. If you have roof racks, even better — we'll get you set up in minutes.</p>
<p><strong>Step 6 — Adventure!</strong> Head to your destination with our waterproof route map. Our phone number is on the map — call us anytime during your rental with questions.</p>
<p><strong>Step 7 — Return:</strong> Bring gear back by your scheduled return time. We'll help you unload. Late returns may incur additional fees — call us if you're running behind.</p>
<p style="margin-bottom:0;"><em>&#9432; First time transporting a kayak? Read our <a href="/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/">Kayak Transport Guide</a> before you arrive.</em></p>
</div>"""

# ============================================================
# PAGE 1: /kayak-rentals/
# ============================================================
kayak_body = """
<h2>Oahu's Best Kayak Rentals — Pick Up in Kailua, Explore the Whole Island</h2>
<p>Active Oahu is Oahu's top-rated kayak outfitter, based in <strong>Kailua on the Windward Coast</strong>. We rent premium sit-on-top ocean kayaks — singles and tandems — with everything included: life vest, paddle, seat back, dry bag, and <strong>free foam pads + straps for transport</strong> on any 4-door vehicle.</p>
<p>Unlike other rental shops that limit you to Kailua Bay only, our kayaks are <strong>built for self-transport</strong>. Pick up at our shop, load up with our soft racks, and paddle wherever the island calls you.</p>

<h2>Kayak Rental Options & Pricing</h2>

<h3>Single Kayak — $45 (4 Hours) / $65 (Full Day)</h3>
<p>Our single sit-on-top kayaks are lightweight, stable, and perfect for solo adventurers. Great for experienced paddlers who want to go at their own pace. Includes: kayak, paddle, life vest (USCG approved), seat back, dry bag, and transport pads.</p>

<h3>Tandem Kayak — $65 (4 Hours) / $85 (Full Day)</h3>
<p>Our tandem kayaks seat two adults comfortably with room for a small cooler. The most popular choice for couples and friends. Same included gear as the single, plus two of everything. Tandem kayaks are more stable in ocean chop and track better on longer crossings.</p>

<h3>Multi-Day Kayak Rentals</h3>
<p>Going for 2-7 days? Check out our <a href="/multi-day-rentals/">Multi-Day Rental page</a> for discounted extended rates — keep the kayaks for your whole vacation.</p>

<h2>How Self-Transport Works</h2>
<div style="background:#fff8e1;border-left:4px solid #f0a030;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#cc7a00;">&#128663; Self-Transport Block</h3>
<p><strong>Pick up at 134B Hamakua Dr, Kailua, HI 96734.</strong> We provide heavy-duty foam pads and cam-lock straps that fit any 4-door vehicle — sedans, SUVs, trucks, and minivans. No roof rack needed. Our team loads and secures your kayak in under 5 minutes.</p>
<p>If your vehicle has <strong>factory or aftermarket roof racks</strong>, we'll use rigid rack adapters for an even faster, more secure fit. Either way, you're ready to drive to any launch point on Oahu.</p>
<p><strong>Read our full guide:</strong> <a href="/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/">How to Transport Kayaks from Our Kailua Shop</a></p>
</div>

<h2>Popular Kayak Destinations from Our Shop</h2>

<h3>&#127754; Mokulua Islands (The Mokes) — Kailua Bay</h3>
<p>The classic: paddle 1 mile across turquoise Kailua Bay to the twin islands. Land on Moku Nui's protected beach, explore tide pools, and find Queens Bath — a natural saltwater pool on the island's back side. <strong>Launch from Kailua Beach Park boat ramp</strong> (2 minutes from our shop). <em>Beginners welcome in calm conditions.</em></p>

<h3>&#127745; Chinaman's Hat (Mokoli'i) — Kualoa</h3>
<p>Just 500 yards offshore from Kualoa Regional Park, this cone-shaped island is Oahu's shortest and most rewarding kayak trip. Paddle across shallow reef (knee-to-waist deep), land on the small beach, and hike 15 minutes to the summit for <strong>360\u00b0 views of Kaneohe Bay</strong>. <em>~30 minute drive from our shop.</em></p>

<h3>&#127965; Kaneohe Sandbar (Ahu o Laka)</h3>
<p>Paddle 1.5 miles across protected Kaneohe Bay to Hawaii's "floating beach" — a sunken reef that emerges at low tide. Anchor your kayak and wade in waist-deep turquoise water surrounded by the Ko'olau Mountains. <em>~25 minute drive; launch from He'eia Kea Pier.</em></p>

<h3>&#129343; Sharks Cove — North Shore</h3>
<p>Combine your kayak rental with our snorkel gear and paddle the calm summer waters of Oahu's North Shore. Sharks Cove is rated <strong>one of the top 12 shore dives in the world</strong>. Launch from the cove itself or nearby Waimea Bay. <em>~50 minute drive; summer only (May-October).</em></p>

<h2>What's Included with Every Kayak Rental</h2>
<ul>
<li><strong>Sit-on-top ocean kayak</strong> — stable, self-bailing, easy to re-enter</li>
<li><strong>USCG-approved life vest</strong> — properly fitted at check-in</li>
<li><strong>Adjustable paddle with leash</strong></li>
<li><strong>Padded seat back</strong> for all-day comfort</li>
<li><strong>Waterproof dry bag</strong> for phone, keys, and snacks</li>
<li><strong>Foam pads + heavy-duty cam-lock straps</strong> for vehicle transport</li>
<li><strong>Waterproof route map</strong> with GPS coordinates and safety tips</li>
<li><strong>On-site orientation and loading assistance</strong></li>
<li><strong>Emergency phone support</strong> during your rental</li>
</ul>

<h2>Kayak Rental FAQ</h2>

<h3>Do I need kayaking experience?</h3>
<p>Our sit-on-top kayaks are beginner-friendly and stable. For first-timers, we recommend Kailua Bay (protected by Oahu's largest barrier reef) or Chinaman's Hat (shallow, short paddle). We provide a thorough orientation at check-in, and our waterproof route maps highlight safe zones. If you're unsure, call us at (808) 498-1894 — we'll help you pick the right destination.</p>

<h3>What kind of vehicle do I need to transport a kayak?</h3>
<p><strong>Any 4-door vehicle works.</strong> We provide foam pads that sit on your roof and cam-lock straps that thread through your door openings (not the windows — the actual door frames). Sedans, SUVs, trucks, minivans — all good. 2-door vehicles can work but are trickier; call us first. Read our <a href="/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/">transport guide</a> for detailed instructions.</p>

<h3>Can I bring a cooler?</h3>
<p>Yes! Our tandem kayaks have room for a small soft-sided cooler. We recommend packing water (at least 1 liter per person), sunscreen (reef-safe please!), and snacks. No glass containers on the beach.</p>

<h3>What if the weather is bad?</h3>
<p>We monitor conditions daily. If small craft advisories or dangerous surf are forecast, we'll contact you to reschedule or cancel with a full refund. Safety is our priority.</p>

<h3>Can I add snorkel gear?</h3>
<p>Absolutely. Add a snorkel set (mask, fins, snorkel) for $15/day. Perfect for the Mokes, Sharks Cove, or Kaneohe Sandbar. See our <a href="/beach-gear-rentals/">Beach Gear Rentals</a> page for more add-ons.</p>

<h2>Why Rent from Active Oahu?</h2>
<ul>
<li><strong>Tripadvisor Travelers' Choice 2022</strong> — Top 10% of attractions worldwide</li>
<li><strong>2 minutes from Kailua Beach</strong> — the closest outfitter to the best launch point on Oahu</li>
<li><strong>Premium gear, maintained daily</strong> — our kayaks are washed, inspected, and sun-protected after every rental</li>
<li><strong>Real local knowledge</strong> — our team paddles these routes weekly. We know the tides, winds, and hidden spots</li>
<li><strong>Self-transport freedom</strong> — not locked into one beach. Take your kayak anywhere on Oahu</li>
<li><strong>5-star rated</strong> on Google, Yelp, and Tripadvisor — read our <a href="/reviews/">reviews</a></li>
</ul>

<p><strong>Ready to paddle?</strong> <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#069;color:#fff;text-decoration:none;border-radius:4px;font-weight:bold;">Book Your Kayak Rental &rarr;</a></p>
"""

# ============================================================
# PAGE 2: /multi-day-rentals/
# ============================================================
multiday_body = """
<h2>Multi-Day Kayak & Beach Gear Rentals — Explore Oahu at Your Own Pace</h2>
<p>Why rush? With Active Oahu's <strong>multi-day rental packages</strong>, you keep your kayaks, snorkel gear, and beach equipment for <strong>2 to 7 days</strong>. Drive to a new destination every morning. Paddle when conditions are perfect. No daily pickup, no daily return — just one checkout and you're equipped for your entire vacation.</p>
<p>Multi-day rentals are our most popular option for visitors staying on the Windward Coast, North Shore, or anywhere on Oahu with a rental car. <strong>Save up to 40% vs. booking single days.</strong></p>

<h2>Multi-Day Pricing</h2>

<h3>Kayak Rentals — Multi-Day</h3>
<ul>
<li><strong>Single Kayak:</strong> $65 first day + $40 each additional day</li>
<li><strong>Tandem Kayak:</strong> $85 first day + $55 each additional day</li>
<li><strong>Example — 3-Day Tandem:</strong> $85 + $55 + $55 = $195 (vs. $255 booking 3 single days — save $60!)</li>
</ul>

<h3>Beach Gear Bundles — Multi-Day</h3>
<ul>
<li><strong>Full Beach Setup (2 chairs, umbrella, cooler, snorkel set):</strong> $45/day, $35/day for 3+ days</li>
<li><strong>Snorkel Set (mask, fins, snorkel):</strong> $15/day, $10/day for 3+ days</li>
<li><strong>Stand-Up Paddleboard:</strong> $55/day, $40/day for 3+ days</li>
</ul>

<h3>Ultimate Oahu Explorer Package</h3>
<p><strong>1 Tandem Kayak + Full Beach Setup + Snorkel Set</strong> — everything you need for a week of adventuring:<br/>
2 Days: $230 | 3 Days: $310 | 5 Days: $430 | 7 Days: $540</p>

<h2>How Multi-Day Rentals Work</h2>
<div style="background:#e8f5e9;border-left:4px solid #2e7d32;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#2e7d32;">&#128197; Multi-Day Rental Process</h3>
<p><strong>Day 1 — Pickup at 134B Hamakua Dr:</strong> Same KBA check-in process as daily rentals. We fit your gear, load your vehicle with our foam pads and straps, and send you off with route maps for every major Oahu kayak destination.</p>
<p><strong>Days 2-6 — Keep the Gear:</strong> The kayak stays on your vehicle or at your accommodation. Keep going to new spots each day — Chinaman's Hat one morning, Kaneohe Sandbar the next, Sharks Cove mid-week. The island is yours.</p>
<p><strong>Final Day — Return:</strong> Bring everything back by your scheduled time. We'll help unload and inspect the gear. Simple.</p>
</div>

<h2>Self-Transport & Storage Tips for Multi-Day Rentals</h2>
<div style="background:#fff8e1;border-left:4px solid #f0a030;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#cc7a00;">&#128663; Multi-Day Transport & Storage Guide</h3>
<p><strong>Overnight storage:</strong> If your accommodation has a ground-floor patio, yard, or dedicated parking, you can leave the kayak strapped to your vehicle or unstrap and store it. Most vacation rentals on the Windward side are kayak-friendly — ask your host. If you're in a condo or hotel, let your vehicle serve as your storage rack; our foam pads and straps keep the kayak secure overnight.</p>
<p><strong>Driving with kayaks:</strong> Our strap system is secure for highway speeds. Check strap tension before each drive — nylon straps can loosen slightly as they settle. A quick 30-second re-tighten takes care of it.</p>
<p><strong>Sun protection:</strong> Oahu's UV is intense. Between uses, we recommend covering the kayak with a tarp or beach towel if it'll sit in direct sun for hours. The kayaks are UV-resistant but prolonged exposure shortens gear life.</p>
<p><strong>Security:</strong> Kayaks are difficult to steal when strapped to a vehicle, but we recommend parking in visible, well-lit areas. If removing the kayak from your vehicle, use a cable lock (available as an add-on for $5/day).</p>
<p><strong>Washing:</strong> Rinse the kayak and gear with fresh water after saltwater use. Most vacation rentals have a hose — a quick rinse prevents salt buildup. We do a deep clean when you return.</p>
</div>

<h2>Sample Multi-Day Itineraries</h2>

<h3>3-Day Windward Explorer</h3>
<ul>
<li><strong>Day 1:</strong> Chinaman's Hat (Mokoli'i) — short paddle + summit hike. Lunch in Kualoa. Afternoon at Kualoa Beach Park.</li>
<li><strong>Day 2:</strong> Kaneohe Sandbar — low tide morning session. Anchor up, wade, snorkel. Pack a floating picnic.</li>
<li><strong>Day 3:</strong> Kailua Bay to Mokulua Islands — the classic. Full morning on Moku Nui. Afternoon swim at Lanikai Beach.</li>
</ul>

<h3>5-Day Ultimate Oahu Paddler</h3>
<ul>
<li><strong>Day 1:</strong> Chinaman's Hat — ease in with the shortest paddle</li>
<li><strong>Day 2:</strong> Kaneohe Sandbar — mid-week, catch low tide</li>
<li><strong>Day 3:</strong> Rest / beach day — use your beach gear at Kailua or Lanikai</li>
<li><strong>Day 4:</strong> Mokulua Islands — the bucket-list paddle</li>
<li><strong>Day 5:</strong> North Shore — Sharks Cove kayak + snorkel combo (summer only)</li>
</ul>

<h3>7-Day Full Island Expedition</h3>
<p>All of the above, plus: Kahana River rainforest paddle (calm river, jungle scenery), Popoia Island (Flat Island) from Kailua Beach, and a bonus snorkel day at Hanauma Bay (separate reservation required). With a full week, you can paddle every major kayak destination on Oahu — at your own pace, on your own schedule.</p>

<h2>Multi-Day Rental FAQ</h2>

<h3>Is there a deposit for multi-day rentals?</h3>
<p>We place a hold on your credit card for the retail value of the gear, released upon return in good condition. This is standard across all kayak outfitters on Oahu.</p>

<h3>Can I extend my rental mid-trip?</h3>
<p>Usually yes — call us at (808) 498-1894. If the gear isn't reserved by another customer, we're happy to extend at the multi-day rate. During peak seasons (December-January, June-August), extensions may not be available, so book your full window upfront.</p>

<h3>What if gear gets damaged?</h3>
<p>Normal wear and tear is expected and covered. Accidental damage (dropping a kayak, losing a paddle) may incur a repair/replacement fee. We inspect all gear at check-in and return — you're only responsible for damage beyond normal use.</p>

<h3>Can I get multi-day pricing on just beach gear (no kayak)?</h3>
<p>Absolutely. See our <a href="/beach-gear-rentals/">Beach Gear Rentals</a> page for full pricing on chairs, umbrellas, snorkel sets, coolers, and SUP boards. Multi-day discounts apply to all gear categories.</p>

<h3>Where can I store gear at my rental?</h3>
<p>Most Windward-side vacation rentals have outdoor space. If you're in Waikiki, storage can be tighter — call us to discuss. Some customers keep gear in their rental vehicle; our foam pads make daily loading/unloading quick.</p>

<p><strong>Ready to commit to a multi-day adventure?</strong> <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#069;color:#fff;text-decoration:none;border-radius:4px;font-weight:bold;">Book Your Multi-Day Rental &rarr;</a></p>
"""

# ============================================================
# PAGE 3: /electric-bike-rentals/
# ============================================================
ebike_body = """
<h2>Electric Bike Rentals — Explore Kailua, Lanikai & Beyond</h2>
<p>Active Oahu's <strong>electric bike rentals</strong> are the best way to explore Oahu's Windward Coast. Cruise effortlessly through Kailua Town, along Lanikai's beachfront loop, up to the Pillbox Hike trailhead, or all the way to Waimanalo Beach. Our pedal-assist e-bikes flatten hills and extend your range — you'll see more with less effort.</p>
<p>Every rental includes a helmet, lock, route map, and a full orientation. Pick up at <strong>134B Hamakua Dr, Kailua</strong> — same location as our kayak shop.</p>

<h2>E-Bike Rental Options & Pricing</h2>

<h3>Standard E-Bike — $55 (4 Hours) / $75 (Full Day)</h3>
<p>Comfortable step-through frame, 5 levels of pedal assist, throttle option for easy starts. Range: <strong>25-40 miles</strong> depending on assist level and terrain. Perfect for Kailua-Lanikai loops and the Pillbox trailhead.</p>

<h3>Premium E-Bike — $75 (4 Hours) / $95 (Full Day)</h3>
<p>Extended range battery (40-60 miles), upgraded suspension, hydraulic disc brakes. Ideal for longer rides to Waimanalo, Makapu'u, or the full Windward Coast route. Includes phone mount and USB charging port.</p>

<h3>Multi-Day E-Bike — $65/day (2+ days)</h3>
<p>Keep the e-bike for your full stay. Ride to breakfast in Kailua every morning, or use it as your primary transportation around the Windward side.</p>

<h2>E-Bike Range & Capabilities</h2>
<div style="background:#e3f2fd;border-left:4px solid #1565c0;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#1565c0;">&#9889; E-Bike Specs & Range</h3>
<ul>
<li><strong>Motor:</strong> 500W rear hub (Standard) / 750W mid-drive (Premium)</li>
<li><strong>Battery:</strong> 48V 14Ah lithium-ion — fully charged at pickup</li>
<li><strong>Range (Standard):</strong> 25-40 miles per charge (varies by assist level, rider weight, wind, and elevation)</li>
<li><strong>Range (Premium):</strong> 40-60 miles per charge</li>
<li><strong>Top speed:</strong> 20 mph (pedal assist) / 20 mph (throttle) — Class 2 e-bike compliant with Hawaii law</li>
<li><strong>Charging:</strong> Full charge in 4-6 hours. Charger included with multi-day rentals</li>
<li><strong>Weight capacity:</strong> 300 lbs</li>
</ul>
</div>

<h2>Self-Transport for E-Bikes</h2>
<div style="background:#fff8e1;border-left:4px solid #f0a030;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#cc7a00;">&#128663; Transporting Your E-Bike</h3>
<p>E-bikes are <strong>ride-away ready</strong> — pick up at 134B Hamakua Dr and start riding immediately. No vehicle transport needed for local rides.</p>
<p><strong>Want to take e-bikes to another part of the island?</strong> We can help load them into a truck bed or onto a hitch-mounted bike rack. E-bikes are heavier than regular bikes (~55 lbs each), so a proper rack is essential. If your vehicle has a 2" hitch receiver, we recommend bringing a tray-style rack rated for e-bike weight. Our team can assist with loading.</p>
<p><strong>Multi-day renters:</strong> The e-bike fits in most SUVs and minivans with seats folded. We'll help you load at pickup.</p>
</div>

<h2>Best E-Bike Routes from Kailua</h2>

<h3>&#128692; Kailua-Lanikai Loop (6 miles, Easy)</h3>
<p>The classic Windward ride. Start at our shop, cruise through Kailua Town, then ride the Lanikai loop past multi-million dollar beachfront homes with the Mokulua Islands as your backdrop. Stop at Lanikai Beach for a swim. Flat, paved, and mostly on quiet residential streets. <strong>45 minutes to 1.5 hours with stops.</strong></p>

<h3>&#9968; Pillbox Hike Trailhead + Coastal Loop (8 miles, Moderate)</h3>
<p>Ride from our shop to the Lanikai Pillbox (Ka'iwa Ridge) trailhead. Lock your bike at the base, hike 20-30 minutes up for <strong>jaw-dropping sunrise views</strong> over the Mokulua Islands and Kailua Bay. Then continue along the coast toward Bellows Beach. Some moderate hills — that's where the e-bike shines. <strong>2-3 hours total.</strong></p>

<h3>&#127754; Kailua to Waimanalo Beach (14 miles round trip, Moderate)</h3>
<p>Ride south along Kalaniana'ole Highway (bike lane available) to Waimanalo Beach — consistently rated one of Oahu's most beautiful stretches of sand. Stop at Waimanalo Beach Park for a swim, then ride back. The e-bike's pedal assist makes the gentle incline on the return effortless. <strong>2-3 hours with beach time.</strong></p>

<h3>&#128293; Makapu'u Point & Tide Pools (22 miles round trip, Challenging)</h3>
<p>For ambitious riders: continue past Waimanalo to Makapu'u. Lock at the lookout trailhead, hike to the lighthouse viewpoint, then descend to the tide pools (wear water shoes). The Premium e-bike is recommended for this route due to the elevation gain. Pack water and sunscreen. <strong>4-5 hours round trip.</strong></p>

<h3>&#127965; Kailua to Kaneohe via Old Pali Road (18 miles, Moderate-Advanced)</h3>
<p>A scenic backroads route connecting Kailua to Kaneohe Town. Ride through quiet residential streets, past Kawainui Marsh (Hawaii's largest wetland), and into Kaneohe for lunch. Return via the same route or loop through the H-3 bike path connector. <strong>3-4 hours.</strong></p>

<h2>What's Included</h2>
<ul>
<li><strong>Pedal-assist electric bike</strong> — fully charged, tuned, and cleaned</li>
<li><strong>Helmet</strong> — properly fitted at check-in (required by Hawaii law for riders under 16; strongly recommended for all)</li>
<li><strong>U-lock + cable</strong> — secure your bike at stops</li>
<li><strong>Waterproof route map</strong> with turn-by-turn directions for all routes above</li>
<li><strong>Phone mount & USB charger</strong> (Premium only)</li>
<li><strong>Charger</strong> — included with full-day and multi-day rentals</li>
<li><strong>Orientation:</strong> 5-minute tutorial on controls, assist levels, and local road rules</li>
</ul>

<h2>E-Bike Rules & Safety</h2>
<ul>
<li><strong>Hawaii e-bike law:</strong> Class 2 e-bikes are legal on roads and bike paths. Helmets required for riders under 16.</li>
<li><strong>Sidewalks:</strong> Riding on sidewalks is prohibited in business districts; use bike lanes or the road.</li>
<li><strong>Beach paths:</strong> E-bikes are allowed on paved paths but NOT on sand. Lock at bike racks before walking onto beaches.</li>
<li><strong>Alcohol:</strong> Zero tolerance — same DUI laws as motor vehicles.</li>
<li><strong>Night riding:</strong> E-bikes have integrated headlights and taillights. If riding after sunset, use lights and wear reflective gear.</li>
</ul>

<h2>E-Bike Rental FAQ</h2>

<h3>Do I need a driver's license?</h3>
<p>Yes — e-bike renters must be 18+ with a valid driver's license. Riders 16-17 may ride as passengers on a tandem booking with a licensed adult.</p>

<h3>What happens if the battery dies mid-ride?</h3>
<p>E-bikes still function as regular bicycles without assist — you can pedal home. But with our route recommendations, you shouldn't come close to the range limits. If you do run out unexpectedly, call us at (808) 498-1894 and we'll coordinate a pickup.</p>

<h3>Can I ride to the North Shore?</h3>
<p>It's technically possible (~35 miles one way) but not recommended for a rental. The highways get narrow, and there are significant elevation changes. Stick to the Windward Coast routes — they're safer and more scenic.</p>

<h3>Are e-bikes allowed on the Lanikai Pillbox hike?</h3>
<p>Bikes (including e-bikes) are NOT allowed on the hiking trail itself. Lock your bike at the trailhead at Kaelepulu Drive and hike up. The trailhead is only a 10-minute ride from our shop.</p>

<h3>Can I combine e-bikes with kayak rentals?</h3>
<p>Yes! Our <strong>Guided Mokulua Islands Kayak & E-Bike Adventure</strong> combines both. For self-guided, book separately and we'll coordinate your schedule so you can ride in the morning and paddle in the afternoon. See our <a href="/activities/">Activities page</a>.</p>

<p><strong>Ready to ride?</strong> <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#069;color:#fff;text-decoration:none;border-radius:4px;font-weight:bold;">Book Your E-Bike Rental &rarr;</a></p>
"""

# ============================================================
# PAGE 4: /beach-gear-rentals/
# ============================================================
beach_body = """
<h2>Oahu Beach Gear Rentals — Everything You Need for a Perfect Beach Day</h2>
<p>Don't pack a beach load onto your flight. Active Oahu rents <strong>premium beach gear</strong> — snorkel sets, beach chairs, umbrellas, coolers, and more — at affordable daily and multi-day rates. Pick up at <strong>134B Hamakua Dr, Kailua</strong> and head to any beach on Oahu.</p>
<p>Whether you're snorkeling at Sharks Cove, sunbathing at Lanikai, or setting up a family camp at Kailua Beach Park, we've got the gear. <strong>Combine with kayak rentals for the ultimate Oahu beach day.</strong></p>

<h2>Beach Gear Rental Options & Pricing</h2>

<h3>&#129343; Snorkel Set — $15/day ($10/day for 3+ days)</h3>
<p>Premium dry-top snorkel, tempered-glass mask (anti-fog treated), and adjustable open-heel fins. Available in sizes XS through XL. We fit your mask at check-in — no leaks, no fog. Each set is sanitized after every rental.</p>
<p><strong>Popular snorkel spots:</strong> Sharks Cove (North Shore), Hanauma Bay (separate reservation required), Kuilima Cove (Turtle Bay), Kahe Point (Electric Beach).</p>

<h3>&#127965; Beach Chair — $10/day ($7/day for 3+ days)</h3>
<p>Lightweight aluminum frame, 4-position recline, padded armrests, cup holder. Weighs ~7 lbs. Folds flat for easy transport in any vehicle.</p>

<h3>&#9730; Beach Umbrella — $12/day ($8/day for 3+ days)</h3>
<p>7.5 ft tilt umbrella with sand anchor. UPF 50+ UV protection. Sets up in 2 minutes. Essential for full-day beach sessions — Oahu's UV index regularly hits 11+ (extreme).</p>

<h3>&#129382; Cooler — $10/day ($7/day for 3+ days)</h3>
<p>28-quart insulated cooler with handle. Holds ~30 cans plus ice. Perfect for beach picnics, post-paddle refreshments, and keeping lunch cold all day. We can pre-fill with ice for $5.</p>

<h3>&#127754; Stand-Up Paddleboard (SUP) — $45/day ($35/day for 3+ days)</h3>
<p>11 ft all-around inflatable SUP with adjustable paddle, pump, leash, and backpack carry bag. Inflates in 5 minutes. Great for Kailua Bay, Kaneohe Bay, or any calm water. Includes life vest.</p>

<h3>&#127946; Bodyboard — $10/day ($7/day for 3+ days)</h3>
<p>42-inch foam bodyboard with leash. Perfect for Waimanalo Beach, Sandy Beach, or Makapu'u (experienced riders only at Sandy's — shore break is powerful).</p>

<h3>&#127748; Full Beach Setup Package — $35/day ($25/day for 3+ days)</h3>
<p>2 beach chairs + 1 umbrella + 1 cooler. Everything you need for a comfortable beach camp. <strong>Add a snorkel set for +$10.</strong></p>

<h2>Beach Gear Transport</h2>
<div style="background:#fff8e1;border-left:4px solid #f0a030;padding:20px;margin:20px 0;border-radius:4px;">
<h3 style="margin-top:0;color:#cc7a00;">&#128663; Transporting Your Beach Gear</h3>
<p>All beach gear fits in <strong>any vehicle</strong> — sedan, SUV, convertible, or truck. Chairs and umbrellas fold flat. The cooler fits in a trunk or back seat. Snorkel sets come in mesh carry bags.</p>
<p>If you're also renting kayaks, everything loads together — chairs and umbrellas strap to the roof alongside your kayak, or tuck into your back seat. Our team helps you pack efficiently at pickup.</p>
<p><strong>Heading to a beach without your own car?</strong> Kailua Beach Park and Lanikai Beach are walking distance from our shop (10-15 minutes on foot). Many customers grab their gear and walk. For other beaches, we recommend having a vehicle.</p>
</div>

<h2>Snorkeling on Oahu — Where to Use Your Rental Gear</h2>

<h3>&#129343; Sharks Cove — North Shore (Summer Only)</h3>
<p>Consistently rated one of the <strong>top 12 shore dives in the world</strong>. Protected cove with 100+ fish species, frequent sea turtle sightings, and vibrant coral. Best May-October when the North Shore is flat. Winter brings massive waves — snorkel elsewhere. <em>~50 minute drive from our shop. Free parking (arrive by 8 AM).</em></p>

<h3>&#127754; Hanauma Bay — Southeast Shore</h3>
<p>Oahu's most famous snorkel destination. A protected marine life conservation district with calm, clear water. <strong>Important:</strong> Hanauma Bay requires a separate reservation (made 2 days in advance at 7 AM HST via the Honolulu Parks website). Entry fee: $25 per person. Our gear is perfect here — just book your Hanauma reservation separately. <em>~35 minute drive from our shop.</em></p>

<h3>&#127965; Kaneohe Sandbar</h3>
<p>When the sandbar emerges at low tide, the shallow water is perfect for snorkeling. Combine with a kayak rental to reach the sandbar, then snorkel the surrounding reef. Sea turtles frequent the area. <em>~25 minute drive; launch from He'eia Kea Pier.</em></p>

<h3>&#128031; Kuilima Cove — Turtle Bay, North Shore</h3>
<p>A sheltered cove at the Turtle Bay Resort. Shallow, calm, and beginner-friendly. Great for families and first-time snorkelers. Protected by a natural rock breakwater. <em>~55 minute drive from our shop.</em></p>

<h3>&#9889; Electric Beach (Kahe Point) — West Shore</h3>
<p>Named for the warm water outflow from the nearby power plant, which attracts abundant marine life. Advanced snorkelers only — entry can be challenging and there are no lifeguards. Spinner dolphins are frequently spotted here. <em>~50 minute drive from our shop.</em></p>

<h2>Best Beaches for Your Gear</h2>

<h3>&#127965; Kailua Beach Park</h3>
<p>3 miles of powdery white sand, consistently rated among the top 5 beaches in the United States. Protected by Oahu's largest barrier reef, so the water is calm year-round. Perfect for SUP, bodyboarding (gentle waves), and setting up your chairs + umbrella. <strong>2 minutes from our shop.</strong> Facilities: restrooms, showers, picnic tables, lifeguards.</p>

<h3>&#127754; Lanikai Beach</h3>
<p>Often photographed, always stunning. The Mokulua Islands sit just offshore, creating a postcard-perfect backdrop. Soft sand, turquoise water, and generally calm conditions. No facilities (no restrooms, no lifeguards) — that's why your cooler and umbrella matter here. <strong>10-15 minute walk from our shop.</strong> Street parking only; respect residential areas.</p>

<h3>&#127754; Waimanalo Beach</h3>
<p>Oahu's longest stretch of uninterrupted white sand. Less crowded than Kailua, with stunning views of the Ko'olau Mountains and offshore islands. Good bodyboarding. Facilities: restrooms, showers, lifeguards, plenty of parking. <em>~20 minute drive from our shop.</em></p>

<h3>&#127940; Sandy Beach</h3>
<p>Famous for its powerful shore break — a bodyboarding mecca. <strong>Experienced riders only.</strong> The waves break right on the sand; neck and back injuries are common. If you're a confident bodyboarder, this is Oahu's best. If you're a beginner, stick to Kailua or Waimanalo. <em>~25 minute drive from our shop.</em></p>

<h2>What's Included with Beach Gear Rentals</h2>
<ul>
<li>All gear is <strong>cleaned and sanitized</strong> between rentals</li>
<li><strong>Proper fitting</strong> at check-in (masks, fins)</li>
<li><strong>Setup instructions</strong> for umbrellas and SUPs</li>
<li><strong>Carry bags</strong> for snorkel sets and SUPs</li>
<li><strong>Safety briefing</strong> on ocean conditions and snorkeling tips</li>
<li>Option to <strong>pre-fill coolers with ice</strong> ($5)</li>
</ul>

<h2>Beach Gear Rental FAQ</h2>

<h3>Can I take snorkel gear to multiple beaches in one day?</h3>
<p>Absolutely! That's the beauty of renting — your gear goes wherever you go. Many customers snorkel Sharks Cove in the morning and then hit a sunset swim at Kailua or Lanikai.</p>

<h3>How do you sanitize snorkel gear?</h3>
<p>Every mask, snorkel, and set of fins is washed with antibacterial soap, rinsed thoroughly, and air-dried between rentals. Mask lenses are anti-fog treated. Mouthpieces are sanitized with food-grade sanitizer. We take hygiene seriously.</p>

<h3>Do I need reef-safe sunscreen?</h3>
<p><strong>Yes — and it's Hawaii law.</strong> Starting in 2021, Hawaii banned sunscreens containing oxybenzone and octinoxate, which damage coral reefs. Use only mineral-based sunscreens (zinc oxide or titanium dioxide). We sell reef-safe sunscreen at our shop if you need it.</p>

<h3>Can I rent gear without a reservation?</h3>
<p>Walk-ins are welcome but subject to availability. During peak seasons (summer and winter holidays), gear can sell out. We strongly recommend <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes">booking online</a> to guarantee your gear.</p>

<h3>What if I lose or damage something?</h3>
<p>We charge replacement cost for lost or significantly damaged items. Normal wear (minor scratches on fins, small scuffs) is expected and not charged. Our gear is durable, but the ocean can be unpredictable — if something happens, just let us know.</p>

<h3>Can I get a discount for large groups?</h3>
<p>Yes! Groups of 4 or more get <strong>15% off</strong> with code <strong>15OFFGROUPS</strong> at checkout. For groups of 8+, call us at (808) 498-1894 for custom pricing and coordinated pickup.</p>

<p><strong>Ready to hit the beach?</strong> <a href="https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&amp;from-ssl=yes" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#069;color:#fff;text-decoration:none;border-radius:4px;font-weight:bold;">Book Your Beach Gear &rarr;</a></p>
"""

# ============================================================
# 4 pages definition
# ============================================================
pages = [
    {
        "slug": "kayak-rentals",
        "title": "Oahu Kayak Rentals — Self-Serve Pickup in Kailua | Active Oahu",
        "description": "Rent single or tandem kayaks on Oahu with self-serve pickup at 134B Hamakua Dr, Kailua. Foam pads and straps included — fits any 4-door vehicle. Paddle the Mokulua Islands, Chinaman's Hat, Kaneohe Sandbar, or Sharks Cove.",
        "h1": "Oahu Kayak Rentals — Self-Serve Pickup in Kailua",
        "body": kayak_body,
        "product_name": "Oahu Kayak Rentals — Single & Tandem",
        "product_description": "Single and tandem sit-on-top ocean kayak rentals from Active Oahu. Self-serve pickup at 134B Hamakua Dr, Kailua. Includes life vest, paddle, seat back, dry bag, foam pads, and straps for transport on any 4-door vehicle.",
        "price_range": "$45-85",
        "low_price": "45",
        "high_price": "85",
        "price_currency": "USD",
    },
    {
        "slug": "multi-day-rentals",
        "title": "Multi-Day Kayak & Beach Gear Rentals — Oahu | Active Oahu",
        "description": "Keep your kayak and beach gear for 2–7 days. Explore Oahu at your own pace with discounted multi-day rates. Self-transport pickup at 134B Hamakua Dr, Kailua. Storage tips and sample itineraries included.",
        "h1": "Multi-Day Kayak & Beach Gear Rentals — Explore Oahu at Your Pace",
        "body": multiday_body,
        "product_name": "Multi-Day Kayak & Beach Gear Rentals",
        "product_description": "Multi-day kayak, snorkel, SUP, and beach gear rentals from Active Oahu in Kailua. Rent for 2-7 days with discounted rates. Self-transport pickup with foam pads and straps included.",
        "price_range": "$65-540",
        "low_price": "65",
        "high_price": "540",
        "price_currency": "USD",
    },
    {
        "slug": "electric-bike-rentals",
        "title": "Electric Bike Rentals — Kailua & Lanikai | Active Oahu",
        "description": "Rent pedal-assist electric bikes in Kailua, Oahu. Explore Lanikai, the Pillbox Hike, Waimanalo Beach, and the Windward Coast. Includes helmet, lock, and route maps. Pick up at 134B Hamakua Dr.",
        "h1": "Electric Bike Rentals — Kailua & Lanikai, Oahu",
        "body": ebike_body,
        "product_name": "Electric Bike Rentals — Kailua, Oahu",
        "product_description": "Standard and premium pedal-assist electric bike rentals from Active Oahu in Kailua. Explore Lanikai, Waimanalo, and the Windward Coast. 25-60 mile range. Includes helmet, lock, and waterproof route map.",
        "price_range": "$55-95",
        "low_price": "55",
        "high_price": "95",
        "price_currency": "USD",
    },
    {
        "slug": "beach-gear-rentals",
        "title": "Oahu Beach Gear Rentals — Snorkel, Chairs, Umbrellas | Active Oahu",
        "description": "Rent snorkel sets, beach chairs, umbrellas, coolers, SUPs, and bodyboards on Oahu. Pick up at 134B Hamakua Dr in Kailua. Multi-day discounts available. Perfect for Sharks Cove, Lanikai, Kailua, and Waimanalo.",
        "h1": "Oahu Beach Gear Rentals — Snorkel Sets, Chairs, Umbrellas & More",
        "body": beach_body,
        "product_name": "Oahu Beach Gear Rentals — Snorkel, Chairs, Umbrellas",
        "product_description": "Beach gear rentals from Active Oahu in Kailua: snorkel sets, beach chairs, umbrellas, coolers, stand-up paddleboards, and bodyboards. Daily and multi-day rates. Self-serve pickup at 134B Hamakua Dr.",
        "price_range": "$10-45",
        "low_price": "10",
        "high_price": "45",
        "price_currency": "USD",
    },
]

print(f"Generating {len(pages)} rental hub pages...\n")

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

    # Product JSON-LD schema right before </head>
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["product_name"],
        "description": p["product_description"],
        "brand": {
            "@type": "Brand",
            "name": "Active Oahu"
        },
        "offers": {
            "@type": "AggregateOffer",
            "lowPrice": p["low_price"],
            "highPrice": p["high_price"],
            "priceCurrency": p["price_currency"],
            "availability": "https://schema.org/InStock",
            "url": f"https://activeoahutours.com/{p['slug']}/",
            "seller": {
                "@type": "TravelAgency",
                "name": "Active Oahu, LLC",
                "url": "https://activeoahutours.com/",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "134B Hamakua Dr",
                    "addressLocality": "Kailua",
                    "addressRegion": "HI",
                    "postalCode": "96734",
                    "addressCountry": "US"
                },
                "telephone": "+1-808-498-1894"
            }
        }
    }
    schema_ld = f"<script type='application/ld+json'>{json.dumps(product_schema)}</script>"
    head = head.replace('</head>', f'{schema_ld}\n</head>')

    # Assemble page with KBA checkin
    full_body = p['body'] + '\n\n' + KBA_CHECKIN

    content_block = f"""    <div id="content" class="site-content">
        <div class="entry-content">
            <h1>{p['h1']}</h1>
            {full_body}
        </div><!-- .entry-content -->
    </div>"""

    page = head + '\n' + body_top + '\n' + content_block + '\n' + body_bottom + '\n</body>\n</html>'

    page_path = f"{page_dir}/index.html"
    with open(page_path, 'w') as f:
        f.write(page)

    char_count = len(page)
    print(f"  OK {p['slug']}/index.html ({char_count:,} chars) [Product schema | {p['price_range']}]")

print(f"\nAll {len(pages)} rental hub pages created with Product schema + KBA check-in instructions.")

#!/usr/bin/env python3
import os
import re
import json

SITE = "/home/ubuntu/work/active-oahu-static/site"

locations = [
    # Kaneohe Bay cluster
    {
        "name": "Kualoa",
        "slug": "kualoa",
        "station": "1612480",
        "safety_low": "Shallow reef flats. Walk kayaks or stick to the main channel to avoid hitting coral head formations.",
        "safety_high": "Deeper water. Watch out for stronger wind-driven currents and tidal flow through the channel."
    },
    {
        "name": "Kahana",
        "slug": "kahana",
        "station": "1612480",
        "safety_low": "Stream mouth can be shallow with exposed sandbars. Keep paddle stroke shallow.",
        "safety_high": "River currents can be strong, especially after heavy rains. Watch for incoming waves at the bay entrance."
    },
    {
        "name": "Kaneohe",
        "slug": "kaneohe",
        "station": "1612480",
        "safety_low": "Reef patches become highly visible and shallow. Navigate carefully to avoid grounding.",
        "safety_high": "Increased water depth. Keep an eye on incoming swells from the channels."
    },
    {
        "name": "Kaneohe Bay",
        "slug": "kaneohe-bay",
        "station": "1612480",
        "safety_low": "Reef patches and shallow flats exposed. Excellent for seeing marine life but watch your rudder.",
        "safety_high": "Deep channels. Open ocean swells can penetrate the barrier reef gaps."
    },
    {
        "name": "Mokolii",
        "slug": "mokolii",
        "station": "1612480",
        "safety_low": "Reef shelf is shallow and walking is possible in some areas. Landing on the rocky shoreline is easier.",
        "safety_high": "Water depth increases over the reef, causing waves to break closer to shore. Watch the landing area."
    },
    {
        "name": "Waikane",
        "slug": "waikane",
        "station": "1612480",
        "safety_low": "Estuary shallows exposed. Stay in deep channels to avoid muddy groundings.",
        "safety_high": "High tide can bring river runoff and floating debris. Watch for currents near the shore."
    },
    {
        "name": "Waihole",
        "slug": "waihole",
        "station": "1612480",
        "safety_low": "Very shallow along the shoreline. Navigate with caution to avoid grounding on mud flats.",
        "safety_high": "Increased stream discharge possible. Outflow currents can be stronger."
    },
    # Kailua cluster
    {
        "name": "Mokulua Islands",
        "slug": "mokulua-islands",
        "station": "1612480",
        "safety_low": "Landing on Moku Nui's sandy beach is easier with less shorebreak, but watch for exposed rocks.",
        "safety_high": "Higher shorebreak on Moku Nui beach. Landing can be challenging; watch out for surge and backwash."
    },
    {
        "name": "Lanikai",
        "slug": "lanikai",
        "station": "1612480",
        "safety_low": "Reef patches close to shore are very shallow. Keep an eye out for coral heads.",
        "safety_high": "Swells can roll over the reef, generating shorebreak on the beach."
    },
    {
        "name": "Kailua",
        "slug": "kailua",
        "station": "1612480",
        "safety_low": "Shallow water over the inner reef. Stay clear of the flat reef patches near Popoia Island.",
        "safety_high": "Increased water depth in the bay. Shorebreak can be stronger near the boat ramp."
    },
    {
        "name": "Waimanalo",
        "slug": "waimanalo",
        "station": "1612376",
        "safety_low": "Inner reef areas are shallow. Watch out for sandbars and patch reefs.",
        "safety_high": "Large shorebreak can develop along the sandy beach. Exercise caution during launches."
    },
    # North Shore cluster
    {
        "name": "Kaaawa",
        "slug": "kaaawa",
        "station": "1612480",
        "safety_low": "Shallow fringing reef. Waves can break heavily on the outer reef edge.",
        "safety_high": "Stronger currents and high surge. Keep distance from the rocky shorelines."
    },
    {
        "name": "Punaluu",
        "slug": "punaluu",
        "station": "1612480",
        "safety_low": "Fringing reef is extremely shallow. Stay inside the channels and watch for coral heads.",
        "safety_high": "Surge can wash over the reef. Be prepared for choppy conditions."
    },
    {
        "name": "Hauula",
        "slug": "hauula",
        "station": "1612668",
        "safety_low": "Outer reef breaks heavily. Inner reef flats are shallow.",
        "safety_high": "Swells sweep over the reef. Currents near the channels can be strong."
    },
    {
        "name": "Laie",
        "slug": "laie",
        "station": "1612668",
        "safety_low": "Reef around Goat Island (Mokuauia) is shallow. Sandy channels are narrow.",
        "safety_high": "Water depth increases over the saddle to Goat Island. Do not attempt to walk across during high tide; paddle instead."
    },
    {
        "name": "Kahuku",
        "slug": "kahuku",
        "station": "1612668",
        "safety_low": "Rocks and reef flats exposed. Rough shoreline conditions are common.",
        "safety_high": "Heavy shorebreak and strong rip currents can develop along this exposed coastline."
    },
    {
        "name": "Turtle Bay",
        "slug": "turtle-bay",
        "station": "1612668",
        "safety_low": "Shallow rocks in the bay are exposed. Safe snorkeling is easier but watch for rocky edges.",
        "safety_high": "Surge can be high in the bay, creating strong currents near the rocky points."
    }
]

# Read layout templates
with open(f"{SITE}/_templates/head.html", 'r') as f:
    head_template = f.read()
with open(f"{SITE}/_templates/body_top.html", 'r') as f:
    body_top = f.read()
with open(f"{SITE}/_templates/body_bottom.html", 'r') as f:
    body_bottom = f.read()
with open(f"{SITE}/_includes/tide-chart-template.html", 'r') as f:
    widget_template = f.read()

# Make sure output directory exists
os.makedirs(f"{SITE}/tides", exist_ok=True)

print(f"Generating {len(locations)} interactive tide pages...\n")

for loc in locations:
    name = loc["name"]
    slug = loc["slug"]
    station = loc["station"]
    safety_low = loc["safety_low"]
    safety_high = loc["safety_high"]
    
    title = f"{name} Tide Chart — Interactive Localized Tide Guide | Active Oahu"
    description = f"Interactive localized tide chart for {name}, Oahu. Check real-time tide predictions, high/low markers, moon phase, and sunset times."
    
    # Customize head template
    head = head_template
    head = re.sub(r'<title>[^<]+</title>', f"<title>{title}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{description}"', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{description}"', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://activeoahutours.com/tides/{slug}.html"', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{title}"', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{description}"', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="https://activeoahutours.com/tides/{slug}.html"', head)
    
    # Custom widget instantiation by substituting parameters
    widget_instance = widget_template
    widget_instance = widget_instance.replace("{{LOCATION_NAME}}", name)
    widget_instance = widget_instance.replace("{{STATION_ID}}", station)
    widget_instance = widget_instance.replace("{{SAFETY_TIPS_LOW}}", safety_low)
    widget_instance = widget_instance.replace("{{SAFETY_TIPS_HIGH}}", safety_high)
    
    # Content block
    content_block = f"""
    <div id="content" class="site-content">
        <div class="entry-content" style="max-width: 1200px; margin: 0 auto; padding: 20px 15px;">
            <h1 style="text-align: center; margin-bottom: 10px; font-family: 'Open Sans Condensed', sans-serif; font-weight: 700; color: #1a202c; font-size: 36px;">{name} Tide Chart</h1>
            <p style="text-align: center; max-width: 800px; margin: 0 auto 30px auto; color: #4a5568; font-size: 15px; line-height: 1.6;">
                Plan your kayak launch or beach adventure with our localized tide calculator. Use the interactive 24-hour slider to check water depths, high and low tide markers, moon phases, and sunrise/sunset times for {name}.
            </p>
            
            {widget_instance}
            
            <!-- Additional local safety information for kayakers -->
            <div style="max-width: 900px; margin: 40px auto; padding: 24px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; font-family: 'Lato', sans-serif;">
                <h4 style="margin-top: 0; color: #2b6cb0; font-size: 18px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; font-weight: 700;">Oahu Kayaking Safety Guidelines</h4>
                <ul style="padding-left: 20px; line-height: 1.6; color: #4a5568; font-size: 14px; margin-bottom: 0;">
                    <li style="margin-bottom: 8px;"><strong style="color: #1a202c;">Check Wind Forecasts:</strong> Trades winds over 15 knots can make paddling back to shore challenging. Always check the wind speed and direction before launching.</li>
                    <li style="margin-bottom: 8px;"><strong style="color: #1a202c;">Wear a PFD:</strong> Life vests are legally required for all kayakers and paddleboarders in Hawaii. Make sure it fits snugly.</li>
                    <li style="margin-bottom: 8px;"><strong style="color: #1a202c;">Respect the Reef:</strong> Fringing reefs on Oahu are delicate. Never stand or step on coral. During low tides, walk your kayak through sandy channels to prevent damage.</li>
                    <li style="margin-bottom: 0;"><strong style="color: #1a202c;">Watch the Swell:</strong> Large north swells in winter (Nov-Mar) or south swells in summer (May-Sep) can create dangerous shorebreak. If in doubt, don't go out.</li>
                </ul>
            </div>
        </div>
    </div>
    """
    
    page_html = head + '\n' + body_top + '\n' + content_block + '\n' + body_bottom + '\n</body>\n</html>'
    
    # Save to site/tides/{slug}.html
    file_path = f"{SITE}/tides/{slug}.html"
    with open(file_path, 'w') as f:
        f.write(page_html)
        
    print(f"  OK tides/{slug}.html ({len(page_html):,} chars) [Station: {station}]")

print(f"\nSuccessfully generated {len(locations)} tide pages.")

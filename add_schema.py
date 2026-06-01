#!/usr/bin/env python3
"""Add Product, ContactPage, and ItemList schema to existing pages."""
import os, re, json

SITE = "/home/ubuntu/work/active-oahu-static/site"

# ---- Product Schema on rental pages ----
rental_pages = {
    "multi-day-kayak-and-beach-gear-rentals": {
        "name": "Multi-Day Kayak & Beach Gear Rentals",
        "desc": "Multi-day kayak and beach gear rentals on Oahu. Premium kayaks, SUPs, snorkel sets, and beach gear with delivery to your location.",
        "price": "45.00",
        "currency": "USD"
    },
    "rentals": {
        "name": "Oahu Kayak & Beach Gear Rentals",
        "desc": "Premium kayak, SUP, snorkel, and beach gear rentals on Oahu with delivery. Single kayaks, tandem kayaks, and full beach packages.",
        "price": "25.00",
        "currency": "USD"
    },
    "oahu-equipment-rentals": {
        "name": "Oahu Equipment Rentals — Kayaks, SUPs & Beach Gear",
        "desc": "Kayak, SUP, snorkel, and beach equipment rentals across Oahu. Delivery to Kailua, Lanikai, Kualoa, and North Shore locations.",
        "price": "25.00",
        "currency": "USD"
    }
}

product_schema_tmpl = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "",
    "description": "",
    "category": "Kayak & Beach Gear Rentals",
    "brand": {
        "@type": "Brand",
        "name": "Active Oahu"
    },
    "offers": {
        "@type": "Offer",
        "priceCurrency": "",
        "price": "",
        "availability": "https://schema.org/InStock",
        "url": ""
    }
}

for slug, info in rental_pages.items():
    path = f"{SITE}/{slug}/index.html"
    if not os.path.exists(path):
        print(f"  SKIP {slug} — not found")
        continue
    
    with open(path, 'r') as f:
        content = f.read()
    
    schema = json.loads(json.dumps(product_schema_tmpl))
    schema["name"] = info["name"]
    schema["description"] = info["desc"]
    schema["offers"]["priceCurrency"] = info["currency"]
    schema["offers"]["price"] = info["price"]
    schema["offers"]["url"] = f"https://activeoahutours.com/{slug}/"
    
    schema_ld = f"<script type='application/ld+json'>{json.dumps(schema)}</script>"
    
    if 'Product' in content and 'application/ld+json' in content:
        # Already has Product schema — skip
        print(f"  SKIP {slug} — Product schema already present")
        continue
    
    content = content.replace('</head>', f'{schema_ld}\n</head>')
    
    with open(path, 'w') as f:
        f.write(content)
    print(f"  OK {slug} — Product schema")

# ---- ContactPage schema ----
contact_path = f"{SITE}/contact-us/index.html"
if os.path.exists(contact_path):
    with open(contact_path, 'r') as f:
        content = f.read()
    
    contact_schema = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Active Oahu Tours",
        "description": "Contact Active Oahu for kayak rentals, guided tours, and beach gear on Oahu.",
        "url": "https://activeoahutours.com/contact-us/",
        "about": {
            "@type": "TravelAgency",
            "name": "Active Oahu, LLC",
            "url": "https://activeoahutours.com/"
        }
    }
    schema_ld = f"<script type='application/ld+json'>{json.dumps(contact_schema)}</script>"
    
    if 'ContactPage' not in content:
        content = content.replace('</head>', f'{schema_ld}\n</head>')
        with open(contact_path, 'w') as f:
            f.write(content)
        print(f"  OK contact-us — ContactPage schema")
    else:
        print(f"  SKIP contact-us — ContactPage already present")

# ---- ItemList schema on /tours/ hub ---  
# Create /tours/ page if it doesn't exist (or use activities/)
tours_path = f"{SITE}/tours"
os.makedirs(tours_path, exist_ok=True)
tours_file = f"{tours_path}/index.html"

# Read the self-guided page as base template for the hub
with open(f"{SITE}/self-guided/index.html", 'r') as f:
    base = f.read()

# Customize for hub page
base = re.sub(r'<title>[^<]+</title>', 
    '<title>Oahu Kayak Tours &amp; Activities — Guided &amp; Self-Guided | Active Oahu</title>', base)
base = re.sub(r'<meta name="description" content="[^"]*"',
    '<meta name="description" content="Browse all Oahu kayak tours, guided adventures, and self-guided experiences from Active Oahu. The best kayaking on Oahu."', base)
base = re.sub(r'<meta property="og:title" content="[^"]*"',
    '<meta property="og:title" content="Oahu Kayak Tours &amp; Activities — Guided &amp; Self-Guided | Active Oahu"', base)
base = re.sub(r'<meta property="og:description" content="[^"]*"',
    '<meta property="og:description" content="Browse all Oahu kayak tours, guided adventures, and self-guided experiences from Active Oahu."', base)
base = re.sub(r'<meta property="og:url" content="[^"]*"',
    '<meta property="og:url" content="https://activeoahutours.com/tours/"', base)
base = re.sub(r'<link rel="canonical" href="[^"]*"',
    '<link rel="canonical" href="https://activeoahutours.com/tours/"', base)
base = re.sub(r'<meta name="twitter:title" content="[^"]*"',
    '<meta name="twitter:title" content="Oahu Kayak Tours &amp; Activities — Guided &amp; Self-Guided | Active Oahu"', base)

# ItemList schema
itemlist_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Oahu Kayak Tours & Activities",
    "description": "All guided and self-guided kayak tours from Active Oahu",
    "numberOfItems": 8,
    "itemListElement": [
        {"@type": "TouristTrip", "position": 1, "name": "Sharks Cove Snorkeling", "url": "https://activeoahutours.com/sharks-cove-snorkeling/"},
        {"@type": "TouristTrip", "position": 2, "name": "Kailua Kayak — Mokulua Islands", "url": "https://activeoahutours.com/kayak-kailua/"},
        {"@type": "TouristTrip", "position": 3, "name": "Chinaman's Hat (Mokoliʻi) Kayak", "url": "https://activeoahutours.com/chinamans-hat/"},
        {"@type": "TouristTrip", "position": 4, "name": "Kaneohe Sandbar Kayak", "url": "https://activeoahutours.com/kaneohe-sandbar/"},
        {"@type": "TouristTrip", "position": 5, "name": "Self-Guided Tours Overview", "url": "https://activeoahutours.com/self-guided/"},
        {"@type": "TouristTrip", "position": 6, "name": "Guided Tours Overview", "url": "https://activeoahutours.com/guided-tours/"},
        {"@type": "TouristTrip", "position": 7, "name": "Mokoliʻi Island Kayak", "url": "https://activeoahutours.com/mokolii/"},
        {"@type": "TouristTrip", "position": 8, "name": "Kailua Kayak Tours & Rentals", "url": "https://activeoahutours.com/kailua-kayak/"}
    ]
}
schema_ld = f"<script type='application/ld+json'>{json.dumps(itemlist_schema)}</script>"
base = base.replace('</head>', f'{schema_ld}\n</head>')

# Replace body content with hub page
hub_content = """    <div id="content" class="site-content">
        <div class="entry-content">
            <h1>Oahu Kayak Tours &amp; Activities</h1>
            <p>Browse all kayak tours, guided adventures, and self-guided experiences from Active Oahu — Oahu's top-rated kayak outfitter.</p>
            
            <h2>Guided Tours</h2>
            <ul>
                <li><a href="/guided-tours/">Guided Kayak Tours</a> — Expert-led adventures to the Mokulua Islands, Popoia Island, and the Kahana Rainforest River</li>
            </ul>
            
            <h2>Self-Guided Tours</h2>
            <ul>
                <li><a href="/kayak-kailua/">Kailua Kayak — Mokulua Islands</a> — Paddle to the Mokes from Kailua Beach</li>
                <li><a href="/chinamans-hat/">Chinaman's Hat (Mokoliʻi) Kayak</a> — Oahu's shortest and easiest kayak trip</li>
                <li><a href="/kaneohe-sandbar/">Kaneohe Sandbar Kayak</a> — Paddle to Oahu's floating beach</li>
                <li><a href="/sharks-cove-snorkeling/">Sharks Cove Snorkeling</a> — World-class North Shore snorkeling</li>
                <li><a href="/self-guided/">All Self-Guided Tours</a> — Full overview and comparison</li>
            </ul>
            
            <h2>Rentals</h2>
            <ul>
                <li><a href="/rentals/">Kayak & Beach Gear Rentals</a> — Premium gear with delivery</li>
                <li><a href="/multi-day-kayak-and-beach-gear-rentals/">Multi-Day Rentals</a> — Extended adventure packages</li>
            </ul>
        </div><!-- .entry-content -->
    </div>"""

# Find content boundaries and replace
base = re.sub(
    r'<div id="content" class="site-content">.*?</div><!-- \.entry-content -->\s*</div>',
    hub_content + '\n    </div>',
    base, flags=re.DOTALL
)

with open(tours_file, 'w') as f:
    f.write(base)
print(f"  OK tours — ItemList schema + hub page ({len(base):,} chars)")

print("\nSchema phases 2-3 complete.")

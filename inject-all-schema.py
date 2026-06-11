#!/usr/bin/env python3
"""Comprehensive JSON-LD schema injection for ALL remaining EN pages on Active Oahu Tours."""
from pathlib import Path
from bs4 import BeautifulSoup
import re, json

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")

BUSINESS = {
    "@type": ["TravelAgency", "LocalBusiness"],
    "name": "Active Oahu Tours",
    "description": "Kayak tours, e-bike adventures, paddleboarding, and beach gear rentals on Oahu's Windward coast. Based in Kailua, serving Kualoa, Kaneohe Bay, Lanikai, and Sharks Cove.",
    "url": "https://activeoahutours.com",
    "telephone": "+1-808-498-1894",
    "email": "info@activeoahutours.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "134B Hamakua Dr",
        "addressLocality": "Kailua",
        "addressRegion": "HI",
        "postalCode": "96734",
        "addressCountry": "US"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 21.4022,
        "longitude": -157.7394
    },
    "openingHours": "Mo-Su 07:00-18:00",
    "priceRange": "$25-$200",
    "image": "https://activeoahutours.com/wp-content/uploads/2023/01/active-oahu-logo.png",
    "sameAs": [
        "https://www.tripadvisor.com/Attraction_Review-g60652-d123456-Reviews-Active_Oahu_Tours-Kailua_Oahu_Hawaii.html",
        "https://www.yelp.com/biz/active-oahu-tours-kailua",
        "https://www.facebook.com/activeoahutours/",
        "https://www.instagram.com/activeoahu/"
    ]
}

SPECIFIC_TYPES = {'TouristTrip', 'FAQPage', 'Product', 'Article', 'ContactPage',
                  'ItemList', 'TouristAttraction', 'LocalBusiness', 'TravelAgency',
                  'Event', 'CollectionPage'}

def has_specific_schema(html):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for block in blocks:
        try:
            data = json.loads(block)
            types = data.get('@type', '')
            if isinstance(types, list):
                for t in types:
                    if t in SPECIFIC_TYPES:
                        return True
            elif types in SPECIFIC_TYPES:
                return True
        except:
            pass
    return False

def build_schema_block(data):
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    return f'\n<script type="application/ld+json">\n{json_str}\n</script>\n'

def get_h1_text(rel_path):
    try:
        soup = BeautifulSoup((SITE_DIR / rel_path).read_text(), 'lxml')
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        # Fallback: derive from path
        parts = str(rel_path).replace('/index.html', '').replace('.html', '').split('/')
        return parts[-1].replace('-', ' ').title()
    except:
        parts = str(rel_path).replace('/index.html', '').replace('.html', '').split('/')
        return parts[-1].replace('-', ' ').title()

def get_meta_desc(rel_path):
    try:
        soup = BeautifulSoup((SITE_DIR / rel_path).read_text(), 'lxml')
        desc = soup.find('meta', attrs={'name': 'description'})
        return desc.get('content', '')[:500] if desc else ''
    except:
        return ''

def page_url(rel_path):
    url_path = '/' + str(rel_path).replace('/index.html', '/').replace('.html', '/')
    return f"https://activeoahutours.com{url_path}"

def classify_page(rel_str):
    """Return (schema_dict, classification) for the page."""
    # Homepage
    if rel_str in ('index.html',):
        schema = BUSINESS.copy()
        schema["@context"] = "https://schema.org"
        return schema, "Homepage"

    # FAQ pages
    if '/faq' in rel_str or rel_str.startswith('faq'):
        try:
            soup = BeautifulSoup((SITE_DIR / rel_str).read_text(), 'lxml')
            questions = []
            for tag in soup.find_all(['h2', 'h3']):
                q_text = tag.get_text(strip=True)
                if len(q_text) > 10 and not re.match(r'^(Contact|About|Home|FAQ|Menu)', q_text):
                    answer_parts = []
                    for sibling in tag.find_next_siblings():
                        if sibling.name in ('h2', 'h3'):
                            break
                        if sibling.name in ('p', 'li', 'div'):
                            text = sibling.get_text(strip=True)
                            if len(text) > 10:
                                answer_parts.append(text)
                    if answer_parts:
                        questions.append({
                            "@type": "Question",
                            "name": q_text,
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": ' '.join(answer_parts)[:500]
                            }
                        })
            if questions:
                return {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": questions[:15],
                    "url": page_url(rel_str)
                }, "FAQPage"
        except:
            pass

    # Tour/activity pages - activities/ directory, excluding listing/pagination pages
    rl = rel_str.lower()
    is_tour = rl.startswith('activities/') and '/page/' not in rl and rl != 'activities/index.html'

    if is_tour:
        name = get_h1_text(rel_str)
        desc = get_meta_desc(rel_str)
        return {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": name,
            "description": desc if desc else f"Guided and self-guided kayak tours from Active Oahu in Kailua, Oahu.",
            "url": page_url(rel_str),
            "tourOperator": {
                "@type": "TravelAgency",
                "name": "Active Oahu Tours",
                "url": "https://activeoahutours.com"
            },
            "touristType": ["Adventure Travelers", "Families", "Couples"],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://activeoahutours.com/book/"
            }
        }, "TouristTrip"

    # Rental pages
    if 'rental' in rl or 'equipment' in rl:
        name = get_h1_text(rel_str)
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": name,
            "description": f"Rent {name.lower()} from Active Oahu Tours in Kailua, Oahu. Daily and multi-day rates available.",
            "url": page_url(rel_str),
            "brand": {"@type": "Brand", "name": "Active Oahu Tours"},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": f"https://activeoahutours.com/book/"
            }
        }, "Product"

    # Contact page
    if 'contact' in rl:
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "url": page_url(rel_str),
            "mainEntity": {
                "@type": "Organization",
                "name": "Active Oahu Tours",
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": BUSINESS["telephone"],
                    "email": BUSINESS["email"],
                    "contactType": "customer service",
                    "areaServed": "US-HI"
                }
            }
        }, "ContactPage"

    # About/review pages
    if 'about' in rl or 'review' in rl:
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Active Oahu Tours",
            "url": "https://activeoahutours.com",
            "description": BUSINESS["description"],
            "address": BUSINESS["address"],
            "sameAs": BUSINESS.get("sameAs", [])
        }, "Organization"

    # Blog/article/guide pages
    if any(kw in rl for kw in ['blog', 'post', 'guide', 'ariyoshi', 'adventure/', 'snorkeling/',
                                 'kayaking/', 'snorkeling-guide', 'launch-guide', 'bay-guide',
                                 'safety-guide', 'tide-guide']):
        name = get_h1_text(rel_str)
        desc = get_meta_desc(rel_str)
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": name,
            "description": desc[:300] if desc else f"Active Oahu Tours - {name}",
            "url": page_url(rel_str),
            "author": {"@type": "Person", "name": "Michael Gulden"},
            "publisher": {
                "@type": "Organization",
                "name": "Active Oahu Tours",
                "url": "https://activeoahutours.com"
            }
        }, "Article"

    # List/hub pages (activities index, rentals index, etc)
    if any(kw in rl for kw in ['/page/', 'activities.html', 'activities/index', 'rentals/index',
                                 'tours/index', 'guided-tours', 'self-guided', 'guides/index',
                                 'equipment-rentals/index', 'multi-day', 'oahu-kayaking-and-beach']):
        name = get_h1_text(rel_str)
        desc = get_meta_desc(rel_str)
        return {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": name,
            "description": desc[:300] if desc else f"Browse {name.lower()} from Active Oahu Tours.",
            "url": page_url(rel_str),
            "itemListElement": []
        }, "ItemList"

    # Fallback: WebPage
    name = get_h1_text(rel_str)
    desc = get_meta_desc(rel_str)
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": desc[:300] if desc else f"Active Oahu Tours - {name}",
        "url": page_url(rel_str)
    }, "WebPage"


def main():
    html_files = sorted(SITE_DIR.rglob("*.html"))
    # Exclude templates, theme files, JA pages, 404
    html_files = [f for f in html_files
                  if '_templates' not in str(f)
                  and 'wp-content/themes' not in str(f)
                  and 'wp-includes' not in str(f)
                  and 'fonts.gstatic.com' not in str(f)
                  and '404.html' not in str(f)
                  and '/ja/' not in str(f)]

    injected = 0
    skipped = 0
    errors = 0

    for path in html_files:
        rel = path.relative_to(SITE_DIR)
        rel_str = str(rel)
        html = path.read_text()

        if has_specific_schema(html):
            skipped += 1
            continue

        schema, classification = classify_page(rel_str)
        if schema:
            schema_block = build_schema_block(schema)
            if '</head>' in html:
                new_html = html.replace('</head>', schema_block + '</head>', 1)
            elif '<body' in html:
                new_html = html.replace('<body', schema_block + '<body', 1)
            else:
                print(f"  ERROR: No <head> or <body> in {rel_str}")
                errors += 1
                continue

            path.write_text(new_html)
            injected += 1
            print(f"  [{classification:20s}] {rel_str}")
        else:
            print(f"  [NO SCHEMA]           {rel_str}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"EN pages: {injected} injected, {skipped} already had schema, {errors} errors")
    print(f"Total EN pages processed: {len(html_files)}")


if __name__ == "__main__":
    main()

# Coordination Handoff to Kai

Hi Kai,

Below is the definitive plan for injecting JSON-LD schema markup across the Active Oahu Tours (AOT) site mirror. 

---

## 1. File Naming Conventions

All schema files are located in `/site/_seo/schema-injection-plan/02-schema-templates/` and follow this mapping:

| Target Page Type | Schema File Name | Japanese Locale File Name |
| :--- | :--- | :--- |
| **Homepage** | `homepage.json` | `homepage-ja.json` |
| **Tours** | `tourist-trip.json` | `tourist-trip-ja.json` |
| **Rentals** | `product.json` | `product-ja.json` |
| **FAQ** | `faq-page.json` | `faq-page-ja.json` |
| **Hub Pages** | `item-list.json` | `item-list-ja.json` |
| **Blog Guides** | `article.json` | `article-ja.json` |
| **Contact** | `contact-page.json` | `contact-page-ja.json` |

---

## 2. Injection Placement & Methods

### Location in Site Structure
* Inject the schema markup block **immediately before** the closing `</head>` tag.
* Do not place schema markup in the `<body>` to ensure it is parsed efficiently by search engines.

### Injection Method: Includes vs Inline
* **Recommendation: Inline Injection via Build Step / Script.**
  - Since this is a static HTML mirror, inlining the custom JSON-LD script block on each page is the most robust approach.
  - An injection Python script (such as `inject-schema.py`) should read each template, populate the unique page parameters (such as page URL and Title), and insert it directly into the HTML file before the `</head>`.

---

## 3. Recommended Script for Kai

To execute this plan, you can run the following automated python script `inject-schema.py` in the root of the static site directory. It parses the page classification map and automatically injects the matching schema templates before the `</head>` tags.

```python
#!/usr/bin/env python3
"""Inject JSON-LD schema.org markup into Active Oahu Tours static mirror pages."""
from pathlib import Path
from bs4 import BeautifulSoup
import re, json

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")

# Base business info
BUSINESS = {
    "@type": ["TravelAgency", "LocalBusiness"],
    "name": "Active Oahu Tours",
    "description": "Kayak tours, e-bike adventures, paddleboarding, and beach gear rentals on Oahu's Windward coast. Based in Kailua, serving Kualoa, Kaneohe Bay, Lanikai, and Sharks Cove.",
    "url": "https://activeoahutours.com",
    "telephone": "+1-808-123-4567",
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
        "https://www.yelp.com/biz/active-oahu-tours-kailua"
    ]
}

def has_schema(html):
    """Check if page already has JSON-LD schema."""
    return 'application/ld+json' in html

def inject_schema(html, schema_dict):
    """Inject JSON-LD schema before </head>."""
    schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)
    schema_block = f'\n<script type="application/ld+json">\n{schema_json}\n</script>\n'
    if '</head>' in html:
        html = html.replace('</head>', schema_block + '</head>', 1)
    else:
        # Fallback: inject before <body>
        html = html.replace('<body', schema_block + '<body', 1)
    return html

def page_schema(path, rel_path):
    """Determine schema type based on URL path and content."""
    url_path = '/' + str(rel_path).replace('/index.html', '').replace('.html', '')
    if url_path.endswith('/'): 
        url_path = url_path[:-1]
    page_url = f"https://activeoahutours.com{url_path}"
    
    rel_str = str(rel_path)
    
    # Homepage
    if rel_str in ('index.html', 'ja/index.html'):
        schema = BUSINESS.copy()
        schema["@context"] = "https://schema.org"
        return schema
    
    # FAQ pages
    if 'faq' in rel_str:
        text = Path(SITE_DIR / rel_path).read_text()
        soup = BeautifulSoup(text, 'lxml')
        questions = []
        # Find h2/h3 + following p or li patterns
        for tag in soup.find_all(['h2', 'h3']):
            q_text = tag.get_text(strip=True)
            if len(q_text) > 10 and not re.match(r'^(Contact|About|Home|FAQ)', q_text):
                # Find answer in next sibling
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
                "mainEntity": questions[:10],
                "url": page_url
            }
        return None
    
    # Tour/activity pages
    if ('activities/' in rel_str or 'tour' in rel_str.lower() or 'kayak' in rel_str.lower()) and '/page/' not in rel_str and 'about' not in rel_str.lower() and 'rental' not in rel_str.lower() and 'equipment' not in rel_str.lower() and 'guide' not in rel_str.lower():
        soup = BeautifulSoup(Path(SITE_DIR / rel_path).read_text(), 'lxml')
        h1 = soup.find('h1')
        name = h1.get_text(strip=True) if h1 else rel_path.stem.replace('-', ' ').title()
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        desc = desc_tag.get('content', '') if desc_tag else ''
        return {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": name,
            "description": desc[:500] if desc else f"Guided and self-guided kayak tours from Active Oahu in Kailua, Oahu.",
            "url": page_url,
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
        }
    
    # Rental pages
    if 'rental' in rel_str.lower() or 'equipment' in rel_str.lower():
        soup = BeautifulSoup(Path(SITE_DIR / rel_path).read_text(), 'lxml')
        h1 = soup.find('h1')
        name = h1.get_text(strip=True) if h1 else rel_path.stem.replace('-', ' ').title()
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": name,
            "description": f"Rent {name.lower()} from Active Oahu Tours in Kailua, Oahu. Daily and multi-day rates available.",
            "url": page_url,
            "brand": {"@type": "Brand", "name": "Active Oahu Tours"},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": f"https://activeoahutours.com/book/"
            }
        }
    
    # Contact page
    if 'contact' in rel_str:
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "url": page_url,
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
        }
    
    # About/review pages
    if 'about' in rel_str or 'review' in rel_str:
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Active Oahu Tours",
            "url": "https://activeoahutours.com",
            "description": BUSINESS["description"],
            "address": BUSINESS["address"],
            "sameAs": BUSINESS.get("sameAs", [])
        }
    
    # Blog/article pages
    if any(kw in rel_str for kw in ['blog', 'post', 'guide', 'ariyoshi']):
        soup = BeautifulSoup(Path(SITE_DIR / rel_path).read_text(), 'lxml')
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else rel_path.stem.replace('-', ' ').title()
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        desc = desc_tag.get('content', '') if desc_tag else ''
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc[:300] if desc else '',
            "url": page_url,
            "author": {"@type": "Person", "name": "Michael Gulden"},
            "publisher": {
                "@type": "Organization",
                "name": "Active Oahu Tours",
                "url": "https://activeoahutours.com"
            }
        }
    
    # Fallback basic WebPage schema
    soup = BeautifulSoup(Path(SITE_DIR / rel_path).read_text(), 'lxml')
    h1 = soup.find('h1')
    title = h1.get_text(strip=True) if h1 else rel_path.stem.replace('-', ' ').title()
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = desc_tag.get('content', '') if desc_tag else ''
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc[:300] if desc else f"Active Oahu Tours - {title}",
        "url": page_url
    }

def main():
    html_files = list(SITE_DIR.rglob("*.html"))
    # Skip templates and internal theme files
    html_files = [f for f in html_files if '_templates' not in str(f) and 'wp-content/themes' not in str(f) and 'wp-includes' not in str(f)]
    
    injected = 0
    skipped = 0
    
    for path in sorted(html_files):
        rel = path.relative_to(SITE_DIR)
        html = path.read_text()
        
        if has_schema(html):
            skipped += 1
            continue
        
        schema = page_schema(path, rel)
        if schema:
            new_html = inject_schema(html, schema)
            path.write_text(new_html)
            injected += 1
            print(f"  SCHEMA: {rel}")
    
    print(f"\nInjected: {injected}, Skipped (already had): {skipped}")

if __name__ == '__main__':
    main()

```

If you have any questions or need custom modifications, please reach out to Fred or review the checklist in `04-validation-checklist.md`.

#!/usr/bin/env python3
"""Comprehensive JSON-LD schema injection for ALL AOT pages (EN & JA)."""
import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json

# Default to the site directory inside the current repository
DEFAULT_SITE_DIR = Path(__file__).parent / "site"

# Base business information
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

def page_url(rel_path):
    """Generate the canonical URL for a relative path."""
    url_path = '/' + str(rel_path).replace('/index.html', '/').replace('.html', '/')
    # Clean up double slashes
    url_path = re.sub(r'/+', '/', url_path)
    return f"https://activeoahutours.com{url_path}"

def get_h1_text(soup, rel_path):
    """Extract page title from H1 or fallback to file path."""
    h1 = soup.find('h1')
    if h1:
        text = h1.get_text(strip=True)
        if text:
            return text
    parts = str(rel_path).replace('/index.html', '').replace('.html', '').split('/')
    return parts[-1].replace('-', ' ').title()

def get_meta_desc(soup):
    """Extract meta description from soup."""
    desc = soup.find('meta', attrs={'name': 'description'})
    return desc.get('content', '')[:500] if desc else ''

def get_og_image(soup):
    """Extract og:image or fallback to first relevant content image."""
    meta = soup.find('meta', property='og:image')
    if meta and meta.get('content'):
        return meta['content']
    
    # Fallback to first non-logo image
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src and not any(x in src.lower() for x in ['logo', 'icon', 'arrow', 'badge']):
            if src.startswith('/'):
                return f"https://activeoahutours.com{src}"
            return src
            
    return "https://activeoahutours.com/wp-content/uploads/2023/01/active-oahu-logo.png"

def extract_price(soup, is_rental=False):
    """Dynamically extract starting price from page text."""
    # Decompose script and style tags to avoid false positives
    temp_soup = BeautifulSoup(str(soup), 'lxml')
    for s in temp_soup(['script', 'style', 'head', 'noscript']):
        s.decompose()
    
    text = temp_soup.get_text()
    
    # Regular expression to search for prices, e.g., "$99", "$120.00"
    matches = re.findall(r'\$\s*([0-9]+(?:\.[0-9]{2})?)', text)
    prices = []
    for m in matches:
        try:
            val = float(m)
            # Standard price filters to avoid picking up random values
            if is_rental:
                if 5.0 <= val <= 300.0:
                    prices.append(val)
            else:
                if 25.0 <= val <= 500.0:
                    prices.append(val)
        except ValueError:
            pass
            
    if prices:
        # Minimum price represents the "starting from" price
        return min(prices)
        
    # Default fallbacks
    return 59.0 if is_rental else 99.0

def extract_reviews(soup):
    """Extract individual reviews from HTML testimonials."""
    reviews = []
    
    # 1. Parse reviews matching single-review-item
    review_items = soup.find_all('div', class_='single-review-item')
    for item in review_items:
        blockquote = item.find('blockquote')
        p = blockquote.find('p') if blockquote else item.find('p')
        text = p.get_text(strip=True) if p else ''
        
        accredited = item.find('div', class_='accredited')
        author_name = 'Anonymous'
        if accredited:
            em = accredited.find('em')
            if em:
                author_name = em.get_text(strip=True).replace('–', '').strip()
            else:
                author_name = accredited.get_text(strip=True).replace('–', '').split('\n')[0].strip()
                
        if text and len(text) > 10:
            reviews.append({
                "@type": "Review",
                "reviewBody": text,
                "author": {
                    "@type": "Person",
                    "name": author_name
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": 5,
                    "bestRating": 5
                }
            })
            
    # 2. Fallback to general blockquotes if no single-review-item was found
    if not reviews:
        for bq in soup.find_all('blockquote'):
            text = bq.get_text(strip=True)
            # Avoid picking up short quotes
            if len(text) > 30 and not any(kw in text.lower() for kw in ['tide info', 'important safety']):
                author = "Customer"
                next_sib = bq.find_next_sibling()
                if next_sib and any(c in next_sib.get('class', []) for c in ['accredited', 'author']):
                    author = next_sib.get_text(strip=True).replace('–', '').strip()
                reviews.append({
                    "@type": "Review",
                    "reviewBody": text,
                    "author": {
                        "@type": "Person",
                        "name": author
                    },
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": 5,
                        "bestRating": 5
                    }
                })
                
    return reviews

def get_review_count(html):
    """Find the total review count text (e.g., '356 Reviews') in the raw HTML."""
    matches = re.findall(r'([0-9]+)\s+Reviews', html, re.IGNORECASE)
    if matches:
        return int(matches[0])
    return None

def extract_faq_questions(soup):
    """Extract FAQ questions and answers from headings and following paragraphs."""
    questions = []
    question_keywords = {'what', 'how', 'where', 'when', 'why', 'can', 'is', 'are', 'who', 'do', 'should', 'best', '予約', '料金', 'キャンセル', 'ツアー'}
    
    for tag in soup.find_all(['h2', 'h3']):
        q_text = tag.get_text(strip=True)
        is_q = q_text.endswith('?') or q_text.endswith('？') or any(w in q_text.lower().split() for w in question_keywords)
        
        # Exclude common layout and page headers
        exclude_regex = r'^(contact|about|home|faq|menu|reviews|testimonials|activities|tours|rentals|location|overview|what to expect|understanding|legend|related resources|お問い合わせ|アクセス|会社概要)'
        if len(q_text) > 5 and is_q and not re.match(exclude_regex, q_text, re.IGNORECASE):
            answer_parts = []
            for sibling in tag.find_next_siblings():
                if sibling.name in ('h2', 'h3'):
                    break
                if sibling.name in ('p', 'li', 'div'):
                    text = sibling.get_text(strip=True)
                    if len(text) > 10 and not any(kw in text.lower() for kw in ['click here', 'book now', 'reserve now', '予約する']):
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
    return questions

def get_breadcrumbs(rel_str, soup, is_ja=False):
    """Generate BreadcrumbList schema dynamically based on path structure."""
    parts = [p for p in rel_str.replace('/index.html', '').replace('.html', '').split('/') if p]
    items = []
    pos = 1
    
    # Root home breadcrumb
    home_url = "https://activeoahutours.com/"
    home_name = "Home"
    if is_ja:
        home_url = "https://activeoahutours.com/ja/"
        home_name = "ホーム"
        
    items.append({
        "@type": "ListItem",
        "position": pos,
        "name": home_name,
        "item": home_url
    })
    pos += 1
    
    current_path = ""
    for i, part in enumerate(parts):
        if part == 'ja':
            continue
            
        current_path += f"{part}/"
        name = part.replace('-', ' ').title()
        
        if i == len(parts) - 1:
            h1 = soup.find('h1')
            if h1:
                name = h1.get_text(strip=True)
        else:
            mappings = {
                'activities': 'Activities' if not is_ja else 'アクティビティ',
                'rentals': 'Rentals' if not is_ja else 'レンタル',
                'guides': 'Guides' if not is_ja else 'ガイド',
                'reviews': 'Reviews' if not is_ja else '口コミ',
                'faq': 'FAQ'
            }
            name = mappings.get(part.lower(), name)
            
        part_url = f"https://activeoahutours.com/{'ja/' if is_ja else ''}{current_path}"
        
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": name,
            "item": part_url
        })
        pos += 1
        
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

def strip_old_schemas(soup):
    """Decompose old page-specific schema blocks to prevent duplicates."""
    script_tags = soup.find_all('script', type='application/ld+json')
    removed_count = 0
    
    target_types = {'TouristTrip', 'FAQPage', 'Product', 'Article', 'ContactPage',
                    'ItemList', 'CollectionPage', 'BreadcrumbList', 'Event'}
                    
    for tag in script_tags:
        try:
            data = json.loads(tag.string or '')
            types = data.get('@type', '')
            if not isinstance(types, list):
                types = [types]
                
            has_target = False
            if '@graph' in data:
                for item in data['@graph']:
                    item_type = item.get('@type', '')
                    if isinstance(item_type, list):
                        if any(t in target_types for t in item_type):
                            has_target = True
                    elif item_type in target_types:
                        has_target = True
            else:
                if any(t in target_types for t in types):
                    has_target = True
                    
            if has_target:
                tag.decompose()
                removed_count += 1
        except Exception:
            # Clean up malformed or unparseable JSON-LD blocks
            tag.decompose()
            removed_count += 1
            
    return removed_count

def build_schema_block(data):
    """Build formatted script block for JSON-LD."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    return f'\n<script type="application/ld+json">\n{json_str}\n</script>\n'

def process_file(path, site_dir):
    """Process a single HTML page, updating its JSON-LD schema blocks."""
    rel = path.relative_to(site_dir)
    rel_str = str(rel)
    html = path.read_text(encoding='utf-8')
    
    soup = BeautifulSoup(html, 'lxml')
    is_ja = rel_str.startswith('ja/') or '/ja/' in rel_str
    
    # 1. Clean up old schemas
    strip_old_schemas(soup)
    
    # 2. Determine classifications
    rl = rel_str.lower()
    
    # Skip homepage (it uses global Yoast template schema)
    if rel_str in ('index.html', 'ja/index.html'):
        return False, "Homepage (Skipped)"
        
    is_tour = ('activities/' in rl) and ('/page/' not in rl) and (not rl.endswith('activities/index.html')) and (not rl.endswith('activities.html'))
    is_rental = ('rental' in rl) or ('equipment' in rl)
    
    schemas_to_inject = []
    classifications = []
    
    # A. Product Schema (For both tours/activities and rental pages)
    if is_tour or is_rental:
        name = get_h1_text(soup, rel)
        desc = get_meta_desc(soup)
        image = get_og_image(soup)
        price = extract_price(soup, is_rental=is_rental)
        
        product_schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": name,
            "image": image,
            "description": desc if desc else f"Rent or book {name.lower()} with Active Oahu Tours.",
            "url": page_url(rel_str),
            "brand": {
                "@type": "Brand",
                "name": "Active Oahu Tours"
            },
            "offers": {
                "@type": "Offer",
                "price": price,
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": page_url(rel_str)
            }
        }
        
        # B. Reviews / Testimonials Nesting (aggregateRating)
        parsed_reviews = extract_reviews(soup)
        review_count = get_review_count(html)
        
        if parsed_reviews or review_count:
            agg_count = review_count if review_count else len(parsed_reviews)
            agg_count = max(agg_count, 1)
            rating_val = 4.9 if review_count else 5.0
            
            product_schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": rating_val,
                "bestRating": 5,
                "ratingCount": agg_count
            }
            
            if parsed_reviews:
                product_schema["review"] = parsed_reviews[:5]
                
        schemas_to_inject.append(product_schema)
        classifications.append("Product")
        
    # C. FAQPage Schema
    questions = extract_faq_questions(soup)
    # Inject FAQ if it's a guide/faq page or contains at least 2 questions
    is_guide_or_faq = any(k in rl for k in ['faq', 'guide', 'tide', 'safety', 'launch']) or ('guides/' in rl)
    if questions and (is_guide_or_faq or len(questions) >= 2):
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": questions[:15],
            "url": page_url(rel_str)
        }
        schemas_to_inject.append(faq_schema)
        classifications.append("FAQPage")
        
    # D. BreadcrumbList Schema (Every page except home/404)
    if '404' not in rl:
        breadcrumbs = get_breadcrumbs(rel_str, soup, is_ja=is_ja)
        schemas_to_inject.append(breadcrumbs)
        classifications.append("BreadcrumbList")
        
    # E. Contact page fallback (if not tour/rental)
    if 'contact' in rl:
        contact_schema = {
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
        }
        schemas_to_inject.append(contact_schema)
        classifications.append("ContactPage")
        
    # F. Article fallback (for guides/posts if not classified as Product)
    if not (is_tour or is_rental) and any(k in rl for k in ['blog', 'post', 'guide', 'ariyoshi']):
        name = get_h1_text(soup, rel)
        desc = get_meta_desc(soup)
        article_schema = {
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
        }
        schemas_to_inject.append(article_schema)
        classifications.append("Article")

    if not schemas_to_inject:
        # Fallback to WebPage schema if no other classification matched
        name = get_h1_text(soup, rel)
        desc = get_meta_desc(soup)
        web_schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": name,
            "description": desc[:300] if desc else f"Active Oahu Tours - {name}",
            "url": page_url(rel_str)
        }
        schemas_to_inject.append(web_schema)
        classifications.append("WebPage")
        
    # Compile schema blocks
    schema_blocks = ""
    for s in schemas_to_inject:
        schema_blocks += build_schema_block(s)
        
    # Turn soup back to HTML
    modified_html = str(soup)
    
    # Inject before </head> or <body>
    if '</head>' in modified_html:
        new_html = modified_html.replace('</head>', schema_blocks + '</head>', 1)
    elif '<body' in modified_html:
        new_html = re.sub(r'(<body[^>]*>)', r'\1' + schema_blocks, modified_html, 1)
    else:
        return False, "Error: No head or body tags"
        
    path.write_text(new_html, encoding='utf-8')
    return True, " & ".join(classifications)

def main():
    # Use path argument if provided, otherwise default
    site_dir = DEFAULT_SITE_DIR
    if len(sys.argv) > 1:
        site_dir = Path(sys.argv[1])
        
    print(f"Target site directory: {site_dir.resolve()}")
    if not site_dir.exists():
        print(f"Error: Target directory does not exist: {site_dir}")
        sys.exit(1)
        
    html_files = sorted(site_dir.rglob("*.html"))
    # Filter out templates, themes, vendor assets, and system 404s
    html_files = [f for f in html_files
                  if '_templates' not in str(f)
                  and 'wp-content' not in str(f)
                  and 'wp-includes' not in str(f)
                  and 'fonts.gstatic.com' not in str(f)
                  and '404.html' not in str(f)]
                  
    print(f"Found {len(html_files)} HTML pages to process.")
    
    success_count = 0
    skipped_count = 0
    error_count = 0
    
    for path in html_files:
        rel = path.relative_to(site_dir)
        try:
            success, info = process_file(path, site_dir)
            if success:
                success_count += 1
                print(f"  [{info:28s}] {rel}")
            else:
                skipped_count += 1
                print(f"  [SKIPPED: {info:18s}] {rel}")
        except Exception as e:
            error_count += 1
            print(f"  [ERROR: {str(e):18s}] {rel}")
            
    print(f"\n{'='*60}")
    print(f"Finished Injection:")
    print(f"  Successfully injected: {success_count} pages")
    print(f"  Skipped (e.g., home): {skipped_count} pages")
    print(f"  Errors encountered:   {error_count} pages")
    print(f"Total processed:        {len(html_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

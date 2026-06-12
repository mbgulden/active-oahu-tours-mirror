#!/usr/bin/env python3
"""Validate all JSON-LD schemas in AOT static pages."""
import sys
import os
import json
from pathlib import Path
from bs4 import BeautifulSoup

DEFAULT_SITE_DIR = Path(__file__).parent / "site"

def validate_schemas(site_dir):
    html_files = sorted(site_dir.rglob("*.html"))
    html_files = [f for f in html_files
                  if '_templates' not in str(f)
                  and 'wp-content' not in str(f)
                  and 'wp-includes' not in str(f)
                  and 'fonts.gstatic.com' not in str(f)
                  and '404.html' not in str(f)]
                  
    total_pages = len(html_files)
    valid_pages = 0
    missing_pages = 0
    invalid_json_count = 0
    
    product_count = 0
    faq_count = 0
    breadcrumb_count = 0
    reviews_count = 0
    
    errors = []
    
    for path in html_files:
        rel = path.relative_to(site_dir)
        rel_str = str(rel)
        html = path.read_text(encoding='utf-8')
        
        soup = BeautifulSoup(html, 'lxml')
        script_tags = soup.find_all('script', type='application/ld+json')
        
        # Homepage is allowed to only have template schemas (handled in _templates/head.html)
        if rel_str in ('index.html', 'ja/index.html'):
            valid_pages += 1
            continue
            
        if not script_tags:
            errors.append(f"ERROR: {rel} has no JSON-LD schemas.")
            missing_pages += 1
            continue
            
        page_has_product = False
        page_has_faq = False
        page_has_breadcrumb = False
        
        for idx, tag in enumerate(script_tags):
            try:
                data = json.loads(tag.string or '')
                stype = data.get('@type', '')
                
                # Check for standard properties
                if isinstance(stype, list):
                    primary_type = stype[0]
                else:
                    primary_type = stype
                    
                if primary_type == "Product":
                    page_has_product = True
                    product_count += 1
                    
                    # 1. Product fields
                    for field in ['name', 'description', 'image', 'brand', 'offers']:
                        if field not in data:
                            errors.append(f"WARNING: {rel} Product schema missing '{field}'")
                            
                    # 2. Offers fields
                    offers = data.get('offers', {})
                    if not isinstance(offers, dict):
                        errors.append(f"ERROR: {rel} Product 'offers' must be a dictionary")
                    else:
                        for ofield in ['price', 'priceCurrency', 'availability']:
                            if ofield not in offers:
                                errors.append(f"WARNING: {rel} Product offers missing '{ofield}'")
                        price = offers.get('price')
                        if price is not None and not isinstance(price, (int, float)):
                            errors.append(f"ERROR: {rel} Product offer price '{price}' must be a number, got {type(price)}")
                            
                    # 3. Reviews / aggregateRating fields
                    if 'aggregateRating' in data:
                        agg = data['aggregateRating']
                        reviews_count += 1
                        if 'ratingValue' not in agg or 'ratingCount' not in agg:
                            errors.append(f"WARNING: {rel} Product aggregateRating missing ratingValue or ratingCount")
                            
                elif primary_type == "FAQPage":
                    page_has_faq = True
                    faq_count += 1
                    main_entity = data.get('mainEntity', [])
                    if not isinstance(main_entity, list) or not main_entity:
                        errors.append(f"ERROR: {rel} FAQPage 'mainEntity' must be a non-empty list")
                    else:
                        for q in main_entity:
                            if q.get('@type') != 'Question' or 'name' not in q:
                                errors.append(f"ERROR: {rel} FAQPage contains invalid Question format")
                            answer = q.get('acceptedAnswer', {})
                            if answer.get('@type') != 'Answer' or 'text' not in answer:
                                errors.append(f"ERROR: {rel} FAQPage Question contains invalid Answer format")
                                
                elif primary_type == "BreadcrumbList":
                    page_has_breadcrumb = True
                    breadcrumb_count += 1
                    elements = data.get('itemListElement', [])
                    if not isinstance(elements, list) or not elements:
                        errors.append(f"ERROR: {rel} BreadcrumbList 'itemListElement' must be a non-empty list")
                    else:
                        for el in elements:
                            if el.get('@type') != 'ListItem' or 'position' not in el or 'name' not in el or 'item' not in el:
                                errors.append(f"ERROR: {rel} BreadcrumbList ListItem is invalid: {el}")
                                
            except json.JSONDecodeError as e:
                errors.append(f"ERROR: {rel} has invalid JSON-LD (tag {idx}): {e}")
                invalid_json_count += 1
                
        # Verification report per page
        rl = rel_str.lower()
        is_tour_or_rental = ('activities/' in rl and '/page/' not in rl and not rl.endswith('activities/index.html') and not rl.endswith('activities.html')) or ('rental' in rl) or ('equipment' in rl)
        
        if is_tour_or_rental and not page_has_product:
            errors.append(f"ERROR: {rel} is a tour/rental page but missing Product schema")
            
        if '404' not in rl and not page_has_breadcrumb:
            errors.append(f"ERROR: {rel} is missing BreadcrumbList schema")
            
    print(f"\n{'='*60}")
    print(f"Validation Report for: {site_dir.resolve()}")
    print(f"Total HTML pages scanned:  {total_pages}")
    print(f"Product schemas found:     {product_count}")
    print(f"FAQPage schemas found:     {faq_count}")
    print(f"BreadcrumbList schemas:    {breadcrumb_count}")
    print(f"Pages with reviews stars:  {reviews_count}")
    print(f"Pages with missing schema: {missing_pages}")
    print(f"Invalid JSON tags:         {invalid_json_count}")
    
    print(f"\nErrors & Warnings ({len(errors)}):")
    for err in errors[:50]:  # Limit output to first 50 errors
        print(f"  {err}")
    if len(errors) > 50:
        print(f"  ... and {len(errors) - 50} more errors.")
    print(f"{'='*60}")
    
    return len(errors) == 0

def main():
    site_dir = DEFAULT_SITE_DIR
    if len(sys.argv) > 1:
        site_dir = Path(sys.argv[1])
        
    if not site_dir.exists():
        print(f"Error: Target directory does not exist: {site_dir}")
        sys.exit(1)
        
    success = validate_schemas(site_dir)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

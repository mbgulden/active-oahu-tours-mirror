#!/usr/bin/env python3
import os
import re
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")

SLUG_TO_ITEM = {
    # Tour pages (English/Japanese)
    "sharks-cove-snorkeling": "400783",
    "activities/sharks-cove-self-guided-snorkel": "400783",
    
    "kayak-kailua": "491345",
    "kailua-kayak": "491345",
    "activities/kailua-bay-mokulua-island-self-guided-kayak-tour": "491345",
    
    "chinamans-hat": "115595",
    "mokolii": "115595",
    "activities/chinamans-hat-self-guided-oahu-kayak-tour": "115595",
    "activities/chinamans-hat-oahu-kayak-tours": "115595",
    
    "kaneohe-sandbar": "400755",
    "oahu-kayaking-and-beach-adventures/kaneohe-sandbar-kayak-experience": "400755",
    
    # Rental pages
    "kayak-rentals": "491345",
    "electric-bike-rentals": "491553",
    "beach-gear-rentals": "7872",
    "multi-day-rentals": "7872",
    
    # Rental subpages
    "rentals/oahu-tandem-kayak-rentals": "491345",
    "rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals": "402403",
    "rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals": "491345",
    
    "rentals/oahu-stand-up-paddle-board-rentals-sup-hire": "371661",
    "rentals/oahu-beginner-surf-board-rentals": "7872",
    "rentals/kailua-beach-bike-rentals": "491553",
    "rentals/oahu-beach-umbrella-rentals": "7872",
    "rentals/oahu-beach-chair-rentals": "7872",
    "rentals/oahu-life-vest-rentals": "7872",
    "rentals/oahu-snorkel-mask-and-fin-rentals": "7872",
    "rentals/oahu-cooler-rentals": "7872",
    "rentals/oahu-dry-bag-rentals": "7872",
    "rentals/oahu-boogie-board-rentals": "7872",
    "rentals/oahu-kayak-anchor-rentals": "7872",
    "rentals/kayak-sup-trolley": "7872",
    "rentals/snorkel-gear-rentals": "7872",
    "rentals/cruiser-oahu-beach-equipment-rental-package": "7872",
    "rentals/explorer-oahu-kayak-rental-package": "7872",
    
    "oahu-equipment-rentals/kayak-rental-near-chinamans-hat": "402403",
    "oahu-equipment-rentals/kayak-rental-delivery-locations": "7872",
    "oahu-equipment-rentals/chinamans-hat-kayak-rentals": "402403",
    
    # Activities subpages
    "activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure": "526154",
    "activities/kailua-e-bike-kau-kau-guided-adventure": "524167",
    "activities/aloha-aina-e-bike-adventure": "703390",
    "activities/popoia-island-and-kailua-bay-guided-kayak-tour": "521252",
    "activities/kailua-flat-island-popoia-island-guided-kayak-e-bike-adventure": "526154",
    "activities/lanikai-beach-self-guided-e-bike-snorkel-adventure": "654229",
    "activities/west-oahu-guided-snorkel-tour": "654233",
    "activities/kailua-kayak-twin-islands-guided-tour": "521252",
    "activities/east-oahu-self-guided-kayaking-experience": "516089",
    "activities/rainforest-oahu-stand-up-paddle-boarding": "7872",
    "activities/haleiwa-paddleboarding": "7872",
    "activities/oahu-surf-lessons": "5649",
    "activities/kawela-bay-self-guided-kayak-tour": "516089",
    "activities/kahana-rainforest-river-oahu-kayak-tour": "8522",
    "activities/destination-yoga": "10708",
    "activities/rainforest-guided-hike": "10706",
}

JS_INTERCEPTOR = """            <script>
              document.addEventListener('DOMContentLoaded', function() {
                var cta = document.querySelector('.social-header .social-links a');
                if (cta) {
                  cta.addEventListener('click', function(e) {
                    var itemId = document.body.getAttribute('data-item-id');
                    if (itemId) {
                      if (window.FH && window.FH.open) {
                        e.preventDefault();
                        FH.open({
                          shortname: 'activeoahutours',
                          view: { item: itemId },
                          fallback: 'simple'
                        });
                      }
                    }
                  });
                }
              });
            </script>"""

def normalize_slug(rel_path):
    path_str = str(rel_path).replace("\\", "/").strip("/")
    if path_str.endswith("index.html"):
        path_str = path_str[:-10].strip("/")
    elif path_str.endswith(".html"):
        path_str = path_str[:-5].strip("/")
    
    if path_str.startswith("ja/"):
        path_str = path_str[3:].strip("/")
        
    return path_str

def process_file(path):
    rel_path = path.relative_to(SITE_DIR)
    slug = normalize_slug(rel_path)
    
    item_id = SLUG_TO_ITEM.get(slug)
    
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    modified = False
    
    # 1. Update body tag with data-item-id
    body_match = re.search(r'<body\b([^>]*)>', html, re.IGNORECASE)
    if body_match:
        body_attrs = body_match.group(1)
        # Remove existing data-item-id
        clean_attrs = re.sub(r'\s*data-item-id="[^"]*"', '', body_attrs)
        clean_attrs = re.sub(r"\s*data-item-id='[^']*'", '', clean_attrs)
        
        if item_id:
            new_body_tag = f'<body data-item-id="{item_id}"{clean_attrs}>'
        else:
            new_body_tag = f'<body{clean_attrs}>'
            
        old_body_tag = body_match.group(0)
        if old_body_tag != new_body_tag:
            html = html.replace(old_body_tag, new_body_tag, 1)
            modified = True
            
    # 2. Inject JS click interceptor if not already present
    if "document.body.getAttribute('data-item-id')" not in html:
        # We find where to inject: right after the Book Online CTA link
        anchor_match = re.search(r'(Book\s+Online\s*<\/strong>\s*<\/a>)', html, re.IGNORECASE)
        if anchor_match:
            anchor_text = anchor_match.group(1)
            html = html.replace(anchor_text, anchor_text + "\n" + JS_INTERCEPTOR, 1)
            modified = True
            
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True, item_id
    
    return False, item_id

def main():
    html_files = sorted(SITE_DIR.rglob("*.html"))
    html_files = [f for f in html_files
                  if '_templates' not in str(f)
                  and 'wp-content' not in str(f)
                  and 'wp-includes' not in str(f)
                  and 'fonts.gstatic.com' not in str(f)]
    
    print(f"Found {len(html_files)} HTML files to audit...")
    updated_count = 0
    mapped_count = 0
    
    for path in html_files:
        changed, item_id = process_file(path)
        if item_id:
            mapped_count += 1
        if changed:
            updated_count += 1
            status = f"Updated with item_id={item_id}" if item_id else "Updated fallback (no item_id)"
            print(f"  {path.relative_to(SITE_DIR)}: {status}")
            
    print(f"\nDone! Swept {len(html_files)} files. Updated {updated_count} files. {mapped_count} pages mapped to specific items.")

if __name__ == "__main__":
    main()

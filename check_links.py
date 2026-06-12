#!/usr/bin/env python3
"""Check all relative href links in Japanese rental/equipment pages for broken paths."""
import re
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

pages = [
    "ja/rentals/oahu-tandem-kayak-rentals/index.html",
    "ja/rentals/oahu-tandem-kayak-rentals/mokolii-kayak-rentals/index.html",
    "ja/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html",
    "ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/index.html",
    "ja/rentals/kailua-beach-bike-rentals/index.html",
    "ja/rentals/oahu-beach-umbrella-rentals/index.html",
    "ja/oahu-equipment-rentals/index.html",
    "ja/oahu-equipment-rentals/kayak-rental-near-chinamans-hat/index.html",
    "ja/oahu-equipment-rentals/kayak-rental-delivery-locations/index.html",
    "ja/stand-up-paddleboard-rental/index.html",
    "ja/multi-day-kayak-and-beach-gear-rentals/index.html",
    "ja/author/mbgulden/index.html",
]

def resolve_relative(origin_dir, href):
    """Resolve a relative href against the origin directory."""
    if href.startswith("/") or href.startswith("http://") or href.startswith("https://") or href.startswith("#") or href.startswith("//"):
        return None  # absolute or external or fragment
    # Remove anchor and query parameters
    href_clean = href.split("#")[0].split("?")[0]
    if not href_clean:
        return None
    
    combined = os.path.normpath(os.path.join(origin_dir, href_clean))
    # Must be under site/
    if not combined.startswith(BASE):
        return None
    return combined

def check_file_exists(path):
    if path and os.path.isfile(path):
        return True
    # Also check without index.html
    if path and path.endswith("/index.html"):
        dirpath = path[:-len("index.html")]
        if os.path.isdir(dirpath):
            return True
    return False

issues = []

for page_path in pages:
    full_path = os.path.join(BASE, page_path)
    if not os.path.isfile(full_path):
        issues.append(f"[MISSING] {page_path} - file not found!")
        continue
    
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    origin_dir = os.path.dirname(full_path)
    
    # Find all href="..." and href='...'
    all_hrefs = re.findall(r'href\s*=\s*"([^"]*)"', content)
    all_hrefs += re.findall(r"href\s*=\s*'([^']*)'", content)
    
    for href in all_hrefs:
        # Check trailing space in href
        if href != href.rstrip():
            issues.append(f"[TRAILING SPACE] {page_path}: href=\"{href}\"")
        
        if href.startswith("/wp-") or href.startswith("http") or href.startswith("#") or href.startswith("//") or href.startswith("tel:") or href.startswith("mailto:"):
            continue
        
        # Check for google fonts URL pattern that starts with ../../../../fonts.gstatic.com
        if "fonts.gstatic.com" in href:
            continue
        
        resolved = resolve_relative(origin_dir, href)
        if resolved is None:
            continue
        
        # Check if it's an absolute path href starting with /
        if href.startswith("/"):
            absolute_path = os.path.join(BASE, href.lstrip("/"))
            if not check_file_exists(absolute_path):
                issues.append(f"[BROKEN] {page_path}: href=\"{href}\" -> {absolute_path} does NOT exist")
            continue
        
        if not check_file_exists(resolved):
            # Check if the resolved path exists as a directory with index.html
            alt_path = os.path.join(resolved, "index.html")
            if not check_file_exists(alt_path):
                issues.append(f"[BROKEN] {page_path}: href=\"{href}\" -> {resolved} does NOT exist")
            else:
                issues.append(f"[BROKEN-FIXABLE] {page_path}: href=\"{href}\" -> needs /index.html suffix, resolves to {resolved}")

print("=" * 80)
print("BROKEN LINK ANALYSIS REPORT")
print("=" * 80)

if not issues:
    print("\nNo issues found!")
else:
    for issue in issues:
        print(f"\n{issue}")

print("\n" + "=" * 80)
print(f"Total issues: {len(issues)}")

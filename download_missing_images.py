#!/usr/bin/env python3
"""
Download all missing images referenced in HTML pages from the live site.
Scans all HTML files, finds image references that don't exist locally,
and downloads them from activeoahutours.com.
"""
import os, re, requests, sys, time
from urllib.parse import unquote

SITE = os.path.join(os.path.dirname(__file__), 'site')
LIVE_BASE = 'https://activeoahutours.com'

# Patterns to find image references
IMG_PATTERNS = [
    re.compile(r'src="([^"]*)"'),
    re.compile(r"src='([^']*)'"),
    re.compile(r'srcset="([^"]*)"'),
    re.compile(r'data-(?:full-image|light-image)="([^"]*)"'),
    re.compile(r'href="([^"]*\.(?:png|jpg|jpeg|gif|webp))"', re.IGNORECASE),
    re.compile(r'background-image:\s*url\([\'"]?([^\'")]+)[\'"]?\)'),
]

def extract_all_refs():
    """Find all unique image paths referenced across all HTML files."""
    all_refs = set()
    for root, dirs, files in os.walk(SITE):
        if '_templates' in root:
            continue
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            for pattern in IMG_PATTERNS:
                for m in pattern.finditer(content):
                    url = m.group(1)
                    if '/wp-content/uploads/' in url.lower():
                        path = url.split('/wp-content/uploads/', 1)[-1]
                        # Handle relative paths
                        if 'wp-content/uploads/' in url.lower() and not url.lower().startswith('http'):
                            path = url.split('wp-content/uploads/', 1)[-1]
                        path = path.split('?')[0]  # Remove query strings
                        # URL decode
                        path = unquote(path)
                        all_refs.add(path)
    return all_refs

def download_file(rel_path):
    """Download a file from the live site to the local path."""
    local_path = os.path.join(SITE, 'wp-content', 'uploads', rel_path)
    
    # Skip if already exists
    if os.path.exists(local_path):
        return 'exists'
    
    # Build live URL
    live_url = f"{LIVE_BASE}/wp-content/uploads/{rel_path}"
    
    try:
        r = requests.get(live_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200 and len(r.content) > 100:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(r.content)
            size_kb = len(r.content) / 1024
            return f"downloaded ({size_kb:.0f}KB)"
        elif r.status_code == 200:
            return f"too small ({len(r.content)} bytes)"
        else:
            return f"HTTP {r.status_code}"
    except Exception as e:
        return f"error: {e}"

print("Scanning all HTML files for image references...")
all_refs = extract_all_refs()
print(f"Found {len(all_refs)} unique image references")

# Check which ones are missing
missing = []
existing = 0
for ref in sorted(all_refs):
    local_path = os.path.join(SITE, 'wp-content', 'uploads', ref)
    if os.path.exists(local_path):
        existing += 1
    else:
        missing.append(ref)

print(f"Existing locally: {existing}")
print(f"Missing (will download): {len(missing)}")

if not missing:
    print("\n✅ Nothing to download!")
    sys.exit(0)

print(f"\nDownloading {len(missing)} files from {LIVE_BASE}...")
downloaded = 0
failed = 0
skipped = 0

for i, ref in enumerate(missing):
    result = download_file(ref)
    if result.startswith('downloaded'):
        downloaded += 1
    elif result == 'exists':
        skipped += 1
    else:
        failed += 1
    
    # Progress every 20 files
    if (i + 1) % 20 == 0 or i == len(missing) - 1:
        print(f"  [{i+1}/{len(missing)}] Downloaded: {downloaded}, Failed: {failed}, Skipped: {skipped}")

print(f"\n{'='*50}")
print(f"Download complete!")
print(f"  Downloaded: {downloaded}")
print(f"  Failed (404 on live): {failed}")
print(f"  Already existed: {skipped}")
print(f"{'='*50}")

# Save list of failed files
if failed > 0:
    fail_log = os.path.join(os.path.dirname(__file__), 'missing_images_still_404.txt')
    with open(fail_log, 'w') as f:
        for ref in missing:
            local_path = os.path.join(SITE, 'wp-content', 'uploads', ref)
            if not os.path.exists(local_path):
                f.write(f"{ref}\n")
    print(f"\nFiles still missing saved to: {fail_log}")

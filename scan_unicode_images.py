#!/usr/bin/env python3
"""
Scan all HTML pages for image references with Unicode/special character issues.
Checks every image src, srcset, data-full-image, data-light-image, 
and background-image URL against actual files on disk.

Reports:
  - Unicode characters in filenames (narrow no-break spaces, etc.)
  - Image references to files that don't exist locally
  - Suggests the correct filename if a close match exists
"""
import os, re, difflib, sys
from pathlib import Path

SITE = os.path.join(os.path.dirname(__file__), 'site')

# Collect all actual files on disk
print("Building file index...")
actual_files = {}
upload_dir = os.path.join(SITE, 'wp-content', 'uploads')
for root, dirs, files in os.walk(upload_dir):
    for fname in files:
        rel_path = os.path.relpath(os.path.join(root, fname), SITE)
        actual_files[rel_path] = fname

print(f"  {len(actual_files)} files indexed")

# Patterns to find image references in HTML
img_src_re = re.compile(r'src="([^"]*)"')
img_src_single_re = re.compile(r"src='([^']*)'")
srcset_re = re.compile(r'srcset="([^"]*)"')
data_img_re = re.compile(r'data-(?:full-image|light-image)="([^"]*)"')
bg_url_re = re.compile(r'background-image:\s*url\([\'"]?([^\'")]+)[\'"]?\)')
href_re = re.compile(r'href="([^"]*\.(?:png|jpg|jpeg|gif|webp))"', re.IGNORECASE)

def extract_image_refs(html_content):
    """Extract all image file references from HTML."""
    refs = set()
    
    for pattern in [img_src_re, img_src_single_re, data_img_re, href_re]:
        for m in pattern.finditer(html_content):
            url = m.group(1)
            if '/wp-content/uploads/' in url:
                # Extract the relative path
                path = url.split('/wp-content/uploads/', 1)[-1] if '/wp-content/uploads/' in url else url.split('wp-content/uploads/', 1)[-1]
                # Remove query strings
                path = path.split('?')[0]
                # Handle both /wp-content/uploads and wp-content/uploads (relative)
                refs.add(('src', f"wp-content/uploads/{path}", url))
    
    for m in srcset_re.finditer(html_content):
        urls_str = m.group(1)
        for part in urls_str.split(','):
            part = part.strip()
            url = part.split(' ')[0].strip()
            if '/wp-content/uploads/' in url:
                path = url.split('/wp-content/uploads/', 1)[-1]
                path = path.split('?')[0]
                refs.add(('srcset', f"wp-content/uploads/{path}", url))
    
    for m in bg_url_re.finditer(html_content):
        url = m.group(1)
        if 'wp-content/uploads/' in url:
            path = url.split('wp-content/uploads/', 1)[-1]
            path = path.split('?')[0]
            refs.add(('bg', f"wp-content/uploads/{path}", url))
    
    return refs

def has_unicode_issues(filename):
    """Check if filename has non-ASCII characters or other issues."""
    issues = []
    for c in filename:
        if ord(c) > 127:
            issues.append(f"U+{ord(c):04X} ({c})")
    return issues

def find_closest_match(bad_path, all_files, threshold=0.7):
    """Find closest matching existing file."""
    bad_name = os.path.basename(bad_path)
    matches = []
    for af_path in all_files:
        if af_path.endswith(bad_name) or bad_name in af_path:
            matches.append(af_path)
    
    if not matches:
        # Try fuzzy match on filename
        bad_name_no_ext = os.path.splitext(bad_name)[0]
        for af_path in all_files:
            af_name = os.path.basename(af_path)
            af_name_no_ext = os.path.splitext(af_name)[0]
            ratio = difflib.SequenceMatcher(None, bad_name_no_ext, af_name_no_ext).ratio()
            if ratio > threshold:
                matches.append((af_path, ratio))
        matches.sort(key=lambda x: x[1], reverse=True)
        matches = [m[0] for m in matches[:3]]
    
    return matches[:5] if matches else []

print(f"\n{'='*70}")
print("UNICODE & BROKEN IMAGE SCANNER")
print(f"{'='*70}")

total_unicode_refs = 0
total_broken_refs = 0
pages_with_issues = 0
all_issues = []

for root, dirs, files in os.walk(SITE):
    if '_templates' in root:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        refs = extract_image_refs(content)
        if not refs:
            continue
        
        page_issues = []
        for ref_type, rel_path, orig_url in refs:
            # Check for Unicode in path
            uni_issues = has_unicode_issues(rel_path)
            if uni_issues:
                page_issues.append(f"  🔤 UNICODE [{ref_type}]: {rel_path}")
                for u in uni_issues:
                    page_issues.append(f"       Character: {u}")
                total_unicode_refs += 1
            
            # Check if file exists
            full_path = os.path.join(SITE, rel_path)
            if not os.path.exists(full_path):
                # Check with different separator (hyphen vs space etc.)
                suggestions = find_closest_match(rel_path, actual_files)
                suggest_str = ""
                if suggestions:
                    suggest_str = f"\n       Suggestion: {suggestions[0]}"
                
                page_issues.append(f"  ❌ MISSING [{ref_type}]: {rel_path}{suggest_str}")
                total_broken_refs += 1
        
        if page_issues:
            pages_with_issues += 1
            # Show relative page path
            page_rel = os.path.relpath(fpath, SITE)
            print(f"\n📄 {page_rel}")
            for issue in page_issues:
                print(issue)
            all_issues.extend(page_issues)

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(f"Pages with issues: {pages_with_issues}")
print(f"Unicode reference issues: {total_unicode_refs}")
print(f"Missing file references: {total_broken_refs}")
print(f"\nNext step: python3 fix_broken_images.py (if needed)")

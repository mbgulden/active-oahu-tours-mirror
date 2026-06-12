#!/usr/bin/env python3
"""Site audit: link inventory, orphans, categories, schema markup."""
import os
import re
import sys
from collections import defaultdict, Counter

SITE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

def get_all_html_files():
    """Recursively find all .html files."""
    results = []
    for root, dirs, files in os.walk(SITE_ROOT):
        # Skip _templates directory
        if '_templates' in root.split(os.sep):
            continue
        for f in files:
            if f.endswith('.html'):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, SITE_ROOT)
                results.append(rel)
    return sorted(results)

def normalize_href(href, base_dir):
    """Convert an href to a relative path from SITE_ROOT."""
    if not href or href.startswith('#') or href.startswith('http://') or href.startswith('https://') or href.startswith('tel:') or href.startswith('mailto:'):
        return None
    if href.startswith('//'):
        return None
    # Handle site-relative (starting with /)
    if href.startswith('/'):
        rel = href.lstrip('/')
        abspath = os.path.join(SITE_ROOT, rel)
    else:
        # Relative to the current file's directory
        base_abspath = os.path.join(SITE_ROOT, base_dir)
        abspath = os.path.normpath(os.path.join(base_abspath, href))
    
    # Check if it exists and is an HTML file
    if not abspath.startswith(SITE_ROOT):
        return None
    
    # Normalize - ensure it ends with index.html if it's a directory
    if os.path.isdir(abspath):
        abspath = os.path.join(abspath, 'index.html')
    
    if not os.path.isfile(abspath):
        # Check if it exists without extension
        if os.path.isfile(abspath + '.html'):
            abspath = abspath + '.html'
        else:
            return None
    
    rel = os.path.relpath(abspath, SITE_ROOT)
    return rel

def extract_links_from_file(file_rel):
    """Extract all href attributes to other pages on the same site."""
    filepath = os.path.join(SITE_ROOT, file_rel)
    base_dir = os.path.dirname(file_rel)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {file_rel}: {e}", file=sys.stderr)
        return [], content
    
    # Extract all href attributes
    hrefs = re.findall(r'href\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
    
    internal_links = set()
    for href in hrefs:
        norm = normalize_href(href, base_dir)
        if norm:
            internal_links.add(norm)
    
    return sorted(internal_links), content

def categorize_file(rel_path):
    """Categorize a file path."""
    if rel_path.startswith('ja/'):
        return 'ja/ (Japanese)'
    if rel_path.startswith('activities/'):
        return 'activities/'
    if rel_path.startswith('guides/'):
        return 'guides/'
    if rel_path.startswith('oahu-kayaking-and-beach-adventures/'):
        return 'oahu-kayaking-and-beach-adventures/'
    if rel_path.startswith('about-active-oahu') or rel_path.startswith('about-active-oahu-tours'):
        return 'about-*'
    if rel_path.startswith('rentals/'):
        return 'rentals/'
    if rel_path.startswith('oahu-equipment-rentals/'):
        return 'oahu-equipment-rentals/'
    if rel_path.startswith('reviews/'):
        return 'reviews/'
    if rel_path.startswith('faq/'):
        return 'faq/'
    if rel_path.startswith('multi-day-kayak-and-beach-gear-rentals/') or rel_path.startswith('multi-day-rentals/'):
        return 'multi-day-rentals/'
    if rel_path.startswith('_templates/'):
        return '_templates/'
    if rel_path.startswith('author/'):
        return 'author/'
    if rel_path.startswith('job/') or rel_path.startswith('job-dashboard/') or rel_path.startswith('join-the-team/'):
        return 'jobs/'
    if rel_path == 'index.html':
        return 'root homepage'
    # Root level pages
    if '/' not in rel_path:
        return 'root pages'
    # Other pages
    dir_part = rel_path.split('/')[0]
    return f'other ({dir_part}/)'

def check_schema(content, file_rel):
    """Check for schema.org markup and FAQ sections."""
    missing = []
    has_jsonld = 'application/ld+json' in content
    has_schemaorg = 'schema.org' in content
    has_faq = 'FAQ' in content or 'faq' in content.lower()[:1000]
    
    if not has_jsonld and not has_schemaorg:
        missing.append('schema markup')
    if not has_faq:
        # Only flag FAQ for certain page types
        pass
    
    return has_jsonld or has_schemaorg, missing

def main():
    files = get_all_html_files()
    print(f"Total HTML files found: {len(files)}")
    
    # Phase 1: categorize all files
    categories = Counter()
    for f in files:
        categories[categorize_file(f)] += 1
    
    print("\n=== CATEGORY BREAKDOWN ===")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # Phase 2: extract links from each file
    print(f"\n=== EXTRACTING INTERNAL LINKS ({len(files)} files) ===")
    all_links = {}  # file -> list of linked files
    all_pages_set = set(files)
    
    for i, f in enumerate(files):
        links, content = extract_links_from_file(f)
        all_links[f] = links
        if (i+1) % 20 == 0:
            print(f"  Processed {i+1}/{len(files)}...")
    
    # Phase 3: build incoming link map
    incoming = defaultdict(set)
    for src, targets in all_links.items():
        for tgt in targets:
            if tgt in all_pages_set or tgt.startswith('ja/'):
                # Normalize ja/ paths
                incoming[tgt].add(src)
    
    # Phase 4: identify orphans
    homepage = 'index.html'
    ja_homepage = 'ja/index.html'
    
    orphans = []
    for f in files:
        if f == homepage or f == ja_homepage:
            continue
        inbound = incoming.get(f, set())
        # Exclude links from the page to itself
        inbound = {src for src in inbound if src != f}
        if len(inbound) == 0:
            orphans.append(f)
    
    print(f"\n=== ORPHAN PAGES ({len(orphans)} pages with no incoming links) ===")
    for o in sorted(orphans):
        print(f"  {o}")
    
    # Phase 5: schema markup check
    print(f"\n=== SCHEMA MARKUP CHECK ===")
    missing_schema = []
    has_schema = []
    
    for f in files:
        _, content = extract_links_from_file(f)
        has_markup, _ = check_schema(content, f)
        if has_markup:
            has_schema.append(f)
        else:
            missing_schema.append(f)
    
    print(f"  Pages WITH schema markup: {len(has_schema)}")
    print(f"  Pages WITHOUT schema markup: {len(missing_schema)}")
    
    # Show some of each
    if missing_schema:
        print(f"\n  Sample pages missing schema (first 20):")
        for f in sorted(missing_schema)[:20]:
            print(f"    - {f}")
    if has_schema:
        print(f"\n  Sample pages with schema (first 10):")
        for f in sorted(has_schema)[:10]:
            print(f"    - {f}")
    
    # Phase 6: write detailed report
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_audit_report.md")
    with open(report_path, 'w') as rpt:
        rpt.write(f"# Active Oahu Tours Mirror - Site Audit Report\n\n")
        rpt.write(f"**Total HTML pages:** {len(files)}\n\n")
        
        rpt.write("## Category Breakdown\n\n")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            rpt.write(f"- **{cat}**: {count}\n")
        
        rpt.write(f"\n## Orphan Pages ({len(orphans)})\n\n")
        rpt.write("Pages with no other pages linking TO them (excluding homepage).\n\n")
        for o in sorted(orphans):
            rpt.write(f"- {o}\n")
        
        rpt.write(f"\n## Schema Markup\n\n")
        rpt.write(f"- Pages **with** schema markup: {len(has_schema)}\n")
        rpt.write(f"- Pages **without** schema markup: {len(missing_schema)}\n\n")
        
        rpt.write("### Pages Missing Schema Markup\n\n")
        for f in sorted(missing_schema):
            rpt.write(f"- {f}\n")
        
        rpt.write(f"\n## Complete Page Listing\n\n")
        for f in sorted(files):
            rpt.write(f"- {f}\n")
    
    print(f"\n=== REPORT WRITTEN TO: {report_path} ===")
    
    # Summary for stdout
    print(f"\n{'='*60}")
    print(f"SITE AUDIT SUMMARY")
    print(f"{'='*60}")
    print(f"Total pages: {len(files)}")
    print(f"Orphan pages: {len(orphans)}")
    print(f"Pages with schema markup: {len(has_schema)}")
    print(f"Pages missing schema markup: {len(missing_schema)}")
    
    # Check for homepage incoming count
    hp_incoming = incoming.get(homepage, set())
    print(f"\nHomepage incoming links: {len(hp_incoming)} sources")
    print(f"Pages that link to homepage: {sorted(hp_incoming)}")

if __name__ == '__main__':
    main()

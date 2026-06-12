#!/usr/bin/env python3
import re
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")
PRIORITY_FILE = Path("/home/ubuntu/work/active-oahu-static/site/_seo/schema-injection-plan/03-priority-order.md")

def parse_priority_pages():
    content = PRIORITY_FILE.read_text()
    # Find all file paths ending in .html in code ticks
    paths = re.findall(r'`([^`]+\.html)`', content)
    return set(paths)

def get_actual_pages():
    html_files = list(SITE_DIR.rglob("*.html"))
    filtered = []
    for f in html_files:
        rel = f.relative_to(SITE_DIR)
        rel_str = str(rel)
        if '_templates' not in rel_str and 'wp-content/themes' not in rel_str and 'wp-includes' not in rel_str:
            filtered.append(rel_str)
    return set(filtered)

def main():
    priority = parse_priority_pages()
    actual = get_actual_pages()
    
    print(f"Total priority pages in markdown: {len(priority)}")
    print(f"Total actual public HTML files: {len(actual)}")
    
    missing_files = priority - actual
    unlisted_files = actual - priority
    
    if missing_files:
        print("\n[WARNING] The following priority pages do NOT exist in the site directory:")
        for f in sorted(missing_files):
            print(f"  - {f}")
    else:
        print("\n[OK] All priority pages exist as physical files.")
        
    if unlisted_files:
        print("\n[WARNING] The following actual HTML files are NOT listed in the priority markdown:")
        for f in sorted(unlisted_files):
            print(f"  - {f}")
    else:
        print("\n[OK] All actual HTML files are listed in the priority markdown.")

if __name__ == '__main__':
    main()

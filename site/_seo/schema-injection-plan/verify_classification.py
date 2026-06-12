#!/usr/bin/env python3
import re
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")
CLASSIFICATION_FILE = Path("/home/ubuntu/work/active-oahu-static/site/_seo/schema-injection-plan/01-page-classification.md")

def parse_classified_pages():
    content = CLASSIFICATION_FILE.read_text()
    # Find all file paths ending in .html in the markdown file
    paths = re.findall(r'-\s+`([^`]+\.html)`', content)
    return set(paths)

def get_actual_pages():
    html_files = list(SITE_DIR.rglob("*.html"))
    # Filter templates and internal paths
    filtered = []
    for f in html_files:
        rel = f.relative_to(SITE_DIR)
        rel_str = str(rel)
        if '_templates' not in rel_str and 'wp-content/themes' not in rel_str and 'wp-includes' not in rel_str:
            filtered.append(rel_str)
    return set(filtered)

def main():
    classified = parse_classified_pages()
    actual = get_actual_pages()
    
    print(f"Total classified pages in markdown: {len(classified)}")
    print(f"Total actual public HTML files: {len(actual)}")
    
    missing_files = classified - actual
    unclassified_files = actual - classified
    
    if missing_files:
        print("\n[WARNING] The following classified pages do NOT exist in the site directory:")
        for f in sorted(missing_files):
            print(f"  - {f}")
    else:
        print("\n[OK] All classified pages exist as physical files.")
        
    if unclassified_files:
        print("\n[WARNING] The following actual HTML files are NOT listed in the classification markdown:")
        for f in sorted(unclassified_files):
            print(f"  - {f}")
    else:
        print("\n[OK] All actual HTML files are classified in the markdown.")

if __name__ == '__main__':
    main()

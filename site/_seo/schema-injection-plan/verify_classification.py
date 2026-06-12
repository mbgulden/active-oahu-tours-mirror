#!/usr/bin/env python3
import re
import os
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static-1212/site")
MD_FILE = Path("/home/ubuntu/work/active-oahu-static-1212/site/_seo/schema-injection-plan/01-page-classification.md")

def parse_md_classifications(file_path):
    classifications = {"EN": [], "JA": []}
    current_schema = None
    current_locale = None
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Check for ### Page Type Pages (Schema: `Type`)
            if line_str.startswith("### "):
                # Extract schema type inside backticks
                match = re.search(r"Schema:\s+`([^`]+)`", line_str)
                if match:
                    current_schema = match.group(1).strip()
                else:
                    current_schema = "Unknown"
                continue
                
            # Check for locale headers
            if "English Pages" in line_str or "#### English" in line_str or "(EN)" in line_str:
                current_locale = "EN"
                continue
            elif "Japanese Pages" in line_str or "#### Japanese" in line_str or "(JA)" in line_str:
                current_locale = "JA"
                continue
                
            # Parse list item
            if line_str.startswith("- `") and current_locale:
                match = re.search(r"- `([^`]+)`", line_str)
                if match:
                    path_str = match.group(1).strip()
                    classifications[current_locale].append({
                        "path": path_str,
                        "schema": current_schema
                    })
                    
    return classifications

EXCLUDE_EN_FILES = {
    "404.html",
    "author/mbgulden/index.html",
    "job/hiring-kayak-delivery-driver-jobs-in-laie/index.html",
    "job-dashboard/index.html",
    "contact-us.html",
    "trip-cancellation-insurance-terms-and-conditions.html",
    "activities.html",
    "activities/page/2/index.html",
    "activities/page/3/index.html",
    "oahu-equipment-rentals/page/2/index.html",
    "reviews/index.html",
    "reviews/page/2/index.html",
    "reviews/page/3/index.html",
    "reviews/page/4/index.html",
    "reviews/page/5/index.html",
    "about-active-oahu/index.html",
    "kailua-kayak/index.html",
    "kaneohe-sandbar/index.html",
    "kayak-kailua/index.html"
}

EXCLUDE_JA_FILES = {
    "ja/404.html",
    "ja/author/mbgulden/index.html",
    "ja/job/hiring-kayak-delivery-driver-jobs-in-laie/index.html",
    "ja/job-dashboard/index.html",
    "ja/activities/page/2/index.html",
    "ja/activities/page/3/index.html"
}

def scan_site_files(site_dir):
    html_files = []
    for root, dirs, files in os.walk(site_dir):
        # Skip internal system/template/includes/theme files
        if any(p in root for p in ["_templates", "_includes", "wp-content", "wp-includes", "_seo"]):
            continue
        for f in files:
            if f.endswith(".html"):
                p = Path(root) / f
                rel = p.relative_to(site_dir)
                rel_str = str(rel)
                if rel_str not in EXCLUDE_EN_FILES and rel_str not in EXCLUDE_JA_FILES:
                    html_files.append(rel_str)
    return sorted(html_files)

def main():
    print("=== Auditing Page Classification ===")
    if not MD_FILE.exists():
        print(f"Error: {MD_FILE} does not exist.")
        return
        
    classifications = parse_md_classifications(MD_FILE)
    site_files = scan_site_files(SITE_DIR)
    
    listed_en = classifications.get("EN", [])
    listed_ja = classifications.get("JA", [])
    
    print(f"Listed in MD: EN={len(listed_en)}, JA={len(listed_ja)} (Total={len(listed_en)+len(listed_ja)})")
    print(f"Actual HTML files on disk (filtered): Total={len(site_files)}")
    
    # Check disk existence for listed files
    print("\n--- Checking Listed Files Existence on Disk ---")
    en_missing_on_disk = []
    ja_missing_on_disk = []
    
    for item in listed_en:
        p = item["path"]
        if not (SITE_DIR / p).exists():
            en_missing_on_disk.append(p)
            
    for item in listed_ja:
        p = item["path"]
        if not (SITE_DIR / p).exists():
            ja_missing_on_disk.append(p)
            
    print(f"EN listed but missing on disk ({len(en_missing_on_disk)}):")
    for p in en_missing_on_disk:
        print(f"  - {p}")
        
    print(f"JA listed but missing on disk ({len(ja_missing_on_disk)}):")
    for p in ja_missing_on_disk:
        print(f"  - {p}")
        
    # Check disk files not listed in MD
    print("\n--- Checking Disk Files Not Listed in MD ---")
    listed_paths = set([item["path"] for item in listed_en + listed_ja])
    unlisted_files = []
    for f in site_files:
        if f not in listed_paths:
            unlisted_files.append(f)
            
    print(f"Files on disk but not listed in MD ({len(unlisted_files)}):")
    for f in unlisted_files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import re
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static-1212/site")
MD_CLASSIFICATION = Path("/home/ubuntu/work/active-oahu-static-1212/site/_seo/schema-injection-plan/01-page-classification.md")
MD_PRIORITY = Path("/home/ubuntu/work/active-oahu-static-1212/site/_seo/schema-injection-plan/03-priority-order.md")

def parse_priority_pages(file_path):
    pages = []
    current_tier = None
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Check for Tier Headings
            if line_str.startswith("## P0"):
                current_tier = "P0"
                continue
            elif line_str.startswith("## P1"):
                current_tier = "P1"
                continue
            elif line_str.startswith("## P2"):
                current_tier = "P2"
                continue
            elif line_str.startswith("## P3"):
                current_tier = "P3"
                continue
                
            # Parse table row
            if line_str.startswith("|") and not line_str.startswith("| :---") and not line_str.startswith("| Rank") and not line_str.startswith("| Relative Path"):
                parts = [p.strip() for p in line_str.split("|")]
                if len(parts) >= 4:
                    path_str = ""
                    if parts[1].isdigit():
                        path_str = parts[2]
                    else:
                        path_str = parts[1]
                    
                    path_str = path_str.replace("`", "")
                    if path_str:
                        pages.append({
                            "path": path_str,
                            "tier": current_tier
                        })
    return pages

def parse_md_classifications(file_path):
    classifications = []
    current_locale = None
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
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
                    classifications.append(path_str)
                    
    return classifications

def main():
    print("=== Auditing Schema Priority Order ===")
    if not MD_PRIORITY.exists():
        print(f"Error: {MD_PRIORITY} does not exist.")
        return
        
    priority_pages = parse_priority_pages(MD_PRIORITY)
    classified_pages = parse_md_classifications(MD_CLASSIFICATION)
    
    print(f"Total pages listed in Priority Order: {len(priority_pages)}")
    print(f"Total pages classified in Classifications: {len(classified_pages)}")
    
    # Check disk existence for priority pages
    print("\n--- Checking Priority Pages Existence on Disk ---")
    missing_on_disk = []
    for item in priority_pages:
        p = item["path"]
        if not (SITE_DIR / p).exists():
            missing_on_disk.append(f"{p} ({item['tier']})")
            
    print(f"Priority pages missing on disk ({len(missing_on_disk)}):")
    for p in missing_on_disk:
        print(f"  - {p}")
        
    # Check sync between Classifications and Priority Order
    print("\n--- Checking Classification vs Priority Sync ---")
    priority_paths = set([item["path"] for item in priority_pages])
    classified_paths = set(classified_pages)
    
    not_in_priority = [p for p in classified_pages if p not in priority_paths]
    not_in_classification = [p for p in priority_paths if p not in classified_paths]
    
    print(f"Classified but not in Priority list ({len(not_in_priority)}):")
    for p in not_in_priority:
        print(f"  - {p}")
        
    print(f"In Priority list but not in Classification list ({len(not_in_classification)}):")
    for p in not_in_classification:
        print(f"  - {p}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import re
from pathlib import Path

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")
PLAN_DIR = SITE_DIR / "_seo/schema-injection-plan"
CLASS_FILE = PLAN_DIR / "01-page-classification.md"
PRIORITY_FILE = PLAN_DIR / "03-priority-order.md"

# Import helper functions
import sys
sys.path.append(str(PLAN_DIR))
import verify_classification
import verify_priority

def main():
    # 1. Get current classifications
    classifications = verify_classification.get_listed_pages()
    
    # 2. Get current priority tiers
    tiers = verify_priority.get_priority_pages()
    p0 = set(tiers["P0"])
    p1 = set(tiers["P1"])
    
    # 3. Identify all English HTML files on disk
    en_on_disk = []
    for p in SITE_DIR.rglob("*.html"):
        rel_path = p.relative_to(SITE_DIR)
        rel_str = str(rel_path)
        # Skip templates, includes, wp-content, wp-includes, and Japanese pages
        if any(x in rel_str for x in ('_templates', '_includes', 'wp-content', 'wp-includes')):
            continue
        if rel_str.startswith("ja/"):
            continue
        en_on_disk.append(rel_str)
        
    # 4. Filter out P0 and P1 pages to get P2 pages
    p2_pages = sorted([p for p in en_on_disk if p not in p0 and p not in p1])
    
    # 5. Format P2 pages table
    p2_rows = ["| Relative Path | Page Type | Primary Schema Type |", "| :--- | :--- | :--- |"]
    
    # Mapping schema name to readable Page Type
    schema_to_type = {
        "Article": "Blog/Guide",
        "ContactPage": "Contact",
        "FAQPage": "FAQ",
        "TravelAgency + LocalBusiness + Travel": "Homepage",
        "ItemList + TouristAttraction": "Location/Hub",
        "WebPage": "Other",
        "Product": "Rental",
        "TouristTrip": "Tour"
    }
    
    for p in p2_pages:
        info = classifications.get(p)
        if not info:
            print(f"Warning: {p} not found in classifications!")
            continue
        schema = info["schema"]
        pg_type = schema_to_type.get(schema, "Other")
        # Handle compound schema display
        schema_display = f"`{schema}`"
        p2_rows.append(f"| `{p}` | {pg_type} | {schema_display} |")
        
    p2_table_content = "\n".join(p2_rows)
    
    # 6. Load current 03-priority-order.md and replace sections
    content = PRIORITY_FILE.read_text()
    
    # Update P2 section
    p2_pattern = re.compile(
        r'(## P2: Remaining English Pages \(.*?\)\n\nThese pages cover.*?\n\n<details>\n<summary>Click to expand P2 page list</summary>\n\n).*?(\n\n</details>)',
        re.DOTALL
    )
    
    new_header = f"## P2: Remaining English Pages ({len(p2_pages)} pages)"
    # Replace header and table
    content = re.sub(
        r'## P2: Remaining English Pages \(.*?\)',
        new_header,
        content
    )
    
    # Find the range inside <details> and replace table
    start_marker = "<summary>Click to expand P2 page list</summary>\n\n"
    end_marker = "\n\n</details>"
    
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find P2 detail tags.")
        return
        
    content = content[:start_idx] + p2_table_content + content[end_idx:]
    
    # 7. Update P3 header to 89 JA pages
    content = re.sub(
        r'## P3: Japanese Locale Pages \(All \d+ JA pages\)',
        "## P3: Japanese Locale Pages (All 89 JA pages)",
        content
    )
    content = re.sub(
        r'\* \*\*P3: Japanese Locale Pages \(All \d+ JA pages\)\*\*',
        "* **P3: Japanese Locale Pages (All 89 JA pages)**",
        content
    )
    
    # Write back the updated file
    PRIORITY_FILE.write_text(content)
    print(f"Successfully updated {PRIORITY_FILE} with {len(p2_pages)} P2 pages and updated P3 header!")

if __name__ == "__main__":
    main()

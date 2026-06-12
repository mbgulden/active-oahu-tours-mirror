#!/usr/bin/env python3
import re
from pathlib import Path

CLASSIFICATION_PATH = Path(__file__).resolve().parent / "01-page-classification.md"
PRIORITY_PATH = Path(__file__).resolve().parent / "03-priority-order.md"


NON_EXISTENT_FILES = {
    "_includes/tide-chart-template.html",
    "_templates/body_bottom.html",
    "_templates/body_top.html",
    "_templates/head.html",
    "tides/hauula.html",
    "tides/kaaawa.html",
    "tides/kahana.html",
    "tides/kahuku.html",
    "tides/kailua.html",
    "tides/kaneohe-bay.html",
    "tides/kaneohe.html",
    "tides/kualoa.html",
    "tides/laie.html",
    "tides/lanikai.html",
    "tides/mokolii.html",
    "tides/mokulua-islands.html",
    "tides/punaluu.html",
    "tides/turtle-bay.html",
    "tides/waihole.html",
    "tides/waikane.html",
    "tides/waimanalo.html"
}

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

ADD_FILES = {
    "Tour": [
        "activities/kawela-bay-self-guided-kayak-tour/index.html",
        "chinamans-hat-kayak-tour/index.html",
        "kaneohe-bay-sandbar-kayak/index.html"
    ],
    "Rental": [
        "rentals/snorkel-gear-rentals/index.html",
        "stand-up-paddleboard-rental/index.html"
    ],
    "Blog/Guide": [
        "guides/oahu-kayak-safety-tide-guide/index.html"
    ],
    "Other": [
        "oahu-kayak-safety-tide-index-map/index.html"
    ]
}

CATEGORIES = [
    ("Blog/Guide", "Blog/Guide Pages", "Article"),
    ("Contact", "Contact Pages", "ContactPage"),
    ("FAQ", "FAQ Pages", "FAQPage"),
    ("Homepage", "Homepage Pages", "Travel"),
    ("Location/Hub", "Location/Hub Pages", "ItemList + TouristAttraction"),
    ("Other", "Other Pages", "WebPage"),
    ("Rental", "Rental Pages", "Product"),
    ("Tour", "Tour Pages", "TouristTrip")
]

def parse_classification_file():
    content = CLASSIFICATION_PATH.read_text()
    lines = content.split('\n')
    
    current_category = None
    current_locale = None
    
    # Structure: category -> locale -> list of files
    data = {cat[0]: {"EN": [], "JA": []} for cat in CATEGORIES}
    
    for line in lines:
        line_str = line.strip()
        if line_str.startswith("### "):
            # Detect category
            current_category = None
            for cat, title, _ in CATEGORIES:
                if title in line_str:
                    current_category = cat
                    break
        elif line_str.startswith("#### "):
            # Detect locale
            if "English Pages" in line_str:
                current_locale = "EN"
            elif "Japanese Pages" in line_str:
                current_locale = "JA"
        elif line_str.startswith("- `"):
            m = re.match(r'^-\s+`([^`]+)`', line_str)
            if m:
                file_path = m.group(1)
                if (file_path not in NON_EXISTENT_FILES and 
                    file_path not in EXCLUDE_EN_FILES and 
                    file_path not in EXCLUDE_JA_FILES):
                    if current_category and current_locale:
                        data[current_category][current_locale].append(file_path)
                        
    # Add new files
    for cat, files in ADD_FILES.items():
        for f in files:
            if f not in EXCLUDE_EN_FILES and f not in data[cat]["EN"]:
                data[cat]["EN"].append(f)
                
    # Sort everything
    for cat in data:
        data[cat]["EN"] = sorted(list(set(data[cat]["EN"])))
        data[cat]["JA"] = sorted(list(set(data[cat]["JA"])))
        
    return data

def write_classification_file(data):
    # Rebuild the file
    out = []
    out.append("# Page Type Classification Plan")
    out.append("")
    out.append("This document contains the schema classification for every page on the Active Oahu Tours (AOT) website, covering English (EN) and Japanese (JA) locales.")
    out.append("")
    out.append("## Summary Counts")
    out.append("")
    out.append("| Page Type | Locale | Schema Type | Page Count |")
    out.append("| :--- | :--- | :--- | :--- |")
    
    for cat, _, schema in sorted(CATEGORIES, key=lambda x: x[0]):
        out.append(f"| {cat} | EN | {schema} | {len(data[cat]['EN'])} |")
        out.append(f"| {cat} | JA | {schema} | {len(data[cat]['JA'])} |")
        
    out.append("")
    out.append("## Detailed Page Mapping")
    out.append("")
    
    for cat, title, schema in CATEGORIES:
        out.append(f"### {title} (Schema: `{schema}`)")
        out.append("")
        out.append("#### English Pages (EN)")
        for f in data[cat]["EN"]:
            out.append(f"- `{f}`")
        out.append("")
        out.append("#### Japanese Pages (JA)")
        for f in data[cat]["JA"]:
            out.append(f"- `{f}`")
        out.append("")
        
    CLASSIFICATION_PATH.write_text("\n".join(out))
    print("Rewritten 01-page-classification.md successfully!")

def update_priority(data):
    content = PRIORITY_PATH.read_text()
    
    # Collect EN files and JA files
    all_en_files = []
    all_ja_files = []
    
    page_type_map = {}
    schema_map = {}
    
    for cat, _, schema in CATEGORIES:
        for f in data[cat]["EN"]:
            all_en_files.append(f)
            page_type_map[f] = cat
            schema_map[f] = schema
        for f in data[cat]["JA"]:
            all_ja_files.append(f)
            page_type_map[f] = cat
            schema_map[f] = schema
            
    all_en_files_set = set(all_en_files)
    all_ja_files = sorted(list(set(all_ja_files)))
    
    # Extract existing order of EN pages from priority-order.md
    # (P0, then P1, then P2) to preserve traffic rank
    ordered_en_from_md = []
    
    # Match all code-ticked paths in the file
    all_matches = re.findall(r'`([^`]+\.html)`', content)
    for m in all_matches:
        if m in all_en_files_set and m not in ordered_en_from_md:
            ordered_en_from_md.append(m)
            
    # Add any remaining EN files that weren't in the markdown yet
    for f in sorted(all_en_files):
        if f not in ordered_en_from_md:
            ordered_en_from_md.append(f)
            
    # Rebuild P0 and P1 lists
    p0_files = ordered_en_from_md[:20]
    p1_files = ordered_en_from_md[20:50]
    p2_files = sorted(ordered_en_from_md[50:])
    
    # Build tables
    def build_p0_p1_table(files, start_rank=1):
        table = [
            "| Rank | Relative Path | Page Type | Primary Schema Type |",
            "| :--- | :--- | :--- | :--- |"
        ]
        for idx, f in enumerate(files):
            rank = start_rank + idx
            pt = page_type_map.get(f, "Other")
            st = schema_map.get(f, "WebPage")
            table.append(f"| {rank} | `{f}` | {pt} | `{st}` |")
        return "\n".join(table)
        
    def build_p2_p3_table(files):
        table = [
            "| Relative Path | Page Type | Primary Schema Type |",
            "| :--- | :--- | :--- |"
        ]
        for f in files:
            pt = page_type_map.get(f, "Other")
            st = schema_map.get(f, "WebPage")
            table.append(f"| `{f}` | {pt} | `{st}` |")
        return "\n".join(table)
        
    p0_table_str = build_p0_p1_table(p0_files, start_rank=1)
    p1_table_str = build_p0_p1_table(p1_files, start_rank=21)
    p2_table_str = build_p2_p3_table(p2_files)
    p3_table_str = build_p2_p3_table(all_ja_files)
    
    out = []
    out.append("# Schema Injection Priority Order")
    out.append("")
    out.append("This document details the rank-order injection schedule based on a traffic x schema gap calculation.")
    out.append("")
    out.append(f"* **P0: Top-20 High-Value Pages (Highest organic ROI)**")
    out.append(f"* **P1: Mid-Traffic Core Pages (Pages 21-50)**")
    out.append(f"* **P2: Remaining English Pages ({len(p2_files)} pages)**")
    out.append(f"* **P3: Japanese Locale Pages (All {len(all_ja_files)} JA pages)**")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## P0: Top-20 High-Traffic Pages (Highest ROI)")
    out.append("")
    out.append("These 20 pages drive over 75% of organic traffic and direct bookings for AOT. Injecting high-quality schema here offers immediate rich result opportunities.")
    out.append("")
    out.append(p0_table_str)
    out.append("")
    out.append("---")
    out.append("")
    out.append("## P1: Mid-Traffic Core Pages (Pages 21-50)")
    out.append("")
    out.append("These pages cover secondary tours, popular equipment rentals, and high-impression blogs.")
    out.append("")
    out.append(p1_table_str)
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"## P2: Remaining English Pages ({len(p2_files)} pages)")
    out.append("")
    out.append("These pages cover supporting blog posts, pagination pages, policy terms, and minor utilities.")
    out.append("")
    out.append("<details>")
    out.append("<summary>Click to expand P2 page list</summary>")
    out.append("")
    out.append(p2_table_str)
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"## P3: Japanese Locale Pages (All {len(all_ja_files)} JA pages)")
    out.append("")
    out.append("Japanese language versions of all core and supporting pages.")
    out.append("")
    out.append("<details>")
    out.append("<summary>Click to expand P3 page list</summary>")
    out.append("")
    out.append(p3_table_str)
    out.append("")
    out.append("</details>")
    
    PRIORITY_PATH.write_text("\n".join(out))
    print("Rewritten 03-priority-order.md successfully!")

def main():
    data = parse_classification_file()
    write_classification_file(data)
    update_priority(data)

if __name__ == '__main__':
    main()

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
    ("Homepage", "Homepage Pages", "TravelAgency + LocalBusiness + Travel"),
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
                if file_path not in NON_EXISTENT_FILES:
                    if current_category and current_locale:
                        data[current_category][current_locale].append(file_path)
                        
    # Add new files
    for cat, files in ADD_FILES.items():
        for f in files:
            if f not in data[cat]["EN"]:
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
            
    # Include 404.html to EN files
    if "404.html" not in all_en_files:
        all_en_files.append("404.html")
    page_type_map["404.html"] = "Other"
    schema_map["404.html"] = "WebPage"
    
    all_en_files = set(all_en_files)
    all_ja_files = sorted(list(set(all_ja_files)))
    
    # Read existing P0 and P1 from priority-order.md
    p0_pattern = r'\|\s*\d+\s*\|\s*`([^`]+)`'
    p0_matches = re.findall(p0_pattern, content)
    
    p0_files = p0_matches[:20]
    p1_files = p0_matches[20:50]
    
    # Ensure they exist in our current EN files list
    p0_files = [f for f in p0_files if f in all_en_files]
    p1_files = [f for f in p1_files if f in all_en_files]
    
    # P2 files are the remaining EN files
    p2_files = sorted(list(all_en_files - set(p0_files) - set(p1_files)))
    
    # Rebuild tables
    def build_table(files):
        table = [
            "| Relative Path | Page Type | Primary Schema Type |",
            "| :--- | :--- | :--- |"
        ]
        for f in files:
            pt = page_type_map.get(f, "Other")
            st = schema_map.get(f, "WebPage")
            table.append(f"| `{f}` | {pt} | `{st}` |")
        return "\n".join(table)
        
    p2_table_str = build_table(p2_files)
    p3_table_str = build_table(all_ja_files)
    
    # Replace sections in file
    sections = re.split(r'(##\s+)', content)
    
    for i in range(1, len(sections), 2):
        header_marker = sections[i]
        sec_body = sections[i+1]
        sec_title = sec_body.split('\n')[0]
        
        if "P2:" in sec_title:
            new_title = f"P2: Remaining English Pages ({len(p2_files)} pages)\n"
            intro = "\nThese pages cover supporting blog posts, pagination pages, policy terms, and minor utilities.\n\n<details>\n<summary>Click to expand P2 page list</summary>\n\n"
            outro = "\n</details>\n"
            sec_body = new_title + intro + p2_table_str + outro
        elif "P3:" in sec_title:
            new_title = f"P3: Japanese Locale Pages (All {len(all_ja_files)} JA pages)\n"
            intro = "\nJapanese language versions of all core and supporting pages.\n\n<details>\n<summary>Click to expand P3 page list</summary>\n\n"
            outro = "\n</details>\n"
            sec_body = new_title + intro + p3_table_str + outro
            
        sections[i+1] = sec_body
        
    PRIORITY_PATH.write_text("".join(sections))
    print("Rewritten 03-priority-order.md successfully!")

def main():
    data = parse_classification_file()
    write_classification_file(data)
    update_priority(data)

if __name__ == '__main__':
    main()

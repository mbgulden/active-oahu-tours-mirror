#!/usr/bin/env python3
import os
import re

SITE = "/home/ubuntu/work/active-oahu-static/site"

pages_to_update = {
    "chinamans-hat/index.html": [
        ("Mokoliʻi Island", "mokolii"),
        ("Kualoa", "kualoa"),
        ("Kahana", "kahana")
    ],
    "mokolii/index.html": [
        ("Mokoliʻi Island", "mokolii"),
        ("Kualoa", "kualoa"),
        ("Kahana", "kahana")
    ],
    "kaneohe-sandbar/index.html": [
        ("Kāneʻohe Bay", "kaneohe-bay"),
        ("Kāneʻohe", "kaneohe"),
        ("Waikāne", "waikane"),
        ("Wāihole", "waihole")
    ],
    "kailua-kayak/index.html": [
        ("Kailua", "kailua"),
        ("Lanikai", "lanikai"),
        ("Mokulua Islands", "mokulua-islands"),
        ("Waimānalo", "waimanalo")
    ],
    "kayak-kailua/index.html": [
        ("Kailua", "kailua"),
        ("Lanikai", "lanikai"),
        ("Mokulua Islands", "mokulua-islands"),
        ("Waimānalo", "waimanalo")
    ],
    "laie-bay-goat-island-kayaking/index.html": [
        ("Lāʻie Bay", "laie"),
        ("Hāʻula", "hauula"),
        ("Kahuku", "kahuku")
    ],
    "sharks-cove-snorkeling/index.html": [
        ("Turtle Bay", "turtle-bay"),
        ("Kaʻaʻawa", "kaaawa"),
        ("Punaluʻu", "punaluu")
    ]
}

print("Adding interactive tide guide links to tour pages...\n")

for page_rel_path, links in pages_to_update.items():
    file_path = f"{SITE}/{page_rel_path}"
    if not os.path.exists(file_path):
        print(f"  Warning: {page_rel_path} does not exist. Skipping.")
        continue
        
    with open(file_path, 'r') as f:
        content = f.read()
        
    # Build the HTML block
    links_html = ""
    for name, slug in links:
        links_html += f'        <a href="/tides/{slug}.html" style="display: inline-block; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 9999px; padding: 8px 16px; font-size: 13px; font-weight: 600; color: #1e293b; text-decoration: none; transition: all 0.2s ease; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin: 4px;" onmouseover="this.style.borderColor=\'#2b6cb0\'; this.style.color=\'#2b6cb0\';" onmouseout="this.style.borderColor=\'#cbd5e1\'; this.style.color=\'#1e293b\';">{name} Tide Chart &rarr;</a>\n'
        
    block = f"""
    <!-- START INTERACTIVE TIDE LINKS SECTION -->
    <div class="tide-guides-section" style="margin: 40px auto; max-width: 900px; padding: 24px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; font-family: 'Lato', sans-serif; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
        <h4 style="margin-top: 0; margin-bottom: 8px; color: #2b6cb0; font-size: 18px; font-weight: 700; font-family: 'Open Sans Condensed', sans-serif; text-transform: uppercase;">Local Interactive Tide Charts</h4>
        <p style="margin-bottom: 16px; font-size: 14px; color: #4a5568; line-height: 1.5;">Plan your paddle adventure with our real-time localized tide guides for nearby launch sites:</p>
        <div style="display: flex; flex-wrap: wrap; margin: -4px;">
{links_html}        </div>
    </div>
    <!-- END INTERACTIVE TIDE LINKS SECTION -->
    """
    
    # Remove existing section if present (to make the script idempotent)
    pattern = r'<!-- START INTERACTIVE TIDE LINKS SECTION -->.*?<!-- END INTERACTIVE TIDE LINKS SECTION -->'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Find the end of entry-content div
    target = '</div><!-- .entry-content -->'
    if target in content:
        new_content = content.replace(target, f"{block}\n    {target}")
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"  Updated {page_rel_path} with {len(links)} links.")
    else:
        print(f"  Warning: Target tag '{target}' not found in {page_rel_path}. Link section not added.")

print("\nDone adding links.")

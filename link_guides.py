#!/usr/bin/env python3
"""Link the five Windward Oahu guides to inter-link with each other across both repos."""
import os
import re

REPOS = [
    "/home/ubuntu/work/active-oahu-static",
    "/home/ubuntu/work/active-oahu-tours-mirror"
]

all_guides = [
    {
        "slug": "kailua-beach-park",
        "title": "Kailua Beach Park Guide",
        "url": "/guides/kailua-beach-park/"
    },
    {
        "slug": "lanikai-beach",
        "title": "Lanikai Beach Guide",
        "url": "/guides/lanikai-beach/"
    },
    {
        "slug": "waimanalo-beach",
        "title": "Waimanalo Beach Guide",
        "url": "/guides/waimanalo-beach/"
    },
    {
        "slug": "lanikai-pillbox-hike",
        "title": "Lanikai Pillbox Hike Guide",
        "url": "/guides/lanikai-pillbox-hike/"
    },
    {
        "slug": "kailua-vs-lanikai",
        "title": "Kailua vs. Lanikai Beach Guide",
        "url": "/guides/kailua-vs-lanikai/"
    }
]

def generate_related_block(current_slug):
    links = []
    for g in all_guides:
        if g["slug"] != current_slug:
            links.append(f'<a href="{g["url"]}" style="display: block; padding: 12px; background: #ffffff; border: 1px solid #dee2e6; border-radius: 6px; text-decoration: none; color: #006699; font-weight: bold; transition: all 0.2s ease-in-out; text-align: center;" onmouseover="this.style.background=\'#f1f3f5\'; this.style.borderColor=\'#ced4da\'" onmouseout="this.style.background=\'#ffffff\'; this.style.borderColor=\'#dee2e6\'">{g["title"]} →</a>')
    
    links_html = "\n        ".join(links)
    
    return f"""
<!-- START RELATED GUIDES SECTION -->
<div class="related-guides-section" style="margin-top: 40px; padding: 25px; background: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef; clear: both;">
    <h3 style="margin-top: 0; margin-bottom: 20px; color: #333; font-size: 1.5rem; border-bottom: 2px solid #dee2e6; padding-bottom: 10px;">Related Windward Coast Guides</h3>
    <div class="related-guides-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
        {links_html}
    </div>
</div>
<!-- END RELATED GUIDES SECTION -->
"""

print("Inter-linking Windward Coast location guides...")

for repo in REPOS:
    site_dir = f"{repo}/site"
    if not os.path.exists(site_dir):
        print(f"  ⚠️ Skip: Directory not found: {site_dir}")
        continue

    for guide in all_guides:
        file_path = f"{site_dir}/guides/{guide['slug']}/index.html"
        if not os.path.exists(file_path):
            print(f"  ⚠️ Warning: File not found: {file_path}")
            continue

        with open(file_path, "r") as f:
            content = f.read()

        # Remove existing related guides section if any
        content = re.sub(
            r'<!-- START RELATED GUIDES SECTION -->.*?<!-- END RELATED GUIDES SECTION -->',
            '',
            content,
            flags=re.DOTALL
        )

        related_block = generate_related_block(guide["slug"])

        # We inject the block inside the content column.
        # For our generated pages and existing pages, they have:
        # </div>\n</div>\n</section>\n</div>\n</div><!-- .entry-content -->
        # We replace the first occurrence of:
        # </div>\n</div>\n</section>\n</div>\n</div><!-- .entry-content -->
        # with:
        # {related_block}\n</div>\n</div>\n</section>\n</div>\n</div><!-- .entry-content -->
        target = "</div>\n</div>\n</section>\n</div>\n</div><!-- .entry-content -->"
        target_alt = "</div></div></section></div></div><!-- .entry-content -->"
        
        if target in content:
            new_content = content.replace(target, related_block + "\n" + target, 1)
        elif target_alt in content:
            new_content = content.replace(target_alt, related_block + "\n" + target_alt, 1)
        else:
            # Fallback: find </div><!-- .entry-content -->
            target_fallback = "</div><!-- .entry-content -->"
            if target_fallback in content:
                new_content = content.replace(target_fallback, related_block + "\n" + target_fallback, 1)
            else:
                print(f"  ❌ Error: Could not find insertion marker in {file_path}")
                continue

        with open(file_path, "w") as f:
            f.write(new_content)
        print(f"  ✅ Updated: {file_path}")

print("Inter-linking completed successfully.")

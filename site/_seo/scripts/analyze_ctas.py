import os
import re
from bs4 import BeautifulSoup
import json

site_dir = "/home/ubuntu/work/active-oahu-static/site"

def audit_site_ctas():
    results = {}
    
    # Walk site directory and find html files
    for root, dirs, files in os.walk(site_dir):
        # Skip wp-content, wp-includes, fonts, ja (to avoid duplicates unless needed)
        if any(p in root for p in ["wp-content", "wp-includes", "fonts.gstatic.com", "/ja/"]):
            continue
            
        for file in files:
            if file == "index.html" or file.endswith(".html"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, site_dir)
                
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    soup = BeautifulSoup(content, "html.parser")
                    
                    # Find all CTAs (buttons, links that look like buttons, or FareHarbor links)
                    ctas = []
                    
                    # 1. FareHarbor links
                    fh_links = soup.find_all("a", href=re.compile(r"fareharbor\.com"))
                    for a in fh_links:
                        text = a.get_text(strip=True)
                        onclick = a.get("onclick", "")
                        href = a.get("href", "")
                        classes = a.get("class", [])
                        
                        ctas.append({
                            "type": "FareHarbor Link",
                            "text": text,
                            "href": href,
                            "onclick": onclick,
                            "classes": classes,
                            "location": "body" # we'll refine this
                        })
                        
                    # 2. Other button-like links (class containing 'btn' or 'button')
                    btn_links = soup.find_all("a", class_=re.compile(r"btn|button"))
                    for a in btn_links:
                        # Skip if already captured in FH links
                        if a in fh_links:
                            continue
                        text = a.get_text(strip=True)
                        href = a.get("href", "")
                        classes = a.get("class", [])
                        
                        ctas.append({
                            "type": "Button Link",
                            "text": text,
                            "href": href,
                            "classes": classes
                        })
                        
                    if ctas:
                        results[rel_path] = ctas
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    # Output results to a json file
    output_path = "/home/ubuntu/work/active-oahu-static/site/_seo/data/cta_inventory.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"CTA Audit complete. Saved inventory of {len(results)} pages to {output_path}")

if __name__ == "__main__":
    audit_site_ctas()

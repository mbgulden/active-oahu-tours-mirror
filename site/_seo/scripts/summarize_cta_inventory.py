import json
import os

inventory_path = "/home/ubuntu/work/active-oahu-static/site/_seo/data/cta_inventory.json"

def main():
    if not os.path.exists(inventory_path):
        print("Inventory file not found.")
        return
        
    with open(inventory_path) as f:
        data = json.load(f)
        
    print(f"Total pages with CTAs: {len(data)}")
    
    # Categorize pages
    categories = {
        "homepage": [],
        "activities/tours": [],
        "rentals": [],
        "guides": [],
        "others": []
    }
    
    for path, ctas in data.items():
        if path == "index.html":
            categories["homepage"].append((path, ctas))
        elif "activities/" in path:
            categories["activities/tours"].append((path, ctas))
        elif "rentals/" in path or "equipment-rentals" in path:
            categories["rentals"].append((path, ctas))
        elif "guides/" in path or "kayaking-guide" in path or "launch-guide" in path:
            categories["guides"].append((path, ctas))
        else:
            categories["others"].append((path, ctas))
            
    for cat, items in categories.items():
        print(f"\nCategory '{cat}': {len(items)} pages")
        for path, ctas in items[:5]:
            print(f"  {path}: {len(ctas)} CTAs")
            for c in ctas[:3]:
                txt = c.get("text", "")
                typ = c.get("type", "Unknown")
                href = c.get("href", "")
                print(f"    - [{typ}] '{txt}' -> {href[:60]}")
                
    # Let's count pages with no FareHarbor links
    no_fh_pages = []
    for path, ctas in data.items():
        has_fh = any(c.get("type") == "FareHarbor Link" for c in ctas)
        if not has_fh:
            no_fh_pages.append(path)
            
    print(f"\nPages with NO FareHarbor booking links: {len(no_fh_pages)}")
    for p in no_fh_pages[:10]:
        print(f"  - {p}")

if __name__ == "__main__":
    main()

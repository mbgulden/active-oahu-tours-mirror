import json

with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/serp_analyses.json") as f:
    serp_data = json.load(f)

for kw, data in serp_data.items():
    print(f"\nKeyword: {kw}")
    if "error" in data:
        print(f"  ERROR: {data['error']}")
        continue
    
    entries = data.get("serpEntries", [])
    if not entries:
        print("  No SERP entries found.")
        continue
        
    print(f"  {'Pos':<3} | {'Domain':<30} | {'Clicks':<8} | {'Title':<40}")
    print(f"  {'-'*3}+{'-'*32}+{'-'*10}+{'-'*42}")
    for entry in entries:
        pos = entry.get("position")
        dom = entry.get("domain", "")
        clicks = entry.get("clicks") or 0
        title = (entry.get("title") or "")[:40]
        # Highlight our domain
        flag = " *" if "activeoahutours.com" in dom else ""
        print(f"  {pos:<3} | {dom + flag:<30} | {clicks:<8} | {title:<40}")

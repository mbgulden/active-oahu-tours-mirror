import json
import os

base_dir = "/home/ubuntu/work/active-oahu-static/site/_seo/data"
behavior_file = os.path.join(base_dir, "google-analytics/ga4_user-behavior_30d.json")
conversions_file = os.path.join(base_dir, "google-analytics/ga4_conversions_90d.json")

with open(behavior_file) as f:
    behavior_data = json.load(f)
    
with open(conversions_file) as f:
    conversions_data = json.load(f)

convs_90d = {}
for r in conversions_data.get("rows", []):
    event = r["dimensionValues"][0]["value"]
    path = r["dimensionValues"][1]["value"]
    val = float(r["metricValues"][0]["value"])
    if event == "purchase":
        convs_90d[path] = convs_90d.get(path, 0.0) + val

rows = behavior_data.get("rows", [])
count = 0

print("| # | Landing Page Path | 30D Sessions | Bounce Rate | Avg. Duration | 90D Purchases | Conv. Rate (Est.) | Status & Issues |")
print("|---|---|---|---|---|---|---|---|")

for r in rows:
    path = r["dimensionValues"][0]["value"]
    if "/embeds/" in path or "calendar" in path or "cart" in path:
        continue
    count += 1
    sess = int(r["metricValues"][0]["value"])
    bounce = float(r["metricValues"][1]["value"]) * 100
    duration = float(r["metricValues"][2]["value"])
    
    # Try to find 90D purchases for this path
    norm_path = path.rstrip("/")
    purchases = 0.0
    for p, v in convs_90d.items():
        if p.rstrip("/") == norm_path:
            purchases += v
            
    # For "/" vs "" homepages
    if norm_path == "":
        purchases += convs_90d.get("/", 0.0)
        purchases += convs_90d.get("", 0.0)
            
    est_conv_rate = (purchases / (3.0 * sess)) * 100 if sess > 0 else 0.0
    
    # We can assign statuses based on performance and path
    status = "🟢 Healthy"
    issues = "No critical conversion leaks."
    
    if path == "/":
        status = "🔴 Critical Leak"
        issues = "Generic header booking links; lack of direct product CTAs."
    elif "sharks-cove" in path:
        status = "🚨 Severe Friction"
        issues = "Kailua storefront gear pickup required for North Shore activity."
    elif "chinamans-hat-kayak-rentals" in path:
        status = "🟢 Healthy"
        issues = "Direct product match, clear local pickup instructions."
    elif path == "/activities/":
        status = "實 Weak"
        status = "🟡 Weak"
        issues = "High engagement but low booking initiation."
    elif "kaneohe-sandbar-kayak-experience" in path:
        status = "🟢 Healthy"
        issues = "High engagement, good intent conversion."
    elif path == "/oahu-equipment-rentals/":
        status = "🟡 Weak"
        issues = "Broad listing page, users drop off without selecting a specific product."
    elif path == "/rentals/oahu-tandem-kayak-rentals/":
        status = "🟢 Top Performer"
        issues = "Strong commercial intent, direct booking alignment."
    elif "kahana-rainforest-river" in path:
        status = "🔴 Friction"
        issues = "Underperforming river kayak tour page; weak CTA hierarchy."
    elif purchases == 0.0 and sess > 50:
        status = "🟡 Underperforming"
        issues = "Zero purchases over 90 days despite traffic."
    elif est_conv_rate > 1.5:
        status = "🟢 High Conv"
        issues = "Highly optimized landing page conversion."
        
    print(f"| {count} | `{path}` | {sess} | {bounce:.1f}% | {duration:.1f}s | {int(purchases)} | {est_conv_rate:.2f}% | {status}: {issues} |")
    if count == 20:
        break

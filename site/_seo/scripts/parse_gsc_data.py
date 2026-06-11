import json
import os
from collections import defaultdict

gsc_file = "/home/ubuntu/work/active-oahu-static/site/_seo/raw/gsc_ja_search_analytics.json"

if not os.path.exists(gsc_file):
    print("GSC data file does not exist.")
    exit(1)

with open(gsc_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = data.get("rows", [])
print(f"Total rows in GSC data: {len(rows)}")

# Aggregate by page
page_stats = defaultdict(lambda: {"clicks": 0, "impressions": 0, "queries": set(), "ctr_sum": 0.0, "pos_sum": 0.0, "count": 0})
query_stats = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pages": set(), "ctr_sum": 0.0, "pos_sum": 0.0, "count": 0})

for row in rows:
    keys = row.get("keys", [])
    if len(keys) < 2:
        continue
    query = keys[0]
    page = keys[1]
    # date is keys[2] if present
    
    clicks = row.get("clicks", 0)
    impressions = row.get("impressions", 0)
    ctr = row.get("ctr", 0.0)
    position = row.get("position", 0.0)
    
    # Page stats
    page_stats[page]["clicks"] += clicks
    page_stats[page]["impressions"] += impressions
    page_stats[page]["queries"].add(query)
    page_stats[page]["ctr_sum"] += ctr
    page_stats[page]["pos_sum"] += position
    page_stats[page]["count"] += 1
    
    # Query stats
    query_stats[query]["clicks"] += clicks
    query_stats[query]["impressions"] += impressions
    query_stats[query]["pages"].add(page)
    query_stats[query]["ctr_sum"] += ctr
    query_stats[query]["pos_sum"] += position
    query_stats[query]["count"] += 1

print("\n=== TOP PAGES BY IMPRESSIONS ===")
sorted_pages = sorted(page_stats.items(), key=lambda x: x[1]["impressions"], reverse=True)
for p, stats in sorted_pages[:15]:
    avg_pos = stats["pos_sum"] / stats["count"]
    print(f"Page: {p}\n  Clicks: {stats['clicks']}, Impressions: {stats['impressions']}, Queries: {len(stats['queries'])}, Avg Pos: {avg_pos:.1f}")

print("\n=== TOP QUERIES BY IMPRESSIONS ===")
sorted_queries = sorted(query_stats.items(), key=lambda x: x[1]["impressions"], reverse=True)
for q, stats in sorted_queries[:20]:
    avg_pos = stats["pos_sum"] / stats["count"]
    print(f"Query: {q}\n  Clicks: {stats['clicks']}, Impressions: {stats['impressions']}, Pages: {len(stats['pages'])}, Avg Pos: {avg_pos:.1f}")

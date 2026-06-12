import json
import os

base_dir = "/home/ubuntu/work/active-oahu-static/site/_seo/data"

def print_summary():
    print("=================== GA4 PAGEVIEWS (30D) ===================")
    p_path = os.path.join(base_dir, "google-analytics/ga4_pageviews_30d.json")
    if os.path.exists(p_path):
        with open(p_path) as f:
            data = json.load(f)
            rows = data.get("rows", [])
            print(f"Total landing pages/paths tracked: {len(rows)}")
            for r in rows[:15]:
                path = r["dimensionValues"][0]["value"]
                sessions = r["metricValues"][0]["value"]
                print(f"  {path}: {sessions} sessions")
                
    print("\n=================== GA4 TRAFFIC SOURCES (30D) ===================")
    t_path = os.path.join(base_dir, "google-analytics/ga4_traffic-source_30d.json")
    if os.path.exists(t_path):
        with open(t_path) as f:
            data = json.load(f)
            for r in data.get("rows", [])[:10]:
                src = r["dimensionValues"][0]["value"]
                sessions = r["metricValues"][0]["value"]
                print(f"  {src}: {sessions} sessions")
                
    print("\n=================== GA4 CONVERSIONS (90D) ===================")
    c_path = os.path.join(base_dir, "google-analytics/ga4_conversions_90d.json")
    if os.path.exists(c_path):
        with open(c_path) as f:
            data = json.load(f)
            rows = data.get("rows", [])
            print(f"Total conversions recorded: {len(rows)}")
            conversions_by_event = {}
            for r in rows:
                event = r["dimensionValues"][0]["value"]
                path = r["dimensionValues"][1]["value"]
                val = float(r["metricValues"][0]["value"])
                conversions_by_event[event] = conversions_by_event.get(event, 0) + val
            for ev, val in conversions_by_event.items():
                print(f"  Event '{ev}': {val} conversions")
            print("  Top conversion landing pages:")
            for r in sorted(rows, key=lambda x: float(x["metricValues"][0]["value"]), reverse=True)[:10]:
                event = r["dimensionValues"][0]["value"]
                path = r["dimensionValues"][1]["value"]
                val = r["metricValues"][0]["value"]
                print(f"    {path} ({event}): {val}")

    print("\n=================== GA4 USER BEHAVIOR (30D) ===================")
    b_path = os.path.join(base_dir, "google-analytics/ga4_user-behavior_30d.json")
    if os.path.exists(b_path):
        with open(b_path) as f:
            data = json.load(f)
            for r in data.get("rows", [])[:15]:
                path = r["dimensionValues"][0]["value"]
                sess = r["metricValues"][0]["value"]
                bounce = float(r["metricValues"][1]["value"]) * 100
                duration = float(r["metricValues"][2]["value"])
                conv = r["metricValues"][3]["value"]
                print(f"  {path}: {sess} sessions, Bounce: {bounce:.1f}%, Duration: {duration:.1f}s, Conv: {conv}")
                
    print("\n=================== GA4 DEVICE SPLIT (30D) ===================")
    d_path = os.path.join(base_dir, "google-analytics/ga4_device_30d.json")
    if os.path.exists(d_path):
        with open(d_path) as f:
            data = json.load(f)
            for r in data.get("rows", []):
                dev = r["dimensionValues"][0]["value"]
                sess = r["metricValues"][0]["value"]
                print(f"  {dev}: {sess} sessions")

    print("\n=================== GSC TOP QUERIES (6MO) ===================")
    q_path = os.path.join(base_dir, "search-console/gsc_top-queries_6mo.json")
    if os.path.exists(q_path):
        with open(q_path) as f:
            data = json.load(f)
            rows = data.get("rows", [])
            for r in rows[:15]:
                q = r["keys"][0]
                clicks = r["clicks"]
                impr = r["impressions"]
                ctr = r["ctr"] * 100
                pos = r["position"]
                print(f"  '{q}': {clicks} Clicks, {impr} Impr, CTR: {ctr:.1f}%, Pos: {pos:.1f}")

    print("\n=================== GSC TOP PAGES (6MO) ===================")
    pg_path = os.path.join(base_dir, "search-console/gsc_top-pages_6mo.json")
    if os.path.exists(pg_path):
        with open(pg_path) as f:
            data = json.load(f)
            rows = data.get("rows", [])
            for r in rows[:15]:
                p = r["keys"][0]
                clicks = r["clicks"]
                impr = r["impressions"]
                ctr = r["ctr"] * 100
                pos = r["position"]
                print(f"  {p}: {clicks} Clicks, {impr} Impr, CTR: {ctr:.1f}%, Pos: {pos:.1f}")

if __name__ == "__main__":
    print_summary()

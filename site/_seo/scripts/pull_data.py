import urllib.request
import urllib.parse
import json
import os
from datetime import datetime, timedelta

# Load Google credentials dynamically
import json
with open("/home/ubuntu/.google_oauth_creds.json") as f_creds:
    creds_data = json.load(f_creds)
client_id = creds_data["client_id"]
client_secret = creds_data["client_secret"]
refresh_token = creds_data["refresh_token"]

# Setup output dirs
base_dir = "/home/ubuntu/work/active-oahu-static/site/_seo/data"
ga_dir = os.path.join(base_dir, "google-analytics")
gsc_dir = os.path.join(base_dir, "search-console")
os.makedirs(ga_dir, exist_ok=True)
os.makedirs(gsc_dir, exist_ok=True)

def refresh_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read().decode("utf-8"))
            return tokens.get("access_token")
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return None

def run_ga4_report(access_token, filename, body):
    property_id = "289642224"
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            filepath = os.path.join(ga_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Saved GA4 report to {filepath}")
    except Exception as e:
        print(f"Error calling GA4 API for {filename}: {e}")
        if hasattr(e, "read"):
            print(e.read().decode("utf-8"))

def run_gsc_report(access_token, filename, body):
    site_url = "sc-domain:activeoahutours.com"
    encoded_site = urllib.parse.quote_plus(site_url)
    url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            filepath = os.path.join(gsc_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Saved GSC report to {filepath}")
    except Exception as e:
        print(f"Error calling GSC API for {filename}: {e}")
        if hasattr(e, "read"):
            print(e.read().decode("utf-8"))

def main():
    token = refresh_access_token()
    if not token:
        print("Failed to authenticate.")
        return
        
    print("OAuth Authenticated. Pulling reports...")
    
    # 1. ga4_pageviews_30d.json (sessions by page, last 30 days, top 50)
    ga4_pageviews_body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
        "metrics": [{"name": "sessions"}],
        "limit": 50
    }
    run_ga4_report(token, "ga4_pageviews_30d.json", ga4_pageviews_body)
    
    # 2. ga4_traffic-source_30d.json (sessions by source/medium, last 30 days)
    ga4_traffic_body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "sessionSourceMedium"}],
        "metrics": [{"name": "sessions"}],
        "limit": 50
    }
    run_ga4_report(token, "ga4_traffic-source_30d.json", ga4_traffic_body)
    
    # 3. ga4_conversions_90d.json (conversions by event and page, last 90 days)
    ga4_conversions_body = {
        "dateRanges": [{"startDate": "90daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "eventName"}, {"name": "pagePath"}],
        "metrics": [{"name": "conversions"}],
        "limit": 100
    }
    run_ga4_report(token, "ga4_conversions_90d.json", ga4_conversions_body)
    
    # 4. ga4_user-behavior_30d.json (bounce rate, duration, conversions by page, last 30 days)
    ga4_behavior_body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "bounceRate"},
            {"name": "averageSessionDuration"},
            {"name": "conversions"}
        ],
        "limit": 100
    }
    run_ga4_report(token, "ga4_user-behavior_30d.json", ga4_behavior_body)
    
    # 5. ga4_device_30d.json (sessions by device, last 30 days)
    ga4_device_body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "deviceCategory"}],
        "metrics": [{"name": "sessions"}],
        "limit": 10
    }
    run_ga4_report(token, "ga4_device_30d.json", ga4_device_body)
    
    # Calculate dates for Search Console (last 6 months, GSC lag: 2-3 days so end on 2 days ago)
    end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=182)).strftime("%Y-%m-%d")
    
    print(f"GSC date range: {start_date} to {end_date}")
    
    # 6. gsc_top-queries_6mo.json (top 100 queries)
    gsc_queries_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 100
    }
    run_gsc_report(token, "gsc_top-queries_6mo.json", gsc_queries_body)
    
    # 7. gsc_top-pages_6mo.json (top 50 pages)
    gsc_pages_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": 50
    }
    run_gsc_report(token, "gsc_top-pages_6mo.json", gsc_pages_body)
    
    # 8. gsc_ctr-analysis_6mo.json (top 500 queries to analyze CTR by position)
    gsc_ctr_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 500
    }
    run_gsc_report(token, "gsc_ctr-analysis_6mo.json", gsc_ctr_body)

if __name__ == "__main__":
    main()

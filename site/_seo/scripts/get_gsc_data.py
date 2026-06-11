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
        print(f"Error refreshing access token: {e}")
        return None

def query_gsc(access_token):
    site_url = "sc-domain:activeoahutours.com"
    # URL encode the site_url to make sure it is valid in the request URL path
    encoded_site = urllib.parse.quote_plus(site_url)
    url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    
    # Dates: last 6 months (approx 180 days)
    end_date = "2026-06-11"
    start_date = "2025-12-11"
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query", "page", "date"],
        "dimensionFilterGroups": [
            {
                "filters": [
                    {
                        "dimension": "page",
                        "operator": "contains",
                        "expression": "/ja/"
                    }
                ]
            }
        ],
        "rowLimit": 25000
    }
    
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
            print("GSC API Query Success!")
            output_dir = "/home/ubuntu/work/active-oahu-static/site/_seo/raw"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "gsc_ja_search_analytics.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved GSC data to {output_path}")
            return data
    except Exception as e:
        print(f"Error calling GSC API: {e}")
        if hasattr(e, "read"):
            print(e.read().decode("utf-8"))
        return None

if __name__ == "__main__":
    access_token = refresh_access_token()
    if access_token:
        print("Access token refreshed successfully.")
        query_gsc(access_token)
    else:
        print("Failed to obtain access token.")
